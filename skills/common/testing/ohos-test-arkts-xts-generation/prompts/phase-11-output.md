## Phase 11: Output Results

---

### ⚙️ 按需加载

本 Phase 不需要额外加载模块。

---

### 🚫 Do NOT Load - 禁止加载

本 Phase 期间禁止加载以下模块：

```
所有模块（仅输出结果）
```

---

### 输出总览

Phase 11 输出一份完整的生成报告，包含以下章节：

1. 任务信息
2. 生成文件清单
3. 测试用例统计
4. 覆盖率总结（核心）
5. 设备测试执行结果（如执行了 Phase 9）
6. 待人工确认事项
7. 工作流执行检查清单
8. 上库前检查清单

---

### 报告模板

```markdown
# XTS 测试用例生成报告

## 1. 任务信息

| 项目 | 值 |
|------|---|
| 日期 | {YYYY-MM-DD} |
| 子系统 | {Subsystem}（如 ArkUI） |
| 测试套 | {测试套1}、{测试套2}、...（单套时仅列一个） |
| d.ts 文件 | {文件名}（如 component/text.d.ts） |
| Flow 类型 | Flow A / Flow B / Flow C（新增接口） |
| ETS 版本 | ets1.1（动态）/ ets1.2（静态）/ 两者 |
| 目标 API 数量 | {N} 个 |
| 生成用例数量 | {M} 个 |

---

## 2. 生成文件清单

> 多测试套时按套分组，单测试套时直接列出。

### {测试套1 名称}（如 ActsAceEtsModuleImageTextTextTest）

#### 测试文件

| 文件 | 路径 | 用例数 | 行数 |
|------|------|--------|------|
| {TestFile1}.test.ets | {relative_path} | {N} | {L} |
| {TestFile2}.test.ets | {relative_path} | {N} | {L} |
| **小计** | `{测试套根目录相对路径}` | **{subtotal}** | **{subtotal_lines}** |

#### Demo 页面文件

| 文件 | 路径 | 类型 | 组件数 |
|------|------|------|--------|
| {Demo1}.ets | {relative_path} | 新建 / 复用 | {N} |

#### 设计文档

| 文件 | 路径 |
|------|------|
| {Design1}.test.design.md | {relative_path} |

#### 路由注册

| 页面路由 | 状态 |
|---------|------|
| MainAbility/pages/{SubDir}/{PageName} | ✅ 新注册 / 已存在 |

---

### {测试套2 名称}

（结构同上，每个测试套重复一组）

---

### 总计

| 指标 | 数量 |
|------|------|
| 测试套数 | {S} |
| 测试文件数 | {F} |
| Demo 页面数 | {D}（新建 {D1} / 复用 {D2}） |
| 总用例数 | **{total}** |

---

## 3. 覆盖率总结

### 3.1 覆盖率变化概览

> 数据来源：APICoverageDetector 扫描结果

**Flow A / Flow B（有 before 对比）**：

| 指标 | 生成前 | 生成后 | 变化 |
|------|--------|--------|------|
| API 总数 | {Y} | {Y} | — |
| 已覆盖 API（全维度） | {X} | {X+M} | **+{M}** |
| 部分覆盖 API | {A} | {A±N} | {±N} |
| 未覆盖 API | {B} | {B-R} | **-{R}** |

**Flow C（新增接口，无 before 基线）**：

| 指标 | 值 | 说明 |
|------|---|------|
| API 总数 | {Y} | 本次新增的全部接口 |
| 已覆盖 API | {M} | 首次覆盖 |
| 覆盖率 | {M/Y}% | 新增接口首次覆盖 |

### 3.2 八维度覆盖率明细

> APICoverageDetector 从 8 个维度评估每个 API 的覆盖情况。

**数据格式规则**：
- **Flow A / Flow B**（生成前后均扫描了覆盖率）：格式为 `{生成前} → {生成后}`，体现变化趋势
- **Flow C / 仅生成后扫描**（无 before 基线）：直接填写已覆盖 API 数

> **示例**（Flow A/B）：`param: 45 → 58` 表示生成前 45 个 API 的入参被覆盖，生成后增加到 58 个。
> **示例**（Flow C / 仅 after）：`param: 12` 表示当前有 12 个 API 的入参已覆盖。

| 维度 | 已覆盖 API 数 | 未覆盖 | 不涉及 | 需人工确认 | 含义 | 判定规则 |
|------|--------------|--------|--------|-----------|------|---------|
| **call** | {N1} → {N2} | {N} | {N} | {N} | 调用覆盖 | 能扫描到 Demo page build() 中的调用，但无法关联 getInspectorByKey 间接断言 → 标记为「需人工确认」 |
| **param** | {N1} → {N2} | {N} | {N} | {N} | 入参覆盖 | 在测试代码中传入不同参数并验证行为 |
| **param_spec** | {N1} → {N2} | {N} | {N} | {N} | 参数规格覆盖 | 仅适用于有详细参数规格定义的 API |
| **return_value** | {N1} → {N2} | {N} | {N} | {N} | 返回值覆盖 | `expect()` 断言了返回值的类型/内容 |
| **error_code** | {N1} → {N2} | {N} | {N} | {N} | 错误码覆盖 | 需 `@throws` 注解声明，每个错误码一个测试 |
| **permission** | {N1} → {N2} | {N} | {N} | {N} | 权限覆盖 | 需要权限的 API 是否测试了有/无权限两种场景 |
| **stage** | {N1} → {N2} | {N} | {N} | {N} | Stage model 标签覆盖 | 组件创建/销毁/前后台切换等场景 |
| **meta** | {N1} → {N2} | {N} | {N} | {N} | 元服务覆盖 | 版本号、废弃标记、SDK 版本等 |
| **全维度已满足** | {N1} → {N2} | — | — | — | — | 所有维度均为「已覆盖」或「不涉及」的 API 数量 |

### 3.3 待人工确认的覆盖维度

> ⚠️ 上表中「需人工确认」列对应的 API 维度需要人工审核确认，自动化工具无法判定。

APICoverageDetector 将某些 API 维度标记为「需人工确认」，这些维度无法通过工具自动判定覆盖与否，需要测试开发者人工审核。

**call 维度 — ArkUI Inspector 模式（最常见的确认类型）**：

APICoverageDetector 的 `call` 维度能扫描到 Demo 页面 `build()` 中对 API 的调用（如 `Text('hello').fontColor(Color.Red)`），但**无法识别对应的断言**。因为 ArkUI 属性 API 采用 Demo page + `getInspectorByKey` 测试模式时：
- API 调用在 Demo 页面的 `build()` 方法中（工具可扫描到）
- 测试函数通过 `getInspectorByKey('component_id')` 读取渲染结果并断言（工具无法将 Demo 中的 API 调用与测试函数中的间接断言关联）

这种模式下，**API 确实被调用且有断言验证**，但工具无法自动建立调用与断言的关联，因此标记为「需人工确认」。这是工具的已知限制，**不代表测试缺失**。

**人工确认操作**：审核测试函数代码，确认对应的 `getInspectorByKey` 断言确实验证了该 API 的效果，即可将 `call` 维度标记为已覆盖。

**需确认清单**：

| API | 所属测试套 | 测试文件 | 确认方式 | 状态 |
|-----|----------|---------|---------|------|
| TextAttribute::{method} | {SuiteName} | {TestFile}.test.ets | 检查 getInspectorByKey 断言验证了该属性效果 | ⬜ 待确认 |
| ... | | | | |

**其他需人工确认的维度**：

| API | 所属测试套 | 维度 | 原因 | 确认操作 | 状态 |
|-----|----------|------|------|---------|------|
| {API名} | {SuiteName} | {维度名} | {为什么工具无法判定} | {需要人做什么} | ⬜ 待确认 |

### 3.4 新增覆盖的 API

**本次新生成测试用例直接覆盖的 API**：

| API | 所属测试套 | 新覆盖维度 | 仍缺维度 | 测试文件 |
|-----|----------|-----------|---------|---------|
| TextAttribute::fontFeature | {SuiteName} | +param | call(需确认), return_value | TextFontFeatureTest.test.ets |
| TextAttribute::incrementalUpdatePolicy | {SuiteName} | +param | call(需确认), return_value | TextIncrementalUpdatePolicyTest.test.ets |
| TextAttribute::orphanCharOptimization | {SuiteName} | +param | call(需确认), return_value | TextOrphanCharOptimization.test.ets |
| ... | | | |

### 3.5 仍需补充测试的 API

以下 API 在本次生成后仍有未覆盖维度，建议后续迭代补充：

| API | 未覆盖维度 | 优先级 | 建议 |
|-----|-----------|--------|------|
| TextAttribute::{method} | return_value | 中 | 需验证链式调用返回 TextAttribute |
| TextAttribute::onCopy | call, param, return_value | 高 | 回调类事件，需专门的事件触发测试 |
| ... | | | |

### 3.6 已知限制说明

| 限制 | 影响范围 | 说明 |
|------|---------|------|
| APICoverageDetector call 维度 | 所有 ArkUI 属性 API | Inspector 模式下能扫描到调用但无法关联 getInspectorByKey 间接断言 |
| return_value 维度 | 大部分属性 API | 链式调用返回 TextAttribute 自身，工具不识别为有效返回值测试 |
| param_spec 维度 | 全部 API | 当前 d.ts 缺少参数规格说明，该维度全部为「不涉及」 |

### 3.7 覆盖率报告文件

| 文件 | 路径 | 说明 |
|------|------|------|
| 生成前报告 | `.coverage_data/iter-{N}/coverage_report_before_{ver}_{timestamp}.md` | 生成前 8 维度覆盖率详情 |
| 生成后报告 | `.coverage_data/iter-{N}/coverage_report_after_{ver}_{timestamp}.md` | 生成后 8 维度覆盖率详情 |
| 对比报告 | `.coverage_data/iter-{N}/coverage_comparison_{timestamp}.md` | before → after 变化对比 |

> 详细报告包含：8 维度覆盖率统计、已覆盖接口列表（含已覆盖场景）、未覆盖接口列表（含优先级）、覆盖率变化对比。请查看上述 MD 文件。

---

## 4. 设备测试执行结果

> 本章节仅在执行了 Phase 9 时出现，跳过时标注「跳过 — {原因}」

### 执行环境

| 项目 | 值 |
|------|---|
| 执行方案 | WSL 原生 / Windows PowerShell / 跳过 |
| 设备 SN | {device_sn} |
| 设备类型 | Phone / Tablet |
| 执行耗时 | {X}m{Y}s |
| 执行命令 | `python3 -m xdevice run -l {TestName} -t ACTS` |

### 测试结果汇总

| 结果 | 数量 | 占比 |
|------|------|------|
| ✅ 通过 | {N} | {Pct}% |
| ❌ 失败 | {N} | {Pct}% |
| ⏭️ 忽略 | {N} | {Pct}% |
| 🚫 不可用 | {N} | {Pct}% |
| **合计** | **{total}** | 100% |

### 失败用例分析

> 无失败时标注「全部通过 ✅」

| 失败套件 | 失败数 | 错误类型 | 根因 | 新/旧 | 处理方式 |
|---------|--------|---------|------|-------|---------|
| {SuiteName} | {N} | beforeEach 错误 / Empty Text / 断言失败 | 路由未注册 / 属性值不匹配 / ... | 新 / 旧 | 已修复 / 记录 / 回退 Phase {N} |

---

## 5. 工作流执行检查清单

| 状态 | Phase | 结果 |
|------|-------|------|
| ✅ | Phase 1 配置加载 | 通过 |
| ✅ | Phase 2 覆盖率扫描（before） | 通过 |
| ✅ | Phase 3 API 解析 | 通过 |
| ✅ | Phase 4 测试设计文档 | 通过 |
| ✅ | Phase 5 测试代码生成 | 通过 |
| ✅ | Phase 6 测试注册 + Demo 页面路由注册 | 通过 |
| ✅ | Phase 7 格式验证 | 通过 |
| ✅/⏭️ | Phase 8 编译验证 | 通过 / 跳过 — {原因} |
| ✅/⏭️ | Phase 9 设备测试执行 | 通过 / 跳过 — {原因} |
| ✅/⏭️ | Phase 10 覆盖率验证 | 通过 / 跳过 — {原因} |
| ✅ | Phase 11 结果输出 | 通过 |

**未通过/跳过的 Phase 必须标注原因和后续计划。**

---

## 6. 上库前检查清单

> ⚠️ **上库提醒**：请确认已完成以下操作后再 git push

| 检查项 | 说明 | 不执行的后果 |
|--------|------|------------|
| **删除 hypium 文件夹** | 本地编译验证需要 hypium，但 git push 上库前必须删除 | hypium 文件夹随测试代码入库 → 仓库体积膨胀、CI 脚本冲突 |
| **BUILD.gn test_hap 注释** | `test_hap = true` 行必须注释掉 | ohosTest 当前不可用，未注释 → 编译报错 |
| **命名合规性** | 目录名、bundleName、hap_name、用例名符合 `ets_version_naming.md` | 不合规 → CodeCheck 门禁拦截 PR |
| **Test.json 一致性** | `module-name` = "entry"，`test-file-name` = hap_name | 不一致 → 测试无法执行 |
| **签名文件** | signature/ 下必须有 .p7b 文件 | 缺失 → HAP 无法安装 |
| **main_pages.json 完整性** | 所有 Demo 页面路由已注册 | 路由缺失 → 设备测试 100% 失败 |
| **人工确认覆盖率** | 审核 §3.3 清单中的 call 等维度 | 覆盖率数据不准确 |
```

