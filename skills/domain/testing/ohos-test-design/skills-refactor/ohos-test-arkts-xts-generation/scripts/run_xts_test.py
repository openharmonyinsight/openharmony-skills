#!/usr/bin/env python3
"""
XTS Test Execution Script - 自动化测试执行与结果收集

在 WSL 环境下，将 acts 套件同步到 Windows 盘，通过 PowerShell 调用 xdevice 执行测试，
并收集结果到 .coverage_data 目录。

用法:
  python run_xts_test.py run --test-name <name> [--acts-source <path>] [--acts-win <path>]
  python run_xts_test.py status --report-dir <path>
  python run_xts_test.py parse --report-dir <path> [--output <path>]

前置条件:
  - Phase 8 编译成功，HAP 已生成
  - Windows 侧已安装 Python + xdevice (pip install)
  - 设备通过 USB 连接到 Windows，hdc.exe 可识别设备
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path


def get_config():
    """读取 agent 配置"""
    config_path = os.path.join(os.path.dirname(__file__), '..', '.oh-xts-config.json')
    config_path = os.path.abspath(config_path)
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return {}


def sync_acts_suite(acts_source: str, acts_win: str) -> bool:
    """同步 acts 套件到 Windows 盘"""
    acts_src = os.path.abspath(acts_source)
    acts_dst = os.path.abspath(acts_win)

    if not os.path.exists(acts_src):
        print(f"❌ acts 源目录不存在: {acts_src}")
        return False

    # 确保 Windows 侧目标目录存在
    os.makedirs(acts_dst, exist_ok=True)

    # 同步关键子目录
    for subdir in ['testcases', 'tools', 'config']:
        src = os.path.join(acts_src, subdir)
        dst = os.path.join(acts_dst, subdir)
        if os.path.exists(src):
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"  ✅ 同步 {subdir}/")

    # 同步必要文件
    for fname in ['run.bat', 'run.sh', 'user_config.xml']:
        src = os.path.join(acts_src, fname)
        dst = os.path.join(acts_dst, fname)
        if os.path.exists(src):
            shutil.copy2(src, dst)

    print(f"✅ acts 套件已同步到: {acts_dst}")
    return True


def run_test_via_windows(acts_win: str, test_name: str, timeout: int = 1800) -> dict:
    """通过 PowerShell 在 Windows 侧执行 xdevice 测试"""
    # Windows 路径转换
    acts_win_winpath = acts_win.replace('/mnt/', '').replace('/', '\\')
    # e.g. /mnt/d/acts_suite/acts -> D:\acts_suite\acts
    drive = acts_win_winpath[0].upper()
    acts_win_winpath = f"{drive}:{acts_win_winpath[1:]}"

    cmd = (
        f'cd {acts_win_winpath}; '
        f'python -m xdevice run -l {test_name} -t ACTS'
    )

    print(f"▶️ 执行测试: {test_name}")
    print(f"   目录: {acts_win_winpath}")
    print(f"   超时: {timeout}s")

    try:
        result = subprocess.run(
            ['powershell.exe', '-Command', cmd],
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        return {
            'success': result.returncode == 0,
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr,
        }
    except subprocess.TimeoutExpired:
        print(f"❌ 测试执行超时 ({timeout}s)")
        return {
            'success': False,
            'returncode': -1,
            'stdout': '',
            'stderr': f'Timeout after {timeout}s',
        }
    except Exception as e:
        print(f"❌ 测试执行异常: {e}")
        return {
            'success': False,
            'returncode': -2,
            'stdout': '',
            'stderr': str(e),
        }


def find_latest_report(acts_win: str) -> str:
    """找到最新的报告目录"""
    reports_dir = os.path.join(acts_win, 'reports')
    if not os.path.exists(reports_dir):
        return None

    report_dirs = sorted([
        d for d in os.listdir(reports_dir)
        if os.path.isdir(os.path.join(reports_dir, d))
    ], reverse=True)

    return os.path.join(reports_dir, report_dirs[0]) if report_dirs else None


def collect_results(report_dir: str, output_dir: str) -> dict:
    """收集测试结果到 output_dir"""
    if not report_dir or not os.path.exists(report_dir):
        print(f"❌ 报告目录不存在: {report_dir}")
        return {}

    os.makedirs(output_dir, exist_ok=True)

    collected = {
        'report_dir': report_dir,
        'files': [],
    }

    # 复制关键文件
    for fname in ['summary.ini', 'summary_report.xml', 'summary_report.html', 'task_info.record']:
        src = os.path.join(report_dir, fname)
        if os.path.exists(src):
            dst = os.path.join(output_dir, fname)
            shutil.copy2(src, dst)
            collected['files'].append(fname)

    # 复制详细结果 XML
    result_dir = os.path.join(report_dir, 'result')
    if os.path.exists(result_dir):
        for f in os.listdir(result_dir):
            if f.endswith('.xml'):
                src = os.path.join(result_dir, f)
                dst = os.path.join(output_dir, f)
                shutil.copy2(src, dst)
                collected['files'].append(f)

    # 复制 module_run.log
    log_dir = os.path.join(report_dir, 'log')
    if os.path.exists(log_dir):
        for module_dir in os.listdir(log_dir):
            module_log = os.path.join(log_dir, module_dir, 'module_run.log')
            if os.path.exists(module_log):
                dst = os.path.join(output_dir, f'{module_dir}_module_run.log')
                shutil.copy2(module_log, dst)
                collected['files'].append(f'{module_dir}_module_run.log')

            # 收集 hilog（压缩文件需要特殊处理）
            hilog_dir = os.path.join(log_dir, module_dir)
            if os.path.isdir(hilog_dir):
                for sn_dir in os.listdir(hilog_dir):
                    sn_path = os.path.join(hilog_dir, sn_dir)
                    if os.path.isdir(sn_path):
                        for hf in os.listdir(sn_path):
                            if hf.startswith('hilog.') and hf.endswith('.gz'):
                                src = os.path.join(sn_path, hf)
                                dst = os.path.join(output_dir, hf)
                                shutil.copy2(src, dst)
                                collected['files'].append(hf)

    print(f"✅ 结果已收集到: {output_dir}")
    print(f"   文件: {', '.join(collected['files'])}")
    return collected


def parse_xml_results(xml_path: str) -> dict:
    """解析 summary_report.xml"""
    if not os.path.exists(xml_path):
        print(f"❌ XML 文件不存在: {xml_path}")
        return {}

    tree = ET.parse(xml_path)
    root = tree.getroot()

    summary = {
        'total': int(root.get('tests', 0)),
        'passed': int(root.get('errors', 0)),  # will recalculate
        'failed': int(root.get('failures', 0)),
        'disabled': int(root.get('disabled', 0)),
        'ignored': int(root.get('ignored', 0)),
        'unavailable': int(root.get('unavailable', 0)),
        'modules': int(root.get('modules', 0)),
        'run_modules': int(root.get('runmodules', 0)),
        'suites': [],
    }

    passed_count = 0
    for suite in root.findall('testsuite'):
        suite_info = {
            'name': suite.get('name', ''),
            'tests': int(suite.get('tests', 0)),
            'failures': int(suite.get('failures', 0)),
            'disabled': int(suite.get('disabled', 0)),
            'time': float(suite.get('time', 0)),
            'cases': [],
        }

        for tc in suite.findall('testcase'):
            case = {
                'name': tc.get('name', ''),
                'classname': tc.get('classname', ''),
                'status': tc.get('status', ''),
                'result': tc.get('result', ''),
                'time': float(tc.get('time', 0)),
                'message': tc.get('message', ''),
            }
            suite_info['cases'].append(case)
            if case['result'] == 'true':
                passed_count += 1

        summary['suites'].append(suite_info)

    summary['passed'] = passed_count
    return summary


def analyze_failures(summary: dict) -> list:
    """分析失败用例，返回详细失败列表"""
    failures = []
    for suite in summary.get('suites', []):
        for tc in suite.get('cases', []):
            # 只关注 status=run 且 result=false 的（排除 disabled）
            if tc['result'] == 'false' and tc['status'] != 'disable':
                failures.append({
                    'suite': suite['name'],
                    'test': tc['name'],
                    'classname': tc['classname'],
                    'time': tc['time'],
                    'message': tc['message'],
                    'status': tc['status'],
                })
    return failures


def analyze_hilog(hilog_gz_path: str, test_name: str) -> dict:
    """从 hilog 中提取测试相关日志"""
    import gzip

    if not os.path.exists(hilog_gz_path):
        return {'error': f'File not found: {hilog_gz_path}'}

    result = {
        'test_logs': [],
        'errors': [],
        'status_codes': [],
    }

    try:
        with gzip.open(hilog_gz_path, 'rt', errors='replace') as f:
            for line in f:
                # 提取测试相关日志
                if test_name in line or 'JSAPP' in line:
                    if 'REPORT_STATUS' in line or 'specStart' in line or 'specDone' in line or 'pass' in line.lower() or 'fail' in line.lower():
                        result['test_logs'].append(line.strip())
                    if 'REPORT_STATUS_CODE' in line:
                        result['status_codes'].append(line.strip())
                    if ('Error' in line or 'error' in line or 'exception' in line) and 'JSAPP' in line:
                        result['errors'].append(line.strip())
    except Exception as e:
        result['error'] = str(e)

    return result


def generate_failure_report(failures: list, output_path: str, hilog_dir: str = None):
    """生成失败分析报告"""
    lines = [
        "# 测试执行失败分析报告",
        f"",
        f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"失败用例数: {len(failures)}",
        "",
    ]

    if not failures:
        lines.append("✅ 所有执行的测试用例均通过！")
        lines.append("")
    else:
        lines.append("## 失败用例详情")
        lines.append("")

        for i, f in enumerate(failures, 1):
            lines.append(f"### {i}. {f['suite']}#{f['test']}")
            lines.append(f"")
            lines.append(f"| 属性 | 值 |")
            lines.append(f"|------|-----|")
            lines.append(f"| 测试套 | {f['suite']} |")
            lines.append(f"| 用例名 | {f['test']} |")
            lines.append(f"| 类名 | {f['classname']} |")
            lines.append(f"| 执行时间 | {f['time']}s |")
            lines.append(f"| 状态 | {f['status']} |")
            lines.append(f"| 错误消息 | {f['message'] or '(无)'} |")
            lines.append(f"")

            # 从 hilog 分析
            if hilog_dir and os.path.isdir(hilog_dir):
                for hf in sorted(os.listdir(hilog_dir)):
                    if hf.startswith('hilog.') and hf.endswith('.gz'):
                        hilog_path = os.path.join(hilog_dir, hf)
                        hilog_result = analyze_hilog(hilog_path, f['test'])
                        if hilog_result.get('test_logs'):
                            lines.append(f"**Hilog 关键日志** (`{hf}`):")
                            lines.append(f"")
                            for log in hilog_result['test_logs'][-20:]:  # 最后 20 条
                                lines.append(f"```")
                                lines.append(log)
                                lines.append(f"```")
                            lines.append(f"")

            # 失败模式分析
            analysis = analyze_failure_pattern(f)
            lines.append(f"**失败模式分析**:")
            lines.append(f"")
            lines.append(f"{analysis}")
            lines.append(f"")
            lines.append(f"---")
            lines.append(f"")

    report = '\n'.join(lines)
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(report)
    print(f"✅ 失败分析报告已生成: {output_path}")
    return report


def analyze_failure_pattern(failure: dict) -> str:
    """根据失败模式推断根因"""
    suite = failure.get('suite', '')
    test = failure.get('test', '')
    msg = failure.get('message', '')
    time_s = failure.get('time', 0)

    patterns = []

    # 模式 1: time=0 且无消息 → done() 未调用 / 测试 hung
    if time_s == 0 and not msg:
        patterns.append(
            "- **疑似 done() 未调用**: 执行时间为 0，无错误消息。"
            "常见原因: 异步回调中 `done()` 未被调用，或 JS 运行时异常被默默吞掉。"
        )

    # 模式 2: message 包含 assertEqual / assertContain → 断言失败
    if 'assert' in msg.lower():
        patterns.append(
            "- **断言失败**: 测试断言不匹配，需检查预期值与实际值。"
        )

    # 模式 3: Inspector 模式测试
    if 'getInspectorByKey' in test or 'Jsunit' in suite:
        patterns.append(
            "- **Inspector 模式测试**: 该用例使用 `getInspectorByKey()` 验证组件属性。"
            "需检查: 1) Demo 页面是否正确渲染; 2) 控件 ID 是否匹配; "
            "3) Inspector 返回的属性格式是否变化。"
        )

    # 模式 4: mark blocked
    if 'blocked' in msg.lower():
        patterns.append(
            "- **用例被标记 blocked**: 该用例已知存在缺陷，已被标记跳过。"
            "无需修复，属于预期行为。"
        )

    if not patterns:
        patterns.append(
            "- **未知模式**: 需查看 hilog 详细日志进一步分析。"
            "建议: 1) 检查 module_run.log; 2) 搜索 hilog 中用例名相关日志; "
            "3) 关注 `[Hypium]` 和 `REPORT_STATUS_CODE` 行。"
        )

    return '\n'.join(patterns)


def cmd_run(args):
    """执行测试命令"""
    config = get_config()
    oh_root = config.get('OH_ROOT', '')

    acts_source = args.acts_source or os.path.join(
        oh_root, 'out/rk3568/suites/acts/acts'
    )
    acts_win = args.acts_win or '/mnt/d/acts_suite/acts'
    output_dir = args.output or '.coverage_data'

    # Step 1: 同步
    print("=== Step 1: 同步 acts 套件到 Windows 盘 ===")
    if not sync_acts_suite(acts_source, acts_win):
        sys.exit(1)

    # Step 2: 执行测试
    print("\n=== Step 2: 执行 XTS 测试 ===")
    result = run_test_via_windows(acts_win, args.test_name, args.timeout)

    # Step 3: 收集结果
    print("\n=== Step 3: 收集测试结果 ===")
    report_dir = find_latest_report(acts_win)
    if report_dir:
        test_output_dir = os.path.join(output_dir, 'test_execution')
        collected = collect_results(report_dir, test_output_dir)

        # Step 4: 解析结果
        print("\n=== Step 4: 解析测试结果 ===")
        xml_path = os.path.join(test_output_dir, 'summary_report.xml')
        if os.path.exists(xml_path):
            summary = parse_xml_results(xml_path)
            print(f"  总用例: {summary['total']}")
            print(f"  通过: {summary['passed']}")
            print(f"  失败: {summary['failed']}")
            print(f"  禁用: {summary['disabled']}")

            # Step 5: 分析失败
            failures = analyze_failures(summary)
            if failures:
                print(f"\n  ⚠️ 发现 {len(failures)} 个失败用例:")
                for f in failures:
                    print(f"    - {f['suite']}#{f['test']}")
            else:
                print(f"\n  ✅ 所有执行的测试用例均通过!")

            # 生成失败报告
            failure_report_path = os.path.join(
                test_output_dir, 'failure_analysis.md'
            )
            generate_failure_report(
                failures, failure_report_path, test_output_dir
            )

            # 保存摘要 JSON
            summary_path = os.path.join(test_output_dir, 'test_summary.json')
            with open(summary_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'summary': summary,
                    'failures': failures,
                    'timestamp': datetime.now().isoformat(),
                    'test_name': args.test_name,
                }, f, ensure_ascii=False, indent=2)

            return {
                'success': len(failures) == 0,
                'summary': summary,
                'failures': failures,
                'report_dir': test_output_dir,
            }
    else:
        print("❌ 未找到测试报告目录")

    return {'success': False}


def cmd_parse(args):
    """解析已有报告"""
    report_dir = args.report_dir
    output_dir = args.output or os.path.join(report_dir, 'analysis')

    xml_path = os.path.join(report_dir, 'summary_report.xml')
    if not os.path.exists(xml_path):
        # 尝试查找 result/ 下的 XML
        result_dir = os.path.join(report_dir, 'result')
        if os.path.exists(result_dir):
            for f in os.listdir(result_dir):
                if f.endswith('.xml'):
                    xml_path = os.path.join(result_dir, f)
                    break

    if not os.path.exists(xml_path):
        print(f"❌ 未找到 XML 报告: {report_dir}")
        sys.exit(1)

    summary = parse_xml_results(xml_path)
    failures = analyze_failures(summary)

    os.makedirs(output_dir, exist_ok=True)
    failure_report_path = os.path.join(output_dir, 'failure_analysis.md')
    generate_failure_report(failures, failure_report_path, report_dir)

    print(f"\n总用例: {summary['total']}")
    print(f"通过: {summary['passed']}")
    print(f"失败: {len(failures)}")
    print(f"禁用: {summary['disabled']}")


def main():
    parser = argparse.ArgumentParser(
        description='XTS Test Execution Script'
    )
    subparsers = parser.add_subparsers(dest='command')

    # run 命令
    p_run = subparsers.add_parser('run', help='执行测试并收集结果')
    p_run.add_argument('--test-name', required=True, help='测试名称 (e.g. ActsAceEtsModuleImageTextTextTest)')
    p_run.add_argument('--acts-source', help='acts 套件源目录 (默认从 config 推导)')
    p_run.add_argument('--acts-win', default='/mnt/d/acts_suite/acts', help='Windows 侧 acts 目录')
    p_run.add_argument('--output', default='.coverage_data', help='输出目录')
    p_run.add_argument('--timeout', type=int, default=1800, help='执行超时 (秒)')

    # parse 命令
    p_parse = subparsers.add_parser('parse', help='解析已有的测试报告')
    p_parse.add_argument('--report-dir', required=True, help='报告目录')
    p_parse.add_argument('--output', help='分析结果输出目录')

    args = parser.parse_args()

    if args.command == 'run':
        cmd_run(args)
    elif args.command == 'parse':
        cmd_parse(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
