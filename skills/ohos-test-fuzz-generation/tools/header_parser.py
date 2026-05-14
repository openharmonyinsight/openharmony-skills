#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版C++头文件解析器
支持模板、宏、条件编译、嵌套类等复杂情况
"""

import re
import os
import sys
import io
from pathlib import Path
from typing import List, Tuple, Optional, Dict

# Windows兼容性：强制UTF-8编码
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
    os.environ["PYTHONIOENCODING"] = "utf-8"


class HeaderParser:
    """增强版头文件解析器"""

    def __init__(self, header_path: str):
        self.header_path = header_path
        self.content = self._read_and_preprocess()

    def _read_and_preprocess(self) -> str:
        """读取文件并进行预处理"""
        try:
            with open(self.header_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            print(f"[WARN] 无法读取头文件: {e}")
            return ""

        # 1. 移除单行注释
        content = re.sub(r"//[^\n]*", "", content)

        # 2. 移除多行注释
        content = re.sub(r"/\*.*?\*/", "", content, flags=re.DOTALL)

        # 3. 处理续行
        content = re.sub(r"\\\s*\n", " ", content)

        # 4. 简化宏定义（保留关键信息）
        content = self._simplify_macros(content)

        # 5. 处理条件编译（保留主要分支）
        content = self._simplify_conditional_compilation(content)

        return content

    def _simplify_macros(self, content: str) -> str:
        """简化宏定义，保留关键信息"""
        # 移除简单的宏定义
        content = re.sub(r"#define\s+\w+\s+[^\n]*", "", content)
        # 保留带参数的宏（可能包含类型信息）
        content = re.sub(r"#define\s+\w+\([^)]*\)\s+[^\n]*", "", content)
        return content

    def _simplify_conditional_compilation(self, content: str) -> str:
        """简化条件编译，保留主要分支"""
        lines = content.split("\n")
        result_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            if line.startswith("#ifndef"):
                match = re.match(r"#ifndef\s+(\w+)", line)
                if match:
                    guard_name = match.group(1)
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        define_match = re.match(r"#define\s+(\w+)", next_line)
                        if define_match and define_match.group(1) == guard_name:
                            end_idx = self._find_matching_endif(lines, i)
                            if end_idx != -1:
                                for j in range(i + 2, end_idx):
                                    result_lines.append(lines[j])
                                i = end_idx + 1
                                continue
            
            if line.startswith("#ifdef"):
                match = re.match(r"#ifdef\s+(\w+)", line)
                if match:
                    macro = match.group(1)
                    end_idx = self._find_matching_endif(lines, i)
                    if end_idx != -1:
                        if macro == "__cplusplus":
                            for j in range(i + 1, end_idx):
                                result_lines.append(lines[j])
                        else:
                            block_content = self._extract_main_branch(lines, i, end_idx)
                            result_lines.extend(block_content)
                        i = end_idx + 1
                        continue
            
            if line.startswith("#if"):
                match = re.match(r"#if\s+(\d+)", line)
                if match:
                    val = int(match.group(1))
                    end_idx = self._find_matching_endif(lines, i)
                    if end_idx != -1:
                        if val == 0:
                            pass
                        elif val == 1:
                            for j in range(i + 1, end_idx):
                                result_lines.append(lines[j])
                        else:
                            block_content = self._extract_main_branch(lines, i, end_idx)
                            result_lines.extend(block_content)
                        i = end_idx + 1
                        continue
            
            if not re.match(r"#\s*(ifdef|ifndef|if|elif|else|endif|pragma|error|warning|line|include)\b", line):
                result_lines.append(lines[i])
            
            i += 1
        
        return "\n".join(result_lines)
    
    def _find_matching_endif(self, lines: List[str], start_idx: int) -> int:
        """找到匹配的#endif"""
        depth = 0
        for i in range(start_idx, len(lines)):
            line = lines[i].strip()
            if re.match(r"#\s*(if|ifdef|ifndef)\b", line):
                depth += 1
            elif re.match(r"#\s*endif\b", line):
                depth -= 1
                if depth == 0:
                    return i
        return -1
    
    def _extract_main_branch(self, lines: List[str], start_idx: int, end_idx: int) -> List[str]:
        """提取条件编译的主分支内容（优先#else分支）"""
        result = []
        depth = 0
        in_else = False
        capture = True
        
        for i in range(start_idx + 1, end_idx):
            line = lines[i].strip()
            
            if re.match(r"#\s*(if|ifdef|ifndef)\b", line):
                if capture and not in_else:
                    result.append(lines[i])
                depth += 1
            elif re.match(r"#\s*endif\b", line):
                depth -= 1
                if capture and not in_else:
                    result.append(lines[i])
            elif re.match(r"#\s*elif\b", line):
                if depth == 0:
                    capture = False
            elif re.match(r"#\s*else\b", line):
                if depth == 0:
                    in_else = True
                    capture = True
                    result = []
            else:
                if capture and depth == 0:
                    result.append(lines[i])
        
        return result

    def parse_class(self, class_name: str) -> List[Tuple[str, str, str]]:
        """
        解析指定类的public方法

        Returns:
            List[(method_name, params, return_type)]
        """
        methods = []

        # 查找类定义（支持模板类）
        class_pattern = (
            rf"\b(?:template\s*<[^>]*>\s*)?(?:class|struct)\s+{re.escape(class_name)}\b"
        )
        class_match = re.search(class_pattern, self.content)

        if not class_match:
            print(f"[WARN] 未找到类定义: {class_name}")
            return methods

        # 提取类体
        start = class_match.end()
        class_body = self._extract_braced_block(start)

        if not class_body:
            print(f"[WARN] 无法提取类体: {class_name}")
            return methods

        # 提取public区域
        public_sections = self._extract_public_sections(class_body)

        for section in public_sections:
            section_methods = self._parse_methods_in_section(section, class_name)
            methods.extend(section_methods)

        # 去重
        seen = set()
        unique_methods = []
        for name, params, ret in methods:
            key = (name, params)
            if key not in seen:
                seen.add(key)
                unique_methods.append((name, params, ret))

        return unique_methods

    def _extract_braced_block(self, start_pos: int) -> str:
        """提取花括号包围的块"""
        # 找到第一个 {
        brace_start = self.content.find("{", start_pos)
        if brace_start == -1:
            return ""

        brace_count = 0
        end_pos = brace_start

        for i in range(brace_start, len(self.content)):
            if self.content[i] == "{":
                brace_count += 1
            elif self.content[i] == "}":
                brace_count -= 1
                if brace_count == 0:
                    end_pos = i
                    break

        return self.content[brace_start : end_pos + 1]

    def _extract_public_sections(self, class_body: str) -> List[str]:
        """提取所有public区域"""
        sections = []

        # 找到所有public:位置
        public_pattern = r"\bpublic\s*:"
        public_matches = list(re.finditer(public_pattern, class_body))

        if not public_matches:
            # 如果是struct，默认所有成员都是public
            if "struct" in class_body[:50]:
                return [class_body]
            return []

        for i, match in enumerate(public_matches):
            start = match.end()

            # 找到下一个访问修饰符或类结束
            if i + 1 < len(public_matches):
                end = public_matches[i + 1].start()
            else:
                # 找到下一个protected/private或类结束
                next_access = re.search(
                    r"\b(protected|private)\s*:", class_body[start:]
                )
                if next_access:
                    end = start + next_access.start()
                else:
                    # 找到匹配的 }
                    end = len(class_body)

            sections.append(class_body[start:end])

        return sections

    def _parse_methods_in_section(
        self, section: str, class_name: str
    ) -> List[Tuple[str, str, str]]:
        """解析区域中的方法"""
        methods = []

        # 改进的方法匹配模式
        # 支持：
        # - 模板方法
        # - 各种修饰符（virtual, static, explicit, constexpr, inline, consteval, constinit）
        # - 返回类型（包括模板类型、指针、引用）
        # - 方法名（包括运算符重载）
        # - 参数列表（包括默认参数）
        # - 后缀（const, override, final, noexcept, = 0, = default, = delete）

        method_pattern = re.compile(
            r"(?:^|;)\s*"  # 开始位置或分号后
            r"(?:template\s*<[^>]*>\s*)?"  # 可选模板声明
            r"(?P<modifiers>(?:virtual|static|explicit|constexpr|inline|consteval|constinit|mutable|friend|\[\[.*?\]\]|\s)*)"  # 修饰符
            r"(?P<ret>[~\w_:][\w\s_:<>,*&.]*?)"  # 返回类型
            r"\s+"
            r"(?P<name>operator\s*[^\s(]+|\w+|~\w+)"  # 方法名（支持运算符重载和析构函数）
            r"\s*\(\s*"
            r"(?P<params>[^)]*)"  # 参数
            r"\)\s*"
            r"(?P<suffix>(?:const\s*)?(?:volatile\s*)?(?:override\s*)?(?:final\s*)?(?:noexcept\s*(?:\([^)]*\))?)?(?:->\s*[\w_:<>\s*&]+)?)"  # 后缀
            r"\s*(?:=\s*(?:0|default|delete)\s*)?"  # 纯虚/默认/删除
            r";",  # 分号结束
            re.MULTILINE,
        )

        for match in method_pattern.finditer(section):
            name = match.group("name").strip()
            ret = match.group("ret").strip()
            params = match.group("params").strip()
            modifiers = match.group("modifiers").strip()

            # 排除构造函数
            if name == class_name or name == f"~{class_name}":
                continue

            # 排除析构函数
            if name.startswith("~"):
                continue

            # 排除friend声明
            if "friend" in modifiers:
                continue

            # 排除纯属性宏
            if not re.match(r"^[A-Za-z_~]\w*$", name) and not name.startswith(
                "operator"
            ):
                continue

            # 排除无参方法
            if not params or params.lower() == "void":
                continue

            # 检查是否所有参数都是输出参数
            if self._is_all_output_params(params):
                continue

            # 清理返回类型
            ret = self._clean_return_type(ret)

            methods.append((name, params, ret))

        return methods

    def _clean_return_type(self, ret_type: str) -> str:
        """清理返回类型"""
        ret_type = ret_type.strip()

        # 移除不必要的修饰符
        ret_type = re.sub(r"\bvirtual\b", "", ret_type).strip()
        ret_type = re.sub(r"\bstatic\b", "", ret_type).strip()
        ret_type = re.sub(r"\bexplicit\b", "", ret_type).strip()
        ret_type = re.sub(r"\bconstexpr\b", "", ret_type).strip()
        ret_type = re.sub(r"\binline\b", "", ret_type).strip()

        # 移除属性
        ret_type = re.sub(r"\[\[.*?\]\]", "", ret_type).strip()

        return ret_type if ret_type else "void"

    def _is_all_output_params(self, param_str: str) -> bool:
        """检查是否所有参数都是输出参数"""
        if not param_str or param_str.lower() == "void":
            return True

        # 分割参数（处理嵌套括号）
        parts = self._split_params(param_str)

        if not parts:
            return True

        for part in parts:
            part = re.sub(r"=.*", "", part).strip()
            if not part:
                continue

            # 检查是否是输入参数
            if self._is_input_param(part):
                return False

        return True

    def _split_params(self, param_str: str) -> List[str]:
        """分割参数列表（处理嵌套括号）"""
        parts = []
        depth = 0
        current = ""

        for ch in param_str:
            if ch in "(<{[":
                depth += 1
                current += ch
            elif ch in ")>}]":
                depth -= 1
                current += ch
            elif ch == "," and depth == 0:
                parts.append(current.strip())
                current = ""
            else:
                current += ch

        if current.strip():
            parts.append(current.strip())

        return parts

    def _is_input_param(self, param: str) -> bool:
        """检查参数是否是输入参数"""
        param = param.strip()
        if not param:
            return False

        # 移除默认值
        param = re.sub(r"=.*", "", param).strip()

        # const引用/指针是输入参数
        if "const" in param.lower() and ("&" in param or "*" in param):
            return True

        # 基本类型是输入参数
        base_type = self._clean_type(param)
        basic_types = {
            "uint8_t",
            "uint16_t",
            "uint32_t",
            "uint64_t",
            "int8_t",
            "int16_t",
            "int32_t",
            "int64_t",
            "int",
            "bool",
            "float",
            "double",
            "size_t",
            "std::string",
            "string",
            "std::u16string",
            "char",
            "wchar_t",
            "char16_t",
            "char32_t",
            "short",
            "long",
            "unsigned",
            "signed",
        }

        if base_type in basic_types:
            return True

        # 枚举类型是输入参数
        if base_type and base_type[0].isupper() and not base_type.startswith("std::"):
            return True

        return False

    def _clean_type(self, raw_type: str) -> str:
        """清理类型字符串"""
        t = raw_type.strip()
        t = re.sub(r"\b(const|volatile)\b", "", t).strip()
        t = t.rstrip("&").rstrip("*").strip()
        t = re.sub(r"=.*", "", t).strip()
        return t


def parse_header_methods_enhanced(
    header_path: str, target_class: str
) -> List[Tuple[str, str, str]]:
    """
    增强版头文件方法解析入口

    Args:
        header_path: 头文件路径
        target_class: 目标类名

    Returns:
        List[(method_name, params, return_type)]
    """
    if not header_path or not os.path.isfile(header_path):
        print(f"[WARN] 头文件不存在: {header_path}")
        return []

    parser = HeaderParser(header_path)
    methods = parser.parse_class(target_class)

    if methods:
        print(f"[OK] 从头文件解析到 {len(methods)} 个 public 有参方法")
        for name, params, ret in methods[:5]:  # 只显示前5个
            print(f"  - {ret} {name}({params})")
        if len(methods) > 5:
            print(f"  ... 还有 {len(methods) - 5} 个方法")
    else:
        print(f"[WARN] 未能从 {header_path} 解析到 {target_class} 的方法")

    return methods


# 向后兼容
parse_header_methods = parse_header_methods_enhanced
