## Phase 5A: Demo 应用生成（UI 类测试点）

**前置条件**：Phase 4 设计文档已生成，且包含控件 ID 清单附录和 Demo 测试点附录。

**加载模块**:
- demo-pipeline 技能：`phases/phase1_ui_design.md`、`phases/phase2_code_generation.md`、`phases/phase3_compile_verify.md`

---

> **`knowledge_root` 降级**：下文中所有 `{knowledge_root}/...` 路径，若 `knowledge_root` 未配置或路径不存在，则降级从 `{skill_root}/modules/` 和 `{skill_root}/references/` 加载对应内置知识。完整映射表见 `system.md`「知识库路径与降级规则」。

### Step 0: 测试用例分类

读取 Phase 4 设计文档，将所有测试用例分为 UI 类和非 UI 类。

#### 分类规则

| 分类 | 条件 | 测试方式 |
|------|------|---------|
| **UI 类** | 测试类型为 `EVENT`，或涉及组件属性/界面交互/页面跳转的用例 | Demo + UiTest |
| **非 UI 类** | 测试类型为 `PARAM`/`ERROR`/`RETURN`/`BOUNDARY`，且不涉及 UI 交互 | 直接 API 调用 |

#### 子系统默认策略

| 子系统 | 默认分类策略 |
|--------|-------------|
| ArkUI | 大部分用例为 UI 类（组件属性、事件、布局） |
| ArkWeb | Web 组件属性/事件为 UI 类，webview API 为非 UI 类 |
| ability | 页面跳转/生命周期为 UI 类，纯 Ability API 为非 UI 类 |
| 其他 | 默认为非 UI 类，除非用例显式涉及 UI 交互 |

#### 分类结果

在输出目录生成 `test_classification.md`：

```markdown
# 测试用例分类结果

## UI 类用例（Demo + UiTest）
| 用例编号 | 用例名 | 类型 | 页面 | 控件ID数 |

## 非 UI 类用例（纯代码测试）
| 用例编号 | 用例名 | 类型 |

## 统计
- UI 类：X 个 | 非 UI 类：X 个
```

**若所有用例均为非 UI 类**：跳过 Step 1（Demo 生成），直接进入 Phase 5（非 UI 类测试代码生成）。

---

### Step 1: Demo 应用生成

仅当存在 UI 类用例时执行。

#### 1a: 确定领域

**直接使用 Phase 1 映射上下文中的 `domain` 字段**，无需再次映射。

映射上下文在 Phase 1 步骤 2（加载配置链）中已通过 `{knowledge_root}/common/xts_experience/09_project_data/component_subsystem_mapping.json` 建立，包含：

| 映射上下文字段 | 用途 |
|-------------|------|
| `domain` | demo-pipeline 领域 key（如 `ArkUI`、`multimedia`） |
| `has_reference` | demo-pipeline 是否有对应 `reference/api-reference/{domain}/` |
| `demo_supported` | 是否支持 Demo 生成 |

**降级处理**：

| 映射上下文状态 | 处理 |
|-------------|------|
| `domain` 有值，`has_reference` 为 true | 正常使用完整配置生成 Demo |
| `domain` 有值，`has_reference` 为 false | 使用默认配置生成 Demo，Phase 10 报告中提示用户补充 `reference/api-reference/{domain}/` 配置以提高生成效果 |
| `domain` 为 null（如 testfwk） | 不生成 Demo，仅走非 UI 类测试 |
| `domain` 来源为 `default`（子系统名作为默认 key） | 使用默认配置生成 Demo，Phase 10 报告中提示用户确认领域映射是否正确 |

#### 1b: 调用 demo-pipeline 三阶段

**输入来源**：直接使用 Phase 4 设计文档中的 Demo 测试点附录（已包含测试点ID、描述、技术类型、优先级、页面、操作步骤、预期结果），无需二次转换。

使用 Agent 子代理执行 demo-pipeline 的三个阶段：

| 子阶段 | demo-pipeline 指令文件 | 输入 | 输出 |
|--------|----------------------|------|------|
| Demo UI 设计 | demo-pipeline `phases/phase1_ui_design.md` | 设计文档 Demo 测试点附录 + 控件 ID 清单 | `demo_design.md` |
| Demo 代码生成 | demo-pipeline `phases/phase2_code_generation.md` | `demo_design.md` | `TestDemo/` 工程 |
| Demo 编译验证 | demo-pipeline `phases/phase3_compile_verify.md` | `TestDemo/` | 编译状态 |

**Agent prompt 模板**：

