## Phase 7: Format & Validate (MANDATORY - NEVER SKIP)

---

> **`knowledge_root` 降级**：下文中所有 `{knowledge_root}/...` 路径，若 `knowledge_root` 未配置或路径不存在，则降级从 `{skill_root}/modules/` 和 `{skill_root}/references/` 加载对应内置知识。完整映射表见 `system.md`「知识库路径与降级规则」。

### 📚 参考文档（按需查阅）

本 Phase 执行过程中可参考以下文件，遇到具体问题时按需查阅：

| 文件 | 内容 | 何时查阅 |
|------|------|---------|
| `{knowledge_root}/common/xts_experience/09_methodology/19_format_validator.md` | 格式化验证规则（@tc 注解、导入、命名、断言格式） | 验证规则不确定、需要确认具体校验项时 |

---

### ⚙️ 按需加载（根据验证任务）

以下模块仅在你执行对应任务时才需要加载：

| 任务 | 加载文件 | 说明 |
|------|---------|------|
| 代码质量深度扫描 | check-test-code-quality skill | 步骤B深度扫描（必选） |
| 静态项目语法校验 | arkts-static-spec skill | 静态项目语法校验（仅 ArkTS-Sta） |
| 需要 Hypium 断言参考 | `{knowledge_root}/common/xts_experience/01_framework/01_hypium_framework.md` | 断言方法参考 |
| 需要 ArkTS 语法参考 | `{knowledge_root}/common/xts_experience/02_arkts/01_dynamic_syntax_rules.md` | 语法规范参考 |
| 需要命名规范参考 | `{knowledge_root}/common/xts_experience/03_standards/01_test_naming_convention.md` | 命名规范参考 |
| UI 测试需要 | `{knowledge_root}/common/xts_experience/01_framework/02_uitest_framework.md` | UI 测试框架参考 |

---

### 🚫 Do NOT Load - 禁止加载

本 Phase 期间禁止加载以下模块：

```
所有 L1_Analysis 模块（{knowledge_root}/common/xts_experience/ 下分析与覆盖率工具相关文件）
所有 L2_Generation 模块（{knowledge_root}/common/xts_experience/ 下生成相关文件）
覆盖率工具相关模块（{knowledge_root}/common/xts_experience/ 下工具相关文件）
```

---

**加载模块**:
- `{knowledge_root}/common/xts_experience/09_methodology/19_format_validator.md`

此阶段分两步执行：A) 生成上下文检查（当前 skill 执行）→ B) 代码质量深度扫描（调用 check-test-code-quality）。

### 重要

此阶段是**核心强制步骤**，绝对不可跳过。跳过此阶段将导致：`as any` 类型断言在 ArkTS-Sta 下编译失败、资源泄漏导致设备内存耗尽、空 catch 块使测试永远"通过"而实际未验证、check-test-code-quality 扫描不通过则无法合入代码。

---

### 步骤 A: 生成上下文检查

#### A.1 自动验证脚本（推荐，新增 2026-05-27）

使用 `validate_test.py` 集成验证脚本一次性完成所有检查：

```bash
# 完整模式（测试文件 + 页面文件 + 设计文档）
python {skill_root}/scripts/validate_test.py \
  --test-file {生成文件路径}.test.ets \
  --page-file {页面文件路径}.ets \
  --design-doc {设计文档路径}.design.md

# 仅测试文件模式（无 UI 组件的测试可省略 page-file 和 design-doc）
python {skill_root}/scripts/validate_test.py \
  --test-file {生成文件路径}.test.ets
```

> `--page-file` 和 `--design-doc` 为可选参数。不提供时自动跳过组件id相关检查（A.9-A.11）。

脚本自动检查以下 13 项（根据提供的文件参数动态调整）：

