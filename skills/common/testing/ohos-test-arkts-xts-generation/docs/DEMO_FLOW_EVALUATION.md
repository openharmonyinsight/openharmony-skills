# Demo 生成流程评价报告

> 评价时间：2026-05-19
> 评价范围：ohos-test-arkts-xts-generation 技能的 Demo 生成相关流程（Phase 4/5A/5B）

---

## 总评

Demo 生成流程是整个技能中**设计最精密、架构最清晰**的部分。三方契约机制（设计文档 ↔ Demo ↔ UiTest）是一个优秀的架构决策，将 UI 测试的端到端复杂性分解为可独立验证的契约关系。

**核心亮点**：控件 ID 契约、Phase 5A/5B 代码生成并行设计、批量模式增量追加。
**主要不足**：缺少端到端验证示例、Demo 失败降级策略不完善。

**综合评分**：7.7/10

---

## 1. 架构设计（9/10，优秀）

### 1.1 三方契约机制（亮点）

```
Phase 4 设计文档（控件 ID 清单附录）
         │
         ├──→ Demo 生成：控件带 .id('xxx')
         │
         └──→ UiTest 生成：通过 ON.id('xxx') 定位
```

- **单一数据源**：控件 ID 在 Phase 4 预定义，Demo 和 UiTest 各自从同一份清单读取，消除了 ID 不一致的可能性
- **并行解耦**：代码生成阶段 Demo 和 UiTest 可并行执行（编译阶段需协调，已修正）
- **可验证性**：Phase 7 有明确的三方一致性检查规则

### 1.2 Phase 分流设计

| Phase | 职责 | 输入 | 输出 |
|-------|------|------|------|
| Phase 4 | 设计文档 + 控件 ID 清单 + Demo 测试点 | API 定义 | `.design.md` |
| Phase 5A Step 0 | 用例分类 | `.design.md` | `test_classification.md` |
| Phase 5A Step 1 | Demo 生成 | Demo 测试点附录 + 控件 ID | `TestDemo/` |
| Phase 5 | 非 UI 类测试代码 | 非 UI 类用例 | `{Module}.test.ets` |
| Phase 5B | UiTest 测试代码 | UI 类用例 + 控件 ID | `{Module}Ui.test.ets` |

---

## 2. 已完成的改进

### 2.1 ✅ 编译阶段描述修正

**问题**：原文"无需等待 Demo 编译完成"不准确。UiTest 测试代码依赖 Demo 产物参与编译。

**修正**：区分代码生成和编译两个阶段——代码生成可并行，编译阶段 Demo 和 UiTest 一起进入编译。

**涉及文件**：
- `prompts/phase-5-uitest-generation.md`
- `SKILL.md`
- `docs/DEMO_INTEGRATION_PLAN.md`

### 2.2 ✅ 测试点转换合并到 Phase 4

**问题**：Phase 5A Step 1a（测试点转换）是冗余步骤。Phase 4 已为 UI 类用例设计了控件操作序列和预期 UI 结果，二次转换没有新增信息。

**修正**：Phase 4 在设计文档中同步输出 Demo 测试点附录，Phase 5A 直接读取，删除 Step 1a。

**涉及文件**：
- `prompts/phase-4-design.md`（新增 Demo 测试点附录）
- `prompts/phase-5-demo-generation.md`（删除 Step 1a）
- `SKILL.md`（更新模块加载映射）

---

## 3. 待改进项

### 3.1 🔴 补充端到端示例（最高优先级）

**问题**：整个 Demo 生成流程缺少一个完整的 walkthrough 示例。

**建议**：在 `demo_testpoint_adapter.md` 或单独文件（如 `docs/DEMO_WALKTHROUGH.md`）中添加完整示例，覆盖：

- 输入：一个具体的 API（如 `Button.width()`）
- Phase 4 输出：设计文档（含控件 ID 清单 + Demo 测试点附录）
- Phase 5A 输出：Demo 页面代码
- Phase 5B 输出：UiTest 测试代码
- Phase 7 验证：三方一致性检查结果

**预期收益**：Agent 理解流程的效率提升最大，比任何规则文档都有效。

### 3.2 ✅ 增加复杂控件场景模板（已实施）

**问题**：`uitest_templates.md` 仅覆盖 5 种静态控件场景（标准输入、Select、Toggle、只读、错误），缺少 ArkUI 测试中常见的动态场景。同时所有模板使用 `sleep` 硬等待，导致用例执行时间过长。

**已实施**：
- 全局消除 `sleep` 硬等待，替换为 `waitForComponent` 轮询等待（控件出现即返回）
- 新增 4 个动态场景模板：
  - 2.6 List 滚动定位：`findComponent` 找容器 → `scrollSearch(ON.id())` 定位 ListItem
  - 2.7 弹窗 Dialog：分支 A（`waitForComponent` 操作弹窗控件）、分支 B（`events_emitter.once` 监听弹窗事件断言）
  - 2.8 页面导航：click 导航 → `waitForComponent` 验证目标页 → 可选 `pressBack()` 返回
  - 2.9 Tabs 切换：click Tab → `waitForComponent` 验证新 TabContent
- `demo_uitest_contract.md` 新增 5 个控件类型：`list`、`item`、`tab`、`dialog_btn`、`dialog_text`
- `uitest_framework.md` 补充滚动/滑动/返回 API：`scrollSearch`、`scrollToTop`、`scrollToBottom`、`swipe`、`fling`、`pressBack`、`waitForIdle`
- 新增 `references/templates/Utils_dyn.ets`（动态模式）和 `references/templates/Utils_sta.ets`（静态模式）固定模板，仅含 `sleep()` + `pushPage()` 最小方法集
- beforeAll 消除冗余 sleep（`pushPage` 内部自带 `sleep(2000)` 等待页面转场）

