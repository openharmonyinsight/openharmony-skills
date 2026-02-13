#!/usr/bin/env python3
"""
Android 到 HarmonyOS 代码迁移辅助脚本
提供代码转换指导和模式匹配
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional


class CodeMigrator:
    """代码迁移器"""

    # 导入语句映射
    IMPORT_REPLACEMENTS = {
        r'import android\.app\.Activity': '// Activity 转换为 @Entry @Component Page',
        r'import android\.app\.Fragment': '// Fragment 转换为 @Component',
        r'import android\.widget\.': '// 使用 ArkUI 组件替代',
        r'import androidx\.recyclerview\.': '// 使用 List + LazyForEach 替代',
        r'import androidx\.room\.': '// 使用 RelationalDB 替代',
        r'import android\.content\.Context': '// import { common } from \'@kit.AbilityKit\'',
        r'import android\.os\.Bundle': '// 通过路由参数传递',
        r'import android\.util\.Log': '// import { hilog } from \'@kit.PerformanceAnalysisKit\'',
        r'import kotlinx\.coroutines\.*': '// 使用 async/await 替代',
        r'import androidx\.lifecycle\.*': '// 使用 @Observed + @ObjectLink',
    }

    # 类型映射
    TYPE_REPLACEMENTS = {
        r'\bActivity\b': 'Page',
        r'\bFragment\b': 'Component',
        r'\bContext\b': 'UIAbilityContext',
        r'\bBundle\b': 'Record<string, Object>',
        r'\bArrayList\b': 'Array',
        r'\bHashMap\b': 'Map',
        r'\bString\?\b': 'string | null',
        r'\bInt\b': 'number',
        r'\bLong\b': 'number',
        r'\bDouble\b': 'number',
        r'\bFloat\b': 'number',
        r'\bBoolean\b': 'boolean',
    }

    # 函数映射
    FUNCTION_REPLACEMENTS = {
        r'\blog\.([diew])\(': r'hilog.\1(DOMAIN, \'TAG\', ',
        r'\bfindViewById\(': '// 不需要，直接使用状态变量',
        r'\bstartActivity\(': '// router.pushUrl()',
        r'\bfinish\(': '// router.back()',
        r'\bsetText\(': '// 使用状态变量赋值',
        r'\bgetText\(\)': '// 直接读取状态变量',
        r'\bsetOnClickListener\s*\{': '.onClick(() => {',
    }

    def __init__(self, source_file: str, target_file: str, mode: str = 'auto'):
        self.source_file = Path(source_file)
        self.target_file = Path(target_file)
        self.mode = mode
        self.source_content = ''
        self.target_content = []

    def migrate(self) -> bool:
        """执行迁移"""
        if not self.source_file.exists():
            print(f"错误: 源文件不存在: {self.source_file}")
            return False

        # 读取源文件
        with open(self.source_file, 'r', encoding='utf-8', errors='ignore') as f:
            self.source_content = f.read()

        # 分析文件类型
        file_type = self._detect_file_type()

        # 根据文件类型执行转换
        if file_type == 'Activity':
            self._migrate_activity()
        elif file_type == 'Fragment':
            self._migrate_fragment()
        elif file_type == 'Adapter':
            self._migrate_adapter()
        elif file_type == 'ViewModel':
            self._migrate_viewmodel()
        elif file_type == 'Data':
            self._migrate_data_class()
        else:
            self._migrate_generic()

        # 写入目标文件
        self.target_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.target_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.target_content))

        print(f"迁移完成: {self.source_file} -> {self.target_file}")
        return True

    def _detect_file_type(self) -> str:
        """检测文件类型"""
        content = self.source_content

        if re.search(r'class\s+\w*Activity\s*:', content):
            return 'Activity'
        elif re.search(r'class\s+\w*Fragment\s*:', content):
            return 'Fragment'
        elif re.search(r'class\s+\w*Adapter\s*:', content):
            return 'Adapter'
        elif re.search(r'class\s+\w*ViewModel\s*:', content):
            return 'ViewModel'
        elif re.search(r'\bdata\s+class\b', content):
            return 'Data'
        else:
            return 'Generic'

    def _migrate_activity(self):
        """迁移 Activity"""
        # 添加文件头
        self.target_content.append('/**')
        self.target_content.append(f' * 从 {self.source_file.name} 迁移')
        self.target_content.append(' * TODO: 完善迁移实现')
        self.target_content.append(' */')
        self.target_content.append('')
        self.target_content.append("import router from '@ohos.router';")

        # 转换类定义
        class_match = re.search(r'class\s+(\w+Activity)\s*:\s*\w+Activity', self.source_content)
        if class_match:
            class_name = class_match.group(1).replace('Activity', 'Page')
            self.target_content.append('')
            self.target_content.append('@Entry')
            self.target_content.append(f'@Component')
            self.target_content.append(f'export struct {class_name} {{')

            # 添加状态变量
            self.target_content.append('  // TODO: 添加状态变量')
            self.target_content.append('  @State private message: string = "Hello World"')
            self.target_content.append('')
            self.target_content.append('  build() {')
            self.target_content.append('    Column() {')
            self.target_content.append('      // TODO: 构建 UI')
            self.target_content.append('      Text(this.message)')
            self.target_content.append('    }')
            self.target_content.append('  }')
            self.target_content.append('')
            self.target_content.append('  async aboutToAppear() {')
            self.target_content.append('    // TODO: 初始化逻辑 (相当于 onCreate)')
            self.target_content.append('  }')
            self.target_content.append('}')
        else:
            self._migrate_generic()

    def _migrate_fragment(self):
        """迁移 Fragment"""
        self.target_content.append('/**')
        self.target_content.append(f' * 从 {self.source_file.name} (Fragment) 迁移')
        self.target_content.append(' */')
        self.target_content.append('')
        self.target_content.append('@Component')
        self.target_content.append('export struct MyComponent {')
        self.target_content.append('  // TODO: 添加 @Prop 装饰的属性')
        self.target_content.append('  @Prop title: string = \'\'')
        self.target_content.append('')
        self.target_content.append('  build() {')
        self.target_content.append('    Column() {')
        self.target_content.append('      // TODO: 构建 UI')
        self.target_content.append('    }')
        self.target_content.append('  }')
        self.target_content.append('}')

    def _migrate_adapter(self):
        """迁移 Adapter"""
        self.target_content.append('/**')
        self.target_content.append(f' * 从 {self.source_file.name} (Adapter) 迁移')
        self.target_content.append(' */')
        self.target_content.append('')
        self.target_content.append('// Adapter 转换为数据源 + LazyForEach')
        self.target_content.append('')
        self.target_content.append('class MyDataSource extends BasicDataSource {')
        self.target_content.append('  private data: Item[] = []')
        self.target_content.append('')
        self.target_content.append('  constructor(data: Item[]) {')
        self.target_content.append('    super()')
        self.target_content.append('    this.data = data')
        self.target_content.append('  }')
        self.target_content.append('')
        self.target_content.append('  totalCount(): number {')
        self.target_content.append('    return this.data.length')
        self.target_content.append('  }')
        self.target_content.append('')
        self.target_content.append('  getData(index: number): Item {')
        self.target_content.append('    return this.data[index]')
        self.target_content.append('  }')
        self.target_content.append('}')
        self.target_content.append('')
        self.target_content.append('// 使用方式:')
        self.target_content.append('// LazyForEach(new DataSource(items), (item: Item) => { ... })')

    def _migrate_viewmodel(self):
        """迁移 ViewModel"""
        self.target_content.append('/**')
        self.target_content.append(f' * 从 {self.source_file.name} (ViewModel) 迁移')
        self.target_content.append(' */')
        self.target_content.append('')
        self.target_content.append('import { Observed, Track } from \'@kit.ArkUI\'')
        self.target_content.append('')
        self.target_content.append('@Observed')
        self.target_content.append('export class MyViewModel {')
        self.target_content.append('  @Track data: string = \'\'')
        self.target_content.append('')
        self.target_content.append('  setData(value: string): void {')
        self.target_content.append('    this.data = value')
        self.target_content.append('  }')
        self.target_content.append('}')

    def _migrate_data_class(self):
        """迁移数据类"""
        self.target_content.append('/**')
        self.target_content.append(f' * 从 {self.source_file.name} (data class) 迁移')
        self.target_content.append(' */')
        self.target_content.append('')
        self.target_content.append('export class MyData {')
        self.target_content.append('  id: number = 0')
        self.target_content.append('  name: string = \'\'')
        self.target_content.append('')
        self.target_content.append('  constructor(data?: Partial<MyData>) {')
        self.target_content.append('    if (data) {')
        self.target_content.append('      this.id = data.id ?? 0')
        self.target_content.append('      this.name = data.name ?? \'\'')
        self.target_content.append('    }')
        self.target_content.append('  }')
        self.target_content.append('}')
        self.target_content.append('')
        self.target_content.append('export function createMyData(data: Partial<MyData>): MyData {')
        self.target_content.append('  return new MyData(data)')
        self.target_content.append('}')

    def _migrate_generic(self):
        """通用迁移"""
        self.target_content.append('/**')
        self.target_content.append(f' * 从 {self.source_file.name} 迁移')
        self.target_content.append(' * TODO: 手动完成迁移')
        self.target_content.append(' */')
        self.target_content.append('')
        self.target_content.append('// 迁移提示:')
        self.target_content.append('// 1. 检查导入语句并替换为 HarmonyOS API')
        self.target_content.append('// 2. 转换类型定义')
        self.target_content.append('// 3. 转换异步操作为 async/await')
        self.target_content.append('// 4. 转换集合操作')
        self.target_content.append('')
        self.target_content.append(self.source_content)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Android 到 HarmonyOS 代码迁移')
    parser.add_argument('source', help='源文件路径')
    parser.add_argument('target', help='目标文件路径')
    parser.add_argument('--mode', '-m', default='auto',
                       choices=['auto', 'activity', 'fragment', 'adapter', 'viewmodel', 'data', 'generic'],
                       help='迁移模式')

    args = parser.parse_args()

    migrator = CodeMigrator(args.source, args.target, args.mode)
    success = migrator.migrate()

    if success:
        print(f"\n请检查生成的文件并完善实现: {args.target}")
    else:
        exit(1)


if __name__ == '__main__':
    main()
