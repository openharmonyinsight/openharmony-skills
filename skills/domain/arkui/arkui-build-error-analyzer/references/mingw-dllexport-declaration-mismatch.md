# 问题：MinGW 平台 dllexport 属性声明不一致

## 错误特征

```
FAILED: mingw_x86_64/obj/foundation/arkui/ace_engine/frameworks/core/components_ng/property/
ace_core_components_property_ng_windows/measure_property.o

../../foundation/arkui/ace_engine/frameworks/core/components_ng/property/measure_property.cpp:313:27:
error: redeclaration of 'OHOS::Ace::NG::PaddingPropertyT::SetEdges' cannot add 'dllexport' attribute
void PaddingPropertyT<T>::SetEdges(const T& padding)
                          ^
../../foundation/arkui/ace_engine/interfaces/inner_api/ace_kit/include/ui/properties/ng/measure_property.h:47:10:
note: previous declaration is here
    void SetEdges(const T& padding);
         ^

../../foundation/arkui/ace_engine/frameworks/core/components_ng/property/measure_property.cpp:323:27:
error: redeclaration of 'OHOS::Ace::NG::PaddingPropertyT::SetEdges' cannot add 'dllexport' attribute
void PaddingPropertyT<T>::SetEdges(const T& leftValue, const T& rightValue, const T& topValue, const T& bottomValue)
                          ^
../../foundation/arkui/ace_engine/interfaces/inner_api/ace_kit/include/ui/properties/ng/measure_property.h:48:10:
note: previous declaration is here
    void SetEdges(const T& leftValue, const T& rightValue, const T& topValue, const T& bottomValue);
         ^
```

**关键特征**:
- 只在 **MinGW/Windows 平台**编译时出现
- 错误信息：`redeclaration cannot add 'dllexport' attribute`
- 头文件声明和 .cpp 实现的导出属性不一致
- 通常在添加了 `ACE_FORCE_EXPORT` 到模板方法后触发

## 根本原因

**MinGW DLL 导出规则**：对于 Windows 平台的 DLL 导出，方法声明和定义的导出属性必须完全一致。

- 如果头文件中没有 `__declspec(dllexport)` (ACE_FORCE_EXPORT)
- 但实现文件中有 `__declspec(dllexport)`
- MinGW 编译器会报错：`redeclaration cannot add 'dllexport' attribute`

这与 Linux/MacOS 不同：
- **Linux/MacOS**: 使用 `__attribute__((visibility("default")))`，对声明/定义不一致更宽容
- **Windows (MinGW/MSVC)**: 使用 `__declspec(dllexport)`，要求严格一致

## 诊断步骤

### 1. 确认是 MinGW 编译

```bash
# 检查编译命令
grep "mingw_x86_64.*measure_property.o" out/sdk/build.log

# 应该看到 MinGW 编译器：
# ../../prebuilts/mingw-w64/ohos/linux-x86_64/clang-mingw/bin/clang++
```

### 2. 比对声明和实现

```bash
# 查看头文件声明
grep -A1 "void SetEdges" \
  interfaces/inner_api/ace_kit/include/ui/properties/ng/measure_property.h

# 查看实现文件定义
grep -B2 "void PaddingPropertyT<T>::SetEdges" \
  frameworks/core/components_ng/property/measure_property.cpp
```

**不一致示例**:
```cpp
// 头文件（无导出标记）
void SetEdges(const T& leftValue, const T& rightValue, const T& topValue, const T& bottomValue);

// 实现文件（有导出标记）
template<typename T>
ACE_FORCE_EXPORT
void PaddingPropertyT<T>::SetEdges(const T& leftValue, const T& rightValue, const T& topValue, const T& bottomValue)
{
    // ...
}
```

### 3. 检查所有重载方法

```bash
# 找出所有重载方法，检查是否一致
grep -n "SetEdges\|operator==" \
  interfaces/inner_api/ace_kit/include/ui/properties/ng/measure_property.h
```

## 解决方案

### 步骤 1: 统一头文件中的导出标记

**文件**: `interfaces/inner_api/ace_kit/include/ui/properties/ng/measure_property.h`

**修改前**:
```cpp
template<typename T>
struct PaddingPropertyT {
    std::optional<T> left;
    std::optional<T> right;
    std::optional<T> top;
    std::optional<T> bottom;

    ACE_FORCE_EXPORT void SetEdges(const T& padding);
    void SetEdges(const T& leftValue, const T& rightValue, const T& topValue, const T& bottomValue);  // ❌ 缺少
    ACE_FORCE_EXPORT bool operator==(const PaddingPropertyT& value) const;
    bool operator!=(const PaddingPropertyT& value) const;  // ❌ 缺少
    ACE_FORCE_EXPORT bool UpdateWithCheck(const PaddingPropertyT& value);
    ACE_FORCE_EXPORT bool UpdateLocalizedPadding(const PaddingPropertyT& value);
    ACE_FORCE_EXPORT void checkNeedReset(const PaddingPropertyT& value);
    ACE_FORCE_EXPORT std::string ToString() const;
    std::string ToJsonString() const;  // ⚠️ 也需要一致
    // ...
};
```

