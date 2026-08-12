#!/usr/bin/env python3
"""
dict 位置验证脚本（跨平台，Python 实现）

用途：验证 dict 文件是否在正确位置，检测 cd 命令错误使用导致的 dict 污染。
支持：--clean 参数自动清理错误位置的 dict
平台：Linux / Windows / macOS 均可运行（无需 bash/du/awk）。

用法:
    python3 verify_dict_location.py <日志目录>
    python3 verify_dict_location.py <日志目录> --clean
"""

import json
import os
import shutil
import sys

SKILL_NAME = "ohos-issue-xts-log-analysis"


def _is_skill_root(d):
    if not d or not os.path.isdir(d):
        return False
    return (
        os.path.isfile(os.path.join(d, "SKILL.md"))
        or os.path.exists(os.path.join(d, "data", "xts_rules.db"))
        or os.path.isdir(os.path.join(d, "tools"))
    )


def _resolve_skill_dir():
    """跨平台解析 skill 根目录（与 parallel_decrypt.py 一致的多候选 + 递归搜索）。"""
    import glob

    env_dir = os.environ.get("OHS_XTS_SKILL_DIR")
    if env_dir and _is_skill_root(env_dir):
        return env_dir

    home = os.path.expanduser("~")

    # __file__ 向上查找
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

    # 常规候选
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

    # 递归搜索兜底
    try:
        search_bases = [os.path.join(home, ".opencode"), os.path.join(home, ".config", "opencode")]
        if cfg_dir:
            search_bases.insert(0, cfg_dir)
        for base in search_bases:
            if not os.path.isdir(base):
                continue
            for hit in glob.glob(os.path.join(base, "**", "skills", SKILL_NAME, "SKILL.md"), recursive=True):
                found = os.path.dirname(hit)
                if _is_skill_root(found):
                    return found
    except Exception:
        pass

    return os.path.join(home, ".opencode", "skills", SKILL_NAME)


def dir_size_human(path):
    """递归计算目录大小（人类可读），跨平台替代 du -sh"""
    total = 0
    for root, _dirs, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(root, f))
            except OSError:
                pass
    for unit in ["B", "KB", "MB", "GB"]:
        if total < 1024.0:
            return f"{total:.1f}{unit}"
        total /= 1024.0
    return f"{total:.1f}TB"


def main():
    auto_clean = False
    log_dir = None

    for arg in sys.argv[1:]:
        if arg == "--clean":
            auto_clean = True
        elif not arg.startswith("-") and log_dir is None:
            log_dir = arg

    if not log_dir:
        print("用法: python3 verify_dict_location.py <日志目录> [--clean]")
        print("示例: python3 verify_dict_location.py /path/to/hilog_FMR0123417000740")
        print("      python3 verify_dict_location.py /path/to/hilog_FMR0123417000740 --clean")
        print()
        print("参数说明:")
        print("  --clean    自动清理错误位置的dict目录")
        sys.exit(1)

    log_dir = os.path.abspath(log_dir)
    output_dir = f"{log_dir}_parsed"

    if not os.path.isdir(log_dir):
        print(f"错误：日志目录不存在: {log_dir}")
        sys.exit(1)

    print("=== 验证dict文件位置 ===")
    print()

    skill_dir = _resolve_skill_dir()
    skill_dict_dir = os.path.join(skill_dir, "dict")

    # 1. 检查技能目录下是否有 dict 文件（错误位置）
    if os.path.isdir(skill_dict_dir):
        size_str = dir_size_human(skill_dict_dir)
        print("❌ 错误：检测到技能目录下有dict文件")
        print(f"位置: {skill_dict_dir} ({size_str})")
        print("原因：执行hilogtool时可能使用了cd命令（错误做法）")
        print()

        if auto_clean:
            print("自动清理中...")
            try:
                shutil.rmtree(skill_dict_dir)
                print("✅ 已清理技能目录下的dict文件")
            except Exception as e:
                print(f"❌ 清理失败，请手动清理：")
                print(f"   rm -rf \"{skill_dict_dir}\"  (Linux/macOS)")
                print(f'   rmdir /s /q "{skill_dict_dir}"  (Windows cmd)')
                print(f'   Remove-Item -Recurse -Force "{skill_dict_dir}"  (PowerShell)')
        else:
            print("清理命令：")
            print(f'   Linux/macOS:  rm -rf "{skill_dict_dir}"')
            print(f'   Windows cmd:  rmdir /s /q "{skill_dict_dir}"')
            print(f'   PowerShell:   Remove-Item -Recurse -Force "{skill_dict_dir}"')
            print()
            print("或使用自动清理：")
            script = os.path.abspath(__file__)
            print(f'   python3 "{script}" "{log_dir}" --clean')
        print()
    else:
        print("✅ 技能目录下无dict文件（正确）")
        print()

    # 2. 检查输出目录
    if not os.path.isdir(output_dir):
        print(f"ℹ️  输出目录不存在: {output_dir}")
        print("   可能尚未解密")
        print()
        print("=== 验证完成 ===")
        return

    # 3. 检查输出目录下的 dict 位置
    expected_dict = os.path.join(output_dir, "dict")
    if os.path.isdir(expected_dict):
        size_str = dir_size_human(expected_dict)
        print(f"✅ dict文件位置正确: {expected_dict} ({size_str})")
    else:
        print("ℹ️  输出目录下无dict文件（可能已清理）")
    print()

    # 4. 检查解密状态文件
    state_file = os.path.join(output_dir, ".decrypt_state.json")
    if os.path.isfile(state_file):
        print(f"✅ 解密状态文件存在: {state_file}")
        print()
        print("状态信息：")
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                state = json.load(f)
            print(f"  解密时间: {state.get('decrypted_time', 'N/A')}")
            print(f"  成功文件: {state.get('success_files', 0)}/{state.get('total_files', 0)}")
            print(f"  并行解密: {'是' if state.get('parallel', False) else '否'}")
        except Exception:
            print("  （状态文件读取失败）")
    else:
        print("ℹ️  解密状态文件不存在")

    print()
    print("=== 验证完成 ===")


if __name__ == "__main__":
    main()
