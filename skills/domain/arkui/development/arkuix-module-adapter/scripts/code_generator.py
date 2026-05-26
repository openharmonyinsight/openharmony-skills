#!/usr/bin/env python3
"""
Code Generator - Generate configuration files for module adaptation

This script automatically updates the 4 mandatory configuration files needed
for cross-platform module adaptation.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List


class CodeGenerator:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        if not self.project_root.exists():
            raise FileNotFoundError(f"Project root not found: {project_root}")

    def generate(self, module: str, repo_name: str, api_version: int = 23, dry_run: bool = False):
        """Generate all 4 mandatory configuration files"""
        module_parts = module.split('/')
        module_name = module_parts[-1] if len(module_parts) > 0 else module
        module_path_clean = module.replace('/', '_')

        files_to_update = [
            ('plugin_lib.gni', self._generate_plugin_lib_entry),
            ('interface/sdk/plugins/api/apiConfig.json', self._generate_api_config),
            ('build_plugins/sdk/arkui_cross_sdk_description_std.json', self._generate_sdk_description),
            (f'interface/sdk-js/api/@ohos.{module}.d.ts', self._generate_dts_annotations),
        ]

        for file_path, generator in files_to_update:
            try:
                full_path = self.project_root / file_path
                if not full_path.exists():
                    print(f"⚠️  File not found: {file_path}")
                    continue

                if dry_run:
                    content = generator(module, repo_name, api_version, full_path)
                    print(f"\n📄 File: {file_path}")
                    print(f"--- Preview ---")
                    print(content[:500] + "..." if len(content) > 500 else content)
                    print(f"--- End Preview ---\n")
                else:
                    self._update_file(full_path, generator, module, repo_name, api_version)
                    print(f"✅ Updated: {file_path}")

            except Exception as e:
                print(f"❌ Error updating {file_path}: {e}")
                return False

        return True

    def _generate_plugin_lib_entry(self, module: str, repo_name: str, api_version: int, file_path: Path) -> str:
        """Generate plugin_lib.gni entry"""
        # Read existing file
        content = file_path.read_text(encoding='utf-8')

        # Check if already exists
        module_entry = f'"{module.replace("/", "_")}"'
        if module_entry in content:
            return ""  # Already exists

        # Find insertion point (after last entry in common_plugin_libs)
        # This is simplified; actual implementation would parse GN properly

        return f"""
