# BUILD.gn 配置指南

> **模块信息**
> - 层级：L2_Analysis
> - 优先级：按需加载（配置 BUILD.gn 时加载）
> - 适用范围：Linux 环境下的 XTS 测试工程编译
> - 平台：Linux
> - 依赖：无
> - 相关：`build_workflow_linux.md`（完整的编译工作流）

> **使用说明**
>
> 本指南提供 BUILD.gn 配置的完整说明，包括基本结构、关键配置字段、Stage 模型和 FA 模型配置。
>
> 用户要求配置 BUILD.gn 时，加载此模块。

---

## 一、BUILD.gn 概述

### 1.1 什么是 BUILD.gn

BUILD.gn 文件定义了测试工程的编译配置，包括：
- 测试套名称
- 依赖关系
- 证书配置
- 编译参数

### 1.2 BUILD.gn 位置

```
test/xts/acts/{subsystem}/{test_suite_name}/BUILD.gn
```

示例：
```
test/xts/acts/testfwk/uitest_errorcode/BUILD.gn
```

### 1.3 BUILD.gn 基本格式

```gni
import("//test/xts/tools/build/suite.gni")

# 测试套配置
ohos_js_app_suite("SuiteName") {
  # 配置参数
}
```

---

## 二、基本结构

### 2.1 标准测试工程

最简单的测试工程配置：

```gni
import("//test/xts/tools/build/suite.gni")

# 主测试套
ohos_js_app_suite("ActsUiTest") {
  test_hap = true
  testonly = true
  certificate_profile = "./signature/auto_ohos_default_com.uitest.test.p7b"
  hap_name = "ActsUiTest"
  part_name = "arkxtest"
  subsystem_name = "testfwk"
}
```

### 2.2 带辅助工程的测试工程

UI 测试通常需要辅助工程（Entry）：

```gni
import("//test/xts/tools/build/suite.gni")

# 辅助工程（Scene）
ohos_app_assist_suite("ActsUiTestEntry") {
  testonly = true
  subsystem_name = "testfwk"
  part_name = "arkxtest"
  certificate_profile = "./signature/auto_ohos_default_com.uitest.test.p7b"
  hap_name = "ActsUiTestEntry"
}

# 主测试套
ohos_js_app_suite("ActsUiTest") {
  test_hap = true
  testonly = true
  certificate_profile = "./signature/auto_ohos_default_com.uitest.test.p7b"
  hap_name = "ActsUiTest"
  part_name = "arkxtest"
  subsystem_name = "testfwk"
  deps = [
    ":ActsUiTestEntry",  # 依赖辅助工程
  ]
}
```

---

## 三、关键配置字段

### 3.1 常用字段说明

| 字段 | 说明 | 示例 | 必需 |
|------|------|------|------|
| `test_hap` | 是否为测试 HAP | `true` | ✅ |
| `hap_name` | HAP 包名称 | `"ActsUiTest"` | ✅ |
| `part_name` | 部件名称 | `"arkxtest"` | ✅ |
| `subsystem_name` | 子系统名称 | `"testfwk"` | ✅ |
| `deps` | 依赖项 | `[":ActsUiTestEntry"]` | ❌ |
| `certificate_profile` | 证书配置 | `"./signature/*.p7b"` | ✅ |
| `testonly` | 是否仅用于测试 | `true` | ✅ |

### 3.2 字段详解

#### test_hap

标识这是一个测试 HAP 包：

```gni
ohos_js_app_suite("ActsUiTest") {
  test_hap = true  # 必须设置为 true
  ...
}
```

#### hap_name

HAP 包的名称，也是编译目标名称：

```gni
ohos_js_app_suite("ActsUiTest") {
  hap_name = "ActsUiTest"  # 与第一个参数一致
  ...
}
```

**编译命令使用**：
```bash
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsUiTest
```

#### part_name

部件名称，标识所属部件：

```gni
part_name = "arkxtest"  # arkxtest部件
```

常用部件名称：
- `arkxtest` - arkxtest部件
- `window_test` - 窗口测试
- `ui_test` - UI 测试

#### subsystem_name

子系统名称，标识所属子系统：

```gni
subsystem_name = "testfwk"  # 测试框架子系统
```

常用子系统名称：
- `testfwk` - 测试框架
- `window` - 窗口管理
- `arkui` - ArkUI 框架

