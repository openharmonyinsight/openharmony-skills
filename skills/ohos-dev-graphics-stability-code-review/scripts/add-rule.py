#!/usr/bin/env python3
"""
add-rule.py - 稳定性规则脚手架工具

用法:
    python add-rule.py --rule-id StabilityCodeReview_ExceptionHandling_008
                       --name "空catch块检测"
                       --category "异常处理"
                       --severity "HIGH"
                       --description "检测空的catch块"

自动完成:
    1. 创建参考文档 references/分类/StabilityCodeReview_xxx.md
    2. 更新 config/rules.yaml 配置
"""

import argparse
import re
import sys
from pathlib import Path
from string import Template

try:
    import yaml
except ImportError:
    yaml = None


CATEGORY_MAP = {
    "异常处理": "ExceptionHandling",
    "并发稳定性": "ConcurrencyStability",
    "资源管理": "ResourceManagement",
    "边界条件": "BoundaryCondition",
    "图形稳定性": "GraphicsStability",
}


def validate_rule_id(rule_id: str) -> bool:
    pattern = r"^StabilityCodeReview_([A-Za-z]+)_([0-9]+)$"
    return bool(re.match(pattern, rule_id))


def create_reference_doc(rule_id: str, rule_name: str, category: str, severity: str, description: str) -> str:
    template_str = '''---
rule_id: "$rule_id"
name: "$rule_name"
category: "$category"
severity: "$severity"
language: ["cpp", "c++"]
author: "OH-Department7 Stability Team"
---

# $rule_name

## 问题描述

$description

## 检测示例

### ❌ 问题代码

```cpp
// 场景1：TODO: 添加具体问题描述
// TODO: 添加问题代码示例

// 场景2：TODO: 添加具体问题描述
// TODO: 添加问题代码示例

// 场景3：TODO: 添加具体问题描述
// TODO: 添加问题代码示例

// 场景4：TODO: 添加具体问题描述
// TODO: 添加问题代码示例

// 场景5：TODO: 添加具体问题描述
// TODO: 添加问题代码示例

// 建议：提供5-10个典型错误场景，覆盖常见变体和实际代码模式
```

### ✅ 修复方案

```cpp
// 修复场景1：TODO: 添加修复方法说明
// TODO: 添加修复后的代码

// 修复场景2：TODO: 添加修复方法说明
// TODO: 添加修复后的代码

// 修复场景3：TODO: 添加修复方法说明
// TODO: 添加修复后的代码

// 修复场景4：TODO: 添加修复方法说明
// TODO: 添加修复后的代码

// 修复场景5：TODO: 添加修复方法说明
// TODO: 添加修复后的代码

// 建议：提供5-10个修复方案，包括最佳实践、RAII模式、实际代码中的标准写法
```

## 检测范围

检查以下API/函数/模式/场景：

1. TODO: 添加检测目标1
2. TODO: 添加检测目标2
3. TODO: 添加检测目标3
4. TODO: 添加检测目标4
5. TODO: 添加检测目标5

## 检测要点

1. TODO: 添加检测步骤1：如何识别目标
2. TODO: 添加检测步骤2：如何检查问题
3. TODO: 添加检测步骤3：如何判断风险
4. TODO: 添加检测步骤4：如何排除误报
5. TODO: 添加检测步骤5：特殊情况处理

### TODO: 可选扩展说明章节

根据规则特点添加以下可选章节：

#### 最佳实践说明

TODO: 说明该类问题的最佳实践模式

- **推荐方式1**：TODO: 说明适用场景和示例
- **推荐方式2**：TODO: 说明适用场景和示例

#### 实际代码参考

TODO: 引用实际项目中的具体函数、常量、模式

- **实际常量值**：TODO: 添加实际项目常量（如MAX_ITEM_COUNT = 1000）
- **实际函数名**：TODO: 添加实际项目函数名
- **实际日志函数**：TODO: 添加实际项目日志函数（如ROSEN_LOGE）

#### 特殊技术说明

TODO: 针对复杂技术点提供详细说明

#### 分类处理策略

TODO: 针对不同场景提供不同的处理方式

- **场景A**：TODO: 处理方式1
- **场景B**：TODO: 处理方式2

## 风险流分析（RiskFlow）

- **RISK_SOURCE**: TODO: 添加稳定性风险来源描述（具体到代码元素）
- **RISK_TYPE**: TODO: 添加具体的稳定性风险类型（如空指针解引用、UAF、数据竞争等）
- **RISK_PATH**: TODO: 添加风险传播的完整路径（从来源到影响点）
- **IMPACT_POINT**: TODO: 添加最终影响系统稳定性的点（如崩溃、资源耗尽等）

## 影响分析（ImpactAnalysis）

- **Trigger**: TODO: 添加触发条件（具体场景描述）
- **Propagation**: TODO: 添加风险传播方式（具体机制）
- **Consequence**: TODO: 添加稳定性后果（具体表现）
- **Mitigation**: TODO: 添加缓解建议（具体修复方案）

## 误报排除

| 场景 | 识别特征 | 处理方式 |
|------|----------|----------|
| NOPROTECT标记 | 有 // NOPROTECT 注释 | 不报 |
| 已有安全防护 | TODO: 具体识别方法 | 不报 |
| 使用最佳实践 | TODO: 具体识别方法 | 不报 |
| 第三方库 | 位于 third_party 目录 | 白名单排除 |
| 测试代码 | 位于 test 目录或 _test.cpp 文件 | 自动跳过 |
| TODO: 其他场景 | TODO: 识别方法 | TODO: 处理方式 |

## 测试用例

### 触发用例（应该报）

```cpp
// test_${rule_id}_trigger.cpp

// 触发用例1：TODO: 添加触发场景描述
void trigger_bad_1()
{
    // TODO: 添加触发场景1的代码
}

// 触发用例2：TODO: 添加触发场景描述
void trigger_bad_2()
{
    // TODO: 添加触发场景2的代码
}

// 触发用例3：TODO: 添加触发场景描述
void trigger_bad_3()
{
    // TODO: 添加触发场景3的代码
}

// 触发用例4：TODO: 添加触发场景描述
void trigger_bad_4()
{
    // TODO: 添加触发场景4的代码
}

// 触发用例5：TODO: 添加触发场景描述
void trigger_bad_5()
{
    // TODO: 添加触发场景5的代码
}

// 建议：提供5-10个触发用例，覆盖典型错误模式和边界情况
```

### 安全用例（不应该报）

```cpp
// test_${rule_id}_safe.cpp

// 安全用例1：TODO: 添加安全写法描述
void safe_good_1()
{
    // TODO: 添加安全写法1的代码
}

// 安全用例2：TODO: 添加安全写法描述
void safe_good_2()
{
    // TODO: 添加安全写法2的代码
}

// 安全用例3：TODO: 添加安全写法描述
void safe_good_3()
{
    // TODO: 添加安全写法3的代码
}

// 安全用例4：TODO: 添加安全写法描述
void safe_good_4()
{
    // TODO: 添加安全写法4的代码
}

// 安全用例5：TODO: 添加安全写法描述
void safe_good_5()
{
    // TODO: 添加安全写法5的代码
}

// NOPROTECT用例：TODO: 添加特殊场景说明
void noprotect_case()
{
    // NOPROTECT: TODO: 添加特殊场景说明
    // TODO: 添加有NOPROTECT标记的代码
}

// 建议：提供5-10个安全用例，覆盖正确做法和误报排除场景
```
'''
    
    template = Template(template_str)
    return template.substitute(
        rule_id=rule_id,
        rule_name=rule_name,
        category=category,
        severity=severity,
        description=description,
    )


