#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2026 Huawei Device Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
统一扫描引擎 v2.0 - 文件级并行

将30个独立规则脚本整合为一个引擎：
1. 简单规则（行级正则）→ 内置模式表
2. 块级规则（需上下文）→ 共享预解析结果
3. 工程级规则 → 单独聚合处理

优势：
- 文件数：30 → 3（减少90%）
- 遍历次数：30×N → 1×N
- 内存：共享上下文，减少重复解析
"""
import os
import re
import sys
import time
from typing import Dict, List, Set, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from common import (
    FileContentCache, BlockCache, get_subsystem, find_testcase_for_line,
    find_matching_brace, grep_scan, parse_it_blocks, is_in_sta_project,
)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from config_loader import get_sta_inapplicable_rules


# ============================================================================
# 规则模式表：所有简单规则的检测模式集中定义
# ============================================================================

FILE_MAP = {
    'R001': 'all_source', 'R002': 'all_source', 'R003': 'all_source',
    'R004': 'all_source', 'R005': 'all_source', 'R006': 'all_source',
    'R007': 'test_json', 'R008': 'test_files', 'R009': 'test_files',
    'R010': 'build_gn', 'R012': 'p7b_files',
    'R013': 'test_files', 'R014': 'build_gn', 'R015': 'test_files',
    'R016': 'test_files', 'R017': 'syscap_f', 'R018': 'test_files',
    'R019': 'all_source', 'R020': 'all_source', 'R021': 'all_source',
    'R022': 'all_source', 'R023': 'all_source',
    'R201': 'test_files', 'R202': 'test_files', 'R203': 'test_files',
    'R204': 'test_files', 'R205': 'test_files', 'R206': 'test_files',
}

SIMPLE_RULES = {
    'R002': {
        'name': '错误码断言必须是number类型',
        'severity': 'Critical',
        'category': '编码规范合规',
        'scope': ['*.ets', '*.ts', '*.js'],
        'grep_filter': [r'\.code\b'],
        'patterns': [
            (r'expect\s*\(\s*\w+\.code\s*\)\s*\.\s*assertEqual\s*\(\s*[\'"](\d+)[\'"]', 'error.code是number，断言时应使用数字而非字符串'),
            (r'expect\s*\(\s*\w+\.code\s*,\s*[\'"]\d+[\'"]\s*\)', 'error.code是number，断言时应使用数字而非字符串'),
            (r'expect\s*\(\s*\w+\.code\s*===?\s*[\'"]\d+[\'"]', 'error.code是number，比较时应使用数字而非字符串'),
            (r'if\s*\(\s*\w+\.code\s*===?\s*[\'"]\d+[\'"]', 'error.code是number，比较时应使用数字而非字符串'),
        ],
    },
    'R003': {
        'name': '禁止恒真断言',
        'severity': 'Critical',
        'category': '编码规范合规',
        'scope': ['*.ets', '*.ts', '*.js'],
        'grep_filter': [r'expect\s*\(\s*true\s*\)', r'expect\s*\(\s*false\s*\)'],
        'patterns': [
            (r'expect\s*\(\s*true\s*\)\s*\.\s*assertTrue\s*\(', 'expect(true).assertTrue()恒成立，请替换为对实际业务逻辑的有效断言'),
            (r'expect\s*\(\s*true\s*\)\s*\.\s*assertEqual\s*\(\s*true\s*\)', 'expect(true).assertEqual(true)恒成立，请替换为对实际业务逻辑的有效断言'),
            (r'expect\s*\(\s*false\s*\)\s*\.\s*assertFalse\s*\(', 'expect(false).assertFalse()恒成立，请替换为对实际业务逻辑的有效断言'),
        ],
    },
    'R005': {
        'name': '组件尺寸使用固定值',
        'severity': 'Warning',
        'category': '编码规范合规',
        'scope': ['*.ets', '*.ts', '*.js'],
        'grep_filter': [r'\.(width|height)\s*\('],
        'patterns': [
            (r'\.(width|height)\s*\(\s*(\d+)\s*\)', '建议使用百分比而非固定像素'),
            (r'\.(width|height)\s*\(\s*["\']\s*(\d+)\s*(?:px|vp|fp|lpx)?\s*["\']\s*\)', '建议使用百分比而非固定像素'),
        ],
        'exclude_patterns': [r'\.(width|height)\s*\(\s*["\']?\s*\d+\.?\d*\s*%'],
    },
    'R007': {
        'name': 'Test.json禁止配置项',
        'severity': 'Critical',
        'category': '编码规范合规',
        'scope': ['test.json'],
        'patterns': [
            (r'setenforce\s*0', '禁止配置setenforce 0'),
            (r'"setenforce"\s*:\s*"0"', '禁止配置setenforce 0'),
            (r'"rerun"\s*:\s*(true|1|"true")', '禁止配置rerun:true'),
            (r'appfreeze\.filter_bundle_name', '禁止配置appfreeze过滤'),
        ],
    },
    'R009': {
        'name': '@tc.number命名不规范',
        'severity': 'Warning',
        'category': '编码规范合规',
        'scope': ['*.ets', '*.ts', '*.js'],
        'grep_filter': [r'@tc\.number'],
        'patterns': [],
    },
    'R015': {
        'name': 'Level参数缺省',
        'severity': 'Warning',
        'category': '编码规范合规',
        'scope': ['*.test.ets', '*.test.ts', '*.test.js'],
        'grep_filter': [r'\bit\s*\('],
        'patterns': [
            (r'\bit\s*\(\s*[\'"][^\'"]+[\'"]\s*,\s*(?:async\s*)?\([^)]*\)\s*=>', 'it()缺少Level参数，应在测试名称后添加Level.LEVEL0'),
            (r'\bit\s*\(\s*[\'"][^\'"]+[\'"]\s*,\s*function\s*\([^)]*\)', 'it()缺少Level参数，应在测试名称后添加Level.LEVEL0'),
        ],
        'exclude_patterns': [r'\bit\s*\(\s*[\'"][^\'"]+[\'"]\s*,\s*Level\.'],
    },
    'R022': {
        'name': 'errcode使用宽松比较',
        'severity': 'Critical',
        'category': '编码规范合规',
        'scope': ['*.ets', '*.ts', '*.js'],
        'grep_filter': [r'\.code\s*[!=]='],
        'patterns': [
            (r'\.code\s*==(?!=)', '.code是number，应使用===严格比较'),
            (r'\.code\s*!=(?!=)', '.code是number，应使用!==严格比较'),
        ],
    },
    'R023': {
        'name': '禁止errcode类型强转后断言',
        'severity': 'Critical',
        'category': '编码规范合规',
        'scope': ['*.ets', '*.ts', '*.js'],
        'grep_filter': [r'\.code\s*\.', r'String\s*\(', r'Number\s*\('],
        'patterns': [
            (r'\.code\s*\.\s*toString\s*\(', 'error.code不应类型强转'),
            (r'String\s*\(\s*\w+\.code', 'error.code不应类型强转'),
            (r'Number\s*\(\s*\w+\.code', 'error.code不应类型强转'),
        ],
    },
}


# ============================================================================
# 文件扫描器：单文件应用所有规则
# ============================================================================

class UnifiedFileScanner:
    """统一文件扫描器：一次加载，应用所有规则"""
    
    def __init__(self, base_dir: str, active_rules: Set[str] = None):
        self.base_dir = base_dir
        self._fcache = FileContentCache()
        self._bcache = BlockCache(self._fcache)
        self.active_rules = active_rules if active_rules is not None else set(SIMPLE_RULES.keys())
        
        # 预编译所有正则
        self._compiled_rules = {}
        for rid, rinfo in SIMPLE_RULES.items():
            # 只编译active_rules中的规则
            if rid not in self.active_rules:
                continue
            compiled_patterns = [(re.compile(p), sug) for p, sug in rinfo.get('patterns', [])]
            compiled_exclude = [re.compile(p) for p in rinfo.get('exclude_patterns', [])]
            compiled_grep = [re.compile(p) for p in rinfo.get('grep_filter', [])]
            self._compiled_rules[rid] = {
                'compiled_patterns': compiled_patterns,
                'compiled_exclude': compiled_exclude,
                'compiled_grep': compiled_grep,
                'info': rinfo,
            }
    
    def scan_file(self, file_path: str) -> List[Dict]:
        """扫描单个文件（应用所有适用规则）"""
        content = self._fcache.get(file_path)
        if content is None:
            return []
        
        lines = content.split('\n')
        rel_path = os.path.relpath(file_path, self.base_dir)
        it_blocks = self._bcache.get_it_blocks(file_path)
        
        all_issues = []
        
        for rid, compiled in self._compiled_rules.items():
            rinfo = compiled['info']
            
            # scope过滤
            if not self._match_scope(file_path, rinfo.get('scope', [])):
                continue
            
            # grep预过滤
            if compiled['compiled_grep']:
                if not any(g.search(content) for g in compiled['compiled_grep']):
                    continue
            
            # 行级扫描
            for i, line in enumerate(lines, 1):
                if self._should_skip_line(line, rinfo):
                    continue
                
                # exclude模式检查
                if any(e.search(line) for e in compiled['compiled_exclude']):
                    continue
                
                # pattern匹配
                for pattern, suggestion in compiled['compiled_patterns']:
                    m = pattern.search(line)
                    if m:
                        testcase = find_testcase_for_line(it_blocks, i)
                        
                        # 自定义验证器
                        validator = rinfo.get('validator')
                        if validator and not validator(m):
                            continue
                        
                        all_issues.append({
                            'rule': rid,
                            'category': rinfo['category'],
                            'type': rinfo['name'],
                            'severity': rinfo['severity'],
                            'file': rel_path,
                            'line': i,
                            'testcase': testcase,
                            'snippet': line.strip()[:120],
                            'suggestion': suggestion,
                            'subsystem': get_subsystem(rel_path),
                        })
        
        return all_issues
    
    def _match_scope(self, file_path: str, scopes: List[str]) -> bool:
        if not scopes:
            return True
        for scope in scopes:
            if scope.startswith('*'):
                if file_path.endswith(scope[1:]):
                    return True
            elif os.path.basename(file_path).lower() == scope.lower():
                return True
        return False
    
    def _should_skip_line(self, line: str, rinfo: Dict) -> bool:
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('*'):
            return True
        if rinfo.get('skip_if'):
            return rinfo['skip_if'](line)
        return False


# ============================================================================
# 文件级并行引擎
# ============================================================================

class FileParallelEngine:
    """文件级并行扫描引擎"""
    
    def __init__(self, base_dir: str, rules: Set[str] = None):
        self.base_dir = base_dir
        # 只有当rules为None时才使用全部规则，空set表示不执行任何简单规则
        self.active_rules = rules if rules is not None else set(SIMPLE_RULES.keys())
        self.scanner = UnifiedFileScanner(base_dir, self.active_rules)
    
    def scan(self, files: List[str], workers: int = 0, progress_callback=None) -> List[Dict]:
        """文件级并行扫描
        
        Args:
            files: 文件列表
            workers: 并行线程数
            progress_callback: 进度回调函数，接收参数 (done_files, total_files, found_issues)
        """
        n_workers = workers or min(os.cpu_count() or 4, len(files))
        n_workers = max(1, min(n_workers, 32))  # 1-32线程
        
        all_issues = []
        done_count = 0
        last_callback_time = time.time()
        CALLBACK_INTERVAL = 2  # 每2秒调用一次回调
        
        with ThreadPoolExecutor(max_workers=n_workers) as executor:
            futures = {executor.submit(self.scanner.scan_file, fp): fp for fp in files}
            
            for future in as_completed(futures):
                try:
                    issues = future.result()
                    all_issues.extend(issues)
                except Exception as e:
                    pass
                
                done_count += 1
                current_time = time.time()
                if progress_callback and (done_count % 100 == 0 or current_time - last_callback_time >= CALLBACK_INTERVAL):
                    progress_callback(done_count, len(files), len(all_issues))
                    last_callback_time = current_time
        
        return all_issues
    
    def scan_by_file_map(self, rule_file_map: Dict[str, List[str]], 
                          workers: int = 0, progress_callback=None) -> List[Dict]:
        """
        按FILE_MAP优化扫描：合并文件列表，每个文件只扫描一次
        
        Args:
            rule_file_map: {规则ID: 文件列表}
            workers: 并行线程数
            progress_callback: 进度回调函数
        """
        all_issues = []
        
        # 合并所有文件，确定每个文件适用的规则
        file_rules_map = defaultdict(set)
        for rid, files in rule_file_map.items():
            if rid in self.scanner._compiled_rules:
                for fp in files:
                    file_rules_map[fp].add(rid)
        
        # 为每个文件-规则组合创建任务（但每个文件只加载一次）
        all_files = list(file_rules_map.keys())
        total_files = len(all_files)
        
        n_workers = workers or min(os.cpu_count() or 4, total_files)
        n_workers = max(1, min(n_workers, 32))
        
        done_count = 0
        last_callback_time = time.time()
        CALLBACK_INTERVAL = 2
        
        # 创建任务：每个文件只扫描一次，应用所有适用的规则
        scan_tasks = [(fp, rules) for fp, rules in file_rules_map.items()]
        
        with ThreadPoolExecutor(max_workers=n_workers) as executor:
            futures = {executor.submit(self._scan_file_with_rules, fp, rules): fp 
                       for fp, rules in scan_tasks}
            
            for future in as_completed(futures):
                try:
                    issues = future.result()
                    all_issues.extend(issues)
                except Exception:
                    pass
                
                done_count += 1
                current_time = time.time()
                if progress_callback and (done_count % 100 == 0 or current_time - last_callback_time >= CALLBACK_INTERVAL):
                    progress_callback(done_count, total_files, len(all_issues))
                    last_callback_time = current_time
        
        return all_issues
    
    def _scan_file_with_rules(self, fp: str, rules: Set[str]) -> List[Dict]:
        """扫描单个文件，只应用指定的规则"""
        content = self.scanner._fcache.get(fp)
        if content is None:
            return []
        
        lines = content.split('\n')
        rel_path = os.path.relpath(fp, self.base_dir)
        it_blocks = self.scanner._bcache.get_it_blocks(fp)
        
        all_issues = []
        
        for rid in rules:
            if rid not in self.scanner._compiled_rules:
                continue
            
            compiled = self.scanner._compiled_rules[rid]
            rinfo = compiled['info']
            
            # grep预过滤
            if compiled['compiled_grep']:
                if not any(g.search(content) for g in compiled['compiled_grep']):
                    continue
            
            # 行级扫描
            for i, line in enumerate(lines, 1):
                if self.scanner._should_skip_line(line, rinfo):
                    continue
                
                # exclude模式检查
                if any(e.search(line) for e in compiled['compiled_exclude']):
                    continue
                
                # pattern匹配
                for pattern, suggestion in compiled['compiled_patterns']:
                    m = pattern.search(line)
                    if m:
                        testcase = find_testcase_for_line(it_blocks, i)
                        
                        # 自定义验证器
                        validator = rinfo.get('validator')
                        if validator and not validator(m):
                            continue
                        
                        all_issues.append({
                            'rule': rid,
                            'category': rinfo['category'],
                            'type': rinfo['name'],
                            'severity': rinfo['severity'],
                            'file': rel_path,
                            'line': i,
                            'testcase': testcase,
                            'snippet': line.strip()[:120],
                            'suggestion': suggestion,
                            'subsystem': get_subsystem(rel_path),
                        })
        
        return all_issues


# ============================================================================
# 工程级规则：需跨文件聚合（单独处理）
# ============================================================================

class ProjectLevelScanner:
    """工程级规则扫描器（R011/R018/R019/R020）
    
    - R011: describe名称工程级去重（同一独立XTS工程内）
    - R018: testcase名称describe内去重（同一文件同一describe块内）
    - R019: .key()值工程级去重（同一独立XTS工程内，扫描page页面）
    - R020: .id()值工程级去重（同一独立XTS工程内，扫描page页面）
    """
    
    def scan(self, files: List[str], base_dir: str, fcache: FileContentCache, 
             progress_callback=None) -> List[Dict]:
        """
        工程级扫描：先识别独立工程，再在每个工程内聚合
        
        这些规则不能在单文件级别完成：
        - R011: describe名称工程级去重（同一独立XTS工程内，扫描测试文件）
        - R019: .key()值工程级去重（同一独立XTS工程内，扫描page页面）
        - R020: .id()值工程级去重（同一独立XTS工程内，扫描page页面）
        
        R018特殊处理（同一文件同一describe块内去重，不跨文件）：
        - R018: testcase名称describe内去重（同一文件同一describe块内）
        """
        issues = []
        
        bcache = BlockCache(fcache)
        
        # Step 1: 使用grep预过滤目标文件
        # R011: 包含describe的测试文件
        describe_results = grep_scan(base_dir, [r'describe\s*\('], ['*.test.ets', '*.test.ts', '*.test.js'])
        describe_files = set(r[0] for r in describe_results)
        
        # R019/R020: 包含.key或.id的page文件
        key_results = grep_scan(base_dir, [r'\.key\s*\('])
        id_results = grep_scan(base_dir, [r'\.id\s*\('])
        key_id_files = set()
        for fp, _, _, _ in key_results + id_results:
            if '/pages/' in fp:
                key_id_files.add(fp)
        
        # Step 2: 从预过滤文件中识别独立XTS工程（确保工程和文件匹配）
        all_target_files = list(describe_files) + list(key_id_files)
        projects = self._find_independent_projects(base_dir, all_target_files)
        
        total_projects = len(projects)
        processed_projects = 0
        
        # Step 3: 每个工程内独立检测重复
        for project_dir in projects:
            processed_projects += 1
            
            if progress_callback and processed_projects % 100 == 0:
                progress_callback(processed_projects, total_projects, len(issues))
            
            # R011: 测试文件中的describe重复
            test_files = [fp for fp in describe_files 
                         if os.path.abspath(fp).startswith(os.path.abspath(project_dir) + os.sep)]
            
            # R019/R020: page页面中的.key()/.id()重复
            page_files = [fp for fp in key_id_files 
                         if os.path.abspath(fp).startswith(os.path.abspath(project_dir) + os.sep)]
            
            if not test_files and not page_files:
                continue
            
            # R011检测
            if test_files:
                describe_map = defaultdict(list)
                describe_pattern = re.compile(r'describe\s*\(\s*["\']([^"\']+)["\']')
                
                for fp in test_files:
                    content = fcache.get(fp)
                    if not content or 'describe' not in content:
                        continue
                    rel_path = os.path.relpath(fp, base_dir)
                    for m in describe_pattern.finditer(content):
                        describe_map[m.group(1)].append((rel_path, content[:m.start()].count('\n') + 1))
                
                for name, locs in describe_map.items():
                    if len(locs) > 1:
                        first = locs[0]
                        others = [f"{p}:{l}" for p, l in locs[1:]]
                        issues.append({
                            'rule': 'R011',
                            'category': '编码规范合规',
                            'type': 'testsuite重复',
                            'severity': 'Critical',
                            'file': first[0],
                            'line': first[1],
                            'testcase': '-',
                            'snippet': f'describe("{name}", ...)',
                            'suggestion': f'testsuite "{name}" 重复{len(locs)}次: {"; ".join(others[:5])}',
                            'subsystem': get_subsystem(first[0]),
                        })
            
            # R018检测: testcase重复 (同一文件同一describe块内)
            if test_files:
                it_pattern = re.compile(r'\bit\s*\(\s*["\']([^"\']+)["\']')
                
                for fp in test_files:
                    content = fcache.get(fp)
                    if not content:
                        continue
                    rel_path = os.path.relpath(fp, base_dir)
                    
                    describe_blocks = bcache.get_describe_blocks(fp)
                    lines = content.split('\n')
                    
                    for desc_block in describe_blocks:
                        all_occurrences = {}
                        for i in range(desc_block['start'], desc_block['end'] + 1):
                            if i >= len(lines):
                                continue
                            line = lines[i]
                            m = it_pattern.search(line)
                            if m:
                                tc_name = m.group(1)
                                if tc_name not in all_occurrences:
                                    all_occurrences[tc_name] = [i]
                                else:
                                    all_occurrences[tc_name].append(i)
                        
                        for tc_name, occurrence_lines in all_occurrences.items():
                            if len(occurrence_lines) < 2:
                                continue
                            
                            first_line = occurrence_lines[0]
                            duplicate_lines = occurrence_lines[1:]
                            duplicate_line_nums = [l + 1 for l in duplicate_lines]
                            
                            snippet = lines[first_line].strip()[:120]
                            dup_str = ', '.join(str(n) for n in duplicate_line_nums)
                            
                            issues.append({
                                'rule': 'R018',
                                'category': '编码规范合规',
                                'type': 'testcase重复',
                                'severity': 'Critical',
                                'file': rel_path,
                                'line': first_line + 1,
                                'testcase': tc_name,
                                'snippet': snippet,
                                'suggestion': f"testcase '{tc_name}' 在describe '{desc_block['name']}' 内重复{len(occurrence_lines)}次。与当前文件第{dup_str}行重复，修改testcase名称确保describe内唯一。",
                                'subsystem': get_subsystem(rel_path),
                            })
            
            # R019/R020检测
            if page_files:
                key_pattern = re.compile(r'\.key\s*\(\s*["\']([^"\']+)["\']')
                id_pattern = re.compile(r'\.id\s*\(\s*["\']([^"\']+)["\']')
                
                key_map = defaultdict(list)
                id_map = defaultdict(list)
                
                for fp in page_files:
                    content = fcache.get(fp)
                    if not content:
                        continue
                    rel_path = os.path.relpath(fp, base_dir)
                    
                    for m in key_pattern.finditer(content):
                        key_map[m.group(1)].append((rel_path, content[:m.start()].count('\n') + 1))
                    
                    for m in id_pattern.finditer(content):
                        id_map[m.group(1)].append((rel_path, content[:m.start()].count('\n') + 1))
                
                for key, locs in key_map.items():
                    if len(locs) > 1:
                        first = locs[0]
                        issues.append({
                            'rule': 'R019',
                            'category': '编码规范合规',
                            'type': '.key重复',
                            'severity': 'Critical',
                            'file': first[0],
                            'line': first[1],
                            'testcase': '-',
                            'snippet': f'.key("{key}")',
                            'suggestion': f'.key("{key}") 重复{len(locs)}次',
                            'subsystem': get_subsystem(first[0]),
                        })
                
                for id_val, locs in id_map.items():
                    if len(locs) > 1:
                        first = locs[0]
                        issues.append({
                            'rule': 'R020',
                            'category': '编码规范合规',
                            'type': '.id重复',
                            'severity': 'Critical',
                            'file': first[0],
                            'line': first[1],
                            'testcase': '-',
                            'snippet': f'.id("{id_val}")',
                            'suggestion': f'.id("{id_val}") 重复{len(locs)}次',
                            'subsystem': get_subsystem(first[0]),
                        })
        
        return issues
    
    def _find_independent_projects(self, base_dir: str, files: List[str]) -> List[str]:
        """识别独立XTS工程
        
        独立XTS工程的判断标准：
        1. 目录结构：.../xxx/entry/src/...，其中xxx是工程根目录
        2. xxx目录下存在BUILD.gn文件且非group类型
        3. 目录下存在测试文件或page页面
        
        Fallback策略：
        如果找不到entry目录，则查找扫描根目录下的BUILD.gn作为工程边界
        """
        # Step 1: 从文件路径提取工程目录（entry的父目录）
        potential_projects = set()
        for fp in files:
            abs_fp = os.path.abspath(fp)
            rel_fp = os.path.relpath(abs_fp, base_dir)
            parts = rel_fp.split('/')
            # 寻找entry目录，其父目录就是工程根目录
            for i, part in enumerate(parts):
                if part == 'entry' and i > 0:
                    project_dir = os.path.join(base_dir, '/'.join(parts[:i]))
                    potential_projects.add(project_dir)
                    break
        
        # Fallback: 如果没有找到entry目录，检查根目录是否有BUILD.gn
        if not potential_projects:
            root_gn_path = os.path.join(base_dir, 'BUILD.gn')
            if os.path.exists(root_gn_path) and not self._is_group_build_gn(root_gn_path):
                potential_projects.add(base_dir)
        
        # Step 2: 检查每个潜在工程目录是否有BUILD.gn且非group
        projects = []
        for d in sorted(potential_projects):
            gn_path = os.path.join(d, 'BUILD.gn')
            if os.path.exists(gn_path) and not self._is_group_build_gn(gn_path):
                projects.append(d)
        
        # Final fallback: 如果仍然没有找到工程，将根目录作为默认工程
        if not projects:
            projects = [base_dir]
        
        return projects
    
    def _is_group_build_gn(self, gn_path: str) -> bool:
        """判断BUILD.gn是否是group类型"""
        try:
            with open(gn_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return bool(re.search(r'\bgroup\s*\(', content))
        except:
            return False


# ============================================================================
# 辅助函数
# ============================================================================

def _validate_tc_number(tc_number: str) -> bool:
    """验证@tc.number命名"""
    if not tc_number.startswith('SUB_'):
        return False
    segments = tc_number[4:].split('_')
    if len(segments) < 3:
        return False
    return segments[-1].isdigit() and len(segments[-1]) == 4


# ============================================================================
# 统一入口函数
# ============================================================================

def unified_scan(files: List[str], base_dir: str, rules: Set[str] = None,
                 workers: int = 0, progress_callback=None, sta_projects: Set[str] = None, **kwargs) -> List[Dict]:
    """
    统一扫描入口 - Phase 0批量预处理 + Phase 1文件级并行
    
    Args:
        files: 文件列表（已废弃，使用cats代替）
        base_dir: 扫描根目录
        rules: 活动规则（None=全部）
        workers: 并行线程数
        progress_callback: 进度回调函数
        sta_projects: Sta工程目录集合（用于跳过R002/R022）
        kwargs: 额外参数（fcache, cats等）
    """
    fcache = kwargs.get('fcache', FileContentCache())
    cats = kwargs.get('cats')
    
    # 使用FILE_MAP优化：每个规则只扫描相关文件类别
    if cats:
        all_source = cats.get('all_source', [])
        test_files = cats.get('test', [])
        build_gn = cats.get('build_gn', [])
        test_json = cats.get('test_json', [])
        p7b_files = cats.get('p7b', [])
        syscap_f = cats.get('syscap', [])
        
        file_categories = {
            'all_source': all_source,
            'test_files': test_files,
            'build_gn': build_gn,
            'test_json': test_json,
            'p7b_files': p7b_files,
            'syscap_f': syscap_f,
        }
        
        # 为每个规则分配正确的文件列表
        rule_file_map = {}
        active_rules = rules if rules is not None else set(SIMPLE_RULES.keys())
        
        for rid in active_rules:
            if rid in SIMPLE_RULES:
                category = FILE_MAP.get(rid, 'all_source')
                rule_file_map[rid] = file_categories.get(category, [])
    else:
        # 兼容旧调用方式：所有规则扫描所有文件
        rule_file_map = {rid: files for rid in (rules if rules is not None else set(SIMPLE_RULES.keys()))}
    
    # ===== Phase 0: 批量grep_scan预处理（10-100倍速度优势）=====
    candidate_files_map = {}  # {规则ID: 候选文件集合}
    
    # 收集所有需要grep_scan的规则及其过滤模式
    grep_tasks = []
    for rid in active_rules:
        if rid in SIMPLE_RULES:
            rinfo = SIMPLE_RULES[rid]
            grep_filters = rinfo.get('grep_filter', [])
            if grep_filters:
                # 有grep_filter的规则：先用grep_scan快速过滤
                grep_tasks.append((rid, grep_filters, rinfo.get('scope', [])))
            else:
                # 无grep_filter的规则：扫描全部相关文件
                candidate_files_map[rid] = set(rule_file_map.get(rid, []))
    
    # 执行批量grep_scan（并行执行多个规则）
    if grep_tasks:
        grep_workers = min(len(grep_tasks), workers or 4)
        
        def _execute_grep_task(task):
            rid, patterns, scopes = task
            file_globs = []
            for scope in scopes:
                if scope.startswith('*'):
                    file_globs.append(scope)
            results = grep_scan(base_dir, patterns, file_globs=file_globs if file_globs else None)
            return rid, set(r[0] for r in results)
        
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=grep_workers) as executor:
            grep_futures = {executor.submit(_execute_grep_task, task): task for task in grep_tasks}
            for future in as_completed(grep_futures):
                rid, candidate_files = future.result()
                # 只保留在FILE_MAP范围内的文件
                allowed_files = set(rule_file_map.get(rid, []))
                candidate_files_map[rid] = candidate_files & allowed_files
    
    if sta_projects:
        sta_inapplicable_rules = get_sta_inapplicable_rules()
        for rid in sta_inapplicable_rules:
            if rid in candidate_files_map:
                non_sta_files = {fp for fp in candidate_files_map[rid] 
                                 if not is_in_sta_project(fp, sta_projects)}
                if non_sta_files != candidate_files_map[rid]:
                    sta_file_count = len(candidate_files_map[rid]) - len(non_sta_files)
                    candidate_files_map[rid] = non_sta_files
                    if sta_file_count > 0:
                        import sys
                        print(f"  Sta文件自动跳过 {rid}: {sta_file_count}个文件（编译器已拦截）", file=sys.stderr, flush=True)
    
    # ===== Phase 1: 文件级并行详细扫描 =====
    # 合并所有候选文件（每个文件只加载一次）
    all_candidate_files = set()
    for rid, files_set in candidate_files_map.items():
        all_candidate_files.update(files_set)
    
    # 对候选文件进行详细扫描
    engine = FileParallelEngine(base_dir, rules)
    line_issues = engine.scan_by_file_map(
        {rid: list(candidate_files_map.get(rid, rule_file_map.get(rid, []))) 
         for rid in active_rules if rid in SIMPLE_RULES},
        workers, progress_callback
    )
    
    # ===== Phase 2: 工程级聚合（R011/R018/R019/R020）=====
    if progress_callback:
        total_files = len(all_candidate_files)
        progress_callback(0, total_files, len(line_issues))
    
    project_scanner = ProjectLevelScanner()
    project_issues = project_scanner.scan(list(all_candidate_files), base_dir, fcache, progress_callback)
    
    if progress_callback:
        progress_callback(total_files, total_files, len(line_issues) + len(project_issues))
    
    return line_issues + project_issues


if __name__ == '__main__':
    # 测试
    import sys
    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
        files = []
        for root, dirs, filenames in os.walk(test_dir):
            for f in filenames:
                if f.endswith(('.ets', '.ts', '.js', '.test.ets')):
                    files.append(os.path.join(root, f))
        
        issues = unified_scan(files, test_dir, workers=8)
        print(f"发现 {len(issues)} 个问题")
        for issue in issues[:10]:
            print(f"  {issue['rule']}: {issue['file']}:{issue['line']}")