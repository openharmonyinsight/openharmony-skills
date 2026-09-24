#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hi3861 MAP 文件分析工具

支持两种模式：
1. 单个 MAP 分析：统计各段大小，输出详细报告
2. 对比分析：比较两个 MAP 文件的差异

Usage:
    python map_analyzer.py analyze <map_file> [-o output.md]
    python map_analyzer.py compare <map_file1> <map_file2> [-o output.md]
"""

import os
import sys
import re
import argparse
from collections import defaultdict
from typing import Dict, List, Tuple


def parse_map_file(map_path: str) -> Dict:
    """解析 MAP 文件，提取段信息"""
    if not os.path.exists(map_path):
        raise FileNotFoundError(f"MAP file not found: {map_path}")

    sections = {}
    symbols = []

    with open(map_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    # 状态机：解析不同部分
    state = None
    current_section = None
    pending_section = None  # 换行段名暂存：段名独占一行时先记录，等下一行取地址/大小

    for i, line in enumerate(lines):
        line = line.rstrip()

        # 检测段开始
        # 格式: .text          0x0000000008000000    0x1234
        section_match = re.match(r'^\.([\w.]+)\s+0x([0-9a-fA-F]+)\s+0x([0-9a-fA-F]+)', line)
        if section_match:
            section_name = '.' + section_match.group(1)
            address = int(section_match.group(2), 16)
            size = int(section_match.group(3), 16)

            if size > 0:  # 只记录非空段
                sections[section_name] = {
                    'address': address,
                    'size': size,
                    'size_kb': size / 1024
                }
                current_section = section_name
                state = 'section'
                continue

        # 换行段名匹配：段名独占一行（如 .very_long_section_name），地址/大小在下一行
        # 格式: .very_long_section_name\n           0xADDR    0xSIZE
        pending_match = re.match(r'^\.([\w.]+)\s*$', line)
        if pending_match:
            pending_section = '.' + pending_match.group(1)
            continue

        # 换行段名的地址行：0xADDR    0xSIZE（pending_section 非空时匹配）
        if pending_section:
            cont_match = re.match(r'^\s+0x([0-9a-fA-F]+)\s+0x([0-9a-fA-F]+)', line)
            if cont_match:
                address = int(cont_match.group(1), 16)
                size = int(cont_match.group(2), 16)
                if size > 0:
                    sections[pending_section] = {
                        'address': address,
                        'size': size,
                        'size_kb': size / 1024
                    }
                    current_section = pending_section
                    state = 'section'
                pending_section = None
                continue
            else:
                # 下一行不是地址行，放弃暂存
                pending_section = None

        # 解析符号（在段内）
        # 格式:  0x0000000008000100                function_name
        if state == 'section' and current_section:
            symbol_match = re.match(r'^\s+0x([0-9a-fA-F]+)\s+(\S+)', line)
            if symbol_match:
                addr = int(symbol_match.group(1), 16)
                name = symbol_match.group(2)
                symbols.append({
                    'section': current_section,
                    'address': addr,
                    'name': name
                })

        # 检测段结束（空行或其他段开始）
        if state == 'section' and (line.strip() == '' or line.startswith('.')):
            state = None
            current_section = None

    return {
        'sections': sections,
        'symbols': symbols,
        'total_symbols': len(symbols)
    }


def estimate_symbol_sizes(symbols: List[Dict], sections: Dict) -> List[Dict]:
    """按段内相邻符号地址差估算符号大小（段内最后一个符号用段末地址）"""
    by_section = defaultdict(list)
    for sym in symbols:
        by_section[sym['section']].append(sym)
    for sec, syms in by_section.items():
        syms.sort(key=lambda s: s['address'])
        sec_info = sections.get(sec, {})
        sec_end = sec_info.get('address', 0) + sec_info.get('size', 0)
        for i, sym in enumerate(syms):
            next_addr = syms[i + 1]['address'] if i + 1 < len(syms) else sec_end
            sym['est_size'] = max(0, next_addr - sym['address'])
    return symbols


def ram_flash_split(sections: Dict) -> Dict:
    """RAM/Flash 口径拆分（Hi3861 L0：RAM=运行时占 SRAM 的段，Flash=只读存储段）

    RAM 口径：.data/.sdata/.bss/.sbss（含初始化数据的加载副本按平台惯例归 Flash，
    此处保守只按段名归属，未归类段单列 other 不强分）
    Flash 口径：.text/.init/.fini/.rodata/.rodata1
    """
    ram_secs = ('.data', '.sdata', '.bss', '.sbss')
    flash_secs = ('.text', '.init', '.fini', '.rodata', '.rodata1')
    ram = sum(i['size'] for n, i in sections.items() if n in ram_secs)
    flash = sum(i['size'] for n, i in sections.items() if n in flash_secs)
    other = sum(i['size'] for n, i in sections.items()
                if n not in ram_secs and n not in flash_secs)
    return {'ram': ram, 'flash': flash, 'other': other}


def analyze_single_map(map_path: str) -> Dict:
    """单个 MAP 文件分析"""
    data = parse_map_file(map_path)
    sections = data['sections']

    # 分类统计
    code_size = 0
    data_size = 0
    bss_size = 0
    rodata_size = 0
    other_size = 0

    for name, info in sections.items():
        size = info['size']
        if name in ['.text', '.init', '.fini']:
            code_size += size
        elif name in ['.data', '.sdata']:
            data_size += size
        elif name in ['.bss', '.sbss']:
            bss_size += size
        elif name in ['.rodata', '.rodata1']:
            rodata_size += size
        else:
            other_size += size

    total_size = code_size + data_size + bss_size + rodata_size + other_size

    # Top-N 段（按大小降序）+ 符号级估算大小
    top_sections = sorted(
        ((n, i['size']) for n, i in sections.items()),
        key=lambda x: x[1], reverse=True)
    sized_symbols = estimate_symbol_sizes(data['symbols'], sections)
    top_symbols = sorted(
        sized_symbols, key=lambda s: s.get('est_size', 0), reverse=True)

    return {
        'map_file': os.path.basename(map_path),
        'sections': sections,
        'summary': {
            'code': code_size,
            'data': data_size,
            'bss': bss_size,
            'rodata': rodata_size,
            'other': other_size,
            'total': total_size
        },
        'ram_flash': ram_flash_split(sections),
        'top_sections': top_sections,
        'top_symbols': top_symbols,
        'total_symbols': data['total_symbols']
    }


def compare_maps(map_path1: str, map_path2: str) -> Dict:
    """对比两个 MAP 文件"""
    data1 = analyze_single_map(map_path1)
    data2 = analyze_single_map(map_path2)

    sections1 = set(data1['sections'].keys())
    sections2 = set(data2['sections'].keys())

    # 找出差异
    added_sections = sections2 - sections1
    removed_sections = sections1 - sections2
    common_sections = sections1 & sections2

    # 计算大小变化
    changes = []
    for section in sorted(common_sections):
        size1 = data1['sections'][section]['size']
        size2 = data2['sections'][section]['size']
        diff = size2 - size1
        if diff != 0:
            changes.append({
                'section': section,
                'size1': size1,
                'size2': size2,
                'diff': diff,
                'diff_pct': (diff / size1 * 100) if size1 > 0 else float('inf')
            })

    # 按差异大小排序
    changes.sort(key=lambda x: abs(x['diff']), reverse=True)

    # 汇总对比
    summary_diff = {}
    for key in ['code', 'data', 'bss', 'rodata', 'other', 'total']:
        val1 = data1['summary'][key]
        val2 = data2['summary'][key]
        summary_diff[key] = val2 - val1

    # RAM/Flash 口径对比
    rf1 = data1['ram_flash']
    rf2 = data2['ram_flash']
    ram_flash_diff = {k: rf2[k] - rf1[k] for k in ('ram', 'flash', 'other')}

    # 符号级变化：两文件共有符号的估算大小差（按 |diff| 降序）
    sym_size1 = {(s['section'], s['name']): s.get('est_size', 0)
                 for s in data1['top_symbols']}
    sym_size2 = {(s['section'], s['name']): s.get('est_size', 0)
                 for s in data2['top_symbols']}
    symbol_changes = []
    for key in set(sym_size1) & set(sym_size2):
        d = sym_size2[key] - sym_size1[key]
        if d != 0:
            symbol_changes.append({
                'section': key[0], 'name': key[1],
                'size1': sym_size1[key], 'size2': sym_size2[key], 'diff': d})
    symbol_changes.sort(key=lambda x: abs(x['diff']), reverse=True)

    return {
        'map_file1': os.path.basename(map_path1),
        'map_file2': os.path.basename(map_path2),
        'analysis1': data1,
        'analysis2': data2,
        'added_sections': sorted(added_sections),
        'removed_sections': sorted(removed_sections),
        'changes': changes,
        'summary_diff': summary_diff,
        'ram_flash_diff': ram_flash_diff,
        'ram_flash1': rf1,
        'ram_flash2': rf2,
        'symbol_changes': symbol_changes
    }


def format_size(size_bytes: int) -> str:
    """格式化大小显示"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


