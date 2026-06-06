## Phase 4: Generate Test Design

---

> **`knowledge_root` 降级**：下文中所有 `{knowledge_root}/...` 路径，若 `knowledge_root` 未配置或路径不存在，则降级从 `{skill_root}/modules/` 和 `{skill_root}/references/` 加载对应内置知识。完整映射表见 `system.md`「知识库路径与降级规则」。

### 📚 参考文档（按需查阅）

本 Phase 执行过程中可参考以下文件，遇到具体问题时按需查阅：

| 文件 | 内容 | 何时查阅 |
|------|------|---------|
| `{knowledge_root}/common/xts_experience/09_methodology/09_design_doc_generator.md` | 测试设计文档生成方法论（测试类型、边界条件、错误码映射） | 设计策略不确定、需要参考测试类型定义时 |

---

### ⚙️ 按需加载

本 Phase 不需要额外加载模块，因为测试设计是基于 Phase 3 的 API 解析结果进行设计。

---

### 🚫 Do NOT Load - 禁止加载

本 Phase 期间禁止加载以下模块：

```
{knowledge_root}/common/xts_experience/09_methodology/ 下的 L1_Analysis 相关文件（01~07号文件）
{knowledge_root}/common/xts_experience/09_methodology/ 下的 L3_Validation 相关文件（19~25号文件）
{knowledge_root}/common/xts_experience/ 下的 01_framework、02_arkts、03_standards、04_project、05_patterns 规范文件
{knowledge_root}/common/xts_experience/03_standards/02_error_handling_guide.md
```

---

**加载模块**: `{knowledge_root}/common/xts_experience/09_methodology/09_design_doc_generator.md`

**关键变更**：此阶段专注于生成测试设计文档，不生成测试代码。设计文档将作为 Phase 5 生成测试用例代码的依据。

### 生成范围

| 条件 | 生成范围 | 说明 |
|------|---------|------|
| Flow A（用户提供了覆盖率报告） | 仅设计报告中的未覆盖项 | 精准：严格按照报告列出的未覆盖项设计 |
| Flow B（无覆盖率报告） | 设计全部目标 API 的测试 | 基于 Phase 3 针对性解析的 API 信息设计 |
| **批量模式** | 仅设计当前批次的 ≤10 个 API | 由 `batch_manager.py start <batch_id>` 指定范围 |

**批量模式检测**：检查 `batch_workspace/batch_plan.json` 是否存在。如果存在且当前有 `start` 的批次，则仅设计该批次的 API。

### 设计流程

1. **从 Phase 3 获取 API 信息**：
   - 未覆盖或部分覆盖的 API 列表
   - 方法签名、参数类型、返回类型
   - 错误码、枚举定义

2. **确定测试类型和级别**（先判断，再设计）：

   基本测试类型（大多数 API 都需要）：
   - PARAM（参数测试）：正常值、空值、undefined
   - ERROR（错误码测试）：从 `@throws` 注解提取
   - RETURN（返回值测试）：验证返回值类型和格式
   - EVENT（事件测试）：ArkUI 事件处理

   **BOUNDARY（边界值测试）不是必选项**——仅在参数同时满足以下三个条件时才生成：

   | 条件 | 含义 | 不满足则跳过 BOUNDARY |
   |------|------|----------------------|
   | 有明确的值域范围 | 参数存在合法/非法的分界线 | `hilog.debug(tag)` — tag 无长度限制，无边界可测 |
   | API 对输入做了有效性校验 | 超出范围的值会被拒绝并返回可断言的结果 | `console.log(msg)` — 不校验内容，传什么都原样输出 |
   | 边界行为可预测 | 能明确写出"传这个值应该得到什么结果" | 行为取决于底层实现且无文档说明 → 标注"待确认"，不生成 |

   不需要 BOUNDARY 的常见 API：日志类（hilog/console）、固定枚举参数、无范围约束的字符串透传型 API。

   **测试级别选择依据**（基于 API 重要性 + 场景影响，而非机械映射测试类型）：

   | 评估维度 | Level1（高优先） | Level2-3（标准优先） | Level4（低优先） |
   |----------|------------------|---------------------|------------------|
   | API 重要性 | 子系统核心入口方法 | 一般功能方法 | 辅助/内部方法 |
   | 失败影响 | 功能完全不可用 | 功能降级/异常 | 极端边界才触发 |
   | 使用频率 | 高频常用路径 | 标准使用路径 | 罕见使用路径 |

   应用方式：三个维度加权判断。核心 API 的正常值测试用 Level1；核心 API 的 null/undefined 测试用 Level2；辅助 API 的所有测试用 Level2-3；极端边界用 Level4。禁止所有测试都标为同一级别。

3. **设计每个测试用例**，包含以下字段：

   | 字段 | 说明 | 示例 |
   |------|------|------|
   | 用例编号 | 唯一标识符，格式：`SUB_[子系统]_[模块]_[API]_[类型]_[序号]` | `SUB_ARKUI_COMPONENT_ONCLICK_PARAM_001` |
   | 用例名 | 简洁描述 | `正常值参数测试` |
   | 预置条件 | 测试前需要满足的条件 | `已初始化测试环境，已导入 @kit.XXXKit` |
   | 测试步骤 | 详细步骤说明（必须精确可执行） | `1. 调用 methodA(param1="test", param2=100)\n2. 等待 Promise 返回` |
   | 预期结果 | 期望的输出或行为（必须精确可验证，禁止模糊描述） | `返回 void，无异常抛出` |
   | 场景 | 测试场景分类 | `正常场景` / `异常场景` / `边界场景` |
   | 类型 | 测试类型 | `PARAM` / `ERROR` / `RETURN` / `BOUNDARY` / `EVENT` |
   | 级别 | 优先级 | `P0`（核心） / `P1`（重要） / `P2`（一般） |
   | 依赖关系 | 依赖的其他用例 | `无` 或 `依赖 XXX_METHOD_PARAM_001` |

