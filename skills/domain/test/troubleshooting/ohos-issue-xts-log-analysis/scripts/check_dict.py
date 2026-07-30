#!/usr/bin/env python3
"""
dict 文件检测脚本（跨平台，Python 实现）

用途：自动检测 hilog 目录中的 dict 文件，并验证是否可用。
平台：Linux / Windows / macOS 均可运行（无需 bash/grep/find）。

用法:
    python3 check_dict.py <hilog日志目录>
    python3 check_dict.py D:\\logs\\hilog_FMR0123417000740
"""

import glob
import os
import platform
import sys


def human_size(num_bytes):
    """人类可读的文件大小"""
    for unit in ["B", "KB", "MB", "GB"]:
        if num_bytes < 1024.0:
            return f"{num_bytes:.1f}{unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f}TB"


def find_hilog_gz_files(log_dir):
    """递归查找所有 hilog.*.gz 文件"""
    pattern = os.path.join(log_dir, "**", "hilog.*.gz")
    return sorted(glob.glob(pattern, recursive=True))


def find_dict_files(log_dir):
    """查找 dict 文件（hilog_dict.*.zip 或 dict.zip）"""
    found = []
    # 顶层优先（与原 bash -maxdepth 1 行为一致）
    for name in ("hilog_dict.*.zip", "dict.zip"):
        found.extend(glob.glob(os.path.join(log_dir, name)))
    # 递归兜底（顶层未找到时）
    if not found:
        for name in ("hilog_dict.*.zip", "dict.zip"):
            found.extend(glob.glob(os.path.join(log_dir, "**", name), recursive=True))
    # 去重保序
    seen = set()
    uniq = []
    for f in found:
        if f not in seen:
            seen.add(f)
            uniq.append(f)
    return uniq


def recommend_command(log_dir, dict_file):
    """输出推荐的解密命令（跨平台）"""
    output_dir = f"{log_dir}_parsed"
    sep = "\\" if platform.system() == "Windows" else "/"
    # 确定脚本所在目录，给出 parallel_decrypt.py 的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pd_script = os.path.join(script_dir, "parallel_decrypt.py")

    lines = []
    lines.append("5. 推荐的解密命令（跨平台，推荐）：")
    lines.append("")
    lines.append('   # 推荐：使用 parallel_decrypt.py（自动适配 Windows原生 / Linux wine64）')
    lines.append(f'   python3 "{pd_script}" "{log_dir}"')
    lines.append("")
    lines.append("   # 手动指定输出目录与 dict 文件")
    lines.append(f'   python3 "{pd_script}" "{log_dir}" "{output_dir}" "{dict_file}"')
    lines.append("")
    lines.append("   # 若自动定位 hilogtool 失败，第5个参数直接传 hilogtool.exe 绝对路径")
    lines.append(f'   python3 "{pd_script}" "{log_dir}" "{output_dir}" "{dict_file}" 4 "<hilogtool.exe绝对路径>"')
    lines.append("")

    if platform.system() == "Windows":
        lines.append("   # Windows 原生直接运行（参考）")
        lines.append(f'   "<hilogtool.exe绝对路径>" parse -i "{log_dir}" -o "{output_dir}" -d "{dict_file}"')
    else:
        lines.append("   # Linux（参考，需 wine64）")
        lines.append(f'   DISPLAY= wine64 "<hilogtool.exe绝对路径>" parse -i "{log_dir}" -o "{output_dir}" -d "{dict_file}"')
    lines.append("")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("用法: python3 check_dict.py <hilog日志目录>")
        print("示例: python3 check_dict.py /path/to/hilog_FMR0123417000740")
        print("      python3 check_dict.py D:\\logs\\hilog_FMR0123417000740")
        sys.exit(1)

    log_dir = os.path.abspath(sys.argv[1])

    if not os.path.isdir(log_dir):
        print(f"错误：目录不存在: {log_dir}")
        sys.exit(1)

    print(f"=== 检查hilog日志目录: {log_dir} ===")
    print()

    # 1. 检查 hilog 文件
    gz_files = find_hilog_gz_files(log_dir)
    hilog_count = len(gz_files)
    print(f"1. hilog文件数量: {hilog_count}")
    if hilog_count == 0:
        print("   ⚠️  未找到hilog.*.gz文件")
        print()
        print("=== 检查完成 ===")
        sys.exit(0)
    else:
        print(f"   ✅ 找到 {hilog_count} 个hilog文件")
    print()

    # 2. 检查 dict 文件
    print("2. 检查dict文件...")
    dict_files = find_dict_files(log_dir)

    if not dict_files:
        print("   ❌ 未找到dict文件")
        print("   可能的原因：")
        print("   - dict文件在其他目录")
        print("   - dict文件未包含在日志包中")
        print()
        print("   建议：")
        print("   - 检查同批次其他测试目录")
        print("   - 联系测试环境负责人获取dict文件")
        sys.exit(1)

    print(f"   ✅ 找到 {len(dict_files)} 个dict文件：")
    for df in dict_files:
        try:
            size = os.path.getsize(df)
            size_str = human_size(size)
        except OSError:
            size_str = "?"
        print(f"   - {os.path.basename(df)} ({size_str})")
    print()

    # 3. 多个 dict 时建议用最近修改的
    if len(dict_files) > 1:
        print("3. ⚠️  检测到多个dict文件，建议使用时间戳最近的：")
        dict_files_sorted = sorted(dict_files, key=lambda f: os.path.getmtime(f), reverse=True)
        for df in dict_files_sorted[:5]:
            import time
            mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(df)))
            print(f"   - {os.path.basename(df)} (修改时间: {mtime})")
        print()

    # 4. dict 时间戳说明
    print("4. dict文件说明...")
    print("   ℹ️  dict时间戳与hilog时间戳不需要匹配")
    print("   - dict文件是密钥字典，与日志时间无关")
    print("   - 即使时间戳不同，也可以正常解密")
    print("   - 例如：dict时间20260626，hilog时间20260630，可以正常解密")
    print()

    # 5. 推荐解密命令
    print(recommend_command(log_dir, dict_files[0]))

    print("=== 检查完成 ===")


if __name__ == "__main__":
    main()