def format_diff(diff: int) -> str:
    """格式化差异显示"""
    if diff > 0:
        return f"+{format_size(diff)}"
    elif diff < 0:
        return f"-{format_size(abs(diff))}"
    else:
        return "0"


def generate_single_report(analysis: Dict) -> str:
    """生成单个 MAP 分析报告"""
    lines = []
    lines.append(f"# MAP 文件分析报告\n")
    lines.append(f"**文件**: {analysis['map_file']}\n")
    lines.append(f"**符号总数**: {analysis['total_symbols']}\n")

    # 汇总
    lines.append("## 内存使用汇总\n")
    summary = analysis['summary']
    total = summary['total']

    lines.append("| 类别 | 大小 | 占比 |")
    lines.append("|------|------|------|")
    for category in ['code', 'data', 'bss', 'rodata', 'other']:
        size = summary[category]
        pct = (size / total * 100) if total > 0 else 0
        lines.append(f"| {category.upper()} | {format_size(size)} | {pct:.1f}% |")
    lines.append(f"| **总计** | **{format_size(total)}** | **100%** |")
    lines.append("")

    # RAM/Flash 口径
    lines.append("## RAM/Flash 口径\n")
    rf = analysis['ram_flash']
    lines.append("| 口径 | 大小 | 说明 |")
    lines.append("|------|------|------|")
    lines.append(f"| RAM（SRAM 运行时占用） | {format_size(rf['ram'])} | .data/.sdata/.bss/.sbss |")
    lines.append(f"| Flash（只读存储） | {format_size(rf['flash'])} | .text/.init/.fini/.rodata |")
    lines.append(f"| 未归类段 | {format_size(rf['other'])} | 平台特定段，按需人工归类 |")
    lines.append("")

    # Top 段（按大小降序 Top 10）
    lines.append("## Top 段（按大小，Top 10）\n")
    lines.append("| 段名 | 大小 |")
    lines.append("|------|------|")
    for name, size in analysis['top_sections'][:10]:
        lines.append(f"| {name} | {format_size(size)} |")
    lines.append("")

    # Top 符号（按估算大小 Top 20）
    lines.append("## Top 符号（按估算大小，Top 20）\n")
    lines.append("> 符号大小为段内相邻符号地址差估算值（est），非链接器精确值\n")
    lines.append("| 符号名 | 段 | 估算大小 |")
    lines.append("|--------|-----|---------|")
    for sym in analysis['top_symbols'][:20]:
        lines.append(f"| {sym['name']} | {sym['section']} | {format_size(sym.get('est_size', 0))} |")
    lines.append("")

    # 详细段列表
    lines.append("## 详细段列表（按段名排序）\n")
    lines.append("| 段名 | 地址 | 大小 |")
    lines.append("|------|------|------|")

    sections = analysis['sections']
    for name in sorted(sections.keys()):
        info = sections[name]
        addr = f"0x{info['address']:08X}"
        size = format_size(info['size'])
        lines.append(f"| {name} | {addr} | {size} |")
    lines.append("")

    return "\n".join(lines)


