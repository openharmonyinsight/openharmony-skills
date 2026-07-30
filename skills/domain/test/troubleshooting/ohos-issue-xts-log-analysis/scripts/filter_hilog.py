#!/usr/bin/env python3
"""
分层过滤脚本 - 用于精准过滤 hilog 日志

⚠️ **定位说明**：此脚本为**可选工具**，AI可以选择使用此脚本，也可以自己用 grep 实现。

**设计理念**：AI主导判断，脚本辅助查询。AI可以选择使用此脚本实现分层过滤，也可以自己实现。

**使用方式**：
- AI选择使用此脚本：调用脚本获取分层过滤结果
- AI选择自己实现：用 grep/sed 实现时间窗过滤、domain分组、渐进式扩展

根据 IMPROVEMENT_PLAN.md 的 A-3 分层过滤模型设计实现：
- Layer 1: 时间窗硬过滤
- Layer 2: domain 分组（主分析集 + 备用集）
- Layer 3: 渐进式扩展（PID/TID 优先 + 位置窗口兜底）
- cppcrash 独立通道

⭐ 新增功能：[Hypium]标记时间窗提取（替代module_run.log）

输出分层切片（带来源标记 [主]、[P1]、[P2]、[P3]）+ 统计信息

详细使用说明：见 docs/TOOLS.md
"""

import argparse
import gzip
import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class LogLine:
    """日志行数据结构"""
    line_num: int
    raw_line: str
    timestamp: Optional[datetime] = None
    pid: Optional[int] = None
    tid: Optional[int] = None
    level: Optional[str] = None
    domain: Optional[str] = None
    tag: Optional[str] = None
    message: Optional[str] = None
    is_parsed: bool = False


@dataclass
class FilterResult:
    """过滤结果"""
    primary_lines: List[LogLine] = field(default_factory=list)
    p1_lines: List[LogLine] = field(default_factory=list)
    p2_lines: List[LogLine] = field(default_factory=list)
    p3_lines: List[LogLine] = field(default_factory=list)
    backup_lines: List[LogLine] = field(default_factory=list)
    cppcrash_lines: List[str] = field(default_factory=list)
    
    stats: Dict = field(default_factory=dict)


@dataclass
class HypiumTimeWindow:
    """[Hypium]标记提取的时间窗"""
    testcase_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    start_line: int = 0
    end_line: int = 0
    status: str = "Unknown"  # "Running", "Passed", "Failed"
    consuming_ms: Optional[int] = None  # [fail] 行的 consuming 真实值
    end_marker: str = ""  # 结束标记类型: specDone/fail/pass/running


class HilogParser:
    """hilog 日志解析器"""
    
    PATTERN = re.compile(
        r'^(\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d{3})\s+'  # timestamp: 06-26 15:53:48.123
        r'(\d+)\s+'  # PID
        r'(\d+)\s+'  # TID
        r'([DIWEF])\s+'  # Level: D/I/W/E/F
        r'(?:[A-Z])?([0-9a-fA-F]{5})/'  # Domain (5 hex digits, optional type-letter prefix C/A/K)
        r'([^:]+):\s*'  # Tag
        r'(.*)$'  # Message
    )
    
    @classmethod
    def parse_line(cls, line: str, line_num: int) -> LogLine:
        """解析单行 hilog 日志"""
        log_line = LogLine(line_num=line_num, raw_line=line.strip())
        
        match = cls.PATTERN.match(line.strip())
        if match:
            try:
                timestamp_str = match.group(1)
                log_line.timestamp = datetime.strptime(f"2026-{timestamp_str}", "%Y-%m-%d %H:%M:%S.%f")
                log_line.pid = int(match.group(2))
                log_line.tid = int(match.group(3))
                log_line.level = match.group(4)
                log_line.domain = match.group(5).upper()
                log_line.tag = match.group(6).strip()
                log_line.message = match.group(7).strip()
                log_line.is_parsed = True
            except Exception:
                pass
        
        return log_line


