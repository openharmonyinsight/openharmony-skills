#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同步 .oh-xts-config.json 中的 ets_version 到 APICoverageDetector/configs/arkts_config.json

用法：
    python scripts/sync_ets_version.py [--arkts-config-path PATH]
"""

import json
import os
import argparse
import sys

# 设置标准输出编码为 UTF-8
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


def load_global_config():
    """加载 .oh-xts-config.json"""
    script_dir = os.path.dirname(__file__)
    global_config_path = os.path.join(script_dir, '..', '.oh-xts-config.json')
    
    if not os.path.exists(global_config_path):
        raise FileNotFoundError(f".oh-xts-config.json not found at {global_config_path}")
    
    with open(global_config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    return config


def resolve_arkts_config_path(global_config, args_path):
    """Resolve arkts_config.json path, preferring scan_tool_root from config."""
    script_dir = os.path.dirname(__file__)
    scan_tool_root = global_config.get('scan_tool_root', '')
    if scan_tool_root and os.path.isdir(scan_tool_root):
        return os.path.join(scan_tool_root, 'configs', 'arkts_config.json')
    return os.path.join(script_dir, '..', args_path)


def sync_ets_version(global_config, arkts_config_path):
    """同步 ets_version 配置"""
    global_ets_version = global_config.get('ets_version', ['ets1.1'])
    
    if isinstance(global_ets_version, str):
        global_ets_version = [v.strip() for v in global_ets_version.split(',')]
    elif not isinstance(global_ets_version, list):
        raise ValueError(f"Invalid ets_version format in .oh-xts-config.json: {global_ets_version}")
    
    if not os.path.exists(arkts_config_path):
        raise FileNotFoundError(f"arkts_config.json not found at {arkts_config_path}")
    with open(arkts_config_path, 'r', encoding='utf-8') as f:
        arkts_config = json.load(f)
    
    # 备份原配置
    backup_path = arkts_config_path + '.bak'
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(arkts_config, f, indent=2, ensure_ascii=False)
    
    # 更新 ets_version
    old_ets_version = arkts_config.get('ets_version', [])
    arkts_config['ets_version'] = global_ets_version
    
    # 保存更新后的配置
    with open(arkts_config_path, 'w', encoding='utf-8') as f:
        json.dump(arkts_config, f, indent=2, ensure_ascii=False)
    
    return {
        'old_version': old_ets_version,
        'new_version': global_ets_version,
        'backup_path': backup_path
    }


def main():
    parser = argparse.ArgumentParser(description='Sync ets_version from .oh-xts-config.json to arkts_config.json')
    parser.add_argument('--arkts-config-path', type=str, 
                       default='APICoverageDetector/configs/arkts_config.json',
                       help='Path to arkts_config.json (relative to script root)')
    args = parser.parse_args()
    
    try:
        # 加载全局配置
        global_config = load_global_config()
        print("[OK] Loaded .oh-xts-config.json")
        
        arkts_config_path = resolve_arkts_config_path(global_config, args.arkts_config_path)
        
        # 同步配置
        result = sync_ets_version(global_config, arkts_config_path)
        print("[OK] Updated arkts_config.json")
        print(f"  Old version: {result['old_version']}")
        print(f"  New version: {result['new_version']}")
        print(f"  Backup saved to: {result['backup_path']}")
        
        print("\n[OK] ETS version synchronization completed successfully!")
        
    except Exception as e:
        print(f"[ERROR] {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
