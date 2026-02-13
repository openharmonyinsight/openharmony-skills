#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI Comparator - Android to HarmonyOS UI Comparison Tool
UI 比对者 - Android 到 HarmonyOS UI 界面比对工具

比对 Android 和 HarmonyOS 应用的 UI 界面，确保视觉和交互一致性。
支持截图比对和布局文件比对两种模式。
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum

class DiffSeverity(Enum):
    """差异严重程度"""
    CRITICAL = "critical"  # 严重差异，影响功能
    MAJOR = "major"        # 较大差异，影响体验
    MINOR = "minor"        # 轻微差异
    INFO = "info"          # 信息提示

@dataclass
class UIComponent:
    """UI 组件定义"""
    name: str
    type: str
    file_path: str
    properties: Dict[str, str] = field(default_factory=dict)
    children: List['UIComponent'] = field(default_factory=list)
    styles: Dict[str, str] = field(default_factory=dict)

@dataclass
class UIDiff:
    """UI 差异"""
    category: str  # layout, style, component, interaction
    description: str
    android_value: str
    harmony_value: str
    severity: DiffSeverity
    suggestion: str = ""
    location: str = ""

@dataclass
class UICompareResult:
    """UI 比对结果"""
    android_components: List[UIComponent]
    harmony_components: List[UIComponent]
    diffs: List[UIDiff]
    matched_count: int
    missing_count: int
    extra_count: int