**修改后**:
```cpp
template<typename T>
struct PaddingPropertyT {
    std::optional<T> left;
    std::optional<T> right;
    std::optional<T> top;
    std::optional<T> bottom;

    ACE_FORCE_EXPORT void SetEdges(const T& padding);
    ACE_FORCE_EXPORT void SetEdges(const T& leftValue, const T& rightValue, const T& topValue, const T& bottomValue);  // ✅ 添加
    ACE_FORCE_EXPORT bool operator==(const PaddingPropertyT& value) const;
    ACE_FORCE_EXPORT bool operator!=(const PaddingPropertyT& value) const;  // ✅ 添加
    ACE_FORCE_EXPORT bool UpdateWithCheck(const PaddingPropertyT& value);
    ACE_FORCE_EXPORT bool UpdateLocalizedPadding(const PaddingPropertyT& value);
    ACE_FORCE_EXPORT void checkNeedReset(const PaddingPropertyT& value);
    ACE_FORCE_EXPORT std::string ToString() const;
    ACE_FORCE_EXPORT std::string ToJsonString() const;  // ✅ 添加
    // ...
};
```

### 步骤 2: 确保实现文件一致

**文件**: `frameworks/core/components_ng/property/measure_property.cpp`

**检查实现**:
```cpp
template<typename T>
ACE_FORCE_EXPORT
void PaddingPropertyT<T>::SetEdges(const T& leftValue, const T& rightValue, const T& topValue, const T& bottomValue)
{
    left = leftValue;
    right = rightValue;
    top = topValue;
    bottom = bottomValue;
}

template<typename T>
ACE_FORCE_EXPORT
bool PaddingPropertyT<T>::operator!=(const PaddingPropertyT& value) const
{
    return !(*this == value);
}
```

确保实现文件中也有 `ACE_FORCE_EXPORT`。

### 步骤 3: 验证修复

```bash
# 重新编译 SDK（MinGW 目标）
./build.sh --product-name ohos-sdk --build-target ace_engine_sdk --ccache

# 检查编译错误
grep "cannot add 'dllexport' attribute" out/sdk/build.log

# 期望: 无输出（0 个错误）
```

## 原理解释

### MinGW DLL 导出机制

**Windows DLL 导出要求**:

```
头文件声明                实现文件定义              结果
─────────────────────────────────────────────────────────────
__declspec(dllexport)   __declspec(dllexport)    ✅ 成功
无导出标记              无导出标记               ✅ 成功（内部符号）
无导出标记              __declspec(dllexport)    ❌ 编译失败
__declspec(dllexport)   无导出标记               ⚠️ 警告（可能失败）
```

**为什么要求一致？**

1. **符号表一致性**: 编译器在解析头文件时记录符号属性，实现必须匹配
2. **DLL 接口契约**: 导出属性是 API 契约的一部分，声明和定义不能矛盾
3. **链接器要求**: MinGW 链接器对 DLL 导出符号有严格检查

### 与 Linux/MacOS 的区别

| 平台 | 导出宏 | 声明/定义一致性要求 | 错误消息 |
|------|--------|-------------------|----------|
| **MinGW/Windows** | `__declspec(dllexport)` | **严格一致** | `redeclaration cannot add 'dllexport' attribute` |
| **Linux (GCC/Clang)** | `__attribute__((visibility("default")))` | 宽松，定义优先 | 链接时可能警告 |
| **macOS (Clang)** | `__attribute__((visibility("default")))` | 宽松，定义优先 | 链接时可能警告 |

### ACE_FORCE_EXPORT 的定义

```cpp
// 在不同平台下的定义
#if defined(_WIN32) || defined(_WIN64)
    #define ACE_FORCE_EXPORT __declspec(dllexport)
#elif defined(__GNUC__)
    #define ACE_FORCE_EXPORT __attribute__((visibility("default")))
#else
    #define ACE_FORCE_EXPORT
#endif
```

在 Windows 下展开为 `__declspec(dllexport)`，因此必须遵守 MinGW 的严格规则。

## 常见错误

### ❌ 错误 1: 只修改实现文件

**错误做法**:
```cpp
// 只在 .cpp 中添加 ACE_FORCE_EXPORT
template<typename T>
ACE_FORCE_EXPORT
void PaddingPropertyT<T>::SetEdges(const T&, const T&, const T&, const T&) { ... }
```

