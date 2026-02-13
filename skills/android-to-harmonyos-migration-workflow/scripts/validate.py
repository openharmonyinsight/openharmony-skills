#!/usr/bin/env python3
"""
HarmonyOS 代码验证脚本
检查迁移后的代码是否符合规范
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple


class CodeValidator:
    """代码验证器"""

    # 常见的 ArkTS 编译错误模式
    SYNTAX_ERRORS = {
        'super.property': r'\bsuper\.\w+',  # 不应该用 super 访问属性
        'var_without_type': r'\bvar\s+\w+\s*=',  # var 应该有类型注解
        'any_type': r'\bany\b',  # 避免 any 类型
    }

    # API 版本检查
    HIGH_LEVEL_APIS = {
        'window.createWindow',  # API 9+
        'worker.startThread',  # 需要检查版本
    }

    # 不推荐的 API
    DEPRECATED_APIS = {
        'router.getState',
        'router.pushUrl',
        'router.replaceUrl',
        'router.back',
        'router.clear',
    }

    def __init__(self, target_path: str):
        self.target_path = Path(target_path)
        self.issues = []
        self.warnings = []
        self.stats = {
            'files_checked': 0,
            'total_lines': 0,
        }

    def validate(self) -> bool:
        """执行验证"""
        if not self.target_path.exists():
            print(f"错误: 目标路径不存在: {self.target_path}")
            return False

        # 查找所有 .ets 文件
        ets_files = list(self.target_path.rglob('*.ets'))

        print(f"找到 {len(ets_files)} 个 ETS 文件")
        print("=" * 60)

        for file_path in ets_files:
            self._validate_file(file_path)

        self._print_report()
        return len(self.issues) == 0

    def _validate_file(self, file_path: Path):
        """验证单个文件"""
        self.stats['files_checked'] += 1

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                self.stats['total_lines'] += len(lines)

                # 检查各种问题
                self._check_syntax_errors(file_path, content, lines)
                self._check_deprecated_apis(file_path, content)
                self._check_type_safety(file_path, content)
                self._check_best_practices(file_path, content)

        except Exception as e:
            self.issues.append({
                'file': str(file_path),
                'line': 0,
                'type': 'ERROR',
                'message': f"无法读取文件: {e}"
            })

    def _check_syntax_errors(self, file_path: Path, content: str, lines: List[str]):
        """检查语法错误"""
        # 检查 super.property 模式
        for match in re.finditer(r'\bsuper\.(\w+)', content):
            line_num = content[:match.start()].count('\n') + 1
            self.issues.append({
                'file': str(file_path.relative_to(self.target_path)),
                'line': line_num,
                'type': 'ERROR',
                'message': f"不应使用 super.{match.group(1)} 访问属性，应使用 this.{match.group(1)}"
            })

        # 检查 var 声明
        for match in re.finditer(r'\bvar\s+(\w+)\s*=', content):
            line_num = content[:match.start()].count('\n') + 1
            self.warnings.append({
                'file': str(file_path.relative_to(self.target_path)),
                'line': line_num,
                'type': 'WARNING',
                'message': f"建议使用 let 替代 var，或添加类型注解: var {match.group(1)}: type ="
            })

    def _check_deprecated_apis(self, file_path: Path, content: str):
        """检查不推荐的 API"""
        for api in self.DEPRECATED_APIS:
            if api in content:
                # 找到出现位置
                start = 0
                while True:
                    pos = content.find(api, start)
                    if pos == -1:
                        break
                    line_num = content[:pos].count('\n') + 1
                    self.warnings.append({
                        'file': str(file_path.relative_to(self.target_path)),
                        'line': line_num,
                        'type': 'WARNING',
                        'message': f"使用了已弃用的 API: {api}"
                    })
                    start = pos + 1

    def _check_type_safety(self, file_path: Path, content: str):
        """检查类型安全"""
        # 检查 any 类型
        for match in re.finditer(r'\bany\b', content):
            # 排除注释中的 any
            line_start = content.rfind('\n', 0, match.start()) + 1
            line_end = content.find('\n', match.start())
            if line_end == -1:
                line_end = len(content)
            line = content[line_start:line_end]
            if '//' in line and line.index('//') < content[:match.start()].count('\n') - line_start:
                continue

            line_num = content[:match.start()].count('\n') + 1
            self.warnings.append({
                'file': str(file_path.relative_to(self.target_path)),
                'line': line_num,
                'type': 'WARNING',
                'message': "避免使用 any 类型，应指定具体类型"
            })

        # 检查函数参数和返回值类型
        for match in re.finditer(r'fn\s+(\w+)\s*\([^)]*\)\s*(?!:)', content):
            line_num = content[:match.start()].count('\n') + 1
            self.warnings.append({
                'file': str(file_path.relative_to(self.target_path)),
                'line': line_num,
                'type': 'INFO',
                'message': f"函数 {match.group(1)} 建议添加返回类型注解"
            })

    def _check_best_practices(self, file_path: Path, content: str):
        """检查最佳实践"""
        # 检查是否有 @Component 但没有 export
        if '@Component' in content and 'export' not in content[:content.find('@Component')]:
            self.warnings.append({
                'file': str(file_path.relative_to(self.target_path)),
                'line': 1,
                'type': 'INFO',
                'message': "Component 建议添加 export 导出"
            })

        # 检查是否有 @Entry 但没有 @Component
        if '@Entry' in content and '@Component' not in content[:content.find('@Entry') + 50]:
            line_num = content[:content.find('@Entry')].count('\n') + 1
            self.issues.append({
                'file': str(file_path.relative_to(self.target_path)),
                'line': line_num,
                'type': 'ERROR',
                'message': "@Entry 必须与 @Component 一起使用"
            })

    def _print_report(self):
        """打印验证报告"""
        print(f"\n验证完成:")
        print(f"  检查文件: {self.stats['files_checked']}")
        print(f"  代码行数: {self.stats['total_lines']}")
        print(f"  错误: {len(self.issues)}")
        print(f"  警告: {len(self.warnings)}")
        print()

        # 按文件分组显示错误
        if self.issues:
            print("=" * 60)
            print("错误:")
            print("=" * 60)
            for issue in self.issues[:20]:  # 只显示前20个
                print(f"{issue['file']}:{issue['line']} - {issue['message']}")
            if len(self.issues) > 20:
                print(f"... 还有 {len(self.issues) - 20} 个错误")

        # 按文件分组显示警告
        if self.warnings:
            print("\n" + "=" * 60)
            print("警告:")
            print("=" * 60)
            for warning in self.warnings[:20]:  # 只显示前20个
                print(f"{warning['file']}:{warning['line']} - {warning['message']}")
            if len(self.warnings) > 20:
                print(f"... 还有 {len(self.warnings) - 20} 个警告")

        print("\n" + "=" * 60)

        if len(self.issues) == 0 and len(self.warnings) == 0:
            print("验证通过！代码符合规范。")
        elif len(self.issues) == 0:
            print(f"没有错误，但有 {len(self.warnings)} 个警告。")
        else:
            print(f"发现 {len(self.issues)} 个错误需要修复。")

        print("=" * 60)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='验证 HarmonyOS 代码')
    parser.add_argument('target_path', help='目标代码路径')
    parser.add_argument('--strict', '-s', action='store_true',
                       help='严格模式（警告也视为错误）')

    args = parser.parse_args()

    validator = CodeValidator(args.target_path)
    success = validator.validate()

    exit(0 if success else 1)


if __name__ == '__main__':
    main()
