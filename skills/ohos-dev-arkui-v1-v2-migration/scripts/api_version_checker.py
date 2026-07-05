#!/usr/bin/env python3
"""
V1->V2 Migration - API Version Checker
Detects project API version from config files to determine which mixing rules apply.
Checks: build-profile.json5, app.json5, module.json5

API < 19: Strict mixing constraints, complex types cannot cross V1/V2 boundary.
API >= 19: Relaxed constraints with enableV2Compatibility / makeV1Observed APIs.

Usage:
    python3 api_version_checker.py <project_dir> [--json]
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import Optional, Dict, List


def strip_json5_comments(text: str) -> str:
    """Remove // comments and trailing commas from JSON5 content."""
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        # Remove single-line comments (not inside strings)
        in_string = False
        quote_char = None
        result = []
        i = 0
        while i < len(line):
            ch = line[i]
            if not in_string:
                if ch in ('"', "'"):
                    in_string = True
                    quote_char = ch
                    result.append(ch)
                elif ch == '/' and i + 1 < len(line) and line[i + 1] == '/':
                    break  # Rest is comment
                else:
                    result.append(ch)
            else:
                result.append(ch)
                if ch == quote_char and (i == 0 or line[i - 1] != '\\'):
                    in_string = False
            i += 1
        cleaned.append(''.join(result))

    text = '\n'.join(cleaned)
    # Remove trailing commas before } or ]
    text = re.sub(r',\s*([}\]])', r'\1', text)
    return text


