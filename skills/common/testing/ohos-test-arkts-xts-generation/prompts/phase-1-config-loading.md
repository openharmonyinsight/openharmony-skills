## Phase 1: 任务参数提取与配置加载

---

### 📚 参考文档（按需查阅）

本 Phase 执行过程中可参考以下文件，遇到具体问题时按需查阅：

| 文件 | 内容 | 何时查阅 |
|------|------|---------|
| `{knowledge_root}/common/xts_experience/README.md` | 知识库目录索引 | 需要了解知识库结构或定位具体知识文件时 |

---

### ⚙️ 按需加载（根据子系统）

以下模块仅在你处理指定子系统时才需要加载：

| 子系统 | 加载文件 | 说明 |
|--------|---------|------|
| 用户指定子系统时 | `{knowledge_root}/domains/{Subsystem}/xts_experience/_common.md` | 子系统特有配置 |
| 需要模块级配置时 | `{knowledge_root}/domains/{Subsystem}/xts_experience/{Module}.md` | 模块特定规则 |

---

### 🚫 Do NOT Load - 禁止加载

本 Phase 期间禁止加载以下模块：

```
所有 L2_Generation 相关知识（{knowledge_root}/common/xts_experience/09_methodology/ 下的 08~18号文件）
所有 L3_Validation 相关知识（{knowledge_root}/common/xts_experience/09_methodology/ 下的 19~25号文件）
{knowledge_root}/common/xts_experience/ 下的 01_framework、02_arkts、03_standards、04_project、05_patterns 规范文件
```

---

### 前置条件

Phase 0 已完成，`{skill_root}/.oh-xts-config.json` 存在且有效。

---

### 步骤 1: 从用户消息中提取任务参数

从用户消息中提取以下参数，缺失的可从配置文件补全或向用户追问：

| 参数 | 来源优先级 | 必填 | 示例 |
|------|-----------|------|------|
| Flow 模式 | 用户消息关键词检测 | ✅ | "新增 API"→Flow C，提供了覆盖率报告→Flow A，否则→Flow B |
| 子系统 | 用户消息 | ✅ | "ArkUI"、"multimedia" |
| ETS 版本 | 用户消息 → `.oh-xts-config.json` → 默认 `["ets1.1"]` | ✅ | "静态语法"→ets1.2 |
| 模块路径 | 用户消息 | ❌ | "ace_ets_module_ui/ace_ets_module_imageText" |
| d.ts 文件路径 | 用户消息 | ❌ | "component/text.d.ts" |
| 指定 API | 用户消息 | ❌ | "fontFeature"、"textAlign" |
| 目标测试套路径 | 用户消息 | ❌ | "{xts_acts_path}/arkui/ace_ets_module_ui/ace_ets_module_text" |

#### Flow 检测规则

| 优先级 | 检测条件 | Flow | 标记 |
|--------|---------|------|------|
| 1 | 用户消息包含"新增接口"/"新 API"/"new API"/"新增属性"/"新接口"/"新属性"等关键词 | **Flow C（新增接口模式）** | `new_api_mode = true` |
| 2 | 用户提供了覆盖率报告文件（CSV/XLSX/JSON/MD） | **Flow A（有覆盖率报告）** | `has_coverage_report = true` |
| 3 | 以上均不满足 | **Flow B（标准扫描模式）** | 默认 |

**Flow C 特殊行为**（后续 Phase 自动适配）：
- Phase 2: 跳过覆盖率扫描（新增接口在当前代码中不存在，覆盖率必为 0）
- Phase 9: 仅执行 after 扫描（无 before baseline）
- Phase 10: 覆盖率表中"生成前"列标注"0（新增接口）"

#### ETS 版本提取

| 优先级 | 来源 | 说明 |
|--------|------|------|
| 1 | 用户消息中明确指定 | 如"生成 1.1 的测试"、"静态语法"、"ArkTS-Sta"、"ets1.2" |
| 2 | `.oh-xts-config.json` 中的 `ets_version` 字段 | 配置文件已保存的默认版本 |
| 3 | 默认值 | `["ets1.1"]`（动态语法） |

确认 `ets_version` 值。配置文件必须使用数组格式：`["ets1.1"]` 或 `["ets1.1", "ets1.2"]`。

#### 提取规则

- **子系统、ETS 版本、Flow 模式**：必须明确，无法推断时向用户追问
- **模块、d.ts、API、测试套**：可选，用户提供则记录，未提供则后续 Phase 按全量处理
- **目标测试套路径**：用于 Phase 5 代码生成和 Phase 8 编译验证

#### 提取完成后输出参数摘要

```
任务参数：
- Flow: {A/B/C}
- 子系统: {Subsystem}
- ETS 版本: {ets_version}
- 模块: {Module or "未指定（全量）"}
- d.ts: {d.ts path or "未指定（全量）"}
- 指定 API: {API list or "未指定（全量）"}
- 目标测试套: {path or "未指定"}
```

---

### 步骤 2: 加载配置链

> **`knowledge_root` 降级规则**：读取 `.oh-xts-config.json` 中的 `knowledge_root` 字段。
> - 已配置且路径存在 → 下表中所有 `{knowledge_root}/...` 路径使用配置的外部路径
> - 未配置 或 路径不存在 → 降级使用 `{skill_root}/modules/` 和 `{skill_root}/references/` 下的内置知识（映射关系见 `system.md` 知识库路径与降级规则章节），且 `{knowledge_root}/domains/` 子系统特定知识不可用，跳过子系统/模块级配置加载

按优先级加载，高优先级覆盖低优先级：

| 优先级 | 配置 | 路径 | 必须 |
|--------|------|------|------|
| 1（基础） | 核心配置规范 | `{knowledge_root}/common/xts_experience/09_project_data/subsystem_config_spec.md` | ✅ |
| 2（子系统） | 子系统通用配置 | `{knowledge_root}/domains/{Subsystem}/xts_experience/_common.md` | 如有 |
| 3（模块） | 模块特定配置 | `{knowledge_root}/domains/{Subsystem}/xts_experience/{Module}.md` | 如需 |

先检查子系统配置是否存在：

```bash
ls {knowledge_root}/domains/{Subsystem}/xts_experience/
```

不存在时降级为基础配置，后续 Phase 按通用规则处理。

---

### 步骤 3: 校验测试套与 ETS 版本匹配（条件性）

**仅当用户同时指定了目标测试套路径和 ETS 版本时执行**，否则跳过。

检查目标测试套的 `build-profile.json5` 中的 `arkTSVersion` 字段：

```bash
cat {target_test_suite}/build-profile.json5
```

| 用户指定 ETS | 工程 arkTSVersion | 处理 |
|-------------|-------------------|------|
| ets1.1（动态） | 无该字段 | ✅ 匹配 |
| ets1.1（动态） | `"1.2"`（静态工程） | ⚠️ **冲突**：动态语法用例放入静态工程将无法编译，提示用户确认 |
| ets1.2（静态） | `"1.2"` | ✅ 匹配 |
| ets1.2（静态） | 无该字段（动态工程） | ⚠️ **冲突**：静态语法用例放入动态工程将无法编译，提示用户确认 |

冲突时**不自动修改**，向用户报告并等待确认。
