#!/usr/bin/env python3
"""
ModuleAnalyzer - 模块分析器
根据文件路径推断模块结构，组织代码元素
"""

import os
from dataclasses import dataclass, field
from typing import List, Dict, Set
from cpp_parser import ParsedFile, ClassInfo, FunctionInfo


@dataclass
class ModuleInfo:
    """模块信息"""
    name: str
    path: str
    files: List[str] = field(default_factory=list)
    classes: List[ClassInfo] = field(default_factory=list)
    functions: List[FunctionInfo] = field(default_factory=list)
    submodules: List[str] = field(default_factory=list)


class ModuleTree:
    """模块层次树"""
    
    def __init__(self):
        self.modules: Dict[str, ModuleInfo] = {}
    
    def add_module(self, module: ModuleInfo):
        """添加模块"""
        self.modules[module.name] = module
    
    def get_module(self, name: str) -> ModuleInfo:
        """获取模块"""
        return self.modules.get(name)
    
    def get_all_modules(self) -> List[ModuleInfo]:
        """获取所有模块"""
        return list(self.modules.values())


class ModuleAnalyzer:
    """模块分析器"""
    
    def infer_module(self, file_path: str) -> str:
        """
        根据文件路径推断模块名
        
        例如:
        - src/Parse/Lambda.cpp -> parse
        - src/Sema/TypeChecker.cpp -> sema
        - src/AST/Node.cpp -> ast
        
        Args:
            file_path: 文件路径
        
        Returns:
            模块名（小写）
        """
        # 规范化路径
        path = file_path.replace('\\', '/')
        parts = path.split('/')
        
        # 查找 src/ 目录后的第一个目录
        try:
            src_idx = parts.index('src')
            if src_idx + 1 < len(parts):
                module_name = parts[src_idx + 1]
                return module_name.lower()
        except ValueError:
            pass
        
        # 如果没有 src/ 目录，使用第一个目录
        if len(parts) > 1:
            return parts[0].lower()
        
        # 默认返回 'unknown'
        return 'unknown'
    
    def build_module_tree(self, parsed_files: List[ParsedFile]) -> ModuleTree:
        """
        构建模块层次结构
        
        Args:
            parsed_files: 解析后的文件列表
        
        Returns:
            ModuleTree 对象
        """
        tree = ModuleTree()
        module_files: Dict[str, List[ParsedFile]] = {}
        
        # 按模块分组文件
        for parsed_file in parsed_files:
            module_name = self.infer_module(parsed_file.path)
            if module_name not in module_files:
                module_files[module_name] = []
            module_files[module_name].append(parsed_file)
        
        # 为每个模块创建 ModuleInfo
        for module_name, files in module_files.items():
            # 推断模块路径（取第一个文件的目录）
            if files:
                first_file = files[0].path
                module_path = os.path.dirname(first_file)
            else:
                module_path = module_name
            
            # 收集模块中的所有类和函数
            all_classes = []
            all_functions = []
            file_paths = []
            
            for parsed_file in files:
                file_paths.append(parsed_file.path)
                all_classes.extend(parsed_file.classes)
                all_functions.extend(parsed_file.functions)
            
            module_info = ModuleInfo(
                name=module_name,
                path=module_path,
                files=file_paths,
                classes=all_classes,
                functions=all_functions
            )
            
            tree.add_module(module_info)
        
        # 分析子模块关系（基于路径层次）
        self._analyze_submodules(tree)
        
        return tree
    
    def _analyze_submodules(self, tree: ModuleTree):
        """分析子模块关系"""
        # 简化实现：基于模块名的前缀关系
        all_modules = tree.get_all_modules()
        
        for module in all_modules:
            # 查找可能的子模块
            for other in all_modules:
                if other.name != module.name:
                    # 如果 other 的路径以 module 的路径开头，则是子模块
                    if other.path.startswith(module.path + '/'):
                        if other.name not in module.submodules:
                            module.submodules.append(other.name)
    
    def get_module_files(self, tree: ModuleTree, module_name: str) -> List[str]:
        """
        获取模块包含的所有文件
        
        Args:
            tree: 模块树
            module_name: 模块名
        
        Returns:
            文件路径列表
        """
        module = tree.get_module(module_name)
        if module:
            return module.files
        return []


if __name__ == '__main__':
    # 简单测试
    from cpp_parser import CppParser
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python3 module_analyzer.py <目录路径>")
        sys.exit(1)
    
    # 扫描并解析文件
    from file_scanner import FileScanner
    
    scanner = FileScanner()
    parser = CppParser()
    analyzer = ModuleAnalyzer()
    
    root = sys.argv[1]
    files = scanner.scan(root, ['.h', '.cpp'])
    
    print(f"解析 {len(files)} 个文件...")
    parsed_files = []
    for file_path in files[:50]:  # 限制测试文件数量
        full_path = os.path.join(root, file_path)
        parsed = parser.parse_file(full_path)
        parsed_files.append(parsed)
    
    print("构建模块树...")
    tree = analyzer.build_module_tree(parsed_files)
    
    print(f"\n找到 {len(tree.modules)} 个模块:")
    for module in tree.get_all_modules():
        print(f"\n模块: {module.name}")
        print(f"  路径: {module.path}")
        print(f"  文件数: {len(module.files)}")
        print(f"  类数: {len(module.classes)}")
        print(f"  函数数: {len(module.functions)}")
        if module.submodules:
            print(f"  子模块: {', '.join(module.submodules)}")