class HypiumMarkerExtractor:
    """
    [Hypium]标记提取器 - 用于从hilog直接提取时间窗 ⭐ **新增功能**
    
    功能：
    - 提取[Hypium]start标记（用例开始）
    - 提取[Hypium]fail标记（用例失败）
    - 提取[Hypium]pass标记（用例通过）
    - 构建时间窗（设备时间）
    
    用途：
    - 替代module_run.log的时间窗提取功能
    - 在module_run.log缺失时，从hilog直接提取时间窗
    
    标记格式（兼容两种 hilog 输出）：
    - 旧版: [Hypium] start test: NAME / [Hypium] fail test: NAME / [Hypium] pass test: NAME
    - hilogtool 实测版: [Hypium]start running case 'NAME' / [Hypium][fail]NAME ; consuming Xms / [Hypium]NAME specDone end print success
    """
    
    # 多格式兼容：start running case 'NAME' | start test: NAME
    HYPIUM_START_PATTERN = re.compile(
        r"\[Hypium\]\s*(?:start\s+running\s+case\s+'([^']+)'|start\s+test:\s+(\w+))"
    )
    # 多格式兼容：[fail]NAME ; consuming Xms | fail test: NAME
    HYPIUM_FAIL_PATTERN = re.compile(
        r"\[Hypium\]\s*(?:\[fail\]\s*(\w+)|fail\s+test:\s+(\w+))(?:\s*;\s*consuming\s+(\d+)\s*ms)?"
    )
    # specDone 精确结束标记（优先级①）：NAME specDone end print success
    HYPIUM_SPECDONE_PATTERN = re.compile(
        r"\[Hypium\]\s*(\w+)\s+specDone\s+end\s+print\s+success"
    )
    # 多格式兼容：pass test: NAME（旧版）
    HYPIUM_PASS_PATTERN = re.compile(
        r"\[Hypium\]\s*pass\s+test:\s+(\w+)"
    )
    
    @classmethod
    def extract_time_windows(cls, hilog_lines: List[LogLine]) -> List[HypiumTimeWindow]:
        """
        从hilog日志提取[Hypium]标记时间窗
        
        Args:
            hilog_lines: 解析后的hilog日志行列表
        
        Returns:
            时间窗列表（每个用例一个时间窗）
        """
        time_windows = []
        testcase_start_map = {}  # testcase_name → HypiumTimeWindow
        
        for line in hilog_lines:
            if not line.message:
                continue
            
            # 检查[Hypium]start标记（兼容 start running case 'NAME' / start test: NAME）
            start_match = cls.HYPIUM_START_PATTERN.search(line.message)
            if start_match:
                testcase_name = start_match.group(1) or start_match.group(2)
                tw = HypiumTimeWindow(
                    testcase_name=testcase_name,
                    start_time=line.timestamp,
                    start_line=line.line_num,
                    status="Running"
                )
                testcase_start_map[testcase_name] = tw
            
            # 检查[Hypium][fail]标记（仅置 Failed 状态 + consuming + 暂定结束，不终结；
            # 精确结束由 specDone 给出，无 specDone 时回退到此暂定结束 = 优先级③）
            fail_match = cls.HYPIUM_FAIL_PATTERN.search(line.message)
            if fail_match:
                testcase_name = fail_match.group(1) or fail_match.group(2)
                if testcase_name in testcase_start_map:
                    tw = testcase_start_map[testcase_name]
                    tw.status = "Failed"
                    tw.consuming_ms = int(fail_match.group(3)) if fail_match.group(3) else None
                    tw.end_time = line.timestamp
                    tw.end_line = line.line_num
                    tw.end_marker = "fail"
            
            # 检查[Hypium] specDone 精确结束标记（优先级①）
            specdone_match = cls.HYPIUM_SPECDONE_PATTERN.search(line.message)
            if specdone_match:
                testcase_name = specdone_match.group(1)
                if testcase_name in testcase_start_map:
                    tw = testcase_start_map[testcase_name]
                    tw.end_time = line.timestamp
                    tw.end_line = line.line_num
                    tw.end_marker = "specDone"
                    if tw.status != "Failed":
                        tw.status = "Passed"
                    else:
                        time_windows.append(tw)  # Failed 用例：精确结束，入结果
                    del testcase_start_map[testcase_name]
            
            # 检查[Hypium]pass标记（旧版格式，无 specDone 时作成功结束）
            pass_match = cls.HYPIUM_PASS_PATTERN.search(line.message)
            if pass_match and not specdone_match:
                testcase_name = pass_match.group(1)
                if testcase_name in testcase_start_map:
                    tw = testcase_start_map[testcase_name]
                    tw.end_time = line.timestamp
                    tw.end_line = line.line_num
                    tw.end_marker = "pass"
                    if tw.status != "Failed":
                        tw.status = "Passed"
                    del testcase_start_map[testcase_name]
        
        # 处理未结束的用例
        for testcase_name, tw in testcase_start_map.items():
            if tw.status == "Failed" and tw.end_marker == "fail":
                # 有 [fail] 但无 specDone：回退用 [fail] 暂定结束（优先级③）
                time_windows.append(tw)
            else:
                tw.status = "Running"
                tw.end_time = None
                tw.end_marker = "running"
                time_windows.append(tw)
        
        return time_windows
    
    @classmethod
    def find_time_window_for_testcase(
        cls,
        hilog_lines: List[LogLine],
        testcase_name: str
    ) -> Optional[HypiumTimeWindow]:
        """
        为指定用例提取时间窗
        
        Args:
            hilog_lines: 解析后的hilog日志行列表
            testcase_name: 用例名
        
        Returns:
            时间窗（如未找到返回None）
        """
        time_windows = cls.extract_time_windows(hilog_lines)
        
        for tw in time_windows:
            if tw.testcase_name == testcase_name:
                return tw
        
        return None
    
    @classmethod
    def print_time_windows(cls, time_windows: List[HypiumTimeWindow]):
        """打印时间窗信息"""
        print("\n[Hypium]标记时间窗提取结果:")
        print("=" * 80)
        
        for i, tw in enumerate(time_windows, 1):
            print(f"{i}. 用例: {tw.testcase_name}")
            print(f"   状态: {tw.status}")
            print(f"   起始: {tw.start_time} (行{tw.start_line})")
            if tw.end_time:
                print(f"   结束: {tw.end_time} (行{tw.end_line})")
                duration = (tw.end_time - tw.start_time).total_seconds()
                print(f"   持续: {duration:.2f}秒")
            else:
                print(f"   结束: 未结束")
            print()


