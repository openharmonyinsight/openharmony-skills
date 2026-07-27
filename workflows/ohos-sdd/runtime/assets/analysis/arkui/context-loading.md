# ArkUI Context Loading

## 最小加载路径

按任务选择最小上下文，不要默认全读 ArkUI profile、全部 subprofile 和所有 analysis 文档。

| 任务 | 必读 | 条件读 | 按需读 |
|---|---|---|---|
| 新需求启动 | `profiles/arkui/profile.md` | `subprofiles/README.md` | `asset-model.md` |
| 写 `spec.md` | `profile.md` | 命中的子 profile | `context-loading.md` 自身不再重复读取 |
| 写 `design.md` | `profile.md` | 命中的子 profile | `validation-playbook.md` 中相关段落 |
| 写 `execution-plan.md` | `profile.md` | 命中的子 profile | `validation-playbook.md` |
| 执行 ArkUI gate / 写 gate 证据 | `profile.md` | 命中的子 profile | `gate-playbook.md` 中对应阶段 |
| Host Preview / SpecTest 设计 | `profile.md` | `arkui/component` 或 `arkui/render` | `validation-playbook.md` |
| 最终 review / gate | `profile.md` | 命中的子 profile | `validation-playbook.md`；需要核对 gate 细则时读 `gate-playbook.md` |

## 子 profile 选择

先根据 `manifest.profile` 决定主 profile，再根据 `manifest.subprofiles` 或 file scope 补读子 profile：

- `arkui/component`：组件 pattern、交互、状态机
- `arkui/capi`：NDK / C API
- `arkui/sdk-api`：ArkTS SDK API、`.d.ets`、Modifier
- `arkui/render`：渲染、布局、绘制链路

若无法确定子 profile，只保留 base `arkui`，并在 `proposal.md` 或 `execution-plan.md` 中记录判断缺口。

## 信息检索流程

Define 阶段澄清以及 Specify / Design 编写 `spec.md` / `design.md` 时，Agent 需要探索项目和源码以获取上下文。若目标项目不存在 `docs/kb_search.py` 或知识库未建立，跳过手段 1，从手段 2 开始。

| 优先级 | 手段 | 适用场景 | 使用方式 |
|--------|------|----------|----------|
| 1 | 仓内知识库检索 `docs/kb_search.py` | 涉及组件、布局、渲染、SDK API 等已有知识库覆盖的领域 | 按关键字检索，定位到具体知识库 `.md` 文件。禁止直接读取 `knowledge_base_INDEX.json` 全文件 |
| 2 | 历史特性规格 `specs/index.md` | 涉及已有功能域或存量特性的上下文收集 | 读取 index.md 查找 FuncID，再读取对应的 `specs/<func-domain>/Feat-XX-*-spec.md` 和 `design.md` |
| 3 | DeepWiki MCP 工具 | 需要 GitHub 仓库级别的架构、设计模式、模块关系等宏观信息 | 使用 `ask_question` 提问，或 `read_wiki_structure` + `read_wiki_contents` 获取结构化文档 |
| 4 | AI 自行探索 | 以上手段无法覆盖的具体实现细节 | 使用 grep/find/Read 等工具直接探索源码 |

## 上下文预算控制

| 场景 | 推荐手段 | 限制 |
|------|----------|------|
| 快速定位模块/组件 | 知识库检索 | 通过 `kb_search.py` 按关键字检索，按需读 1-2 个知识库文件 |
| 了解存量特性设计 | 历史特性规格 | 只读 index.md + 目标 Feat spec，不读整个 specs 目录 |
| 架构级宏观理解 | DeepWiki | 1-2 次提问，不超过 3 次 |
| 具体实现细节确认 | 源码探索 | 优先用 grep 定位关键符号，减少全文件读取 |

## 读取停止条件

满足下面条件后，停止继续扩上下文：

- 已能确定主 profile 和需要的子 profile
- 已能写出当前阶段所需文档
- 已定位需要的验证路径或缺口

如果只是为了“看起来更全面”而继续读 analysis，应该停止。
