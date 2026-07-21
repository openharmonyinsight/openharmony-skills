# MVP Plan

## 目标

先把 `ohos-delivery-kit` 做成一个可定义、可校验、可被平台封装的轻交付规范层。

MVP 不追求一上来覆盖所有插件和所有平台。

## MVP 范围

### 必做

- 固定仓定位和分层边界
- 定义 `.codespec/` 最小目录结构
- 定义变更最小文档章节 contract
- 提供第一版 validator 设计
- 优先准备 Codex 侧最小封装

### 暂不做

- 全量平台自动安装脚本
- 全量子系统 profile 深度规则
- 复杂语义质量评分
- 一次性适配所有第三方插件
- bugfix 场景（后续迭代补充）
- 多 feature 索引机制（manifest/lineage/registry，后续迭代补充）

## 建议实施顺序

### Phase 1: 规范定稿 [已完成]

> 工作量: M · 当前状态: 设计文档已完成 (8 docs)

### Phase 2: Core 骨架 [已完成]

```text
core/
├── templates/
│   ├── ai/          # AI 生成交付件模板
│   └── review/      # 人工审核用模板
├── rules/
│   └── delivery/
└── validators/
```

输出：

- 轻量模板骨架（ai/ + review/ 分离）
- validator 输入输出约定

通过标准：

- 可以对一个最小 `.codespec/` 样例做静态结构校验

### Phase 3: Example 样例 [已完成]

```text
examples/
└── issue-12345-arkui-focus/
```

输出：

- 一个最小 Feature 例子

通过标准：

- 能作为 validator 回归样例
- 能作为插件适配对照输入

### Phase 4: 平台静态壳 + 生成分发 [✅ 完成]

当前落地形态：

```text
packaging/
├── claude/      # 静态壳：manifest + hooks + README
├── codex/       # 静态壳：manifest + hooks + README
└── opencode/    # 静态壳：package.json + plugins/ohos-delivery-kit.js + README

dist/
├── claude/      # 生成分发产物
├── codex/       # 生成分发产物
└── opencode/    # OpenCode 项目本地拷贝源
```

最低交付：

- `packaging/*` 保留静态输入壳
- `scripts/distribute-skills.sh` 生成 `dist/*`
- 安装脚本和验证脚本以 `dist/*` 为准

通过标准：

- Codex 能识别该插件
- 能基于统一规范在业务仓生成 `.codespec/` 初始结构

### Phase 5: Adapter 接入 [✅ 完成]

桥接命令 (11 个) 全部实现：
- Superpowers: `odk-sp-brainstorm` / `odk-sp-plan` / `odk-sp-implement` / `odk-sp-review`
- OpenSpec: `odk-ops-propose` / `odk-ops-apply`
- MatrixSpec: `odk-ms-proposal` / `odk-ms-delta-spec` / `odk-ms-delta-design` / `odk-ms-tasks` / `odk-ms-validation`

详见 `docs/designs/two-layer-command-architecture.md`。

通过标准：

- 三者均映射到同一套 `.codespec/changes/<id>/` contract ✅

## 并行策略

- **Phase 2 + Phase 3 可并行**: 最小样例可与模板草案同步编写，样例驱动模板迭代
- **Phase 4 建议推迟**: 在 pilot 验证 core contract 可用后再做平台封装，避免过早绑定平台机制
- **Phase 5 依赖 Phase 2**: Adapter 文档需要 Core 模板稳定后才能精确写映射

## 风险

### 风险 1：规范写得太重

症状：

- 文档数量过多
- 简单需求也必须走重流程

控制：

- 始终把"最小章节 contract"放在"完整模板"之前

### 风险 2：规范写得太轻

症状：

- 只有模板，没有追溯机制
- AC 与代码映射失去约束

控制：

- 代码映射和 AC-Task 追溯不做妥协

### 风险 3：过早平台化

症状：

- 先把 Codex/Claude/OpenCode 壳子铺满
- 后续 core 变更时平台层一起返工

控制：

- 先稳定 `core` contract，再做平台壳

---

> Last reviewed: 2026-06-05. Status: Phase 1-5 全部完成，MVP 范围已交付。
