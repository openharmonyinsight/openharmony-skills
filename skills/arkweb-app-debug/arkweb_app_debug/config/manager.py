"""Configuration manager - Minimal zero-dependency version."""

import logging
from pathlib import Path
from typing import Dict, Optional, Any

from .detector import ProjectDetector


class ConfigManager:
    """
    Minimal configuration manager for arkweb.app.debug.

    Zero-dependency version: No config files, uses auto-detection and defaults.
    Configuration priority: CLI args > auto-detected > hardcoded defaults.
    """

    # Hardcoded sensible defaults (no external config files needed)
    DEFAULT_CONFIG = {
        "defaults": {
            "debug_port": 8888,
            "local_port_base": 9222,
            "hdc_timeout": 10,
            "app_start_timeout": 15,
        },
        "resource_management": {
            "auto_cleanup": True,
            "cleanup_orphans": True,
            "max_sessions": 5,
        },
        "logging": {
            "level": "INFO",
            "file": None,  # Log to stdout only
        },
    }

    def __init__(self, logger: Optional[logging.Logger] = None):
        """Initialize configuration manager."""
        self.logger = logger or logging.getLogger(__name__)

    def load_config(
        self,
        project_path: Optional[str] = None,
        global_config_path: Optional[str] = None,
        auto_detect: bool = True,
    ) -> Dict[str, Any]:
        """
        Load and merge configuration levels.

        Priority: CLI args > auto-detected > hardcoded defaults

        Args:
            project_path: Path to project directory
            global_config_path: Ignored (for compatibility)
            auto_detect: Whether to auto-detect project config

        Returns:
            Merged configuration dictionary
        """
        # Start with hardcoded defaults
        config = self.DEFAULT_CONFIG.copy()

        # Auto-detect project config (optional enhancement)
        if auto_detect:
            detector = ProjectDetector(self.logger)

            # Try to find project root (searches upward)
            project_root = detector.find_project_root(project_path)

            if project_root or detector.is_harmonyos_project(project_path):
                self.logger.info("Auto-detecting project configuration...")
                project_config = detector.detect_project_config(project_path)
                if project_config:
                    self.logger.info("✓ Auto-detected project configuration")
                    # Merge: project config overrides defaults
                    config = self._deep_merge(config, project_config)

        self.logger.debug(f"Final configuration: {config}")
        return config

    def apply_cli_args(
        self, config: Dict[str, Any], cli_args: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply CLI arguments to configuration (highest precedence).

        Args:
            config: Base configuration
            cli_args: CLI arguments dictionary

        Returns:
            Updated configuration
        """
        # Create app section if it doesn't exist
        if "app" not in config:
            config["app"] = {}

        # Apply app-specific args
        if "package" in cli_args and cli_args["package"]:
            config["app"]["package"] = cli_args["package"]

        if "bundle" in cli_args and cli_args["bundle"]:
            config["app"]["bundle"] = cli_args["bundle"]

        if "hap_path" in cli_args and cli_args["hap_path"]:
            config["app"]["hap_path"] = cli_args["hap_path"]

        # Create debug section if it doesn't exist
        if "debug" not in config:
            config["debug"] = {}

        # Apply debug-specific args
        if "local_port" in cli_args and cli_args["local_port"]:
            config["debug"]["local_port"] = cli_args["local_port"]

        if "device_port" in cli_args and cli_args["device_port"]:
            config["debug"]["device_port"] = cli_args["device_port"]

        if "device_id" in cli_args and cli_args["device_id"]:
            config["debug"]["device_id"] = cli_args["device_id"]

        self.logger.debug(f"Applied CLI args: {cli_args}")
        return config

    def _deep_merge(
        self, base: Dict[str, Any], override: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Deep merge two dictionaries.

        Args:
            base: Base dictionary
            override: Override dictionary

        Returns:
            Merged dictionary
        """
        result = base.copy()

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value

        return result
