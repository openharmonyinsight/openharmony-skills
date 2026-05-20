#!/usr/bin/env python3
"""
CrossRefBuilder - 交叉引用构建器
构建模块依赖和函数调用的交叉引用
"""

import json
from dataclasses import dataclass, field, asdict
from typing import Dict, List
from dependency_analyzer import DependencyGraph, CallGraph


@dataclass
class ModuleReference:
    """模块交叉引用"""
    depends_on: List[str] = field(default_factory=list)
    depended_by: List[str] = field(default_factory=list)


@dataclass
class FunctionReference:
    """函数交叉引用"""
    calls: List[str] = field(default_factory=list)
    called_by: List[str] = field(default_factory=list)


@dataclass
class CrossReference:
    """交叉引用数据结构"""
    module_dependencies: Dict[str, ModuleReference] = field(default_factory=dict)
    function_calls: Dict[str, FunctionReference] = field(default_factory=dict)


class CrossRefBuilder:
    """交叉引用构建器"""
    
    def build_module_refs(self, dep_graph: DependencyGraph) -> Dict[str, ModuleReference]:
        """
        构建模块依赖的双向引用
        
        Args:
            dep_graph: 依赖图
        
        Returns:
            模块名 -> ModuleReference 的字典
        """
        module_refs = {}
        
        # 获取所有模块名
        all_modules = set(dep_graph.module_dependencies.keys()) | set(dep_graph.module_dependents.keys())
        
        for module in all_modules:
            module_refs[module] = ModuleReference(
                depends_on=dep_graph.module_dependencies.get(module, []),
                depended_by=dep_graph.module_dependents.get(module, [])
            )
        
        return module_refs
    
    def build_function_refs(self, call_graph: CallGraph) -> Dict[str, FunctionReference]:
        """
        构建函数调用的双向引用
        
        Args:
            call_graph: 调用图
        
        Returns:
            函数名 -> FunctionReference 的字典
        """
        function_refs = {}
        
        # 获取所有函数名
        all_functions = set(call_graph.function_calls.keys()) | set(call_graph.function_callers.keys())
        
        for function in all_functions:
            function_refs[function] = FunctionReference(
                calls=call_graph.function_calls.get(function, []),
                called_by=call_graph.function_callers.get(function, [])
            )
        
        return function_refs
    
    def build(self, dep_graph: DependencyGraph, call_graph: CallGraph) -> CrossReference:
        """
        构建完整的交叉引用
        
        Args:
            dep_graph: 依赖图
            call_graph: 调用图
        
        Returns:
            CrossReference 对象
        """
        return CrossReference(
            module_dependencies=self.build_module_refs(dep_graph),
            function_calls=self.build_function_refs(call_graph)
        )
    
    def to_json(self, cross_ref: CrossReference) -> str:
        """
        将交叉引用转换为 JSON 字符串
        
        Args:
            cross_ref: 交叉引用对象
        
        Returns:
            JSON 字符串
        """
        # 转换为字典格式
        data = {
            "module_dependencies": {
                module: {
                    "depends_on": ref.depends_on,
                    "depended_by": ref.depended_by
                }
                for module, ref in cross_ref.module_dependencies.items()
            },
            "function_calls": {
                function: {
                    "calls": ref.calls,
                    "called_by": ref.called_by
                }
                for function, ref in cross_ref.function_calls.items()
            }
        }
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def save_to_file(self, cross_ref: CrossReference, output_path: str):
        """
        将交叉引用保存到文件
        
        Args:
            cross_ref: 交叉引用对象
            output_path: 输出文件路径
        """
        json_str = self.to_json(cross_ref)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(json_str)


if __name__ == '__main__':
    # 简单测试
    from file_scanner import FileScanner
    from cpp_parser import CppParser
    from module_analyzer import ModuleAnalyzer
    from dependency_analyzer import DependencyAnalyzer
    import sys
    import os
    
    if len(sys.argv) < 2:
        print("用法: python3 cross_ref_builder.py <目录路径>")
        sys.exit(1)
    
    scanner = FileScanner()
    parser = CppParser()
    module_analyzer = ModuleAnalyzer()
    dep_analyzer = DependencyAnalyzer()
    builder = CrossRefBuilder()
    
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
    
    print("分析依赖关系...")
    dep_graph = dep_analyzer.analyze_module_dependencies(tree, parsed_files)
    call_graph = dep_analyzer.analyze_function_calls(parsed_files)
    
    print("构建交叉引用...")
    cross_ref = builder.build(dep_graph, call_graph)
    
    print(f"\n模块交叉引用（前 5 个）:")
    count = 0
    for module, ref in cross_ref.module_dependencies.items():
        if (ref.depends_on or ref.depended_by) and count < 5:
            print(f"\n{module}:")
            if ref.depends_on:
                print(f"  depends_on: {', '.join(ref.depends_on)}")
            if ref.depended_by:
                print(f"  depended_by: {', '.join(ref.depended_by)}")
            count += 1
    
    print(f"\n函数交叉引用（前 5 个）:")
    count = 0
    for function, ref in cross_ref.function_calls.items():
        if (ref.calls or ref.called_by) and count < 5:
            print(f"\n{function}:")
            if ref.calls:
                print(f"  calls: {', '.join(ref.calls[:3])}")
            if ref.called_by:
                print(f"  called_by: {', '.join(ref.called_by[:3])}")
            count += 1
    
    # 保存到文件
    output_path = "cross-references.json"
    builder.save_to_file(cross_ref, output_path)
    print(f"\n交叉引用已保存到: {output_path}")
