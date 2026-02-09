"""Port forward manager with resource cleanup."""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Set

from arkweb_app_debug.utils.hdc import HDCWrapper
from arkweb_app_debug.utils.logger import log_info, log_success, log_warn, log_error


class PortForwardManager:
    """
    Port forward management with lifecycle tracking and cleanup.

    This manager tracks all port forwards created by arkweb-app-debug and
    provides automatic cleanup of orphaned forwards.
    """

    def __init__(
        self,
        device_id: str,
        hdc_cmd: str = "hdc",
        timeout: int = 10,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize port forward manager.

        Args:
            device_id: Target device ID
            hdc_cmd: HDC command path
            timeout: Command timeout
            logger: Optional logger instance
        """
        self.device_id = device_id
        self.hdc = HDCWrapper(hdc_cmd=hdc_cmd, timeout=timeout, logger=logger)
        self.logger = logger or logging.getLogger(__name__)

        # State file for tracking forwards
        self.state_file = Path.home() / ".arkweb-app-debug" / "sessions.json"
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

    def find_webview_socket(self, timeout: int = 15) -> Optional[str]:
        """
        动态查找 Web 调试 socket

        Args:
            timeout: 查找超时时间（秒）

        Returns:
            Socket 名称或 None
        """
        import time
        import re

        start_time = time.time()
        package_name = self._get_package_name_from_state()

        while time.time() - start_time < timeout:
            # 方法1: 查找明确的 webview_devtools socket
            result = self.hdc.shell_command(
                self.device_id, "cat /proc/net/unix | grep webview_devtools_remote"
            )

            if result and "webview_devtools_remote" in result:
                # 解析所有 socket
                for line in result.split('\n'):
                    match = re.search(r'@(\S+webview_devtools_remote\S+)', line)
                    if match:
                        socket_name = match.group(1)
                        self.logger.info(f"Found socket: {socket_name}")
                        return socket_name

            # 方法2: 通过应用 PID 查找
            if package_name:
                pid_result = self.hdc.shell_command(
                    self.device_id, f"ps -A | grep {package_name} | grep -v grep"
                )

                if pid_result:
                    pid_match = re.search(r'\s+(\d+)', pid_result)
                    if pid_match:
                        app_pid = pid_match.group(1)
                        self.logger.debug(f"App PID: {app_pid}")

                        # 查找与 PID 相关的 socket
                        socket_result = self.hdc.shell_command(
                            self.device_id, f"cat /proc/net/unix | grep {app_pid}"
                        )

                        if socket_result:
                            for line in socket_result.split('\n'):
                                if 'webview' in line.lower() or 'devtools' in line.lower():
                                    socket_match = re.search(r'@(\S+)', line)
                                    if socket_match:
                                        socket_name = socket_match.group(1)
                                        self.logger.info(f"Found socket via PID: {socket_name}")
                                        return socket_name

            # 未找到，等待后重试
            time.sleep(2)

        self.logger.warning("Socket not found within timeout")
        return None

    def create_forward(
        self,
        device_port: int,
        local_port: int,
        session_id: str,
        socket_path: Optional[str] = None,
        wait_for_socket: bool = True,
    ) -> bool:
        """
        创建端口转发（支持动态 socket 查找）

        Args:
            device_port: Device debug port
            local_port: Local port number
            session_id: Session ID for tracking
            socket_path: Optional socket path (default: auto-detect)
            wait_for_socket: Whether to wait for socket creation

        Returns:
            True if successful
        """
        log_info(
            self.logger,
            f"Creating port forward: {device_port} -> localhost:{local_port}",
        )

        # Step 1: Remove old forward on this port
        self.remove_forward(local_port)

        # Step 2: Determine socket path
        if not socket_path:
            if wait_for_socket:
                log_info(self.logger, "Searching for debug socket...")
                socket_path = self.find_webview_socket(timeout=15)

            if not socket_path:
                socket_path = f"tcpabstract:webview_devtools_remote_{device_port}"
                log_warn(self.logger, f"Using default socket path: {socket_path}")

        # Step 3: Parse socket type and name
        forward_spec = self._parse_socket_spec(socket_path)

        # Step 4: Create new forward
        if not self.hdc.create_port_forward(self.device_id, local_port, forward_spec):
            log_error(self.logger, "Failed to create port forward")
            return False

        # Step 5: Register in state file
        self._register_forward(session_id, local_port, device_port, socket_path)

        log_success(self.logger, f"Port forward created: localhost:{local_port}")
        return True

    def _parse_socket_spec(self, socket_path: str) -> str:
        """
        解析 socket 路径为 HDC 转发规范

        Args:
            socket_path: Socket 路径

        Returns:
            HDC 转发规范字符串
        """
        if socket_path.startswith('/'):
            # 文件系统 socket
            return f"localfilesystem:{socket_path}"
        else:
            # 抽象 socket（默认）
            if not socket_path.startswith('localabstract:') and not socket_path.startswith('localfilesystem:'):
                return f"localabstract:{socket_path}"
            return socket_path

    def _get_package_name_from_state(self) -> Optional[str]:
        """从状态文件获取包名"""
        state = self._load_state()
        for session_id, session_data in state.get("sessions", {}).items():
            return session_data.get("package")
        return None

    def remove_forward(self, local_port: int) -> bool:
        """
        Remove port forward and unregister from state.

        Args:
            local_port: Local port number

        Returns:
            True if successful
        """
        log_info(self.logger, f"Removing port forward: localhost:{local_port}")

        # Remove from HDC
        self.hdc.remove_port_forward(self.device_id, local_port)

        # Unregister from state file
        self._unregister_forward(local_port)

        return True

    def remove_all_forwards(self) -> int:
        """
        Remove all arkweb-app-debug port forwards.

        Returns:
            Number of forwards removed
        """
        log_info(self.logger, "Removing all arkweb-app-debug port forwards")

        forwards = self.list_forwards()
        count = 0

        for forward in forwards:
            if self._is_arkweb_forward(forward):
                if self.remove_forward(forward["local_port"]):
                    count += 1

        log_success(self.logger, f"Removed {count} port forward(s)")
        return count

    def list_forwards(self) -> List[Dict]:
        """
        List all port forwards on the device.

        Returns:
            List of forward information dictionaries
        """
        return self.hdc.list_port_forwards(self.device_id)

    def cleanup_orphans(self) -> int:
        """
        Clean up orphaned port forwards.

        Orphaned forwards are those that exist on the device but are not
        registered in the state file (e.g., from crashed sessions).

        Returns:
            Number of orphaned forwards cleaned up
        """
        log_info(self.logger, "Cleaning up orphaned port forwards...")

        # Get current forwards from device
        current_forwards = self.list_forwards()
        current_ports = {f["local_port"] for f in current_forwards}

        # Get registered forwards from state file
        registered_ports = self._get_registered_forwards()

        # Find orphaned forwards
        orphan_ports = current_ports - registered_ports

        # Filter to only arkweb-app-debug ports
        orphan_ports = {p for p in orphan_ports if self._is_arkweb_port(p)}

        # Clean up orphans
        count = 0
        for port in orphan_ports:
            log_warn(self.logger, f"Cleaning up orphaned forward: localhost:{port}")
            if self.remove_forward(port):
                count += 1

        if count > 0:
            log_success(self.logger, f"Cleaned up {count} orphaned forward(s)")
        else:
            log_info(self.logger, "No orphaned forwards found")

        return count

    def is_forward_active(self, local_port: int) -> bool:
        """
        Check if port forward is active.

        Args:
            local_port: Local port number

        Returns:
            True if active
        """
        forwards = self.list_forwards()
        return any(f["local_port"] == local_port for f in forwards)

    def find_free_port(self, start_port: int = 9222) -> int:
        """
        Find an available local port.

        Args:
            start_port: Starting port number

        Returns:
            Available port number
        """
        import socket

        for port in range(start_port, start_port + 100):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(("127.0.0.1", port))
                    return port
            except OSError:
                continue

        log_error(self.logger, "No available port found")
        return start_port

    def _is_arkweb_forward(self, forward: Dict) -> bool:
        """
        Check if forward was created by arkweb-app-debug.

        Args:
            forward: Forward information dictionary

        Returns:
            True if arkweb-app-debug forward
        """
        port = forward["local_port"]
        return self._is_arkweb_port(port)

    def _is_arkweb_port(self, port: int) -> bool:
        """
        Check if port is in arkweb-app-debug range.

        Args:
            port: Port number

        Returns:
            True if in range
        """
        # ArkWeb-app-debug uses ports 9220-9299
        return 9220 <= port <= 9299

    def _load_state(self) -> Dict:
        """Load state file."""
        if not self.state_file.exists():
            return {"sessions": {}, "forwards": {}}

        try:
            with open(self.state_file, "r") as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load state file: {e}")
            return {"sessions": {}, "forwards": {}}

    def _save_state(self, state: Dict) -> None:
        """Save state file."""
        try:
            with open(self.state_file, "w") as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save state file: {e}")

    def _register_forward(
        self, session_id: str, local_port: int, device_port: int, socket_path: str
    ) -> None:
        """
        Register port forward in state file.

        Args:
            session_id: Session ID
            local_port: Local port
            device_port: Device port
            socket_path: Socket path
        """
        state = self._load_state()

        state["forwards"][str(local_port)] = {
            "session_id": session_id,
            "device_port": device_port,
            "socket_path": socket_path,
            "created_at": datetime.now().isoformat(),
        }

        self._save_state(state)
        self.logger.debug(f"Registered forward: localhost:{local_port}")

    def _unregister_forward(self, local_port: int) -> None:
        """
        Unregister port forward from state file.

        Args:
            local_port: Local port
        """
        state = self._load_state()
        state["forwards"].pop(str(local_port), None)
        self._save_state(state)
        self.logger.debug(f"Unregistered forward: localhost:{local_port}")

    def _get_registered_forwards(self) -> Set[int]:
        """
        Get set of registered port numbers.

        Returns:
            Set of port numbers
        """
        state = self._load_state()
        return set(int(port) for port in state["forwards"].keys())

    def print_forward_list(self) -> None:
        """Print formatted list of port forwards."""
        forwards = self.list_forwards()

        if not forwards:
            log_info(self.logger, "No port forwards")
            return

        log_info(self.logger, "Active port forwards:")
        print("-" * 80)

        for forward in forwards:
            port = forward["local_port"]
            registered = str(port) in self._get_registered_forwards()
            status = "✓" if registered else "⚠ (orphan)"
            print(f"  localhost:{port} {status}")

        print("-" * 80)