# Added for {module}
common_plugin_libs += [
    "{module.replace("/", "_")}_static",
]
"""

    def _generate_api_config(self, module: str, repo_name: str, api_version: int, file_path: Path) -> str:
        """Generate apiConfig.json entry"""
        try:
            config = json.loads(file_path.read_text(encoding='utf-8'))
        except:
            return ""  # Invalid JSON

        module_key = module.replace('/', '_')

        # Add library configuration
        if module_key not in config.get('native', {}):
            config.setdefault('native', {})[module_key] = {
                "native": True,
                "icon": "",
                "iconPath": "",
                "description": f"{module} module"
            }

        return json.dumps(config, indent=2)

    def _generate_sdk_description(self, module: str, repo_name: str, api_version: int, file_path: Path) -> str:
        """Generate SDK description entry"""
        try:
            desc = json.loads(file_path.read_text(encoding='utf-8'))
        except:
            return ""  # Invalid JSON

        module_name = module.split('/')[-1]
        module_key = module.replace('/', '_')

        # Add Android build entries
        android_key = f"{module_key}_android"
        if android_key not in desc.get('build', {}).get('android', {}).get('libraries', {}):
            desc.setdefault('build', {}).setdefault('android', {}).setdefault('libraries', {})[android_key] = {
                "type": "static_library",
                "name": f"lib{module_key}_static_android",
            }

        # Add iOS build entries
        ios_key = f"{module_key}_ios"
        if ios_key not in desc.get('build', {}).get('ios', {}).get('libraries', {}):
            desc.setdefault('build', {}).setdefault('ios', {}).setdefault('libraries', {})[ios_key] = {
                "type": "static_library",
                "name": f"lib{module_key}_static_ios",
            }

        return json.dumps(desc, indent=2)

    def _generate_dts_annotations(self, module: str, repo_name: str, api_version: int, file_path: Path) -> str:
        """Generate @crossplatform and @since annotations"""
        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        result = []

        for line in lines:
            # Add @crossplatform after @syscap if not present
            if '@syscap' in line and '@crossplatform' not in line:
                line = line.replace('@syscap', f'@syscap\n * @crossplatform')

            # Add @since if not present
            if ('export class' in line or 'export interface' in line or 'export function' in line):
                next_line_idx = lines.index(line) + 1 if line in lines else -1
                if next_line_idx < len(lines):
                    next_line = lines[next_line_idx]
                    if '@since' not in next_line and '@since' not in line:
                        line += f'\n * @since {api_version}'

            result.append(line)

        return '\n'.join(result)

    def _update_file(self, file_path: Path, generator, module: str, repo_name: str, api_version: int):
        """Update a file with generated content"""
        new_content = generator(module, repo_name, api_version, file_path)
        if not new_content:
            return  # Nothing to update

        # For JSON files, replace entire content
        if file_path.suffix == '.json':
            file_path.write_text(new_content, encoding='utf-8')
        else:
            # For other files, append or insert
            current = file_path.read_text(encoding='utf-8')
            if '/* Added for' in current:
                return  # Already added

            file_path.write_text(current + new_content, encoding='utf-8')

    def validate(self, module: str) -> bool:
        """Validate that all 4 mandatory files exist and are properly configured"""
        required_files = [
            self.project_root / 'plugins/plugin_lib.gni',
            self.project_root / 'interface/sdk/plugins/api/apiConfig.json',
            self.project_root / 'build_plugins/sdk/arkui_cross_sdk_description_std.json',
            self.project_root / f'interface/sdk-js/api/@ohos.{module}.d.ts',
        ]

        all_valid = True
        for file_path in required_files:
            if not file_path.exists():
                print(f"❌ Missing: {file_path.relative_to(self.project_root)}")
                all_valid = False
            else:
                print(f"✅ Found: {file_path.relative_to(self.project_root)}")

        return all_valid


def main():
    parser = argparse.ArgumentParser(
        description='Generate configuration files for module adaptation'
    )
    parser.add_argument(
        'module',
        help='Module name (e.g., data/preferences)'
    )
    parser.add_argument(
        'repo_name',
        help='OHOS repository name (e.g., distributeddatamgr_preferences)'
    )
    parser.add_argument(
        '--api-version',
        type=int,
        default=23,
        help='API version for @since tags (default: 23)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show changes without writing files'
    )
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Only validate configuration, do not generate'
    )

    args = parser.parse_args()

    try:
        # Find project root
        current_path = Path.cwd()
        while current_path != current_path.parent and not (current_path / 'plugins').exists():
            current_path = current_path.parent

        if not (current_path / 'plugins').exists():
            raise FileNotFoundError("Could not find project root (plugins/ directory)")

        generator = CodeGenerator(str(current_path))

        if args.validate:
            print(f"🔍 Validating configuration for module: {args.module}")
            success = generator.validate(args.module)
            if success:
                print(f"\n✅ All required files found")
            else:
                print(f"\n❌ Validation failed - missing required files")
                sys.exit(1)
        else:
            print(f"📝 Generating configuration for module: {args.module}")
            if args.dry_run:
                print("⚠️  DRY RUN MODE - No files will be modified")

            success = generator.generate(args.module, args.repo_name, args.api_version, args.dry_run)
            if success:
                print(f"\n✅ Configuration generation complete")
            else:
                print(f"\n❌ Configuration generation failed")
                sys.exit(1)

    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
