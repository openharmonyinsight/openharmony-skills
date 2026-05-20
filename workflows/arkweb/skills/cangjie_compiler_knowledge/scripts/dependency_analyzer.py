#!/usr/bin/env python3
"""
DependencyAnalyzer - 依赖分析器
分析模块间依赖和函数调用关系
"""

import re
from dataclasses import dataclass, field
from typing import Dict, List, Set
from module_analyzer import ModuleTree, ModuleInfo
from cpp_parser import ParsedFile


@dataclass
class DependencyGraph:
    """依赖图"""
    # 模块依赖: module_name -> [依赖的模块列表]
    module_dependencies: Dict[str, List[str]] = field(default_factory=dict)
    # 反向依赖: module_name -> [依赖它的模块列表]
    module_dependents: Dict[str, List[str]] = field(default_factory=dict)


@dataclass
class CallGraph:
    """调用图"""
    # 函数调用: function_name -> [调用的函数列表]
    function_calls: Dict[str, List[str]] = field(default_factory=dict)
    # 反向调用: function_name -> [调用它的函数列表]
    function_callers: Dict[str, List[str]] = field(default_factory=dict)


class DependencyAnalyzer:
    """依赖分析器"""
    
    def __init__(self):
        self.module_analyzer = None  # 将在分析时设置
    
    def analyze_module_dependencies(
        self,
        tree: ModuleTree,
        parsed_files: List[ParsedFile]
    ) -> DependencyGraph:
        """
        分析模块依赖关系（通过 #include 语句）
        
        Args:
            tree: 模块树
            parsed_files: 解析后的文件列表
        
        Returns:
            DependencyGraph 对象
        """
        from module_analyzer import ModuleAnalyzer
        analyzer = ModuleAnalyzer()
        
        graph = DependencyGraph()
        
        # 为每个模块初始化依赖列表
        for module in tree.get_all_modules():
            graph.module_dependencies[module.name] = []
            graph.module_dependents[module.name] = []
        
        # 分析每个文件的 #include 语句
        for parsed_file in parsed_files:
            source_module = analyzer.infer_module(parsed_file.path)
            
            # 从 #include 推断依赖的模块
            for include in parsed_file.includes:
                # 从 include 路径推断模块
                # 例如: "Parse/Lambda.h" -> parse
                target_module = self._infer_module_from_include(include)
                
                if target_module and target_module != source_module:
                    # 添加依赖关系
                    if target_module not in graph.module_dependencies[source_module]:
                        graph.module_dependencies[source_module].append(target_module)
                    
                    # 添加反向依赖
                    if source_module not in graph.module_dependents.get(target_module, []):
                        if target_module not in graph.module_dependents:
                            graph.module_dependents[target_module] = []
                        graph.module_dependents[target_module].append(source_module)
        
        return graph
    
    def _infer_module_from_include(self, include_path: str) -> str:
        """
        从 #include 路径推断模块名
        
        例如:
        - "Parse/Lambda.h" -> parse
        - "Sema/TypeChecker.h" -> sema
        
        Args:
            include_path: include 路径
        
        Returns:
            模块名（小写）
        """
        # 规范化路径
        path = include_path.replace('\\', '/')
        parts = path.split('/')
        
        if len(parts) > 1:
            # 取第一个目录作为模块名
            return parts[0].lower()
        
        return None
    
    def analyze_function_calls(
        self,
        parsed_files: List[ParsedFile]
    ) -> CallGraph:
        """
        分析函数调用关系（使用启发式方法）
        
        这是一个简化的实现，使用文本匹配识别函数调用。
        更精确的实现需要使用 clang static analyzer。
        
        Args:
            parsed_files: 解析后的文件列表
        
        Returns:
            CallGraph 对象
        """
        graph = CallGraph()
        
        # 收集所有已知的函数名
        all_functions = set()
        for parsed_file in parsed_files:
            for func in parsed_file.functions:
                all_functions.add(func.name)
        
        # 分析每个文件中的函数调用
        for parsed_file in parsed_files:
            try:
                with open(parsed_file.path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except:
                continue
            
            # 对于文件中的每个函数，查找它调用的其他函数
            for func in parsed_file.functions:
                if func.name not in graph.function_calls:
                    graph.function_calls[func.name] = []
                
                # 使用启发式方法：查找 "函数名(" 模式
                for other_func in all_functions:
                    if other_func != func.name:
                        # 查找函数调用模式
                        pattern = rf'\b{re.escape(other_func)}\s*\('
                        if re.search(pattern, content):
                            if other_func not in graph.function_calls[func.name]:
                                graph.function_calls[func.name].append(other_func)
                            
                            # 添加反向调用关系
                            if other_func not in graph.function_callers:
                                graph.function_callers[other_func] = []
                            if func.name not in graph.function_callers[other_func]:
                                graph.function_callers[other_func].append(func.name)
        
        return graph


if __name__ == '__main__':
    # 简单测试
    from file_scanner import FileScanner
    from cpp_parser import CppParser
    from module_analyzer import ModuleAnalyzer
    import sys
    import os
    
    if len(sys.argv) < 2:
        print("用法: python3 dependency_analyzer.py <目录路径>")
        sys.exit(1)
    
    scanner = FileScanner()
    parser = CppParser()
    module_analyzer = ModuleAnalyzer()
    dep_analyzer = DependencyAnalyzer()
    
    root = sys.argv[1]
    files = scanner.scan(root, ['.h', '.cpp'])
    
    print(f"解析 {len(files)} 个文件...")
    parsed_files = []
    for file_path in files[:30]:  # 限制测试文件数量
        full_path = os.path.join(root, file_path)
        parsed = parser.parse_file(full_path)
        parsed.path = file_path  # 使用相对路径
        parsed_files.append(parsed)
    
    print("构建模块树...")
    tree = module_analyzer.build_module_tree(parsed_files)
    
    print("分析模块依赖...")
    dep_graph = dep_analyzer.analyze_module_dependencies(tree, parsed_files)
    
    print(f"\n模块依赖关系:")
    for module, deps in dep_graph.module_dependencies.items():
        if deps:
            print(f"  {module} -> {', '.join(deps)}")
    
    print("\n分析函数调用...")
    call_graph = dep_analyzer.analyze_function_calls(parsed_files)
    
    print(f"\n函数调用关系（前 5 个）:")
    count = 0
    for func, calls in call_graph.function_calls.items():
        if calls and count < 5:
            print(f"  {func} -> {', '.join(calls[:3])}")
            count += 1
