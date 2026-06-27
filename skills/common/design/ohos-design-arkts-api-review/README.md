# ohos-design-arkts-api-review

鸿蒙 ArkTS API 接口设计的规范性检视技能，覆盖 `.ts` / `.ets` 文件中 API 声明的命名、签名、注释、异常、事件等全方位规范要求。

## 项目说明

由 OpenHarmony API 规范团队维护，面向 HarmonyOS ArkTS API 设计场景。技能内置 54 条规则，分为 11 大类：

| 类别 | 覆盖范围 |
|------|---------|
| 命名规范 | 命名准确性、肯定表达式、英语/拼写、对仗词、缩写、争议词、动词/名词词性、单复数 |
| 接口设计 | 可见性最小化、单一职责、参数个数、可选参数、配置对象 |
| 安全 | 敏感权限、隐私数据保护 |
| 同步异步规范 | Promise 回调、async/async 使用、避免阻塞 |
| 异常定义 | 错误码设计、异常类层级 |
| 异常实现 | throw 时机、错误信息、参数校验 |
| 事件命名 | on/off 对仗、事件名格式、监听器生命周期 |
| 类型与数据规范 | 类型精度、字面量、枚举、联合类型 |
| 注释说明 | JSDoc 完整性、描述准确性、避免冗余 |
| 结构定义规范 | 属性顺序、可变性、分层 |
| 公共事件规范 | 公共事件命名、参数、生命周期 |

## 目录结构

```text
ohos-design-arkts-api-review/
├── SKILL.md              # 技能定义与全部 54 条规则
├── README.md             # 本文件
├── evals/
│   ├── evals.json        # 90 个评估用例
│   └── files/
│       ├── negative/     # 45 个违规样本（应被检出）
│       └── positive/     # 45 个合规样本（不应被误报）
└── benchmark.md          # with_skill / without_skill 评估对比报告
```

## 使用方式

将本仓库放到 opencode / Claude Code skills 路径下：

```bash
# 全局
~/.config/opencode/skills/ohos-design-arkts-api-review/

# 项目级
<project>/.opencode/skills/ohos-design-arkts-api-review/
```

触发方式（在对话中直接描述需求即可，技能会自动匹配）：

```
检视以下 ArkTS API 文件的规范性：./sdk/arkts/animation/animation.ts
审查这份 API 接口设计：@ohos.animation.d.ts
```

输出：在 `save_dir` 目录下为每个被检文件生成 `review.md`，按规则逐条标注 `line_number`、`rule_name`、`advice`。

## 评估结果摘要

基于 `iteration-3` 的 90 个 eval（45 负向 + 45 正向）评估结果：

| 指标 | with_skill | without_skill |
|------|-----------|---------------|
| 平均通过率 | **100.0%** | 62.2% |
| 总检出数 | 400 | 126 |
| 正向用例误报 | **0** | 多处误报 |
| 问题检出倍数 | — | **3.2×** |

详细数据见 [`benchmark.md`](./benchmark.md)。
