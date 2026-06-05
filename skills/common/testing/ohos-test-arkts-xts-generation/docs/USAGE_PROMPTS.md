# Prompt 模板

> 用户填写以下模板，技能将根据提供的信息**自动判定意图、路由到对应 Phase**，无需手动指定执行阶段。

---

## 模板

### 生成类（测试用例生成）

用于生成新的测试用例，走 Phase 1 → 10 完整流程。

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

---

## 自动路由规则

| 用户填写内容 | 自动判定 |
|-------------|---------|
| 开场白含"补充…测试用例" | 生成类 → Phase 1 → 10 |
| 开场白含"编译" | 编译类 → Phase 8 |
| 开场白含"扫描…覆盖率" | 扫描类 → Phase 1 → 2 → 停止 |
| 开场白含"格式验证" | 验证类 → Phase 7 |
| 开场白含"覆盖率验证" | 验证类 → Phase 9 |
| 开场白含"继续执行" | 恢复类 → 指定 Phase → 10 |
| 提供覆盖率报告 | Flow A |
| 无覆盖率报告 | Flow B |
| 是否为新增接口=是 | Flow C |

---

## 使用场景

### 生成类场景

#### 场景 1：最简用法（仅指定 d.ts 文件）

最常见用法。指定 d.ts 文件，自动扫描覆盖率、生成测试、编译验证。

```
请为指定范围补充 XTS 测试用例。

- d.ts 文件路径：component/text.d.ts
- 子系统：ArkUI开发框架
```

#### 场景 2：提供覆盖率报告

已有 APICoverageDetector 报告，跳过耗时扫描，直接从报告提取未覆盖 API。

```
请为指定范围补充 XTS 测试用例。

- d.ts 文件路径：component/text.d.ts
- 类名：TextAttribute
- 子系统：ArkUI开发框架
- 覆盖率报告：{粘贴报告内容或路径}
```

#### 场景 3：新增接口

新 API 尚无任何测试，生成前覆盖率为 0，跳过 before 扫描。

```
请为指定范围补充 XTS 测试用例。

- d.ts 文件路径：component/text.d.ts
- 类名：TextAttribute
- 接口/方法名：fontFeature、wordBreak
- 子系统：ArkUI开发框架
- 是否为新增接口：是
```

#### 场景 4：指定 Kit + 类名

不指定具体 d.ts 文件，按 Kit 和类名筛选。

```
请为指定范围补充 XTS 测试用例。

- Kit 名称：ArkUI
- 类名：TextAttribute
- 子系统：ArkUI开发框架
```

#### 场景 5：分批执行

未覆盖 API 数量较多，分批生成避免上下文溢出。

```
请为指定范围补充 XTS 测试用例。

- d.ts 文件路径：component/rich_editor.d.ts
- 子系统：ArkUI开发框架
- 分批大小：10
```

#### 场景 6：多 d.ts 文件

同时为多个 d.ts 文件补充用例。

```
请为指定范围补充 XTS 测试用例。

- d.ts 文件路径：component/list.d.ts、component/grid.d.ts
- 子系统：ArkUI开发框架
```

#### 场景 7：指定接口名

只关注特定接口，不为整个 d.ts 文件的所有未覆盖 API 生成。

```
请为指定范围补充 XTS 测试用例。

- d.ts 文件路径：component/text.d.ts
- 接口/方法名：fontFeature
- 子系统：ArkUI开发框架
```

#### 场景 8：包含 UI 类用例（Demo + UiTest）

目标 API 涉及 UI 组件，需要生成 Demo 被测应用和 UiTest 自动化测试。

```
请为指定范围补充 XTS 测试用例。

- d.ts 文件路径：component/list.d.ts
- 子系统：ArkUI开发框架
- 其他要求：包含 UI 类用例，需生成 Demo 和 UiTest
```

#### 场景 9：静态语法项目（ArkTS-Sta）

目标工程使用 ArkTS 静态语法。

```
请为指定范围补充 XTS 测试用例。

- d.ts 文件路径：component/text.d.ts
- 子系统：ArkUI开发框架
- ETS 版本：ets1.2
```

#### 场景 10：多版本同时生成

同时为动态和静态版本生成测试。

```
请为指定范围补充 XTS 测试用例。

- d.ts 文件路径：component/text.d.ts
- 子系统：ArkUI开发框架
- ETS 版本：ets1.1、ets1.2
```

