#!/usr/bin/env python3
"""
CppParser - C++ 解析器
解析 C++ 源文件，提取类、函数、#include 等信息
"""

import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ClassInfo:
    """类信息"""
    name: str
    file: str
    line: int
    is_struct: bool = False


@dataclass
class FunctionInfo:
    """函数信息"""
    name: str
    file: str
    line: int
    return_type: Optional[str] = None


@dataclass
class ParsedFile:
    """解析后的文件信息"""
    path: str
    classes: List[ClassInfo]
    functions: List[FunctionInfo]
    includes: List[str]


class CppParser:
    """C++ 源文件解析器"""
    
    # 类定义正则表达式（匹配 class 和 struct）
    CLASS_PATTERN = re.compile(
        r'^\s*(?:class|struct)\s+(\w+)',
        re.MULTILINE
    )
    
    # 函数定义正则表达式（简化版，匹配常见模式）
    FUNCTION_PATTERN = re.compile(
        r'^\s*(?:[\w:]+\s+)?(\w+)\s*\([^)]*\)\s*(?:const)?\s*(?:override)?\s*\{',
        re.MULTILINE
    )
    
    # #include 语句正则表达式
    INCLUDE_PATTERN = re.compile(
        r'^\s*#include\s+[<"]([^>"]+)[>"]',
        re.MULTILINE
    )
    
    def parse_file(self, file_path: str, relative_path: str = None) -> ParsedFile:
        """
        解析单个文件，返回提取的信息
        
        Args:
            file_path: 文件的完整路径（用于读取）
            relative_path: 文件的相对路径（用于存储，如果为None则使用file_path）
        
        Returns:
            ParsedFile 对象
        """
        # 使用相对路径存储，如果没有提供则使用完整路径
        stored_path = relative_path if relative_path else file_path
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            # 如果读取失败，返回空结果
            return ParsedFile(path=stored_path, classes=[], functions=[], includes=[])
        
        classes = self.extract_classes(content, stored_path)
        functions = self.extract_functions(content, stored_path)
        includes = self.extract_includes(content)
        
        return ParsedFile(
            path=stored_path,
            classes=classes,
            functions=functions,
            includes=includes
        )
    
    def extract_classes(self, content: str, file_path: str) -> List[ClassInfo]:
        """
        提取类定义
        
        Args:
            content: 文件内容
            file_path: 文件路径
        
        Returns:
            ClassInfo 列表
        """
        classes = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, start=1):
            # 跳过注释行
            if line.strip().startswith('//'):
                continue
            
            # 匹配 class 或 struct
            match = re.match(r'^\s*(class|struct)\s+(\w+)', line)
            if match:
                keyword, class_name = match.groups()
                classes.append(ClassInfo(
                    name=class_name,
                    file=file_path,
                    line=i,
                    is_struct=(keyword == 'struct')
                ))
        
        return classes
    
    def extract_functions(self, content: str, file_path: str) -> List[FunctionInfo]:
        """
        提取函数定义和声明
        
        Args:
            content: 文件内容
            file_path: 文件路径
        
        Returns:
            FunctionInfo 列表
        """
        functions = []
        lines = content.split('\n')
        
        # 简化的函数匹配：查找包含 '(' 的行
        for i, line in enumerate(lines, start=1):
            # 跳过注释和预处理指令
            stripped = line.strip()
            if stripped.startswith('//') or stripped.startswith('#'):
                continue
            
            # 匹配函数定义模式：返回类型 [命名空间::]函数名(参数) {
            # 支持命名空间限定名，如 TypeChecker::TypeCheckerImpl::InferTypeOfThis
            match_def = re.match(
                r'^\s*(?:[\w:<>*&]+\s+)?([\w:]+)\s*\([^)]*\)\s*(?:const)?\s*(?:override)?\s*\{',
                line
            )
            
            # 匹配函数声明模式：返回类型 [命名空间::]函数名(参数);
            match_decl = re.match(
                r'^\s*(?:[\w:<>*&]+\s+)?([\w:]+)\s*\([^)]*\)\s*(?:const)?\s*(?:override)?\s*;',
                line
            )
            
            match = match_def or match_decl
            if match:
                func_name = match.group(1)
                # 过滤掉一些常见的非函数关键字
                if func_name not in {'if', 'while', 'for', 'switch', 'catch'}:
                    functions.append(FunctionInfo(
                        name=func_name,
                        file=file_path,
                        line=i
                    ))
        
        return functions
    
    def extract_includes(self, content: str) -> List[str]:
        """
        提取 #include 语句
        
        Args:
            content: 文件内容
        
        Returns:
            包含的头文件列表
        """
        includes = []
        for match in self.INCLUDE_PATTERN.finditer(content):
            includes.append(match.group(1))
        return includes


if __name__ == '__main__':
    # 简单测试
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python3 cpp_parser.py <文件路径>")
        sys.exit(1)
    
    parser = CppParser()
    result = parser.parse_file(sys.argv[1])
    
    print(f"文件: {result.path}")
    print(f"\n类 ({len(result.classes)}):")
    for cls in result.classes:
        print(f"  {cls.name} (行 {cls.line})")
    
    print(f"\n函数 ({len(result.functions)}):")
    for func in result.functions[:10]:  # 只显示前 10 个
        print(f"  {func.name} (行 {func.line})")
    if len(result.functions) > 10:
        print(f"  ... 还有 {len(result.functions) - 10} 个函数")
    
    print(f"\n包含 ({len(result.includes)}):")
    for inc in result.includes[:10]:
        print(f"  {inc}")
    if len(result.includes) > 10:
        print(f"  ... 还有 {len(result.includes) - 10} 个包含")
