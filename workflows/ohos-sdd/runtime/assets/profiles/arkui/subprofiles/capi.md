---
name: capi
applies_to:
  - "**/napi/**"
  - "**/*_napi.cpp"
  - "**/interfaces/kits/**"
  - "**/interfaces/native/**"
  - "**/native_interface_*"
  - "**/arkui_*"
---

# ArkUI C API Sub-profile

适用于 C API / NDK 接口开发。

## Define 追加要求

`proposal.md` 必须确认：

- 是否新增、修改或废弃 C API
- 是否影响 ABI / NDK 兼容性
- API 所属组件或能力域
- 目标调用方：应用、系统应用、框架内部或测试工具
- 是否需要同步 ArkTS SDK API 或运行时实现

## Specify / Design 追加要求

`design.md` 与 `spec.md` 必须对齐：

- API 名称、参数、返回值、错误处理和生命周期
- ABI 兼容性声明和废弃策略
- C API 与 C++ 实现层的映射关系
- modifier / accessor / utility 的分类
- 验证映射：modifier、accessor、utility、SpecTest 或人工验证项
- 每条 C API AC 必须映射到对应 C API unittest；不能只依赖 SDK 编译或组件 unittest
- 若 modifier / accessor 最终影响 UI 布局、绘制、节点属性或交互结果，必须补充 SpecTest case 或写明 N/A 理由
- 若 C API 与 ArkTS SDK API 共同暴露同一能力，必须记录双向一致性：命名、参数语义、默认值、错误处理和验证证据

## Plan / Post-Plan 自闭环

### Unittest 编译

全部 C API 测试：

```bash
./build.sh --product-name rk3568 --build-target //foundation/arkui/ace_engine/test/unittest/capi:capi_unittest
```

具体模块测试（modifiers）：

```bash
./build.sh --product-name rk3568 --ccache --build-target //foundation/arkui/ace_engine/test/unittest/capi/modifiers:capi_all_modifiers_test
```

Linux host (x86) 测试编译：

```bash
./build.sh --product-name rk3568 --build-target //foundation/arkui/ace_engine/test/unittest:linux_unittest_capi
```

### 编译目标推导规则

1. C API 测试集中在 `test/unittest/capi/` 目录下
2. Modifier 测试在 `test/unittest/capi/modifiers/` 目录
3. Accessor 测试在 `test/unittest/capi/accessors/` 目录
4. 读取对应 `BUILD.gn` 中的 `ace_unittest("<target_name>")` 获取编译目标名

### 测试文件约定

- 测试文件位置：`test/unittest/capi/modifiers/` 或 `test/unittest/capi/accessors/`
- 测试文件命名：`<component>_modifier_test.cpp` 或 `<component>_accessor_test.cpp`
- 编译宏：`ARKUI_CAPI_UNITTEST`
- BUILD.gn 中 `module_name = "C-API-Main"`
- 支持 linux host (x86) 测试执行

### UI 可见行为验证

C API modifier / accessor 影响 UI 可见结果时，C API unittest 只验证接口层正确性，还必须补充可见行为验证：

```bash
cd examples/SpecTest
./tools/host_preview/run_feature.sh --case-id <case-id>
./tools/host_preview/run_feature.sh --suite-id <suite-id>
```

完成条件：

1. C API unittest 覆盖参数、返回值、异常/边界和 ABI 兼容风险
2. SpecTest 或替代验证覆盖最终 UI 行为，例如尺寸、位置、绘制属性或节点状态
3. C API 测试报告、SpecTest 报告和 N/A 替代证据写入 Task Card、`evidence/checks/` 或 `review.md`
4. 如果当前 Host Preview 无法直接触达该 C API 能力，必须说明桥接路径缺失，并转入组件 unittest、SDK API 验证或设备矩阵

## 最终交付追加要求

- API 变更必须有兼容性复核结论
- 新增或变更 API 必须确认文档 / 声明 / 测试同步
- 如无法在当前环境执行 host 测试，必须在 `evidence/reviews/` 记录人工验证阻塞项
- UI 可见的 C API 变更必须归档 SpecTest 或替代验证报告；只通过 C API unittest 不满足发布 gate
- ABI / API 兼容性、ArkTS SDK 同步状态和跨平台支持范围必须在 `evidence/reviews/` 闭合
