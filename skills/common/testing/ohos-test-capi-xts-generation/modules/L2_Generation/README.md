# L2_Generation（生成与规范层）

> **层级**: 第 2 层 | **输出**: 测试用例代码（C++ + ETS）、工程配置

本层根据 API 解析结果和覆盖率缺口，生成 N-API 方式的 CAPI 测试用例（C++ NAPI 封装 + ETS 测试调用）及配套工程配置。

---

## 子模块

### generator/（测试生成器）

| 文件 | 说明 |
|------|------|
| `test_generation_c.md` | C++ NAPI 测试用例生成策略 |
| `test_patterns_napi_ets.md` | ETS 测试模式（基础） |
| `test_patterns_napi_ets_advance.md` | ETS 测试模式（回调/异步/句柄类） |
| `napi_api_reference.md` | N-API 函数参考（不常用函数） |
| `project_config_templates.md` | 工程配置模板（新建工程） |
| `verification_common.md` | N-API 三重校验规范 |
| `test_suite_structure_checklist.md` | 测试套结构检查清单 |

---

## 使用方式

### Phase 4: 测试用例生成

```
modules/L2_Generation/generator/test_generation_c.md
modules/L2_Generation/generator/test_patterns_napi_ets.md
modules/L2_Generation/generator/test_patterns_napi_ets_advance.md（回调/异步/句柄类 API）
modules/L2_Generation/generator/project_config_templates.md（新建工程）
modules/L2_Generation/generator/napi_api_reference.md（不常用 napi 函数）
```

### Phase 5: N-API 三重校验

```
modules/L2_Generation/generator/verification_common.md
modules/L2_Generation/generator/test_suite_structure_checklist.md
```

---

## 注意事项

1. 生成方式为 N-API 封装测试（方式2），需同步维护 C++ 和 ETS 两套代码
2. generator 依赖 `modules/conventions/` 中的框架规范
3. 回调/异步/句柄类 API 使用 advance 模式，普通 API 使用基础模式

---

**更新日期**: 2026-04-07
**版本**: 2.0.0
