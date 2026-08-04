#!/usr/bin/env python3
"""
analyze_crash_stack.py - SO 崩溃栈快速分析

解析 cppcrash-*.log 文件（或含多个 crash 文件的目录），提取 Callstack 中的
#NN pc 行，解析 SO 库名，查询 xts_rules.db 的 so_mapping 表获取子系统归属与
责任人，输出定界结论。

用法：
    # 分析单个 cppcrash 文件
    python3 analyze_crash_stack.py /path/to/cppcrash-media_service-*.log

    # 分析 crash_log 目录下所有 cppcrash-*.log
    python3 analyze_crash_stack.py /path/to/crash_log_*/

    # 从标准输入解析崩溃栈文本
    grep -A 20 "Callstack" cppcrash-*.log | python3 analyze_crash_stack.py -

    # 运行内置示例（无参数时）
    python3 analyze_crash_stack.py --example
"""

import sqlite3
import os
import re
import sys
import glob as glob_module
import argparse

# 跨平台解析 DB 路径：多候选 + 标记文件验证
SKILL_NAME = "ohos-issue-xts-log-analysis"

def _is_skill_root(d):
    if not d or not os.path.isdir(d):
        return False
    return (
        os.path.isfile(os.path.join(d, "SKILL.md"))
        or os.path.exists(os.path.join(d, "data", "xts_rules.db"))
    )

def _resolve_skill_dir():
    env_dir = os.environ.get("OHS_XTS_SKILL_DIR")
    if env_dir and _is_skill_root(env_dir):
        return env_dir
    home = os.path.expanduser("~")
    try:
        p = os.path.abspath(__file__)
        for _ in range(5):
            if _is_skill_root(p):
                return p
            parent = os.path.dirname(p)
            if parent == p:
                break
            p = parent
    except Exception:
        pass
    candidates = [
        os.path.join(home, ".config", "opencode", "skills", SKILL_NAME),
        os.path.join(home, ".opencode", "skills", SKILL_NAME),
        os.path.join(home, ".opencode", ".config", "opencode", "skills", SKILL_NAME),
        os.path.join(home, ".claude", "skills", SKILL_NAME),
        os.path.join(home, ".agents", "skills", SKILL_NAME),
    ]
    cfg_dir = os.environ.get("OPENCODE_CONFIG_DIR")
    if cfg_dir:
        candidates.insert(0, os.path.join(cfg_dir, "skills", SKILL_NAME))
    for c in candidates:
        if _is_skill_root(c):
            return c
    return os.path.join(home, ".opencode", "skills", SKILL_NAME)

DB_PATH = os.path.join(_resolve_skill_dir(), 'data', 'xts_rules.db')

# 匹配 #NN pc <addr> <path>(<func>+<offset>) 格式的栈帧
# 兼容多种库路径：/system/lib64/, /system/lib64/media/, /system/lib64/platformsdk/,
# /system/lib/, /data/storage/.../, /system/lib/ld-musl-*.so.1 等
STACK_FRAME_RE = re.compile(
    r'^#(\d+)\s+pc\s+[\da-fA-Fx]+\s+(.+?\.so.*?)'
    r'(?:\((.+?)\))?'
    r'(?:\s*\([0-9a-fA-F]+\))?',
    re.MULTILINE
)

# 更宽容的 SO 库提取：从路径中提取 .so 文件名
SO_PATH_RE = re.compile(r'(/[^\s()]+\.so(?:\.\d+)?)')

def extract_so_from_backtrace(backtrace):
    """从崩溃栈文本提取 (帧号, SO库完整路径, 函数名) 列表"""
    frames = []
    for line in backtrace.splitlines():
        line = line.strip()
        m = re.match(r'^#(\d+)\s+pc\s+[\da-fA-Fx]+\s+(.+)', line)
        if not m:
            continue
        frame_num = int(m.group(1))
        rest = m.group(2)
        so_match = SO_PATH_RE.search(rest)
        if not so_match:
            continue
        so_path = so_match.group(1)
        so_name = os.path.basename(so_path)
        func_match = re.search(r'\(([^)]+)\)', rest)
        func_name = func_match.group(1) if func_match else ""
        frames.append((frame_num, so_name, so_path, func_name))
    return frames

