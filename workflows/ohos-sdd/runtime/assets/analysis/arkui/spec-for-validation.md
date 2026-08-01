# ArkUI Spec for Validation Playbook

## 定位

Spec for Validation 是 `spec.md`、`design.md` Approved 后由开发者显式触发的 ArkUI 旁路。输出 `spec-for-validation.md`，作为测试人员开展测试设计的输入；具体用例、环境和执行结果不写回该文件。

## 输出格式与保真规则

- 公共层保留 `templates/spec-for-validation.md` 作为默认格式；ArkUI 因 2D、NFR、2C 需要不同的细项表格，通过 Profile `template_override` 使用 `profiles/arkui/templates/spec-for-validation.md`。产物必须自包含，测试人员无需打开其他文档即可开展测试设计。
- 每个 `US-*` 必须完整保留标题、角色（作为）、目标（我想要/我希望）、价值（以便/以免）和该 US 下全部 AC，不得概括、合并或缩写。
- `规则定义` 同时兼容统一规则表和存量 Spec 的业务规则、功能规则、异常/豁免规则、恢复契约；只投影对外触发条件、预期行为、边界和恢复结果。
- API 只保留系统/开放调用方可见的签名、参数、返回值、错误语义和兼容迁移，不保留源码基线、内部类关系或调用链。
- 第五章 2D 按十二个能力维度分别提供专用字段；第六章非功能性需求按性能、功耗、稳定性与可靠性、安全隐私合规、DFX 分别展开；第七章 2C 按静态 UI、动态 UI、交互/焦点、用户数据分别展开，不得退化为统一七列表。
- 非功能性需求只保留对外指标和用户可观察要求，不复制 SpecTest、UT、构建命令、报告路径或开发证据列。
- `GENERATED:EXTERNAL-SPEC` 和 `GENERATED:DESIGN-CONSTRAINTS` 只能由 CLI 刷新。Agent 只编辑 `TEST-ANALYSIS`，不得为了删除内部信息而重写、摘要或压缩来源投影。

## Design 输入约束

需要补充测试可观察性时，在 `design.md` 增加以下条件区段：

```markdown
## 测试输入约束

| AC | 可观察表面 | 测试侧验证方式 | 环境/设备限制 | 不可自动化项 |
|---|---|---|---|---|
| AC-x.x | [返回值/UI/Inspector/日志/指标] | [设备测试/XTS/兼容性测试/人工交互/截图对比] | [限制] | [无/原因] |
```

本区段只描述测试人员可执行的验证契约，不得写源码文件、内部类/函数、调用链、BUILD.gn target、内部算法或开发侧自验证方式。

## 回流规则

| 测试输入分析发现 | 回流交付件 |
|---|---|
| 对外行为、边界或兼容性缺失 | `spec.md` |
| 缺少可观察能力或验证入口 | `design.md`，必要时回修 Spec 可测试性 NFR |
| 2C/2D 适用范围改变需求范围 | `proposal.md` / `spec.md` |
| NFR 细项缺少可量化指标或触发条件 | `spec.md`；缺少可观察入口时同时回修 `design.md` |
| 仅测试数据、环境或用例拆分问题 | `test-spec.md` 或测试用例系统 |

任一上游文件变更后，旧 `spec-for-validation.md` 的来源 hash 失效，必须执行 `ohos-sdd spec-for-validation refresh`。
