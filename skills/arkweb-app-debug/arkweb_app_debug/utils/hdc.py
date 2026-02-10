"""HDC (HarmonyOS Device Connector) wrapper."""

import subprocess
import logging
from typing import List, Optional, Dict
from dataclasses import dataclass


@dataclass
class DeviceInfo:
    """Device information."""

    device_id: str
    model: str
    android_version: str
    harmony_version: Optional[str] = None
    ip_address: Optional[str] = None
    manufacturer: Optional[str] = None
    device_name: Optional[str] = None

    def __str__(self) -> str:
        """String representation."""
        return (
            f"Device(id={self.device_id}, model={self.model}, "
            f"android={self.android_version}, harmony={self.harmony_version})"
        )


class HDCWrapper:
    """
    Wrapper for HDC (HarmonyOS Device Connector) commands.

    Provides a Python interface to HDC tool with error handling and timeout support.
    """

    def __init__(
        self,
        hdc_cmd: str = "hdc",
        timeout: int = 10,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize HDC wrapper.

        Args:
            hdc_cmd: HDC command path (default: "hdc")
            timeout: Command timeout in seconds
            logger: Optional logger instance
        """
        self.hdc_cmd = hdc_cmd
        self.timeout = timeout
        self.logger = logger or logging.getLogger(__name__)

    def _run_command(
        self,
        args: List[str],
        capture_output: bool = True,
        check: bool = False,
        timeout: Optional[int] = None,
    ) -> subprocess.CompletedProcess:
        """
        Run HDC command.

        Args:
            args: Command arguments
            capture_output: Capture stdout/stderr
            check: Raise exception on non-zero exit
            timeout: Override default timeout

        Returns:
            Completed process result

        Raises:
            subprocess.TimeoutExpired: Command timeout
            subprocess.CalledProcessError: Command failed (if check=True)
        """
        cmd = [self.hdc_cmd] + args
        timeout = timeout or self.timeout

        self.logger.debug(f"Running command: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=capture_output,
                text=True,
                timeout=timeout,
                check=check,
            )
            return result
        except subprocess.TimeoutExpired:
            self.logger.error(f"Command timeout: {' '.join(cmd)}")
            raise
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed: {e.stderr}")
            raise

    def check_hdc(self) -> bool:
        """
        Check if HDC tool is available.

        Returns:
            True if HDC is available
        """
        try:
            result = self._run_command(["--version"], timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def list_devices(self) -> List[str]:
        """
        List all connected devices.

        Returns:
            List of device IDs
        """
        try:
            result = self._run_command(["list", "targets"])
            if result.returncode != 0:
                return []

            device_ids = [
                line.strip()
                for line in result.stdout.strip().split("\n")
                if line.strip()
            ]
            return device_ids
        except subprocess.TimeoutExpired:
            self.logger.error("Timeout listing devices")
            return []

    def shell_command(
        self, device_id: str, command: str, timeout: Optional[int] = None
    ) -> str:
        """
        Execute shell command on device.

        Args:
            device_id: Target device ID
            command: Shell command to execute
            timeout: Command timeout

        Returns:
            Command output
        """
        result = self._run_command(
            ["-t", device_id, "shell", command],
            timeout=timeout or self.timeout,
        )
        return result.stdout.strip()

    def get_device_prop(self, device_id: str, prop: str) -> str:
        """
        Get device property.

        Args:
            device_id: Target device ID
            prop: Property name (e.g., "ro.product.model")

        Returns:
            Property value
        """
        return self.shell_command(device_id, f"getprop {prop}")

    def start_app(
        self, device_id: str, package_name: str, ability_name: str
    ) -> bool:
        """
        Start application.

        Args:
            device_id: Target device ID
            package_name: Application package name
            ability_name: Ability name

        Returns:
            True if successful
        """
        try:
            result = self._run_command(
                ["-t", device_id, "shell", "aa", "start", "-a", ability_name, package_name],
                check=False,
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False

    def stop_app(self, device_id: str, package_name: str) -> bool:
        """
        Stop application.

        Args:
            device_id: Target device ID
            package_name: Application package name

        Returns:
            True if successful
        """
        try:
            result = self._run_command(
                ["-t", device_id, "shell", "aa", "force-stop", package_name],
                check=False,
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False

    def is_app_installed(self, device_id: str, package_name: str) -> bool:
        """
        Check if application is installed.

        Args:
            device_id: Target device ID
            package_name: Application package name

        Returns:
            True if installed
        """
        try:
            result = self._run_command(
                ["-t", device_id, "shell", "bm", "dump", "-n", package_name],
                check=False,
            )
            return result.returncode == 0 and package_name in result.stdout
        except subprocess.TimeoutExpired:
            return False

    def install_app(self, device_id: str, hap_path: str) -> bool:
        """
        Install application from HAP file.

        Args:
            device_id: Target device ID
            hap_path: Path to HAP file

        Returns:
            True if successful
        """
        try:
            result = self._run_command(
                ["-t", device_id, "install", hap_path],
                timeout=60,  # Installation may take longer
                check=False,
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False

    def uninstall_app(self, device_id: str, package_name: str) -> bool:
        """
        Uninstall application.

        Args:
            device_id: Target device ID
            package_name: Application package name

        Returns:
            True if successful
        """
        try:
            result = self._run_command(
                ["-t", device_id, "uninstall", package_name],
                check=False,
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False

    def create_port_forward(
        self, device_id: str, local_port: int, remote_spec: str
    ) -> bool:
        """
        Create port forwarding.

        Args:
            device_id: Target device ID
            local_port: Local port number
            remote_spec: Remote specification (e.g., "tcpabstract:webview_devtools_remote_8888")

        Returns:
            True if successful
        """
        try:
            result = self._run_command(
                ["fport", f"tcp:{local_port}", remote_spec],
                check=False,
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False

    def remove_port_forward(self, device_id: str, local_port: int) -> bool:
        """
        Remove port forwarding.

        Args:
            device_id: Target device ID
            local_port: Local port number

        Returns:
            True if successful
        """
        try:
            result = self._run_command(
                ["fport", "rm", f"tcp:{local_port}"],
                check=False,
            )
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False

    def remove_all_port_forwards(self, device_id: str) -> bool:
        """
        Remove all port forwards.

        Args:
            device_id: Target device ID

        Returns:
            True if successful
        """
        try:
            # List all forwards first
            list_result = self._run_command(
                ["fport", "ls"],
                check=False,
            )

            if list_result.returncode != 0:
                return False

            # Parse and remove each forward
            import re
            forwards = list_result.stdout.strip().split('\n')
            for forward in forwards:
                # Extract local port from format: "tcp:9222 ..."
                match = re.search(r'tcp:(\d+)', forward)
                if match:
                    local_port = match.group(1)
                    self._run_command(
                        ["fport", "rm", f"tcp:{local_port}"],
                        check=False,
                    )

            return True
        except subprocess.TimeoutExpired:
            return False

    def list_port_forwards(self, device_id: str) -> List[Dict[str, any]]:
        """
        List all port forwards.

        Args:
            device_id: Target device ID

        Returns:
            List of forward information dictionaries
        """
        try:
            result = self._run_command(
                ["fport", "ls"],
                check=False,
            )

            if result.returncode != 0:
                return []

            forwards = []
            import re

            for line in result.stdout.strip().split("\n"):
                # Parse line format: "tcp:9222 ..."
                match = re.search(r"tcp:(\d+)", line)
                if match:
                    local_port = int(match.group(1))
                    forwards.append({
                        "local_port": local_port,
                        "raw": line.strip(),
                    })

            return forwards
        except subprocess.TimeoutExpired:
            return []
