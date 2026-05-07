#!/usr/bin/env python3
"""Filter uncovered testfwk APIs that need test generation.

Supports multiple ETS versions (ets1.1, ets1.2) and generates timestamped output files.
"""

import glob
import os
import json
import csv
from datetime import datetime
from collections import defaultdict


def load_config():
    """Load .oh-xts-config.json to get ets_version and scan_tool_root settings."""
    global_config_path = os.path.join(os.path.dirname(__file__), '..', '.oh-xts-config.json')
    scan_tool_root = ''
    if os.path.exists(global_config_path):
        with open(global_config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            ets_version = config.get('ets_version', 'ets1.1')
            if isinstance(ets_version, str):
                ets_version = ets_version.split(',')
            scan_tool_root = config.get('scan_tool_root', '')
            if not scan_tool_root or not os.path.isdir(scan_tool_root):
                scan_tool_root = ''
            return [v.strip() for v in ets_version if v.strip()], scan_tool_root
    
    config_path = os.path.join(os.path.dirname(__file__), '..', 'APICoverageDetector', 'configs', 'arkts_config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            ets_version = config.get('ets_version', ['ets1.1'])
            return ets_version if isinstance(ets_version, list) else [ets_version], ''
    
    return ['ets1.1'], ''


COL_FORMAT_24 = {
    'module': 0, 'class': 1, 'method': 2, 'func': 3, 'type': 4,
    'start_version': 5, 'latest_version': 6, 'deprecate_version': 7,
    'syscap': 8, 'error_codes': 9, 'is_system_api': 10,
    'model_constraint': 11, 'permission': 12,
    'kit': 19, 'file_path': 20, 'subsystem': 21,
    'parent_type': 22, 'is_optional': 23,
}

COL_FORMAT_27 = {
    'module': 0, 'class': 1, 'method': 2, 'func': 3, 'type': 4,
    'start_version': 5, 'deprecate_version': 7,
    'error_codes': 9, 'model_constraint': 11,
    'kit': 17, 'subsystem': 19,
    'param_optional': 20, 'params': 21, 'param_range': 22,
    'is_promise': 23, 'is_covered': 26,
    'uncovered_err': 28,
    'permission_covered': 29, 'permission_uncovered': 30,
    'param_coverage': 31, 'param_uncovered_desc': 32,
    'param_coverage_note': 33,
    'return_value_coverage': 34, 'return_value_status': 35,
    'return_value_uncovered_desc': 36,
    'return_value_uncovered_note': 37,
}

SKIPPED_TYPES = {'Import', 'TypeAlias', 'EnumValue'}


def detect_col_format(vals):
    if len(vals) >= 27:
        return '27+'
    elif len(vals) >= 20:
        return '24'
    return None


def safe_get(vals, index, default=''):
    if index < len(vals) and vals[index] and str(vals[index]).strip() not in ('', 'None'):
        return str(vals[index]).strip()
    return default


def get_latest_csv_file(results_dir, iter_phase=None, file_prefix='before_generation'):
    """Get the latest CSV file from a directory.

    Tries multiple prefixes in order: before_generation, all_collect, collect.

    Args:
        results_dir: Directory to search
        iter_phase: Iteration phase number (1, 2, etc.)
        file_prefix: File prefix to search (default: 'before_generation')
    """
    search_prefixes = [file_prefix, 'all_collect', 'collect']
    for prefix in search_prefixes:
        if iter_phase:
            pattern = os.path.join(results_dir, f'iter-{iter_phase}', f'{prefix}_*.csv')
        else:
            pattern = os.path.join(results_dir, f'{prefix}_*.csv')
        files = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
        if files:
            return files[0]
    return None


def parse_csv_file(file_path, subsystem=None, module_name=None):
    """Parse a CSV file and extract uncovered API entries.

    Supports two CSV column formats:
    - 27+ columns: detailed coverage report from APICoverageDetector (has is_covered column)
    - 24 columns: raw API listing from all_collect (no coverage column, treats all as uncovered)

    Args:
        file_path: Path to the CSV file
        subsystem: The subsystem to filter (optional, default: None)
        module_name: The module name to filter (optional, default: None)
    """
    rows = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)

    if len(rows) < 2:
        return [], [], []

    sample_row = rows[1] if len(rows[1]) >= len(rows[0]) else rows[0]
    fmt = detect_col_format(sample_row)
    if fmt is None:
        print(f"Warning: unrecognized CSV format ({len(sample_row)} columns) in {file_path}")
        return [], [], []

    col = COL_FORMAT_27 if fmt == '27+' else COL_FORMAT_24

    methods = []
    interfaces = []
    properties = []

    for row in rows[1:]:
        vals = list(row)

        api_type = safe_get(vals, col['type'])
        if api_type in SKIPPED_TYPES:
            continue

        subsystem_col = col['subsystem']
        subsystem_val = safe_get(vals, subsystem_col)
        if subsystem is not None and subsystem != subsystem_val:
            continue

        if fmt == '27+' and 'is_covered' in col:
            is_covered = safe_get(vals, col['is_covered'])
            if is_covered and is_covered.lower() not in ('', 'false', '0'):
                continue

        module = safe_get(vals, col['module'])
        if module_name is not None and module_name not in module:
            continue

        cls = safe_get(vals, col['class'])
        method = safe_get(vals, col['method'])
        func = safe_get(vals, col['func'])
        kit = safe_get(vals, col['kit'])
        error_codes = safe_get(vals, col['error_codes'])
        start_version = safe_get(vals, col.get('start_version', 5))
        deprecate_version = safe_get(vals, col.get('deprecate_version', 7))
        stage_label = safe_get(vals, col.get('model_constraint', 11))

        entry = {
            'module': module, 'class': cls, 'method': method,
            'type': api_type, 'func': func, 'kit': kit,
            'error_codes': error_codes,
            'start_version': start_version,
            'deprecate_version': deprecate_version,
            'stage_label': stage_label,
            'csv_format': fmt,
        }

        if fmt == '24':
            entry['file_path'] = safe_get(vals, col['file_path'])
            entry['is_optional'] = safe_get(vals, col['is_optional'])
            entry['parent_type'] = safe_get(vals, col['parent_type'])

        if fmt == '27+':
            for field_name, col_idx in [
                ('param_optional', 20), ('params', 21), ('param_range', 22),
                ('is_promise', 23), ('uncovered_err', 28),
                ('permission_covered', 29), ('permission_uncovered', 30),
                ('param_coverage', 31), ('param_uncovered_desc', 32),
                ('param_coverage_note', 33),
                ('return_value_coverage', 34), ('return_value_status', 35),
                ('return_value_uncovered_desc', 36),
                ('return_value_uncovered_note', 37),
            ]:
                if col_idx < len(vals):
                    val = safe_get(vals, col_idx)
                    if val:
                        entry[field_name] = val

        entry = clean_empty_fields(entry)

        if api_type == 'Method':
            methods.append(entry)
        elif api_type == 'Interface':
            interfaces.append(entry)
        elif api_type == 'Property':
            properties.append(entry)

    return methods, interfaces, properties


def deduplicate_entries(entries):
    """Deduplicate entries based on module+class+method combination."""
    seen = {}
    for entry in entries:
        key = f"{entry['module']}|{entry['class']}|{entry['method']}"
        if key not in seen:
            seen[key] = entry
    return list(seen.values())


def clean_empty_fields(entry):
    """Keep specific coverage fields even if empty to preserve coverage info."""
    coverage_fields = ['param_coverage', 'return_value_coverage', 'permission_covered']
    return {k: v for k, v in entry.items() if (k in coverage_fields) or (v and str(v).strip())}


def clean_metadata(metadata):
    """Clean metadata to remove empty summary entries."""
    if not metadata.get('summary'):
        return metadata
        
    summary = metadata['summary']
    if not summary.get('ets1.1') and not summary.get('ets1.2'):
        return {k: v for k, v in metadata.items() if k != 'summary'}
        
    cleaned_summary = {}
    for version in ['ets1.1', 'ets1.2']:
        version_summary = summary.get(version, {})
        if version_summary:
            cleaned_summary[version] = version_summary
    
    if cleaned_summary:
        metadata['summary'] = cleaned_summary
    
    return metadata


def analyze_coverage_details(methods):
    """Analyze coverage details for methods."""
    analysis = {
        'error_code_issues': 0,
        'param_issues': 0,
        'return_value_issues': 0,
        'permission_issues': 0,
        'specific_issues': []
    }

    for method in methods:
        has_error_code = method.get('error_codes', '') and method['error_codes'].strip()
        has_uncovered_err = method.get('uncovered_err', '') and method['uncovered_err'].strip()
        has_param_issue = method.get('param_coverage', '').lower() != 'true'
        has_return_issue = method.get('return_value_uncovered_desc', '') and method['return_value_uncovered_desc'].strip()
        has_permission_issue = method.get('permission_uncovered', '') and method['permission_uncovered'].strip()

        if has_error_code or has_uncovered_err or has_param_issue or has_return_issue or has_permission_issue:
            issue_info = {
                'method': f"{method['class']}.{method['method']}",
                'api_type': method['type'],
                'signature': method['func']
            }

            if has_error_code:
                analysis['error_code_issues'] += 1
                issue_info['error_codes'] = method['error_codes']
            
            if has_uncovered_err:
                issue_info['uncovered_err'] = method['uncovered_err']
            
            if has_param_issue:
                analysis['param_issues'] += 1
                issue_info['param_issues'] = {
                    'coverage': method.get('param_coverage', ''),
                    'uncovered_desc': method.get('param_uncovered_desc', ''),
                    'coverage_note': method.get('param_coverage_note', '')
                }
            
            if has_return_issue:
                analysis['return_value_issues'] += 1
                issue_info['return_value_issues'] = {
                    'coverage': method.get('return_value_coverage', ''),
                    'status': method.get('return_value_status', ''),
                    'uncovered_desc': method.get('return_value_uncovered_desc', ''),
                    'uncovered_note': method.get('return_value_uncovered_note', '')
                }
            
            if has_permission_issue:
                analysis['permission_issues'] += 1
                issue_info['permission_issues'] = {
                    'covered': method.get('permission_covered', ''),
                    'uncovered': method.get('permission_uncovered', '')
                }

            analysis['specific_issues'].append(issue_info)

    return analysis


def main(subsystem=None, module_name=None, iter_phase=1):
    """Main function to extract uncovered APIs from multiple ETS versions.

    Args:
        subsystem: The subsystem to filter (optional, default: None)
        module_name: The module name to filter (optional, default: None)
        iter_phase: Iteration phase number (default: 1)
    """
    ets_versions, scan_tool_root = load_config()

    version_data = {}
    total_methods = 0
    total_interfaces = 0
    total_properties = 0

    for ets_version in ets_versions:
        results_dir = os.path.join(os.path.dirname(__file__), '..', '.coverage_data')

        csv_candidates = []
        for prefix in [f'before_generation_{ets_version}', f'all_collect_{ets_version}', f'collect_{ets_version}']:
            path = get_latest_csv_file(results_dir, iter_phase=iter_phase, file_prefix=prefix)
            if path:
                csv_candidates.append(path)
            path = get_latest_csv_file(results_dir, file_prefix=prefix)
            if path and path not in csv_candidates:
                csv_candidates.append(path)

        csv_file = None
        for candidate in csv_candidates:
            methods_t, interfaces_t, properties_t = parse_csv_file(candidate, subsystem=subsystem, module_name=module_name)
            if methods_t or interfaces_t or properties_t:
                csv_file = candidate
                methods, interfaces, properties = methods_t, interfaces_t, properties_t
                break
            else:
                print(f"Skipped (no usable data): {os.path.basename(candidate)}")

        if not csv_file:
            print(f"No usable CSV file found for {ets_version}")
            continue

        print(f"Using: {os.path.basename(csv_file)} ({os.path.getsize(csv_file)} bytes)")

        coverage_analysis = analyze_coverage_details(methods)

        version_data[ets_version] = {
            'methods': methods,
            'interfaces': interfaces,
            'properties': properties,
            'coverage_analysis': coverage_analysis
        }

        total_methods += len(methods)
        total_interfaces += len(interfaces)
        total_properties += len(properties)

        print(f"{ets_version}: {len(methods)} methods, {len(interfaces)} interfaces, {len(properties)} properties")

    output = {
        'ets1.1': version_data.get('ets1.1', {'methods': [], 'interfaces': [], 'properties': [], 'coverage_analysis': {}}),
        'ets1.2': version_data.get('ets1.2', {'methods': [], 'interfaces': [], 'properties': [], 'coverage_analysis': {}}),
        'metadata': {
            'ets_versions': ets_versions,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'summary': {
                'ets1.1': {
                    'methods': len(version_data.get('ets1.1', {}).get('methods', [])),
                    'interfaces': len(version_data.get('ets1.1', {}).get('interfaces', [])),
                    'properties': len(version_data.get('ets1.1', {}).get('properties', [])),
                    'error_code_issues': version_data.get('ets1.1', {}).get('coverage_analysis', {}).get('error_code_issues', 0),
                    'param_issues': version_data.get('ets1.1', {}).get('coverage_analysis', {}).get('param_issues', 0),
                    'return_value_issues': version_data.get('ets1.1', {}).get('coverage_analysis', {}).get('return_value_issues', 0),
                    'permission_issues': version_data.get('ets1.1', {}).get('coverage_analysis', {}).get('permission_issues', 0)
                },
                'ets1.2': {
                    'methods': len(version_data.get('ets1.2', {}).get('methods', [])),
                    'interfaces': len(version_data.get('ets1.2', {}).get('interfaces', [])),
                    'properties': len(version_data.get('ets1.2', {}).get('properties', [])),
                    'error_code_issues': version_data.get('ets1.2', {}).get('coverage_analysis', {}).get('error_code_issues', 0),
                    'param_issues': version_data.get('ets1.2', {}).get('coverage_analysis', {}).get('param_issues', 0),
                    'return_value_issues': version_data.get('ets1.2', {}).get('coverage_analysis', {}).get('return_value_issues', 0),
                    'permission_issues': version_data.get('ets1.2', {}).get('coverage_analysis', {}).get('permission_issues', 0)
                }
            }
        }
    }

    output['metadata'] = clean_metadata(output['metadata'])

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    output_dir = os.path.join(os.path.dirname(__file__), '..', '.coverage_data', f'iter-{iter_phase}')
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f'uncovered_apis_{timestamp}.json')

    with open(out_path, 'w', encoding='utf-8') as fp:
        json.dump(output, fp, indent=2, ensure_ascii=False)

    print(f"\n=== SUMMARY ===")
    print(f"Processing: {', '.join(ets_versions)}")
    print(f"Total uncovered APIs: {total_methods} methods, {total_interfaces} interfaces, {total_properties} properties")
    for version in ets_versions:
        analysis = version_data.get(version, {}).get('coverage_analysis', {})
        print(f"{version}: error_code={analysis.get('error_code_issues', 0)}, param={analysis.get('param_issues', 0)}, return_value={analysis.get('return_value_issues', 0)}")
    print(f"Saved to: {out_path}")
    return out_path


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Extract uncovered APIs from CSV coverage reports')
    parser.add_argument('--subsystem', type=str, default=None, help='Filter by subsystem name')
    parser.add_argument('--module-name', type=str, default=None, help='Filter by module name')
    parser.add_argument('--iter-phase', type=int, default=1, help='Iteration phase number (default: 1)')
    args = parser.parse_args()
    main(subsystem=args.subsystem, module_name=args.module_name, iter_phase=args.iter_phase)