---

### 数据来源

报告中的数据来源于前序 Phase 的产出：

| 章节 | 数据来源 |
|------|---------|
| 文件清单 | Phase 5 生成的文件列表 |
| 测试用例统计 | Phase 4 设计文档 + Phase 5 代码 |
| 覆盖率总结 | Phase 2/10 的 APICoverageDetector 扫描结果 + `extract_uncovered.py` / `compare_uncovered.py` 输出 |
| 设备测试结果 | Phase 9 的 `summary_report.xml` + `summary.ini` + hilog |
| 待人工确认 | Phase 10 的 `manual_confirm_*.json` + `uncovered_apis_*.json` |
| 检查清单 | `phase_tracker.py report` 输出 |

### 输出方式

1. **直接输出到对话**：按上述模板格式，填充实际数据，直接展示给用户
2. **保存报告文件（必须）**：将完整报告保存到 `{skill_root}/.task_summary/session_{日期}_{sessionId}.md`
   - 日期格式：`YYYYMMDD`（如 `20260528`）
   - sessionId：本次会话的唯一标识（如使用启动时间戳 `HHmmss` 或自增序号）
   - 示例路径：`{skill_root}/.task_summary/session_20260528_204538.md`
   - 如果 `{skill_root}/.task_summary/` 目录不存在，先创建
