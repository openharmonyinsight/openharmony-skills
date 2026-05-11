# ohos-dev-arkui-code-review

ACE Engine (OpenHarmony ArkUI) 领域的结构化代码审查 Skill。

## 定位

面向 ACE Engine (OpenHarmony ArkUI 框架) 代码库的代码审查能力，覆盖 C++、TypeScript 和 ArkTS。聚焦项目特定的架构约束、智能指针约定 (RefPtr/WeakPtr/DynamicCast)、组件生命周期规则和四层边界校验。

## 放置信息

| 字段 | 值 |
|------|------|
| 命名空间 | `domain` |
| 领域 | `arkui` |
| 阶段 | `development` |
| 机器名 | `ohos-dev-arkui-code-review` |

## 目录结构

```text
ohos-dev-arkui-code-review/
  SKILL.md
  README.md
  references/
    ACE_ARCHITECTURE.md
    ACE_LIFECYCLE.md
    ACE_TESTING.md
    CODE_SMELLS.md
    DIMENSIONS.md
    MEMORY.md
    SECURITY.md
    SOLID.md
    STABILITY.md
  assets/
    report_template.md
  examples/
  evals/
```

## 与公共能力的关系

本 Skill 强依赖 ACE Engine 框架架构和 ArkUI 组件体系，属于领域特定能力。通用的 C++ 编码规范审查请使用公共 Skill `ohos-dev-cpp-coding-style`。

## 维护者

- OpenHarmony ArkUI 团队
