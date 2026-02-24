#!/usr/bin/env python3
"""
Android 代码分析脚本
扫描 Android 项目目录，生成代码结构报告
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Any


class AndroidCodeAnalyzer:
    """Android 代码分析器"""

    # Kotlin/Java 文件扩展名
    SOURCE_EXTENSIONS = {'.kt', '.kts', '.java'}

    # 组件类型识别
    COMPONENT_PATTERNS = {
        'Activity': r'class\s+\w*Activity\s*:',
        'Fragment': r'class\s+\w*Fragment\s*:',
        'Service': r'class\s+\w*Service\s*:',
        'Receiver': r'class\s+\w*Receiver\s*:',
        'Provider': r'class\s+\w*Provider\s*:',
        'Adapter': r'class\s+\w*Adapter\s*:',
        'ViewModel': r'class\s+\w*ViewModel\s*:',
        'Dialog': r'class\s+\w*Dialog\s*:',
    }

    # 导入语句识别
    IMPORT_PATTERNS = {
        'Room': r'androidx\.room',
        'RecyclerView': r'androidx\.recyclerview',
        'Lifecycle': r'androidx\.lifecycle',
        'Coroutines': r'kotlinx\.coroutines',
        'Retrofit': r'retrofit2',
        'Glide': r'com\.bumptech\.glide',
        'Gson': r'com\.google\.gson',
    }

    def __init__(self, source_path: str):
        self.source_path = Path(source_path)
        self.results = {
            'files': [],
            'statistics': {},
            'components': defaultdict(list),
            'dependencies': Counter(),
            'complexity': {},
        }

    def analyze(self) -> Dict[str, Any]:
        """执行分析"""
        if not self.source_path.exists():
            raise FileNotFoundError(f"源码路径不存在: {self.source_path}")

        self._scan_files()
        self._calculate_statistics()
        self._detect_components()
        self._analyze_dependencies()
        self._calculate_complexity()

        return self.results

    def _scan_files(self):
        """扫描所有源码文件"""
        for root, dirs, files in os.walk(self.source_path):
            # 跳过 build 目录
            if 'build' in dirs:
                dirs.remove('build')

            for file in files:
                ext = Path(file).suffix
                if ext in self.SOURCE_EXTENSIONS:
                    file_path = Path(root) / file
                    relative_path = file_path.relative_to(self.source_path)
                    line_count = self._count_lines(file_path)

                    self.results['files'].append({
                        'path': str(relative_path),
                        'extension': ext,
                        'lines': line_count,
                        'package': self._extract_package(file_path),
                    })

    def _count_lines(self, file_path: Path) -> int:
        """计算文件行数（排除空行和注释）"""
        count = 0
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('//') and not line.startswith('*'):
                    count += 1
        return count

    def _extract_package(self, file_path: Path) -> str:
        """提取包名"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    if line.strip().startswith('package '):
                        return line.strip().replace('package ', '').replace(';', '')
        except:
            pass
        return ''

    def _calculate_statistics(self):
        """计算统计数据"""
        files = self.results['files']
        total_lines = sum(f['lines'] for f in files)
        ext_count = Counter(f['extension'] for f in files)

        self.results['statistics'] = {
            'total_files': len(files),
            'total_lines': total_lines,
            'kotlin_files': ext_count.get('.kt', 0) + ext_count.get('.kts', 0),
            'java_files': ext_count.get('.java', 0),
            'average_lines_per_file': total_lines // len(files) if files else 0,
        }

    def _detect_components(self):
        """检测组件类型"""
        for file_info in self.results['files']:
            file_path = self.source_path / file_info['path']
            components = self._find_components_in_file(file_path)
            for comp_type in components:
                self.results['components'][comp_type].append(file_info['path'])

    def _find_components_in_file(self, file_path: Path) -> List[str]:
        """在文件中查找组件"""
        found = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                for comp_type, pattern in self.COMPONENT_PATTERNS.items():
                    if re.search(pattern, content):
                        found.append(comp_type)
        except:
            pass
        return found

    def _analyze_dependencies(self):
        """分析依赖库"""
        for file_info in self.results['files']:
            file_path = self.source_path / file_info['path']
            deps = self._find_imports_in_file(file_path)
            for dep in deps:
                self.results['dependencies'][dep] += 1

    def _find_imports_in_file(self, file_path: Path) -> List[str]:
        """在文件中查找导入"""
        found = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                for dep_name, pattern in self.IMPORT_PATTERNS.items():
                    if re.search(pattern, content):
                        found.append(dep_name)
        except:
            pass
        return found

    def _calculate_complexity(self):
        """计算复杂度评分"""
        for file_info in self.results['files']:
            file_path = self.source_path / file_info['path']
            complexity = self._calculate_file_complexity(file_path)
            self.results['complexity'][file_info['path']] = complexity

    def _calculate_file_complexity(self, file_path: Path) -> int:
        """计算单个文件的复杂度"""
        complexity = 0
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                # 根据不同模式增加复杂度
                complexity += len(re.findall(r'\bif\b', content))
                complexity += len(re.findall(r'\bfor\b', content)) * 2
                complexity += len(re.findall(r'\bwhile\b', content)) * 2
                complexity += len(re.findall(r'\btry\b', content))
                complexity += len(re.findall(r'\bwhen\b', content)) * 2
                complexity += len(re.findall(r'class\s+\w+', content)) * 3
        except:
            pass
        return complexity

    def print_report(self):
        """打印分析报告"""
        print("=" * 60)
        print("Android 代码分析报告")
        print("=" * 60)

        stats = self.results['statistics']
        print(f"\n总文件数: {stats['total_files']}")
        print(f"总代码行数: {stats['total_lines']}")
        print(f"Kotlin 文件: {stats['kotlin_files']}")
        print(f"Java 文件: {stats['java_files']}")
        print(f"平均文件行数: {stats['average_lines_per_file']}")

        print("\n" + "-" * 60)
        print("组件分布:")
        for comp_type, files in self.results['components'].items():
            print(f"  {comp_type}: {len(files)} 个")

        print("\n" + "-" * 60)
        print("依赖库:")
        for dep, count in self.results['dependencies'].most_common():
            print(f"  {dep}: {count} 个文件使用")

        print("\n" + "-" * 60)
        print("高复杂度文件 (>50):")
        high_complexity = {k: v for k, v in self.results['complexity'].items() if v > 50}
        for path, complexity in sorted(high_complexity.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {complexity:3d} - {path}")

        print("\n" + "=" * 60)

    def export_json(self, output_path: str):
        """导出 JSON 报告"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"报告已导出到: {output_path}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='分析 Android 代码')
    parser.add_argument('source_path', help='Android 源码路径')
    parser.add_argument('--output', '-o', help='输出 JSON 报告路径')
    parser.add_argument('--quiet', '-q', action='store_true', help='静默模式')

    args = parser.parse_args()

    analyzer = AndroidCodeAnalyzer(args.source_path)
    analyzer.analyze()

    if not args.quiet:
        analyzer.print_report()

    if args.output:
        analyzer.export_json(args.output)


if __name__ == '__main__':
    main()
