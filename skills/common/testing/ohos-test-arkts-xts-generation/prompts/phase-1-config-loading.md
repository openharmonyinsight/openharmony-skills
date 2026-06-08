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

### 步骤 0: Issue 日志初始化（必须执行）

> ⚠️ **这是 Phase 1 的第一步，在任何其他操作之前执行。**

1. 确认 `{skill_root}/.task_summary/` 目录存在（不存在则 `mkdir -p` 创建）
2. 在 `{skill_root}/.task_summary/` 下创建 `session_issues_{日期}.md`
3. 写入会话头信息（日期、子系统、模块、Flow 类型、目标）
4. 整个任务执行过程中，**遇到问题时立即追加 issue 记录**

---

### 步骤 0.5: 依赖 Skill 兼容性校验

> 在正式开始任务前校验依赖 skill 的版本和能力兼容性。

1. 检查 `{skill_root}/.probe_results` 是否存在且修改时间 < 24 小时：
   ```bash
   test -f {skill_root}/.probe_results && find {skill_root}/.probe_results -mmin -1440 | grep -q .
   ```
2. 如果文件不存在或已过期，执行：
   ```bash
   bash {skill_root}/scripts/install_related_skills.sh --check-probes
   ```
3. 读取 `{skill_root}/.probe_results`，根据每行的 status 列采取行动：

| status | 含义 | 行动 |
|--------|------|------|
| `OK` | 版本和探测均通过 | 继续 |
| `WARN_VERSION` | 版本未知但探测通过 | 警告，继续 |
| `MISSING_OPTIONAL` | 可选 skill 未安装 | 警告，相关 Phase 自动降级 |
| `MISSING` | 必选 skill 未安装 | **阻断**：提示运行 `install_related_skills.sh` |
| `VERSION_LOW` | 版本低于 min_version | **阻断**：提示运行 `install_related_skills.sh --force` |
| `FAIL_PROBES` | 探测失败（接口不兼容） | **阻断**：提示运行 `install_related_skills.sh --force` |

4. 阻断时向用户展示具体失败项和建议命令，**不自动执行安装**
5. 将校验结果追加到 `session_issues_{日期}.md`

**Issue 记录触发条件**：

| 触发场景 | 示例 |
|---------|------|
| 编译失败 | 语法错误、类型错误、缺失依赖 |
| 测试执行失败 | 路由未注册、断言失败、页面渲染空白 |
| 覆盖率异常 | 扫描超时、结果不符合预期 |
| 工具/脚本错误 | 脚本报错、hdc 连接失败、APICoverageDetector 崩溃 |
| 工作流缺陷发现 | Phase 缺少步骤、prompt 描述不准确 |

**Issue 记录格式**：

```markdown
## Issue N: {简要标题}

- **严重程度**: Critical / High / Medium / Low
- **发现阶段**: Phase {N} - {Phase 名称}
- **症状**: {具体症状描述，包含错误信息}
- **根因**: {识别到的根本原因}
- **影响**: {对后续工作流的影响}
- **修复方法**: {如何修复的，或建议的优化方案}
- **建议优化**: {如何防止类似问题再次出现（如修改 prompt、脚本等）}
```

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

---

### 步骤 4: 多版本串行生成模式（仅 ets_version 含 ets1.2 时）

当 `ets_version` 为 `["ets1.1", "ets1.2"]` 时启用串行生成模式（**禁止并行编译**，因为 hvigor 版本不兼容）：

> **核心约束**：动态版本（ets1.1）和静态版本（ets1.2）需要不同的 hvigor 版本，不能同时编译。必须先完成完整的 1.1 流程（生成→注册→验证→编译通过），然后切换环境再执行 1.2。

```
Phase 1~4（执行一次，结果共享）
  → Phase 5A: 生成 ets1.1 动态测试用例（跳过 [sta-only]）
  → Phase 6A: 注册 ets1.1 测试套
  → Phase 7A: 验证 ets1.1 测试套
  → Phase 8A: 编译 ets1.1（使用 prebuilts_for_dyn）→ 修复直至通过
  → Phase 5B: 语法迁移 1.1→1.2（共享用例）+ 补充 [sta-only] 用例
  → Phase 6B: 注册 ets1.2 测试套
  → Phase 7B: 验证 ets1.2 测试套
  → Phase 8B: 备份 prebuilts → 切换到 prebuilts_for_sta → 编译 ets1.2 → 修复直至通过
  → Phase 9~11（执行一次）
```

| Phase | 行为 | 说明 |
|-------|------|------|
| 1-4 | 执行一次 | 覆盖率扫描/API 解析/设计文档跨版本共享 |
| 5A | 生成 ets1.1 | 仅动态测试用例，跳过 `[sta-only]` |
| 6A-7A | 注册+验证 ets1.1 | 动态版本测试套 |
| 8A | 编译 ets1.1 | 使用 `prebuilts`（动态 SDK），修复直至通过 |
| 5B | 迁移+补充 ets1.2 | 1.1→1.2 语法迁移（共享用例）+ 补充 `[sta-only]` 用例 |
| 6B-7B | 注册+验证 ets1.2 | 静态版本测试套 |
| 8B | 编译 ets1.2 | 切换 `prebuilts`（见下方切换机制），修复直至通过 |
| 9-11 | 执行一次 | 覆盖率统计合并 |

#### prebuilts 环境切换机制

动态和静态版本使用不同的 SDK/hvigor，通过切换 `prebuilts` 目录实现：

| 目录 | 用途 | ohos-sdk/linux/26/ets/ | hvigor 版本 |
|------|------|----------------------|-------------|
| `prebuilts_for_dyn` | 动态编译环境 | 直接包含 `api/arkts/build-tools/component/kits`（无 dynamic/static 子目录） | 5.x |
| `prebuilts_for_sta` | 静态编译环境 | 包含 `dynamic/` 和 `static/` 子目录 | `6.0.0-arkts1.2-ohosTest-*` |
| `prebuilts`（当前激活） | 实际编译使用 | 从上述两者之一软链接或重命名 | — |

**切换流程**（Phase 8B 编译静态版本时）：

```bash
cd {OH_ROOT}

# 1. 首次备份当前动态环境
if [ ! -d prebuilts_for_dyn ]; then
    mv prebuilts prebuilts_for_dyn
fi

# 2. 检查静态环境是否已存在
if [ -d prebuilts_for_sta ]; then
    mv prebuilts prebuilts_for_dyn 2>/dev/null
    mv prebuilts_for_sta prebuilts
else
    # 首次：下载并配置静态环境
    mv prebuilts prebuilts_for_dyn
    git clone https://gitee.com/laoji-fuli/hvigor0702.git -b debug2 prebuilts
fi

# 3. 验证静态环境
cat prebuilts/command-line-tools/hvigor/hvigor/package.json | grep '"version"'
# 应为 6.0.0-arkts1.2-ohosTest-*
ls prebuilts/ohos-sdk/linux/26/ets/dynamic prebuilts/ohos-sdk/linux/26/ets/static
# 两个目录都应存在
```

**切回动态**（下次编译动态版本时需要）：

```bash
cd {OH_ROOT}
mv prebuilts prebuilts_for_sta
mv prebuilts_for_dyn prebuilts
```
