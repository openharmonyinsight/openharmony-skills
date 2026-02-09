"""Debug session management."""

import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from arkweb_app_debug.port.manager import PortForwardManager
from arkweb_app_debug.app.manager import AppManager
from arkweb_app_debug.utils.chrome import ChromeDevTools
from arkweb_app_debug.utils.logger import log_info, log_success, log_warn, log_error


@dataclass
class DebugConfig:
    """Debug configuration."""

    package: str
    bundle: Optional[str] = None
    hap_path: Optional[str] = None
    device_port: int = 8888
    local_port: int = 9222
    device_id: Optional[str] = None
    auto_start: bool = True
    auto_cleanup: bool = True


@dataclass
class DebugSession:
    """
    Debug session instance.

    Manages a single debugging session including app launch, port forwarding,
    and cleanup.
    """

    session_id: str
    config: DebugConfig
    device_id: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "created"
    local_port: int = 0
    device_port: int = 0
    websocket_url: str = ""

    def get_websocket_url(self) -> str:
        """Get WebSocket URL for DevTools connection."""
        return f"ws://localhost:{self.local_port}"


class SessionManager:
    """
    Manage multiple debug sessions.

    Provides session creation, tracking, and cleanup with automatic
    resource management.
    """

    def __init__(
        self,
        hdc_cmd: str = "hdc",
        timeout: int = 10,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize session manager.

        Args:
            hdc_cmd: HDC command path
            timeout: Command timeout
            logger: Optional logger instance
        """
        self.hdc_cmd = hdc_cmd
        self.timeout = timeout
        self.logger = logger or logging.getLogger(__name__)

        # State file
        self.state_file = Path.home() / ".arkweb-app-debug" / "sessions.json"
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

        # Active sessions
        self.active_sessions: Dict[str, DebugSession] = {}

    def create_session(self, config: DebugConfig) -> Optional[DebugSession]:
        """
        Create and start a new debug session.

        Args:
            config: Debug configuration

        Returns:
            DebugSession object or None
        """
        session_id = str(uuid.uuid4())[:8]
        session = DebugSession(
            session_id=session_id,
            config=config,
            device_id=config.device_id or "",
            status="created",
        )

        log_info(self.logger, f"Creating debug session: {session_id}")

        try:
            # Step 1: Select device
            from arkweb_app_debug.device.manager import DeviceManager

            device_mgr = DeviceManager(
                hdc_cmd=self.hdc_cmd, timeout=self.timeout, logger=self.logger
            )

            if config.device_id:
                device_id = config.device_id
            else:
                device_id = device_mgr.get_default_device()

            if not device_id:
                log_error(self.logger, "No device available")
                return None

            session.device_id = device_id

            # Step 2: Initialize managers
            port_mgr = PortForwardManager(
                device_id=device_id,
                hdc_cmd=self.hdc_cmd,
                timeout=self.timeout,
                logger=self.logger,
            )

            app_mgr = AppManager(
                device_id=device_id,
                package=config.package,
                bundle=config.bundle,
                hdc_cmd=self.hdc_cmd,
                timeout=self.timeout,
                logger=self.logger,
            )

            # Step 3: Check app installation
            if not app_mgr.is_installed():
                if config.hap_path:
                    log_info(self.logger, "Installing application...")
                    if not app_mgr.install(config.hap_path):
                        log_error(self.logger, "App installation failed")
                        return None
                else:
                    log_error(self.logger, "App not installed and no HAP path provided")
                    return None

            # Step 4: Stop app if running
            app_mgr.stop()
            time.sleep(1)

            # Step 5: Start app
            if config.auto_start:
                if not app_mgr.start():
                    log_error(self.logger, "Failed to start app")
                    return None

                # Wait for app to initialize
                log_info(self.logger, "Waiting for app initialization...")
                time.sleep(5)

            # Step 6: Clean up old forwards
            port_mgr.remove_forward(config.local_port)

            # Step 7: Wait for app to fully initialize (CRITICAL!)
            log_info(self.logger, "Waiting for Web component initialization...")
            time.sleep(10)

            # Step 8: Create port forward (with dynamic socket detection)
            if not port_mgr.create_forward(
                device_port=config.device_port,
                local_port=config.local_port,
                session_id=session_id,
                wait_for_socket=True,  # Enable dynamic socket finding
            ):
                log_error(self.logger, "Failed to create port forward")
                if config.auto_cleanup:
                    app_mgr.stop()
                return None

            session.local_port = config.local_port
            session.device_port = config.device_port
            session.status = "active"
            session.websocket_url = session.get_websocket_url()

            # Step 9: Test connection
            chrome = ChromeDevTools(logger=self.logger)
            time.sleep(2)  # Give socket time to initialize

            if chrome.test_connection(config.local_port):
                log_success(self.logger, "DevTools connection verified")
            else:
                log_warn(self.logger, "Could not verify DevTools connection")

            # Step 10: Register session
            self._register_session(session)
            self.active_sessions[session_id] = session

            log_success(self.logger, f"Debug session created: {session_id}")
            return session

        except Exception as e:
            log_error(self.logger, f"Failed to create session: {e}")
            if config.auto_cleanup:
                self.cleanup_session(session_id)
            return None

    def get_session(self, session_id: str) -> Optional[DebugSession]:
        """
        Get session by ID.

        Args:
            session_id: Session ID

        Returns:
            DebugSession object or None
        """
        return self.active_sessions.get(session_id)

    def list_sessions(self) -> List[DebugSession]:
        """
        List all active sessions.

        Returns:
            List of DebugSession objects
        """
        return list(self.active_sessions.values())

    def stop_session(self, session_id: str) -> bool:
        """
        Stop a debug session with cleanup.

        Args:
            session_id: Session ID

        Returns:
            True if successful
        """
        session = self.get_session(session_id)

        if not session:
            log_warn(self.logger, f"Session not found: {session_id}")
            return False

        log_info(self.logger, f"Stopping session: {session_id}")

        # Clean up resources
        if self.cleanup_session(session_id):
            session.status = "stopped"
            del self.active_sessions[session_id]
            log_success(self.logger, f"Session stopped: {session_id}")
            return True

        return False

    def cleanup_session(self, session_id: str) -> bool:
        """
        Clean up session resources.

        Args:
            session_id: Session ID

        Returns:
            True if successful
        """
        session = self.get_session(session_id)

        if not session:
            # Try to load from state file
            state = self._load_state()
            session_data = state["sessions"].get(session_id)
            if not session_data:
                return False

            device_id = session_data.get("device_id")
            local_port = session_data.get("local_port")
        else:
            device_id = session.device_id
            local_port = session.local_port

        # Remove port forward
        if device_id and local_port:
            port_mgr = PortForwardManager(
                device_id=device_id,
                hdc_cmd=self.hdc_cmd,
                timeout=self.timeout,
                logger=self.logger,
            )
            port_mgr.remove_forward(local_port)

        # Unregister session
        self._unregister_session(session_id)

        return True

    def cleanup_all_sessions(self) -> int:
        """
        Clean up all sessions.

        Returns:
            Number of sessions cleaned up
        """
        log_info(self.logger, "Cleaning up all sessions...")

        session_ids = list(self.active_sessions.keys())
        count = 0

        for session_id in session_ids:
            if self.stop_session(session_id):
                count += 1

        log_success(self.logger, f"Cleaned up {count} session(s)")
        return count

    def cleanup_expired_sessions(self, max_age_hours: int = 24) -> int:
        """
        Clean up expired sessions.

        Args:
            max_age_hours: Maximum session age in hours

        Returns:
            Number of sessions cleaned up
        """
        log_info(self.logger, f"Cleaning up sessions older than {max_age_hours} hours...")

        state = self._load_state()
        now = datetime.now()
        count = 0

        for session_id, session_data in state["sessions"].items():
            created_at = datetime.fromisoformat(session_data["created_at"])
            age_hours = (now - created_at).total_seconds() / 3600

            if age_hours > max_age_hours:
                log_info(self.logger, f"Cleaning up expired session: {session_id}")
                if self.cleanup_session(session_id):
                    count += 1

        if count > 0:
            log_success(self.logger, f"Cleaned up {count} expired session(s)")
        else:
            log_info(self.logger, "No expired sessions found")

        return count

    def _register_session(self, session: DebugSession) -> None:
        """Register session in state file."""
        state = self._load_state()

        state["sessions"][session.session_id] = {
            "session_id": session.session_id,
            "device_id": session.device_id,
            "package": session.config.package,
            "local_port": session.local_port,
            "device_port": session.device_port,
            "created_at": session.created_at,
            "status": session.status,
        }

        self._save_state(state)
        self.logger.debug(f"Registered session: {session.session_id}")

    def _unregister_session(self, session_id: str) -> None:
        """Unregister session from state file."""
        state = self._load_state()
        state["sessions"].pop(session_id, None)
        self._save_state(state)
        self.logger.debug(f"Unregistered session: {session_id}")

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