```
你是 Demo 流水线系统的阶段执行器。

{demo-pipeline phase 文件的完整内容}

## 运行时上下文
- 测试点数据：从 Phase 4 设计文档的「附录：Demo 测试点」章节读取
- 控件 ID 清单：从 Phase 4 设计文档的「附录：控件 ID 清单」章节读取
- 领域：从 Phase 1 映射上下文的 `domain` 字段读取（{映射后的领域名称}）
- API 参考目录：{demo-pipeline路径}/reference/api-reference/{领域}/
- 工程模板目录：{demo-pipeline路径}/reference/template/
- 输出目录：{输出目录}

## 通用约束
- 全程不生成 JSON 数据块，仅使用 Markdown 表格
- 输出文件写入磁盘后返回摘要
- 摘要必须包含具体数字，不含占位符

## 返回格式
完成后请返回以下摘要信息：
- Demo 页面数、控件数、编译状态、修复次数
```

#### 1c: Demo 编译失败处理

| 场景 | 处理 |
|------|------|
| BUILD SUCCESSFUL | 正常继续 |
| BUILD FAILED（SDK 缺失 API） | 暂停，询问用户是否替换 SDK 或跳过 |
| BUILD FAILED（编译错误，≤5 轮） | 自动修复后重新编译 |
| BUILD FAILED（>5 轮，单页面 Demo） | 终止修复，标记 Demo 为"编译未通过"，UiTest 用例标记为"待验证"，将问题抛给用户 |
| BUILD FAILED（>5 轮，多页面 Demo） | **逐页面隔离编译**：将 Demo 拆分为单个页面独立编译，定位失败的页面，将失败页面的具体编译错误抛给用户求助；编译通过的页面对应的 UiTest 用例正常进入后续流程 |

**多页面降级流程**：

```
整体编译失败 > 5 轮
  │
  ├─ 检查 Demo 页面数
  │    ├─ 仅 1 个页面 → 标记"编译未通过"，抛给用户
  │    └─ 多个页面 → 逐页面隔离编译
  │
  ├─ 逐页面隔离编译结果
  │    ├─ PAGE-001 编译通过 → 对应 UiTest 用例正常推进
  │    ├─ PAGE-002 编译失败 → 记录错误，抛给用户求助
  │    └─ PAGE-003 编译通过 → 对应 UiTest 用例正常推进
  │
  └─ 输出编译报告
       - 通过页面列表及对应 UiTest 用例编号
       - 失败页面列表及具体编译错误信息
       - 用户可基于错误信息修复后重新编译失败页面
```

#### 1d: 编译修复经验回刷

当用户协助修复编译问题后，将修复经验总结回刷到技能文件中，避免同类问题重复发生。

**回刷规则**：

| 修复类型 | 回刷目标文件 | 回刷内容 |
|---------|------------|---------|
| ArkUI 组件 API 用法错误 | `{knowledge_root}/common/xts_experience/05_patterns/01_demo_uitest_contract.md` 控件类型映射 | 补充正确的组件用法或约束 |
| 控件 ID 命名冲突/不规范 | `{knowledge_root}/common/xts_experience/05_patterns/01_demo_uitest_contract.md` 命名规范 | 补充命名冲突案例或约束 |
| UiTest API 使用方式错误 | `{knowledge_root}/common/xts_experience/01_framework/02_uitest_framework.md` | 补充正确的 API 用法或反模式 |
| Demo 代码模板缺失场景 | `{knowledge_root}/common/xts_experience/09_methodology/14_uitest_templates.md` | 新增对应场景的模板 |
| Demo 页面结构设计缺陷 | `{knowledge_root}/common/xts_experience/09_methodology/15_demo_testpoint_adapter.md` | 补充设计约束 |

**回刷流程**：

```
用户修复编译问题
  │
  ├─ 1. 记录修复内容（原始错误 → 修复方案 → 修复后代码片段）
  │
  ├─ 2. 归类修复类型（组件 API / 控件 ID / UiTest API / 模板缺失 / 设计缺陷）
  │
  ├─ 3. 判断通用性：
  │    ├─ 个案（特定 API 的特殊行为）→ 仅记录到当前设计文档的注意事项
  │    └─ 通用（同类 API/组件都可能遇到）→ 回刷到对应技能文件
  │
  └─ 4. 回刷方式：
       - 在目标文件的约束/反模式章节追加新条目
       - 条目包含：问题描述、错误示例、正确示例、原因说明
       - 不删除已有内容，仅追加
```

**向用户确认**：回刷前向用户展示拟回刷的内容，确认后方可写入。
```
