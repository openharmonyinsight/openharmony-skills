# R014: 测试HAP命名规范修复指南

## 一、概述

本文档提供R014规则（测试HAP命名不规范）的详细修复指南

## 二、命名规范

### 2.1 命名要求

**hap包命名采用大驼峰方式**

| 模板类型 | 命名规范 | 正确示例 |
|---------|---------|---------|
| `ohos_js_app_suite` | 以`Acts`开头（A大写），以`Test`结尾（T大写） | `ActsAbilityTest` |
| `ohos_js_app_static_suite` | 以`Acts`开头（A大写），以`StaticTest`结尾（S、T大写） | `ActsAbilityStaticTest` |
| `ohos_moduletest_suite` | 以`Acts`开头（A大写），以`Test`结尾（T大写） | `ActsModuleTest` |

### 2.2 修复规则

| 错误类型 | 修复方法 | 示例 |
|---------|---------|------|
| 不以`Acts`开头 | 在名称前添加`Acts`前缀 | `MyTest` → `ActsMyTest` |
| `ohos_js_app_suite`不以`Test`结尾 | 添加`Adapt001Test`后缀 | `ActsMyHap` → `ActsMyHapAdapt001Test` |
| `ohos_js_app_static_suite`不以`StaticTest`结尾 | 添加`Adapt001StaticTest`后缀 | `ActsMyHap` → `ActsMyHapAdapt001StaticTest` |
| C++工程不以`Test`结尾 | 添加`Adapt001Test`后缀 | `ActsMyModule` → `ActsMyModuleAdapt001Test` |
| 大小写不符合规范 | 确保`A`、`T`、`S`大写 | `ActsStatictest` → `ActsStaticTest` |

**注意**:
- `Adapt`+数字需放在`Test`或`StaticTest`之前
- 数字从001开始递增

## 三、修复步骤

### 3.1 JS/TS工程 - ohos_js_app_suite

**重要说明：target名称与hap_name的关系**

```
ohos_js_app_suite("XXXX") {
  hap_name = "YYYY"
}
```

- **target名称 `XXXX`**：与上层BUILD.gn中deps字段的引用保持一致，**不需要修改**
- **hap_name `YYYY`**：HAP包的实际输出名称，**需要符合R014规范**

修复时**只修改hap_name**，target名称保持不变。

**步骤1**: 修改BUILD.gn文件

```python
# 修复前
ohos_js_app_suite("mytest") {        # target名称，保持不变
  testonly = true
  part_name = "ace_engine"
  subsystem_name = "arkui"
  hap_name = "actsability"  # ✗ 不以Acts开头，不以Test结尾
}

# 修复后
ohos_js_app_suite("mytest") {        # target名称，保持不变
  testonly = true
  part_name = "ace_engine"
  subsystem_name = "arkui"
  hap_name = "ActsAbilityAdapt001Test"  # ✓ 只修改hap_name
}
```

**步骤2**: 同步修改Test.json文件

```json
// 修复前
{
  "hap_name": "ActsAbility"
}

// 修复后
{
  "hap_name": "ActsAbilityAdapt001Test"
}
```

### 3.2 JS/TS工程 - ohos_js_app_static_suite

**重要说明：target名称与hap_name的关系**

与`ohos_js_app_suite`相同，target名称不需要修改，只修改hap_name。

**步骤1**: 修改BUILD.gn文件

```python
# 修复前
ohos_js_app_static_suite("statictest") {  # target名称，保持不变
  testonly = true
  part_name = "ace_engine"
  subsystem_name = "arkui"
  hap_name = "ActsAbility"  # ✗ 不以StaticTest结尾
}

# 修复后
ohos_js_app_static_suite("statictest") {  # target名称，保持不变
  testonly = true
  part_name = "ace_engine"
  subsystem_name = "arkui"
  hap_name = "ActsAbilityAdapt001StaticTest"  # ✓ 只修改hap_name
}
```

**步骤2**: 同步修改Test.json文件

```json
// 修复前
{
  "hap_name": "ActsAbility"
}

// 修复后
{
  "hap_name": "ActsAbilityAdapt001StaticTest"
}
```

### 3.3 C++工程 - ohos_moduletest_suite

**重要说明：target名称就是输出文件名**

```
ohos_moduletest_suite("XXXX") {
  ...
}
```

- `ohos_moduletest_suite`**没有hap_name字段**
- target名称 `XXXX` 就是编译输出的可执行文件名
- 因此**target名称必须符合R014规范**，需要修改

**步骤**: 修改BUILD.gn文件

```python
# 修复前
ohos_moduletest_suite("mymoduletest") {  # ✗ 不以Acts开头
  testonly = true
  part_name = "ace_engine"
  subsystem_name = "arkui"
}

# 修复后
ohos_moduletest_suite("ActsMyModuleAdapt001Test") {  # ✓ target名称需要符合规范
  testonly = true
  part_name = "ace_engine"
  subsystem_name = "arkui"
}
```

**步骤2**: 同步修改Test.json文件

```json
// 修复前
{
  "kits": [
    {
      "push": [
        "mymoduletest->/data/local/tmp/mymoduletest"
      ]
    }
  ],
  "driver": {
    "module-name": "mymoduletest"
  }
}

// 修复后
{
  "kits": [
    {
      "push": [
        "ActsMyModuleAdapt001Test->/data/local/tmp/ActsMyModuleAdapt001Test"
      ]
    }
  ],
  "driver": {
    "module-name": "ActsMyModuleAdapt001Test"
  }
}
```

## 四、常见问题

### Q1: 为什么需要添加Adapt+数字？

A: 为了保持hap名称的唯一性，如果直接添加Test后缀可能导致与现有hap名称冲突，添加Adapt+数字可以确保名称唯一

### Q2: 数字从多少开始？

A: 从001开始，如果已存在Adapt001，则使用Adapt002，依次递增

### Q3: BUILD.gn中的target名称需要修改吗？

A: 取决于模板类型：

| 模板类型 | target名称 | hap_name | 修改说明 |
|---------|-----------|----------|---------|
| `ohos_js_app_suite` | 不需要修改 | 需要修改 | target与hap_name无直接关系 |
| `ohos_js_app_static_suite` | 不需要修改 | 需要修改 | target与hap_name无直接关系 |
| `ohos_moduletest_suite` | **需要修改** | 无此字段 | target名称就是输出文件名 |

**原因说明**：
- `ohos_js_app_suite`和`ohos_js_app_static_suite`的target名称（如`("mytest")`）是与上层BUILD.gn中deps字段的引用保持一致，用户可能将其配置成与hap_name一致，但它们之间没有直接关系
- `ohos_moduletest_suite`没有hap_name字段，target名称直接决定输出文件名，因此必须符合R014规范

### Q4: Test.json在哪里？

A: 通常位于XTS工程的`entry/src/main/`目录下

## 五、验证方法

修复完成后，可以使用以下命令验证：

```bash
/check-test-code-quality /path/to/fixed/code --rules R014
```

如果没有发现问题，则修复成功。
