#!/usr/bin/env python3
"""
preflight_gate.py - 报告生成前硬门禁（解密 + 取数前置校验）

定位：生成报告「之前」必跑的强制门禁；非 0 退出即禁止生成完整报告。
与 validate_report.py 职责不重叠：
  - preflight_gate : 生成前 → 「能不能开始取数」（hilog 是否解密）
  - validate_report: 生成后 → 「报告是否合规」（结构/计数/真实性）

用法：
    python3 scripts/preflight_gate.py <日志目录>

退出码：
    0 = 通过（已解密或无加密日志，可生成完整报告）
    1 = 解密硬门禁失败（含 hilog.*.gz 但未解密）→ 只许输出「解密失败桩报告」
    2 = dict 缺失（无法解密）→ 同上

设计理念：把 SKILL.md 的「解密硬门禁」从文字约束变成程序门禁。
  why：实测 Windows 端未解密即生成"看似完整"报告并伪造 hilog 内容；
       有 hilog.*.gz 却无解密产物时，定界=猜测=必错，必须硬拦。
"""

import os
import sys
import glob


def _find(log_dir, patterns, recursive=True):
    files = []
    for pat in patterns:
        if recursive:
            files += glob.glob(os.path.join(log_dir, '**', pat), recursive=True)
        else:
            files += glob.glob(os.path.join(log_dir, pat))
    # 去重 + 排除 Zone.Identifier 之类的 ADS 残留
    uniq = []
    for f in files:
        if f not in uniq and not f.endswith(':Zone.Identifier'):
            uniq.append(f)
    return uniq


def run_gate(log_dir):
    if not os.path.isdir(log_dir):
        print(f"❌ 日志目录不存在: {log_dir}")
        return 1

    gz = _find(log_dir, ['hilog.*.gz', '*.gz'])
    gz = [f for f in gz if 'hilog' in os.path.basename(f).lower() or f.endswith('.gz')]
    # 只关心 hilog 加密文件
    hilog_gz = [f for f in gz if os.path.basename(f).startswith('hilog') and f.endswith('.gz')]

    # 无加密日志 → 放行（纯 module_run.log 的 L1 有限分析是允许的）
    if not hilog_gz:
        print("✅ preflight 通过：未发现 hilog.*.gz（纯 module_run.log 场景，允许有限分析）")
        return 0

    # 有加密日志 → 必须有解密产物
    parsed_txt = _find(log_dir, ['*.txt'])  # *_parsed/*.txt
    parsed_txt = [f for f in parsed_txt if '_parsed' in f or f.endswith('.txt')]
    decrypt_state = _find(log_dir, ['.decrypt_state.json'])

    has_parsed_output = any(
        os.path.basename(f).startswith('hilog') and f.endswith('.txt')
        for f in _find(log_dir, ['*.txt'])
    )

    if (not has_parsed_output) and (not decrypt_state):
        # dict 是否存在（决定是 exit 1 还是 2）
        dict_files = _find(log_dir, ['hilog_dict*.zip', 'dict.zip', 'hilog_dict'])
        print("=" * 70)
        print("🚫 解密硬门禁失败：发现 hilog.*.gz 但未解密")
        print("=" * 70)
        print(f"日志目录: {log_dir}")
        print(f"加密 hilog: {len(hilog_gz)} 个")
        print(f"解密产物(*_parsed/*.txt): {'无' if not has_parsed_output else '有'}")
        print(f"decrypt_state: {'无' if not decrypt_state else '有'}")
        print()
        print("⚠️  解密硬门禁：含 hilog.*.gz 且未解密 → 禁止生成含")
        print("    「行号/domain分层/崩溃栈/定界结论」的完整报告。")
        print("    只可输出「解密失败桩报告」（失败原因 + 下方命令 + 解密后重新生成）。")
        print("    why：定界回答的是「为什么失败」，而「为什么」只在解密后的 hilog 里")
        print("    （崩溃栈/domain/行号）。module_run.log 只有结果没有根因，未解密即定界=猜测=必错。")
        print()
        print("【解密命令（跨平台，自动适配 Windows原生 / Linux wine64）】")
        print("  python3 scripts/check_dict.py <hilog目录>          # 先检查 dict")
        print("  python3 scripts/parallel_decrypt.py <hilog目录>    # 并行解密 → <目录>_parsed/")
        print("  python3 scripts/verify_dict_location.py <日志目录> # 解密后验证")
        if not dict_files:
            print()
            print("⚠️  未找到 dict 文件（hilog_dict*.zip / dict.zip），需先从设备获取字典后再解密")
            return 2
        return 1

    print("✅ preflight 通过：发现 hilog.*.gz 且已解密（有 _parsed/*.txt 或 decrypt_state）")
    print("ℹ️  取数铁律：filter_hilog.py 若返回 0 条结果，必须 debug（查正则/格式）或写「未提取到」，")
    print("    禁止改用文字描述或编造日志行（详见 AI_CONSTRAINTS 空结果处置铁律）")
    return 0


def main():
    if len(sys.argv) < 2:
        print("用法: python3 scripts/preflight_gate.py <日志目录>")
        print("退出码: 0=通过 1=未解密(硬门禁失败) 2=dict缺失")
        sys.exit(1)
    sys.exit(run_gate(sys.argv[1]))


if __name__ == '__main__':
    main()