#### deps

依赖项列表，用于指定依赖的其他模块：

```gni
deps = [
  ":ActsUiTestEntry",  # 依赖辅助工程
  ":OtherModule",      # 依赖其他模块
]
```

#### certificate_profile

证书配置文件路径：

```gni
certificate_profile = "./signature/auto_ohos_default_com.uitest.test.p7b"
```

证书文件通常位于 `./signature/` 目录。

---

## 四、Stage 模型配置

### 4.1 Stage 模型概述

Stage 模型是 OpenHarmony 推荐的应用模型，需要额外配置 `ohos_app_scope`。

### 4.2 完整配置示例

```gni
import("//test/xts/tools/build/suite.gni")

# AppScope 配置
ohos_app_scope("actmoduletest_app_profile") {
  app_profile = "AppScope/app.json"
  sources = [ "AppScope/resources" ]
}

# 资源配置
ohos_resources("test_resources") {
  sources = [ "./src/main/resources" ]
  deps = [
    ":actmoduletest_app_profile",
  ]
  hap_profile = "./src/main/module.json"
}

# 主测试套
ohos_js_hap_suite("ActsStageTest") {
  ets2abc = true
  hap_profile = "entry/src/main/module.json"
  deps = [
    ":test_js_assets",
    ":test_resources",
  ]
  certificate_profile = "./signature/auto_ohos_default_com.example.test.p7b"
  hap_name = "ActsStageTest"
}
```

### 4.3 Stage 模型目录结构

```
ActsStageTest/
├── AppScope/
│   ├── app.json
│   └── resources/
├── entry/
│   └── src/
│       └── main/
│           ├── module.json
│           ├── resources/
│           └── ets/
├── BUILD.gn
└── signature/
    └── *.p7b
```

### 4.4 Stage 模型关键点

1. **AppScope 配置**：应用级配置文件
2. **module.json**：模块配置文件（替代 config.json）
3. **ohos_js_hap_suite**：使用 `ohos_js_hap_suite` 而非 `ohos_js_app_suite`
4. **ets2abc**：启用 ArkTS 编译

---

## 五、FA 模型配置

### 5.1 FA 模型概述

FA 模型是 OpenHarmony 早期的应用模型，使用 `config.json` 配置。

### 5.2 完整配置示例

```gni
import("//test/xts/tools/build/suite.gni")

ohos_js_hap_suite("ActsFaTest") {
  hap_profile = "./src/main/config.json"
  deps = [
    ":test_js_assets",
    ":test_resources",
  ]
  certificate_profile = "./signature/openharmony_sx.p7b"
  hap_name = "ActsFaTest"
}
```

### 5.3 FA 模型目录结构

```
ActsFaTest/
├── src/
│   └── main/
│       ├── config.json
│       ├── resources/
│       └── ets/
├── BUILD.gn
└── signature/
    └── *.p7b
```

### 5.4 FA 模型关键点

1. **config.json**：模块配置文件
2. **ohos_js_hap_suite**：使用 `ohos_js_hap_suite`
3. **hap_profile**：指向 config.json 文件

---

## 六、辅助工程配置

### 6.1 什么是辅助工程

辅助工程（Assist Suite）用于 UI 测试，提供测试场景和界面。

### 6.2 辅助工程配置

```gni
# 辅助工程
ohos_app_assist_suite("ActsUiTestEntry") {
  testonly = true
  subsystem_name = "testfwk"
  part_name = "arkxtest"
  certificate_profile = "./signature/auto_ohos_default_com.uitest.test.p7b"
  hap_name = "ActsUiTestEntry"
}
```

### 6.3 主测试套依赖辅助工程

```gni
# 主测试套
ohos_js_app_suite("ActsUiTest") {
  test_hap = true
  testonly = true
  certificate_profile = "./signature/auto_ohos_default_com.uitest.test.p7b"
  hap_name = "ActsUiTest"
  part_name = "arkxtest"
  subsystem_name = "testfwk"
  deps = [
    ":ActsUiTestEntry",  # 依赖辅助工程
  ]
}
```

### 6.4 辅助工程目录结构

```
ActsUiTest/
├── entry/              # 辅助工程（Entry）
│   └── src/
│       └── main/
│           ├── ets/
│           ├── resources/
│           └── module.json5
├── ActsUiTestEntry/    # 测试代码
│   └── src/
│       └── main/
│           └── ets/
├── BUILD.gn
└── signature/
    └── *.p7b
```

