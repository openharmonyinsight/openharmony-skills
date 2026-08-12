## Phase 6: N-API Triple Verification

---

### 📚 参考文档（按需查阅）

| 文件 | 内容 | 何时查阅 |
|------|------|---------|
| `modules/L2_Generation/generator/verification_common.md` | N-API 三重校验规则、校验清单、自动修复流程、工程结构校验 | 校验细节不明确时参考 |

---

### ⚙️ 按需加载

| 任务 | 加载文件 | 说明 |
|------|---------|------|
| 编译/运行错误排查 | `references/error_handling.md` | 错误分级、重试策略 |

---

### 🚫 Do NOT Load

```
所有 modules/L1_Analysis 模块
modules/L2_Generation/generator/test_generation_c.md（已在 Phase 5 使用）
modules/L2_Generation/generator/test_patterns_napi_ets*.md（已在 Phase 5 使用）
所有 modules/L3_Validation 模块
```

---

**MANDATORY — NEVER SKIP**: 此阶段是核心质量门控。跳过将导致运行时 crash、函数未注册、类型不匹配。

### 三重校验定义

N-API 三重校验验证 C++ / TypeScript / ETS 三层之间的一致性：

| 校验层 | 文件 | 校验内容 |
|--------|------|---------|
| C++ 层 | `entry/src/main/cpp/NapiTest.cpp` | 函数实现、`napi_property_descriptor` 注册 |
| TypeScript 层 | `entry/src/main/cpp/types/libentry/index.d.ts` | 函数声明、参数类型、返回类型 |
| ETS 层 | `entry/src/ohosTest/ets/test/*.test.ets` | 函数调用、参数传递、断言 |

### 校验步骤

#### 步骤 A：自动化脚本校验

```bash
# 三重一致性校验
bash {skill_root}/scripts/verify_napi_triple.sh ${TARGET_PATH}

# 工程结构校验
bash {skill_root}/scripts/check_test_suite_structure.sh ${TARGET_PATH}
```

#### 步骤 B：自动修复（校验失败时）

```bash
bash {skill_root}/scripts/auto_fix_napi_triple.sh ${TARGET_PATH}
```

自动修复后，**必须重新运行校验脚本**确认修复结果。

#### 步骤 C：人工检查项

自动脚本无法覆盖的检查项：

| 检查项 | 检查方式 | 常见问题 |
|--------|---------|---------|
| N-API 参数转换正确性 | 对照 .h 签名检查 `napi_get_value_*` 调用 | int 参数用了 `napi_get_value_string_utf8` |
| 返回值转换正确性 | 检查 `napi_create_*` 调用与 C 返回值类型匹配 | 指针返回值未用 `napi_wrap` |
| null 参数处理 | 检查 nullable 参数是否有 `napi_null` 分支 | 传 null 时 crash |
| 内存释放 | 检查 `napi_finalize` 回调是否注册 | 内存泄漏 |

### 校验结果判定

| 结果 | 操作 |
|------|------|
| 全部通过 | Phase 6 完成，进入 Phase 7 |
| 自动修复后通过 | Phase 6 完成，记录修复内容 |
| 手动修复后通过 | Phase 6 完成，记录修复内容 |
| 无法修复 | 回退到 Phase 5 重新生成对应代码 |