| 检查项 | 说明 | 对应问题 |
|--------|------|---------|
| A.1 无 as any | 无 `as any` 类型断言 | 原有 |
| A.2 无 Function 类型 | 无 `: Function` 或 `: Function)` | 问题6 |
| A.3 无 any/unknown | 无 `: any` 或 `: unknown` | 问题6 |
| A.4 正确的 router 导入 | `@ohos.router` 而非 `@ohos/router` | 问题6 |
| A.5 @tc 注释完整 | 每个 it() 都有 @tc 注释块 | 原有 |
| A.6 it() 名称 camelCase | it() 名称首字母小写 | 原有 |
| A.7 Level 值合法 | Level.LEVEL0~4，无 Level.Level0 | 问题10 |
| A.8 ESObject 类型风格 | JSON.parse 结果用 ESObject | 问题10 |
| A.9 组件id一致性 | 测试中 getInspectorByKey 的 id 在页面中存在 | 问题9 |
| A.10 设计文档组件id | 设计文档每个用例有 `**组件id**` 字段 | 问题9 |
| A.11 设计文档id一致性 | 设计文档中的组件id在页面中存在 | 问题9 |
| A.12 export default function | 测试文件包含 export default | 原有 |
| A.13 hypium 导入 | 测试文件包含 from "@ohos/hypium" 或 from ".../hypium/index"（相对路径） | 原有 |

**处理脚本结果**：全部 PASS 则通过；有 FAIL 则按报告修复后重新运行。

#### A.2 原有 validate_test_context.py（仍可使用）

```bash
python {skill_root}/scripts/validate_test_context.py \
  --file {生成文件路径}.test.ets \
  --expected-module "{被测模块，如 @ohos.multimedia.media}" \
  --design-doc {设计文档路径}.design.md
```

脚本自动检查以下 5 项：

| 检查项 | 说明 | 检测方式 |
|--------|------|---------|
| A.1 许可证头 | Apache 2.0 完整头 | 匹配 `Apache License` + `Version 2.0` + `Copyright` |
| A.2 hypium 导入 | `@ohos/hypium` 或 `.../hypium/index`（相对路径）包含 describe/it/expect | 正则匹配 import 语句 |
| A.3 被测模块导入 | 导入了正确的被测模块 | 匹配 `--expected-module` 参数 |
| A.7 禁止 as any | 无 `as any` 类型断言 | 正则匹配（排除注释行） |
| A.8 设计文档一致性 | 每个 `@tc.number` 在设计文档中有对应条目 | 提取所有 @tc.number 并在 design.md 中搜索 |

**处理脚本结果**：如果脚本输出 `[PASS]`，说明这 5 项全部通过；如果有 `[ISSUES]`，按报告修复后重新运行脚本。

#### 手动检查（模型执行）

以下检查项需要模型理解代码语义，无法正则匹配：

- **A.4 afterEach 资源释放**：afterEach 中释放播放器、文件描述符等资源，使用 try-catch 包裹
- **A.5 null/undefined 安全**：对象使用前先创建/初始化，文件描述符关闭前检查有效性
- **A.6 deprecated API**：不使用已废弃的 API（如 AudioPlayer→AVPlayer）
- **A.9 ArkTS 语法规范**：动态项目遵循 `{knowledge_root}/common/xts_experience/02_arkts/01_dynamic_syntax_rules.md`，静态项目调用 `arkts-static-spec`

---

### 步骤 B: 代码质量深度扫描（必选）

启动 subagent 调用 `check-test-code-quality` 对生成的测试文件执行深度质量扫描：

```
/check-test-code-quality {生成文件路径} --rules R002,R003,R004,R008,R009,R013,R015,R016,R018,R022,R023
```

**扫描结果处理**：

| 结果 | 处理方式 |
|------|---------|
| 0 issues | 通过，进入 Phase 8 |
| 有 issues | 自动修复所有问题 → 重新扫描 → 直到通过 |

**注意**：Phase 5 已在生成时内化了这 11 条规则约束，步骤 B 作为兜底确认。如果扫描发现问题，说明生成阶段遗漏了约束，需修复后重新扫描。

---

### 完成条件

步骤 A 和步骤 B 全部通过后，进入 Phase 8。

- [ ] 许可证头完整
- [ ] hypium 导入正确
- [ ] 被测模块导入正确
- [ ] afterEach 资源释放完整
- [ ] 无 as any 类型断言
- [ ] 设计文档一致
- [ ] ArkTS 语法规范（动态/静态）
- [ ] check-test-code-quality 扫描通过（0 issues）
