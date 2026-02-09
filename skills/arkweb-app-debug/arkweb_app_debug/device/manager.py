"""Device manager."""

import logging
import re
from typing import List, Optional
from dataclasses import dataclass

from arkweb_app_debug.utils.hdc import HDCWrapper
from arkweb_app_debug.utils.logger import log_info, log_success, log_warn, log_error


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
            f"android={self.android_version}, harmony={self.harmony_version}, "
            f"ip={self.ip_address})"
        )


class DeviceManager:
    """
    Device detection and management.

    Provides device listing, information retrieval, and device selection.
    """

    def __init__(
        self,
        hdc_cmd: str = "hdc",
        timeout: int = 10,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize device manager.

        Args:
            hdc_cmd: HDC command path
            timeout: Command timeout in seconds
            logger: Optional logger instance
        """
        self.hdc = HDCWrapper(hdc_cmd=hdc_cmd, timeout=timeout, logger=logger)
        self.logger = logger or logging.getLogger(__name__)

    def check_hdc(self) -> bool:
        """
        Check if HDC tool is available.

        Returns:
            True if HDC is available
        """
        if not self.hdc.check_hdc():
            log_error(self.logger, "HDC tool not found")
            log_info(self.logger, "Please install HarmonyOS SDK and configure HDC tool")
            return False

        return True

    def list_devices(self) -> List[DeviceInfo]:
        """
        List all connected devices.

        Returns:
            List of device information
        """
        if not self.check_hdc():
            return []

        device_ids = self.hdc.list_devices()

        if not device_ids:
            log_warn(self.logger, "No devices found")
            return []

        devices = []
        for device_id in device_ids:
            device_info = self.get_device_info(device_id)
            if device_info:
                devices.append(device_info)

        return devices

    def get_device_info(self, device_id: str) -> Optional[DeviceInfo]:
        """
        Get detailed information about a device.

        Args:
            device_id: Target device ID

        Returns:
            DeviceInfo object or None
        """
        try:
            # Get device model
            model = self.hdc.get_device_prop(device_id, "ro.product.model").strip()

            # Android version
            android_version = self.hdc.get_device_prop(
                device_id, "ro.build.version.release"
            ).strip()

            # HarmonyOS version (optional)
            harmony_version_val = self.hdc.get_device_prop(
                device_id, "hw_sc.build.platform.version"
            ).strip()
            harmony_version = harmony_version_val if harmony_version_val else None

            # Manufacturer
            manufacturer_val = self.hdc.get_device_prop(
                device_id, "ro.product.manufacturer"
            ).strip()
            manufacturer = manufacturer_val if manufacturer_val else None

            # Device name
            device_name_val = self.hdc.get_device_prop(device_id, "ro.product.name").strip()
            device_name = device_name_val if device_name_val else None

            # IP address
            ip_address = self._get_device_ip(device_id)

            return DeviceInfo(
                device_id=device_id,
                model=model,
                android_version=android_version,
                harmony_version=harmony_version,
                ip_address=ip_address,
                manufacturer=manufacturer,
                device_name=device_name,
            )

        except Exception as e:
            self.logger.error(f"Failed to get device info: {e}")
            return None

    def _get_device_ip(self, device_id: str) -> Optional[str]:
        """
        Get device IP address.

        Args:
            device_id: Target device ID

        Returns:
            IP address or None
        """
        try:
            output = self.hdc.shell_command(device_id, "ip addr show wlan0")

            # Parse IP address from output
            match = re.search(r"inet (\d+\.\d+\.\d+\.\d+)", output)
            if match:
                return match.group(1)

            return None

        except Exception as e:
            self.logger.debug(f"Failed to get device IP: {e}")
            return None

    def get_default_device(self) -> Optional[str]:
        """
        Get the first available device ID.

        Returns:
            Device ID or None
        """
        devices = self.list_devices()

        if devices:
            log_success(self.logger, f"Found device: {devices[0].device_id}")
            return devices[0].device_id

        log_error(self.logger, "No device found")
        return None

    def wait_for_device(
        self, timeout: int = 30, interval: int = 2
    ) -> Optional[str]:
        """
        Wait for a device to be connected.

        Args:
            timeout: Maximum wait time in seconds
            interval: Check interval in seconds

        Returns:
            Device ID or None
        """
        import time

        log_info(self.logger, f"Waiting for device (timeout: {timeout}s)...")

        start_time = time.time()
        while time.time() - start_time < timeout:
            device_id = self.get_default_device()
            if device_id:
                return device_id

            time.sleep(interval)

        log_error(self.logger, "No device connected within timeout")
        return None

    def print_device_list(self, devices: List[DeviceInfo]) -> None:
        """
        Print device list in formatted table.

        Args:
            devices: List of device information
        """
        if not devices:
            log_info(self.logger, "No devices found")
            return

        log_info(self.logger, "Connected devices:")
        print("-" * 80)

        for i, device in enumerate(devices, 1):
            print(f"{i}. Device ID: {device.device_id}")
            print(f"   Model: {device.model}")
            print(f"   Android: {device.android_version}")
            if device.harmony_version:
                print(f"   HarmonyOS: {device.harmony_version}")
            if device.ip_address:
                print(f"   IP: {device.ip_address}")
            print()

        print("-" * 80)