class LayeredFilter:
    """分层过滤器"""
    
    def __init__(
        self,
        primary_domains: Set[str],
        time_window: Optional[Tuple[datetime, datetime]] = None,
        context_lines: int = 20,
        cppcrash_files: Optional[List[str]] = None
    ):
        """
        初始化过滤器
        
        Args:
            primary_domains: 主分析域集合（短格式，如 '00310', '0013X'）
            time_window: 时间窗 (start, end)
            context_lines: 上下文行数（默认前后各20行）
            cppcrash_files: cppcrash 文件列表
        """
        self.primary_domains = self._normalize_domains(primary_domains)
        self.time_window = time_window
        self.context_lines = context_lines
        self.cppcrash_files = cppcrash_files or []
    
    def _normalize_domains(self, domains: Set[str]) -> Set[str]:
        """标准化 domain 格式（转大写，处理通配符）"""
        normalized = set()
        for d in domains:
            d = d.upper().strip()
            if d.startswith('0X'):
                d = d[2:]
            if len(d) > 5:
                d = d[-5:]
            if 'X' in d:
                normalized.add(d)
            else:
                normalized.add(d.zfill(5))
        return normalized
    
    def _match_domain(self, log_domain: str) -> bool:
        """检查日志 domain 是否匹配主分析域"""
        if not log_domain or not self.primary_domains:
            return False
        
        log_domain = log_domain.upper().zfill(5)
        
        for pattern in self.primary_domains:
            if 'X' in pattern:
                pattern_prefix = pattern.split('X')[0]
                if log_domain.startswith(pattern_prefix):
                    return True
            else:
                if log_domain == pattern:
                    return True
        
        return False
    
    def _is_in_time_window(self, log_line: LogLine) -> bool:
        """检查日志是否在时间窗内"""
        if not self.time_window:
            return True
        
        if not log_line.timestamp:
            return True
        
        start, end = self.time_window
        return start <= log_line.timestamp <= end
    
    def filter_layer1_time_window(self, all_lines: List[LogLine]) -> Tuple[List[LogLine], List[LogLine]]:
        """
        Layer 1: 时间窗硬过滤
        
        Returns:
            (时间窗内日志, 时间窗外日志)
        """
        if not self.time_window:
            return all_lines, []
        
        in_window = []
        out_window = []
        
        for line in all_lines:
            if self._is_in_time_window(line):
                in_window.append(line)
            else:
                out_window.append(line)
        
        return in_window, out_window
    
    def filter_layer2_domain_group(
        self,
        lines_in_window: List[LogLine]
    ) -> Tuple[List[LogLine], List[LogLine]]:
        """
        Layer 2: domain 分组
        
        Returns:
            (主分析集, 备用集)
        """
        primary = []
        backup = []
        
        for line in lines_in_window:
            if self._match_domain(line.domain or ''):
                primary.append(line)
            else:
                backup.append(line)
        
        return primary, backup
    
    def filter_layer3_extend(
        self,
        primary_lines: List[LogLine],
        all_lines_in_window: List[LogLine]
    ) -> Tuple[List[LogLine], List[LogLine], List[LogLine]]:
        """
        Layer 3: 渐进式扩展
        
        Args:
            primary_lines: 主分析集
            all_lines_in_window: 时间窗内所有日志
        
        Returns:
            (P1扩展, P2扩展, P3扩展)
        """
        if not primary_lines:
            return [], [], []
        
        p1_set = set()
        p2_set = set()
        p3_set = set()
        
        primary_set = {line.line_num for line in primary_lines}
        
        primary_pids_tids = {(line.pid, line.tid) for line in primary_lines if line.pid and line.tid}
        primary_pids = {line.pid for line in primary_lines if line.pid}
        primary_line_nums = {line.line_num for line in primary_lines}
        
        line_map = {line.line_num: line for line in all_lines_in_window}
        sorted_lines = sorted(all_lines_in_window, key=lambda x: x.line_num)
        
        for line in sorted_lines:
            if line.line_num in primary_set:
                continue
            
            if (line.pid, line.tid) in primary_pids_tids:
                p1_set.add(line.line_num)
            elif line.pid in primary_pids:
                p2_set.add(line.line_num)
        
        for primary_line in primary_lines:
            primary_idx = None
            for idx, line in enumerate(sorted_lines):
                if line.line_num == primary_line.line_num:
                    primary_idx = idx
                    break
            
            if primary_idx is not None:
                start_idx = max(0, primary_idx - self.context_lines)
                end_idx = min(len(sorted_lines), primary_idx + self.context_lines + 1)
                
                for idx in range(start_idx, end_idx):
                    line_num = sorted_lines[idx].line_num
                    if line_num not in primary_set:
                        p3_set.add(line_num)
        
        p1_lines = [line_map[num] for num in sorted(p1_set)]
        p2_lines = [line_map[num] for num in sorted(p2_set - p1_set)]
        p3_lines = [line_map[num] for num in sorted(p3_set - p1_set - p2_set)]
        
        return p1_lines, p2_lines, p3_lines
    
    def load_cppcrash(self) -> List[str]:
        """加载 cppcrash 文件内容"""
        cppcrash_lines = []
        
        for filepath in self.cppcrash_files:
            try:
                if filepath.endswith('.gz'):
                    with gzip.open(filepath, 'rt', encoding='utf-8', errors='ignore') as f:
                        cppcrash_lines.extend(f.readlines())
                else:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        cppcrash_lines.extend(f.readlines())
            except Exception as e:
                print(f"Warning: Failed to load cppcrash file {filepath}: {e}", file=sys.stderr)
        
        return cppcrash_lines
    
    def filter(self, all_lines: List[LogLine]) -> FilterResult:
        """执行分层过滤"""
        result = FilterResult()
        
        result.cppcrash_lines = self.load_cppcrash()
        
        lines_in_window, lines_out_window = self.filter_layer1_time_window(all_lines)
        
        primary_lines, backup_lines = self.filter_layer2_domain_group(lines_in_window)
        
        p1_lines, p2_lines, p3_lines = self.filter_layer3_extend(
            primary_lines if primary_lines else backup_lines,
            lines_in_window
        )
        
        result.primary_lines = primary_lines
        result.p1_lines = p1_lines
        result.p2_lines = p2_lines
        result.p3_lines = p3_lines
        result.backup_lines = backup_lines if primary_lines else []
        
        result.stats = {
            'total_lines': len(all_lines),
            'time_window_filtered': len(lines_out_window),
            'time_window_kept': len(lines_in_window),
            'primary_domain_lines': len(primary_lines),
            'backup_domain_lines': len(backup_lines),
            'p1_extension_lines': len(p1_lines),
            'p2_extension_lines': len(p2_lines),
            'p3_extension_lines': len(p3_lines),
            'cppcrash_files': len(self.cppcrash_files),
            'cppcrash_lines': len(result.cppcrash_lines),
            'total_output_lines': (
                len(primary_lines) + 
                len(p1_lines) + 
                len(p2_lines) + 
                len(p3_lines)
            ),
            'extended_from_backup': len(primary_lines) == 0,
            'primary_domains': list(self.primary_domains),
        }
        
        return result


