# 使用方式与工作流程

> Prompt 模板、使用场景、12-Phase 完整工作流详解

## 目录

- [一、Prompt 模板](#一prompt-模板)
- [二、使用场景](#二使用场景)
- [三、工作流程详解](#三工作流程详解)

---

## 一、Prompt 模板

> 用户填写以下模板，技能将根据提供的信息**自动判定意图、路由到对应 Phase**，无需手动指定执行阶段。

### 生成类（测试用例生成）

用于生成新的测试用例，走 Phase 0 → 11 完整流程。

```
请为指定范围补充 XTS 测试用例。

【必填】
- 目标接口范围（以下任选一种或组合）：
  □ d.ts 文件路径：{例如 component/text.d.ts}
  □ Kit 名称：{例如 ArkUI}
  □ 类名：{例如 TextAttribute}
  □ 接口/方法名：{例如 fontFeature}
- 子系统：{例如 ArkUI开发框架}

【可选】
- ETS 版本：{ets1.1（默认）/ ets1.2}
- 覆盖率报告：{提供文件路径或内容，有则填，无则自动走 APICoverageDetector 扫描}
- 是否为新增接口：{是/否，是则跳过 before 扫描}
- 测试目录：{例如 test/xts/acts/arkui/，不填则自动推断}
- 分批大小：{每批 API 数量，不填则在 API>20 时自动分批}
- 其他要求：{例如 "包含 UI 类用例"、"需生成 Demo 和 UiTest" 等}
```

### 编译类（仅编译 / 重新编译）

测试代码已存在，只需编译验证。跳过 Phase 1-7，直接进入 Phase 8。

```
请编译验证以下 XTS 测试套。

- 子系统：{例如 ArkUI开发框架}
- 测试目录：{例如 test/xts/acts/arkui/ace_ets_text/}
```

### 扫描类（仅覆盖率扫描 / 报告）

只想查看覆盖率情况，不生成测试代码。

```
请扫描以下范围的 XTS 覆盖率并生成报告。

- 目标接口范围（以下任选一种或组合）：
  □ d.ts 文件路径：{例如 component/text.d.ts}
  □ Kit 名称：{例如 ArkUI}
  □ 类名：{例如 TextAttribute}
  □ 接口/方法名：{例如 fontFeature}
- 子系统：{例如 ArkUI开发框架}

【可选】
- ETS 版本：{ets1.1（默认）/ ets1.2}
- 是否生成对比报告：{是/否}
- 对比基准文件：{.coverage_data/iter-{N}/coverage_report_before_{ver}_{ts}.json，不填则仅生成单点报告}
```

### 验证类（仅格式验证 / 覆盖率验证）

代码已生成，只想做格式检查或覆盖率对比。

```
请对以下 XTS 测试代码执行{格式验证 / 覆盖率验证}。

- 子系统：{例如 ArkUI开发框架}
- 测试目录：{例如 test/xts/acts/arkui/ace_ets_text/}
```

### 恢复类（从断点继续）

上次流程中断，从指定 Phase 继续。

```
请继续执行上次中断的 XTS 测试生成任务。

- 上次中断位置：{例如 Phase 5}
- 子系统：{例如 ArkUI开发框架}
- 已有产出：{例如 "设计文档已有"、"Phase 3 的 uncovered_apis.json 已生成"}
```

### 自动路由规则

| 用户填写内容 | 自动判定 |
|-------------|---------|
| 开场白含"补充…测试用例" | 生成类 → Phase 0 → 11 |
| 开场白含"编译" | 编译类 → Phase 8 |
| 开场白含"扫描…覆盖率" | 扫描类 → Phase 1 → 2 → 停止 |
| 开场白含"格式验证" | 验证类 → Phase 7 |
| 开场白含"覆盖率验证" | 验证类 → Phase 10 |
| 开场白含"继续执行" | 恢复类 → 指定 Phase → 11 |
| 提供覆盖率报告 | Flow A |
| 无覆盖率报告 | Flow B |
| 是否为新增接口=是 | Flow C |

---

## 二、使用场景

### 生成类场景

**场景 1：最简用法（仅指定 d.ts 文件）**

```
请为指定范围补充 XTS 测试用例。
- d.ts 文件路径：component/text.d.ts
- 子系统：ArkUI开发框架
```

**场景 2：提供覆盖率报告（Flow A）**

```
请为指定范围补充 XTS 测试用例。
- d.ts 文件路径：component/text.d.ts
- 类名：TextAttribute
- 子系统：ArkUI开发框架
- 覆盖率报告：{粘贴报告内容或路径}
```

**场景 3：新增接口（Flow C）**

```
请为指定范围补充 XTS 测试用例。
- d.ts 文件路径：component/text.d.ts
- 类名：TextAttribute
- 接口/方法名：fontFeature、wordBreak
- 子系统：ArkUI开发框架
- 是否为新增接口：是
```

**场景 4：指定 Kit + 类名**

```
请为指定范围补充 XTS 测试用例。
- Kit 名称：ArkUI
- 类名：TextAttribute
- 子系统：ArkUI开发框架
```

**场景 5：分批执行**

```
请为指定范围补充 XTS 测试用例。
- d.ts 文件路径：component/rich_editor.d.ts
- 子系统：ArkUI开发框架
- 分批大小：10
```

**场景 6：多 d.ts 文件**

```
请为指定范围补充 XTS 测试用例。
- d.ts 文件路径：component/list.d.ts、component/grid.d.ts
- 子系统：ArkUI开发框架
```

**场景 7：指定接口名**

```
请为指定范围补充 XTS 测试用例。
- d.ts 文件路径：component/text.d.ts
- 接口/方法名：fontFeature
- 子系统：ArkUI开发框架
```

**场景 8：包含 UI 类用例（Demo + UiTest）**

```
请为指定范围补充 XTS 测试用例。
- d.ts 文件路径：component/list.d.ts
- 子系统：ArkUI开发框架
- 其他要求：包含 UI 类用例，需生成 Demo 和 UiTest
```

**场景 9：静态语法项目（ArkTS-Sta）**

```
请为指定范围补充 XTS 测试用例。
- d.ts 文件路径：component/text.d.ts
- 子系统：ArkUI开发框架
- ETS 版本：ets1.2
```

**场景 10：多版本同时生成**

```
请为指定范围补充 XTS 测试用例。
- d.ts 文件路径：component/text.d.ts
- 子系统：ArkUI开发框架
- ETS 版本：ets1.1、ets1.2
```

**场景 11：指定迭代阶段**

```
请为指定范围补充 XTS 测试用例。
- d.ts 文件路径：component/text.d.ts
- 子系统：ArkUI开发框架
- 其他要求：第 2 轮迭代，基于 iter-1 的 after 数据作为 before 基线
```

**场景 12：按子系统全量补充**

```
请为指定范围补充 XTS 测试用例。
- 子系统：ArkUI开发框架
```

### 编译类场景

**场景 13：仅编译验证**

```
请编译验证以下 XTS 测试套。
- 子系统：ArkUI开发框架
- 测试目录：test/xts/acts/arkui/ace_ets_text/
```

**场景 14：SDK 补齐后重新编译**

```
请编译验证以下 XTS 测试套。
- 子系统：ArkUI开发框架
- 测试目录：test/xts/acts/arkui/
- 说明：SDK 已补齐，请重新编译
```

**场景 15：编译失败后修复重试**

```
请编译验证以下 XTS 测试套。
- 子系统：ArkUI开发框架
- 测试目录：test/xts/acts/arkui/ace_ets_text/
- 说明：已修复编译错误，请重新编译
```

### 扫描类场景

**场景 16：仅扫描覆盖率（不生成用例）**

```
请扫描以下范围的 XTS 覆盖率并生成报告。
- d.ts 文件路径：component/text.d.ts
- 子系统：ArkUI开发框架
```

**场景 17：查看覆盖率对比报告**

```
请扫描以下范围的 XTS 覆盖率并生成报告。
- Kit 名称：ArkUI
- 子系统：ArkUI开发框架
- 是否生成对比报告：是
- 对比基准文件：.coverage_data/iter-1/coverage_report_before_ets1.1_xxx.json
```

**场景 18：扫描指定接口的覆盖率**

```
请扫描以下范围的 XTS 覆盖率并生成报告。
- d.ts 文件路径：component/text.d.ts
- 类名：TextAttribute
- 接口/方法名：fontFeature
- 子系统：ArkUI开发框架
```

### 验证类场景

**场景 19：仅格式验证**

```
请对以下 XTS 测试代码执行格式验证。
- 子系统：ArkUI开发框架
- 测试目录：test/xts/acts/arkui/ace_ets_text/
```

**场景 20：仅覆盖率验证（不编译）**

```
请对以下 XTS 测试代码执行覆盖率验证。
- 子系统：ArkUI开发框架
- 测试目录：test/xts/acts/arkui/ace_ets_text/
```

### 恢复类场景

**场景 21：从断点继续**

```
请继续执行上次中断的 XTS 测试生成任务。
- 上次中断位置：Phase 5
- 子系统：ArkUI开发框架
- 已有产出：设计文档已有
```

**场景 22：设计文档已有，直接生成代码**

```
请继续执行上次中断的 XTS 测试生成任务。
- 上次中断位置：Phase 5
- 子系统：ArkUI开发框架
- 已有产出：Phase 4 设计文档已生成，位于 {设计文档路径}
```

### 场景 → Phase 路由速查

| 场景类型 | 执行范围 |
|---------|---------|
| 生成类（默认） | Phase 0 → 11 |
| 生成类 + 新增接口 | Phase 0 → 11（Flow C，跳过 Phase 2 扫描） |
| 编译类 | Phase 8 |
| 扫描类 | Phase 1 → 2 → 停止 |
| 扫描类 + 对比 | Phase 1 → 2 → 10 → 停止 |
| 格式验证 | Phase 7 |
| 覆盖率验证 | Phase 10 |
| 恢复类 | 指定 Phase → 11 |

---

## 三、工作流程详解

### 流程总览

```
Phase 0          Phase 1         Phase 2              Phase 3           Phase 4
初始化配置  →  任务配置  →  覆盖率扫描+报告  →  API深度解析  →  测试设计文档

     Phase 5A/5/5B（测试代码生成，可并行）
          ↓
Phase 6         Phase 7         Phase 8         Phase 9         Phase 10        Phase 11
注册测试  →  格式验证  →  编译验证  →  设备测试  →  覆盖率验证  →  输出结果
```

### Flow 判定规则（Phase 1 步骤 0 检测，优先级从高到低）

| 优先级 | 条件 | Flow | 说明 |
|--------|------|------|------|
| 1 | 用户明确说明"新增接口"/"新 API" | **Flow C** | 跳过 before 扫描，覆盖率为 0 |
| 2 | 用户提供了覆盖率报告（CSV/XLSX/JSON/MD） | **Flow A** | 基于报告解析覆盖缺口 |
| 3 | 以上均不满足 | **Flow B** | 标准 APICoverageDetector 扫描 |

### Phase 1：配置加载

1. 读取 `.oh-xts-config.json`（首次使用从 `.oh-xts-config.example.json` 初始化）
2. 从用户消息中提取 d.ts 文件路径（如 `component\text.d.ts`）
3. 通过 `references/component_subsystem_mapping.json`（360+ 组件→56 子系统映射）确定所属子系统
4. 通过目标工程的 `build-profile.json5` 中 `arkTSVersion` 判断语法类型（ArkTS-Dyn / ArkTS-Sta）
5. 加载子系统配置：`references/subsystems/{Subsystem}/_common.md` + 模块配置

### Phase 2：覆盖率扫描（确定覆盖缺口）

#### Flow B 详细步骤（最常见）

| 步骤 | 操作 | 脚本 |
|------|------|------|
| 1 | 准备扫描环境（复制子系统文件+SDK到扫描目录） | `manage_scan_env.py setup --subsystem {Subsystem}` |
| 2 | 启动异步扫描，轮询等待完成（30-60 分钟） | `async_coverage_scan.py start` → `status` → `get_results` |
| 3 | 按 d.ts 文件筛选，提取未覆盖 API | `extract_uncovered.py --dts-file "component\\text.d.ts"` |
| 3.5 | 可选：Excel→CSV 转换 | `convert_results.py --iter 1 --phase before` |
| 3.6 | 生成覆盖率 MD 报告（生成前） | `generate_coverage_report.py --phase before --dts-file "..."` |

#### 8 维度（AQ-AX 列，独立判断）

| 维度 | 说明 | 对应 Excel 列 |
|------|------|---------------|
| call | 调用覆盖 | AQ |
| param | 入参覆盖 | AR |
| param_spec | 参数规格覆盖 | AS |
| return_value | 返回值覆盖 | AT |
| error_code | 错误码覆盖 | AU |
| permission | 权限覆盖 | AV |
| stage | stagemodel 标签覆盖 | AW |
| meta | 元服务覆盖 | AX |

#### Phase 2 输出文件

| 文件 | 内容 |
|------|------|
| `uncovered_apis_{ts}.json` | 未覆盖 API（Phase 3 输入） |
| `manual_confirm_{ts}.json` | 需人工确认的 API |
| `coverage_report_before_{ver}_{ts}.md` | 生成前覆盖率报告（Phase 10 对比基准） |
| `coverage_report_before_{ver}_{ts}.json` | 结构化数据（供 `--compare-with` 引用） |

### Phase 3：API 深度解析

仅解析 Phase 2 识别出的**未覆盖 API**，构建完整知识库。

#### 信息源优先级

| 信息源 | 获取内容 | 优先级 |
|--------|---------|--------|
| .d.ts 文件 | 方法签名、参数类型、返回值、@throws 错误码、@since 版本 | 最高 |
| 官方文档 | 使用场景、限制条件、最佳实践 | 高 |
| 现有测试 | 断言方法、代码模式、错误处理 | 中 |
| 子系统配置 | 特殊规则、命名规范 | 补充 |

#### 信息源降级策略

| 缺失的信息源 | 处理方式 |
|-------------|---------|
| .d.ts 文件 | **终止**该 API 解析（无法 import，代码无法编译） |
| 官方文档 | 降级：仅使用 .d.ts + 现有测试 + 子系统配置 |
| 现有测试 | 降级：使用通用模板 |
| 子系统配置 | 降级：仅使用核心配置 |
| 全部缺失 | **终止**该 API 解析 |

### Phase 4：生成测试设计文档（**强制**，不可跳过）

为每个未覆盖 API 生成 `.design.md`：

- 测试场景设计（PARAM / ERROR / RETURN / BOUNDARY）
- 测试用例列表（含预期结果）
- **控件 ID 契约**（UI 类用例的 Demo ↔ UiTest 控件 ID 预定义）
- 分批执行计划（API > 20 或复杂场景时分批）

### Phase 5：测试代码生成

#### 执行顺序

```
Phase 5A（用例分类 + Demo 生成）— 仅 UI 类
     ↓
Phase 5（非 UI 类）| Phase 5B（UiTest）| Phase 5A Step1（Demo）— 并行
     ↓
Demo + UiTest 同 HAP 编译
```

#### 生成时加载的规范

| 规范文件 | 用途 |
|---------|------|
| `references/conventions/hypium_framework.md` | 断言方法 |
| `references/conventions/test_conventions.md` | 命名规范 |
| `references/conventions/arkts_standards.md` | ArkTS 语法 |
| `references/conventions/ets_version_naming.md` | ETS 版本命名（影响目录名/bundleName/hap_name） |
| `references/subsystems/{Subsystem}/_common.md` | 子系统特有规则 |

### Phase 6：注册测试

在 List.test.ets 中注册新测试文件：

```bash
python {skill_root}/scripts/register_test.py
```

### Phase 7：格式验证（**强制**，不可跳过）

| 步骤 | 内容 |
|------|------|
| A | `validate_test_context.py` 检查 5/9 项 + `arkts-static-spec` 校验（仅 ArkTS-Sta） |
| B | `check-test-code-quality` 技能执行 11 条规则深度扫描 |

### Phase 8：编译验证（推荐）

独立编译模式：
- Linux: `build_workflow_linux.md`
- Windows: `build_workflow_windows.md`

### Phase 10：覆盖率验证 + 报告

| 步骤 | 操作 | 脚本 |
|------|------|------|
| 10.1 | 再次执行 APICoverageDetector 扫描 | `async_coverage_scan.py` |
| 10.2 | 保存 after_generation CSV | `convert_results.py --phase after` |
| 10.4 | 生成覆盖率 MD 报告（生成后）+ before/after 对比 | `generate_coverage_report.py --phase after --compare-with before.json` |

#### 对比报告内容

| 章节 | 内容 |
|------|------|
| 总体变化 | 已覆盖接口数、覆盖率的 before → after 变化 |
| 8 维度变化 | 每个维度的覆盖率变化 |
| 新增覆盖的接口 | API + 新覆盖维度 + 原未覆盖 → 现已覆盖 |
| 仍然未覆盖的接口 | API + 未覆盖维度 + 优先级 |

### Phase 11：输出结果

- 文件清单（所有新建/修改的 .test.ets 文件）
- 测试设计文档路径
- 覆盖率报告文件路径
- 覆盖率变化表
- 工作流执行检查清单（`phase_tracker.py report`）
- 上库前检查提醒（删除 hypium、注释 test_hap、命名合规、签名文件等）

### 关键约束

1. **Phase 4/7 不可跳过** — 设计文档和格式验证是质量门禁
2. **严格遵循 .d.ts 声明** — 未声明的接口在编译环境中不存在
3. **@tc 注解必须** — 每个测试用例必须有标准 @tc 块
4. **ETS 版本命名规范** — 目录名/bundleName/hap_name 必须符合 `ets_version_naming.md`
5. **Demo-UiTest 三方契约** — 控件 ID 在设计文档预定义，三方必须一致
6. **不修改 BUILD.gn** — 仅在指定目录创建测试文件
