#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置验证工具
验证 .oh-xts-config.json 中的路径在当前平台下的有效性
"""

import os
import sys
import io
import argparse
import json
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def _resolve_derived_paths(config):
    platform_val = config.get('platform', '').lower()
    oh_root = config.get('OH_ROOT', '')
    derived = {}
    if oh_root:
        if not config.get('xts_acts_path'):
            derived['xts_acts_path'] = os.path.join(oh_root, 'test', 'xts', 'acts')
        # 源接口声明路径（兼容旧配置 sdk_path）
        if not config.get('interface_path') and not config.get('sdk_path'):
            derived['interface_path'] = os.path.join(oh_root, 'interface', 'sdk-js')
        # 编译后 SDK 路径（仅 use_builtin_sdk=False 时需要）
        use_builtin = config.get('use_builtin_sdk', True)
        if not use_builtin and not config.get('sdk_local_path'):
            ets_version = config.get('ets_version', ['ets1.1'])
            ver_num = ets_version[0].replace('ets', '') if ets_version else '1.1'
            derived['sdk_local_path'] = os.path.join(oh_root, 'prebuilts', 'ohos-sdk', 'linux', ver_num, 'ets')
        if not config.get('docs_path'):
            derived['docs_path'] = os.path.join(oh_root, 'docs')
    return derived


class ConfigValidator:

    def __init__(self):
        self.config_file = Path(__file__).parent.parent / '.oh-xts-config.json'

    def load_config(self):
        if not self.config_file.exists():
            print(f"❌ 配置文件不存在: {self.config_file}")
            return None
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ 配置文件格式错误: {e}")
            return None
        except Exception as e:
            print(f"❌ 读取配置文件失败: {e}")
            return None

    def validate_path(self, path, description, required=True):
        if path is None or path == '':
            if required:
                print(f"❌ {description}: 路径未配置")
                return False
            else:
                print(f"⚠️  {description}: 路径未配置（可选）")
                return True
        if not os.path.exists(path):
            print(f"❌ {description}: 路径不存在 - {path}")
            return False
        if not os.access(path, os.R_OK):
            print(f"❌ {description}: 路径不可读 - {path}")
            return False
        print(f"✅ {description}: 路径有效 - {path}")
        return True

    def validate_config(self, config):
        platform_val = config.get('platform', '').lower()
        print(f"\n=== 配置验证（platform: {platform_val}）===\n")
        all_valid = True

        all_valid &= self.validate_path(config.get('OH_ROOT'), 'OH_ROOT', required=True)
        all_valid &= self.validate_path(config.get('skill_root'), 'skill_root', required=True)
        all_valid &= self.validate_path(config.get('scan_tool_root'), 'scan_tool_root',
                                          required=(platform_val != 'linux'))

        xts_acts = config.get('xts_acts_path')
        derived = _resolve_derived_paths(config)
        if not xts_acts:
            xts_acts = derived.get('xts_acts_path', '')
        all_valid &= self.validate_path(xts_acts, 'xts_acts_path', required=True)

        # 源接口声明路径（兼容旧字段名 sdk_path）
        interface_path = config.get('interface_path') or config.get('sdk_path')
        if not interface_path:
            interface_path = derived.get('interface_path', '')
        self.validate_path(interface_path, 'interface_path (源接口声明)', required=False)

        # 编译后 SDK 路径
        use_builtin = config.get('use_builtin_sdk', True)
        if platform_val == 'wsl' and not use_builtin:
            sdk_local = config.get('sdk_local_path') or derived.get('sdk_local_path', '')
            all_valid &= self.validate_path(sdk_local, 'sdk_local_path (编译后 SDK)', required=True)
        elif use_builtin:
            builtin_sdk = os.path.join(config.get('scan_tool_root', ''), 'sdk', 'openharmony', 'ets')
            self.validate_path(builtin_sdk, '内置SDK (scan_tool_root/sdk/openharmony/ets)', required=False)

        if platform_val == 'windows':
            self.validate_path(config.get('deveco_studio_path'), 'deveco_studio_path', required=False)
            self.validate_path(config.get('hvigor_path_1.1'), 'hvigor_path_1.1', required=False)
            self.validate_path(config.get('hvigor_path_1.2'), 'hvigor_path_1.2', required=False)

        docs_path = config.get('docs_path') or derived.get('docs_path', '')
        self.validate_path(docs_path, 'docs_path', required=False)

        ets_version = config.get('ets_version', [])
        if not ets_version:
            print("❌ ets_version: 未配置")
            all_valid = False
        else:
            print(f"✅ ets_version: {ets_version}")

        return all_valid

    def show_config_status(self, config):
        print("\n=== 配置状态 ===\n")
        print(f"  platform: {config.get('platform', '未配置')}")
        for key in ['OH_ROOT', 'skill_root', 'scan_tool_root', 'ets_version',
                     'xts_acts_path', 'interface_path', 'sdk_local_path', 'use_builtin_sdk',
                     'deveco_studio_path', 'hvigor_path_1.1', 'hvigor_path_1.2', 'docs_path']:
            value = config.get(key)
            if value is not None and value != '':
                print(f"  {key}: {value}")

        derived = _resolve_derived_paths(config)
        if derived:
            print("\n  从 OH_ROOT 推导的路径:")
            for key, value in derived.items():
                if value:
                    print(f"    {key}: {value}")

    def validate(self):
        print("=== 配置验证工具 ===\n")
        config = self.load_config()
        if config is None:
            return False
        self.show_config_status(config)
        is_valid = self.validate_config(config)
        print("\n" + "=" * 50)
        if is_valid:
            print("✅ 配置验证通过！")
            return True
        else:
            print("❌ 配置验证失败！请检查上述错误信息。")
            print(f"💡 提示: 编辑配置文件 {self.config_file}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description='配置验证工具 - 验证 .oh-xts-config.json 中的路径有效性'
    )
    parser.parse_args()
    validator = ConfigValidator()
    is_valid = validator.validate()
    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
