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
复杂规则扫描引擎 v2.0

整合需要块解析、递归追踪、远程数据获取的复杂规则：
- R004: 测试用例断言检测（递归函数调用链）
- R006: deviceInfo变量追踪
- R008: 文档注释块解析
- R010: part_name/subsystem_name匹配（远程映射表）
- R012: p7b签名证书解析
- R201-R206: 异步/资源/设计规则
"""
import os
import re
import sys
import json
import subprocess
import urllib.request
import time
from typing import Dict, List, Set, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from common import (
    FileContentCache, BlockCache, get_subsystem, find_testcase_for_line,
    find_matching_brace, find_matching_paren, parse_it_blocks, parse_describe_blocks,
    grep_scan, extract_block_body, extract_called_functions, extract_hook_body,
    find_hook_line, find_function_definition, parse_imports, resolve_import_path,
    check_cross_file_wrapper, is_in_sta_project, FunctionDefinitionCache,
    MAX_WRAPPER_FILE_SIZE,
    has_assertion,
)


# ============================================================================
# R004: 测试用例缺少断言（递归函数调用链追踪）
# ============================================================================

class R003Scanner:
    base_dir = ''
    """恒真断言检测（精确匹配3个模式）"""
    
    PATTERNS = [
        (re.compile(r'expect\s*\(\s*true\s*\)\s*\.\s*assertTrue\s*\('), 'expect(true).assertTrue()恒成立'),
        (re.compile(r'expect\s*\(\s*true\s*\)\s*\.\s*assertEqual\s*\(\s*true\s*\)'), 'expect(true).assertEqual(true)恒成立'),
        (re.compile(r'expect\s*\(\s*false\s*\)\s*\.\s*assertFalse\s*\('), 'expect(false).assertFalse()恒成立'),
    ]
    
    def scan_file(self, fp: str, content: str, fcache: FileContentCache, bc: BlockCache) -> List[Dict]:
        """检测恒真断言"""
        issues = []
        rel_path = os.path.relpath(fp, self.base_dir)
        
        lines = content.split('\n')
        it_blocks = bc.get_it_blocks(fp)
        
        for i, line in enumerate(lines, 1):
            for pattern, suggestion in self.PATTERNS:
                if pattern.search(line):
                    testcase = find_testcase_for_line(it_blocks, i)
                    issues.append({
                        'rule': 'R003',
                        'category': '编码规范合规',
                        'type': '禁止恒真断言',
                        'severity': 'Critical',
                        'file': rel_path,
                        'line': i,
                        'testcase': testcase,
                        'snippet': line.strip()[:80],
                        'suggestion': suggestion + '，请替换为对实际业务逻辑的有效断言',
                        'subsystem': get_subsystem(rel_path),
                    })
        
        return issues


class R004Scanner:
    """测试用例断言检测（采用v1.1核心逻辑）"""
    
    MAX_RECURSION_DEPTH = 5
    
    def scan_file(self, fp: str, content: str, fcache: FileContentCache, bc: BlockCache) -> List[Dict]:
        """扫描单个文件的断言问题（包含try-catch检测和递归追踪）"""
        issues = []
        rel_path = os.path.relpath(fp, self.base_dir if hasattr(self, 'base_dir') else '')
        
        if not re.search(r'\bit\s*\(', content):
            return issues
        
        local_funcs = self._collect_function_definitions(content)
        class_methods = self._extract_class_methods(content)
        local_funcs.update(class_methods)
        
        imports = parse_imports(content)
        imported_funcs = {}
        for name, import_path in imports.items():
            resolved = resolve_import_path(fp, import_path)
            if resolved:
                imported_funcs.update(self._get_imported_functions(resolved, fcache))
        
        it_blocks = bc.get_it_blocks(fp)
        lines = content.split('\n')
        
        # 去重：同一个函数的try-catch问题只报告一次
        reported_gap_keys = set()
        
        for it_block in it_blocks:
            it_name = it_block['name']
            it_line = it_block['start']
            body = extract_block_body(content, it_line, it_block['end'])
            
            if not body:
                continue
            
            # 直接检测断言
            if has_assertion(body):
                continue
            
            # 递归检测封装函数中的断言
            has_assertion_via_func = self._check_function_has_assertion(body, local_funcs, imported_funcs)
            if has_assertion_via_func:
                # 检查被调用函数内部的try-catch问题
                tc_gaps = self._find_try_catch_gaps_in_called_functions(body, local_funcs, imported_funcs)
                if tc_gaps:
                    gap_parts = []
                    for gap in tc_gaps:
                        # 去重：同一个函数的同一个问题只报告一次
                        gap_key = (gap['func_name'], gap['line'], gap['gap_type'])
                        if gap_key in reported_gap_keys:
                            continue
                        reported_gap_keys.add(gap_key)
                        
                        if gap['gap_type'] == 'catch_missing':
                            gap_parts.append(f"函数 {gap['func_name']} 的catch块（第{gap['line']}行）缺少断言")
                        elif gap['gap_type'] == 'try_missing':
                            gap_parts.append(f"函数 {gap['func_name']} 的try块（第{gap['line']}行）缺少断言")
                    
                    if gap_parts:
                        snippet = lines[it_line - 1].strip()[:120]
                        issues.append({
                            'rule': 'R004',
                            'category': '编码规范合规',
                            'type': '测试用例缺少断言',
                            'severity': 'Critical',
                            'file': rel_path,
                            'line': it_line,
                            'testcase': it_name,
                            'snippet': snippet,
                            'suggestion': f"调用的辅助函数存在try-catch断言缺陷。{'; '.join(gap_parts[:3])}。请确保所有分支都包含断言方法。",
                            'subsystem': get_subsystem(rel_path),
                        })
                        continue
                    else:
                        continue
                else:
                    continue
            
            # 检测try-catch结构中的断言问题
            try_catch_issue = self._analyze_try_catch(body, it_line, local_funcs, imported_funcs)
            if try_catch_issue:
                snippet = lines[it_line - 1].strip()[:120]
                issues.append({
                    'rule': 'R004',
                    'category': '编码规范合规',
                    'type': '测试用例缺少断言',
                    'severity': 'Critical',
                    'file': rel_path,
                    'line': it_line,
                    'testcase': it_name,
                    'snippet': snippet,
                    'suggestion': try_catch_issue,
                    'subsystem': get_subsystem(rel_path),
                })
                continue
            
            # 检测注释掉的断言
            commented_assertions = self._find_commented_assertions(body)
            if commented_assertions:
                snippet = lines[it_line - 1].strip()[:120]
                issues.append({
                    'rule': 'R004',
                    'category': '编码规范合规',
                    'type': '测试用例缺少断言',
                    'severity': 'Warning',
                    'file': rel_path,
                    'line': it_line,
                    'testcase': it_name,
                    'snippet': snippet,
                    'suggestion': f'检测到注释掉的断言（第{", ".join(map(str, commented_assertions[:3]))}行），可能影响测试有效性',
                    'subsystem': get_subsystem(rel_path),
                })
                continue
            
            # 完全缺少断言
            snippet = lines[it_line - 1].strip()[:120]
            issues.append({
                'rule': 'R004',
                'category': '编码规范合规',
                'type': '测试用例缺少断言',
                'severity': 'Critical',
                'file': rel_path,
                'line': it_line,
                'testcase': it_name,
                'snippet': snippet,
                'suggestion': '请在it()块中添加expect或assert*断言方法',
                'subsystem': get_subsystem(rel_path),
            })
        
        return issues
    
    def _check_function_has_assertion(self, body: str, local_funcs: Dict, imported_funcs: Dict,
                                       visited: Set = None, depth: int = 0) -> bool:
        """递归检测函数调用链中的断言"""
        if visited is None:
            visited = set()
        
        if depth > self.MAX_RECURSION_DEPTH:
            return False
        
        # 检测封装函数中的断言
        called_funcs = extract_called_functions(body)
        for func_name in called_funcs:
            if func_name in visited:
                continue
            visited.add(func_name)
            
            # 处理成员方法调用: Obj.methodName
            if '.' in func_name:
                obj_name, method_name = func_name.split('.', 1)
                # 检查对象是否在导入列表中
                if obj_name in imported_funcs:
                    obj_body = imported_funcs[obj_name]
                    # 在对象定义中查找方法定义
                    method_body = self._find_class_method(obj_body, method_name)
                    if method_body and has_assertion(method_body):
                        return True
                continue
            
            # 本地函数
            if func_name in local_funcs:
                func_body = local_funcs[func_name]
                if has_assertion(func_body):
                    return True
                if self._check_function_has_assertion(func_body, local_funcs, imported_funcs, visited, depth + 1):
                    return True
            
            # 导入函数
            if func_name in imported_funcs:
                func_body = imported_funcs[func_name]
                if has_assertion(func_body):
                    return True
        
        return False
    
    def _find_class_method(self, class_body: str, method_name: str) -> Optional[str]:
        """在类定义中查找方法定义"""
        # 先找到方法名称的位置
        method_start_pattern = re.compile(
            rf'(?:static\s+)?(?:async\s+)?(?:public|private|protected\s+)?'
            rf'{re.escape(method_name)}\s*\('
        )
        
        match = method_start_pattern.search(class_body)
        if not match:
            return None
        
        # 找到方法参数的结束括号（处理嵌套括号）
        start_idx = match.end() - 1  # 第一个(的位置
        paren_end = find_matching_paren(class_body, start_idx)
        if paren_end == -1:
            return None
        
        # 找到方法体的起始大括号
        brace_start = class_body.find('{', paren_end)
        if brace_start == -1:
            return None
        
        # 找到方法体的结束大括号
        block_end = find_matching_brace(class_body, brace_start)
        if block_end == -1:
            return None
        
        return class_body[brace_start + 1:block_end]
    
    def _analyze_try_catch(self, body: str, body_start_line: int, local_funcs: Dict, imported_funcs: Dict) -> str:
        """分析try-catch结构中的断言问题"""
        try_blocks = self._find_try_catch_blocks(body)
        
        if not try_blocks:
            return None
        
        issues = []
        for tb in try_blocks:
            try_has_assertion = has_assertion(tb['try_content'])
            catch_has_assertion = has_assertion(tb['catch_content']) if tb['catch_content'] else True
            
            # 通过封装函数检测
            if not try_has_assertion:
                try_has_assertion = self._check_function_has_assertion(tb['try_content'], local_funcs, imported_funcs)
            if not catch_has_assertion and tb['catch_content']:
                catch_has_assertion = self._check_function_has_assertion(tb['catch_content'], local_funcs, imported_funcs)
            
            try_line = body_start_line + tb['try_line']
            catch_line = body_start_line + tb['catch_line'] if tb['catch_line'] != -1 else 0
            
            if not try_has_assertion and not catch_has_assertion:
                if catch_line:
                    issues.append(f'try块（第{try_line}行）和catch块（第{catch_line}行）都缺少断言')
                else:
                    issues.append(f'try块（第{try_line}行）缺少断言')
            elif not try_has_assertion:
                issues.append(f'try块（第{try_line}行）缺少断言')
            elif not catch_has_assertion and tb['catch_content']:
                issues.append(f'catch块（第{catch_line}行）缺少断言')
        
        if issues:
            return f'检测到try-catch结构，{"; ".join(issues)}。请确保try和catch的每个分支都包含断言方法。'
        
        return None
    
    def _find_try_catch_blocks(self, body: str) -> List[Dict]:
        """查找try-catch块"""
        try_blocks = []
        lines = body.split('\n')
        
        i = 0
        while i < len(lines):
            stripped = lines[i].strip()
            if re.match(r'try\s*\{', stripped):
                try_start = i
                brace_count = stripped.count('{') - stripped.count('}')
                j = i + 1
                
                while j < len(lines) and brace_count > 0:
                    line_j = lines[j].strip()
                    brace_count += line_j.count('{') - line_j.count('}')
                    if re.match(r'\}\s*catch\s*(?:\([^)]*\))?\s*\{', line_j):
                        break
                    j += 1
                
                if j >= len(lines):
                    i += 1
                    continue
                
                try_content = '\n'.join(lines[try_start:j])
                
                # 查找catch块
                catch_start = j
                catch_brace_count = 1
                k = catch_start + 1
                while k < len(lines) and catch_brace_count > 0:
                    catch_brace_count += lines[k].count('{') - lines[k].count('}')
                    k += 1
                
                catch_content = '\n'.join(lines[catch_start:k])
                
                try_blocks.append({
                    'try_content': try_content,
                    'catch_content': catch_content,
                    'try_line': try_start,
                    'catch_line': catch_start,
                })
                
                i = k
            else:
                i += 1
        
        return try_blocks
    
    def _find_commented_assertions(self, body: str) -> List[int]:
        """查找注释掉的断言"""
        commented_lines = []
        lines = body.split('\n')
        
        commented_assertion_pattern = re.compile(
            r'^\s*//\s*(expect\s*\(|assertEqual\s*\(|assertTrue\s*\(|'
            r'assertFalse\s*\(|assertNull\s*\(|assertFail\s*\()'
        )
        
        for i, line in enumerate(lines):
            if commented_assertion_pattern.match(line):
                commented_lines.append(i + 1)
        
        return commented_lines
    
    def _find_try_catch_gaps_in_called_functions(self, body: str, local_funcs: Dict, 
                                                    imported_funcs: Dict, visited: Set = None, 
                                                    depth: int = 0) -> List[Dict]:
        """递归检查被调用函数内部的try-catch断言缺陷"""
        if visited is None:
            visited = set()
        
        if depth > self.MAX_RECURSION_DEPTH:
            return []
        
        all_gaps = []
        called_funcs = extract_called_functions(body)
        
        for func_name in called_funcs:
            key = f"tc_gap:{func_name}"
            if key in visited:
                continue
            
            # 本地函数
            if func_name in local_funcs:
                visited.add(key)
                func_body = local_funcs[func_name]
                gaps = self._find_try_catch_gaps_in_func_body(func_body, func_name, 0)
                all_gaps.extend(gaps)
                
                # 递归检查函数体中调用的其他函数
                sub_gaps = self._find_try_catch_gaps_in_called_functions(
                    func_body, local_funcs, imported_funcs, visited, depth + 1
                )
                all_gaps.extend(sub_gaps)
            
            # 导入函数
            if func_name in imported_funcs:
                visited.add(key)
                func_body = imported_funcs[func_name]
                gaps = self._find_try_catch_gaps_in_func_body(func_body, func_name, 0)
                all_gaps.extend(gaps)
        
        return all_gaps
    
    def _find_try_catch_gaps_in_func_body(self, body: str, func_name: str, 
                                           func_start_line: int) -> List[Dict]:
        """分析函数体内部的try-catch断言缺陷"""
        gaps = []
        try_blocks = self._find_try_catch_blocks(body)
        
        for tb in try_blocks:
            try_has = has_assertion(tb['try_content'])
            catch_has = has_assertion(tb['catch_content']) if tb['catch_content'] else True
            
            # try块缺少断言
            if not try_has:
                abs_try_line = func_start_line + tb['try_line'] + 1
                gaps.append({
                    'func_name': func_name,
                    'line': abs_try_line,
                    'gap_type': 'try_missing',
                })
            
            # catch块缺少断言
            if tb['catch_content'] and not catch_has:
                abs_catch_line = func_start_line + tb['catch_line'] + 1
                gaps.append({
                    'func_name': func_name,
                    'line': abs_catch_line,
                    'gap_type': 'catch_missing',
                })
        
        return gaps
    
    def _collect_function_definitions(self, content: str) -> Dict[str, str]:
        """收集函数定义"""
        funcs = {}
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            # function声明
            m = re.search(r'function\s+(\w+)\s*\(', line)
            if m:
                fname = m.group(1)
                remaining = '\n'.join(lines[i:])
                brace_idx = remaining.find('{')
                if brace_idx == -1:
                    continue
                block_end = find_matching_brace(remaining, brace_idx)
                if block_end == -1:
                    continue
                funcs[fname] = remaining[brace_idx + 1:block_end]
            
            # 箭头函数
            m = re.search(r'(?:let|const|var)\s+(\w+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>', line)
            if m:
                fname = m.group(1)
                remaining = '\n'.join(lines[i:])
                brace_idx = remaining.find('{')
                if brace_idx == -1:
                    continue
                block_end = find_matching_brace(remaining, brace_idx)
                if block_end == -1:
                    continue
                funcs[fname] = remaining[brace_idx + 1:block_end]
        
        return funcs
    
    def _extract_class_methods(self, content: str) -> Dict[str, str]:
        """提取类方法"""
        methods = {}
        m = re.search(r'class\s+\w+\s*\{', content)
        if not m:
            return methods
        
        brace_idx = m.end() - 1
        block_end = find_matching_brace(content, brace_idx)
        if block_end == -1:
            return methods
        
        class_body = content[brace_idx + 1:block_end]
        
        for m in re.finditer(r'(?:async\s+)?(\w+)\s*\([^)]*\)\s*\{', class_body):
            fname = m.group(1)
            remaining = class_body[m.start():]
            brace = remaining.find('{')
            if brace == -1:
                continue
            end = find_matching_brace(remaining, brace)
            if end == -1:
                continue
            methods[fname] = remaining[brace + 1:end]
        
        return methods
    
    def _get_imported_functions(self, filepath: str, fcache: FileContentCache) -> Dict[str, str]:
        """获取导入文件中的函数定义和类定义"""
        try:
            content = fcache.get(filepath)
            if content is None:
                return {}
            
            funcs = self._collect_function_definitions(content)
            methods = self._extract_class_methods(content)
            funcs.update(methods)
            
            # 提取导出的类定义（支持export class）
            classes = self._extract_exported_classes(content)
            funcs.update(classes)
            
            return funcs
        except Exception:
            return {}
    
    def _extract_exported_classes(self, content: str) -> Dict[str, str]:
        """提取导出的类定义（export class / export default class）"""
        classes = {}
        # 匹配 export class 和 export default class
        pattern = re.compile(r'export\s+(?:default\s+)?class\s+(\w+)\s*\{')
        
        for match in pattern.finditer(content):
            class_name = match.group(1)
            brace_idx = match.end() - 1
            block_end = find_matching_brace(content, brace_idx)
            if block_end > 0:
                classes[class_name] = content[brace_idx + 1:block_end]
            else:
                # Fallback: 如果大括号匹配失败，提取到文件末尾（用于处理文件语法错误或未闭合的情况）
                last_brace = content.rfind('}')
                if last_brace > brace_idx:
                    classes[class_name] = content[brace_idx + 1:last_brace]
        
        return classes


# ============================================================================
# R006: 禁止基于设备类型差异化
# ============================================================================

class R006Scanner:
    """deviceInfo.deviceType检测"""
    
    DEVICEINFO_IMPORT_PATTERNS = [
        re.compile(r"import\s+.*deviceInfo\s+.*from\s+['\"]@ohos\.deviceInfo['\"]"),
        re.compile(r"import\s+\{[^}]*deviceInfo[^}]*\}\s+from\s+['\"]@kit\.BasicServicesKit['\"]"),
    ]
    base_dir = ''
    
    def scan_file(self, fp: str, content: str, fcache: FileContentCache, bc: BlockCache) -> List[Dict]:
        """检测deviceInfo.deviceType在条件判断中的使用"""
        issues = []
        
        has_import = any(p.search(content) for p in self.DEVICEINFO_IMPORT_PATTERNS)
        if not has_import:
            return issues
        
        rel_path = os.path.relpath(fp, self.base_dir)
        it_blocks = bc.get_it_blocks(fp)
        lines = content.split('\n')
        
        assigned_vars = set()
        var_pattern = re.compile(r'(?:let|const|var)\s+(\w+)\s*(?::\s*string)?\s*=\s*deviceInfo\.deviceType')
        for line in lines:
            m = var_pattern.search(line)
            if m:
                assigned_vars.add(m.group(1))
        
        seen_lines = set()
        for i, line in enumerate(lines, 1):
            if i in seen_lines:
                continue
            if re.search(r'console\.\s*(?:log|info|debug|error|warn)', line):
                continue
            stripped = line.strip()
            if re.match(r'^(let|const|var|this\.)', stripped) and not re.search(r'\b(if|else|switch|case|return|&&|\|\||\?)\b', stripped):
                continue
            if re.search(r'\bdeviceInfo\.deviceType\b', line):
                if re.search(r'(if\s*\(|else\s*if\s*\(|switch\s*\(|case\s+|\?\s*|&&|\|\||==|!=|\breturn\b)', line):
                    seen_lines.add(i)
                    testcase = find_testcase_for_line(it_blocks, i)
                    issues.append({
                        'rule': 'R006',
                        'category': '编码规范合规',
                        'type': '禁止基于设备类型差异化',
                        'severity': 'Critical',
                        'file': rel_path,
                        'line': i,
                        'testcase': testcase,
                        'snippet': stripped[:120],
                        'suggestion': '使用SystemCapability和canIUse进行能力判断',
                        'subsystem': get_subsystem(rel_path),
                    })
                    continue
            for var_name in assigned_vars:
                if re.search(rf'\b{re.escape(var_name)}\.\w+\s*$', stripped):
                    continue
                if re.match(rf'^\s*(?:let|const|var)\s+{re.escape(var_name)}\s*=', line):
                    continue
                if re.search(rf'\b{re.escape(var_name)}\b', line):
                    if re.search(r'(if\s*\(|else\s*if\s*\(|switch\s*\(|case\s+|\?\s*|&&|\|\||==|!=)', line):
                        seen_lines.add(i)
                        testcase = find_testcase_for_line(it_blocks, i)
                        issues.append({
                            'rule': 'R006',
                            'category': '编码规范合规',
                            'type': '禁止基于设备类型差异化',
                            'severity': 'Critical',
                            'file': rel_path,
                            'line': i,
                            'testcase': testcase,
                            'snippet': stripped[:120],
                            'suggestion': f'使用变量{var_name}进行设备类型判断，应使用SystemCapability和canIUse进行能力判断',
                            'subsystem': get_subsystem(rel_path),
                        })
                        break
        
        return issues


# ============================================================================
# R008: 用例声明格式不规范
# ============================================================================

_COLON_SEP_RE = re.compile(r'@(tc\.\w+)\s*:\s')
_NO_AT_RE = re.compile(r'^\s*(tc\.\w+)\s+\S')

class R008Scanner:
    """文档注释格式检测"""
    
    base_dir = ''
    
    def scan_file(self, fp: str, content: str, fcache: FileContentCache, bc: BlockCache) -> List[Dict]:
        """检测文档注释格式问题"""
        issues = []
        rel_path = os.path.relpath(fp, self.base_dir)
        
        # 只扫描测试文件
        if not (fp.endswith('.test.ets') or fp.endswith('.test.ts') or fp.endswith('.test.js')):
            return issues
        
        doc_blocks = self._extract_doc_blocks(content)
        
        for block in doc_blocks:
            block_issues = self._check_doc_block(block)
            for issue in block_issues:
                issues.append({
                    'rule': 'R008',
                    'category': '编码规范合规',
                    'type': '用例声明格式不规范',
                    'severity': 'Warning',
                    'file': rel_path,
                    'line': issue['line'],
                    'testcase': block['testcase'],
                    'snippet': issue['snippet'][:120],
                    'suggestion': issue['detail'],
                    'subsystem': get_subsystem(rel_path),
                })
        
        return issues
    
    def _extract_doc_blocks(self, content: str) -> List[Dict]:
        """提取文档注释块"""
        blocks = []
        lines = content.split('\n')
        i = 0
        
        while i < len(lines):
            stripped = lines[i].strip()
            if stripped.startswith('/**'):
                block_start = i + 1
                block_lines = [lines[i]]
                j = i + 1
                while j < len(lines):
                    block_lines.append(lines[j])
                    if '*/' in lines[j]:
                        break
                    j += 1
                
                block_end = j + 1
                next_code_idx = j + 1
                testcase_name = None
                has_empty_line = False
                
                while next_code_idx < len(lines) and lines[next_code_idx].strip() == '':
                    has_empty_line = True
                    next_code_idx += 1
                
                if next_code_idx < len(lines):
                    tc_match = re.search(r"\bit\s*\(\s*['\"]([^'\"]+)['\"]", lines[next_code_idx])
                    if tc_match:
                        testcase_name = tc_match.group(1)
                
                blocks.append({
                    'start_line': block_start,
                    'end_line': block_end,
                    'lines': block_lines,
                    'testcase': testcase_name or '-',
                    'has_empty_line_before_it': has_empty_line,
                })
                i = j + 1
            else:
                i += 1
        
        return blocks
    
    def _check_doc_block(self, block: Dict) -> List[Dict]:
        """检查文档注释块格式"""
        issues = []
        lines = block['lines']
        
        first_line = lines[0].strip()
        last_line = lines[-1].strip()
        
        if not first_line.startswith('/**'):
            issues.append({
                'line': block['start_line'],
                'snippet': first_line,
                'detail': '文档注释未以/**开头'
            })
        
        if '*/' not in last_line and (len(lines) == 1 or '*/' not in lines[-1]):
            issues.append({
                'line': block['end_line'],
                'snippet': last_line,
                'detail': '文档注释未以*/结尾'
            })
        
        for idx, line in enumerate(lines[1:-1], start=block['start_line'] + 1):
            stripped = line.strip()
            if stripped and not stripped.startswith('*'):
                issues.append({
                    'line': idx,
                    'snippet': stripped,
                    'detail': '注释行未以*开始'
                })
        
        for idx, line in enumerate(lines, start=block['start_line']):
            colon_match = _COLON_SEP_RE.search(line)
            if colon_match:
                issues.append({
                    'line': idx,
                    'snippet': line.strip(),
                    'detail': f'参数 {colon_match.group(1)} 使用了冒号分隔符，应使用空格'
                })
        
        for idx, line in enumerate(lines, start=block['start_line']):
            inner = line.strip().lstrip('*').strip()
            no_at_match = _NO_AT_RE.match(inner)
            if no_at_match:
                issues.append({
                    'line': idx,
                    'snippet': line.strip(),
                    'detail': f'参数 {no_at_match.group(1)} 缺少@修饰符'
                })
        
        if block['has_empty_line_before_it'] and block['testcase'] != '-':
            issues.append({
                'line': block['end_line'],
                'snippet': '*/ 后存在空行',
                'detail': '文档注释结束行与测试用例之间不应有空行'
            })
        
        return issues


# ============================================================================
# R016: testcase命名规范
# ============================================================================

class R016Scanner:
    """testcase命名规范检测"""
    
    TC_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9_-]+$')
    IT_PATTERN = re.compile(r'\bit\s*\(\s*([\'"])([^\'"]+)\1')
    base_dir = ''
    
    def scan_file(self, fp: str, content: str, fcache: FileContentCache, bc: BlockCache) -> List[Dict]:
        """检测it()参数命名规范"""
        issues = []
        rel_path = os.path.relpath(fp, self.base_dir)
        
        it_blocks = bc.get_it_blocks(fp)
        lines = content.split('\n')
        
        it_entries = self._extract_all_it_entries(lines)
        
        for entry in it_entries:
            tc_name = entry['it_tc_name']
            it_line_idx = entry['line_idx']
            
            if self.TC_NAME_PATTERN.match(tc_name):
                continue
            
            snippet = lines[it_line_idx].strip()
            if len(snippet) > 120:
                snippet = snippet[:120] + '...'
            
            suggestion = self._build_r016_suggestion(rel_path, it_line_idx + 1, tc_name, lines, entry)
            testcase = find_testcase_for_line(it_blocks, it_line_idx + 1)
            
            issues.append({
                'rule': 'R016',
                'category': '编码规范合规',
                'type': 'testcase命名规范',
                'severity': 'Warning',
                'file': rel_path,
                'line': it_line_idx + 1,
                'testcase': tc_name,
                'snippet': snippet,
                'suggestion': suggestion,
                'subsystem': get_subsystem(rel_path),
            })
        
        return issues
    
    def _extract_all_it_entries(self, lines: List[str]) -> List[Dict]:
        """提取所有it()条目"""
        entries = []
        i = 0
        while i < len(lines):
            line = lines[i]
            match = self.IT_PATTERN.search(line)
            if match:
                it_tc_name = match.group(2)
                tc_name_line_idx = None
                has_tc_annotation = False
                
                for back in range(i - 1, max(i - 20, -1), -1):
                    back_line = lines[back].strip()
                    if not back_line:
                        continue
                    if back_line.startswith('* @tc.name') or back_line.startswith('@tc.name'):
                        break
                    if back_line.startswith('/**') or back_line.startswith('/*'):
                        break
                    if not back_line.startswith('*') and not back_line.startswith('//'):
                        break
                
                entries.append({
                    'line_idx': i,
                    'it_tc_name': it_tc_name,
                    'has_tc_annotation': has_tc_annotation,
                })
            
            i += 1
        
        return entries
    
    def _build_r016_suggestion(self, file_path: str, line_num: int, tc_name: str, 
                               lines: List[str], entry: Dict) -> str:
        """构建R016修复建议"""
        import re as re_module
        cleaned = re_module.sub(r'[^a-zA-Z0-9_-]', '', tc_name)
        if not cleaned:
            cleaned = 'unnamedTest'
        
        existing_names = set()
        for e in self._extract_all_it_entries(lines):
            existing_names.add(e['it_tc_name'])
        
        new_name = None
        for suffix_num in range(1, 1000):
            candidate = f"{cleaned}Adapt{suffix_num:03d}"
            if candidate not in existing_names:
                new_name = candidate
                break
        
        if new_name is None:
            new_name = f"{cleaned}Adapt999"
        
        suggestion_parts = [
            f"路径: {file_path}, 行号: {line_num}, ",
            f"问题描述: testcase名称 '{tc_name}' 包含特殊字符。",
            f"仅允许英文字母、数字、下划线、连字符。",
        ]
        
        if entry['has_tc_annotation']:
            suggestion_parts.append(
                f"修复: 将it()参数和@tc.name修改为 '{new_name}'。"
            )
        else:
            suggestion_parts.append(
                f"修复: 将it()参数修改为 '{new_name}'。"
            )
        
        return ''.join(suggestion_parts)


# ============================================================================
# R009: @tc.number命名不规范
# ============================================================================

class R009Scanner:
    """@tc.number命名规范检测"""
    
    TC_NUMBER_PATTERN = re.compile(r'@tc\.number\s+([^\s*]+)')
    base_dir = ''
    
    def scan_file(self, fp: str, content: str, fcache: FileContentCache, bc: BlockCache) -> List[Dict]:
        """检测@tc.number命名格式"""
        # 只扫描测试文件
        if not (fp.endswith('.test.ets') or fp.endswith('.test.ts') or fp.endswith('.test.js')):
            return []
        
        # grep预过滤
        if '@tc.number' not in content and '@tc.number' not in content:
            return []
        
        issues = []
        rel_path = os.path.relpath(fp, self.base_dir)
        
        it_blocks = bc.get_it_blocks(fp)
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            match = self.TC_NUMBER_PATTERN.search(line)
            if match:
                tc_number = match.group(1).strip()
                errors = self._validate_tc_number(tc_number)
                
                if errors:
                    testcase = find_testcase_for_line(it_blocks, i)
                    
                    snippet = line.strip()
                    if len(snippet) > 120:
                        snippet = snippet[:120] + '...'
                    
                    suggestion = (
                        f"路径: {rel_path}, 行号: {i}, "
                        f"问题描述: @tc.number命名不规范: {'; '.join(errors)}。"
                        "正确格式: SUB_{子系统}_{部件}_XXXX"
                    )
                    
                    issues.append({
                        'rule': 'R009',
                        'category': '编码规范合规',
                        'type': '@tc.number命名不规范',
                        'severity': 'Warning',
                        'file': rel_path,
                        'line': i,
                        'testcase': testcase,
                        'snippet': snippet,
                        'suggestion': suggestion,
                        'subsystem': get_subsystem(rel_path),
                    })
        
        return issues
    
    def _validate_tc_number(self, tc_number: str) -> List[str]:
        """验证@tc.number格式"""
        errors = []
        
        # 规则1: 必须以SUB_开头
        if not tc_number.startswith('SUB_'):
            errors.append(f'不以SUB_开头')
            return errors
        
        # 规则2: SUB_后必须至少有3段（子系统_部件_数字）
        remainder = tc_number[4:]
        if not remainder:
            errors.append('SUB_后缺少内容')
            return errors
        
        segments = remainder.split('_')
        if len(segments) < 3:
            errors.append(f'段数不足（至少需要3段: 子系统_部件_数字）')
            return errors
        
        # 规则3: 子系统名称必须全大写字母
        subsystem = segments[0]
        if subsystem != subsystem.upper() or not subsystem.isalpha():
            errors.append(f'子系统"{subsystem}"应使用全大写字母')
        
        # 规则4: 部件名称必须全大写字母
        component = segments[1]
        if component != component.upper() or not component.isalpha():
            errors.append(f'部件"{component}"应使用全大写字母')
        
        # 规则5: 最后一段必须是4位数字
        last_segment = segments[-1]
        if not last_segment.isdigit():
            errors.append(f'数字部分"{last_segment}"应为纯数字')
        elif len(last_segment) != 4:
            errors.append(f'数字部分"{last_segment}"应为4位（当前{len(last_segment)}位）')
        
        return errors


# ============================================================================
# R010: part_name/subsystem_name不匹配（远程映射表）
# ============================================================================

_R010_MAPPING_URLS = [
    ('https://gitee.com/openharmony/vendor_hihope/raw/master/rk3568/config.json', False),
    ('https://gitee.com/openharmony/productdefine_common/raw/master/inherit/rich.json', False),
    ('https://gitee.com/openharmony/productdefine_common/raw/master/inherit/chipset_common.json', False),
]
_R010_CACHE_FILE = '/tmp/r010_mapping_cache.json'
_r010_mapping_cache = None
_r010_warning_shown = False

def _r010_load_mapping() -> Dict[str, Set[str]]:
    global _r010_mapping_cache, _r010_warning_shown
    if _r010_mapping_cache is not None:
        return _r010_mapping_cache
    
    if os.path.exists(_R010_CACHE_FILE):
        try:
            cache_age = time.time() - os.path.getmtime(_R010_CACHE_FILE)
            if cache_age < 7 * 24 * 3600:
                with open(_R010_CACHE_FILE, 'r', encoding='utf-8') as f:
                    _r010_mapping_cache = {k: set(v) for k, v in json.load(f).items()}
                return _r010_mapping_cache
        except Exception:
            pass
    
    subsystem_map = {}
    fetch_success = False
    for url, _ in _R010_MAPPING_URLS:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                fetch_success = True
            for subsys in data.get('subsystems', []):
                name = subsys.get('subsystem', '')
                if name not in subsystem_map:
                    subsystem_map[name] = set()
                for c in subsys.get('components', []):
                    if isinstance(c, str):
                        subsystem_map[name].add(c)
                    elif isinstance(c, dict):
                        subsystem_map[name].add(c.get('component', ''))
        except Exception:
            continue
    
    if subsystem_map:
        try:
            with open(_R010_CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump({k: sorted(v) for k, v in subsystem_map.items()}, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    if not subsystem_map and not _r010_warning_shown:
        print(f"警告: R010无法获取子系统-部件映射表，将跳过该规则检测", file=sys.stderr)
        print(f"  数据来源: {_R010_MAPPING_URLS[0][0]} 等3个远程配置文件", file=sys.stderr)
        print(f"  请检查网络连接，或手动下载映射表到 {_R010_CACHE_FILE}", file=sys.stderr)
        _r010_warning_shown = True
    
    _r010_mapping_cache = subsystem_map
    return subsystem_map

class R014Scanner:
    """测试HAP命名规范检测
    
    检测ohos_js_app_suite、ohos_js_app_static_suite、ohos_moduletest_suite的命名规范：
    - ohos_js_app_suite: hap_name必须以Acts开头，以Test结尾
    - ohos_js_app_static_suite: hap_name必须以Acts开头，以StaticTest结尾
    - ohos_moduletest_suite: target_name必须以Acts开头，以Test结尾
    """
    base_dir = ''
    
    TEMPLATE_TYPES = {
        'ohos_js_app_suite': {
            'pattern': re.compile(r'ohos_js_app_suite\s*\(\s*["\']([^"\']+)["\']'),
            'check_field': 'hap_name',
            'must_start': 'Acts',
            'must_end': 'Test',
        },
        'ohos_js_app_static_suite': {
            'pattern': re.compile(r'ohos_js_app_static_suite\s*\(\s*["\']([^"\']+)["\']'),
            'check_field': 'hap_name',
            'must_start': 'Acts',
            'must_end': 'StaticTest',
        },
        'ohos_moduletest_suite': {
            'pattern': re.compile(r'ohos_moduletest_suite\s*\(\s*["\']([^"\']+)["\']'),
            'check_field': 'target_name',
            'must_start': 'Acts',
            'must_end': 'Test',
        },
    }
    
    HAP_NAME_PATTERN = re.compile(r'hap_name\s*=\s*["\']([^"\']+)["\']')
    
    def scan_file(self, fp: str, content: str, fcache: FileContentCache, bc: BlockCache) -> List[Dict]:
        """检测BUILD.gn中的HAP命名规范"""
        if os.path.basename(fp) != 'BUILD.gn':
            return []
        
        issues = []
        rel_path = os.path.relpath(fp, self.base_dir)
        
        templates = self._parse_build_gn_templates(content)
        
        for template in templates:
            validation = self._validate_naming(template)
            if validation is None:
                continue
            
            suggestion = self._generate_fix_suggestion(template, validation)
            
            if validation['check_field'] == 'hap_name':
                snippet = f'hap_name = "{validation["name"]}"'
            else:
                snippet = f'{template["type"]}("{validation["name"]}")'
            
            issues.append({
                'rule': 'R014',
                'category': '编码规范合规',
                'type': '测试HAP命名不规范',
                'severity': 'Critical',
                'file': rel_path,
                'line': validation['line'],
                'testcase': '-',
                'snippet': snippet,
                'suggestion': suggestion,
                'subsystem': get_subsystem(rel_path),
            })
        
        return issues
    
    def _parse_build_gn_templates(self, content: str) -> List[Dict]:
        """解析BUILD.gn中的模板"""
        templates = []
        lines = content.split('\n')
        state = 'IDLE'
        current_template = None
        brace_depth = 0
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if state == 'IDLE':
                for tname, tinfo in self.TEMPLATE_TYPES.items():
                    match = tinfo['pattern'].search(line)
                    if match:
                        target_name = match.group(1)
                        current_template = {
                            'type': tname,
                            'target_name': target_name,
                            'target_line': line_num,
                            'hap_name': None,
                            'hap_name_line': 0,
                        }
                        state = 'IN_TEMPLATE'
                        brace_depth = line.count('{') - line.count('}')
                        break
            
            elif state == 'IN_TEMPLATE':
                brace_depth += line.count('{') - line.count('}')
                hap_match = self.HAP_NAME_PATTERN.search(line)
                if hap_match:
                    current_template['hap_name'] = hap_match.group(1)
                    current_template['hap_name_line'] = line_num
                
                if brace_depth <= 0:
                    templates.append(current_template)
                    current_template = None
                    state = 'IDLE'
        
        return templates
    
    def _validate_naming(self, template: Dict) -> Optional[Dict]:
        """验证命名规范"""
        tname = template['type']
        tinfo = self.TEMPLATE_TYPES[tname]
        
        if tinfo['check_field'] == 'hap_name':
            name = template['hap_name']
            report_line = template['hap_name_line']
        else:
            name = template['target_name']
            report_line = template['target_line']
        
        if not name:
            return None
        
        if 'validator' in name.lower():
            return None
        
        must_start = tinfo['must_start']
        must_end = tinfo['must_end']
        
        starts_ok = name.startswith(must_start)
        ends_ok = name.endswith(must_end)
        
        if starts_ok and ends_ok:
            return None
        
        errors = []
        if not starts_ok:
            errors.append(f'不以"{must_start}"开头')
        if not ends_ok:
            errors.append(f'不以"{must_end}"结尾')
        
        return {
            'name': name,
            'line': report_line,
            'errors': errors,
            'template_type': tname,
            'check_field': tinfo['check_field'],
        }
    
    def _generate_fix_suggestion(self, template: Dict, validation: Dict) -> str:
        """生成修复建议"""
        name = validation['name']
        tname = validation['template_type']
        check_field = validation['check_field']
        tinfo = self.TEMPLATE_TYPES[tname]
        errors = validation['errors']
        
        must_start = tinfo['must_start']
        must_end = tinfo['must_end']
        
        fixed_name = name
        if not fixed_name.startswith(must_start):
            fixed_name = must_start + fixed_name[0].upper() + fixed_name[1:]
        if not fixed_name.endswith(must_end):
            fixed_name = fixed_name + 'Adapt001' + must_end
        
        if check_field == 'hap_name':
            target_info = f"target名称 \"{template['target_name']}\" 保持不变，只修改hap_name"
        else:
            target_info = f"target名称 \"{template['target_name']}\" 需要修改为 \"{fixed_name}\""
        
        return (
            f"{check_field} \"{name}\" 不符合规范：{', '.join(errors)}。"
            f"修复: {check_field}改为 \"{fixed_name}\"。{target_info}。"
        )


class R010Scanner:
    base_dir = ''
    
    def scan_file(self, fp: str, content: str, fcache: FileContentCache, bc: BlockCache) -> List[Dict]:
        if os.path.basename(fp) != 'BUILD.gn':
            return []
        
        subsystem_map = _r010_load_mapping()
        if not subsystem_map:
            return []
        
        issues = []
        rel_path = os.path.relpath(fp, self.base_dir)
        
        part_match = re.search(r'part_name\s*=\s*["\']([^"\']+)["\']', content)
        subsys_match = re.search(r'subsystem_name\s*=\s*["\']([^"\']+)["\']', content)
        
        if not part_match or not subsys_match:
            return issues
        
        part_name = part_match.group(1)
        subsystem_name = subsys_match.group(1)
        
        if subsystem_name not in subsystem_map:
            return issues
        
        if part_name in subsystem_map[subsystem_name]:
            return issues
        
        part_line = 0
        for i, line in enumerate(content.split('\n'), 1):
            if re.search(r'part_name\s*=\s*["\']' + re.escape(part_name) + '["\']', line):
                part_line = i
                break
        
        issues.append({
            'rule': 'R010',
            'category': '编码规范合规',
            'type': 'part_name/subsystem_name不匹配',
            'severity': 'Critical',
            'file': rel_path,
            'line': part_line or 1,
            'testcase': '-',
            'snippet': f'part_name = "{part_name}", subsystem_name = "{subsystem_name}"',
            'suggestion': f'part_name "{part_name}" 不在 subsystem_name "{subsystem_name}" 的components中',
            'subsystem': get_subsystem(rel_path),
        })
        
        return issues


# ============================================================================
# R017: syscap.json配置多个能力
# ============================================================================

class R017Scanner:
    base_dir = ''
    
    def scan_file(self, fp: str, content: str, fcache: FileContentCache, bc: BlockCache) -> List[Dict]:
        if os.path.basename(fp) != 'syscap.json':
            return []
        
        issues = []
        rel_path = os.path.relpath(fp, self.base_dir)
        
        try:
            data = json.loads(content)
            
            cap_count = 0
            cap_key = ''
            
            xts_list = data.get('devices', {}).get('custom', [])
            if xts_list and isinstance(xts_list[0], dict):
                xts = xts_list[0].get('xts', [])
                cap_count = len(xts) if isinstance(xts, list) else 0
                cap_key = 'xts'
            
            system_caps = data.get('system_capabilities', [])
            if isinstance(system_caps, list) and len(system_caps) > 0:
                cap_count = len(system_caps)
                cap_key = 'system_capabilities'
            
            if cap_count > 1:
                lines = content.split('\n')
                line_num = 1
                for i, line in enumerate(lines, 1):
                    if cap_key in line and '[' in line:
                        line_num = i
                        break
                
                snippet = lines[line_num - 1].strip()[:120] if line_num <= len(lines) else ''
                issues.append({
                    'rule': 'R017',
                    'category': '编码规范合规',
                    'type': 'syscap.json配置多个能力',
                    'severity': 'Critical',
                    'file': rel_path,
                    'line': line_num,
                    'testcase': '-',
                    'snippet': snippet,
                    'suggestion': f'syscap.json中{cap_key}配置了{cap_count}个能力，应只配置1个能力',
                    'subsystem': get_subsystem(rel_path),
                })
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass
        
        return issues


# ============================================================================
# R023: 禁止errcode值类型强转后断言
# ============================================================================

_CAST_PATTERNS = [
    re.compile(r'\bNumber\s*\('),
    re.compile(r'\bparseInt\s*\('),
    re.compile(r'\bString\s*\('),
]

_METHOD_CAST_PATTERN = re.compile(
    r'\.code\s*\.\s*(toString|toFixed|valueOf|split|trim|substring|substr|charAt|'
    r'toUpperCase|toLowerCase|replace|match|concat|padStart|padEnd|repeat)\s*\('
)

_TS_TYPE_ASSERTION_PATTERN = re.compile(r'\.code\s+as\s+(?:number|string|Number|String)')


class R023Scanner:
    base_dir = ''
    
    def scan_file(self, fp: str, content: str, fcache: FileContentCache, bc: BlockCache) -> List[Dict]:
        issues = []
        rel_path = os.path.relpath(fp, self.base_dir)
        it_blocks = bc.get_it_blocks(fp)
        
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('//') or stripped.startswith('*'):
                continue
            
            matches = []
            for pattern in _CAST_PATTERNS:
                for m in pattern.finditer(stripped):
                    start = m.end()
                    depth = 1
                    j = start
                    while j < len(stripped) and depth > 0:
                        if stripped[j] == '(':
                            depth += 1
                        elif stripped[j] == ')':
                            depth -= 1
                        j += 1
                    if depth == 0 and '.code' in stripped[m.start():j]:
                        matches.append(m.group(0).strip().rstrip('('))
            
            for m in _METHOD_CAST_PATTERN.finditer(stripped):
                matches.append(f'.code.{m.group(1)}()')
            
            for m in _TS_TYPE_ASSERTION_PATTERN.finditer(stripped):
                matches.append('.code as type')
            
            if matches:
                testcase = find_testcase_for_line(it_blocks, i)
                issues.append({
                    'rule': 'R023',
                    'category': '编码规范合规',
                    'type': '禁止errcode值类型强转后断言',
                    'severity': 'Critical',
                    'file': rel_path,
                    'line': i,
                    'testcase': testcase,
                    'snippet': stripped[:120],
                    'suggestion': f'errcode值断言使用了类型强转{matches[0]}，应移除强转',
                    'subsystem': get_subsystem(rel_path),
                })
        
        return issues


# ============================================================================
# R012: 签名证书APL等级错误（p7b解析）
# ============================================================================

class R012Scanner:
    base_dir = ''
    APL_RE = re.compile(r'"apl"\s*:\s*"([^"]+)"')
    APP_FEATURE_RE = re.compile(r'"app-feature"\s*:\s*"([^"]+)"')
    
    def scan_file(self, fp: str, content: str, fcache: FileContentCache, bc: BlockCache) -> List[Dict]:
        """检测p7b签名证书配置"""
        if not fp.endswith('.p7b'):
            return []
        
        issues = []
        rel_path = os.path.relpath(fp, self.base_dir)
        
        config = self._extract_p7b_json(fp)
        if not config:
            return issues
        
        bundle_info = config.get('bundle-info', {})
        current_apl = bundle_info.get('apl', '')
        current_feature = bundle_info.get('app-feature', '')
        
        has_problem = current_apl == 'system_core' or \
                     (current_feature != 'hos_normal_app' and current_feature != '')
        
        if not has_problem:
            return issues
        
        issues.append({
            'rule': 'R012',
            'category': '编码规范合规',
            'type': '签名证书APL等级错误',
            'severity': 'Critical',
            'file': rel_path,
            'line': 1,
            'testcase': '-',
            'snippet': f'apl={current_apl}, app-feature={current_feature}',
            'suggestion': 'APL等级和app-feature配置错误，请修正',
            'subsystem': get_subsystem(rel_path),
        })
        
        return issues
    
    def _extract_p7b_json(self, p7b_path: str) -> Optional[Dict]:
        """从p7b提取JSON配置"""
        try:
            result = subprocess.run(
                ['openssl', 'cms', '-verify', '-in', p7b_path, '-inform', 'DER', '-noverify'],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0 and result.stdout:
                return json.loads(result.stdout)
        except Exception:
            pass
        
        try:
            with open(p7b_path, 'rb') as f:
                raw = f.read()
            text = raw.decode('utf-8', errors='replace')
            apl_match = self.APL_RE.search(text)
            feature_match = self.APP_FEATURE_RE.search(text)
            if apl_match:
                return {
                    'bundle-info': {
                        'apl': apl_match.group(1),
                        'app-feature': feature_match.group(1) if feature_match else ''
                    }
                }
        except Exception:
            pass
        
        return None


# ============================================================================
# R001: 禁止使用getSync系统接口（采用v1.1完整逻辑）
# ============================================================================

class R001Scanner:
    base_dir = ''
    """getSync系统接口检测（grep预过滤+import追踪）"""
    
    IMPORT_PATTERNS = [
        re.compile(r"import\s+\{([^}]+)\}\s+from\s+['\"]@ohos\.systemparameter['\"]"),
        re.compile(r"import\s+\{([^}]+)\}\s+from\s+['\"]@ohos\.systemParameterEnhance['\"]"),
        re.compile(r"import\s+(\w+)\s+from\s+['\"]@ohos\.systemparameter['\"]"),
        re.compile(r"import\s+(\w+)\s+from\s+['\"]@ohos\.systemParameterEnhance['\"]"),
        re.compile(r"import\s+\{([^}]*\b(?:systemParameter|systemParameterEnhance)\b[^}]*)\}\s+from\s+['\"]@kit\.BasicServicesKit['\"]"),
    ]
    
    def scan_file(self, fp: str, content: str, fcache: FileContentCache, bc: BlockCache) -> List[Dict]:
        """检测getSync调用（必须import systemParameter）"""
        issues = []
        rel_path = os.path.relpath(fp, self.base_dir)
        
        # Step 1: 检查是否导入systemParameter
        has_system_param_import = False
        system_param_vars = set()
        
        for pattern in self.IMPORT_PATTERNS:
            for match in pattern.finditer(content):
                has_system_param_import = True
                g1 = match.group(1)
                if g1:
                    # 解析导入的变量名
                    if '{' in match.group(0) and '}' in match.group(0) and ',' in g1:
                        for name in g1.split(','):
                            name = name.strip()
                            if name in ('systemParameter', 'systemParameterEnhance'):
                                system_param_vars.add(name)
                    elif g1 in ('systemParameter', 'systemParameterEnhance'):
                        system_param_vars.add(g1)
                    elif 'systemParameter' in g1 or 'systemParameterEnhance' in g1:
                        nm = re.search(r'\b(systemParameter|systemParameterEnhance)\b', g1)
                        if nm:
                            system_param_vars.add(nm.group(1))
                    else:
                        system_param_vars.add(g1)
        
        # Step 2: 未导入systemParameter则跳过
        if not has_system_param_import:
            return issues
        
        # Step 3: 检测getSync调用（变量必须在import列表中）
        it_blocks = bc.get_it_blocks(fp)
        lines = content.split('\n')
        
        getsync_pattern = re.compile(r'(\w+)\.getSync\s*\(')
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('//') or stripped.startswith('*'):
                continue
            
            for match in getsync_pattern.finditer(line):
                var_name = match.group(1)
                # 只有导入的systemParameter变量调用getSync才报错
                if var_name in system_param_vars:
                    testcase = find_testcase_for_line(it_blocks, i)
                    issues.append({
                        'rule': 'R001',
                        'category': '编码规范合规',
                        'type': '禁止使用getSync系统接口',
                        'severity': 'Critical',
                        'file': rel_path,
                        'line': i,
                        'testcase': testcase,
                        'snippet': line.strip(),
                        'suggestion': "多设备XTS适配禁止使用getSync()系统接口。请使用canIUse接口替代或差异化API接口替代。",
                        'subsystem': get_subsystem(rel_path),
                    })
        
        return issues


# ============================================================================
# R201: 异步用例缺少done回调
# ============================================================================

class R201Scanner:
    base_dir = ''
    """异步done/await检测（采用v1.1完整逻辑）"""
    
    ASYNC_INDICATORS = [
        r'\bsetTimeout\s*\(',
        r'\bsetInterval\s*\(',
        r'\.\s*then\s*\(',
        r'\bnew\s+Promise\s*[<(]',
        r'(?:callback|cb|onComplete|onSuccess|onError|onResult)\s*[,\)]',
    ]
    
    def scan_file(self, fp: str, content: str, fcache: FileContentCache, bc: BlockCache,
                  sta_projects: Set[str] = None, fdef_cache=None) -> List[Dict]:
        """检测异步用例问题（包含封装函数追踪）"""
        issues = []
        rel_path = os.path.relpath(fp, self.base_dir)
        
        # Sta工程特殊检测：async executor
        if sta_projects and is_in_sta_project(fp, sta_projects):
            issues.extend(self._check_sta_async_executor(content, rel_path))
        
        it_blocks = bc.get_it_blocks(fp)
        imports = parse_imports(content)
        
        for block in it_blocks:
            body = extract_block_body(content, block['start'], block['end'])
            if not body:
                continue
            
            # 检测异步操作（直接或封装函数）
            direct_async = self._has_async_operation(body)
            wrapper_async = False
            
            if not direct_async:
                # 检测同文件封装函数
                called_funcs = extract_called_functions(body)
                for func_name in called_funcs:
                    if func_name in ('expect', 'console', 'sleep', 'done'):
                        continue
                    # 使用缓存避免重复解析
                    if fdef_cache:
                        func_body = fdef_cache.get(fp, func_name)
                    else:
                        func_body = find_function_definition(content, func_name)
                    if func_body and self._has_async_operation(func_body):
                        wrapper_async = True
                        break
            
            is_async_case = direct_async or wrapper_async
            if not is_async_case:
                continue
            
            # 检查多行声明文本（最多取3行，处理跨行it声明）
            decl_lines = content.split('\n')[max(0, block['start'] - 1):block['start'] + 2]
            decl_text = '\n'.join(decl_lines)
            
            is_async = bool(re.search(r'\basync\b', decl_text))
            has_done_param = bool(re.search(r'\bdone\s*:', decl_text)) or bool(re.search(r'\bdone\s*(?:\(\s*\)|:|\b)', decl_text))
            has_done_call = bool(re.search(r'\bdone\s*\(\s*\)', body))
            done_passed_as_arg = bool(re.search(r'\b\w+\s*\(\s*[^)]*\bdone\b', body))
            
            async_source = '用例体内直接包含异步操作' if direct_async else '用例调用了封装函数包含异步操作'
            
            # 检测问题
            if is_async and not has_done_param:
                # async用例缺少done参数，需检查是否正确await
                unawaited = self._find_unawaited_async(body)
                if unawaited:
                    line_offset, snippet = unawaited
                    issues.append({
                        'rule': 'R201',
                        'category': '异步/时序安全',
                        'type': '异步用例缺少done回调或未await',
                        'severity': 'Critical',
                        'file': rel_path,
                        'line': block['start'] + line_offset,
                        'testcase': block['name'],
                        'snippet': snippet,
                        'suggestion': f'异步操作未使用await等待。{async_source}。',
                        'subsystem': get_subsystem(rel_path),
                    })
            
            elif is_async and has_done_param:
                # async用例有done参数，需要检测未await的异步操作（包括.then()和setTimeout）
                # 但如果.then()回调中已调用done()，则不报告（这种模式可以正常工作）
                unawaited = self._find_unawaited_async(body)
                if unawaited:
                    line_offset, snippet = unawaited
                    # 检查.then()回调中是否有done()调用
                    if '.then' in snippet or '.then(' in body:
                        has_done_in_chain = self._check_done_in_promise_chain(body, line_offset)
                        if has_done_in_chain:
                            # 回调中有done()，跳过（改为Warning级别）
                            continue
                    # setTimeout的情况：检查是否有done()在回调中
                    if 'setTimeout' in snippet or 'setInterval' in snippet:
                        # setTimeout/setInterval通常不会在回调中调用done()
                        # 需要特殊处理，保留Critical报告
                        pass
                    
                    issues.append({
                        'rule': 'R201',
                        'category': '异步/时序安全',
                        'type': '异步用例缺少done回调或未await',
                        'severity': 'Critical',
                        'file': rel_path,
                        'line': block['start'] + line_offset,
                        'testcase': block['name'],
                        'snippet': snippet,
                        'suggestion': f'async+done混用模式下异步操作仍需await或确保done在所有回调分支中调用。{async_source}。',
                        'subsystem': get_subsystem(rel_path),
                    })
            
            elif has_done_param and has_done_call:
                # done参数已调用，需检查catch分支
                if not self._all_paths_have_done(body):
                    issues.append({
                        'rule': 'R201',
                        'category': '异步/时序安全',
                        'type': '异步用例缺少done回调或未await',
                        'severity': 'Critical',
                        'file': rel_path,
                        'line': block['start'],
                        'testcase': block['name'],
                        'snippet': decl_text.strip()[:120],
                        'suggestion': f'done()未在所有执行路径上调用（如catch分支）。{async_source}。',
                        'subsystem': get_subsystem(rel_path),
                    })
            
            elif not is_async and not has_done_param:
                # 既非async也无done参数，但包含异步操作
                issues.append({
                    'rule': 'R201',
                    'category': '异步/时序安全',
                    'type': '异步用例缺少done回调或未await',
                    'severity': 'Critical',
                    'file': rel_path,
                    'line': block['start'],
                    'testcase': block['name'],
                    'snippet': decl_text.strip()[:120],
                    'suggestion': f'用例包含异步操作但缺少done回调且未使用async/await。{async_source}。',
                    'subsystem': get_subsystem(rel_path),
                })
            
            elif has_done_param and not has_done_call and not done_passed_as_arg:
                # done参数声明但未调用
                issues.append({
                    'rule': 'R201',
                    'category': '异步/时序安全',
                    'type': '异步用例缺少done回调或未await',
                    'severity': 'Critical',
                    'file': rel_path,
                    'line': block['start'],
                    'testcase': block['name'],
                    'snippet': decl_text.strip()[:120],
                    'suggestion': f'用例声明了done参数但未调用done()，将导致用例超时。{async_source}。',
                    'subsystem': get_subsystem(rel_path),
                })
        
        return issues
    
    def _has_async_operation(self, body: str) -> bool:
        """检测是否包含异步操作"""
        return any(re.search(p, body) for p in self.ASYNC_INDICATORS)
    
    def _find_unawaited_async(self, body: str) -> Tuple[int, str]:
        """查找未await的异步操作"""
        lines = body.split('\n')
        for i, line in enumerate(lines):
            stripped = line.strip()
            if re.match(r'await\s+', stripped):
                continue
            if re.search(r'\.\s*then\s*\(', stripped):
                return i, stripped[:120]
            if re.match(r'(?:setTimeout|setInterval)\s*\(', stripped):
                return i, stripped[:120]
        return None
    
    def _find_unawaited_promise_chain(self, body: str) -> Tuple[int, str]:
        """查找未await的.then()链式调用（仅用于混用模式检测）"""
        lines = body.split('\n')
        for i, line in enumerate(lines):
            stripped = line.strip()
            if re.match(r'await\s+', stripped):
                continue
            # 只检测.then()链式调用，不检测setTimeout（混用模式下合法）
            if re.search(r'\.\s*then\s*\(', stripped):
                return i, stripped[:120]
        return None
    
    def _all_paths_have_done(self, body: str) -> bool:
        """检查done是否在所有执行路径上调用"""
        has_try_catch = bool(re.search(r'\btry\s*\{', body))
        if not has_try_catch:
            return True
        
        catch_matches = list(re.finditer(r'\}\s*catch\s*(?:\([^)]*\))?\s*\{', body))
        if not catch_matches:
            return True
        
        # 检查每个catch块是否调用done
        for cm in catch_matches:
            pos = cm.start()
            brace_idx = body[pos:].index('{')
            block_end = find_matching_brace(body, pos + brace_idx)
            block_content = body[pos:block_end + 1] if block_end > 0 else body[pos:pos + 200]
            if not re.search(r'\bdone\s*\(\s*\)', block_content):
                # catch块缺少done，检查是否有后续done
                last_block_end = block_end if block_end > 0 else pos + 200
                after_catch = body[last_block_end + 1:]
                if not re.search(r'\bdone\s*\(\s*\)', after_catch):
                    return False
        
        return True
    
    def _check_done_in_promise_chain(self, body: str, start_line_offset: int) -> bool:
        """检查.then()链中是否有done()调用"""
        lines = body.split('\n')
        if start_line_offset >= len(lines):
            return False
        
        # 从.then()行开始，向后查找50行范围内的done()调用
        search_range = 50
        combined_text = '\n'.join(lines[start_line_offset:start_line_offset + search_range])
        
        # 检查是否有done()调用
        if re.search(r'\bdone\s*\(\s*\)', combined_text):
            return True
        
        return False
    
    def _check_sta_async_executor(self, content: str, rel_path: str) -> List[Dict]:
        """Sta模式额外检测：async executor"""
        issues = []
        for i, line in enumerate(content.split('\n'), 1):
            if re.search(r'new\s+Promise\s*\(\s*async\b', line):
                issues.append({
                    'rule': 'R201',
                    'category': '异步/时序安全',
                    'type': 'Promise executor声明为async',
                    'severity': 'Critical',
                    'file': rel_path,
                    'line': i,
                    'testcase': '-',
                    'snippet': line.strip()[:120],
                    'suggestion': 'Promise executor不应声明为async',
                    'subsystem': get_subsystem(rel_path),
                })
        return issues


# ============================================================================
# R202: 异步错误处理缺失
# ============================================================================

_R202_SYSTEM_API_PATTERNS = [
    r'\bawait\s+(?:delegator|abilityDelegator)\.',
    r'\bawait\s+\w+\.\w+(?:Async|Promise)\s*\(',
    r'\bawait\s+\w+\.(?:get|set|put|delete|query|execute|create|open|close|start|stop|release|read|write|register|unregister|connect|disconnect|send|receive|enable|disable|subscribe|unsubscribe|on|off)\w*\s*\(',
]

_R202_PATTERN_DESC = {
    'await_no_try_catch': 'await调用未包裹try-catch',
    'then_no_catch': '.then()链缺少.catch()',
    'ignored_error_callback': 'error回调参数未检查',
}

class R202Scanner:
    base_dir = ''
    """异步回调/Promise未正确处理错误"""
    
    def scan_file(self, fp: str, content: str, fcache: FileContentCache, bc: BlockCache,
                  sta_projects: Set[str] = None, fdef_cache=None) -> List[Dict]:
        """检测异步错误处理"""
        issues = []
        rel_path = os.path.relpath(fp, self.base_dir)
        
        # 跳过大文件的封装函数追踪
        _skip_wrappers = len(content) > MAX_WRAPPER_FILE_SIZE
        
        if sta_projects and is_in_sta_project(fp, sta_projects):
            issues.extend(self._check_sta_reject_non_error(content, rel_path))
        
        it_blocks = bc.get_it_blocks(fp)
        imports = parse_imports(content)
        
        for block in it_blocks:
            body = extract_block_body(content, block['start'], block['end'])
            if not body:
                continue
            
            direct_issues = self._check_r202_patterns(body)
            for di in direct_issues:
                issues.append({
                    'rule': 'R202',
                    'category': '异步/时序安全',
                    'type': '异步回调/Promise未正确处理错误',
                    'severity': 'Critical',
                    'file': rel_path,
                    'line': block['start'] + di['line'] - 1,
                    'testcase': block['name'],
                    'snippet': di['snippet'],
                    'suggestion': f'{_R202_PATTERN_DESC[di["pattern"]]}。建议添加错误处理（try-catch/.catch()/error检查）。',
                    'subsystem': get_subsystem(rel_path),
                })
            
            if not direct_issues and not _skip_wrappers and fdef_cache:
                called_funcs = extract_called_functions(body)
                body_lines = body.split('\n')
                for func_name in called_funcs:
                    if func_name in ('expect', 'assertEqual', 'assertTrue', 'console', 'sleep'):
                        continue
                    func_body = fdef_cache.get(fp, func_name)
                    if func_body:
                        call_line_in_body = None
                        for li, bl in enumerate(body_lines):
                            if re.search(r'(?:await\s+)?' + re.escape(func_name) + r'\s*\(', bl):
                                call_line_in_body = li
                                break
                        if call_line_in_body is not None and not self._is_inside_try_block(body_lines, call_line_in_body):
                            wrapper_issues = self._check_r202_patterns(func_body)
                            if wrapper_issues:
                                first_wrapper = wrapper_issues[0]
                                issues.append({
                                    'rule': 'R202',
                                    'category': '异步/时序安全',
                                    'type': '异步回调/Promise未正确处理错误',
                                    'severity': 'Critical',
                                    'file': rel_path,
                                    'line': block['start'],
                                    'testcase': block['name'],
                                    'snippet': first_wrapper['snippet'],
                                    'suggestion': f'用例调用的封装函数 {func_name}（同文件）内部存在错误处理缺失。建议在封装函数中添加错误处理，或在调用处添加try-catch。',
                                    'subsystem': get_subsystem(rel_path),
                                })
                                break
                
                if not direct_issues and not _skip_wrappers:
                    result = check_cross_file_wrapper(
                        called_funcs, imports, fp,
                        lambda body, file, name: self._check_r202_patterns(body),
                        max_depth=2
                    )
                    if result:
                        func_name, source_file, wrapper_issues = result
                        rel_src = os.path.relpath(source_file, self.base_dir) if self.base_dir else source_file
                        first_wrapper = wrapper_issues[0]
                        issues.append({
                            'rule': 'R202',
                            'category': '异步/时序安全',
                            'type': '异步回调/Promise未正确处理错误',
                            'severity': 'Critical',
                            'file': rel_path,
                            'line': block['start'],
                            'testcase': block['name'],
                            'snippet': first_wrapper['snippet'],
                            'suggestion': f'用例调用的跨文件函数 {func_name}（{rel_src}）内部存在错误处理缺失。建议在封装函数中添加错误处理，或在调用处添加try-catch。',
                            'subsystem': get_subsystem(rel_path),
                        })
        
        return issues
    
    def _check_r202_patterns(self, body: str) -> List[Dict]:
        """检查异步错误处理模式"""
        issues = []
        lines = body.split('\n')
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            if re.search(r'assertPromiseIsRejected', stripped):
                continue
            
            if re.match(r'await\s+', stripped) and not re.match(r'await\s+sleep\s*\(', stripped):
                if not self._is_inside_try_block(lines, i):
                    if any(re.search(p, stripped) for p in _R202_SYSTEM_API_PATTERNS):
                        issues.append({
                            'pattern': 'await_no_try_catch',
                            'line': i + 1,
                            'snippet': stripped[:100],
                        })
            
            if re.search(r'\.\s*then\s*\(', stripped):
                has_catch = self._find_chain_catch(stripped, stripped.index('.then'))
                if not has_catch:
                    remaining_text = '\n'.join(lines[i + 1:i + 30])
                    combined = stripped + '\n' + remaining_text
                    then_pos_in_combined = combined.index('.then')
                    has_catch = self._find_chain_catch(combined, then_pos_in_combined)
                if not has_catch:
                    if not self._is_inside_try_block(lines, i):
                        issues.append({
                            'pattern': 'then_no_catch',
                            'line': i + 1,
                            'snippet': stripped[:100],
                        })
            
            err_cb = re.search(r'\(\s*(err(?:or)?)\s*\)\s*=>\s*\{([^}]*)\}', stripped)
            if err_cb:
                param, cb_body = err_cb.group(1), err_cb.group(2)
                if param not in cb_body and param != '_':
                    issues.append({
                        'pattern': 'ignored_error_callback',
                        'line': i + 1,
                        'snippet': stripped[:100],
                    })
        
        # 去重：同一行只保留一个问题
        line_issues = {}
        for issue in issues:
            line = issue['line']
            if line not in line_issues:
                line_issues[line] = issue
        
        return list(line_issues.values())
    
    def _is_inside_try_block(self, lines: List[str], line_idx: int) -> bool:
        """检查是否在try块内"""
        try_starts = []
        try_ends = []
        for i, line in enumerate(lines):
            s = line.strip()
            if re.match(r'try\s*\{', s):
                try_starts.append(i)
            elif re.match(r'\}\s*catch', s):
                try_ends.append(i)
            elif re.match(r'\}\s*finally', s):
                try_ends.append(i)
        for ts in reversed(try_starts):
            if ts >= line_idx:
                continue
            matching_te = None
            for te in try_ends:
                if te > ts:
                    matching_te = te
                    break
            if matching_te is not None and matching_te >= line_idx:
                return True
        return False
    
    def _find_chain_catch(self, text: str, start_pos: int) -> bool:
        """查找Promise链中的catch"""
        depth = 0
        i = start_pos
        while i < len(text):
            c = text[i]
            if c in ('"', "'", '`'):
                quote = c
                i += 1
                while i < len(text) and text[i] != quote:
                    if text[i] == '\\':
                        i += 1
                    i += 1
                i += 1
                continue
            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
                if depth < 0:
                    break
            elif depth == 0:
                if c == ';':
                    break
                if text[i:i + 7] == '.catch(' or text[i:i + 7] == '.catch (':
                    return True
                if c == '.' and (i + 1 >= len(text) or not text[i + 1].isalpha()):
                    break
                if c not in ('.', '\n', '\r', ' ', '\t') and not c.isalpha() and not c.isdigit() and c != '_':
                    break
            i += 1
        return False
    
    def _check_sta_reject_non_error(self, content: str, rel_path: str) -> List[Dict]:
        """Sta模式检测reject参数类型"""
        issues = []
        for i, line in enumerate(content.split('\n'), 1):
            stripped = line.strip()
            if stripped.startswith('//') or stripped.startswith('*'):
                continue
            m = re.search(r'\breject\s*\(\s*([^)]+)\s*\)', stripped)
            if not m:
                continue
            arg = m.group(1).strip()
            if not arg:
                continue
            if arg in ('undefined', 'null', 'void 0'):
                continue
            if re.match(r'new\s+Error\b', arg):
                continue
            if re.match(r'Error\b', arg):
                continue
            if re.match(r'err(?:or)?$', arg) or re.match(r'e$', arg):
                continue
            issues.append({
                'rule': 'R202',
                'category': '异步/时序安全',
                'type': '异步回调/Promise未正确处理错误',
                'severity': 'Critical',
                'file': rel_path,
                'line': i,
                'testcase': '-',
                'snippet': stripped[:120],
                'suggestion': f'reject()应传入Error实例，当前传入的是"{arg}"。建议改为 reject(new Error("..."))。',
                'subsystem': get_subsystem(rel_path),
            })
        return issues


# ============================================================================
# R204: 资源创建后未释放
# ============================================================================

class R204Scanner:
    base_dir = ''
    """资源创建未释放检测（采用v1.1完整逻辑）"""
    
    CREATE_PATTERNS = [
        (re.compile(r'(\w+)\.on\s*\(["\']([^"\']+)["\']'), 'event_listener', 'obj', True),
        (re.compile(r'(\w+)\.addEventListener\s*\('), 'event_listener', 'obj', False),
        (re.compile(r'(?:rdb|relationalStore)\.getRdbStore\s*\('), 'database', 'global', False),
        (re.compile(r'(?:kv|distributedKV)\.getKVStore\s*\('), 'database', 'global', False),
        (re.compile(r'new\s+MockKit\s*\('), 'mock_object', 'global', False),
        (re.compile(r'new\s+PerfTest\s*\('), 'perftest', 'global', False),
        (re.compile(r'(\w+)\.subscribe\s*\('), 'subscription', 'obj', False),
        (re.compile(r'(\w+)\.register\s*\('), 'subscription', 'obj', False),
    ]
    
    RELEASE_PATTERNS = [
        (re.compile(r'(\w+)\.off\s*\(["\']([^"\']+)["\']'), 'event_listener', 'obj', True),
        (re.compile(r'(\w+)\.removeEventListener\s*\('), 'event_listener', 'obj', False),
        (re.compile(r'(\w+)\.close\s*\('), 'database', 'obj', False),
        (re.compile(r'rdb\.deleteRdbStore\s*\('), 'database', 'global', False),
        (re.compile(r'mocker\.clear\s*\('), 'mock_object', 'global', False),
        (re.compile(r'mocker\.clearAll\s*\('), 'mock_object', 'global', False),
        (re.compile(r'PerfTest\.destroy\s*\('), 'perftest', 'global', False),
        (re.compile(r'(\w+)\.destroy\s*\('), 'perftest', 'obj', False),
        (re.compile(r'(\w+)\.unsubscribe\s*\('), 'subscription', 'obj', False),
        (re.compile(r'(\w+)\.unregister\s*\('), 'subscription', 'obj', False),
    ]
    
    def scan_file(self, fp: str, content: str, fcache: FileContentCache, bc: BlockCache) -> List[Dict]:
        """检测资源创建未释放（包含beforeAll/afterAll配对检测）"""
        issues = []
        rel_path = os.path.relpath(fp, self.base_dir)
        
        describe_blocks = bc.get_describe_blocks(fp)
        
        for desc in describe_blocks:
            desc_body = extract_block_body(content, desc['start'], desc['end'])
            
            before_all = extract_hook_body(desc_body, 'beforeAll')
            after_all = extract_hook_body(desc_body, 'afterAll')
            
            # 定义aa_released（无论before_all是否存在）
            aa_released = self._find_releases(after_all) if after_all else []
            
            # beforeAll创建的资源必须在afterAll中释放
            if before_all:
                ba_created = self._find_creations(before_all)
                
                if ba_created and not after_all:
                    hook_line = find_hook_line(desc_body, 'beforeAll')
                    for res in ba_created:
                        issues.append({
                            'rule': 'R204',
                            'category': '资源管理',
                            'type': '资源创建后未释放',
                            'severity': 'Critical',
                            'file': rel_path,
                            'line': hook_line,
                            'testcase': '-',
                            'snippet': res['snippet'],
                            'suggestion': f"beforeAll中创建了{res['type']}资源，但缺少afterAll来释放",
                            'subsystem': get_subsystem(rel_path),
                        })
                elif ba_created:
                    hook_line = find_hook_line(desc_body, 'beforeAll')
                    for res in ba_created:
                        if not self._has_matching_release(res, aa_released):
                            issues.append({
                                'rule': 'R204',
                                'category': '资源管理',
                                'type': '资源创建后未释放',
                                'severity': 'Critical',
                                'file': rel_path,
                                'line': hook_line,
                                'testcase': '-',
                                'snippet': res['snippet'],
                                'suggestion': f"beforeAll创建了{res['type']}，但afterAll中未找到对应释放",
                                'subsystem': get_subsystem(rel_path),
                            })
            
            it_blocks = [b for b in bc.get_it_blocks(fp)
                        if b['start'] >= desc['start'] and b['end'] <= desc['end']]
            
            for it_block in it_blocks:
                it_body = extract_block_body(content, it_block['start'], it_block['end'])
                created = self._find_creations(it_body)
                released = self._find_releases(it_body)
                
                # 用例创建的资源必须在用例或afterAll中释放
                all_released = released + aa_released
                
                for res in created:
                    if not self._has_matching_release(res, all_released):
                        issues.append({
                            'rule': 'R204',
                            'category': '资源管理',
                            'type': '资源创建后未释放',
                            'severity': 'Critical',
                            'file': rel_path,
                            'line': it_block['start'],
                            'testcase': it_block['name'],
                            'snippet': res['snippet'],
                            'suggestion': f'用例创建了{res["type"]}，需在结束前释放',
                            'subsystem': get_subsystem(rel_path),
                        })
        
        return issues
    
    def _find_creations(self, body: str) -> List[Dict]:
        """查找资源创建（排除once自动释放）"""
        created = []
        for pat, res_type, kind, has_event in self.CREATE_PATTERNS:
            for m in pat.finditer(body):
                # 排除once()事件监听器（会自动释放）
                if res_type == 'event_listener' and re.search(r'\.once\s*\(', m.group(0)):
                    continue
                
                entry = {
                    'type': res_type,
                    'object': '',
                    'event': '',
                    'snippet': m.group(0)[:80],
                }
                
                if kind == 'obj' and m.lastindex and m.lastindex >= 1:
                    entry['object'] = m.group(1)
                if has_event and m.lastindex and m.lastindex >= 2:
                    entry['event'] = m.group(2)
                
                created.append(entry)
        
        return created
    
    def _find_releases(self, body: str) -> List[Dict]:
        """查找资源释放"""
        released = []
        for pat, res_type, kind, has_event in self.RELEASE_PATTERNS:
            for m in pat.finditer(body):
                entry = {
                    'type': res_type,
                    'object': '',
                    'event': '',
                }
                
                if kind == 'obj' and m.lastindex and m.lastindex >= 1:
                    entry['object'] = m.group(1)
                if has_event and m.lastindex and m.lastindex >= 2:
                    entry['event'] = m.group(2)
                
                released.append(entry)
        
        return released
    
    def _has_matching_release(self, creation: Dict, releases: List[Dict]) -> bool:
        """检查是否有匹配的释放（支持跨类型匹配：对象相同即可）"""
        obj = creation.get('object', '')
        evt = creation.get('event', '')
        
        for rel in releases:
            rob = rel.get('object', '')
            rev = rel.get('event', '')
            
            # 对象匹配（放宽条件：跨类型匹配）
            # 如 netConn.on('xxx') 可通过 netConn.unregister() 释放
            if obj and rob and obj == rob:
                # 如果有事件名匹配要求
                if evt and rev:
                    if evt == rev:
                        return True
                # 没有事件名或释放操作没有事件名，对象匹配即可
                else:
                    return True
            
            # 全局资源匹配
            if not obj and not evt:
                return True
        
        return False


# ============================================================================
# R205: 钩子配对缺失
# ============================================================================

class R205Scanner:
    base_dir = ''
    """beforeAll缺少afterAll检测"""
    
    def scan_file(self, fp: str, content: str, fcache: FileContentCache, bc: BlockCache) -> List[Dict]:
        """检测钩子配对"""
        issues = []
        rel_path = os.path.relpath(fp, self.base_dir)
        
        describe_blocks = bc.get_describe_blocks(fp)
        
        for desc in describe_blocks:
            desc_body = extract_block_body(content, desc['start'], desc['end'])
            
            has_before_all = bool(re.search(r'\bbeforeAll\s*\(', desc_body))
            has_after_all = bool(re.search(r'\bafterAll\s*\(', desc_body))
            has_before_each = bool(re.search(r'\bbeforeEach\s*\(', desc_body))
            has_after_each = bool(re.search(r'\bafterEach\s*\(', desc_body))
            
            if has_before_all and not has_after_all:
                hook_line = find_hook_line(desc_body, 'beforeAll')
                abs_line = desc['start'] + hook_line - 1 if hook_line else desc['start']
                issues.append({
                    'rule': 'R205',
                    'category': '资源管理',
                    'type': 'beforeAll存在但缺少配对的afterAll',
                    'severity': 'Critical',
                    'file': rel_path,
                    'line': abs_line,
                    'testcase': '-',
                    'snippet': 'beforeAll',
                    'suggestion': 'describe块中定义了beforeAll但缺少配对的afterAll。beforeAll中分配的资源需要在afterAll中释放。',
                    'subsystem': get_subsystem(rel_path),
                })
            
            if has_before_each and not has_after_each:
                hook_line = find_hook_line(desc_body, 'beforeEach')
                abs_line = desc['start'] + hook_line - 1 if hook_line else desc['start']
                issues.append({
                    'rule': 'R205',
                    'category': '资源管理',
                    'type': 'beforeEach存在但缺少配对的afterEach',
                    'severity': 'Critical',
                    'file': rel_path,
                    'line': abs_line,
                    'testcase': '-',
                    'snippet': 'beforeEach',
                    'suggestion': 'describe块中定义了beforeEach但缺少配对的afterEach。beforeEach中设置的测试状态需要在afterEach中重置。',
                    'subsystem': get_subsystem(rel_path),
                })
        
        return issues


# ============================================================================
# R206: 用例间隐式依赖（全局状态共享）
# ============================================================================

class R206Scanner:
    """用例间隐式依赖检测（Sta/Dyn差异化检测）"""
    
    base_dir = ''
    
    MODIFY_PATTERNS = [
        (re.compile(r'(?<![.\w])(\w+)\s*=\s*[^=]'), 'assign'),
        (re.compile(r'(\w+)\s*\+='), 'plus_assign'),
        (re.compile(r'(\w+)\.push\s*\('), 'push'),
        (re.compile(r'(\w+)\.set\s*\('), 'set'),
    ]
    
    ASSIGN_KW = re.compile(r'^(?:let|const|var|function|class|return|if|else|for|while|switch|case|break|continue|new|typeof|import|export|default)\b')
    
    EAWORKER_SHARED_RE = re.compile(r'\b(?:SharedArrayBuffer|Atomics|SharedMap|SharedSet)\b')
    EAWORKER_POST_RE = re.compile(r'\b(?:postMessage|onmessage|transferList)\b')
    
    GLOBALTHIS_RE = re.compile(r'\bglobalThis\s*\.\s*\w+')
    
    def scan_file(self, fp: str, content: str, fcache: FileContentCache, bc: BlockCache,
                  sta_projects: Set[str] = None, fdef_cache=None) -> List[Dict]:
        """检测全局状态共享（Sta工程检测EAWorker，Dyn工程检测describe块级变量）"""
        issues = []
        rel_path = os.path.relpath(fp, self.base_dir)
        
        it_blocks = bc.get_it_blocks(fp)
        describe_blocks = bc.get_describe_blocks(fp)
        
        # Sta工程检测EAWorker共享对象
        if sta_projects and is_in_sta_project(fp, sta_projects):
            issues.extend(self._check_eaworker_shared(content, rel_path, describe_blocks))
        
        # 检测globalThis全局状态共享
        globalthis_issues = self._check_globalthis_usage(content, rel_path, it_blocks)
        issues.extend(globalthis_issues)
        
        # Dyn工程检测describe块级共享变量被多用例修改
        file_shared_vars = self._find_file_level_variables(content)
        
        for desc in describe_blocks:
            desc_body = extract_block_body(content, desc['start'], desc['end'])
            if not desc_body:
                continue
            
            desc_shared_vars = self._find_shared_variable(desc_body)
            shared_vars = desc_shared_vars | file_shared_vars
            if not shared_vars:
                continue
            
            has_before_each = bool(re.search(r'\bbeforeEach\s*\(', desc_body))
            
            it_blocks_in_desc = [b for b in it_blocks 
                                 if b['start'] >= desc['start'] and b['end'] <= desc['end']]
            
            if not it_blocks_in_desc:
                continue
            
            var_mutators = {}
            for it_block in it_blocks_in_desc:
                it_body = extract_block_body(content, it_block['start'], it_block['end'])
                mutations = self._find_mutations(it_body, shared_vars)
                for m in mutations:
                    var_mutators.setdefault(m['var'], []).append(it_block['name'])
            
            problematic_vars = [v for v, mutators in var_mutators.items() if len(mutators) >= 2]
            
            if problematic_vars and not has_before_each:
                first_mutations = list(var_mutators.values())[0]
                issues.append({
                    'rule': 'R206',
                    'category': '测试设计',
                    'type': '用例间存在隐式依赖（全局状态共享）',
                    'severity': 'Warning',
                    'file': rel_path,
                    'line': desc['start'],
                    'testcase': '-',
                    'snippet': f'共享变量 {", ".join(problematic_vars[:3])} 被多个用例修改',
                    'suggestion': f"共享变量 {', '.join(sorted(problematic_vars))} 被多个用例修改，但缺少beforeEach重置。",
                    'subsystem': get_subsystem(rel_path),
                })
        
        return issues
    
    def _check_globalthis_usage(self, content: str, rel_path: str, it_blocks: List[Dict]) -> List[Dict]:
        """检测globalThis全局状态共享"""
        issues = []
        lines = content.split('\n')
        
        globalthis_testcases = {}
        for i, line in enumerate(lines, 1):
            if self.GLOBALTHIS_RE.search(line):
                testcase = find_testcase_for_line(it_blocks, i)
                if testcase and testcase != '-':
                    globalthis_testcases.setdefault(testcase, []).append(i)
        
        if len(globalthis_testcases) >= 1:
            first_tc = list(globalthis_testcases.keys())[0]
            first_line = globalthis_testcases[first_tc][0]
            snippet = lines[first_line - 1].strip()[:120] if first_line <= len(lines) else ''
            issues.append({
                'rule': 'R206',
                'category': '测试设计',
                'type': '用例间存在隐式依赖（globalThis共享）',
                'severity': 'Warning',
                'file': rel_path,
                'line': first_line,
                'testcase': first_tc,
                'snippet': snippet,
                'suggestion': '使用globalThis会导致用例间隐式依赖，建议使用局部变量或beforeEach重置。',
                'subsystem': get_subsystem(rel_path),
            })
        
        return issues
    
    def _count_braces_outside_strings(self, line: str) -> int:
        """计算行中花括号数量（排除字符串内的）"""
        in_s = in_d = in_bt = False
        opens = closes = 0
        i = 0
        while i < len(line):
            c = line[i]
            if c == '\\' and (in_s or in_d or in_bt):
                i += 2
                continue
            if c == '`' and not in_s and not in_d:
                in_bt = not in_bt
            elif c == "'" and not in_d and not in_bt:
                in_s = not in_s
            elif c == '"' and not in_s and not in_bt:
                in_d = not in_d
            elif not in_s and not in_d and not in_bt:
                if c == '{':
                    opens += 1
                elif c == '}':
                    closes += 1
            i += 1
        return opens - closes
    
    def _find_shared_variable(self, desc_body: str) -> Set[str]:
        """查找describe块级的共享变量（let/var声明）- 使用花括号计数排除函数内部变量"""
        shared_vars = set()
        lines = desc_body.split('\n')
        if not lines:
            return shared_vars
        
        in_block = 0
        block_keywords = re.compile(r'\b(?:it|beforeAll|beforeEach|afterAll|afterEach|describe|function)\s*\(')
        initial_depth_set = False
        
        for line in lines:
            stripped = line.strip()
            brace_delta = self._count_braces_outside_strings(stripped)
            
            if block_keywords.search(stripped):
                in_block += brace_delta
            else:
                in_block += brace_delta
            
            if not initial_depth_set and in_block > 0:
                in_block = 0
                initial_depth_set = True
            
            if in_block <= 0:
                in_block = 0
                m = re.match(r'(?:let|var)\s+(\w+)', stripped)
                if m:
                    shared_vars.add(m.group(1))
        
        return shared_vars
    
    def _find_file_level_variables(self, content: str) -> Set[str]:
        """查找文件级别的共享变量（describe外部声明）"""
        shared_vars = set()
        lines = content.split('\n')
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
                continue
            if re.match(r'^\s*import\b', stripped):
                continue
            if re.match(r'^\s*export\b', stripped):
                continue
            
            m = re.match(r'(?:let|var)\s+(\w+)', stripped)
            if m:
                shared_vars.add(m.group(1))
            
            if re.match(r'^\s*describe\s*\(', stripped):
                break
        
        return shared_vars
    
    def _find_mutations(self, body: str, shared_vars: Set[str]) -> List[Dict]:
        """查找对共享变量的修改"""
        mutations = []
        
        for pattern, _ in self.MODIFY_PATTERNS:
            for match in pattern.finditer(body):
                var_name = match.group(1)
                if var_name in shared_vars and not self.ASSIGN_KW.match(var_name):
                    before = body[max(0, match.start() - 1)]
                    if before == '.':
                        continue
                    
                    mutations.append({
                        'var': var_name,
                        'snippet': match.group(0)[:80],
                    })
        
        return mutations
    
    def _check_eaworker_shared(self, content: str, rel_path: str, describe_blocks: List[Dict]) -> List[Dict]:
        """检测EAWorker共享对象"""
        issues = []
        
        # 检测SharedArrayBuffer等共享类型
        shared_types = set()
        for m in self.EAWORKER_SHARED_RE.finditer(content):
            shared_types.add(m.group(0))
        
        # 检测共享变量声明
        shared_var_pattern = re.compile(
            r'(?:let|var|const)\s+(\w+)\s*=\s*new\s+'
            r'(?:SharedArrayBuffer|SharedMap|SharedSet|Uint8Array|Int32Array|ArrayBuffer)'
        )
        shared_vars = set()
        for m in shared_var_pattern.finditer(content):
            shared_vars.add(m.group(1))
        
        if not shared_vars:
            return issues
        
        # 检测describe块内对共享变量的修改（且没有beforeEach/beforeAll）
        for desc in describe_blocks:
            desc_body = extract_block_body(content, desc['start'], desc['end'])
            if not desc_body:
                continue
            
            has_before_each = bool(re.search(r'\bbeforeEach\s*\(', desc_body))
            has_before_all = bool(re.search(r'\bbeforeAll\s*\(', desc_body))
            
            # 查找在describe块内对共享变量的修改
            # 注意：即使有beforeEach/beforeAll也要检测，因为可能没有正确重置所有共享变量
            mutations_in_desc = []
            lines = desc_body.split('\n')
            for idx, line in enumerate(lines):
                stripped = line.strip()
                if stripped.startswith('//') or stripped.startswith('*'):
                    continue
                
                # 跳过beforeEach/beforeAll那一行（不检测钩子函数内部的修改）
                if re.search(r'\b(?:beforeEach|beforeAll|afterEach|afterAll)\s*\(', stripped):
                    continue
                
                for var in shared_vars:
                    for pattern, _ in self.MODIFY_PATTERNS:
                        pm = pattern.search(stripped)
                        if pm and pm.group(1) == var and not self.ASSIGN_KW.match(var):
                            before = stripped[max(0, pm.start() - 1)]
                            if before != '.':
                                # 计算绝对行号（describe起始行 + 块内偏移）
                                abs_line = desc['start'] + idx
                                mutations_in_desc.append({
                                    'var': var,
                                    'line': abs_line,
                                    'snippet': stripped[:120],
                                })
                                break
            
            # 如果有修改，报告问题（即使有beforeEach也要报告，因为beforeEach可能没正确重置）
            if mutations_in_desc:
                var_names = sorted(set(m['var'] for m in mutations_in_desc))
                type_names = sorted(shared_types) if shared_types else ['Uint8Array', 'ArrayBuffer']
                first = mutations_in_desc[0]
                issues.append({
                    'rule': 'R206',
                    'category': '测试设计',
                    'type': '用例间存在隐式依赖（EAWorker共享对象）',
                    'severity': 'Warning',
                    'file': rel_path,
                    'line': first['line'],
                    'testcase': '-',
                    'snippet': first['snippet'],
                    'suggestion': f"EAWorker共享对象 {', '.join(var_names)} (类型: {', '.join(type_names)}) 在EAWorker场景下被多个用例共享修改。ArkTS-Sta内存模型下共享对象变更会影响所有引用它的Worker。建议在beforeEach中重置共享对象状态，或将对象创建移到it()内部。",
                    'subsystem': get_subsystem(rel_path),
                })
        
        return issues


# ============================================================================
# R013: 注释的废弃代码
# ============================================================================

class R013Scanner:
    base_dir = ''
    """检测连续注释块中的废弃代码"""
    
    CODE_PATTERNS = [
        re.compile(r'\bfunction\b'),
        re.compile(r'\bvar\b'),
        re.compile(r'\blet\b'),
        re.compile(r'\bconst\b'),
        re.compile(r'\breturn\b'),
        re.compile(r'\bif\s*\('),
        re.compile(r'\bfor\s*\('),
        re.compile(r'\bwhile\s*\('),
        re.compile(r'\bswitch\s*\('),
        re.compile(r'\bcase\b'),
        re.compile(r'\bbreak\b'),
        re.compile(r'\bclass\b'),
        re.compile(r'\bimport\b'),
        re.compile(r'\bexport\b'),
        re.compile(r'\basync\b'),
        re.compile(r'\bawait\b'),
        re.compile(r'\btry\b'),
        re.compile(r'\bcatch\b'),
        re.compile(r'\bthrow\b'),
        re.compile(r'\bnew\b'),
        re.compile(r'\bthis\b'),
        re.compile(r'\bexpect\b'),
        re.compile(r'\bit\s*\('),
        re.compile(r'\bdescribe\s*\('),
        re.compile(r'\{'),
        re.compile(r'\}'),
        re.compile(r';'),
        re.compile(r'\=\>'),
        re.compile(r'\.\w+\s*\('),
    ]
    
    COMPLETE_FUNC_PATTERNS = [
        re.compile(r'function\s+\w+\s*\([^)]*\)\s*\{'),
        re.compile(r'(?:async\s+)?\w+\s*=\s*(?:async\s+)?\([^)]*\)\s*(?:=>|\{)'),
        re.compile(r'it\s*\(\s*["\'][^"\']+["\']'),
        re.compile(r'describe\s*\(\s*["\'][^"\']+["\']'),
        re.compile(r'\bclass\s+\w+'),
        re.compile(r'\bnew\s+\w+'),
        re.compile(r'\bexpect\s*\('),
        re.compile(r'\btry\s*\{'),
        re.compile(r'\bif\s*\('),
        re.compile(r'\bfor\s*\('),
        re.compile(r'\bwhile\s*\('),
        re.compile(r'\bswitch\s*\('),
    ]
    
    TEMPLATE_COMMENT_PATTERNS = [
        re.compile(r'Presets an action'),
        re.compile(r'Presets a clear action'),
        re.compile(r'is\s+not\s+allowed\s+to\s+use\s+weakly\s+typed\b', re.IGNORECASE),
    ]
    
    def scan_file(self, fp: str, content: str, fcache: FileContentCache, bc: BlockCache) -> List[Dict]:
        """检测注释废弃代码"""
        issues = []
        rel_path = os.path.relpath(fp, self.base_dir)
        
        blocks = self._find_comment_blocks(content)
        
        for block in blocks:
            comment_text = self._extract_comment_text(block)
            
            if self._is_license_header(comment_text):
                continue
            
            if self._is_javadoc(comment_text):
                continue
            
            if not self._has_code_characteristics(comment_text):
                continue
            
            is_function = self._has_complete_function(comment_text)
            is_template = any(p.search(comment_text) for p in self.TEMPLATE_COMMENT_PATTERNS)
            
            if not is_function and not is_template and len(block) < 3:
                continue
            
            if is_template and not is_function and len(block) < 6:
                continue
            
            first_line = block[0]
            last_line = block[-1]
            line_num = first_line[0]
            end_line_num = last_line[0]
            snippet = first_line[1].strip()[:120]
            
            testcase = find_testcase_for_line(bc.get_it_blocks(fp), line_num)
            
            issues.append({
                'rule': 'R013',
                'category': '编码规范合规',
                'type': '注释的废弃代码',
                'severity': 'Warning',
                'file': rel_path,
                'line': line_num,
                'testcase': testcase,
                'snippet': snippet,
                'suggestion': f'第{line_num}-{end_line_num}行存在注释的废弃代码（共{len(block)}行）。建议直接删除，使用版本控制系统保留历史记录。',
                'subsystem': get_subsystem(rel_path),
            })
        
        return issues
    
    def _find_comment_blocks(self, content: str) -> List[List[Tuple[int, str]]]:
        """找出连续3行及以上的注释块"""
        lines = content.split('\n')
        blocks = []
        current_block = []
        in_multi_comment = False
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            if in_multi_comment:
                current_block.append((i, line))
                if '*/' in stripped:
                    in_multi_comment = False
                    if len(current_block) >= 3:
                        blocks.append(list(current_block))
                    current_block = []
                continue
            
            if stripped.startswith('/*'):
                in_multi_comment = True
                current_block.append((i, line))
                if '*/' in stripped:
                    in_multi_comment = False
                    if len(current_block) >= 3:
                        blocks.append(list(current_block))
                    current_block = []
                continue
            
            is_comment = (
                stripped.startswith('//') or
                stripped.startswith('*') and not stripped.startswith('*/')
            )
            
            if is_comment:
                current_block.append((i, line))
            else:
                if len(current_block) >= 3:
                    blocks.append(list(current_block))
                current_block = []
        
        if len(current_block) >= 3:
            blocks.append(list(current_block))
        
        return blocks
    
    def _extract_comment_text(self, block: List[Tuple[int, str]]) -> str:
        """提取注释块的文本内容"""
        texts = []
        for _, line in block:
            stripped = line.strip()
            if stripped.startswith('//'):
                texts.append(stripped[2:].strip())
            elif stripped.startswith('*') and not stripped.startswith('*/'):
                texts.append(stripped[1:].strip())
            elif stripped.startswith('/*'):
                texts.append(stripped[2:].strip())
            elif stripped.startswith('*/'):
                texts.append(stripped[2:].strip())
            else:
                texts.append(stripped)
        return '\n'.join(texts)
    
    def _has_complete_function(self, comment_text: str) -> bool:
        """检测是否包含完整函数定义或测试用例"""
        for pattern in self.COMPLETE_FUNC_PATTERNS:
            if pattern.search(comment_text):
                return True
        return False
    
    def _is_javadoc(self, comment_text: str) -> bool:
        """检测是否是javadoc格式注释"""
        javadoc_markers = [
            r'@tc\.name',
            r'@tc\.number',
            r'@tc\.desc',
            r'@tc\.size',
            r'@tc\.type',
            r'@tc\.level',
            r'@param',
            r'@return',
            r'@throws',
            r'@since',
            r'@deprecated',
        ]
        
        match_count = 0
        for marker in javadoc_markers:
            if re.search(marker, comment_text):
                match_count += 1
        
        return match_count >= 2
    
    def _has_code_characteristics(self, comment_text: str) -> bool:
        """判断注释文本是否包含代码特征"""
        pattern_count = 0
        for pattern in self.CODE_PATTERNS:
            if pattern.search(comment_text):
                pattern_count += 1
        return pattern_count >= 2
    
    def _is_license_header(self, comment_text: str) -> bool:
        """判断是否是版权声明"""
        license_indicators = [
            'Copyright',
            'Licensed under the Apache License',
            'http://www.apache.org/licenses/LICENSE-2.0',
            'Apache License',
            'Licensed under',
            'Huawei Device',
        ]
        
        for indicator in license_indicators:
            if indicator in comment_text:
                return True
        
        return False


# ============================================================================
# R002: 错误码断言必须是number类型
# ============================================================================

class R002Scanner:
    """错误码断言number类型检测"""
    
    base_dir = ''
    
    STRING_CODE_PATTERNS = [
        re.compile(r'expect\s*\(\s*\w+\.code\s*\)\s*\.\s*assertEqual\s*\(\s*["\'][0-9]+["\']'),
        re.compile(r'expect\s*\(\s*\w+\.code\s*===?\s*["\'][0-9]+["\']'),
        re.compile(r'expect\s*\(\s*\w+\.code\s*!==?\s*["\'][0-9]+["\']'),
        re.compile(r'if\s*\(\s*\w+\.code\s*===?\s*["\'][0-9]+["\']'),
        re.compile(r'if\s*\(\s*\w+\.code\s*!==?\s*["\'][0-9]+["\']'),
        re.compile(r'\w+\.code\s*===?\s*["\'][0-9]+["\']\s*\)\s*\.\s*assertTrue'),
        re.compile(r'\w+\.code\s*!==?\s*["\'][0-9]+["\']\s*\)\s*\.\s*assertTrue'),
    ]
    
    def scan_file(self, fp: str, content: str, fcache: FileContentCache, bc: BlockCache) -> List[Dict]:
        """检测error.code使用string字面量断言"""
        issues = []
        rel_path = os.path.relpath(fp, self.base_dir)
        
        if '.code' not in content:
            return issues
        
        it_blocks = bc.get_it_blocks(fp)
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('//') or stripped.startswith('*'):
                continue
            
            if '.code' not in line:
                continue
            
            for pattern in self.STRING_CODE_PATTERNS:
                m = pattern.search(line)
                if m:
                    testcase = find_testcase_for_line(it_blocks, i)
                    snippet = stripped[:120]
                    issues.append({
                        'rule': 'R002',
                        'category': '编码规范合规',
                        'type': '错误码断言必须是number类型',
                        'severity': 'Critical',
                        'file': rel_path,
                        'line': i,
                        'testcase': testcase,
                        'snippet': snippet,
                        'suggestion': 'error.code是number类型，断言时应使用数字而非字符串字面量',
                        'subsystem': get_subsystem(rel_path),
                    })
                    break
        
        return issues


# ============================================================================
# R021: hypium版本号>=1.0.26
# ============================================================================

class R021Scanner:
    """hypium版本号检测"""
    
    base_dir = ''
    
    def scan_file(self, fp: str, content: str, fcache: FileContentCache, bc: BlockCache) -> List[Dict]:
        """检测oh-package.json5中的hypium版本"""
        if os.path.basename(fp) != 'oh-package.json5':
            return []
        
        issues = []
        rel_path = os.path.relpath(fp, self.base_dir)
        
        hypium_version = self._extract_hypium_version(content)
        if hypium_version:
            if self._version_lt(hypium_version, '1.0.26'):
                issues.append({
                    'rule': 'R021',
                    'category': '编码规范合规',
                    'type': 'hypium版本号>=1.0.26',
                    'severity': 'Critical',
                    'file': rel_path,
                    'line': 1,
                    'testcase': '-',
                    'snippet': f'@ohos/hypium: {hypium_version}',
                    'suggestion': f'hypium版本{hypium_version}过低，需要>=1.0.26',
                    'subsystem': get_subsystem(rel_path),
                })
        
        return issues
    
    def _extract_hypium_version(self, content: str) -> Optional[str]:
        """提取hypium版本号"""
        try:
            m = re.search(r'@ohos/hypium["\']?\s*:\s*["\']([^"\']+)["\']', content)
            if m:
                return m.group(1).strip()
        except Exception:
            pass
        return None
    
    def _version_lt(self, v1: str, v2: str) -> bool:
        """比较版本号，v1 < v2 返回True"""
        try:
            parts1 = [int(x) for x in v1.split('.')]
            parts2 = [int(x) for x in v2.split('.')]
            for i in range(max(len(parts1), len(parts2))):
                p1 = parts1[i] if i < len(parts1) else 0
                p2 = parts2[i] if i < len(parts2) else 0
                if p1 < p2:
                    return True
                if p1 > p2:
                    return False
            return False
        except Exception:
            return False


# ============================================================================
# R203: 多异步接口并发调用无隔离
# ============================================================================

class R203Scanner:
    """多异步并发调用无隔离检测（采用v1.1精确逻辑）"""
    
    base_dir = ''
    
    EXCLUDED_OBJ_NAMES = {
        'console', 'expect', 'describe', 'it', 'beforeAll', 'beforeEach',
        'afterAll', 'afterEach', 'sleep', 'mocker', 'done',
        'hilog', 'HiLog', 'HiSysEvent', 'reporter', 'Report',
        'sinon', 'jest',
    }
    
    EXCLUDED_METHOD_PATTERNS = {
        'assertEqual', 'assertTrue', 'assertFalse', 'assertContain',
        'assertFail', 'assertNull', 'assertUndefined', 'assertInstanceOf',
        'assertClose', 'assertNaN', 'assertThrowError', 'assertDeepEquals',
        'assertLarger', 'assertLess',
        'log', 'info', 'error', 'warn', 'debug', 'trace',
        'on', 'off', 'emit',
        'toString', 'valueOf', 'hasOwnProperty',
        'push', 'pop', 'shift', 'unshift', 'splice', 'slice',
        'map', 'filter', 'reduce', 'forEach', 'find', 'findIndex',
        'keys', 'values', 'entries', 'assign',
        'stringify', 'parse',
        'replace', 'split', 'trim', 'toLowerCase', 'toUpperCase', 'substring',
        'startsWith', 'endsWith', 'includes', 'indexOf',
        'addEventListener', 'removeEventListener',
        'getAbsolutePath', 'getUri',
    }
    
    def scan_file(self, fp: str, content: str, fcache: FileContentCache, bc: BlockCache,
                  sta_projects: Set[str] = None) -> List[Dict]:
        """检测同一用例内多个异步调用共享状态且未序列化"""
        issues = []
        rel_path = os.path.relpath(fp, self.base_dir)
        
        it_blocks = bc.get_it_blocks(fp)
        
        for block in it_blocks:
            body = extract_block_body(content, block['start'], block['end'])
            if not body:
                continue
            
            decl_line = content.split('\n')[block['start'] - 1]
            is_async = bool(re.search(r'\bit\s*\([^)]*,\s*async\b', decl_line))
            
            if not is_async:
                continue
            
            if re.search(r'Promise\.all\s*\(', body):
                continue
            
            calls = self._find_async_calls(body)
            
            if len(calls) >= 2:
                shared = self._detect_shared_state(calls)
                for obj_name, obj_calls in shared.items():
                    is_safe, reason = self._check_serialization(obj_calls, body)
                    if not is_safe:
                        issues.append({
                            'rule': 'R203',
                            'category': '异步/时序安全',
                            'type': '多异步接口并发调用无隔离导致时序异常',
                            'severity': 'Critical',
                            'file': rel_path,
                            'line': obj_calls[0]['line'] + block['start'],
                            'testcase': block['name'],
                            'snippet': obj_calls[0]['raw'],
                            'suggestion': f"对象 '{obj_name}' 上的 {len(obj_calls)} 个异步调用存在并发风险。原因: {reason}。建议逐一await每个调用。",
                            'subsystem': get_subsystem(rel_path),
                        })
                        break
        
        return issues
    
    def _find_async_calls(self, body: str) -> List[Dict]:
        """查找await异步调用（排除callback函数定义内部的await）"""
        calls = []
        lines = body.split('\n')
        
        # 检测函数定义区域（箭头函数/function定义）
        # 注意：排除it()/beforeEach()等测试钩子的回调函数，这些回调是测试体本身，不是嵌套回调
        function_regions = []
        test_hook_patterns = [r'\bit\s*\(', r'\bbeforeEach\s*\(', r'\bbeforeAll\s*\(', 
                             r'\bafterEach\s*\(', r'\bafterAll\s*\(', r'\bdescribe\s*\(']
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            # 检测是否是测试钩子回调（如it('...', async () => {），不应被排除
            is_test_hook_callback = any(re.search(p, stripped) for p in test_hook_patterns)
            if is_test_hook_callback:
                continue
            
            # 检测箭头函数定义开始：let/const X = async (...) => { 或独立 async (...) => {
            if re.search(r'(?:let|const)\s+\w+\s*=\s*async\s*\([^)]*\)\s*=>\s*\{', stripped) or \
               re.search(r'async\s*\([^)]*\)\s*=>\s*\{', stripped):
                brace_idx = line.find('{')
                if brace_idx >= 0:
                    end_brace = find_matching_brace('\n'.join(lines[i:]), 0)
                    if end_brace > 0:
                        function_regions.append((i, i + end_brace))
            # 检测function定义开始
            elif re.search(r'async\s+function\s+\w+\s*\([^)]*\)\s*\{', stripped):
                brace_idx = line.find('{')
                if brace_idx >= 0:
                    end_brace = find_matching_brace('\n'.join(lines[i:]), 0)
                    if end_brace > 0:
                        function_regions.append((i, i + end_brace))
        
        # 检测是否在函数定义区域内
        def is_in_function_def(line_idx):
            for start, end in function_regions:
                if start <= line_idx <= end:
                    return True
            return False
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not re.match(r'await\s+', stripped):
                continue
            if re.match(r'await\s+new\s+Promise\b', stripped):
                continue
            if re.match(r'await\s+sleep\b', stripped):
                continue
            
            # 排除在函数定义内部的await（callback不立即执行）
            if is_in_function_def(i):
                continue
            
            target = self._extract_call_target(stripped)
            if not target or '.' not in target:
                continue
            if self._is_excluded_target(target):
                continue
            
            calls.append({
                'line': i,
                'type': 'await',
                'target': target,
                'raw': stripped[:100],
            })
        
        return calls
    
    def _extract_call_target(self, stripped: str) -> str:
        """提取调用目标"""
        m = re.match(r'await\s+(\w+(?:\.\w+)*)\s*\(', stripped)
        if m:
            return m.group(1)
        return stripped[:50]
    
    def _is_excluded_target(self, target: str) -> bool:
        """检查是否为排除对象"""
        m = re.match(r'(\w+)\.(\w+)', target)
        if m:
            obj_name = m.group(1)
            method_name = m.group(2)
            if obj_name in self.EXCLUDED_OBJ_NAMES:
                return True
            if method_name in self.EXCLUDED_METHOD_PATTERNS:
                return True
        return False
    
    def _detect_shared_state(self, calls: List[Dict]) -> Dict[str, List[Dict]]:
        """检测共享状态（同一对象的多个调用）"""
        shared_groups = {}
        for call in calls:
            target = call.get('target', '')
            m = re.match(r'(\w+)\.', target)
            if m:
                obj_name = m.group(1)
                if obj_name not in self.EXCLUDED_OBJ_NAMES:
                    if obj_name not in shared_groups:
                        shared_groups[obj_name] = []
                    shared_groups[obj_name].append(call)
        return {k: v for k, v in shared_groups.items() if len(v) >= 2}
    
    def _check_serialization(self, calls: List[Dict], body: str = None) -> Tuple[bool, str]:
        """检查是否正确序列化（await调用之间是否有未await的异步交错）"""
        await_calls = sorted(calls, key=lambda c: c['line'])
        
        if len(await_calls) < 2:
            return True, None
        
        lines = body.split('\n') if body else []
        
        # 检查await之间是否有未await的异步交错操作（真正的并发风险）
        has_async_interleaving = False
        for i in range(len(await_calls) - 1):
            curr = await_calls[i]
            next_c = await_calls[i + 1]
            
            # 获取两个await之间的代码行
            if lines and next_c['line'] - curr['line'] > 1:
                interleave_lines = lines[curr['line'] + 1:next_c['line']]
                
                # 检查是否有未await的异步操作（真正的并发风险）
                for line in interleave_lines:
                    stripped = line.strip()
                    # 排除同步操作
                    if re.match(r'(?:let|const|var)\s+', stripped):
                        continue
                    if re.match(r'console\.', stripped) or re.match(r'hilog\.', stripped):
                        continue
                    if re.match(r'expect\.', stripped):
                        continue
                    if re.match(r'if\s*\(', stripped) or stripped == '}':
                        continue
                    if stripped.startswith('//') or stripped.startswith('*'):
                        continue
                    if not stripped:
                        continue
                    
                    # 排除已await的异步操作（序列化执行，不构成并发风险）
                    if re.match(r'await\s+', stripped):
                        continue
                    
                    # 排除明确的同步操作（不构成并发风险）
                    sync_patterns = [
                        r'hilog\.(info|error|warn|debug|log)',    # hilog日志
                        r'console\.(log|info|error|warn)',        # console日志
                        r'expect\.',                               # expect断言
                        r'\.(setPoint|setMarker|setValue)',       # 数据设置方法
                        r'\.(getType|getName|getSize)',           # 数据查询方法
                        r'\.(toString|valueOf|hasOwnProperty)',   # Object方法
                        r'\.(push|pop|shift|splice|slice)',       # Array方法
                        r'\.(map|filter|forEach|find)',           # Array遍历
                        r'JSON\.(stringify|parse)',               # JSON方法
                        r'\w+\.\w+\s*=\s*',                        # 属性赋值
                    ]
                    
                    is_sync = False
                    for sync_pat in sync_patterns:
                        if re.search(sync_pat, stripped):
                            is_sync = True
                            break
                    
                    if is_sync:
                        continue
                    
                    # 检查是否有未await的异步操作（真正的并发风险）
                    async_patterns = [
                        r'setTimeout\s*\(',                 # 定时器
                        r'setInterval\s*\(',                 # 定时器
                        r'Promise\.',                        # Promise操作
                        r'Promise\s*<',                      # Promise类型
                        r'\.start\s*\(',                     # 启动操作
                        r'\.run\s*\(',                       # 运行操作
                        r'\.execute\s*\(',                   # 执行操作
                        r'\.trigger\s*\(',                   # 触发操作
                        r'\.emit\s*\(',                      # 事件触发
                        r'\.subscribe\s*\(',                 # 订阅操作
                        r'\.on\s*\([^)]*\)\s*;',             # 事件监听（无await）
                        r'new\s+\w+\s*\(',                   # 新建对象（可能是Promise/异步类）
                    ]
                    
                    for pattern in async_patterns:
                        if re.search(pattern, stripped):
                            has_async_interleaving = True
                            break
                    
                    if has_async_interleaving:
                        break
            
            if has_async_interleaving:
                break
        
        if not has_async_interleaving:
            return True, None
        
        return False, "多个await调用之间存在未await的异步操作，存在并发风险"


# ============================================================================
# 复杂规则统一调度器
# ============================================================================

class ComplexRuleEngine:
    """复杂规则统一引擎 - 支持grep预过滤优化"""
    
    SCANNERS = {
        'R001': R001Scanner(),
        'R004': R004Scanner(),
        'R006': R006Scanner(),
        'R008': R008Scanner(),
        'R009': R009Scanner(),
        'R010': R010Scanner(),
        'R012': R012Scanner(),
        'R013': R013Scanner(),
        'R014': R014Scanner(),
        'R017': R017Scanner(),
        'R021': R021Scanner(),
        'R016': R016Scanner(),
        'R201': R201Scanner(),
        'R202': R202Scanner(),
        'R203': R203Scanner(),
        'R204': R204Scanner(),
        'R205': R205Scanner(),
        'R206': R206Scanner(),
    }
    
    GREP_KEYWORDS = {
        'R001': ['@ohos.systemparameter', 'getSync'],
        'R004': [],
        'R006': [],
        'R008': [],
        'R009': [],
        'R010': [],
        'R012': [],
        'R013': [],
        'R014': [],
        'R017': [],
        'R021': [],
        'R016': [],
        'R201': [],  # 不使用grep预过滤，需要扫描所有源文件
        'R202': ['.then\\(', '.catch\\(', 'await'],
        'R203': ['await'],
        'R204': ['.on\\(', '.subscribe\\('],
        'R205': [],
        'R206': ['globalThis', 'SharedArrayBuffer', 'SharedMap', 'SharedSet', 'new ArrayBuffer', 'new Uint8Array', 'new Int32Array'],
    }
    
    FILE_SCOPE = {
        'R001': ['*.ets', '*.ts', '*.js'],
        'R004': ['*.ets', '*.ts', '*.js'],
        'R006': ['*.ets', '*.ts', '*.js'],
        'R008': ['*.test.ets', '*.test.ts', '*.test.js'],
        'R009': ['*.test.ets', '*.test.ts', '*.test.js'],
        'R010': ['BUILD.gn'],
        'R012': ['*.p7b'],
        'R013': ['*.test.ets', '*.test.ts', '*.test.js'],
        'R017': ['syscap.json'],
        'R021': ['oh-package.json5'],
        'R016': ['*.test.ets', '*.test.ts', '*.test.js'],
        'R201': ['*.ets', '*.ts', '*.js'],
        'R202': ['*.ets', '*.ts', '*.js'],
        'R203': ['*.ets', '*.ts', '*.js'],
        'R204': ['*.ets', '*.ts', '*.js'],
        'R205': ['*.ets', '*.ts', '*.js'],
        'R206': ['*.ets', '*.ts', '*.js'],
    }
    
    def __init__(self, base_dir: str, rules: Set[str] = None, **kwargs):
        self.base_dir = base_dir
        self.active_rules = rules or set(self.SCANNERS.keys())
        self._fcache = kwargs.get('fcache', FileContentCache())
        self._bcache = kwargs.get('bc', BlockCache(self._fcache))
        self._fdef_cache = FunctionDefinitionCache(self._fcache)
        
        # 为所有Scanner设置base_dir
        for rid, scanner in self.SCANNERS.items():
            scanner.base_dir = base_dir
    
    def scan(self, files: List[str], workers: int = 0, progress_callback=None, 
                 sta_projects: Set[str] = None, cats: Dict = None) -> List[Dict]:
            """文件级并行扫描 - grep预过滤优化"""
            n_workers = workers or min(os.cpu_count() or 4, len(files))
            all_issues = []
            
            base_dir = self.base_dir
            
            if cats:
                all_source = cats.get('all_source', [])
                test_files = cats.get('test', [])
                build_gn = cats.get('build_gn', [])
                test_json = cats.get('test_json', [])
                p7b_files = cats.get('p7b', [])
                syscap_f = cats.get('syscap', [])
                oh_pkg = cats.get('oh_package', [])
                
                file_categories = {
                    'all_source': all_source,
                    'test_files': test_files,
                    'build_gn': build_gn,
                    'test_json': test_json,
                    'p7b_files': p7b_files,
                    'syscap_f': syscap_f,
                    'oh_package': oh_pkg,
                }

                FILE_MAP_COMPLEX = {
                    'R001': 'all_source',
                    'R004': 'all_source',  # 需要追踪跨文件的断言封装函数
                    'R006': 'all_source',  # 检测所有源文件中的deviceInfo.deviceType
                    'R008': 'test_files', 'R009': 'test_files',
                    'R010': 'build_gn', 'R012': 'p7b_files', 'R014': 'build_gn',
                    'R013': 'test_files', 'R016': 'test_files',
                    'R017': 'syscap_f', 'R021': 'oh_package',
                    'R201': 'all_source', 'R202': 'all_source', 'R203': 'all_source',
                    'R204': 'all_source', 'R205': 'all_source', 'R206': 'all_source',
                }
                FILE_GLOB_MAP = {
                    'all_source': ['*.ets', '*.ts', '*.js'],
                    'test_files': ['*.test.ets', '*.test.ts', '*.test.js'],
                    'build_gn': ['BUILD.gn'],
                    'test_json': ['test.json', 'Test.json'],
                    'p7b_files': ['*.p7b'],
                    'syscap_f': ['syscap.json'],
                    'oh_package': ['oh-package.json5'],
                }
                
                file_rule_map = {}
                for rid in self.active_rules:
                    if rid in self.SCANNERS:
                        category = FILE_MAP_COMPLEX.get(rid, 'all_source')
                        rule_files = file_categories.get(category, [])
                        
                        keywords = self.GREP_KEYWORDS.get(rid, [])
                        if keywords:
                            grep_patterns = [k for k in keywords if k]
                            if grep_patterns:
                                file_globs = FILE_GLOB_MAP.get(category, ['*.ets', '*.ts', '*.js'])
                                grep_results = grep_scan(base_dir, grep_patterns, file_globs=file_globs)
                                if grep_results:
                                    candidate_files = set(fp for fp, _, _, _ in grep_results)
                                    rule_files = [fp for fp in rule_files if fp in candidate_files]
                        
                        for fp in rule_files:
                            if fp not in file_rule_map:
                                file_rule_map[fp] = []
                            file_rule_map[fp].append(rid)
                
                scan_tasks = [(fp, rules) for fp, rules in file_rule_map.items()]
            else:
                scan_tasks = [(fp, self._get_rules_for_file(fp)) for fp in files]
            
            total_tasks = len(scan_tasks)
            done_count = 0
            last_callback_time = time.time()
            CALLBACK_INTERVAL = 2
            
            with ThreadPoolExecutor(max_workers=n_workers) as executor:
                futures = {executor.submit(self._scan_one_file_batch, fp, rules, sta_projects): fp
                           for fp, rules in scan_tasks}
                
                for future in as_completed(futures):
                    issues = future.result()
                    all_issues.extend(issues)
                    done_count += 1
                    current_time = time.time()
                    if progress_callback and (done_count % 100 == 0 or current_time - last_callback_time >= CALLBACK_INTERVAL):
                        progress_callback(done_count, total_tasks, len(all_issues))
                        last_callback_time = current_time
            
            return all_issues

    def _scan_one_file_batch(self, fp: str, rules: List[str], sta_projects: Set[str] = None) -> List[Dict]:
        """批量扫描单个文件的多个规则"""
        content = self._fcache.get(fp)
        if not content:
            return []
        
        all_issues = []
        for rid in rules:
            scanner = self.SCANNERS[rid]
            if rid == 'R202':
                issues = scanner.scan_file(fp, content, self._fcache, self._bcache,
                                          fdef_cache=self._fdef_cache)
            elif rid in ('R201', 'R206'):
                issues = scanner.scan_file(fp, content, self._fcache, self._bcache,
                                          sta_projects=sta_projects, fdef_cache=self._fdef_cache)
            else:
                issues = scanner.scan_file(fp, content, self._fcache, self._bcache)
            all_issues.extend(issues)
        return all_issues

    def _get_rules_for_file(self, fp: str) -> Set[str]:
        """获取适用于该文件的规则 - 支持多种文件命名模式"""
        applicable = set()
        basename = os.path.basename(fp)
        
        for rid, scopes in self.FILE_SCOPE.items():
            if rid not in self.active_rules:
                continue
            for scope in scopes:
                # 支持三种模式:
                # 1. *.ext - 扩展名匹配 (如 *.ets, *.test.ets)
                # 2. prefix_*.ext - 前缀匹配 (如 test_*.ets)
                # 3. *_suffix.ext - 后缀匹配 (如 *_test.ets)
                
                # 判断模式类型
                has_prefix_wildcard = scope.startswith('test_') or scope.startswith('*_')
                has_suffix_wildcard = '_*' in scope or '.test.' in scope
                
                if scope.startswith('*') and scope.count('*') == 1 and not scope.startswith('*_'):
                    # 标准扩展名匹配: *.ets, *.test.ets
                    if fp.endswith(scope[1:]):
                        applicable.add(rid)
                elif scope.startswith('*_'):
                    # 后缀匹配: *_test.ets
                    suffix_part = scope[1:]  # _test.ets
                    if basename.endswith(suffix_part):
                        applicable.add(rid)
                elif 'test_*' in scope:
                    # 前缀匹配: test_*.ets
                    parts = scope.split('.')
                    if len(parts) >= 2:
                        prefix_pattern = parts[0]  # test_*
                        ext = '.' + parts[-1]  # .ets
                        prefix = prefix_pattern.replace('*', '')  # test_ (去掉*)
                        if basename.startswith(prefix) and fp.endswith(ext):
                            applicable.add(rid)
                else:
                    # 完整文件名匹配
                    if basename == scope:
                        applicable.add(rid)
        
        return applicable
    
    def _scan_one_file(self, fp: str, rules: Set[str], sta_projects: Set[str] = None) -> List[Dict]:
        """扫描单个文件"""
        content = self._fcache.get(fp)
        if not content:
            return []
        
        all_issues = []
        for rid in rules:
            scanner = self.SCANNERS[rid]
            # 根据Scanner需求传递不同参数
            if rid == 'R202':
                # R202需要fdef_cache用于封装函数追踪
                issues = scanner.scan_file(fp, content, self._fcache, self._bcache, 
                                          fdef_cache=self._fdef_cache)
            elif rid in ('R201', 'R206'):
                # R201/R206需要sta_projects参数
                issues = scanner.scan_file(fp, content, self._fcache, self._bcache,
                                          sta_projects=sta_projects)
            else:
                # 其他Scanner只需要基本参数
                issues = scanner.scan_file(fp, content, self._fcache, self._bcache)
            all_issues.extend(issues)
        
        return all_issues


# ============================================================================
# 统一入口
# ============================================================================

def scan_complex_rules(files: List[str], base_dir: str, rules: Set[str] = None,
                       workers: int = 0, progress_callback=None, sta_projects: Set[str] = None, **kwargs) -> List[Dict]:
    """复杂规则扫描入口 - 使用cats优化"""
    cats = kwargs.get('cats')
    engine = ComplexRuleEngine(base_dir, rules, **kwargs)
    return engine.scan(files, workers, progress_callback, sta_projects, cats)


if __name__ == '__main__':
    print("复杂规则引擎 v2.0")
    print("已整合规则: R004, R006, R008, R012, R201, R202, R204, R205, R206")
    print("文件级并行，共享FileCache和BlockCache")