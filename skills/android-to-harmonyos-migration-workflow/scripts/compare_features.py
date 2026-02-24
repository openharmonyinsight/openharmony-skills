#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Feature Comparator - Android to HarmonyOS Migration Feature Comparison Tool
功能比对者 - Android 到 HarmonyOS 迁移功能比对工具

比对 Android 源码与迁移后的 HarmonyOS 代码，找出遗漏的功能。
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum

class Priority(Enum):
    """功能优先级"""
    CRITICAL = "critical"  # 核心功能，必须迁移
    HIGH = "high"          # 重要功能，应该迁移
    MEDIUM = "medium"      # 一般功能，建议迁移
    LOW = "low"            # 次要功能，可选迁移

@dataclass
class AndroidFeature:
    """Android 功能定义"""
    name: str
    type: str  # Activity, Fragment, Service, BroadcastReceiver, ViewModel, Repository, etc.
    file_path: str
    methods: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    api_calls: List[str] = field(default_factory=list)
    priority: Priority = Priority.MEDIUM

@dataclass
class HarmonyFeature:
    """HarmonyOS 功能定义"""
    name: str
    type: str  # Page, Component, UIAbility, ServiceExtensionAbility, etc.
    file_path: str
    methods: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)

@dataclass
class FeatureCompareResult:
    """功能比对结果"""
    android_features: List[AndroidFeature]
    harmony_features: List[HarmonyFeature]
    migrated: List[Tuple[AndroidFeature, HarmonyFeature]]
    missing: List[AndroidFeature]
    partial: List[Tuple[AndroidFeature, HarmonyFeature, List[str]]]  # (android, harmony, missing_methods)
    extra: List[HarmonyFeature]  # HarmonyOS 中新增的功能

