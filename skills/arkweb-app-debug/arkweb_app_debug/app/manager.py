"""Application manager."""

import logging
import time
from typing import Optional
from pathlib import Path

from arkweb_app_debug.utils.hdc import HDCWrapper
from arkweb_app_debug.utils.logger import log_info, log_success, log_warn, log_error


class AppManager:
    """
    Application management for ArkWeb apps.

    Provides app installation, launch, stop, and status checking.
    """

    def __init__(
        self,
        device_id: str,
        package: str,
        bundle: Optional[str] = None,
        hdc_cmd: str = "hdc",
        timeout: int = 10,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize application manager.

        Args:
            device_id: Target device ID
            package: Application package name
            bundle: Ability name (optional)
            hdc_cmd: HDC command path
            timeout: Command timeout
            logger: Optional logger instance
        """
        self.device_id = device_id
        self.package = package
        self.bundle = bundle
        self.hdc = HDCWrapper(hdc_cmd=hdc_cmd, timeout=timeout, logger=logger)
        self.logger = logger or logging.getLogger(__name__)

    def is_installed(self) -> bool:
        """
        Check if application is installed.

        Returns:
            True if installed
        """
        return self.hdc.is_app_installed(self.device_id, self.package)

    def install(self, hap_path: str) -> bool:
        """
        Install application from HAP file.

        Args:
            hap_path: Path to HAP file

        Returns:
            True if successful
        """
        path = Path(hap_path).expanduser()

        if not path.exists():
            log_error(self.logger, f"HAP file not found: {hap_path}")
            return False

        log_info(self.logger, f"Installing application from: {hap_path}")

        if self.hdc.install_app(self.device_id, str(path)):
            log_success(self.logger, "Application installed successfully")
            return True

        log_error(self.logger, "Application installation failed")
        return False

    def uninstall(self) -> bool:
        """
        Uninstall application.

        Returns:
            True if successful
        """
        log_info(self.logger, f"Uninstalling application: {self.package}")

        if self.hdc.uninstall_app(self.device_id, self.package):
            log_success(self.logger, "Application uninstalled successfully")
            return True

        log_error(self.logger, "Application uninstallation failed")
        return False

    def start(self) -> bool:
        """
        Start application.

        Returns:
            True if successful
        """
        if not self.bundle:
            log_error(self.logger, "Bundle name not specified")
            return False

        log_info(self.logger, f"Starting application: {self.package}/{self.bundle}")

        if self.hdc.start_app(self.device_id, self.package, self.bundle):
            log_success(self.logger, "Application started successfully")
            return True

        log_error(self.logger, "Application failed to start")
        return False

    def stop(self) -> bool:
        """
        Stop application.

        Returns:
            True if successful
        """
        log_info(self.logger, f"Stopping application: {self.package}")

        if self.hdc.stop_app(self.device_id, self.package):
            log_success(self.logger, "Application stopped")
            return True

        log_warn(self.logger, "Application may not have been running")
        return True

    def restart(self) -> bool:
        """
        Restart application.

        Returns:
            True if successful
        """
        log_info(self.logger, f"Restarting application: {self.package}")

        # Stop the app
        self.stop()

        # Wait a moment
        time.sleep(2)

        # Start the app
        return self.start()

    def is_running(self) -> bool:
        """
        Check if application is currently running.

        Returns:
            True if running
        """
        # This is a simplified check - actual implementation may need
        # to query running processes
        try:
            output = self.hdc.shell_command(
                self.device_id, f"ps -A | grep {self.package}"
            )
            return self.package in output
        except Exception:
            return False

    def get_version(self) -> Optional[str]:
        """
        Get application version.

        Returns:
            Version string or None
        """
        try:
            # Try to get version from dumpsys
            output = self.hdc.shell_command(
                self.device_id, f"bm dump -n {self.package} | grep versionName"
            )

            import re

            match = re.search(r"versionName=([^\s]+)", output)
            if match:
                return match.group(1)

            return None

        except Exception as e:
            self.logger.debug(f"Failed to get app version: {e}")
            return None
