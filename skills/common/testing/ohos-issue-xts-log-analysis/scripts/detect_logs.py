#!/usr/bin/env python3
"""
日志文件检测脚本 - 纯检测，不分析

设计定位：
- ✅ 只检测日志文件状态
- ✅ 只输出提示信息
- ❌ 不做任何分析判断
- ❌ 不替代AI决策

AI应该：
1. 运行此脚本获取文件状态提示
2. 根据提示阅读文档要点
3. 主动调用工具（如hilogtool）解密
4. 主动分析日志内容
5. 主动生成报告
"""

import os
import sys
import glob
import subprocess
from pathlib import Path

def detect_log_files(log_dir):
    """
    检测日志目录中的文件状态，输出提示信息
    不做任何分析！
    """
    print("=" * 70)
    print("日志文件检测报告")
    print("=" * 70)
    print(f"日志目录: {log_dir}\n")
    
    # 检测各类日志文件
    log_files = {
        'task.log': False,
        'agent.log': False,
        'module_run.log': False,
        'hilog.log': False,
        'crash日志': 0,
        '加密hilog(.gz)': [],
        '加密hilog(.zst)': [],
        'hilog_dict文件': []
    }
    
    # 检测普通日志文件
    for log_name in ['task.log', 'agent.log', 'module_run.log', 'hilog.log']:
        log_path = os.path.join(log_dir, log_name)
        if os.path.exists(log_path):
            log_files[log_name] = True
            size = os.path.getsize(log_path)
            print(f"✅ {log_name}: 已找到 ({size} bytes)")
        else:
            print(f"❌ {log_name}: 未找到")
    
    # 检测crash日志
    crash_files = glob.glob(os.path.join(log_dir, '*crash*.log'))
    log_files['crash日志'] = len(crash_files)
    if crash_files:
        print(f"✅ crash日志: 找到 {len(crash_files)} 个文件")
        for f in crash_files:
            print(f"   - {os.path.basename(f)}")
    else:
        print(f"❌ crash日志: 未找到")
    
    # 检测加密hilog文件
    gz_files = glob.glob(os.path.join(log_dir, '**/*.gz'), recursive=True)
    zst_files = glob.glob(os.path.join(log_dir, '**/*.zst'), recursive=True)
    
    log_files['加密hilog(.gz)'] = gz_files
    log_files['加密hilog(.zst)'] = zst_files
    
    if gz_files:
        print(f"\n⚠️  发现加密hilog文件（.gz格式）")
        print(f"加密文件数量: {len(gz_files)} 个")
        print("加密文件列表:")
        for f in gz_files:
            rel_path = os.path.relpath(f, log_dir)
            size = os.path.getsize(f)
            print(f"   - {rel_path} ({size} bytes)")
    
    if zst_files:
        print(f"\n⚠️  发现加密hilog文件（.zst格式）")
        print(f"加密文件数量: {len(zst_files)} 个")
        print("加密文件列表:")
        for f in zst_files:
            rel_path = os.path.relpath(f, log_dir)
            size = os.path.getsize(f)
            print(f"   - {rel_path} ({size} bytes)")
    
    # 检测hilog_dict文件
    dict_files = glob.glob(os.path.join(log_dir, '**/hilog_dict*.zip'), recursive=True)
    dict_dirs = glob.glob(os.path.join(log_dir, '**/hilog_dict'), recursive=True)
    
    log_files['hilog_dict文件'] = dict_files + dict_dirs
    
    if dict_files or dict_dirs:
        print(f"\n✅ 找到hilog_dict字典文件")
        if dict_files:
            print(f"字典zip文件: {len(dict_files)} 个")
            for f in dict_files:
                rel_path = os.path.relpath(f, log_dir)
                print(f"   - {rel_path}")
        if dict_dirs:
            print(f"字典目录: {len(dict_dirs)} 个")
            for d in dict_dirs:
                rel_path = os.path.relpath(d, log_dir)
                print(f"   - {rel_path}/")
    
    # 输出解密提示（如果有加密文件）
    if gz_files or zst_files:
        print("\n" + "=" * 70)
        print("📌 解密方法提示")
        print("=" * 70)
        print("\n⚠️  说明：加密文件需要使用hilogtool解密")
        print("AI应该根据文档要点主动调用hilogtool\n")
        
        print("【文档要点位置】")
        print("  SKILL.md: 第2.5节 - hilogtool关键使用要点")
        print("  详细文档: docs/tools/hilogtool-guide.md\n")
        
        print("【工具位置】")
        print("  docs/tools/hilogtool/hilogtool.exe\n")
        
        if dict_files or dict_dirs:
            print("【dict字典文件】")
            print("  已找到dict文件，可用于解密")
            if dict_files:
                print(f"  建议：unzip {os.path.basename(dict_files[0])} -d hilog_dict")
            print()
        
        print("【核心命令参数】")
        print("  hilogtool parse -i <输入目录/文件> -o <输出目录> -d <dict目录>")
        print("  参数说明：")
        print("    -i : 输入文件或目录")
        print("    -o : 输出目录")
        print("    -d : dict字典目录")
        print()
        
        print("【AI调用示例】（根据文档动态执行）")
        print("  # 步骤1：解压dict字典（如有zip文件）")
        if dict_files:
            print(f"  unzip {os.path.basename(dict_files[0])} -d hilog_dict")
        print()
        print("  # 步骤2：使用hilogtool解密")
        print("  wine hilogtool.exe parse -i . -o hilog_decrypted -d hilog_dict")
        print()
        print("  # 步骤3：验证解密结果")
        print("  ls -lh hilog_decrypted/")
        print()
    
    # 输出后续分析提示
    print("=" * 70)
    print("后续分析提示")
    print("=" * 70)
    print("\n⚠️  重要：此脚本只做检测，不做分析！")
    print("\nAI应该：")
    print("1. ✅ 根据上述提示阅读文档要点")
    print("2. ✅ 如有加密文件，主动调用hilogtool解密")
    print("3. ✅ 使用辅助查询脚本（query_rules.py、query_so_mapping.py）")
    print("4. ✅ 分析日志内容，匹配关键字")
    print("5. ✅ 根据文档格式要求生成报告")
    print("\n辅助查询脚本示例：")
    print("  python3 query_rules.py App died")
    print("  python3 query_so_mapping.py libace.z.so")
    print("\n详细分析流程：参见 SKILL.md 核心分析流程章节")
    print("=" * 70)
    
    return log_files

def main():
    if len(sys.argv) < 2:
        print("用法: python3 detect_logs.py <日志目录>")
        print("\n功能：检测日志文件状态，输出提示信息")
        print("定位：纯检测脚本，不做分析判断")
        print("\n示例: python3 detect_logs.py /path/to/logs")
        sys.exit(1)
    
    log_dir = sys.argv[1]
    
    if not os.path.exists(log_dir):
        print(f"错误：目录不存在 - {log_dir}")
        sys.exit(1)
    
    detect_log_files(log_dir)

if __name__ == "__main__":
    main()