class FeatureComparator:
    """功能比对器"""

    # Android 组件模式
    ANDROID_PATTERNS = {
        'Activity': r'class\s+(\w+)\s*:\s*\w*Activity',
        'Fragment': r'class\s+(\w+)\s*:\s*\w*Fragment',
        'Service': r'class\s+(\w+)\s*:\s*\w*Service',
        'BroadcastReceiver': r'class\s+(\w+)\s*:\s*BroadcastReceiver',
        'ViewModel': r'class\s+(\w+)\s*:\s*\w*ViewModel',
        'Repository': r'class\s+(\w+Repository)',
        'Adapter': r'class\s+(\w+Adapter)',
        'Dialog': r'class\s+(\w+Dialog)',
    }

    # HarmonyOS 组件模式
    HARMONY_PATTERNS = {
        'Page': r'@Entry\s*\n?\s*@Component\s*\n?\s*(?:export\s+)?struct\s+(\w+)',
        'Component': r'@Component\s*\n?\s*(?:export\s+)?struct\s+(\w+)',
        'UIAbility': r'class\s+(\w+)\s+extends\s+UIAbility',
        'ServiceExtensionAbility': r'class\s+(\w+)\s+extends\s+ServiceExtensionAbility',
        'ViewModelClass': r'@Observed\s*\n?\s*(?:export\s+)?class\s+(\w+)',
    }

    # Android API 调用模式
    ANDROID_API_PATTERNS = [
        r'SharedPreferences',
        r'SQLiteDatabase',
        r'Room\.',
        r'Retrofit',
        r'OkHttp',
        r'Glide\.',
        r'Picasso\.',
        r'Intent\(',
        r'startActivity',
        r'startService',
        r'sendBroadcast',
        r'ContentResolver',
        r'MediaStore',
        r'Camera\.',
        r'Location',
        r'Notification',
        r'AlarmManager',
        r'WorkManager',
        r'Firebase',
    ]

    def __init__(self, android_path: str, harmony_path: str):
        self.android_path = Path(android_path)
        self.harmony_path = Path(harmony_path)

    def scan_android_features(self) -> List[AndroidFeature]:
        """扫描 Android 源码中的功能"""
        features = []

        for ext in ['*.java', '*.kt']:
            for file_path in self.android_path.rglob(ext):
                try:
                    content = file_path.read_text(encoding='utf-8')
                    features.extend(self._extract_android_features(content, str(file_path)))
                except Exception as e:
                    print(f"Warning: Failed to read {file_path}: {e}")

        return features

    def scan_harmony_features(self) -> List[HarmonyFeature]:
        """扫描 HarmonyOS 源码中的功能"""
        features = []

        for ext in ['*.ets', '*.ts']:
            for file_path in self.harmony_path.rglob(ext):
                try:
                    content = file_path.read_text(encoding='utf-8')
                    features.extend(self._extract_harmony_features(content, str(file_path)))
                except Exception as e:
                    print(f"Warning: Failed to read {file_path}: {e}")

        return features

    def _extract_android_features(self, content: str, file_path: str) -> List[AndroidFeature]:
        """从 Android 代码中提取功能"""
        features = []

        for feature_type, pattern in self.ANDROID_PATTERNS.items():
            matches = re.findall(pattern, content)
            for name in matches:
                methods = self._extract_methods(content, name)
                api_calls = self._extract_api_calls(content)
                priority = self._determine_priority(feature_type, methods)

                features.append(AndroidFeature(
                    name=name,
                    type=feature_type,
                    file_path=file_path,
                    methods=methods,
                    api_calls=api_calls,
                    priority=priority
                ))

        return features

    def _extract_harmony_features(self, content: str, file_path: str) -> List[HarmonyFeature]:
        """从 HarmonyOS 代码中提取功能"""
        features = []

        for feature_type, pattern in self.HARMONY_PATTERNS.items():
            matches = re.findall(pattern, content)
            for name in matches:
                methods = self._extract_methods(content, name)

                features.append(HarmonyFeature(
                    name=name,
                    type=feature_type,
                    file_path=file_path,
                    methods=methods
                ))

        return features

    def _extract_methods(self, content: str, class_name: str) -> List[str]:
        """提取类中的方法"""
        # 匹配函数/方法定义
        patterns = [
            rf'fun\s+(\w+)\s*\(',  # Kotlin
            rf'(?:public|private|protected)?\s+\w+\s+(\w+)\s*\(',  # Java
            rf'(\w+)\s*\([^)]*\)\s*(?::\s*\w+)?\s*\{{',  # TypeScript/ArkTS
        ]

        methods = set()
        for pattern in patterns:
            matches = re.findall(pattern, content)
            methods.update(matches)

        # 过滤掉构造函数和常见的 getter/setter
        filtered = [m for m in methods if not m.startswith(('get', 'set', 'is')) and m != class_name]
        return list(filtered)[:20]  # 限制数量

    def _extract_api_calls(self, content: str) -> List[str]:
        """提取 API 调用"""
        calls = []
        for pattern in self.ANDROID_API_PATTERNS:
            if re.search(pattern, content):
                calls.append(pattern.replace('\\', '').replace('.', '').replace('(', ''))
        return calls

    def _determine_priority(self, feature_type: str, methods: List[str]) -> Priority:
        """确定功能优先级"""
        if feature_type in ['Activity', 'Fragment']:
            return Priority.CRITICAL
        elif feature_type in ['Service', 'ViewModel']:
            return Priority.HIGH
        elif feature_type in ['Repository', 'Adapter']:
            return Priority.MEDIUM
        else:
            return Priority.LOW

    def compare(self) -> FeatureCompareResult:
        """执行功能比对"""
        android_features = self.scan_android_features()
        harmony_features = self.scan_harmony_features()

        migrated = []
        missing = []
        partial = []
        matched_harmony = set()

        for android_feature in android_features:
            match = self._find_matching_harmony_feature(android_feature, harmony_features)

            if match:
                matched_harmony.add(match.name)
                missing_methods = self._find_missing_methods(android_feature, match)

                if missing_methods:
                    partial.append((android_feature, match, missing_methods))
                else:
                    migrated.append((android_feature, match))
            else:
                missing.append(android_feature)

        # 找出 HarmonyOS 中新增的功能
        extra = [f for f in harmony_features if f.name not in matched_harmony]

        return FeatureCompareResult(
            android_features=android_features,
            harmony_features=harmony_features,
            migrated=migrated,
            missing=missing,
            partial=partial,
            extra=extra
        )

    def _find_matching_harmony_feature(self, android: AndroidFeature,
                                        harmony_list: List[HarmonyFeature]) -> HarmonyFeature:
        """查找匹配的 HarmonyOS 功能"""
        # 名称匹配规则
        android_name = android.name.lower()

        for harmony in harmony_list:
            harmony_name = harmony.name.lower()

            # 精确匹配
            if android_name == harmony_name:
                return harmony

            # 去除后缀后匹配 (e.g., MainActivity -> Main, MainPage -> Main)
            android_base = re.sub(r'(activity|fragment|dialog|adapter)$', '', android_name)
            harmony_base = re.sub(r'(page|component|view)$', '', harmony_name)

            if android_base and harmony_base and android_base == harmony_base:
                return harmony

            # 相似度匹配
            if self._name_similarity(android_name, harmony_name) > 0.7:
                return harmony

        return None

    def _name_similarity(self, name1: str, name2: str) -> float:
        """计算名称相似度"""
        if not name1 or not name2:
            return 0.0

        # 简单的字符重叠率
        set1, set2 = set(name1), set(name2)
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0.0

    def _find_missing_methods(self, android: AndroidFeature,
                              harmony: HarmonyFeature) -> List[str]:
        """查找遗漏的方法"""
        android_methods = set(m.lower() for m in android.methods)
        harmony_methods = set(m.lower() for m in harmony.methods)

        missing = android_methods - harmony_methods
        return list(missing)

    def generate_report(self, result: FeatureCompareResult) -> str:
        """生成比对报告"""
        total = len(result.android_features)
        migrated_count = len(result.migrated)
        partial_count = len(result.partial)
        missing_count = len(result.missing)

        coverage = (migrated_count + partial_count * 0.5) / total * 100 if total > 0 else 0

        report = []
        report.append("=" * 60)
        report.append("功能迁移比对报告")
        report.append("Feature Migration Comparison Report")
        report.append("=" * 60)
        report.append("")

        # 概览
        report.append("## 概览 Summary")
        report.append(f"- Android 功能总数: {total}")
        report.append(f"- 已完整迁移: {migrated_count}")
        report.append(f"- 部分迁移: {partial_count}")
        report.append(f"- 未迁移: {missing_count}")
        report.append(f"- HarmonyOS 新增: {len(result.extra)}")
        report.append(f"- **功能覆盖率: {coverage:.1f}%**")
        report.append("")

        # 遗漏功能 - 按优先级分组
        if result.missing:
            report.append("## 遗漏功能清单 (按优先级)")

            for priority in [Priority.CRITICAL, Priority.HIGH, Priority.MEDIUM, Priority.LOW]:
                priority_missing = [f for f in result.missing if f.priority == priority]
                if priority_missing:
                    report.append(f"\n### {priority.value.upper()} ({len(priority_missing)})")
                    for feature in priority_missing:
                        report.append(f"- [{feature.type}] {feature.name}")
                        report.append(f"  文件: {feature.file_path}")
                        if feature.methods:
                            report.append(f"  关键方法: {', '.join(feature.methods[:5])}")
                        if feature.api_calls:
                            report.append(f"  使用的API: {', '.join(feature.api_calls[:5])}")
            report.append("")

        # 部分迁移
        if result.partial:
            report.append("## 部分迁移功能 (需补充)")
            for android, harmony, missing_methods in result.partial:
                report.append(f"\n### {android.name} -> {harmony.name}")
                report.append(f"- Android: {android.file_path}")
                report.append(f"- HarmonyOS: {harmony.file_path}")
                report.append(f"- 遗漏方法: {', '.join(missing_methods[:10])}")
            report.append("")

        # 已迁移功能
        if result.migrated:
            report.append("## 已完整迁移功能")
            for android, harmony in result.migrated[:20]:  # 限制显示数量
                report.append(f"- {android.name} ({android.type}) -> {harmony.name} ({harmony.type})")
            if len(result.migrated) > 20:
                report.append(f"  ... 及其他 {len(result.migrated) - 20} 个功能")
            report.append("")

        # HarmonyOS 新增功能
        if result.extra:
            report.append("## HarmonyOS 新增功能")
            for feature in result.extra[:10]:
                report.append(f"- [{feature.type}] {feature.name}")
            if len(result.extra) > 10:
                report.append(f"  ... 及其他 {len(result.extra) - 10} 个功能")
            report.append("")

        # 建议
        report.append("## 迁移建议")
        if missing_count > 0:
            critical_missing = [f for f in result.missing if f.priority == Priority.CRITICAL]
            if critical_missing:
                report.append(f"1. 【紧急】请优先迁移 {len(critical_missing)} 个核心功能")
            report.append(f"2. 共有 {missing_count} 个功能需要迁移")
        if partial_count > 0:
            report.append(f"3. 有 {partial_count} 个功能需要补充完整")
        if coverage >= 90:
            report.append("4. 功能覆盖率良好，请进行功能测试验证")
        elif coverage >= 70:
            report.append("4. 功能覆盖率一般，建议继续完善迁移")
        else:
            report.append("4. 功能覆盖率较低，请加快迁移进度")

        return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(
        description='Android to HarmonyOS Feature Comparison Tool'
    )
    parser.add_argument('android_source', help='Android source code directory')
    parser.add_argument('harmony_target', help='HarmonyOS target code directory')
    parser.add_argument('--output', '-o', help='Output report file path')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')

    args = parser.parse_args()

    if not os.path.isdir(args.android_source):
        print(f"Error: Android source directory not found: {args.android_source}")
        return 1

    if not os.path.isdir(args.harmony_target):
        print(f"Error: HarmonyOS target directory not found: {args.harmony_target}")
        return 1

    print(f"Comparing features...")
    print(f"  Android source: {args.android_source}")
    print(f"  HarmonyOS target: {args.harmony_target}")
    print()

    comparator = FeatureComparator(args.android_source, args.harmony_target)
    result = comparator.compare()

    if args.json:
        # JSON 输出
        output = {
            'summary': {
                'android_total': len(result.android_features),
                'harmony_total': len(result.harmony_features),
                'migrated': len(result.migrated),
                'partial': len(result.partial),
                'missing': len(result.missing),
                'extra': len(result.extra),
            },
            'missing': [{'name': f.name, 'type': f.type, 'priority': f.priority.value}
                       for f in result.missing],
            'partial': [{'android': a.name, 'harmony': h.name, 'missing_methods': m}
                       for a, h, m in result.partial],
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