**为什么错误**:
- 头文件声明没有导出标记
- MinGW 编译器发现声明和定义不匹配
- 编译失败

### ❌ 错误 2: 部分重载方法添加标记

**错误做法**:
```cpp
// 只给第一个 SetEdges 添加
ACE_FORCE_EXPORT void SetEdges(const T& padding);
void SetEdges(const T&, const T&, const T&, const T&);  // ❌ 忘记添加
```

**为什么错误**:
- 同名方法的不同重载都需要一致处理
- 部分添加会导致编译错误
- 容易遗漏其他重载版本

### ❌ 错误 3: 混淆内联方法和非内联方法

**错误做法**:
```cpp
// 头文件中的内联方法
std::string ToString() const {
    return "some string";  // 内联实现
}

// 期望在 .cpp 中添加导出标记
template<typename T>
ACE_FORCE_EXPORT
std::string PaddingPropertyT<T>::ToString() const { ... }  // ❌ 冲突
```

**为什么错误**:
- 头文件中已有内联实现
- .cpp 中重复定义
- 需要选择一种方式（推荐头文件内联 + 导出标记）

## 预防措施

### 添加模板方法导出的清单

**在添加 ACE_FORCE_EXPORT 时**:

1. ✅ 确认是否需要导出（跨模块使用）
2. ✅ 给头文件中的**所有声明**添加 `ACE_FORCE_EXPORT`
3. ✅ 给实现文件中的**所有定义**添加 `ACE_FORCE_EXPORT`
4. ✅ 检查所有重载版本（不遗漏）
5. ✅ 确认内联方法不在 .cpp 中重复定义
6. ✅ 在 Windows/MinGW 平台测试编译

### 检查脚本

```bash
# 检查声明和实现的一致性
#!/bin/bash
HEADER="interfaces/inner_api/ace_kit/include/ui/properties/ng/measure_property.h"
IMPL="frameworks/core/components_ng/property/measure_property.cpp"

# 提取头文件中的方法声明（包括 ACE_FORCE_EXPORT）
echo "=== 头文件声明 ==="
grep -E "ACE_FORCE_EXPORT.*void SetEdges|void SetEdges" "$HEADER"

echo ""
echo "=== 实现文件定义 ==="
grep -B2 "void PaddingPropertyT<T>::SetEdges" "$IMPL"
```

### 编译平台测试矩阵

| 目标平台 | 编译命令 | 预期结果 |
|---------|---------|---------|
| **rk3568** (Linux) | `./build.sh --product-name rk3568 --build-target ace_engine` | ✅ 应该成功 |
| **ohos-sdk** (MinGW) | `./build.sh --product-name ohos-sdk --build-target ace_engine_sdk` | ✅ 应该成功 |
| **Windows 预览** | MinGW 编译 | ✅ 应该成功 |

## 修复验证

### 完整测试流程

```bash
# 1. 清理构建缓存
rm -rf out/sdk/arkui/ace_engine/

# 2. 重新编译 SDK
./build.sh --product-name ohos-sdk --build-target ace_engine_sdk --ccache

# 3. 检查 MinGW 编译错误
grep "cannot add 'dllexport' attribute" out/sdk/build.log
# 期望: 无输出

# 4. 检查其他编译错误
grep "error:" out/sdk/build.log | head -20
# 期望: 无 dllexport 相关错误

# 5. 验证生成的库文件
ls -lh out/sdk/mingw_x86_64/arkui/ace_engine/libace_compatible.z.so
# 期望: 文件存在且大小合理
```

### 符号导出验证

```bash
# 检查 Windows DLL 导出符号
mingw-nm -D out/sdk/mingw_x86_64/arkui/ace_engine/libace_compatible.z.so | \
  grep "PaddingPropertyT.*SetEdges"

# 期望输出（导出的符号）:
# 00000000 T _ZN4OHOS3Ace2NG16PaddingPropertyT...8SetEdgesERKS3_
# 00000000 T _ZN4OHOS3Ace2NG16PaddingPropertyT...8SetEdgesERKS3_S6_S6_S6_
```

## 相关案例

- **模板显式实例化导出**: 参见 `template-instantiation-type-export.md`
- **基础符号导出**: 参见 `symbol-export-ace-force-export.md`
- **libace.map 白名单**: 参见 `symbol-export-libace-map.md`

## 参考资料

- **文件**: `interfaces/inner_api/ace_kit/include/ui/properties/ng/measure_property.h:47-61`
- **文件**: `frameworks/core/components_ng/property/measure_property.cpp:312-343`
- **MinGW 文档**: https://sourceware.org/binutils/docs/ld/WIN32.html
- **MSVC dllexport**: https://docs.microsoft.com/en-us/cpp/cpp/dllexport-dllimport
- **日期**: 2026-02-04