class UIComparator:
    """UI 比对器"""

    # Android XML 组件映射到 HarmonyOS
    COMPONENT_MAPPING = {
        # 布局
        'LinearLayout': ['Column', 'Row', 'Flex'],
        'FrameLayout': ['Stack'],
        'RelativeLayout': ['RelativeContainer'],
        'ConstraintLayout': ['RelativeContainer'],
        'ScrollView': ['Scroll'],
        'RecyclerView': ['List', 'Grid', 'WaterFlow'],
        'ViewPager': ['Swiper', 'Tabs'],
        'ViewPager2': ['Swiper', 'Tabs'],

        # 基础组件
        'TextView': ['Text'],
        'EditText': ['TextInput', 'TextArea'],
        'Button': ['Button'],
        'ImageView': ['Image'],
        'ImageButton': ['Button'],
        'CheckBox': ['Checkbox'],
        'RadioButton': ['Radio'],
        'Switch': ['Toggle'],
        'ProgressBar': ['Progress', 'LoadingProgress'],
        'SeekBar': ['Slider'],
        'RatingBar': ['Rating'],

        # 列表
        'ListView': ['List'],
        'GridView': ['Grid'],

        # 其他
        'WebView': ['Web'],
        'VideoView': ['Video'],
        'CardView': ['Column'],  # 需要添加 borderRadius 和 shadow
        'TabLayout': ['Tabs'],
        'BottomNavigationView': ['Tabs'],
        'FloatingActionButton': ['Button'],
        'Toolbar': ['Navigation'],
        'SearchView': ['Search'],
        'CalendarView': ['CalendarPicker'],
        'DatePicker': ['DatePicker'],
        'TimePicker': ['TimePicker'],
    }

    # 样式属性映射
    STYLE_MAPPING = {
        # 尺寸
        'layout_width': 'width',
        'layout_height': 'height',
        'layout_margin': 'margin',
        'layout_marginLeft': 'margin.left',
        'layout_marginRight': 'margin.right',
        'layout_marginTop': 'margin.top',
        'layout_marginBottom': 'margin.bottom',
        'padding': 'padding',
        'paddingLeft': 'padding.left',
        'paddingRight': 'padding.right',
        'paddingTop': 'padding.top',
        'paddingBottom': 'padding.bottom',

        # 背景和颜色
        'background': 'backgroundColor',
        'backgroundTint': 'backgroundColor',
        'textColor': 'fontColor',
        'tint': 'fillColor',

        # 文本
        'textSize': 'fontSize',
        'textStyle': 'fontWeight',
        'fontFamily': 'fontFamily',
        'textAlignment': 'textAlign',
        'gravity': 'textAlign',
        'maxLines': 'maxLines',
        'ellipsize': 'textOverflow',

        # 边框
        'cornerRadius': 'borderRadius',

        # 可见性
        'visibility': 'visibility',
        'alpha': 'opacity',
    }

    def __init__(self, android_path: str, harmony_path: str, mode: str = 'layout'):
        self.android_path = Path(android_path)
        self.harmony_path = Path(harmony_path)
        self.mode = mode  # 'layout' or 'screenshot'

    def scan_android_layouts(self) -> List[UIComponent]:
        """扫描 Android 布局文件"""
        components = []

        for xml_file in self.android_path.rglob('*.xml'):
            # 跳过非布局文件
            if 'values' in str(xml_file) or 'drawable' in str(xml_file):
                continue

            try:
                content = xml_file.read_text(encoding='utf-8')
                parsed = self._parse_android_xml(content, str(xml_file))
                components.extend(parsed)
            except Exception as e:
                print(f"Warning: Failed to parse {xml_file}: {e}")

        return components

    def scan_harmony_layouts(self) -> List[UIComponent]:
        """扫描 HarmonyOS 布局文件（ETS）"""
        components = []

        for ets_file in self.harmony_path.rglob('*.ets'):
            try:
                content = ets_file.read_text(encoding='utf-8')
                parsed = self._parse_harmony_ets(content, str(ets_file))
                components.extend(parsed)
            except Exception as e:
                print(f"Warning: Failed to parse {ets_file}: {e}")

        return components

    def _parse_android_xml(self, content: str, file_path: str) -> List[UIComponent]:
        """解析 Android XML 布局"""
        components = []

        # 简单的正则解析（实际项目建议使用 xml.etree）
        # 匹配组件标签
        pattern = r'<(\w+)\s+([^>]*?)(?:/>|>)'

        for match in re.finditer(pattern, content, re.DOTALL):
            tag_name = match.group(1)
            attrs_str = match.group(2)

            # 跳过非 UI 组件
            if tag_name in ['resources', 'manifest', 'application', 'activity',
                           'service', 'receiver', 'provider', 'meta-data',
                           'intent-filter', 'action', 'category', 'data']:
                continue

            # 解析属性
            properties = {}
            styles = {}

            attr_pattern = r'android:(\w+)="([^"]*)"'
            for attr_match in re.finditer(attr_pattern, attrs_str):
                attr_name = attr_match.group(1)
                attr_value = attr_match.group(2)

                if attr_name == 'id':
                    properties['id'] = attr_value.replace('@+id/', '').replace('@id/', '')
                elif attr_name in self.STYLE_MAPPING:
                    styles[self.STYLE_MAPPING[attr_name]] = attr_value
                else:
                    properties[attr_name] = attr_value

            components.append(UIComponent(
                name=properties.get('id', tag_name),
                type=tag_name,
                file_path=file_path,
                properties=properties,
                styles=styles
            ))

        return components

    def _parse_harmony_ets(self, content: str, file_path: str) -> List[UIComponent]:
        """解析 HarmonyOS ETS 布局"""
        components = []

        # 匹配 ArkUI 组件
        # 格式：ComponentName(params) { ... } 或 ComponentName(params).attr()
        component_pattern = r'\b(Column|Row|Stack|Flex|List|Grid|Text|Button|Image|TextInput|' \
                           r'TextArea|Checkbox|Radio|Toggle|Progress|Slider|Rating|Scroll|' \
                           r'Swiper|Tabs|Navigation|Web|Video|Search|DatePicker|TimePicker|' \
                           r'CalendarPicker|LoadingProgress|RelativeContainer|WaterFlow)\s*\('

        for match in re.finditer(component_pattern, content):
            component_type = match.group(1)
            start_pos = match.end()

            # 提取样式链
            styles = {}
            style_pattern = r'\.(\w+)\(([^)]*)\)'

            # 查找组件后的样式调用
            rest_content = content[start_pos:start_pos + 500]  # 限制查找范围
            for style_match in re.finditer(style_pattern, rest_content):
                style_name = style_match.group(1)
                style_value = style_match.group(2).strip('\'"')
                styles[style_name] = style_value

            components.append(UIComponent(
                name=f"{component_type}_{len(components)}",
                type=component_type,
                file_path=file_path,
                styles=styles
            ))

        return components

    def compare(self) -> UICompareResult:
        """执行 UI 比对"""
        android_components = self.scan_android_layouts()
        harmony_components = self.scan_harmony_layouts()

        diffs = []
        matched = 0
        missing = 0

        # 统计 Android 组件类型
        android_types = {}
        for comp in android_components:
            android_types[comp.type] = android_types.get(comp.type, 0) + 1

        # 统计 HarmonyOS 组件类型
        harmony_types = {}
        for comp in harmony_components:
            harmony_types[comp.type] = harmony_types.get(comp.type, 0) + 1

        # 检查组件映射
        for android_type, count in android_types.items():
            expected_harmony_types = self.COMPONENT_MAPPING.get(android_type, [])

            if not expected_harmony_types:
                diffs.append(UIDiff(
                    category='component',
                    description=f'未知的 Android 组件类型: {android_type}',
                    android_value=f'{android_type} x {count}',
                    harmony_value='N/A',
                    severity=DiffSeverity.INFO,
                    suggestion=f'请检查 {android_type} 在 HarmonyOS 中的对应实现'
                ))
                continue

            # 检查 HarmonyOS 中是否有对应组件
            harmony_count = sum(harmony_types.get(t, 0) for t in expected_harmony_types)

            if harmony_count == 0:
                diffs.append(UIDiff(
                    category='component',
                    description=f'缺少对应的 HarmonyOS 组件',
                    android_value=f'{android_type} x {count}',
                    harmony_value=f'期望: {expected_harmony_types}',
                    severity=DiffSeverity.MAJOR if count > 1 else DiffSeverity.MINOR,
                    suggestion=f'请添加 {expected_harmony_types[0]} 组件来替代 {android_type}'
                ))
                missing += count
            elif abs(harmony_count - count) > count * 0.3:  # 差异超过 30%
                diffs.append(UIDiff(
                    category='component',
                    description=f'组件数量差异较大',
                    android_value=f'{android_type} x {count}',
                    harmony_value=f'{expected_harmony_types} x {harmony_count}',
                    severity=DiffSeverity.MINOR,
                    suggestion='请检查是否有遗漏或多余的组件'
                ))
                matched += min(count, harmony_count)
            else:
                matched += count

        # 检查样式差异
        self._compare_styles(android_components, harmony_components, diffs)

        # 计算额外的 HarmonyOS 组件
        android_type_set = set(android_types.keys())
        extra = 0
        for harmony_type, count in harmony_types.items():
            # 检查是否是 Android 组件的映射目标
            is_mapped = any(
                harmony_type in self.COMPONENT_MAPPING.get(at, [])
                for at in android_type_set
            )
            if not is_mapped:
                extra += count

        return UICompareResult(
            android_components=android_components,
            harmony_components=harmony_components,
            diffs=diffs,
            matched_count=matched,
            missing_count=missing,
            extra_count=extra
        )

    def _compare_styles(self, android_comps: List[UIComponent],
                        harmony_comps: List[UIComponent], diffs: List[UIDiff]):
        """比对样式差异"""
        # 收集 Android 中使用的样式
        android_styles = set()
        for comp in android_comps:
            android_styles.update(comp.styles.keys())

        # 收集 HarmonyOS 中使用的样式
        harmony_styles = set()
        for comp in harmony_comps:
            harmony_styles.update(comp.styles.keys())

        # 检查常用样式是否迁移
        important_styles = ['width', 'height', 'backgroundColor', 'fontSize',
                           'fontColor', 'margin', 'padding', 'borderRadius']

        for style in important_styles:
            in_android = any(style in comp.styles or
                            any(s.startswith(style) for s in comp.styles.keys())
                            for comp in android_comps)
            in_harmony = style in harmony_styles

            if in_android and not in_harmony:
                diffs.append(UIDiff(
                    category='style',
                    description=f'样式 {style} 在 HarmonyOS 中未使用',
                    android_value=f'已使用',
                    harmony_value=f'未使用',
                    severity=DiffSeverity.MINOR,
                    suggestion=f'请检查 {style} 样式是否需要迁移'
                ))

    def compare_screenshots(self, android_dir: str, harmony_dir: str) -> List[UIDiff]:
        """比对截图（需要 PIL 库）"""
        diffs = []

        try:
            from PIL import Image
            import hashlib
        except ImportError:
            diffs.append(UIDiff(
                category='screenshot',
                description='截图比对需要安装 Pillow 库',
                android_value='N/A',
                harmony_value='N/A',
                severity=DiffSeverity.INFO,
                suggestion='请运行: pip install Pillow'
            ))
            return diffs

        android_path = Path(android_dir)
        harmony_path = Path(harmony_dir)

        android_images = {f.stem: f for f in android_path.glob('*.png')}
        harmony_images = {f.stem: f for f in harmony_path.glob('*.png')}

        # 匹配同名截图
        for name, android_file in android_images.items():
            if name in harmony_images:
                harmony_file = harmony_images[name]

                try:
                    android_img = Image.open(android_file)
                    harmony_img = Image.open(harmony_file)

                    # 尺寸比对
                    if android_img.size != harmony_img.size:
                        diffs.append(UIDiff(
                            category='screenshot',
                            description=f'截图 {name} 尺寸不一致',
                            android_value=str(android_img.size),
                            harmony_value=str(harmony_img.size),
                            severity=DiffSeverity.MINOR,
                            location=name
                        ))

                    # 简单的像素差异检测
                    if android_img.size == harmony_img.size:
                        diff_pixels = self._count_diff_pixels(android_img, harmony_img)
                        total_pixels = android_img.size[0] * android_img.size[1]
                        diff_ratio = diff_pixels / total_pixels

                        if diff_ratio > 0.1:  # 超过 10% 差异
                            diffs.append(UIDiff(
                                category='screenshot',
                                description=f'截图 {name} 存在明显视觉差异',
                                android_value='原始',
                                harmony_value=f'{diff_ratio*100:.1f}% 差异',
                                severity=DiffSeverity.MAJOR if diff_ratio > 0.3 else DiffSeverity.MINOR,
                                location=name,
                                suggestion='请检查颜色、布局、字体等是否一致'
                            ))

                except Exception as e:
                    diffs.append(UIDiff(
                        category='screenshot',
                        description=f'无法比对截图 {name}: {e}',
                        android_value=str(android_file),
                        harmony_value=str(harmony_file),
                        severity=DiffSeverity.INFO
                    ))
            else:
                diffs.append(UIDiff(
                    category='screenshot',
                    description=f'缺少对应的 HarmonyOS 截图',
                    android_value=name,
                    harmony_value='未找到',
                    severity=DiffSeverity.MINOR,
                    suggestion=f'请添加 {name}.png 截图'
                ))

        return diffs

    def _count_diff_pixels(self, img1, img2) -> int:
        """计算不同的像素数"""
        from PIL import ImageChops
        diff = ImageChops.difference(img1.convert('RGB'), img2.convert('RGB'))
        diff_data = diff.getdata()
        return sum(1 for pixel in diff_data if sum(pixel) > 30)  # 容差

    def generate_report(self, result: UICompareResult) -> str:
        """生成比对报告"""
        report = []
        report.append("=" * 60)
        report.append("UI 界面比对报告")
        report.append("UI Comparison Report")
        report.append("=" * 60)
        report.append("")

        # 概览
        total_android = len(result.android_components)
        total_harmony = len(result.harmony_components)

        report.append("## 概览 Summary")
        report.append(f"- Android 组件总数: {total_android}")
        report.append(f"- HarmonyOS 组件总数: {total_harmony}")
        report.append(f"- 已匹配组件: {result.matched_count}")
        report.append(f"- 缺失组件: {result.missing_count}")
        report.append(f"- 新增组件: {result.extra_count}")
        report.append(f"- 发现差异: {len(result.diffs)}")
        report.append("")

        # 按严重程度分组显示差异
        if result.diffs:
            report.append("## 差异详情")

            for severity in [DiffSeverity.CRITICAL, DiffSeverity.MAJOR,
                            DiffSeverity.MINOR, DiffSeverity.INFO]:
                severity_diffs = [d for d in result.diffs if d.severity == severity]
                if severity_diffs:
                    report.append(f"\n### {severity.value.upper()} ({len(severity_diffs)})")
                    for diff in severity_diffs:
                        report.append(f"\n**[{diff.category}] {diff.description}**")
                        report.append(f"- Android: {diff.android_value}")
                        report.append(f"- HarmonyOS: {diff.harmony_value}")
                        if diff.suggestion:
                            report.append(f"- 建议: {diff.suggestion}")
                        if diff.location:
                            report.append(f"- 位置: {diff.location}")

        # 组件统计
        report.append("\n## 组件类型统计")

        report.append("\n### Android 组件")
        android_type_count = {}
        for comp in result.android_components:
            android_type_count[comp.type] = android_type_count.get(comp.type, 0) + 1
        for comp_type, count in sorted(android_type_count.items(), key=lambda x: -x[1]):
            mapped = self.COMPONENT_MAPPING.get(comp_type, ['?'])
            report.append(f"- {comp_type}: {count} -> {mapped}")

        report.append("\n### HarmonyOS 组件")
        harmony_type_count = {}
        for comp in result.harmony_components:
            harmony_type_count[comp.type] = harmony_type_count.get(comp.type, 0) + 1
        for comp_type, count in sorted(harmony_type_count.items(), key=lambda x: -x[1]):
            report.append(f"- {comp_type}: {count}")

        # 建议
        report.append("\n## 优化建议")

        critical_count = len([d for d in result.diffs if d.severity == DiffSeverity.CRITICAL])
        major_count = len([d for d in result.diffs if d.severity == DiffSeverity.MAJOR])

        if critical_count > 0:
            report.append(f"1. 【紧急】有 {critical_count} 个严重问题需要立即修复")
        if major_count > 0:
            report.append(f"2. 有 {major_count} 个较大差异建议尽快处理")
        if result.missing_count > 0:
            report.append(f"3. 有 {result.missing_count} 个组件需要补充")

        coverage = result.matched_count / total_android * 100 if total_android > 0 else 0
        if coverage >= 90:
            report.append(f"4. UI 覆盖率 {coverage:.1f}%，整体迁移良好")
        elif coverage >= 70:
            report.append(f"4. UI 覆盖率 {coverage:.1f}%，建议继续完善")
        else:
            report.append(f"4. UI 覆盖率 {coverage:.1f}%，需要加快迁移进度")

        return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(
        description='Android to HarmonyOS UI Comparison Tool'
    )
    parser.add_argument('android_path', help='Android UI source (layout dir or screenshots dir)')
    parser.add_argument('harmony_path', help='HarmonyOS UI target (ets dir or screenshots dir)')
    parser.add_argument('--layout', action='store_true', help='Compare layout files (default)')
    parser.add_argument('--screenshot', action='store_true', help='Compare screenshots')
    parser.add_argument('--output', '-o', help='Output report file path')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')

    args = parser.parse_args()

    if not os.path.isdir(args.android_path):
        print(f"Error: Android path not found: {args.android_path}")
        return 1

    if not os.path.isdir(args.harmony_path):
        print(f"Error: HarmonyOS path not found: {args.harmony_path}")
        return 1

    mode = 'screenshot' if args.screenshot else 'layout'

    print(f"Comparing UI ({mode} mode)...")
    print(f"  Android: {args.android_path}")
    print(f"  HarmonyOS: {args.harmony_path}")
    print()

    comparator = UIComparator(args.android_path, args.harmony_path, mode)

    if args.screenshot:
        diffs = comparator.compare_screenshots(args.android_path, args.harmony_path)
        result = UICompareResult(
            android_components=[],
            harmony_components=[],
            diffs=diffs,
            matched_count=0,
            missing_count=0,
            extra_count=0
        )
    else:
        result = comparator.compare()

    if args.json:
        output = {
            'summary': {
                'android_components': len(result.android_components),
                'harmony_components': len(result.harmony_components),
                'matched': result.matched_count,
                'missing': result.missing_count,
                'extra': result.extra_count,
                'diffs': len(result.diffs),
            },
            'diffs': [
                {
                    'category': d.category,
                    'description': d.description,
                    'severity': d.severity.value,
                    'android': d.android_value,
                    'harmony': d.harmony_value,
                    'suggestion': d.suggestion,
                }
                for d in result.diffs
            ]
        }
        report = json.dumps(output, ensure_ascii=False, indent=2)
    else:
        report = comparator.generate_report(result)

    if args.output:
        Path(args.output).write_text(report, encoding='utf-8')
        print(f"Report saved to: {args.output}")
    else:
        print(report)

    return 0

if __name__ == '__main__':
    exit(main())