def update_rules_config(config_path: Path, rule_id: str, rule_name: str, category: str, severity: str, description: str) -> bool:
    if yaml is None:
        print("Error: PyYAML not installed, cannot update config", file=sys.stderr)
        return False
    
    if not config_path.exists():
        print(f"Error: Config file not found: {config_path}", file=sys.stderr)
        return False
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Error: Failed to load config: {e}", file=sys.stderr)
        return False
    
    rules = config.get("rules", {})
    
    if category not in rules:
        print(f"Error: Category '{category}' not found in config", file=sys.stderr)
        print(f"Available categories: {list(rules.keys())}", file=sys.stderr)
        return False
    
    rule_config = {
        "enabled": True,
        "id": rule_id,
        "name": rule_name,
        "severity": severity,
        "description": description,
        "reference": f"{CATEGORY_MAP[category]}/{rule_id}.md",
    }
    
    rules[category]["rules"][rule_id] = rule_config
    
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        return True
    except Exception as e:
        print(f"Error: Failed to save config: {e}", file=sys.stderr)
        return False


def main():
    import io
    
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    parser = argparse.ArgumentParser(
        description="Add a new stability rule to the framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument("--rule-id", required=True, help="Rule ID (e.g., StabilityCodeReview_ExceptionHandling_008)")
    parser.add_argument("--name", required=True, help="Rule name (e.g., 空catch块检测)")
    parser.add_argument("--category", required=True, help="Category (e.g., 异常处理)")
    parser.add_argument("--severity", required=True, choices=["CRITICAL", "HIGH", "MEDIUM", "LOW"], help="Severity level")
    parser.add_argument("--description", required=True, help="Rule description")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be created without actually creating")
    
    args = parser.parse_args()
    
    if not validate_rule_id(args.rule_id):
        print(f"Error: Invalid rule ID format: {args.rule_id}", file=sys.stderr)
        print("Expected format: StabilityCodeReview_<CategoryShort>_XXX", file=sys.stderr)
        return 1
    
    if args.category not in CATEGORY_MAP:
        print(f"Error: Invalid category: {args.category}", file=sys.stderr)
        print(f"Available categories: {list(CATEGORY_MAP.keys())}", file=sys.stderr)
        return 1
    
    script_dir = Path(__file__).resolve().parent.parent
    references_dir = script_dir / "references"
    config_path = script_dir / "config" / "rules.yaml"
    
    reference_path = references_dir / CATEGORY_MAP[args.category] / f"{args.rule_id}.md"
    
    if args.dry_run:
        print("\n=== Dry Run - Files that would be created ===")
        print(f"\n1. Reference doc: {reference_path}")
        content = create_reference_doc(args.rule_id, args.name, args.category, args.severity, args.description)
        print("\nPreview (first 800 chars):")
        print(content[:800] + "...")
        print(f"\nTotal length: {len(content)} chars")
        print(f"\n2. Config update: {config_path}")
        print(f"   Adding rule to category: {args.category}")
        return 0
    
    # 先检查前置条件，避免创建半成品
    if yaml is None:
        print("Error: PyYAML not installed, cannot update config", file=sys.stderr)
        return 1
    
    if not config_path.exists():
        print(f"Error: Config file not found: {config_path}", file=sys.stderr)
        return 1
    
    reference_content = create_reference_doc(args.rule_id, args.name, args.category, args.severity, args.description)
    reference_path.parent.mkdir(parents=True, exist_ok=True)
    with open(reference_path, "w", encoding="utf-8") as f:
        f.write(reference_content)
    print(f"✅ Created reference doc: {reference_path}")
    
    if update_rules_config(config_path, args.rule_id, args.name, args.category, args.severity, args.description):
        print(f"✅ Updated config: {config_path}")
    else:
        # 配置更新失败，删除已创建的文件
        reference_path.unlink()
        print("❌ Error: Failed to update config file", file=sys.stderr)
        print(f"   Deleted incomplete reference doc: {reference_path}", file=sys.stderr)
        return 1
    
    print("\n=== Next Steps ===")
    print("1. Edit the reference doc to add examples and details:")
    print(f"   {reference_path}")
    print("\n2. Fill in all TODO sections following RULE_TEMPLATE.md guidelines:")
    print("   - Provide 5-10 problem code scenarios with detailed comments")
    print("   - Provide 5-10 fix solutions with best practices")
    print("   - Add specific detection targets (numbered list)")
    print("   - Add 5+ detection steps (numbered list)")
    print("   - Add optional extension sections if applicable:")
    print("     * Best practices explanation")
    print("     * Actual code references (function names, constants)")
    print("     * Special technical details")
    print("     * Classification strategies")
    print("   - Complete RiskFlow (4 fields, specific to code elements)")
    print("   - Complete ImpactAnalysis (4 fields, specific scenarios)")
    print("   - Complete false positive exclusion table:")
    print("     * NOPROTECT marker")
    print("     * Third-party libraries")
    print("     * Test code")
    print("     * Rule-specific safe patterns")
    print("   - Provide 5-10 trigger test cases")
    print("   - Provide 5-10 safe test cases")
    print("   - Add NOPROTECT example")
    print("\n3. Use actual project references:")
    print("   - Real function names (e.g., RSCanvasDrawingRenderNodeDrawable::CreateGpuSurface)")
    print("   - Real constants (e.g., MAX_ITEM_COUNT = 1000)")
    print("   - Real log functions (e.g., ROSEN_LOGE())")
    print("\n4. Verify the rule with AI code review")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())