def parse_json5(filepath: str) -> Optional[Dict]:
    """Parse a JSON5 file (strip comments + trailing commas, then parse as JSON)."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (IOError, UnicodeDecodeError):
        return None

    cleaned = strip_json5_comments(content)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return None


def find_config_files(project_dir: str) -> Dict[str, Optional[str]]:
    """Find all relevant config files in the project."""
    project = Path(project_dir)
    configs = {}

    # build-profile.json5: typically at project root
    bp = project / 'build-profile.json5'
    configs['build-profile'] = str(bp) if bp.exists() else None

    # app.json5: AppScope/app.json5 or app.json5
    for candidate in ['AppScope/app.json5', 'app.json5']:
        p = project / candidate
        if p.exists():
            configs['app'] = str(p)
            break
    else:
        configs['app'] = None

    # module.json5: may exist in multiple modules, collect all
    module_files = list(project.glob('**/src/main/module.json5'))
    # Deduplicate: prefer shorter paths (top-level modules)
    module_files = sorted(module_files, key=lambda p: len(str(p)))
    configs['modules'] = [str(f) for f in module_files] if module_files else None

    return configs


def parse_api_version(val) -> Optional[int]:
    """Parse API version from various formats:
    - int: 24
    - str plain number: "24"
    - str with sdk name: "6.1.1(24)", "API 24", "5.0.0(19)"
    Returns the integer API version number or None.
    """
    if isinstance(val, int):
        return val
    if not isinstance(val, str):
        return None
    val = val.strip()
    # Try plain integer
    try:
        return int(val)
    except ValueError:
        pass
    # Try "X.Y.Z(N)" format — extract N from parentheses
    m = re.search(r'\((\d+)\)', val)
    if m:
        return int(m.group(1))
    # Try "API N" or "apiN" format
    m = re.search(r'(?:api|API)\s*(\d+)', val)
    if m:
        return int(m.group(1))
    return None


def extract_version_from_build_profile(data: Dict) -> Optional[int]:
    """Extract API version from build-profile.json5.
    Looks for compatibleSdkVersion/targetSdkVersion in app.products[]."""
    products = data.get('app', {}).get('products', [])
    if not products:
        return None

    # Use the first product, or look for a default product
    product = products[0]
    for key in ('compatibleSdkVersion', 'targetSdkVersion'):
        val = product.get(key)
        if val is not None:
            parsed = parse_api_version(val)
            if parsed is not None:
                return parsed
    return None


def extract_version_from_app_json5(data: Dict) -> Optional[int]:
    """Extract API version from AppScope/app.json5.
    Looks for minAPIVersion/targetAPIVersion in app section."""
    app = data.get('app', {})
    for key in ('minAPIVersion', 'targetAPIVersion'):
        val = app.get(key)
        if val is not None:
            parsed = parse_api_version(val)
            if parsed is not None:
                return parsed
    return None


def extract_version_from_module_json5(data: Dict) -> Optional[int]:
    """Extract API version from module.json5.
    Some modules may have minAPIVersion in the module section."""
    module = data.get('module', {})
    # Check distro or direct fields
    for key in ('minAPIVersion', 'targetAPIVersion'):
        val = module.get(key)
        if val is not None:
            parsed = parse_api_version(val)
            if parsed is not None:
                return parsed
    # Some use distro.deviceConfig
    distro = module.get('distro', {})
    for key in ('minAPIVersion',):
        val = distro.get(key)
        if val is not None:
            parsed = parse_api_version(val)
            if parsed is not None:
                return parsed
    return None


API_VERSION_THRESHOLD = 19


def detect_api_version(project_dir: str) -> Dict:
    """Detect the API version of a HarmonyOS project.

    Returns a dict with:
    - compatibleApiVersion: the minimum/compatible API version detected
    - targetApiVersion: the target API version
    - apiLevel: 'pre19' or 'post19' based on compatibleSdkVersion
    - sources: where each version was found
    - mixingRules: 'strict' (API<19) or 'relaxed' (API>=19)
    - availableApis: list of V1V2 compatibility APIs available
    """
    config_paths = find_config_files(project_dir)
    sources = {}
    compatible_version = None
    target_version = None

    # Check build-profile.json5
    if config_paths.get('build-profile'):
        data = parse_json5(config_paths['build-profile'])
        if data:
            v = extract_version_from_build_profile(data)
            if v is not None:
                compatible_version = v
                sources['build-profile'] = {
                    'file': config_paths['build-profile'],
                    'version': v,
                }
                products = data.get('app', {}).get('products', [])
                if products:
                    tv = products[0].get('targetSdkVersion') or products[0].get('compileSdkVersion')
                    if tv is not None:
                        try:
                            target_version = int(tv)
                        except (ValueError, TypeError):
                            pass

    # Check app.json5 (may override or be the only source)
    if config_paths.get('app'):
        data = parse_json5(config_paths['app'])
        if data:
            v = extract_version_from_app_json5(data)
            if v is not None:
                if compatible_version is None or v < compatible_version:
                    compatible_version = v
                sources['app'] = {
                    'file': config_paths['app'],
                    'version': v,
                }
                app = data.get('app', {})
                tv = app.get('targetAPIVersion')
                if tv is not None and target_version is None:
                    try:
                        target_version = int(tv)
                    except (ValueError, TypeError):
                        pass

    # Check module.json5 files (use minimum across all modules)
    if config_paths.get('modules'):
        module_versions = []
        for mf in config_paths['modules']:
            data = parse_json5(mf)
            if data:
                v = extract_version_from_module_json5(data)
                if v is not None:
                    module_versions.append({'file': mf, 'version': v})
                    if compatible_version is None or v < compatible_version:
                        compatible_version = v
        if module_versions:
            sources['modules'] = module_versions

    # Determine API level and mixing rules
    if compatible_version is None:
        return {
            'projectDir': project_dir,
            'compatibleApiVersion': None,
            'targetApiVersion': target_version,
            'apiLevel': 'unknown',
            'mixingRules': 'strict',
            'availableApis': [],
            'sources': sources,
            'warning': 'Could not detect API version. Defaulting to strict (API<19) rules. '
                       'Check build-profile.json5, app.json5, or module.json5.',
        }

    api_level = 'post19' if compatible_version >= API_VERSION_THRESHOLD else 'pre19'
    mixing_rules = 'relaxed' if compatible_version >= API_VERSION_THRESHOLD else 'strict'

    available_apis = []
    if compatible_version >= API_VERSION_THRESHOLD:
        available_apis = [
            'UIUtils.makeV1Observed()',
            'UIUtils.enableV2Compatibility()',
        ]

    return {
        'projectDir': project_dir,
        'compatibleApiVersion': compatible_version,
        'targetApiVersion': target_version,
        'apiLevel': api_level,
        'mixingRules': mixing_rules,
        'availableApis': available_apis,
        'sources': sources,
    }


def main():
    parser = argparse.ArgumentParser(
        description='Detect API version for V1->V2 migration mixing rules'
    )
    parser.add_argument('project_dir', help='Project root directory')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    if not Path(args.project_dir).is_dir():
        print(f"Error: {args.project_dir} is not a valid directory", file=sys.stderr)
        sys.exit(1)

    result = detect_api_version(args.project_dir)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*60}")
        print(f"API Version Check: {result['projectDir']}")
        print(f"{'='*60}")

        if result.get('warning'):
            print(f"\n  WARNING: {result['warning']}")

        print(f"\n  Compatible API Version: {result['compatibleApiVersion'] or 'NOT DETECTED'}")
        print(f"  Target API Version:     {result['targetApiVersion'] or 'N/A'}")
        print(f"  API Level:              {result['apiLevel']}")
        print(f"  Mixing Rules:           {result['mixingRules']}")

        if result.get('availableApis'):
            print(f"  Available V1V2 APIs:    {', '.join(result['availableApis'])}")

        print(f"\n  Sources:")
        for source_name, source_info in result.get('sources', {}).items():
            if isinstance(source_info, list):
                for item in source_info:
                    print(f"    {source_name}: v{item['version']} ({item['file']})")
            else:
                print(f"    {source_name}: v{source_info['version']} ({source_info['file']})")

        if result['mixingRules'] == 'strict':
            print(f"\n  Implications (API < {API_VERSION_THRESHOLD}):")
            print(f"    - Complex types CANNOT cross V1/V2 boundary")
            print(f"    - Bridge pattern required for @Observed class passing V1->V2")
            print(f"    - Simple types only: boolean, number, string, null, undefined")
            print(f"    - UIUtils.makeV1Observed / enableV2Compatibility NOT available")
        else:
            print(f"\n  Implications (API >= {API_VERSION_THRESHOLD}):")
            print(f"    - UIUtils.enableV2Compatibility() available for complex type passing")
            print(f"    - UIUtils.makeV1Observed() available for wrapping objects")
            print(f"    - Bridge pattern still needed for some edge cases")


if __name__ == '__main__':
    main()
