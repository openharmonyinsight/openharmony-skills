"""Chrome DevTools utilities."""

import subprocess
import logging
from typing import Optional
from pathlib import Path
import platform


class ChromeDevTools:
    """
    Chrome DevTools integration utilities.

    Provides methods to open Chrome DevTools and manage debugging sessions.
    """

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize Chrome DevTools utilities.

        Args:
            logger: Optional logger instance
        """
        self.logger = logger or logging.getLogger(__name__)
        self.system = platform.system()

    def find_chrome(self) -> Optional[str]:
        """
        Find Chrome browser executable.

        Returns:
            Path to Chrome executable or None
        """
        possible_paths = []

        if self.system == "Darwin":  # macOS
            possible_paths = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chromium.app/Contents/MacOS/Chromium",
            ]
        elif self.system == "Linux":
            possible_paths = [
                "/usr/bin/google-chrome",
                "/usr/bin/chromium-browser",
                "/usr/bin/chromium",
            ]
        elif self.system == "Windows":
            possible_paths = [
                "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
            ]

        for path in possible_paths:
            if Path(path).exists():
                return path

        # Try to find in PATH
        import shutil

        chrome_path = shutil.which("google-chrome") or shutil.which("chrome")
        if chrome_path:
            return chrome_path

        return None

    def open_devtools(self, local_port: int = 9222) -> bool:
        """
        Open Chrome DevTools with inspect page.

        Args:
            local_port: Local port for device connection

        Returns:
            True if successful
        """
        url = "chrome://inspect/#devices"

        try:
            if self.system == "Darwin":  # macOS
                # Use 'open' command on macOS
                subprocess.run(
                    ["open", "-a", "Google Chrome", url],
                    check=False,
                    capture_output=True,
                )
            elif self.system == "Linux":
                # Try to open with xdg-open
                subprocess.run(
                    ["xdg-open", url],
                    check=False,
                    capture_output=True,
                )
            elif self.system == "Windows":
                # Use start command on Windows
                subprocess.run(
                    ["start", "chrome", url],
                    shell=True,
                    check=False,
                    capture_output=True,
                )
            else:
                self.logger.warning(f"Unsupported system: {self.system}")
                return False

            self.logger.info(f"Opened Chrome DevTools: {url}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to open Chrome DevTools: {e}")
            return False

    def test_connection(self, local_port: int = 9222, timeout: int = 5) -> bool:
        """
        Test connection to Chrome DevTools endpoint.

        Args:
            local_port: Local port number
            timeout: Request timeout in seconds

        Returns:
            True if connection successful
        """
        try:
            import urllib.request
            import json

            url = f"http://127.0.0.1:{local_port}/json"
            self.logger.debug(f"Testing connection to: {url}")

            with urllib.request.urlopen(url, timeout=timeout) as response:
                data = json.loads(response.read().decode())

                # Check if response contains DevTools endpoints
                for item in data:
                    if "webSocketDebuggerUrl" in item:
                        self.logger.info("DevTools connection test successful")
                        return True

                self.logger.warning("DevTools endpoint not found in response")
                return False

        except urllib.error.URLError as e:
            self.logger.warning(f"Connection test failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Connection test error: {e}")
            return False

    def get_debug_targets(self, local_port: int = 9222) -> list:
        """
        Get list of debug targets from Chrome DevTools endpoint.

        Args:
            local_port: Local port number

        Returns:
            List of debug target dictionaries
        """
        try:
            import urllib.request
            import json

            url = f"http://127.0.0.1:{local_port}/json"

            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode())
                return data

        except Exception as e:
            self.logger.error(f"Failed to get debug targets: {e}")
            return []
