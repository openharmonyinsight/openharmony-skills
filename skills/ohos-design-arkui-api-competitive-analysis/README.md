# ohos-design-arkui-api-competitive-analysis

ArkUI 接口竞品分析 skill —— 对 ArkUI 的 UI 接口（事件 / 手势 / 组件 / 布局 / 状态 / 动画）产出**结构一致、规格准确**的对标报告，对标 **Android（Compose/View）** 与 **iOS（SwiftUI/UIKit）**。

## 为什么需要 / Why

团队做 ArkUI 接口对标时常见问题：维度零散、口径不一、**易把"内部实现"当"公共能力"**（如误用 ace_engine 内部 `.d.ts` 把触摸坐标单位当 px、把 `force`/`operatingHand` 当公共字段）。本 skill 用统一框架 + 数据铁律（以 `interface_sdk-js` 为权威）+ 报告模板 + 金标准样例固化方法论。

## 安装 / Install

```bash
npx skills add openharmonyinsight/openharmony-skills --skill ohos-design-arkui-api-competitive-analysis
```

## 用法 / Usage

触发词示例："竞品分析 ArkUI onTouch"、"对标 ArkUI 与 Android/iOS 的触摸能力"、"做接口对标 / capability gap analysis"。

典型产出见 `examples/onTouch-analysis.md`：Meta → 规格速览 → 能力对比矩阵 → 关键差异点 → 结论与迁移路径 → 附录来源。

## 目录 / Layout

```
SKILL.md                         # 主入口（canonical 7 段骨架，中英双语）
references/
  analysis-dimensions.md         # 12 维框架 + API 类别→维度权重裁剪表
  authoritative-sources.md       # interface_sdk-js 取数铁律 + 校准后的 onTouch 公共规格
examples/
  onTouch-analysis.md            # 金标准样例
evals/
  onTouch.md                     # with/without skill 测试用例
  README.md                      # 跑法与通过标准
```

## 与相关 skill 的边界 / Boundaries

- `arkui-api-design`：关注**如何设计/编写** ArkUI API（static/dynamic 同步、JSDOC、Resource 类型）。本 skill 关注**对已有接口做跨平台能力对标**。
- `android-to-harmonyos-migration-workflow`：关注**代码迁移**全流程（多 agent + 脚本）。本 skill 关注**接口层规格对标**，是迁移前的能力对齐输入。