#### 场景 11：指定迭代阶段

第 N 轮补充，已有 iter-1 数据，从 iter-2 开始。

```
请为指定范围补充 XTS 测试用例。

- d.ts 文件路径：component/text.d.ts
- 子系统：ArkUI开发框架
- 其他要求：第 2 轮迭代，基于 iter-1 的 after 数据作为 before 基线
```

#### 场景 12：按子系统全量补充

为整个子系统的未覆盖 API 补充用例。

```
请为指定范围补充 XTS 测试用例。

- 子系统：ArkUI开发框架
```

---

### 编译类场景

#### 场景 13：仅编译验证

测试代码已手动编写或上次生成后修复了编译错误，只需编译。

```
请编译验证以下 XTS 测试套。

- 子系统：ArkUI开发框架
- 测试目录：test/xts/acts/arkui/ace_ets_text/
```

#### 场景 14：SDK 补齐后重新编译

上次编译因 SDK 缺失失败，SDK 已补齐，重新编译。

```
请编译验证以下 XTS 测试套。

- 子系统：ArkUI开发框架
- 测试目录：test/xts/acts/arkui/
- 说明：SDK 已补齐，请重新编译
```

#### 场景 15：编译失败后修复重试

编译失败后修改了代码，重新编译验证。

```
请编译验证以下 XTS 测试套。

- 子系统：ArkUI开发框架
- 测试目录：test/xts/acts/arkui/ace_ets_text/
- 说明：已修复编译错误，请重新编译
```

---

### 扫描类场景

#### 场景 16：仅扫描覆盖率（不生成用例）

只想了解当前覆盖率情况，不生成测试代码。

```
请扫描以下范围的 XTS 覆盖率并生成报告。

- d.ts 文件路径：component/text.d.ts
- 子系统：ArkUI开发框架
```

#### 场景 17：查看覆盖率对比报告

测试用例已生成，想看 before/after 覆盖率变化。

```
请扫描以下范围的 XTS 覆盖率并生成报告。

- Kit 名称：ArkUI
- 子系统：ArkUI开发框架
- 是否生成对比报告：是
- 对比基准文件：.coverage_data/iter-1/coverage_report_before_ets1.1_xxx.json
```

#### 场景 18：扫描指定接口的覆盖率

只看特定接口的覆盖情况。

```
请扫描以下范围的 XTS 覆盖率并生成报告。

- d.ts 文件路径：component/text.d.ts
- 类名：TextAttribute
- 接口/方法名：fontFeature
- 子系统：ArkUI开发框架
```

---

### 验证类场景

#### 场景 19：仅格式验证

代码已生成，只想做格式检查，不编译。

```
请对以下 XTS 测试代码执行格式验证。

- 子系统：ArkUI开发框架
- 测试目录：test/xts/acts/arkui/ace_ets_text/
```

#### 场景 20：仅覆盖率验证（不编译）

跳过编译，直接重新扫描覆盖率生成对比报告。

```
请对以下 XTS 测试代码执行覆盖率验证。

- 子系统：ArkUI开发框架
- 测试目录：test/xts/acts/arkui/ace_ets_text/
```

---

### 恢复类场景

#### 场景 21：从断点继续

上次流程中断，从指定 Phase 继续。

```
请继续执行上次中断的 XTS 测试生成任务。

- 上次中断位置：Phase 5
- 子系统：ArkUI开发框架
- 已有产出：设计文档已有
```

#### 场景 22：设计文档已有，直接生成代码

跳过 Phase 1-4，从设计文档直接生成代码。

```
请继续执行上次中断的 XTS 测试生成任务。

- 上次中断位置：Phase 5
- 子系统：ArkUI开发框架
- 已有产出：Phase 4 设计文档已生成，位于 {设计文档路径}
```

---

## 场景 → Phase 路由速查

| 场景类型 | 执行范围 |
|---------|---------|
| 生成类（默认） | Phase 1 → 10 |
| 生成类 + 新增接口 | Phase 1 → 10（Flow C，跳过 Phase 2 扫描） |
| 编译类 | Phase 8 |
| 扫描类 | Phase 1 → 2 → 停止 |
| 扫描类 + 对比 | Phase 1 → 2 → 9 → 停止 |
| 格式验证 | Phase 7 |
| 覆盖率验证 | Phase 9 |
| 恢复类 | 指定 Phase → 10 |