---

## 七、编译目标名称

### 7.1 编译目标名称规则

编译目标名称由 `BUILD.gn` 中 `ohos_js_app_suite()` 的第一个参数决定：

```gni
# BUILD.gn
ohos_js_app_suite("ActsUiTestErrorCodeTest") {  # ← 编译目标名称
  ...
}
```

### 7.2 编译命令使用

```bash
# 编译命令中的 suite 参数必须与 BUILD.gn 中的名称一致
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsUiTestErrorCodeTest
```

### 7.3 常见错误

❌ **错误**：名称不匹配
```bash
# BUILD.gn 中为 "ActsUiTestErrorCodeTest"
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsUiTest
# ❌ 错误：找不到测试套
```

✅ **正确**：名称一致
```bash
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=ActsUiTestErrorCodeTest
# ✅ 正确
```

---

## 八、配置示例

### 8.1 基础测试工程

```gni
import("//test/xts/tools/build/suite.gni")

ohos_js_app_suite("ActsSampleTest") {
  test_hap = true
  testonly = true
  certificate_profile = "./signature/auto_ohos_default_com.sample.test.p7b"
  hap_name = "ActsSampleTest"
  part_name = "sample_test"
  subsystem_name = "sample"
}
```

### 8.2 带 Entry 的 UI 测试

```gni
import("//test/xts/tools/build/suite.gni")

# 辅助工程
ohos_app_assist_suite("ActsSampleTestEntry") {
  testonly = true
  subsystem_name = "sample"
  part_name = "sample_test"
  certificate_profile = "./signature/auto_ohos_default_com.sample.test.p7b"
  hap_name = "ActsSampleTestEntry"
}

# 主测试套
ohos_js_app_suite("ActsSampleTest") {
  test_hap = true
  testonly = true
  certificate_profile = "./signature/auto_ohos_default_com.sample.test.p7b"
  hap_name = "ActsSampleTest"
  part_name = "sample_test"
  subsystem_name = "sample"
  deps = [
    ":ActsSampleTestEntry",
  ]
}
```

### 8.3 Stage 模型测试

```gni
import("//test/xts/tools/build/suite.gni")

ohos_app_scope("actmoduletest_app_profile") {
  app_profile = "AppScope/app.json"
  sources = [ "AppScope/resources" ]
}

ohos_resources("test_resources") {
  sources = [ "./src/main/resources" ]
  deps = [
    ":actmoduletest_app_profile",
  ]
  hap_profile = "./src/main/module.json"
}

ohos_js_hap_suite("ActsStageTest") {
  ets2abc = true
  hap_profile = "entry/src/main/module.json"
  deps = [
    ":test_js_assets",
    ":test_resources",
  ]
  certificate_profile = "./signature/auto_ohos_default_com.example.test.p7b"
  hap_name = "ActsStageTest"
}
```

---

## 九、配置检查清单

创建或修改 BUILD.gn 时，确保完成以下检查：

- [ ] 已导入 `//test/xts/tools/build/suite.gni`
- [ ] 编译目标名称与 `hap_name` 一致
- [ ] `test_hap` 设置为 `true`
- [ ] `testonly` 设置为 `true`
- [ ] `part_name` 和 `subsystem_name` 正确
- [ ] `certificate_profile` 路径正确
- [ ] 辅助工程（如果有）配置正确
- [ ] 依赖项（`deps`）配置正确

---

## 十、参考资源

### 10.1 相关文档

- [Linux 编译工作流](./build_workflow_linux.md)
- [编译问题排查](./linux_compile_troubleshooting.md)

### 10.2 参考路径

| 类型 | 路径 |
|------|------|
| 模板文件 | `./test/xts/tools/build/suite.gni` |
| 测试框架 | `./test/xts/acts/` |

### 10.3 常用命令

```bash
# 验证 BUILD.gn 语法
python3 test/xts/tools/build/check_gn.py path/to/BUILD.gn

# 查找测试套
find test/xts/acts -name "BUILD.gn" -type f
```

---

## 十一、版本历史

- **v1.0.0** (2026-02-06): 从 `build_workflow_linux.md` 中抽取 BUILD.gn 配置相关内容，创建独立模块
