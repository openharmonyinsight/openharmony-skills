---
name: ohos-sdd-config
description: OHOS SDD 技能映射配置。用户可修改此文件替换各步骤使用的技能，不修改则使用默认值。
---

# SDD 技能映射配置

> 修改此文件可替换各步骤调用的技能，无需改动命令文件。
> 未列出的条目保持默认行为。

## 工具匹配矩阵（ohos-test-design 使用）

| API 分类 | 默认技能 |
|----------|----------|
| public_arkts | ohos-test-arkts-xts-generation |
| public_capi | ohos-test-capi-xts-generation |
| public_web | 黑盒测试 |
| system_arkts | ohos-test-arkts-xts-generation |
| internal | gtest |

## 测试代码生成（ohos-test-gen 使用）

| 生成类型 | 默认技能 |
|----------|----------|
| xts | ohos-test-arkts-xts-generation |
| capi | ohos-test-capi-xts-generation |
| manual | gtest |
| web | 黑盒测试 |

## 质量检查

默认技能: `check-test-code-quality`

## 测试设计协调

默认技能: `ohos-design-test-coordinator`
