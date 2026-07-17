#!/usr/bin/env python3
"""
SO崩溃栈快速分析示例
演示如何使用SO库映射功能分析崩溃栈
"""

import sqlite3
import os
import re

DB_PATH = os.path.expanduser('~/.opencode/skills/xts-issue-analysis/data/xts_rules.db')

def extract_so_from_backtrace(backtrace):
    """从崩溃栈提取SO库名"""
    pattern = r'#\d+ pc [\da-f]+ /system/lib64/(.+\.so)'
    matches = re.findall(pattern, backtrace)
    return matches

def query_so_subsystem(so_name):
    """查询SO库的子系统归属"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT subsystem, description, owner_name, owner_zhanma
        FROM so_mapping
        WHERE so_name = ?
    ''', (so_name,))
    
    result = cursor.fetchone()
    conn.close()
    return result

def analyze_crash_stack(backtrace):
    """分析崩溃栈并定界"""
    so_list = extract_so_from_backtrace(backtrace)
    
    if not so_list:
        print("❌ 未找到系统SO库，可能是应用私有库崩溃")
        return
    
    print("=" * 70)
    print("崩溃栈分析结果")
    print("=" * 70)
    
    print("\n【崩溃栈SO库列表】")
    for i, so in enumerate(so_list, 1):
        result = query_so_subsystem(so)
        if result:
            subsystem, desc, owner, zhanma = result
            owner_info = f" [{owner}({zhanma})]" if owner else ""
            print(f"{i}. {so}")
            print(f"   子系统: {subsystem}")
            print(f"   说明: {desc or '无'}{owner_info}")
        else:
            print(f"{i}. {so}")
            print(f"   ❌ 未找到映射，需添加到数据库")
    
    # 分析主崩溃点
    main_crash_so = so_list[0]
    main_result = query_so_subsystem(main_crash_so)
    
    if main_result:
        subsystem = main_result[0]
        
        print("\n【定界结论】")
        print(f"主崩溃库: {main_crash_so}（崩溃栈#00位置）")
        print(f"问题归属: {subsystem}子系统")
        
        # 生成调用链
        if len(so_list) > 1:
            chain = " → ".join([query_so_subsystem(so)[0] if query_so_subsystem(so) else "未知" for so in reversed(so_list)])
            print(f"调用链: {chain}")
        
        if main_result[2]:
            print(f"建议流转: {main_result[2]} ({main_result[3]})")
        else:
            print(f"建议流转: {subsystem}责任人（需查询contacts表）")
    
    print("=" * 70)

def main():
    # 示例崩溃栈
    example_backtrace = """
    #00 pc 00000000000a5b3c /system/lib64/libace.z.so
    #01 pc 00000000000c7a5d /system/lib64/libark_jsruntime.so
    #02 pc 00000000000b3f21 /system/lib64/libability_runtime.z.so
    """
    
    print("SO崩溃栈快速分析示例")
    print("\n输入示例崩溃栈：")
    print(example_backtrace)
    
    analyze_crash_stack(example_backtrace)

if __name__ == '__main__':
    main()