> **设计文档准确性约束（重要！）**：
> - 所有字段（参数名、参数类型、返回值类型、错误码）必须与 Phase 3 解析的 UnifiedAPIInfo **严格一致**
> - 禁止编造 `.d.ts` 中不存在的方法或参数
> - 禁止使用模糊的预期结果（如"正常工作"、"行为正确"、"符合预期"）
> - 禁止使用模糊的测试步骤（如"测试各种参数"、"检查所有返回值"）
> - 每个测试用例只对应**一个确定的**错误码，禁止使用"或"表达多个错误码
>
> 违反这些约束的后果：Phase 5 生成的代码与设计不一致、Phase 7 验证无法判定通过/失败、模糊描述导致生成的测试无法复现。

4. **应用子系统特有规则**：
   - 从 Phase 1 配置中获取特殊规则
   - 考虑 API 的版本兼容性
   - 遵循测试用例编号规范

5. **生成设计文档**：
   - 文件命名: `{测试文件名}.design.md`
   - 按接口/方法分组组织
   - 每个测试用例占用一个章节
   - **必须包含以下章节（问题 8+9 约束）**：
     1. **文件清单**表格：测试文件、Demo页面（标注"新建"或"复用"）、设计文档路径
     2. **Demo页面设计**：页面路由、页面结构、组件数量、验证方式（`getInspectorByKey`）
     3. **每个用例必须包含 `**组件id**` 字段**：值为 `getInspectorByKey('xxx')` 中使用的 id，三方（设计文档、Demo页面、测试代码）必须完全一致
     4. **Demo页面组件清单**表格：组件id → API → 属性值 → 预期Inspector值

### 参数测试设计规则

| 参数类型 | 测试场景 | 数量 |
|----------|----------|------|
| string | 正常值、空字符串、undefined、null、超长字符串 | 5 |
| number | 正常值、0、负数、NaN、Infinity、边界值 | 6 |
| boolean | true、false、undefined、null | 4 |
| enum | 每个枚举值 + undefined + null | N+2 |
| array | 正常、空数组、单元素、大数组、undefined | 5 |
| object | 正常、空对象、缺少字段、错误类型、undefined | 5 |

### 错误码测试设计规则

- 必须从 `.d.ts` 的 `@throws` 注解提取错误码
- 每个错误码设计一个测试用例
- 场景标记为"异常场景"
- 级别根据上述三维度评估设置

### 输出格式

设计文档采用 Markdown 格式，结构如下：

```markdown
# {测试文件名} 测试设计文档

## 文件清单

| 文件 | 路径 | 说明 |
|------|------|------|
| 测试文件 | `{测试文件路径}` | {用例数}个测试用例 |
| Demo页面（新建/复用） | `{页面文件路径}` | {独立Demo页面/复用历史页面}，包含{N}个带id的组件 |
| 设计文档 | `{设计文档路径}` | 本文件 |

## Demo页面设计

- **页面路由**: `MainAbility/pages/XXX`
- **页面结构**: {Scroll > Column / Column 等}
- **组件数量**: {N}个
- **验证方式**: `getInspectorByKey` + `$attrs` 属性断言

## 接口/方法 1: methodName

### 测试用例 1: SUB_MODULE_METHOD_PARAM_001

| 字段 | 内容 |
|------|------|
| 用例编号 | SUB_MODULE_METHOD_PARAM_001 |
| 用例名 | 正常值参数测试 |
| **组件id** | `{component_id}` |
| 预置条件 | 已初始化测试环境，已导入 @kit.XXXKit |
| 测试步骤 | 1. 调用 methodA(param1="test", param2=100)\n2. 等待 Promise 返回\n3. 验证无异常 |
| 预期结果 | `obj.$attrs.xxx === 'expected_value'` (精确断言表达式) |
| 场景 | 正常场景 |
| 类型 | PARAM |
| 级别 | P0 |
| 依赖关系 | 无 |

### 测试用例 2: SUB_MODULE_METHOD_PARAM_002

...（后续用例，每个用例都必须有 **组件id** 字段）

## Demo页面组件清单

| 组件id | API | 属性值 | 预期Inspector值 |
|--------|-----|--------|----------------|
| `{text_xxx_value}` | {API名} | {属性值} | {预期值} |

## 接口/方法 2: anotherMethod

...（后续接口）
```

### 设计文档输出位置

与测试文件同目录，文件名格式：`{测试文件名}.design.md`

例如：`test/xts/acts/arkui/entry/src/main/ets/test/xxx.test.design.md`

### 输出

完整的测试设计文档，供 Phase 5 生成测试用例代码使用。

设计文档将包含：
- 所有目标 API 的测试用例设计
- 每个用例的详细字段（编号、名称、预置条件、步骤、预期结果等）
- 按接口/方法分组的组织结构
- 符合子系统规范的用例编号和命名
