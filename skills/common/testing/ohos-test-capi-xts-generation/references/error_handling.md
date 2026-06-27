# 错误分类与处理指南

> ohos-test-capi-xts-generation 生成过程中的错误分类、处理和重试策略

## 1. 错误分类

### Level 1：自动修复（无需用户干预）

| 错误类型 | 触发场景 | 处理策略 |
|----------|----------|----------|
| C++ 语法错误 | NAPI 封装代码语法违规 | 根据编译错误信息自动修复 |
| ETS 调用语法错误 | testNapi.xxx 调用方式错误 | 按 N-API 封装规范自动修正 |
| napi_property_descriptor 缺失 | 三重校验发现未注册函数 | 自动补充注册 |
| index.d.ts 声明缺失 | 三重校验发现声明不匹配 | 自动补充 export const 声明 |
| 命名不规范 | camelCase 违规 | 自动转换为 camelCase |
| 断言方法错误 | 使用了 assertNotX | 替换为正确的断言方法 |

### Level 2：重试修复（自动重试后可能需用户确认）

| 错误类型 | 触发场景 | 处理策略 |
|----------|----------|----------|
| 编译链接错误 | build.sh 编译失败 | 自动修复，最多重试 3 次 |
| .h 头文件解析失败 | 宏定义或条件编译复杂 | 降级为逐函数解析 |
| 头文件过大 | 读取超时 | 分块读取（200 行/块） |
| NAPI 函数签名不匹配 | C++ 与 .d.ts 类型不一致 | 对照头文件自动修正 |

### Level 3：需用户确认

| 错误类型 | 触发场景 | 处理策略 |
|----------|----------|----------|
| 编译配置错误 | BUILD.gn 配置问题 | 展示错误信息，等待用户确认 |
| 子系统配置冲突 | 配置规则矛盾 | 展示矛盾内容，等待用户裁定 |
| NAPI 封装歧义 | .h 与 .d.ts 类型不一致 | 展示证据和选项，等待用户选择 |
| 覆盖率报告格式异常 | 无法解析报告 | 请求用户提供正确格式的报告 |

### Level 4：任务终止

| 错误类型 | 触发场景 | 处理策略 |
|----------|----------|----------|
| OH_ROOT 不存在 | 路径配置错误 | 终止，提示修正配置 |
| .h 头文件不存在 | API 声明文件缺失 | 终止，提示检查路径 |
| 无任何测试代码 | 完全无法参考 | 继续但标注"无测试参考" |

## 2. 编译错误重试策略

### 语法错误（自动修复）

```
编译失败 → 提取错误信息 → 判断错误类型
  ├─ C++ 语法错误 → 修正语法 → 重新编译
  ├─ NAPI 注册错误 → 补充 napi_property_descriptor → 重新编译
  ├─ 链接错误 → 检查依赖配置 → 重新编译
  └─ 其他语法错误 → 展示错误 → 尝试修复 → 重新编译

最多重试 3 次。3 次后仍失败 → 提交给用户确认。
```

### 配置错误（需用户确认）

```
编译失败 → 提取错误信息 → 判断为配置错误
  → 展示完整错误信息
  → 列出可能的解决方案
  → 等待用户确认
```

## 3. 三重校验错误处理

Phase 5 三重校验发现问题时：

| 检查项 | 失败处理 |
|--------|----------|
| C++ 函数未注册 | 自动补充 napi_property_descriptor 后重新检查 |
| .d.ts 声明缺失 | 自动补充 export const 声明后重新检查 |
| ETS 调用不匹配 | 对照 .d.ts 修正调用方式后重新检查 |
| 参数类型不一致 | 对照 C++ 实现修正类型声明后重新检查 |

所有自动修复完成后，如果仍有未通过的检查项，提交给用户确认。

## 4. Common Failure Patterns

### 编译失败：OH_xxx 函数未定义
- **症状**：`undefined reference to 'OH_Camera_Start'`（链接阶段报错，不是编译阶段）
- **根因**：.h 头文件中该函数被 `#ifdef OHOS_ENABLE_*` 包裹，目标编译配置未启用该 feature
- **排查**：在 .h 中搜索目标函数，检查其上方是否有条件编译宏；如果有，确认目标设备的 feature 配置是否启用
- **修复**：在 N-API 封装中加 `#ifdef` 守卫，或跳过该函数

### 运行时崩溃：所有 N-API 函数都是 undefined
- **症状**：`TypeError: testNapi.xxx is not a function`（不是某个函数，而是**所有**函数都报错）
- **根因**：`napi_module` 的 `nm_modname` 字段不是 `"entry"`，或 ETS 侧 `import testNapi from 'libentry.so'` 中 so 名与模块名不匹配
- **排查**：检查 NapiTest.cpp 中 `napi_module` 的 `.nm_modname` → 检查 `oh-package.json5` 的 `name` 字段 → 检查 ETS import 路径，三者必须一致
- **修复**：统一使用 `nm_modname = "entry"`，ETS 侧 `import testNapi from 'libentry.so'`

### 编译失败：测试套名称不匹配
- **症状**：`build.sh` 执行成功但 `out/` 目录下无 HAP 产物
- **根因**：传入的 `suite` 参数与 BUILD.gn 中 `ohos_js_app_suite("Name")` 的 Name 不一致
- **排查**：读取测试套目录下的 BUILD.gn，用 `grep -E 'ohos_js_app_suite\(' BUILD.gn | sed -n 's/.*("\([^"]*\)").*/\1/p'` 提取正确名称
- **修复**：用提取的名称重新执行编译命令
- **注意**：名称区分大小写，且可能与目录名不同

### 运行时崩溃：三层名称不一致
- **症状**：单个函数 `TypeError: testNapi.someFunc is not a function`（其他函数正常）
- **根因**：NapiTest.cpp 中 `DECLARE_NAPI_FUNCTION("someFunc", ...)` 的第一个字符串参数 ↔ index.d.ts 中 `export const someFunc: ...` ↔ .test.ets 中 `testNapi.someFunc(...)` 三者名称不完全一致（大小写差异、拼写错误、命名风格混用）
- **排查**：运行 `bash scripts/verify_napi_triple.sh ${TARGET_PATH}`，脚本会列出定义/注册/声明/调用四层的不一致
- **修复**：以 index.d.ts 的声明名为准，修改 NapiTest.cpp 中的字符串参数和 .test.ets 中的调用名

### 编译通过但行为异常：字符串参数截断
- **症状**：编译通过，但某些测试运行时 C API 返回意外结果（如 HiLog 输出乱码、文件路径无效）
- **根因**：N-API 封装中 `napi_get_value_string_utf8(env, args[0], buffer, bufferSize, &len)` 的 `bufferSize` 设置过小（如 64），字符串被截断但函数不报错（返回 `napi_ok`）
- **排查**：检查 NapiTest.cpp 中所有字符串提取的 buffer 大小，对比 .h 中文档声明的最大长度
- **修复**：使用 256 或更大的缓冲区，或先用 `napi_get_value_string_utf8` 传入 `nullptr` 获取所需长度再动态分配

### 覆盖率扫描：API 调用计数为 0
- **症状**：APICoverageDetector 扫描报告显示测试文件存在但目标 API 调用计数为 0
- **根因**：N-API 封装中调用的 C 函数名与 .h 中声明的函数名不完全匹配（大小写差异、拼写错误、或调用了内部实现而非公开 API）
- **排查**：对比 NapiTest.cpp 中的函数调用名与 .h 中的声明，逐字符比对
- **修复**：确保 N-API 封装中调用的函数名与 .h 头文件中的公开 API 声明完全一致
