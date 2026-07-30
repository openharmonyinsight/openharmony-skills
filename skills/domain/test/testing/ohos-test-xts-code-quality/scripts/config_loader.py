#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2026 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""XTS Test Code Quality Scanner - Configuration Loader

Load skill_config.json and provide convenient access to configuration values.
"""
import os
import json

_SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CONFIG_PATH = os.path.join(_SKILL_DIR, 'skill_config.json')

_config = None

def load_config(config_path=None):
    """Load configuration from JSON file.
    
    Args:
        config_path: Optional custom config path. Defaults to skill_config.json.
    
    Returns:
        dict: Configuration dictionary
    """
    global _config
    path = config_path or _CONFIG_PATH
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        _config = json.load(f)
    return _config

def get_config():
    """Get loaded configuration, load if not already loaded."""
    if _config is None:
        load_config()
    return _config

def get_skill_dir():
    """Get skill directory path."""
    return _SKILL_DIR

def get_version():
    """Get scanner version."""
    return get_config().get('version', '2.0.2')

def get_all_rules():
    """Get all rules as list of (id, name, severity) tuples."""
    cfg = get_config()
    rules = []
    critical_desc = cfg.get('rule_descriptions', {}).get('critical', {})
    warning_desc = cfg.get('rule_descriptions', {}).get('warning', {})
    
    for rid in cfg.get('rules', {}).get('critical', []):
        name = critical_desc.get(rid, '')
        rules.append((rid, name, 'Critical'))
    
    for rid in cfg.get('rules', {}).get('warning', []):
        name = warning_desc.get(rid, '')
        rules.append((rid, name, 'Warning'))
    
    return rules

def get_rule_ids():
    """Get all rule IDs as set."""
    return {r[0] for r in get_all_rules()}

def get_critical_rules():
    """Get critical rule IDs."""
    return set(get_config().get('rules', {}).get('critical', []))

def get_warning_rules():
    """Get warning rule IDs."""
    return set(get_config().get('rules', {}).get('warning', []))

def get_category_rules():
    """Get category -> rule IDs mapping."""
    result = {}
    for cat, info in get_config().get('rule_categories', {}).items():
        result[cat] = info.get('rules', [])
    return result

def get_excluded_dirs():
    """Get default excluded directories."""
    return set(get_config().get('config', {}).get('excluded_dirs', []))

def get_assertion_methods():
    """Get assertion method names list."""
    return get_config().get('config', {}).get('assertion_methods', [])

def get_supported_file_types():
    """Get supported file types list."""
    return get_config().get('config', {}).get('supported_file_types', [])

def get_fixable_rules():
    """Get fixable rule IDs."""
    return set(get_config().get('fixable_rules', []))

def get_fix_guide_path(rule_id):
    """Get fix guide path for a rule."""
    return get_config().get('fix_guide_paths', {}).get(rule_id, '')

def is_fixable_rule(rule_id):
    """Check if a rule is fixable."""
    return rule_id in get_fixable_rules()

def get_custom_rules_config():
    """Get custom rules configuration."""
    return get_config().get('custom_rules_config', {})

def get_extensions_dir():
    """Get extensions rules directory path."""
    rel_path = get_config().get('custom_rules_config', {}).get('extensions_dir', '')
    return os.path.join(_SKILL_DIR, rel_path) if rel_path else ''

def get_performance_config():
    """Get performance configuration."""
    return get_config().get('performance', {})

def get_parallel_enabled():
    """Check if parallel processing is enabled."""
    return get_config().get('performance', {}).get('enable_parallel_processing', True)

def get_progress_interval():
    """Get progress report interval in seconds."""
    return get_config().get('performance', {}).get('progress_report_interval', 300)

def get_cache_config():
    """Get cache configuration."""
    return get_config().get('loading_strategy', {}).get('cache', {})

def validate_rule_id(rule_id):
    """Validate if rule ID is valid (builtin or extension/custom format)."""
    valid_builtin = get_rule_ids()
    if rule_id in valid_builtin:
        return True, 'builtin'
    
    cfg = get_config()
    custom_cfg = cfg.get('custom_rules_config', {})
    
    ext_pattern = custom_cfg.get('rule_types', {}).get('extension', {}).get('id_pattern', 'R{NNN}_EXT')
    custom_pattern = custom_cfg.get('rule_types', {}).get('custom', {}).get('id_pattern', 'C{NNN}')
    
    if '_EXT' in rule_id:
        return True, 'extension'
    if rule_id.startswith('C') and rule_id[1:].isdigit():
        return True, 'custom'
    
    return False, None

def get_sta_applicability():
    """Get Sta applicability configuration."""
    return get_config().get('sta_applicability', {})

def get_sta_inapplicable_rules():
    """Get rules that are not applicable to Sta projects."""
    sta_cfg = get_sta_applicability()
    return frozenset(sta_cfg.get('not_applicable', []))

def is_rule_sta_inapplicable(rule_id):
    """Check if a rule is not applicable to Sta projects."""
    return rule_id in get_sta_inapplicable_rules()

def reload_config(config_path=None):
    """Reload configuration from file."""
    global _config
    _config = None
    return load_config(config_path)