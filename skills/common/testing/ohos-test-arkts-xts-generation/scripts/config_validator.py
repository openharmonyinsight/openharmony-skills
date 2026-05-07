#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置验证工具
验证配置文件中的路径在当前平台下的有效性
"""

import os
import sys
import io
import json
import platform
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

class ConfigValidator:
    """配置验证器"""
    
    def __init__(self):
        """初始化验证器"""
        self.config_file = Path(__file__).parent.parent / '.oh-xts-config.json'
        self.current_platform = platform.system()  # Windows, Linux, Darwin
        
    def load_config(self):
        """加载配置文件"""
        if not self.config_file.exists():
            print(f"❌ 配置文件不存在: {self.config_file}")
            return None
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config
        except json.JSONDecodeError as e:
            print(f"❌ 配置文件格式错误: {e}")
            return None
        except Exception as e:
            print(f"❌ 读取配置文件失败: {e}")
            return None
    
    def validate_path(self, path, description, required=True):
        """验证单个路径"""
        if path is None:
            if required:
                print(f"❌ {description}: 路径未配置")
                return False
            else:
                print(f"⚠️  {description}: 路径未配置（可选）")
                return True
        
        path_obj = Path(path)
        
        if not path_obj.exists():
            print(f"❌ {description}: 路径不存在 - {path}")
            return False
        
        if not os.access(path, os.R_OK):
            print(f"❌ {description}: 路径不可读 - {path}")
            return False
        
        print(f"✅ {description}: 路径有效 - {path}")
        return True
    
    def validate_config(self, config):
        """验证配置"""
        print(f"\n=== 配置验证（当前平台: {self.current_platform}）===\n")
        
        all_valid = True
        
        if self.current_platform == 'Windows':
            win_config = config.get('for_windows', {})
            linux_config = config.get('for_linux', {})
            
            print("Windows 环境路径验证:")
            print("-" * 50)
            
            xts_acts_path = win_config.get('xts_acts_path')
            sdk_path = win_config.get('sdk_path')
            docs_path = win_config.get('docs_path')
            hvigor_path_1_1 = win_config.get('hvigor_path_1.1')
            hvigor_path_1_2 = win_config.get('hvigor_path_1.2')
            deveco_studio_path = win_config.get('deveco_studio_path')
            
            if not self.validate_path(xts_acts_path, 'xts_acts_path', required=True):
                all_valid = False
            
            if not self.validate_path(sdk_path, 'sdk_path', required=True):
                all_valid = False
            
            self.validate_path(hvigor_path_1_1, 'hvigor_path_1.1', required=False)
            self.validate_path(hvigor_path_1_2, 'hvigor_path_1.2', required=False)
            self.validate_path(deveco_studio_path, 'deveco_studio_path', required=False)
            
            if docs_path:
                self.validate_path(docs_path, 'docs_path', required=False)
            
            oh_root = linux_config.get('OH_ROOT')
            if oh_root:
                print(f"ℹ️  for_linux.OH_ROOT: Linux路径配置 - {oh_root}（当前Windows环境不使用）")
            
        elif self.current_platform == 'Linux':
            linux_config = config.get('for_linux', {})
            win_config = config.get('for_windows', {})
            
            print("Linux 环境路径验证:")
            print("-" * 50)
            
            oh_root = linux_config.get('OH_ROOT')
            if not self.validate_path(oh_root, 'OH_ROOT', required=True):
                all_valid = False
            
            xts_acts_path = win_config.get('xts_acts_path')
            sdk_path = win_config.get('sdk_path')
            docs_path = win_config.get('docs_path')
            
            if xts_acts_path:
                print(f"ℹ️  for_windows.xts_acts_path: Windows路径配置 - {xts_acts_path}（当前Linux环境不使用）")
            if sdk_path:
                print(f"ℹ️  for_windows.sdk_path: Windows路径配置 - {sdk_path}（当前Linux环境不使用）")
            if docs_path:
                print(f"ℹ️  for_windows.docs_path: Windows路径配置 - {docs_path}（当前Linux环境不使用）")
        
        else:
            print(f"⚠️  不支持的平台: {self.current_platform}")
            print("请根据实际需求配置路径")
        
        skill_root = config.get('skill_root')
        if not self.validate_path(skill_root, 'skill_root', required=True):
            all_valid = False
        
        return all_valid
    
    def show_config_status(self, config):
        """显示配置状态"""
        print("\n=== 配置状态 ===\n")
        
        win_config = config.get('for_windows', {})
        linux_config = config.get('for_linux', {})
        
        print("全局配置:")
        for key in ['skill_root', 'ets_version']:
            value = config.get(key)
            if value:
                print(f"  {key}: {value}")
            else:
                print(f"  {key}: 未配置")
        
        print("\nfor_windows 配置:")
        if win_config:
            for key, value in win_config.items():
                if value:
                    print(f"  {key}: {value}")
                else:
                    print(f"  {key}: 未配置")
        else:
            print("  (无)")
        
        print("\nfor_linux 配置:")
        if linux_config:
            for key, value in linux_config.items():
                if value:
                    print(f"  {key}: {value}")
                else:
                    print(f"  {key}: 未配置")
        else:
            print("  (无)")
        
        print(f"\n当前平台: {self.current_platform}")
        
        if self.current_platform == 'Windows':
            print("所需路径: for_windows.xts_acts_path, for_windows.sdk_path")
            print("可选路径: for_linux.OH_ROOT, for_windows.docs_path, for_windows.hvigor_path_1.1, for_windows.hvigor_path_1.2")
        elif self.current_platform == 'Linux':
            print("所需路径: for_linux.OH_ROOT")
            print("可选路径: for_windows.*（Windows环境使用）")
    
    def validate(self):
        """执行完整验证流程"""
        print("=== 配置验证工具 ===\n")
        
        # 加载配置
        config = self.load_config()
        if config is None:
            return False
        
        # 显示配置状态
        self.show_config_status(config)
        
        # 验证配置
        is_valid = self.validate_config(config)
        
        # 验证结果
        print("\n" + "=" * 50)
        if is_valid:
            print("✅ 配置验证通过！当前平台所需的路径均有效。")
            return True
        else:
            print("❌ 配置验证失败！请检查上述错误信息并修正配置。")
            print(f"💡 提示: 编辑配置文件 {self.config_file}")
            return False

def main():
    """主函数"""
    validator = ConfigValidator()
    is_valid = validator.validate()
    
    sys.exit(0 if is_valid else 1)

if __name__ == "__main__":
    main()