### 3.3 🟡 增加 Demo 失败降级策略

**问题**：Demo 编译持续失败（>5 轮）时仅标记"待验证"，缺少降级路径。

**降级方案**：
- Demo 存在多个页面时，逐个页面隔离编译，定位到具体哪个页面导致失败
- 将无法编译通过的页面问题抛给人类求助解决
- 编译通过的页面对应的 UiTest 用例可正常进入后续流程
- 整体 Demo 不再是"全有或全无"，而是按页面粒度推进

**经验回刷机制**：
- 用户协助修复编译问题后，将修复经验总结回刷到技能文件中（如 `demo_uitest_contract.md`、`uitest_framework.md`、`uitest_templates.md`）
- 区分个案（特定 API 特殊行为，仅记录到设计文档注意事项）和通用问题（同类 API/组件都可能遇到，回刷到技能文件）
- 回刷前向用户确认拟回刷内容

### 3.4 🟡 补充动态控件规范

**问题**：`demo_uitest_contract.md` 的控件类型映射仅覆盖静态控件（Button、TextInput、Toggle、Select、Text）。

**建议补充**：
- List/Grid 动态渲染项的 id 命名规范（如 `item_{page_seq}_{index}_{semantic}`）
- 弹窗控件的定位和操作规范
- 动画/过渡效果的等待策略

### 3.5 🟢 未映射子系统的处理

**问题**：`phase-5-demo-generation.md` 中子系统→领域映射表有"其他 → 需在 domains.yaml 中补充"，用户遇到未映射子系统时会卡住。

**建议**：
- 映射失败时给出明确的用户提示和操作指引
- 提供手动映射的模板格式

### 3.6 🟢 demo_testpoint_adapter.md 的定位调整

**问题**：合并 Step 1a 后，`demo_testpoint_adapter.md` 不再作为 Phase 5A 的加载模块，但其内容（转换映射表、输出格式）对 Phase 4 仍有参考价值。

**建议**：
- 文件保留在 `modules/L2_Generation/generator/` 中，作为 Phase 4 生成 Demo 测试点附录的参考规则
- 在 Phase 4 的 Conditionally Load 中明确引用
- 考虑将转换规则内联到 `design_doc_generator.md` 中，减少文件间跳转

### 3.7 ✅ 子系统→领域映射机制（已实施）

**原问题**：`phase-5-demo-generation.md` 中子系统→领域映射表仅覆盖 4 个子系统，"其他"场景无明确方案。映射仅在 Phase 5A 使用，Phase 1 不做映射。

**已实施**：
- 新建 `references/component_subsystem_mapping.json`：归档 360+ 组件→56 子系统→领域的映射数据（来源于 OpenHarmony bundle.json）
- Phase 1 新增步骤 5a：读取归档映射表，建立映射上下文，供 Phase 2-10 使用
- Phase 5A 步骤 1a 改为直接读取 Phase 1 映射上下文的 `domain` 字段
- 降级策略：未映射组件从源码 bundle.json 动态查找 → 使用子系统名作为默认领域 key → 使用默认配置生成 Demo → Phase 10 报告提示用户补充 reference 配置

---

## 4. 文件质量评估

| 文件 | 行数 | 评分 | 说明 |
|------|------|------|------|
| `prompts/phase-5-demo-generation.md` | ~120 | 8/10 | 分类规则明确，编译失败处理有梯度 |
| `prompts/phase-5-uitest-generation.md` | ~95 | 8/10 | 控件 ID 约束清晰，模板匹配实用 |
| `modules/L2_Generation/generator/demo_testpoint_adapter.md` | 77 | 7/10 | 精练，转换规则已合并到 Phase 4 |
| `references/conventions/demo_uitest_contract.md` | 146 | 9/10 | 核心文件，契约规范完整实用 |
| `modules/L2_Generation/generator/uitest_templates.md` | 300+ | 9/10 | 9 种模板覆盖静态+动态场景，消除 sleep 硬等待 |
| `references/conventions/uitest_framework.md` | 420 | 9/10 | UiTest API 参考完整，补充滚动/滑动 API |
| `docs/DEMO_INTEGRATION_PLAN.md` | 529 | 8/10 | 设计方案完整，已作为实施依据 |

---

## 5. 改进优先级

| 优先级 | 改进项 | 预期收益 | 状态 |
|--------|--------|---------|------|
| 🔴 P0 | 补充端到端 walkthrough 示例 | Agent 理解流程效率大幅提升 | 待实施 |
| 🔴 P0 | 增加复杂控件场景模板 | 覆盖 List/弹窗/页面跳转等常见场景 | ✅ 已实施 |
| 🟡 P1 | Demo 失败降级策略 + 经验回刷 | 提升 UI 测试的鲁棒性 | ✅ 已实施 |
| 🟡 P1 | 动态控件规范 | 支持动态渲染场景的 Demo 和 UiTest | 待实施 |
| 🟢 P2 | 未映射子系统处理 | 改善用户体验 | ✅ 已实施（Phase 1 映射上下文） |
| 🟢 P2 | demo_testpoint_adapter.md 定位调整 | 减少维护负担 | 待实施 |
