#!/usr/bin/env python3
"""
流程状态管理脚本

功能：
1. 检查流程状态文件是否存在
2. 读取当前执行阶段和已完成步骤
3. 更新流程状态（执行完成后）
4. 重置流程状态（重新分析时）

状态文件位置：<日志目录>/.xts_analysis_state.json
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

STATE_FILE_NAME = ".xts_analysis_state.json"

def get_state_file_path(log_dir):
    """获取状态文件路径"""
    return os.path.join(log_dir, STATE_FILE_NAME)

def init_state(log_dir):
    """初始化状态文件"""
    state_file = get_state_file_path(log_dir)
    
    # 确保目录存在
    os.makedirs(log_dir, exist_ok=True)
    
    state = {
        "log_dir": log_dir,
        "current_stage": None,
        "completed_steps": [],
        "failed_steps": [],
        "step_results": {},
        "start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    
    return state

def load_state(log_dir):
    """加载状态文件"""
    state_file = get_state_file_path(log_dir)
    
    if not os.path.exists(state_file):
        return None
    
    try:
        with open(state_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 状态文件读取失败: {e}")
        return None

def save_state(log_dir, state):
    """保存状态文件"""
    state_file = get_state_file_path(log_dir)
    
    state["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def check_step_completed(log_dir, step_name):
    """检查步骤是否已完成"""
    state = load_state(log_dir)
    
    if state is None:
        return False
    
    return step_name in state.get("completed_steps", [])

def mark_step_completed(log_dir, step_name, result=None):
    """标记步骤为已完成"""
    state = load_state(log_dir)
    
    if state is None:
        state = init_state(log_dir)
    
    if step_name not in state["completed_steps"]:
        state["completed_steps"].append(step_name)
    
    if result is not None:
        state["step_results"][step_name] = result
    
    save_state(log_dir, state)
    print(f"✅ 步骤已完成: {step_name}")

def mark_step_failed(log_dir, step_name, error=None):
    """标记步骤为失败"""
    state = load_state(log_dir)
    
    if state is None:
        state = init_state(log_dir)
    
    if step_name not in state["failed_steps"]:
        state["failed_steps"].append(step_name)
    
    if error is not None:
        if "step_results" not in state:
            state["step_results"] = {}
        state["step_results"][step_name] = {"status": "failed", "error": str(error)}
    
    save_state(log_dir, state)
    print(f"❌ 步骤失败: {step_name}")

def set_current_stage(log_dir, stage_name):
    """设置当前执行阶段"""
    state = load_state(log_dir)
    
    if state is None:
        state = init_state(log_dir)
    
    state["current_stage"] = stage_name
    save_state(log_dir, state)
    print(f"📍 当前阶段: {stage_name}")

def reset_state(log_dir):
    """重置状态文件"""
    state_file = get_state_file_path(log_dir)
    
    if os.path.exists(state_file):
        os.remove(state_file)
        print(f"✅ 状态文件已重置: {state_file}")
    else:
        print(f"ℹ️  状态文件不存在: {state_file}")

def print_state(log_dir):
    """打印状态信息"""
    state = load_state(log_dir)
    
    if state is None:
        print("❌ 状态文件不存在")
        return
    
    print("\n" + "="*70)
    print("流程状态信息")
    print("="*70)
    print(f"日志目录: {state.get('log_dir', 'N/A')}")
    print(f"当前阶段: {state.get('current_stage', '未开始')}")
    print(f"开始时间: {state.get('start_time', 'N/A')}")
    print(f"最后更新: {state.get('last_update', 'N/A')}")
    
    completed_steps = state.get("completed_steps", [])
    if completed_steps:
        print(f"\n已完成步骤 ({len(completed_steps)}个):")
        for i, step in enumerate(completed_steps, 1):
            print(f"  {i}. {step}")
    
    failed_steps = state.get("failed_steps", [])
    if failed_steps:
        print(f"\n失败步骤 ({len(failed_steps)}个):")
        for i, step in enumerate(failed_steps, 1):
            print(f"  {i}. {step}")
    
    print("="*70)

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 state_manager.py <命令> [参数]")
        print("\n命令列表:")
        print("  init <日志目录>              - 初始化状态文件")
        print("  check <日志目录> <步骤名>    - 检查步骤是否已完成")
        print("  complete <日志目录> <步骤名> - 标记步骤为已完成")
        print("  fail <日志目录> <步骤名>     - 标记步骤为失败")
        print("  stage <日志目录> <阶段名>    - 设置当前执行阶段")
        print("  reset <日志目录>             - 重置状态文件")
        print("  show <日志目录>              - 显示状态信息")
        print("\n示例:")
        print("  python3 state_manager.py init /path/to/logs")
        print("  python3 state_manager.py check /path/to/logs L0_PreAnalyze")
        print("  python3 state_manager.py complete /path/to/logs L1_Decrypt")
        print("  python3 state_manager.py show /path/to/logs")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "init":
        if len(sys.argv) < 3:
            print("❌ 缺少日志目录参数")
            sys.exit(1)
        log_dir = sys.argv[2]
        init_state(log_dir)
        print(f"✅ 状态文件已初始化: {get_state_file_path(log_dir)}")
    
    elif command == "check":
        if len(sys.argv) < 4:
            print("❌ 缺少参数")
            sys.exit(1)
        log_dir = sys.argv[2]
        step_name = sys.argv[3]
        completed = check_step_completed(log_dir, step_name)
        if completed:
            print(f"✅ 步骤已完成: {step_name}")
        else:
            print(f"⏳ 步骤未完成: {step_name}")
    
    elif command == "complete":
        if len(sys.argv) < 4:
            print("❌ 缺少参数")
            sys.exit(1)
        log_dir = sys.argv[2]
        step_name = sys.argv[3]
        mark_step_completed(log_dir, step_name)
    
    elif command == "fail":
        if len(sys.argv) < 4:
            print("❌ 缺少参数")
            sys.exit(1)
        log_dir = sys.argv[2]
        step_name = sys.argv[3]
        mark_step_failed(log_dir, step_name)
    
    elif command == "stage":
        if len(sys.argv) < 4:
            print("❌ 缺少参数")
            sys.exit(1)
        log_dir = sys.argv[2]
        stage_name = sys.argv[3]
        set_current_stage(log_dir, stage_name)
    
    elif command == "reset":
        if len(sys.argv) < 3:
            print("❌ 缺少日志目录参数")
            sys.exit(1)
        log_dir = sys.argv[2]
        reset_state(log_dir)
    
    elif command == "show":
        if len(sys.argv) < 3:
            print("❌ 缺少日志目录参数")
            sys.exit(1)
        log_dir = sys.argv[2]
        print_state(log_dir)
    
    else:
        print(f"❌ 未知命令: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()