def generate_compare_report(comparison: Dict) -> str:
    """生成对比分析报告"""
    lines = []
    lines.append(f"# MAP 文件对比分析报告\n")
    lines.append(f"**文件 1**: {comparison['map_file1']}\n")
    lines.append(f"**文件 2**: {comparison['map_file2']}\n")

    # 汇总对比
    lines.append("## 内存使用对比\n")
    lines.append("| 类别 | 文件 1 | 文件 2 | 变化 |")
    lines.append("|------|--------|--------|------|")

    summary1 = comparison['analysis1']['summary']
    summary2 = comparison['analysis2']['summary']
    diff = comparison['summary_diff']

    for category in ['code', 'data', 'bss', 'rodata', 'other', 'total']:
        size1 = format_size(summary1[category])
        size2 = format_size(summary2[category])
        change = format_diff(diff[category])
        lines.append(f"| {category.upper()} | {size1} | {size2} | {change} |")
    lines.append("")

    # RAM/Flash 口径对比
    lines.append("## RAM/Flash 口径对比\n")
    rf1 = comparison['ram_flash1']
    rf2 = comparison['ram_flash2']
    rf_diff = comparison['ram_flash_diff']
    lines.append("| 口径 | 文件 1 | 文件 2 | 变化 |")
    lines.append("|------|--------|--------|------|")
    for key, label in [('ram', 'RAM（SRAM 运行时）'), ('flash', 'Flash（只读存储）'), ('other', '未归类段')]:
        lines.append(f"| {label} | {format_size(rf1[key])} | {format_size(rf2[key])} | {format_diff(rf_diff[key])} |")
    lines.append("")

    # 符号级变化 Top
    if comparison['symbol_changes']:
        lines.append("## 符号级变化 Top 20（按 |变化| 排序，估算大小）\n")
        lines.append("> 符号大小为段内相邻符号地址差估算值（est）\n")
        lines.append("| 符号名 | 段 | 文件 1 | 文件 2 | 变化 |")
        lines.append("|--------|-----|--------|--------|------|")
        for sc in comparison['symbol_changes'][:20]:
            lines.append(f"| {sc['name']} | {sc['section']} | "
                         f"{format_size(sc['size1'])} | {format_size(sc['size2'])} | "
                         f"{format_diff(sc['diff'])} |")
        lines.append("")

    # 段大小变化
    if comparison['changes']:
        lines.append("## 段大小变化（按差异排序）\n")
        lines.append("| 段名 | 文件 1 | 文件 2 | 变化 | 变化% |")
        lines.append("|------|--------|--------|------|-------|")

        for change in comparison['changes']:
            section = change['section']
            size1 = format_size(change['size1'])
            size2 = format_size(change['size2'])
            diff_str = format_diff(change['diff'])
            pct = f"{change['diff_pct']:+.1f}%" if change['diff_pct'] != float('inf') else "NEW"
            lines.append(f"| {section} | {size1} | {size2} | {diff_str} | {pct} |")
        lines.append("")

    # 新增段
    if comparison['added_sections']:
        lines.append("## 新增段（仅文件 2 有）\n")
        for section in comparison['added_sections']:
            size = comparison['analysis2']['sections'][section]['size']
            lines.append(f"- {section}: {format_size(size)}")
        lines.append("")

    # 移除段
    if comparison['removed_sections']:
        lines.append("## 移除段（仅文件 1 有）\n")
        for section in comparison['removed_sections']:
            size = comparison['analysis1']['sections'][section]['size']
            lines.append(f"- {section}: {format_size(size)}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='Hi3861 MAP 文件分析工具')
    subparsers = parser.add_subparsers(dest='command', help='命令')

    # analyze 子命令
    analyze_parser = subparsers.add_parser('analyze', help='分析单个 MAP 文件')
    analyze_parser.add_argument('map_file', help='MAP 文件路径')
    analyze_parser.add_argument('-o', '--output', help='输出 Markdown 文件路径')

    # compare 子命令
    compare_parser = subparsers.add_parser('compare', help='对比两个 MAP 文件')
    compare_parser.add_argument('map_file1', help='第一个 MAP 文件路径')
    compare_parser.add_argument('map_file2', help='第二个 MAP 文件路径')
    compare_parser.add_argument('-o', '--output', help='输出 Markdown 文件路径')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == 'analyze':
        print(f"分析 MAP 文件: {args.map_file}")
        analysis = analyze_single_map(args.map_file)
        report = generate_single_report(analysis)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"报告已保存: {args.output}")
        else:
            print("\n" + report)

    elif args.command == 'compare':
        print(f"对比 MAP 文件:")
        print(f"  文件 1: {args.map_file1}")
        print(f"  文件 2: {args.map_file2}")
        comparison = compare_maps(args.map_file1, args.map_file2)
        report = generate_compare_report(comparison)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"报告已保存: {args.output}")
        else:
            print("\n" + report)


if __name__ == '__main__':
    main()
