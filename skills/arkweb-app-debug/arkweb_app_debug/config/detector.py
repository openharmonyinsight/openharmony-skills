"""
Auto-detect HarmonyOS project configuration.

Automatically extracts package name and HAP path from HarmonyOS project files.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Optional, Any


class ProjectDetector:
    """
    Auto-detect HarmonyOS project configuration.

    Detects:
    - Bundle name from AppScope/app.json5
    - HAP output path from build directories
    - Module names from entry/src/main/module.json5
    """

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize project detector.

        Args:
            logger: Optional logger instance
        """
        self.logger = logger or logging.getLogger(__name__)

    def find_project_root(self, start_path: Optional[str] = None) -> Optional[Path]:
        """
        Find HarmonyOS project root by searching upward.

        Args:
            start_path: Starting directory (default: current directory)

        Returns:
            Project root path or None
        """
        if start_path:
            current_dir = Path(start_path).expanduser().resolve()
        else:
            current_dir = Path.cwd()

        # Search upward for project markers
        max_levels = 5  # Limit search depth
        for _ in range(max_levels):
            if self.is_harmonyos_project(current_dir):
                return current_dir

            parent = current_dir.parent
            if parent == current_dir:  # Reached root
                break
            current_dir = parent

        return None

    def detect_project_config(
        self, project_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Auto-detect project configuration from HarmonyOS project files.

        Args:
            project_path: Path to project directory (default: current directory)

        Returns:
            Detected configuration dictionary with keys:
            - package: Bundle name (e.g., "com.example.arkwebtesting")
            - hap: HAP file path (relative to project root)
            - modules: List of module names (e.g., ["entry"])
            - detected: True (indicates auto-detected config)
        """
        # First, try to find project root
        project_dir = self.find_project_root(project_path)

        if not project_dir:
            if project_path:
                project_dir = Path(project_path).expanduser().resolve()
            else:
                project_dir = Path.cwd()

        self.logger.info(f"Auto-detecting project config in: {project_dir}")

        config = {"app": {}}  # Use 'app' key for consistency

        # Detect bundle name from AppScope/app.json5
        bundle_name = self._detect_bundle_name(project_dir)
        if bundle_name:
            config["app"]["package"] = bundle_name
            self.logger.info(f"✓ Detected bundle name: {bundle_name}")
        else:
            self.logger.warning("✗ Could not detect bundle name")

        # Detect HAP path
        hap_path = self._detect_hap_path(project_dir)
        if hap_path:
            config["app"]["hap"] = str(hap_path)
            self.logger.info(f"✓ Detected HAP path: {hap_path}")
        else:
            self.logger.warning("✗ Could not detect HAP path")

        # Detect modules
        modules = self._detect_modules(project_dir)
        if modules:
            config["app"]["modules"] = modules
            self.logger.info(f"✓ Detected modules: {modules}")
        else:
            self.logger.warning("✗ Could not detect modules")

        # Add detection flag and default port
        if config["app"]:
            config["app"]["detected"] = True
            config["app"]["port"] = 9222  # Default port

        return config

    def _detect_bundle_name(self, project_dir: Path) -> Optional[str]:
        """
        Detect bundle name from AppScope/app.json5.

        Args:
            project_dir: Project root directory

        Returns:
            Bundle name or None
        """
        app_json5_path = project_dir / "AppScope" / "app.json5"

        if not app_json5_path.exists():
            self.logger.debug(f"AppScope/app.json5 not found: {app_json5_path}")
            return None

        try:
            with open(app_json5_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse JSON5 (handle comments and trailing commas)
            # Remove // comments
            import re
            content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)

            # Remove trailing commas before } or ]
            content = re.sub(r',(\s*[}\]])', r'\1', content)

            data = json.loads(content)

            if "app" in data and "bundleName" in data["app"]:
                return data["app"]["bundleName"]

            self.logger.debug(f"No bundleName found in {app_json5_path}")
            return None

        except Exception as e:
            self.logger.debug(f"Failed to parse {app_json5_path}: {e}")
            return None

    def _detect_hap_path(self, project_dir: Path) -> Optional[Path]:
        """
        Detect HAP output path from build directories.

        Searches for HAP files in common build output directories:
        - entry/build/default/outputs/default/
        - entry/build/outputs/default/

        Args:
            project_dir: Project root directory

        Returns:
            Path to HAP file (relative to project root) or None
        """
        # Common module names
        module_names = self._detect_modules(project_dir) or ["entry"]

        # Common build paths
        build_patterns = [
            "{module}/build/default/outputs/default/{module}-default-signed.hap",
            "{module}/build/default/outputs/default/{module}-default.hap",
            "{module}/build/outputs/default/{module}-default-signed.hap",
            "{module}/build/outputs/default/{module}-default.hap",
        ]

        for module in module_names:
            for pattern in build_patterns:
                hap_path = project_dir / pattern.format(module=module)

                if hap_path.exists():
                    # Return relative path from project root
                    return hap_path.relative_to(project_dir)

        self.logger.debug("No HAP file found in build directories")
        return None

    def _detect_modules(self, project_dir: Path) -> Optional[list]:
        """
        Detect module names from project structure.

        Looks for directories with module.json5 files:
        - entry/src/main/module.json5
        - <module>/src/main/module.json5

        Args:
            project_dir: Project root directory

        Returns:
            List of module names or None
        """
        modules = []

        # Check for common module directories
        for item in project_dir.iterdir():
            if not item.is_dir():
                continue

            # Skip common non-module directories
            if item.name in [
                "oh_modules",
                "node_modules",
                ".idea",
                ".git",
                "build",
                "dist",
                "AppScope",
                "hvigor",
                "oh-package.json5",
            ]:
                continue

            # Check if it has module.json5
            module_json5 = item / "src" / "main" / "module.json5"
            if module_json5.exists():
                modules.append(item.name)

        return modules if modules else None

    def is_harmonyos_project(self, project_path: Optional[str] = None) -> bool:
        """
        Check if directory is a HarmonyOS project.

        Args:
            project_path: Path to check (default: current directory)

        Returns:
            True if HarmonyOS project
        """
        if project_path:
            project_dir = Path(project_path).expanduser().resolve()
        else:
            project_dir = Path.cwd()

        # Check for HarmonyOS project markers
        markers = [
            "AppScope",
            "build-profile.json5",
            "oh-package.json5",
        ]

        for marker in markers:
            if (project_dir / marker).exists():
                return True

        return False