def format_output_line(log_line: LogLine, source: str) -> str:
    """格式化输出行，带来源标记"""
    return f"[{source}] 行{log_line.line_num}: {log_line.raw_line}"


def format_cppcrash_line(line: str, line_num: int) -> str:
    """格式化 cppcrash 行"""
    return f"[cppcrash] 行{line_num}: {line.rstrip()}"


def parse_time_window(time_str: str) -> datetime:
    """解析时间字符串"""
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%m-%d %H:%M:%S",
        "%m-%d %H:%M:%S.%f",
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(time_str, fmt)
            if dt.year == 1900:
                dt = dt.replace(year=datetime.now().year)
            return dt
        except ValueError:
            continue
    
    raise ValueError(f"无法解析时间字符串: {time_str}")


def main():
    parser = argparse.ArgumentParser(
        description='分层过滤 hilog 日志',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本用法
  %(prog)s -i hilog.txt -d 00310 0013X
  
  # 指定时间窗
  %(prog)s -i hilog.txt -d 00310 --time-start "06-26 15:53:48" --time-end "06-26 15:53:52"
  
  # 多个输入文件
  %(prog)s -i hilog1.txt hilog2.txt -d 00310 001300
  
  # 包含 cppcrash 文件
  %(prog)s -i hilog.txt -d 00310 --cppcrash cppcrash.log
  
  # 输出 JSON 格式统计
  %(prog)s -i hilog.txt -d 00310 --stats-only
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        nargs='+',
        required=True,
        help='输入 hilog 文件（支持 .txt 或 .gz）'
    )
    
    parser.add_argument(
        '-d', '--domains',
        nargs='+',
        default=[],
        help='主分析域列表（支持通配符 X，如 00310, 0013X）。使用 --extract-hypium 仅提取时间窗时可省略'
    )
    
    parser.add_argument(
        '--time-start',
        type=str,
        help='时间窗起始时间（格式: MM-DD HH:MM:SS 或 YYYY-MM-DD HH:MM:SS）'
    )
    
    parser.add_argument(
        '--time-end',
        type=str,
        help='时间窗结束时间'
    )
    
    parser.add_argument(
        '--context-lines',
        type=int,
        default=20,
        help='上下文行数（默认: 20）'
    )
    
    parser.add_argument(
        '--cppcrash',
        nargs='+',
        default=[],
        help='cppcrash 文件列表（独立通道，不过滤）'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='输出文件（默认输出到 stdout）'
    )
    
    parser.add_argument(
        '--stats-only',
        action='store_true',
        help='仅输出统计信息'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='以 JSON 格式输出'
    )
    
    parser.add_argument(
        '--extract-hypium',
        action='store_true',
        help='提取[Hypium]标记时间窗（替代module_run.log）'
    )
    
    parser.add_argument(
        '--testcase',
        type=str,
        help='指定用例名（用于提取特定用例的时间窗）'
    )
    
    args = parser.parse_args()
    
    # 参数校验：分层过滤模式必须提供 -d，仅 --extract-hypium 模式可省略
    if not args.extract_hypium and not args.domains:
        parser.error('分层过滤模式必须提供 -d/--domains（如 00310 0013X）；仅 --extract-hypium 模式可省略')
    
    # 加载所有hilog文件
    all_lines = []
    line_offset = 0
    
    for filepath in args.input:
        try:
            if filepath.endswith('.gz'):
                with gzip.open(filepath, 'rt', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, start=1):
                        parsed_line = HilogParser.parse_line(line, line_offset + line_num)
                        all_lines.append(parsed_line)
                    line_offset += line_num
            else:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, start=1):
                        parsed_line = HilogParser.parse_line(line, line_offset + line_num)
                        all_lines.append(parsed_line)
                    line_offset += line_num
        except Exception as e:
            print(f"Error: Failed to read file {filepath}: {e}", file=sys.stderr)
            sys.exit(1)
    
    # ⭐ 新增：[Hypium]标记时间窗提取
    if args.extract_hypium:
        print("[Hypium]标记时间窗提取模式")
        print("=" * 80)
        
        # 提取所有[Hypium]标记时间窗
        time_windows = HypiumMarkerExtractor.extract_time_windows(all_lines)
        
        # 如果指定了特定用例，只输出该用例的时间窗
        if args.testcase:
            tw = HypiumMarkerExtractor.find_time_window_for_testcase(all_lines, args.testcase)
            if tw:
                print(f"\n找到用例 {args.testcase} 的时间窗:")
                print(f"  状态: {tw.status}")
                print(f"  起始: {tw.start_time} (行{tw.start_line})")
                if tw.end_time:
                    print(f"  结束: {tw.end_time} (行{tw.end_line})")
                    duration = (tw.end_time - tw.start_time).total_seconds()
                    print(f"  持续: {duration:.2f}秒")
                    
                    # 输出时间窗JSON格式（供后续脚本使用）
                    if args.json:
                        time_window_json = {
                            'testcase': tw.testcase_name,
                            'status': tw.status,
                            'start_time': tw.start_time.strftime("%m-%d %H:%M:%S.%f"),
                            'end_time': tw.end_time.strftime("%m-%d %H:%M:%S.%f"),
                            'start_line': tw.start_line,
                            'end_line': tw.end_line,
                            'duration_seconds': duration
                        }
                        print(json.dumps(time_window_json, ensure_ascii=False, indent=2))
                else:
                    print(f"  结束: 未结束（用例仍在运行或未找到fail/pass标记）")
            else:
                print(f"\n未找到用例 {args.testcase} 的[Hypium]标记")
                print("提示: 请检查用例名是否正确，或检查hilog是否包含[Hypium]标记")
        else:
            # 输出所有用例的时间窗
            HypiumMarkerExtractor.print_time_windows(time_windows)
            
            # 输出统计信息
            failed_count = sum(1 for tw in time_windows if tw.status == "Failed")
            passed_count = sum(1 for tw in time_windows if tw.status == "Passed")
            running_count = sum(1 for tw in time_windows if tw.status == "Running")
            
            print(f"\n统计信息:")
            print(f"  Failed用例: {failed_count}个")
            print(f"  Passed用例: {passed_count}个")
            print(f"  Running用例: {running_count}个（未结束）")
            print(f"  总计: {len(time_windows)}个用例")
            
            # 输出JSON格式（供后续脚本使用）
            if args.json:
                time_windows_json = {
                    'stats': {
                        'failed': failed_count,
                        'passed': passed_count,
                        'running': running_count,
                        'total': len(time_windows)
                    },
                    'time_windows': [
                        {
                            'testcase': tw.testcase_name,
                            'status': tw.status,
                            'start_time': tw.start_time.strftime("%m-%d %H:%M:%S.%f") if tw.start_time else None,
                            'end_time': tw.end_time.strftime("%m-%d %H:%M:%S.%f") if tw.end_time else None,
                            'start_line': tw.start_line,
                            'end_line': tw.end_line,
                            'duration_seconds': (tw.end_time - tw.start_time).total_seconds() if tw.end_time else None
                        }
                        for tw in time_windows
                    ]
                }
                print("\nJSON格式输出:")
                print(json.dumps(time_windows_json, ensure_ascii=False, indent=2))
        
        sys.exit(0)
    
    # 原有的分层过滤逻辑
    time_window = None
    if args.time_start and args.time_end:
        start = parse_time_window(args.time_start)
        end = parse_time_window(args.time_end)
        time_window = (start, end)
    
    primary_domains = set(args.domains)
    
    all_lines = []
    line_offset = 0
    
    for filepath in args.input:
        try:
            if filepath.endswith('.gz'):
                with gzip.open(filepath, 'rt', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, start=1):
                        parsed_line = HilogParser.parse_line(line, line_offset + line_num)
                        all_lines.append(parsed_line)
                    line_offset += line_num
            else:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    for line_num, line in enumerate(f, start=1):
                        parsed_line = HilogParser.parse_line(line, line_offset + line_num)
                        all_lines.append(parsed_line)
                    line_offset += line_num
        except Exception as e:
            print(f"Error: Failed to read file {filepath}: {e}", file=sys.stderr)
            sys.exit(1)
    
    layered_filter = LayeredFilter(
        primary_domains=primary_domains,
        time_window=time_window,
        context_lines=args.context_lines,
        cppcrash_files=args.cppcrash
    )
    
    result = layered_filter.filter(all_lines)
    
    if args.json:
        output_data = {
            'stats': result.stats,
            'primary': [
                {'line': line.line_num, 'raw': line.raw_line, 'domain': line.domain, 'tag': line.tag}
                for line in result.primary_lines
            ],
            'p1': [
                {'line': line.line_num, 'raw': line.raw_line, 'domain': line.domain, 'tag': line.tag}
                for line in result.p1_lines
            ],
            'p2': [
                {'line': line.line_num, 'raw': line.raw_line, 'domain': line.domain, 'tag': line.tag}
                for line in result.p2_lines
            ],
            'p3': [
                {'line': line.line_num, 'raw': line.raw_line, 'domain': line.domain, 'tag': line.tag}
                for line in result.p3_lines
            ],
        }
        output_str = json.dumps(output_data, ensure_ascii=False, indent=2)
    elif args.stats_only:
        output_str = json.dumps(result.stats, ensure_ascii=False, indent=2)
    else:
        lines = []
        
        lines.append("=" * 80)
        lines.append("【分层过滤结果】")
        lines.append("=" * 80)
        
        if result.primary_lines:
            lines.append(f"\n【主分析集】共 {len(result.primary_lines)} 行")
            lines.append("-" * 80)
            for log_line in result.primary_lines:
                lines.append(format_output_line(log_line, '主'))
        
        if result.p1_lines:
            lines.append(f"\n【P1 扩展 - 同(PID,TID)】共 {len(result.p1_lines)} 行")
            lines.append("-" * 80)
            for log_line in result.p1_lines:
                lines.append(format_output_line(log_line, 'P1'))
        
        if result.p2_lines:
            lines.append(f"\n【P2 扩展 - 同PID】共 {len(result.p2_lines)} 行")
            lines.append("-" * 80)
            for log_line in result.p2_lines:
                lines.append(format_output_line(log_line, 'P2'))
        
        if result.p3_lines:
            lines.append(f"\n【P3 扩展 - 位置窗口】共 {len(result.p3_lines)} 行")
            lines.append("-" * 80)
            for log_line in result.p3_lines:
                lines.append(format_output_line(log_line, 'P3'))
        
        if result.cppcrash_lines:
            lines.append(f"\n【cppcrash 独立通道】共 {len(result.cppcrash_lines)} 行")
            lines.append("-" * 80)
            for line_num, line in enumerate(result.cppcrash_lines, start=1):
                lines.append(format_cppcrash_line(line, line_num))
        
        lines.append("\n" + "=" * 80)
        lines.append("【统计信息】")
        lines.append("=" * 80)
        lines.append(f"总行数: {result.stats['total_lines']}")
        lines.append(f"时间窗过滤: {result.stats['time_window_filtered']} 行被丢弃")
        lines.append(f"时间窗保留: {result.stats['time_window_kept']} 行")
        lines.append(f"主分析集(domain匹配): {result.stats['primary_domain_lines']} 行")
        lines.append(f"备用集(domain不匹配): {result.stats['backup_domain_lines']} 行")
        lines.append(f"P1 扩展(同PID+TID): {result.stats['p1_extension_lines']} 行")
        lines.append(f"P2 扩展(同PID): {result.stats['p2_extension_lines']} 行")
        lines.append(f"P3 扩展(位置窗口): {result.stats['p3_extension_lines']} 行")
        lines.append(f"输出总计: {result.stats['total_output_lines']} 行")
        lines.append(f"cppcrash 文件: {result.stats['cppcrash_files']} 个")
        lines.append(f"cppcrash 行数: {result.stats['cppcrash_lines']} 行")
        
        if result.stats['extended_from_backup']:
            lines.append("\n⚠️ 扩展提示: 主分析集(domain匹配) 0 条，已扩展到备用集（时间窗内全量）重跑分析")
        
        lines.append(f"\n主分析域: {', '.join(result.stats['primary_domains'])}")
        
        output_str = "\n".join(lines)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output_str)
        print(f"结果已保存到: {args.output}")
    else:
        print(output_str)


if __name__ == '__main__':
    main()