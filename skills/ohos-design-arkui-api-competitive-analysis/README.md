# ohos-design-arkui-api-competitive-analysis

面向 ArkUI 公共 UI API 的 Android/iOS 竞品分析 Skill，覆盖事件、键盘、手势、组件、布局、状态和动画。

## 能力

- 锁定接口作用域和平台版本基线。
- 以 `interface_sdk-js` 作为 ArkUI 公共接口权威源。
- Android/iOS 优先引用 Android Developers 和 Apple Developer 官方文档。
- 区分直接等价、功能等价、组合实现、替代方案和未找到等价能力。
- 使用 Fact Ledger 与 Claim Ledger 管理证据、推论和待核事项。
- 输出规格事实、能力矩阵、影响评估、迁移建议和来源审计。

## 使用

```text
对 ArkUI keyboardShortcut 做 Android/iOS 应用级键盘快捷键竞品分析。
```

```text
对 ArkUI Flex 做快速能力扫描，重点比较布局语义和迁移风险。
```

安装：

```bash
npx skills add openharmonyinsight/openharmony-skills --skill ohos-design-arkui-api-competitive-analysis
```

## 工作流

```text
分析契约
  → 能力拆解
  → 对标对象映射
  → 各平台独立取证
  → 规格归一化
  → 断言审计
  → 差异与影响
  → 分级建议
  → 报告与质量门禁
```

## 目录

```text
SKILL.md                         # 紧凑编排入口和不可违反的规则
assets/report-template.md        # 通用主报告模板与按子类型启用的条件区块
references/workflow.md           # 阶段产物、质量门禁和异常处理
references/evidence-ledger.md    # Fact/Comparator/Claim 台账格式
references/analysis-dimensions.md
references/authoritative-sources.md
references/platform-source-routing.md
evals/evals.json                 # benchmark Prompt、预期输出和评分断言
evals/README.md                  # benchmark 运行约定
```

## 边界

- `arkui-api-design` 负责 ArkUI API 的设计和实现规范；本 Skill 负责跨平台能力与规格对标。
- `android-to-harmonyos-migration-workflow` 负责完整代码迁移；本 Skill 产出的接口映射和风险可作为迁移输入。
- 最小代码段用于解释 API 心智，不代表修改或实现真实项目。
