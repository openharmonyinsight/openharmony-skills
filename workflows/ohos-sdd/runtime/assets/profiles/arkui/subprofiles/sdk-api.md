---
name: sdk-api
applies_to:
  - "**/interfaces/inner_api/**"
  - "**/@systemapi/**"
  - "**/*.d.ets"
  - "**/interface/sdk-js/**"
---

# ArkUI SDK API Sub-profile

适用于 ArkTS SDK API 开发（.d.ets 声明文件、Modifier 定义等）。

## Define 追加要求

`proposal.md` 必须确认：

- API 面向开发者的使用场景
- 是否新增、修改或废弃 Public/System API
- API 版本、兼容性和迁移策略
- 是否需要同步运行时实现、C API、文档或示例
- 是否涉及权限、安全、隐私或跨设备行为

## Specify / Design 追加要求

`design.md` 与 `spec.md` 必须对齐：

- API 名称、签名、参数类型、默认值、异常或错误语义
- API 兼容性、废弃标注和替代方案
- SDK 声明文件与运行时实现文件的映射
- Modifier 链式调用、属性覆盖和状态更新语义
- 验证映射：SDK 编译、运行时组件 unittest、SpecTest 或人工验证项
- 每条 API AC 必须映射到 SDK 编译、运行时实现测试、真实 ArkTS 工程验证或 SpecTest；不能只记录声明文件修改
- 若 API / Modifier / 属性影响布局、绘制、节点属性或交互结果，必须映射到 SpecTest case；不适用时写明 N/A 理由和替代验证
- 若 API 同步影响 C API、组件实现或文档示例，`execution-plan.md` 必须拆分对应 Task，并在 `manifest.subprofiles` 中记录命中的子 profile

## Plan / Post-Plan 自闭环

SDK API 变更不一定通过传统 unittest 验证，默认使用 SDK 编译确认接口定义正确。

### SDK 编译验证

```bash
./build.sh --product-name ohos-sdk --build-target ace_engine
```

### API 定义文件位置

- 组件声明：`interface/sdk-js/api/@ohos.arkui.<Component>.static.d.ets`（OpenHarmony 根目录下）
- Modifier 定义：`interface/sdk-js/api/arkui/<Component>Modifier.static.d.ets`（OpenHarmony 根目录下）

### 自闭环替代检查

1. API 定义文件编写完成（.d.ets）
2. SDK 编译验证通过
3. API 签名与 `design.md` / `spec.md` 一致
4. 若涉及运行时实现变更，对应组件 unittest 也需通过

### SpecTest Host Preview

API 或 Modifier 最终影响可观测 UI 行为时，必须补充真实 ArkTS 页面验证。优先使用 SpecTest：

```bash
cd examples/SpecTest
./tools/host_preview/run_feature.sh --case-id <case-id>
./tools/host_preview/run_feature.sh --suite-id <suite-id>
```

完成条件：

1. 用例页面使用公开 ArkTS API / Modifier 触发行为，不直接依赖内部 C++ 接口
2. `expected/expected.json` 断言 API 影响后的节点尺寸、位置、属性或状态
3. affected case / suite 执行结果 `failed_cases=0`
4. 报告路径写入 Task Card、`evidence/checks/` 或 `review.md`

## 最终交付追加要求

- 新增 API 必须确认声明文件、运行时实现、测试和文档同步
- 废弃 API 必须添加 `@deprecated` 标注和替代方案说明
- SDK 编译无法执行时，必须在 `evidence/reviews/` 记录人工验证阻塞项
- 涉及 UI 行为的 API 变更必须归档 SpecTest、真实 ArkTS 工程验证或明确的 N/A 替代证据
- 跨平台或多设备行为差异必须在发布 gate 中记录支持范围、差异原因和补验结论
