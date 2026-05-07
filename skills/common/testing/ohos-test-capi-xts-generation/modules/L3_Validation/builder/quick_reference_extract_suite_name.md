# BUILD.gn 测试套名称提取快速参考

> **模块信息**
> - 用途：快速从 BUILD.gn 中提取测试套名称
> - 适用场景：Linux 环境下编译测试套时获取正确的 suite 参数值
> - 相关文档：[build_workflow_c.md](./build_workflow_c.md)

---

## 一、快速提取命令

### 方法1：使用 awk（推荐）

```bash
awk -F'"' '/ohos_(js_app_suite|native_test_suite)\(/ {print $2; exit}' {测试套目录}/BUILD.gn
```

**示例**：
```bash
TEST_SUITE_DIR="{OH_ROOT}/test/xts/acts/bundlemanager/bundle_standard/bundlemanager/actsbmsgetabilityresourcendkenterprisetest"

awk -F'"' '/ohos_(js_app_suite|native_test_suite)\(/ {print $2; exit}' \
  "$TEST_SUITE_DIR/BUILD.gn"

# 输出：ActsBmsGetAbilityResourceNdkEnterpriseTest
```

### 方法2：使用 grep 和 sed

```bash
grep -E "ohos_(js_app_suite|native_test_suite)\(" {测试套目录}/BUILD.gn | \
  sed -n 's/.*("\([^"]*\)").*/\1/p' | head -1
```

**示例**：
```bash
grep -E "ohos_(js_app_suite|native_test_suite)\(" \
  {OH_ROOT}/test/xts/acts/bundlemanager/bundle_standard/bundlemanager/actsbmsgetabilityresourcendkenterprisetest/BUILD.gn | \
  sed -n 's/.*("\([^"]*\)").*/\1/p' | head -1

# 输出：ActsBmsGetAbilityResourceNdkEnterpriseTest
```

---

## 二、手动提取步骤

### 步骤1：打开 BUILD.gn 文件

```bash
# 使用 cat 查看文件内容
cat {测试套目录}/BUILD.gn

# 或使用编辑器打开
vi {测试套目录}/BUILD.gn
```

### 步骤2：查找测试套定义

BUILD.gn 中包含以下几种测试套类型：

| 类型 | BUILD.gn 模式 | 示例 |
|------|--------------|------|
| **静态 JS 测试套** | `ohos_js_app_static_suite("TestSuiteName")` | `ohos_js_app_static_suite("ActsUiStaticTest")` |
| **动态 JS 测试套** | `ohos_js_app_suite("TestSuiteName")` | `ohos_js_app_suite("ActsBmsGetAbilityResourceNdkEnterpriseTest")` |
| **App Assist 测试套** | `ohos_app_assist_suite("TestSuiteName")` | `ohos_app_assist_suite("ActsBmsGetAbilityResourceTwoNdkEnterpriseTest")` |

### 步骤3：提取测试套名称

**规则**：提取引号内的名称（不包括引号）

**示例**：
```gni
# BUILD.gn 内容
ohos_js_app_suite("ActsBmsGetAbilityResourceNdkEnterpriseTest") {
  test_hap = true
  testonly = true
  ...
}
```

**提取结果**：`ActsBmsGetAbilityResourceNdkEnterpriseTest`

### 步骤4：验证提取结果

```bash
# 验证 BUILD.gn 中是否存在该目标
grep -q "ohos_js_app_suite(\"ActsBmsGetAbilityResourceNdkEnterpriseTest\")" \
  "$TEST_SUITE_DIR/BUILD.gn" && echo "✅ 验证通过" || echo "❌ 验证失败"
```

---

## 三、完整编译流程示例

```bash
#!/bin/bash

# 配置测试套路径
TEST_SUITE_DIR="{OH_ROOT}/test/xts/acts/bundlemanager/bundle_standard/bundlemanager/actsbmsgetabilityresourcendkenterprisetest"

# 步骤1：提取测试套名称
SUITE_NAME=$(awk -F'"' '/ohos_(js_app_suite|native_test_suite)\(/ {print $2; exit}' \
  "$TEST_SUITE_DIR/BUILD.gn")

echo "提取的测试套名称: $SUITE_NAME"

# 步骤2：验证提取结果
if [ -z "$SUITE_NAME" ]; then
  echo "❌ 错误：无法从 BUILD.gn 中提取测试套名称"
  exit 1
fi

# 步骤3：执行编译
cd {OH_ROOT}
echo "开始编译测试套: $SUITE_NAME"
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite="$SUITE_NAME"

# 步骤4：检查编译结果
if [ $? -eq 0 ]; then
  echo "✅ 编译成功"
else
  echo "❌ 编译失败"
  exit 1
fi
```

