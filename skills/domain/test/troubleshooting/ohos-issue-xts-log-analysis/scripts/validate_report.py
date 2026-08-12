#!/usr/bin/env python3
"""
validate_report.py - XTS分析报告结构校验脚本（Low freedom强制门禁）

用法：
    python3 scripts/validate_report.py <报告.md> [<module_run.log>] [<crash_log目录>]

校验项：
    1. 报告含2章节（一、hilog日志用例详情 + 二、总结）
    2. 每个FAILED用例含6段落标题
    3. 崩溃/冻结检测：crash_log有cppcrash→报告有崩溃分析节；有appfreeze→报告有BLOCKED类型A节
    4. BLOCKED计数交叉校验：FAILED+BLOCKED+PASSED = Collected test count
    5. 分层统计完整性：每个FAILED用例含 主/P1/P2/P3 统计
    6. 禁止XXX占位符
    7. 时间窗：起始行号 < 结束行号

退出码：0=通过，1=有错误（必须修正），2=有警告（建议修正）
"""

import sys
import re
import os
import glob
import json
from datetime import datetime


def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ 无法读取文件 {path}: {e}")
        sys.exit(1)


def find_crash_logs(crash_dir):
    """检测crash_log目录中的cppcrash和appfreeze文件"""
    cppcrash_count = 0
    has_appfreeze = False
    if crash_dir and os.path.isdir(crash_dir):
        for f in os.listdir(crash_dir):
            if 'cppcrash' in f.lower() and f.endswith('.log'):
                cppcrash_count += 1
            if 'appfreeze' in f.lower():
                has_appfreeze = True
    return cppcrash_count, has_appfreeze


def parse_module_run_stats(module_run_log):
    """从module_run.log解析测试统计"""
    stats = {
        'collected': 0,
        'failed': 0,
        'blocked': 0,
        'missed_tests': 0,
        'missed_suites': 0,
    }
    if not module_run_log or not os.path.isfile(module_run_log):
        return stats

    content = read_file(module_run_log)

    # Collected suite count
    m = re.search(r'Collected suite count is:\s*\d+,\s*test count is:\s*(\d+)', content)
    if m:
        stats['collected'] = int(m.group(1))

    # FAILED count
    stats['failed'] = len(re.findall(r'\] \[Listener\].*FAILED', content))

    # BLOCKED count
    stats['blocked'] = len(re.findall(r'\] \[Listener\].*BLOCKED', content))

    # missed
    for m in re.finditer(r'(\d+) tests in \S+ had missed', content):
        stats['missed_tests'] += int(m.group(1))
    for m in re.finditer(r'(\d+) suites have missed', content):
        stats['missed_suites'] += int(m.group(1))

    return stats


def _find_parsed_hilog_files(report_path):
    """查找报告同级的解密后 hilog txt（hilog_*_parsed/**/*.txt 或 hilog_*/_parsed/**/*.txt）"""
    report_dir = os.path.dirname(os.path.abspath(report_path))
    parsed = []
    # 模式1: hilog_*_parsed/ (sibling directory, parallel_decrypt默认输出)
    for entry in glob.glob(os.path.join(report_dir, 'hilog_*_parsed')):
        if os.path.isdir(entry):
            parsed += glob.glob(os.path.join(entry, '*.txt'))
        elif os.path.isfile(entry) and entry.endswith('.txt'):
            parsed.append(entry)
    # 模式2: hilog_*/_parsed/ (subdirectory, 某些解密工具输出到此结构)
    for entry in glob.glob(os.path.join(report_dir, 'hilog_*', '_parsed')):
        if os.path.isdir(entry):
            parsed += glob.glob(os.path.join(entry, '*.txt'))
    return parsed


def _check_cited_hilog_realness(report, parsed_files):
    """
    取数真实性校验(C1)：提取报告中引用的 hilog 行，验证其在解密后 hilog 中真实存在。
    报告可能裁剪行首行号前缀/trace-id，故仅校验“消息片段”是否作为子串出现。
    返回疑似伪造/无法核对的行列表（最多 5 条）。
    """
    fabricated = []
    if not parsed_files:
        return None  # 无解密 hilog → 跳过(由解密门禁处理)，返回 None 表示跳过
    # 构建搜索语料
    corpus_parts = []
    for pf in parsed_files:
        try:
            with open(pf, 'r', encoding='utf-8', errors='ignore') as f:
                corpus_parts.append(f.read())
        except Exception:
            pass
    corpus = '\n'.join(corpus_parts)

    # 提取 ``` 围栏代码块
    blocks = re.findall(r'```[^\n]*\n(.*?)```', report, re.DOTALL)
    hilog_line_re = re.compile(
        r'^\s*(?:\d+\s+)?(\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d{3})\s+(\d+)\s+(\d+)\s+([DIWEF])\s+\S+/([^:]+):\s*(.+)$'
    )
    for block in blocks:
        for raw in block.split('\n'):
            m = hilog_line_re.match(raw)
            if not m:
                continue
            msg = m.group(6).strip()  # 第6组为消息体（第5组是 tag）
            # 去掉行首 [trace-id] 前缀后取稳定消息片段
            frag = re.sub(r'^(\[[^\]]*\]\s*)+', '', msg)[:40].strip()
            if len(frag) < 8:
                continue
            if frag not in corpus:
                fabricated.append(frag)
                if len(fabricated) >= 5:
                    return fabricated
    return fabricated