def query_so_subsystem(so_name):
    """查询SO库的子系统归属"""
    if not os.path.exists(DB_PATH):
        return None
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

def parse_cppcrash_file(filepath):
    """解析单个 cppcrash-*.log 文件，提取关键字段"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        return {"file": filepath, "error": str(e)}

    info = {"file": os.path.basename(filepath)}

    # 提取 Reason
    reason_match = re.search(r'Reason:Signal:(\w+)', content)
    if reason_match:
        info["signal"] = reason_match.group(1)
    else:
        reason_match = re.search(r'Reason:(\w+)', content)
        if reason_match:
            info["signal"] = reason_match.group(1)

    # 提取 Process Name
    proc_match = re.search(r'Process Name:\s*(.+)', content)
    if proc_match:
        info["process"] = proc_match.group(1).strip()

    # 提取 Timestamp
    ts_match = re.search(r'Timestamp:\s*(.+)', content)
    if ts_match:
        info["timestamp"] = ts_match.group(1).strip()

    # 提取 Fault thread Name
    tid_match = re.search(r'Tid:\d+,\s*Name:(.+)', content)
    if tid_match:
        info["thread_name"] = tid_match.group(1).strip()

    # 提取 Callstack（#NN pc 行）
    callstack_lines = []
    for line in content.splitlines():
        if re.match(r'^#\d+\s+pc\s+', line.strip()):
            callstack_lines.append(line.strip())
    info["callstack"] = "\n".join(callstack_lines)

    return info

def collect_crash_files(path):
    """从文件/目录收集 cppcrash-*.log 文件列表"""
    if path == "-":
        return None  # stdin 模式
    if os.path.isfile(path):
        return [path]
    if os.path.isdir(path):
        files = sorted(glob_module.glob(os.path.join(path, "cppcrash-*.log")))
        if not files:
            files = sorted(glob_module.glob(os.path.join(path, "**", "cppcrash-*.log"), recursive=True))
        return files
    # glob 模式
    return sorted(glob_module.glob(path))

def analyze_crash_stack(backtrace, source_label=""):
    """分析崩溃栈并定界"""
    frames = extract_so_from_backtrace(backtrace)

    if not frames:
        print("❌ 未找到 SO 库栈帧（可能是纯 JS 崩溃或无 #NN pc 行）")
        return

    print("=" * 70)
    if source_label:
        print("崩溃栈分析结果 — {}".format(source_label))
    else:
        print("崩溃栈分析结果")
    print("=" * 70)

    print("\n【崩溃栈 SO 库列表】")
    so_results = {}
    for frame_num, so_name, so_path, func_name in frames:
        if so_name not in so_results:
            so_results[so_name] = query_so_subsystem(so_name)
        result = so_results[so_name]
        func_info = " ({})".format(func_name) if func_name else ""
        if result:
            subsystem, desc, owner, zhanma = result
            owner_info = " [{}({})]".format(owner, zhanma) if owner else ""
            print("  #{:<2} {}{}".format(frame_num, so_name, func_info))
            print("      路径: {}".format(so_path))
            print("      子系统: {}{}".format(subsystem, owner_info))
            print("      说明: {}".format(desc or "无"))
        else:
            print("  #{:<2} {}{}".format(frame_num, so_name, func_info))
            print("      路径: {}".format(so_path))
            print("      ❌ 未找到映射，需添加到数据库")

    # 分析主崩溃点（#00 或最低帧号）
    main_frame = min(frames, key=lambda f: f[0])
    main_so = main_frame[1]
    main_result = so_results.get(main_so)

    print("\n【定界结论】")
    print("主崩溃库: {}（崩溃栈#{}位置）".format(main_so, main_frame[0]))
    if main_frame[3]:
        print("崩溃函数: {}".format(main_frame[3]))

    if main_result:
        subsystem = main_result[0]
        print("问题归属: {}子系统".format(subsystem))

        # 生成调用链（从底到顶）
        chain_parts = []
        for _, so_name, _, _ in reversed(frames):
            r = so_results.get(so_name)
            chain_parts.append(r[0] if r else "未知({})".format(so_name))
        if len(chain_parts) > 1:
            print("调用链: {}".format(" → ".join(chain_parts)))

        if main_result[2]:
            print("建议流转: {} ({})".format(main_result[2], main_result[3]))
        else:
            print("建议流转: {}责任人（需查询contacts表）".format(subsystem))
    else:
        print("问题归属: 未知（{} 未在 so_mapping 表中）".format(main_so))
        print("建议流转: 需手动确认子系统归属")

    print("=" * 70)

def main():
    ap = argparse.ArgumentParser(
        description="SO 崩溃栈快速分析（解析 cppcrash 文件，查询 so_mapping 定界）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 分析单个 cppcrash 文件
  python3 analyze_crash_stack.py /path/to/cppcrash-media_service-*.log

  # 分析 crash_log 目录下所有 cppcrash
  python3 analyze_crash_stack.py /path/to/crash_log_*/

  # 从标准输入解析崩溃栈文本
  grep -A 20 "Callstack" cppcrash-*.log | python3 analyze_crash_stack.py -

  # 运行内置示例
  python3 analyze_crash_stack.py --example
        """,
    )
    ap.add_argument("path", nargs="?", help="cppcrash 文件/目录路径（省略时需配合 --example）")
    ap.add_argument("--example", action="store_true", help="运行内置示例崩溃栈")
    args = ap.parse_args()

    if args.example or not args.path:
        example_backtrace = """
#00 pc 0000000000138028 /system/lib64/media/libmedia_engine_histreamer.z.so(OHOS::Media::HiTransCoderImpl::OnEvent(OHOS::Media::Event const&)+80)
#01 pc 000000000008a698 /system/lib64/platformsdk/libmedia_foundation.z.so(OHOS::Media::TaskInner::HandleJob()+1336)
#02 pc 0000000000085fb0 /system/lib64/platformsdk/libmedia_foundation.z.so(OHOS::Media::PipeLineThread::Run()+908)
#03 pc 000000000008b8f4 /system/lib64/platformsdk/libmedia_foundation.z.so(OHOS::Media::Thread::Run(void*) (.cfi)+360)
#04 pc 00000000001e2d94 /system/lib/ld-musl-aarch64.so.1(start+240)
"""
        print("SO崩溃栈快速分析 — 内置示例\n")
        print("输入示例崩溃栈：")
        print(example_backtrace)
        analyze_crash_stack(example_backtrace, "内置示例")
        return

    if args.path == "-":
        # stdin 模式
        backtrace = sys.stdin.read()
        if not backtrace.strip():
            print("❌ 标准输入为空")
            sys.exit(1)
        analyze_crash_stack(backtrace, "stdin")
        return

    # 文件/目录模式
    crash_files = collect_crash_files(args.path)
    if not crash_files:
        print("❌ 未找到 cppcrash-*.log 文件: {}".format(args.path))
        sys.exit(1)

    print("找到 {} 个 cppcrash 文件\n".format(len(crash_files)))

    for i, filepath in enumerate(crash_files, 1):
        info = parse_cppcrash_file(filepath)
        if "error" in info:
            print("❌ 读取失败: {} ({})".format(filepath, info["error"]))
            continue

        print("#" * 70)
        print("# [{}/{}] {}".format(i, len(crash_files), info["file"]))
        print("#" * 70)

        if info.get("signal"):
            print("Reason: {}".format(info["signal"]))
        if info.get("process"):
            print("Process: {}".format(info["process"]))
        if info.get("timestamp"):
            print("Timestamp: {}".format(info["timestamp"]))
        if info.get("thread_name"):
            print("Thread: {}".format(info["thread_name"]))
        print()

        if not info.get("callstack"):
            print("⚠️  未找到 #NN pc 栈帧（可能不是 cppcrash 格式）\n")
            continue

        analyze_crash_stack(info["callstack"], info["file"])
        print()

if __name__ == '__main__':
    main()
