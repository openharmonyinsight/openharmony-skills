#!/usr/bin/env python3
"""
FileScanner - 文件扫描器
递归遍历编译器源码目录，识别需要处理的 C++ 文件
"""

import os
from datetime import datetime
from typing import List, Set


class FileScanner:
    """扫描编译器源码目录，返回需要处理的文件列表"""
    
    def __init__(self, exclude_dirs: Set[str] = None):
        """
        初始化文件扫描器
        
        Args:
            exclude_dirs: 需要排除的目录名集合
        """
        self.exclude_dirs = exclude_dirs or {'build', 'test', 'tests', '.git', '__pycache__'}
    
    def scan(self, root_dir: str, extensions: List[str]) -> List[str]:
        """
        扫描目录，返回所有匹配扩展名的文件路径
        
        Args:
            root_dir: 根目录路径
            extensions: 文件扩展名列表（如 ['.h', '.cpp']）
        
        Returns:
            文件路径列表（相对于 root_dir）
        """
        if not os.path.exists(root_dir):
            raise FileNotFoundError(f"目录不存在: {root_dir}")
        
        files = []
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # 排除指定目录
            dirnames[:] = [d for d in dirnames if d not in self.exclude_dirs]
            
            # 收集匹配扩展名的文件
            for filename in filenames:
                if any(filename.endswith(ext) for ext in extensions):
                    file_path = os.path.join(dirpath, filename)
                    # 返回相对路径
                    rel_path = os.path.relpath(file_path, root_dir)
                    files.append(rel_path)
        
        return sorted(files)
    
    def get_modified_files(self, root_dir: str, extensions: List[str], since: datetime) -> List[str]:
        """
        返回自指定时间以来修改过的文件（用于增量更新）
        
        Args:
            root_dir: 根目录路径
            extensions: 文件扩展名列表
            since: 时间戳，只返回此时间之后修改的文件
        
        Returns:
            修改过的文件路径列表
        """
        all_files = self.scan(root_dir, extensions)
        modified_files = []
        
        since_timestamp = since.timestamp()
        
        for rel_path in all_files:
            full_path = os.path.join(root_dir, rel_path)
            try:
                mtime = os.path.getmtime(full_path)
                if mtime > since_timestamp:
                    modified_files.append(rel_path)
            except OSError:
                # 文件可能在扫描过程中被删除
                continue
        
        return modified_files


if __name__ == '__main__':
    # 简单测试
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python3 file_scanner.py <目录路径>")
        sys.exit(1)
    
    scanner = FileScanner()
    root = sys.argv[1]
    
    print(f"扫描目录: {root}")
    files = scanner.scan(root, ['.h', '.cpp'])
    print(f"找到 {len(files)} 个文件:")
    for f in files[:10]:  # 只显示前 10 个
        print(f"  {f}")
    if len(files) > 10:
        print(f"  ... 还有 {len(files) - 10} 个文件")
