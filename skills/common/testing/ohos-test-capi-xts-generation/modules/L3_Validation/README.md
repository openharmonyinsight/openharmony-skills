# L3_Validation（验证层）

> **层级**: 第 3 层 | **输出**: 验证结果、编译产物

本层整合格式验证和构建验证功能，验证生成的测试用例是否符合 CAPI XTS 规范并确保编译通过。

---

## 子模块

### builder/（构建验证）

| 文件 | 说明 |
|------|------|
| `build_workflow_c.md` | CAPI 编译工作流 |
| `linux_compile_env_setup_c.md` | Linux 编译环境配置 |
| `linux_compile_workflow_c.md` | Linux 详细编译流程 |
| `quick_reference_extract_suite_name.md` | 提取测试套名称速查 |

---

## 使用方式

### Phase 6: 编译验证

```
modules/L3_Validation/builder/build_workflow_c.md
modules/L3_Validation/builder/linux_compile_env_setup_c.md（环境配置）
modules/L3_Validation/builder/linux_compile_workflow_c.md（Linux 详细流程）
modules/L3_Validation/builder/quick_reference_extract_suite_name.md（提取测试套名称）
```

---

## 注意事项

1. CAPI 编译涉及 NDK/工具链配置，环境要求比 ArkTS 更严格
2. N-API 三重校验（Phase 5）在编译前必须通过
3. Linux 和 Windows 编译流程差异较大，本文档以 Linux 为主
4. 编译需正确配置 OH_ROOT 和 build-profile.json5

---

**更新日期**: 2026-04-07
**版本**: 2.0.0