---

## 四、常见错误示例

### 错误1：使用目录名作为 suite 参数

```bash
# ❌ 错误
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=actsbmsgetabilityresourcendkenterprisetest

# 错误原因：
# - 目录名：actsbmsgetabilityresourcendkenterprisetest（小写开头）
# - BUILD.gn 名称：ActsBmsGetAbilityResourceNdkEnterpriseTest（大写开头）
# - 名称不匹配导致编译失败
```

**正确做法**：
```bash
# ✅ 正确
SUITE_NAME=$(awk -F'"' '/ohos_(js_app_suite|native_test_suite)\(/ {print $2; exit}' \
  "$TEST_SUITE_DIR/BUILD.gn")
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite="$SUITE_NAME"
```

### 错误2：使用 target_subsystem 参数

```bash
# ❌ 错误
./test/xts/acts/build.sh target_subsystem=bundlemanager

# 错误原因：
# - target_subsystem 会编译整个子系统的所有测试套
# - 不是编译单个测试套的正确方式
# - 可能导致编译时间过长或资源浪费
```

**正确做法**：
```bash
# ✅ 正确：使用 suite 参数指定具体的测试套名称
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsBmsGetAbilityResourceNdkEnterpriseTest
```

### 错误3：从错误的 BUILD.gn 提取

```bash
# ❌ 错误：从子系统 BUILD.gn 提取
grep "ohos_js_app_suite" /test/xts/acts/bundlemanager/BUILD.gn

# 正确做法：
# ✅ 应该从测试套目录下的 BUILD.gn 提取
grep "ohos_js_app_suite" {测试套目录}/BUILD.gn
```

---

## 五、BUILD.gn 目标类型说明

### 5.1 ohos_js_app_suite

**用途**：JS 或 N-API 封装测试套

**示例**：
```gni
ohos_js_app_suite("ActsBmsGetAbilityResourceNdkEnterpriseTest") {
  test_hap = true
  testonly = true
  certificate_profile = "./signature/openharmony.p7b"
  hap_name = "ActsBmsGetAbilityResourceNdkEnterpriseTest"
  part_name = "bundle_framework"
  subsystem_name = "bundlemanager"
}
```

**特点**：
- 生成 HAP 包
- 支持 ETS/ArkTS 测试代码
- 可以包含 N-API 封装的 C/C++ 代码

### 5.2 ohos_js_app_static_suite

**用途**：静态 JS 测试套（包含 N-API 封装的 C/C++ 代码）

**示例**：
```gni
ohos_js_app_static_suite("ActsUiStaticTest") {
  testonly = true
  certificate_profile = "./signature/openharmony_sx.p7b"
  hap_name = "ActsUiStaticTest"
  part_name = "arkxtest"
  subsystem_name = "testfwk"
  external_deps = [
    "hilog:libhilog",
    "ui_component:libui_component",
  ]
}
```

**特点**：
- 生成原生测试可执行文件
- 使用 gtest/HWTEST_F 测试框架
- 直接测试 C/C++ 函数

### 5.3 ohos_app_assist_suite

**用途**：辅助测试套（通常被其他测试套依赖）

**示例**：
```gni
ohos_app_assist_suite("ActsBmsGetAbilityResourceTwoNdkEnterpriseTest") {
  testonly = true
  certificate_profile = "./signature/openharmony.p7b"
  hap_name = "ActsBmsGetAbilityResourceTwoNdkEnterpriseTest"
  part_name = "bundle_framework"
  subsystem_name = "bundlemanager"
}
```

**特点**：
- 生成辅助 HAP 包
- 通常被主测试套通过 deps 依赖
- 不直接作为 suite 参数使用

---

## 六、验证清单

在执行编译前，请检查以下项目：

- [ ] 已从 BUILD.gn 中提取测试套名称
- [ ] 验证 BUILD.gn 中确实存在该测试套定义
- [ ] 确认测试套名称格式正确（通常以 Acts 开头，Test 结尾）
- [ ] 确认编译命令参数正确（product_name=rk3568 system_size=standard）
- [ ] 确认在 OH_ROOT 目录下执行编译命令

---

## 七、版本信息

- **版本**: 1.0.0
- **创建日期**: 2026-03-09
- **兼容性**: OpenHarmony API 10+，XACTS 测试框架
- **基于**: OH_CAPI_XTS_GENERATOR v1.0.0