def _count_crash_timeline_timestamps(report, cppcrash_count):
    """崩溃时间线完整性(C2)：统计崩溃分析节中出现的去重全格式崩溃时间戳数。"""
    if cppcrash_count < 2:
        return None
    # 截取崩溃分析节（从"崩溃分析/1.1 崩溃"到下一个 ### 1.X）
    m = re.search(r'(崩溃分析|1\.1\s*崩溃|崩溃根因).*?(?=\n###\s+1\.\d+|\Z)', report, re.DOTALL)
    section = m.group(0) if m else report
    # 匹配全格式(2026-06-30 00:34:15.847)和短格式(06-30 00:34:15.847)
    ts = set(re.findall(r'(?:\d{4}-)?\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}\.\d{3}', section))
    return len(ts)


def _record_state(report_path, passed, exit_code, count):
    """硬门禁状态记录——写状态文件（不致命）"""
    try:
        report_dir = os.path.dirname(os.path.abspath(report_path))
        status = {
            'report': os.path.basename(report_path),
            'passed': bool(passed),
            'exit_code': exit_code,
            'count': count,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        with open(os.path.join(report_dir, '.report_validation_status'), 'w', encoding='utf-8') as f:
            json.dump(status, f, ensure_ascii=False, indent=2)
    except Exception:
        pass  # 状态记录失败不影响校验本身


def validate_report(report_path, module_run_log=None, crash_dir=None):
    """主校验函数"""
    errors = []
    warnings = []

    report = read_file(report_path)
    report_lines = report.split('\n')

    # ========== 校验1：2章节结构 ==========
    has_chapter1 = bool(re.search(r'##\s*一[、\.].*hilog', report))
    has_chapter2 = bool(re.search(r'##\s*二[、\.].*总结', report))
    if not has_chapter1:
        errors.append("缺少「一、hilog日志用例详情」章节")
    if not has_chapter2:
        errors.append("缺少「二、总结」章节")

    # ========== 校验2：FAILED用例6段落 ==========
    # 查找所有用例节标题（### 1.X 用例名）
    case_sections = re.findall(r'###\s+1\.\d+\s+(.+?)(?:\n|$)', report)
    # 排除非用例节（崩溃分析/级联阻塞/汇总等）
    skip_keywords = ['崩溃', '级联', '阻塞', '汇总', 'BLOCKED类型', 'media_service']
    case_sections = [c.strip() for c in case_sections
                     if not any(kw in c for kw in skip_keywords)]

    # 完整用例需6段落，同根因用例只需4段落（基本信息+时间窗+根因继承+定界）
    six_paragraphs = ['基本信息', '时间窗', '证据链', '关键日志', '源码定位', '问题定界']
    same_root_paragraphs = ['基本信息', '时间窗', '定界']  # 同根因用例最低要求

    for case_name in case_sections:
        pattern = rf'###\s+1\.\d+\s+{re.escape(case_name)}.*?(?=\n###\s+1\.\d+|\n---\s*$|\Z)'
        match = re.search(pattern, report, re.DOTALL)
        if match:
            section_content = match.group()
            is_same_root = '同根因' in case_name
            required = same_root_paragraphs if is_same_root else six_paragraphs
            for para in required:
                if para not in section_content:
                    level = '⚠️' if is_same_root else '❌'
                    msg = f"用例「{case_name}」缺少段落：{para}"
                    if is_same_root:
                        warnings.append(msg)
                    else:
                        errors.append(msg)

    # ========== 校验3：崩溃/冻结检测 ==========
    cppcrash_count, has_appfreeze = find_crash_logs(crash_dir)

    if cppcrash_count > 0:
        has_crash_section = bool(re.search(r'###\s+1\.1.*崩溃|崩溃分析|崩溃根因', report))
        if not has_crash_section:
            errors.append(f"检测到{cppcrash_count}个cppcrash文件，但报告中无崩溃分析节（1.1）")

    if has_appfreeze:
        has_appfreeze_section = bool(re.search(r'appfreeze|THREAD_BLOCK|BLOCKED类型A|BLOCKED.*类型A', report, re.IGNORECASE))
        if not has_appfreeze_section:
            errors.append("检测到appfreeze文件，但报告中无appfreeze/BLOCKED类型A分析节")

    # ========== 校验4：BLOCKED计数交叉校验 ==========
    if module_run_log and os.path.isfile(module_run_log):
        stats = parse_module_run_stats(module_run_log)
        total_blocked = stats['blocked'] + stats['missed_tests']

        # 从报告中提取BLOCKED统计（多种格式兼容）
        report_blocked = -1
        for pattern in [r'阻塞用例总数\s*\|\s*(\d+)', r'BLOCKED.*?(\d+)\s*个', r'(\d+)\s*BLOCKED', r'阻塞.*?(\d+)']:
            m = re.search(pattern, report)
            if m:
                report_blocked = int(m.group(1))
                break

        if total_blocked > 0:
            if report_blocked < 0:
                errors.append(
                    f"报告中未找到BLOCKED计数，module_run.log应有{total_blocked}条"
                    f"(BLOCKED={stats['blocked']} + missed={stats['missed_tests']})"
                )
            elif report_blocked != total_blocked:
                errors.append(
                    f"BLOCKED计数不一致：报告={report_blocked}，module_run.log={total_blocked} "
                    f"(BLOCKED={stats['blocked']} + missed={stats['missed_tests']})，"
                    f"可能漏算套件内missed({stats['missed_tests']}条)"
                )

        # 检查是否漏算missed
        if stats['missed_tests'] > 0:
            has_missed_in_report = bool(re.search(r'missed|套件内', report))
            if not has_missed_in_report:
                errors.append(
                    f"module_run.log有{stats['missed_tests']}条missed，但报告中未统计"
                )

    # ========== 校验5：分层统计完整性 ==========
    # 检查报告中的FAILED用例是否含分层统计
    # 兼容三种列/单元格式：执行结果|FAILED / 实际结果|FAILED(表头与FAILED分行则不匹配) / | FAILED |(单元格)
    failed_sections = re.findall(
        r'(?:执行结果|测试结果|实际结果|结果)\s*\|\s*FAILED|\|\s*FAILED\s*\|',
        report, re.IGNORECASE)
    if failed_sections:
        has_layered_stats = bool(re.search(r'主分析集|主.*domain.*匹配|P1扩展|P2扩展', report))
        if not has_layered_stats:
            errors.append("有FAILED用例但报告中无分层统计（主/P1/P2/P3），请用 filter_hilog.py --stats-only 补取")

        has_markers = bool(re.search(r'\[主\]|\[P1\]|\[P2\]|\[P3\]', report))
        if not has_markers:
            errors.append("有FAILED用例但报告中无[主]/[P1]/[P2]/[P3]分层标记，请用 filter_hilog.py --json 补取")

    # ========== 校验6：禁止XXX占位符 ==========
    xxx_patterns = re.findall(r'XXX|\.XXX|占位|推测\)', report)
    if xxx_patterns:
        errors.append(f"报告中发现{len(xxx_patterns)}处XXX占位符/推测标记，禁止使用（取不到写「未提取到」）")

    # ========== 校验7：时间窗起始<结束 ==========
    # 提取所有"起始行号 | 数字" 和 "结束行号 | 数字"
    start_lines = re.findall(r'起始行号\s*\|\s*(\d+)', report)
    end_lines = re.findall(r'结束行号\s*\|\s*(\d+)', report)

    for i in range(min(len(start_lines), len(end_lines))):
        s = int(start_lines[i])
        e = int(end_lines[i])
        if s >= e:
            errors.append(f"时间窗违规：起始行号({s}) >= 结束行号({e})，起始必须 < 结束，用 filter_hilog.py --extract-hypium 重取")

    # ========== 校验8：取数真实性(C1)——引用的hilog行必须真实存在 ==========
    parsed_files = _find_parsed_hilog_files(report_path)
    cited_check = _check_cited_hilog_realness(report, parsed_files)
    if cited_check is None:
        warnings.append("未找到解密后 hilog(_parsed/*.txt)，跳过引用行真实性校验（若含 hilog.*.gz 请先解密）")
    elif cited_check:
        sample = cited_check[0]
        errors.append(
            f"取数真实性校验失败：报告中引用的 {len(cited_check)} 条 hilog 行在解密后 hilog 中不存在(疑似伪造/编造)，"
            f"示例片段「{sample[:30]}…」。禁止编造日志，取不到请写「未提取到」并用 filter_hilog.py 重取"
        )

    # ========== 校验9：崩溃时间线完整性(C2)——cppcrash数=时间线条目数 ==========
    if cppcrash_count >= 2:
        tl_count = _count_crash_timeline_timestamps(report, cppcrash_count)
        if tl_count is not None and tl_count < cppcrash_count:
            warnings.append(
                f"崩溃时间线可能不完整：crash_log 有 {cppcrash_count} 个 cppcrash，但崩溃分析节仅列 {tl_count} 个去重崩溃时间戳，"
                f"请逐条列出全部 {cppcrash_count} 条（禁用「等」省略）"
            )

    # ========== 校验10：崩溃分析必须在1.1节（C3，2026-07-15新增）==========
    # why：崩溃是根因时，崩溃分析必须作为1.1节（所有FAILED/BLOCKED的根因引用起点），
    # 放在后面会导致后续用例无法引用根因，证据链断裂
    if cppcrash_count > 0:
        crash_at_1_1 = bool(re.search(r'###\s+1\.1\s+.*崩溃|###\s+1\.1\s+.*SIGSEGV|###\s+1\.1\s+.*cppcrash', report))
        crash_at_later = bool(re.search(r'###\s+1\.[2-9]\d?\s+.*崩溃分析|###\s+1\.3\s+.*崩溃', report))
        if not crash_at_1_1 and crash_at_later:
            errors.append(
                "崩溃分析节位置错误：应在1.1节（根因节，所有FAILED/BLOCKED引用起点），"
                "实际在1.3或之后。why：崩溃是根因时必须放最前，否则后续用例证据链断裂"
            )

    # ========== 校验11：appfreeze必须含主线程调用栈分析（C4，2026-07-15新增）==========
    # why：appfreeze的核心证据是主线程调用栈（显示阻塞函数），不含栈=纯猜测=定界必错。
    # 实测：Windows报告只写"可能原因: media_service崩溃后等待超时"（猜测），
    # 未提取栈中的sleep()+64←libavplayerndk.so，误判为系统侧（实际测试侧）
    if has_appfreeze:
        appfreeze_section = re.search(
            r'(appfreeze|THREAD_BLOCK|BLOCKED类型A).*?(?=\n###\s+1\.\d+|\n---\s*$|\Z)',
            report, re.DOTALL | re.IGNORECASE)
        if appfreeze_section:
            section_text = appfreeze_section.group()
            has_stack = bool(re.search(r'#\d{2}\s+pc\s+0x|pc\s+\w|调用栈|stack|Tid:\d+.*Name:', section_text))
            has_guess = bool(re.search(r'可能原因|推测原因|疑似原因', section_text))
            if not has_stack:
                errors.append(
                    "appfreeze分析节缺少主线程调用栈：必须从appfreeze-*.log提取主线程栈"
                    "（如 #00 pc 0x... sleep+64）并分析阻塞函数，禁止只用「可能原因」猜测。"
                    "why：栈是定界依据，无栈=猜测=必错（实测把测试侧sleep误判为系统侧）"
                )
            if has_guess and not has_stack:
                errors.append(
                    "appfreeze分析节使用「可能原因」而非调用栈证据："
                    "必须提取主线程调用栈定界，禁止猜测"
                )

    # ========== 校验12：行号禁止用~前缀/约数（C5，2026-07-15新增）==========
    # why：Windows报告用"~23220"代替精确行号，违反"禁止约N行"规则
    approx_lines = re.findall(r'[~～]\s*\d{3,}|约\s*\d{3,}\s*行', report)
    if approx_lines:
        errors.append(
            f"发现{len(approx_lines)}处近似行号（~前缀/约N行），禁止使用。"
            f"必须用 filter_hilog.py --extract-hypium --testcase <用例名> 取精确行号，"
            f"取不到写「未提取到」"
        )

    # ========== 校验13：多根因检测（C6，2026-07-15新增）==========
    # why：cppcrash+appfreeze同时存在时，可能是两个独立根因（崩溃→FAILED + sleep→appfreeze→BLOCKED），
    # 必须分别分析、分别定界。实测：Windows报告把appfreeze误归因为media_service崩溃（系统侧），
    # 实际是测试侧NAPI sleep()无限循环，导致172条BLOCKED误流转给系统团队
    if cppcrash_count > 0 and has_appfreeze:
        # 检查报告是否有两个独立的根因分析节
        crash_section = re.search(r'###\s+1\.1\s+.*崩溃.*?(?=\n###\s+1\.\d+|\Z)', report, re.DOTALL)
        appfreeze_section_pattern = re.search(
            r'###\s+1\.\d+\s+.*appfreeze.*?(?=\n###\s+1\.\d+|\Z)', report, re.DOTALL | re.IGNORECASE)
        if crash_section and appfreeze_section_pattern:
            # 检查两个节是否有不同的归属判定
            crash_text = crash_section.group()
            appfreeze_text = appfreeze_section_pattern.group()
            # 检查appfreeze节是否有独立的归属判定（不依赖崩溃节）
            has_independent_attribution = bool(
                re.search(r'测试侧|归属.*测试|归属.*NAPI|sleep|while.*true', appfreeze_text, re.IGNORECASE))
            all_system = bool(re.search(r'系统侧|系统服务', appfreeze_text)) and not has_independent_attribution
            if all_system:
                errors.append(
                    "多根因检测：同时存在cppcrash和appfreeze，但appfreeze分析节未识别为独立根因。"
                    "appfreeze的根因可能与崩溃不同（如测试侧sleep() vs 系统侧SIGSEGV），"
                    "必须提取主线程栈独立定界，禁止直接归因为「media_service崩溃导致」。"
                    "why：误判会导致172条BLOCKED误流转给系统团队（实际应流转给测试团队）"
                )

    # ========== 汇总输出 ==========
    print("=" * 70)
    print("📋 XTS分析报告结构校验")
    print("=" * 70)
    print(f"报告文件：{report_path}")
    print(f"报告行数：{len(report_lines)}")
    if crash_dir:
        print(f"崩溃日志：{cppcrash_count}个cppcrash, {'有' if has_appfreeze else '无'}appfreeze")
    if module_run_log and os.path.isfile(module_run_log):
        stats = parse_module_run_stats(module_run_log)
        total_blocked = stats['blocked'] + stats['missed_tests']
        print(f"module_run.log：Collected={stats['collected']}, FAILED={stats['failed']}, "
              f"BLOCKED={total_blocked}(显式{stats['blocked']}+missed{stats['missed_tests']})")
    print("-" * 70)

    if errors:
        print(f"❌ 错误（{len(errors)}项，必须修正）：")
        for e in errors:
            print(f"   ❌ {e}")

    if warnings:
        print(f"⚠️  警告（{len(warnings)}项，建议修正）：")
        for w in warnings[:10]:
            print(f"   ⚠️  {w}")
        if len(warnings) > 10:
            print(f"   ... 还有{len(warnings) - 10}条警告")

    if not errors and not warnings:
        print("✅ 校验通过，报告结构合规")
        _record_state(report_path, True, 0, len(warnings))
        return 0
    elif not errors:
        print(f"\n⚠️  有{len(warnings)}项警告，建议修正后重新校验")
        _record_state(report_path, True, 2, len(warnings))
        return 2
    else:
        print(f"\n❌ 有{len(errors)}项错误，必须修正后重新生成报告")
        print("=" * 70)
        print("🚫 报告未通过校验门禁，禁止交付：必须修正全部错误后重跑本脚本至 0 错误")
        print("    why：事后校验是最后一道闸；带错误交付=把定界错误流转给下游团队。")
        print("=" * 70)
        _record_state(report_path, False, 1, len(errors))
        return 1


def main():
    if len(sys.argv) < 2:
        print("用法: python3 scripts/validate_report.py <报告.md> [<module_run.log>] [<crash_log目录>]")
        print("示例: python3 scripts/validate_report.py XTS_Analysis_Report_20260714.md module_run.log crash_log_*/")
        sys.exit(1)

    report_path = sys.argv[1]
    module_run_log = sys.argv[2] if len(sys.argv) > 2 else None
    crash_dir = sys.argv[3] if len(sys.argv) > 3 else None

    # 自动查找crash_log目录
    if not crash_dir:
        report_dir = os.path.dirname(os.path.abspath(report_path))
        crash_dirs = glob.glob(os.path.join(report_dir, 'crash_log_*'))
        if crash_dirs:
            crash_dir = crash_dirs[0]

    # 自动查找module_run.log
    if not module_run_log:
        report_dir = os.path.dirname(os.path.abspath(report_path))
        mrl = os.path.join(report_dir, 'module_run.log')
        if os.path.isfile(mrl):
            module_run_log = mrl

    return validate_report(report_path, module_run_log, crash_dir)


if __name__ == '__main__':
    sys.exit(main())
