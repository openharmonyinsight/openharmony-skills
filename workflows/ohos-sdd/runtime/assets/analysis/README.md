# Analysis Assets

> 本目录用于沉淀长期有效的二次分析资产。它不是一次性查询记录，也不是某个 Feature 的临时上下文包，而是面向复杂子系统复用的长期上下文层。

## 为什么需要单独的 analysis 资产

对复杂 OpenHarmony 子系统，单次任务前临时查询往往不够。真正影响 `Specify / Design` 上下文和后续实现审查质量的，通常是长期积累的背景判断，例如：

- 仓内主要模块关系
- 与上游框架或外部依赖的耦合方式
- 常见兼容性边界
- 历史设计取舍
- 反复出现的风险点和 review 焦点

这些内容不适合每次都重新从源码和 DeepWiki 里提取一次，更适合沉淀为长期分析资产。

## 与其他上下文的区别

| 类型 | 存放位置 | 作用 |
|------|----------|------|
| 临时查询记录 | Feature / Bugfix 目录下的 context pack | 为单次任务服务 |
| 规则与 Skill | `rules/architecture/` + `skills/` | 开发规则正文与 SDD 流程 skill |
| 长期分析资产 | `context-engine/analysis/` | 沉淀可复用的子系统背景和长期判断 |

## 推荐目录结构

```text
context-engine/analysis/
├── README.md
├── arkweb/
│   ├── subsystem-overview.md
│   ├── dependency-map.md
│   ├── compatibility-boundaries.md
│   └── review-focus.md
├── arkui/
├── arkgraphic/
├── arkdata/
└── system-service/
```

说明：上述子目录是推荐结构，不要求一次性建齐。当前仓已创建 `arkweb/`、`arkui/`、`arkgraphic/`、`arkdata/` 作为占位入口，后续按试点优先级逐步补真实分析内容。

## 推荐内容

每个子系统目录至少可以包含以下材料：

1. `subsystem-overview.md`
2. `dependency-map.md`
3. `compatibility-boundaries.md`
4. `review-focus.md`
5. `open-questions.md`

### 每个文件的内容定位

| 文件 | 核心内容 | 深度要求 | 信息源 |
|------|----------|----------|--------|
| subsystem-overview.md | 模块划分、仓结构、对外接口面 | 新人能看懂模块关系图即可 | 源码 BUILD.gn + bundle.json |
| dependency-map.md | 上游/下游依赖、跨仓调用边界 | 列出直接依赖和 IPC 边界 | bundle.json + DeepWiki |
| compatibility-boundaries.md | 版本约束、API 兼容红线 | 只写已知坑和红线 | 历史缺陷 + Owner 问答 |
| review-focus.md | 常见缺陷模式、Owner 反复追问的点 | 3-5 条最有价值的审查经验 | review 记录 + Committer 反馈 |
| open-questions.md | 待确认的架构假设或待补充的分析 | 列出问题 + 置信度 | 分析过程中的不确定项 |

### 填充原则

- 按需填充，不要求一次性建齐。有实际需求驱动时再补
- 优先级：review-focus > subsystem-overview > dependency-map > 其余
- 从一个子系统试点（如 arkweb）开始，验证结构有效后再推广

要求：

- 结论要能追溯到源码、官方文档、历史设计或 review 记录
- 推断性内容必须标明置信度和待确认点
- 不重复搬运整份源码说明，重点写”对后续任务真正有帮助的判断”
- 变化快的事实应写更新时间和适用范围

## 使用规则

1. `Specify / Design` 可以把本目录作为 context source，但不能跳过针对当前任务的事实确认。
2. Post-Plan 审查可以把 `review-focus.md` 作为审查辅助，但不能替代本轮审查证据。
3. 发现 analysis 与当前源码、官方文档或 Owner 结论冲突时，以当前事实为准，并回写修订。
4. 新建复杂子系统 profile 时，应优先引用本目录，再定义 `experts.md` 和 profile checklist。

## 适用场景

- 同一子系统反复进入试点或多轮演进
- 子系统跨仓、跨层、跨角色协作频繁
- DeepWiki 查询结果需要长期复核和沉淀
- Post-Plan 代码审查常出现相似的 Owner / Committer 关注点

## 当前状态

| 子目录 | 当前状态 |
|--------|----------|
| `arkweb/` | 已填充 subsystem-overview.md，其余待补充 |
| `arkui/` | 已包含上下文加载、资产模型、验证/gate 与 Spec for Validation playbook |
| `arkgraphic/` | 已创建占位 README，待补真实分析内容 |
| `arkdata/` | 已创建占位 README，待补真实分析内容 |
