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
规则扫描器基类 v1.0

提供共享工具方法，各规则继承此基类只需定义核心检测逻辑。

使用方式:
    class R001Scanner(RuleScanner):
        def get_grep_patterns(self):
            return [r'systemparameter']
        
        def detect_issue(self, file_path, content, line_num, line, **ctx):
            if 'getSync' in line:
                return self.make_issue(file_path, line_num, line, "建议使用异步API")

优势:
    - 减少代码重复（缓存初始化、grep过滤、issue构建）
    - 保持规则独立性（每个规则仍是独立文件）
    - 保持并行能力（engine.py统一调度）
"""
import os
import re
import sys
from typing import List, Dict, Set, Optional, Tuple, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from common import (
    FileContentCache, BlockCache, get_subsystem, 
    find_testcase_for_line, parse_it_blocks, grep_scan
)


class RuleScanner:
    """规则扫描器基类"""
    
    # 规则元数据（子类必须覆盖）
    RULE_ID: str = ''
    RULE_NAME: str = ''
    RULE_SEVERITY: str = ''
    RULE_CATEGORY: str = ''
    
    # 扫描范围（子类可覆盖）
    SCAN_GLOBS: List[str] = ['*.ets', '*.ts', '*.js']
    
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        self._fcache: Optional[FileContentCache] = None
        self._bc: Optional[BlockCache] = None
    
    def set_cache(self, fcache: FileContentCache, bc: BlockCache):
        """设置缓存（由engine.py统一管理）"""
        self._fcache = fcache
        self._bc = bc
    
    def get_grep_patterns(self) -> List[str]:
        """返回grep预过滤模式（可选，用于加速）"""
        return []
    
    def should_scan_file(self, file_path: str) -> bool:
        """判断是否应扫描此文件（可选，用于精细过滤）"""
        return True
    
    def preprocess_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """预处理文件内容（可选，用于提取上下文）"""
        return {}
    
    def detect_issue(self, file_path: str, content: str, line_num: int, 
                     line: str, **ctx) -> Optional[Dict]:
        """
        检测单行是否有问题（核心方法，子类必须实现）
        
        Args:
            file_path: 文件路径
            content: 文件完整内容
            line_num: 行号（1-indexed）
            line: 当前行内容
            **ctx: 预处理上下文（如it_blocks, string_vars等）
        
        Returns:
            问题字典或None
        """
        raise NotImplementedError("子类必须实现detect_issue方法")
    
    def scan(self, files: List[str], **kwargs) -> List[Dict]:
        """
        执行扫描（统一流程，子类一般不需覆盖）
        
        流程:
            1. grep预过滤（可选）
            2. 逐文件扫描
            3. 预处理文件
            4. 逐行检测
            5. 构建issue
        """
        if self._fcache is None:
            self._fcache = kwargs.get('fcache', FileContentCache())
        if self._bc is None:
            self._bc = kwargs.get('bc', BlockCache(self._fcache))
        
        issues = []
        file_set = set(os.path.abspath(f) for f in files)
        
        # grep预过滤（如果有定义）
        candidate_files = file_set
        grep_patterns = self.get_grep_patterns()
        if grep_patterns:
            grep_results = grep_scan(self.base_dir, grep_patterns, file_globs=self.SCAN_GLOBS)
            candidate_files = set()
            for filepath, _, _, _ in grep_results:
                if os.path.abspath(filepath) in file_set:
                    candidate_files.add(filepath)
        
        # 逐文件扫描
        for fp in candidate_files:
            if not self.should_scan_file(fp):
                continue
            
            content = self._fcache.get(fp)
            if content is None:
                continue
            
            lines = content.split('\n')
            rel_path = os.path.relpath(fp, self.base_dir)
            
            # 预处理（提取it_blocks等上下文）
            ctx = self.preprocess_file(fp, content)
            ctx['it_blocks'] = self._bc.get_it_blocks(fp)
            ctx['rel_path'] = rel_path
            
            # 逐行检测
            for i, line in enumerate(lines, 1):
                issue = self.detect_issue(fp, content, i, line, **ctx)
                if issue:
                    issues.append(issue)
        
        return issues
    
    def make_issue(self, file_path: str, line_num: int, line: str,
                   suggestion: str, testcase: str = None, **extra) -> Dict:
        """
        构建标准issue字典（共享方法）
        
        Args:
            file_path: 文件路径
            line_num: 行号
            line: 代码行
            suggestion: 修复建议
            testcase: 所属用例（可选，自动查找）
            **extra: 额外字段
        """
        rel_path = os.path.relpath(file_path, self.base_dir)
        
        # 自动查找testcase
        if testcase is None:
            if self._bc is not None:
                it_blocks = self._bc.get_it_blocks(file_path)
                testcase = find_testcase_for_line(it_blocks, line_num)
            else:
                testcase = '-'
        
        issue = {
            'rule': self.RULE_ID,
            'category': self.RULE_CATEGORY,
            'type': self.RULE_NAME,
            'severity': self.RULE_SEVERITY,
            'file': rel_path,
            'line': line_num,
            'testcase': testcase,
            'snippet': line.strip()[:120],
            'suggestion': suggestion,
            'subsystem': get_subsystem(rel_path),
        }
        
        # 合并额外字段
        issue.update(extra)
        return issue
    
    def is_comment_line(self, line: str) -> bool:
        """判断是否为注释行"""
        stripped = line.strip()
        return (stripped.startswith('//') or 
                stripped.startswith('*') or 
                stripped.startswith('/*'))
    
    def is_console_line(self, line: str) -> bool:
        """判断是否为console输出行"""
        return bool(re.search(r'console\.\s*(?:log|info|warn|error|debug)', line))
    
    def is_assignment_line(self, line: str) -> bool:
        """判断是否为变量赋值行"""
        return bool(re.match(r'\s*(?:let|const|var)\s+', line))
    
    def extract_import_vars(self, content: str, module_pattern: str) -> Set[str]:
        """提取import语句中的变量名"""
        vars_set = set()
        import_pattern = re.compile(module_pattern)
        for match in import_pattern.finditer(content):
            g1 = match.group(1)
            if g1:
                if '{' in match.group(0) and '}' in match.group(0) and ',' in g1:
                    for name in g1.split(','):
                        name = name.strip()
                        vars_set.add(name)
                else:
                    vars_set.add(g1)
        return vars_set
    
    def collect_string_vars(self, lines: List[str]) -> Set[str]:
        """收集string类型变量"""
        string_vars = set()
        for line in lines:
            m = re.search(r"(?:let|const|var)\s+(\w+)\s*=\s*['\"]([^'\"]*)['\"]", line)
            if m:
                string_vars.add(m.group(1))
            params = re.findall(r"(\w+)\s*:\s*string", line)
            string_vars.update(params)
        return string_vars


# 规则注册表（engine.py使用）
RULE_REGISTRY: Dict[str, type] = {}

def register_rule(rule_id: str, scanner_class: type):
    """注册规则扫描器"""
    RULE_REGISTRY[rule_id] = scanner_class

def get_scanner(rule_id: str, base_dir: str) -> Optional[RuleScanner]:
    """获取规则扫描器实例"""
    scanner_class = RULE_REGISTRY.get(rule_id)
    if scanner_class:
        return scanner_class(base_dir)
    return None