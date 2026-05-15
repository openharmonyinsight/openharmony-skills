# 问题：构建系统配置 - ace_core_ng_source_set

## 问题描述

添加了新的 .cpp 文件到组件 BUILD.gn，但 libace.z.so 链接时仍然报 "undefined symbol"。

## 错误特征

```
[666/809] SOLINK arkui/ace_engine/libace.z.so
FAILED: arkui/ace_engine/libace.z.so
ld.lld: error: undefined symbol: OHOS::Ace::ClassName::MethodName
>>> referenced by some_file.cpp
```

同时，.cpp 文件确实存在于组件的 BUILD.gn 中。

## 根本原因

OpenHarmony 的构建架构中，libace.z.so 只链接 ace_core_ng 库，不链接各个组件的独立库。

## 构建架构解析

### 库的层次结构

```
┌────────────────────────────────────────────────┐
│  libace.z.so (ACE Engine 最终产物)            │
│  ↓ 只链接这些库:                              │
│  - ace_core_ng_ohos_ng                        │
│  - ace_core_ng_ohos                           │
│  - ace_core_ohos                              │
└────────────────────────────────────────────────┘
                    ↕
┌────────────────────────────────────────────────┐
│  ace_core_ng 库                               │
│  包含: frameworks/core/BUILD.gn 中定义        │
│  ace_core_ng_source_set 模板中的所有源文件    │
└────────────────────────────────────────────────┘
                    ↕
┌────────────────────────────────────────────────┐
│  组件库（不会被 libace.z.so 链接）            │
│  - ace_core_components_text_ohos              │
│  - ace_core_components_common_ohos            │
│  - ace_core_components_button_ohos            │
│  - etc.                                       │
└────────────────────────────────────────────────┘
```

### 关键点

1. **组件库的目的**: 提供模块化编译，不用于最终链接
2. **ace_core_ng_source_set**: 汇集所有需要进入 libace.z.so 的源文件
3. **文件需要同时在两处**:
   - 组件 BUILD.gn：用于组件内编译
   - ace_core_ng_source_set：用于 libace.z.so 链接

## 诊断步骤

### 1. 确认 .cpp 已添加到组件 BUILD.gn

```bash
# 检查组件 BUILD.gn
grep "new_file.cpp" frameworks/core/components/<component>/BUILD.gn
```

期望：找到该文件。

### 2. 检查是否在 ace_core_ng_source_set

```bash
# 检查 frameworks/core/BUILD.gn
grep "new_file.cpp" frameworks/core/BUILD.gn
```

如果找不到，就是问题所在。

### 3. 确认 libace.z.so 需要这个符号

```bash
# 查看哪些库使用了相关符号
grep -r "ClassName::MethodName" --include="*.cpp" frameworks/ | grep -v "new_file.cpp"
```

### 4. 验证构建流程

```bash
# 查看编译目标文件
ls -la out/rk3568/obj/foundation/arkui/ace_engine/*/new_file.o

# 如果存在，说明编译成功，但未链接到 libace.z.so
```

## 解决方案

### 修改 frameworks/core/BUILD.gn

**文件**: `frameworks/core/BUILD.gn`

**位置**: `template("ace_core_ng_source_set")` 模板内的 `sources` 列表

**修改前**:
```gn
template("ace_core_ng_source_set") {
  sources = [
    # ... 其他文件 ...
    "components/other/other_file.cpp",
    # 新文件在这里
  ]
}
```

**修改后**:
```gn
template("ace_core_ng_source_set") {
  sources = [
    # ... 其他文件 ...
    "components/other/other_file.cpp",
    "components/<component>/new_file.cpp",  # ✅ 添加这里
  ]
}
```

### 路径规则

路径格式：
- 相对于 `frameworks/` 目录
- 包含 `components/` 或 `components_ng/` 前缀
- 使用正斜杠 `/`，不以斜杠开头或结尾

**示例**:
```gn
"components/text/text_theme.cpp",                    # ✅ 正确
"components_ng/pattern/button/button_layout_property.cpp",  # ✅ 正确
"components/common/properties/advanced_text_style.cpp",  # ✅ 正确

"/components/text/text_theme.cpp",                   # ❌ 错误：有前导斜杠
"components\\text\\text_theme.cpp",                  # ❌ 错误：Windows 路径分隔符
"text_theme.cpp",                                   # ❌ 错误：缺少组件路径
```

## 常见场景

### 场景 1: 头文件优化后添加 .cpp

**背景**: 将内联函数移到 .cpp 文件以减少头文件依赖

**步骤**:
1. 创建 `text_theme.cpp`，包含实现
2. 添加到 `frameworks/core/components/text/BUILD.gn`
3. **关键**：添加到 `frameworks/core/BUILD.gn` ace_core_ng_source_set

### 场景 2: 重构时创建新的实现文件

**背景**: 将大类拆分，创建新的实现文件

**步骤**:
1. 创建 `advanced_text_style.cpp`
2. 添加到 `frameworks/core/components/common/BUILD.gn`
3. **关键**：添加到 `frameworks/core/BUILD.gn` ace_core_ng_source_set

### 场景 3: 添加新的模式类

**背景**: 创建新的 pattern 实现

**步骤**:
1. 创建 `button_layout_property.cpp`
2. 添加到 `frameworks/core/components_ng/pattern/BUILD.gn`
3. **关键**：添加到 `frameworks/core/BUILD.gn` ace_core_ng_source_set

## 验证方法

### 1. 检查源文件被编译

```bash
# 编译
./build.sh --product-name rk3568 --build-target ace_engine --ccache

# 检查目标文件
ls -la out/rk3568/obj/foundation/arkui/ace_engine/*/new_file.o
```

应该看到目标文件存在。

### 2. 检查符号在 libace.z.so 中

```bash
# 检查动态库符号表
nm -D out/rk3568/arkui/ace_engine/libace.z.so | grep ClassName
```

应该看到相关符号。

### 3. 检查链接错误

```bash
# 统计链接错误数量
grep "ld.lld: error:" out/rk3568/build.log | wc -l
```

期望：0（无错误）

## 注意事项

### 1. 不要添加到错误的位置

**错误位置**:
```gn
# ❌ 不要添加到这里
ohos_shared_library("ace_core_components_text_ohos") {
  sources = [
    "text_theme.cpp",  # 这里是组件库
  ]
}
```

**正确位置**:
```gn
# ✅ 添加到这里
template("ace_core_ng_source_set") {
  sources = [
    "components/text/text_theme.cpp",  # 这里是 NG 汇聚点
  ]
}
```

### 2. 保持路径一致

确保 ace_core_ng_source_set 中的路径与实际文件位置一致。

```bash
# 验证路径
ls frameworks/core/components/text/text_theme.cpp
# 确保文件存在
```

### 3. 避免重复添加

检查文件是否已经在 ace_core_ng_source_set 中：

```bash
grep "text_theme.cpp" frameworks/core/BUILD.gn
```

如果已经存在，不要重复添加。

## 相关案例

- **未定义符号**: 参见 `undefined-symbol-missing-cpp.md`
- **符号导出**: 参见 `symbol-export-ace-force-export.md`
