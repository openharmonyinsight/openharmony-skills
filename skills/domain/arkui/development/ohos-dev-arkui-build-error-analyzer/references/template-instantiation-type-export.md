# 问题：模板显式实例化符号导出失败

## 错误特征

```
ld.lld: error: undefined symbol:
  OHOS::Ace::NG::PaddingPropertyT<OHOS::Ace::NG::CalcLength>::SetEdges
  (OHOS::Ace::NG::CalcLength const&)
>>> referenced by arkts_native_calendar_picker_bridge.cpp:407
>>>               thinlto-cache/llvmcache-xxx:(OHOS::Ace::NG::SetCalendarPickerJSPadding(...))

clang-15: error: linker command failed with exit code 1 (use -v to see invocation)
```

**关键特征**:
- 模板类有显式实例化
- 模板方法已添加 `ACE_FORCE_EXPORT`
- 类似模板的其他类型实例化能正常导出
- 只有特定类型（inline 方法类）的实例化导出失败

## 根本原因

当模板类显式实例化的类型参数满足以下条件时符号导出失败：
1. 类型的关键方法（如 `ToString()`, `operator==`）都是 **inline** 定义（在头文件中）
2. **类型定义本身缺少 `ACE_FORCE_EXPORT`**

模板实例化会继承类型参数的可见性：
- 如果类型没有导出属性 → 整个模板特化被标记为内部可见
- 即使模板方法有 `ACE_FORCE_EXPORT`，也会被类型可见性覆盖

## 对比分析

### 正常工作的版本（Dimension）

| 特性 | Dimension |
|------|-----------|
| **ToString()** | 在 `dimension.cpp` 实现（外部） |
| **FromString()** | 在 `dimension.cpp` 实现（外部） |
| **可见性** | 外部链接（强制生成符号） |
| **导出结果** | ✅ 成功（弱符号 W） |

### 失败的版本（CalcLength）

| 特性 | CalcLength |
|------|------------|
| **ToString()** | **inline** 在头文件 |
| **FromString()** | **inline** 在头文件 |
| **operator==** | **inline** 在头文件 |
| **类型导出** | ❌ 无 `ACE_FORCE_EXPORT` |
| **导出结果** | ❌ 失败（无符号） |

## 诊断步骤

### 1. 确认模板实例化存在

```bash
# 检查显式实例化
grep -n "template struct PaddingPropertyT" \
  frameworks/core/components_ng/property/measure_property.cpp

# 应该看到：
# template struct PaddingPropertyT<CalcLength>;
# template struct PaddingPropertyT<Dimension>;
```

### 2. 检查模板方法有导出标记

```bash
# 检查方法定义
grep -B1 "void PaddingPropertyT<T>::SetEdges" \
  frameworks/core/components_ng/property/measure_property.cpp

# 应该看到：
# ACE_FORCE_EXPORT
# void PaddingPropertyT<T>::SetEdges(const T& padding)
```

### 3. 检查类型的定义方式

```bash
# 检查 CalcLength 类定义
grep -A5 "^class CalcLength\|^struct CalcLength" \
  interfaces/inner_api/ace_kit/include/ui/properties/ng/calc_length.h | head -10

# 检查是否有 ACE_FORCE_EXPORT
```

### 4. 检查方法是否 inline

```bash
# 检查关键方法实现位置
grep -n "ToString\|FromString" \
  interfaces/inner_api/ace_kit/include/ui/properties/ng/calc_length.h

# 如果在头文件中有完整实现体 { ... }，则是 inline
```

### 5. 验证符号导出状态

```bash
# 检查 Dimension 版本（应该有符号）
nm -D out/rk3568/arkui/ace_engine/libace_compatible.z.so | \
  grep "PaddingPropertyT.*Dimension.*SetEdges"

# 检查 CalcLength 版本（失败时无符号）
nm -D out/rk3568/arkui/ace_engine/libace_compatible.z.so | \
  grep "PaddingPropertyT.*CalcLength.*SetEdges"
```

## 解决方案

### 步骤 1: 添加类型级导出

**文件**: `interfaces/inner_api/ace_kit/include/ui/properties/ng/calc_length.h`

**位置**: 类定义

**修改前**:
```cpp
namespace OHOS::Ace::NG {

class CalcLength {  // ❌ 缺少导出标记
public:
    CalcLength() = default;
    std::string ToString() const {
        if (calcValue_.empty()) {
            return dimension_.ToString();
        }
        return calcValue_;
    }
    static CalcLength FromString(const std::string& str) {
        return CalcLength(Dimension::FromString(str));
    }
    // ... 其他 inline 方法
};

} // namespace OHOS::Ace::NG
```

**修改后**:
```cpp
namespace OHOS::Ace::NG {

class ACE_FORCE_EXPORT CalcLength {  // ✅ 添加类型级导出
public:
    CalcLength() = default;
    std::string ToString() const {
        if (calcValue_.empty()) {
            return dimension_.ToString();
        }
        return calcValue_;
    }
    static CalcLength FromString(const std::string& str) {
        return CalcLength(Dimension::FromString(str));
    }
    // ... 其他 inline 方法（保持 inline）
};

} // namespace OHOS::Ace::NG
```

**关键点**:
- ✅ 添加到**类定义**本身
- ✅ 不是单个方法
- ✅ **保持方法 inline**（不要移到 .cpp）

### 步骤 2: 验证修复

```bash
# 重新编译
./build.sh --product-name rk3568 --build-target ace_engine --ccache

# 检查符号导出
nm -D out/rk3568/arkui/ace_engine/libace_compatible.z.so | \
  grep "PaddingPropertyT.*CalcLength"

# 期望输出（12个方法，全部为弱符号 W）:
# 020d009d W _ZN4OHOS3Ace2NG16PaddingPropertyTINS1_10CalcLengthEE8SetEdgesERKS3_
# 020d00c9 W _ZN4OHOS3Ace2NG16PaddingPropertyTINS1_10CalcLengthEE8SetEdgesERKS3_S6_S6_S6_
# 020d00f7 W _ZNK4OHOS3Ace2NG16PaddingPropertyTINS1_10CalcLengthEEeqERKS4_
# 020d01b3 W _ZNK4OHOS3Ace2NG16PaddingPropertyTINS1_10CalcLengthEEneERKS4_
# ... (8 more methods)
```

## 原理解释

### 为什么需要类型级导出？

**模板实例化的可见性继承规则**:

```
模板参数类型（CalcLength）的可见性
    ↓
模板特化（PaddingPropertyT<CalcLength>）的可见性
    ↓
模板方法的可见性
```

如果 `CalcLength` 没有导出属性：
1. 编译器认为它是内部可见类型
2. `PaddingPropertyT<CalcLength>` 特化继承内部可见性
3. 即使方法有 `ACE_FORCE_EXPORT`，编译器也会忽略（因为特化本身是内部的）
4. 生成的符号被标记为内部，不导出

### 为什么 Dimension 版本能工作？

`Dimension` 的关键方法在 `.cpp` 文件中实现：
- `ToString()` 在 `dimension.cpp:218`
- `FromString()` 在 `dimension.cpp:241`

这强制编译器为这些方法生成外部符号，使得 `PaddingPropertyT<Dimension>` 实例化时具有外部链接。

### 完整的导出条件

模板显式实例化成功导出需要**三层保障**：

```
1. 类型级导出
   class ACE_FORCE_EXPORT CalcLength { ... };

2. 方法级导出
   template<typename T>
   ACE_FORCE_EXPORT
   void PaddingPropertyT<T>::SetEdges(...) { ... }

3. 显式实例化
   template struct PaddingPropertyT<CalcLength>;
```

**缺少任何一层都会导致导出失败**。

## 常见错误

### ❌ 错误 1: 将 inline 方法移到 .cpp

**错误做法**:
```cpp
// calc_length.h
class CalcLength {
    std::string ToString() const;  // 移到 .cpp
};

// calc_length.cpp
std::string CalcLength::ToString() const { /* ... */ }
```

**为什么错误**:
- 破坏头文件优化
- 增加编译依赖
- 降低编译速度
- 违背代码优化目标

### ❌ 错误 2: 只给单个方法加导出

**错误做法**:
```cpp
class CalcLength {
    ACE_FORCE_EXPORT std::string ToString() const { /* ... */ }
    ACE_FORCE_EXPORT static CalcLength FromString(...) { /* ... */ }
};
```

**为什么错误**:
- 不解决根本问题（类型可见性）
- 模板实例化仍然失败

### ❌ 错误 3: 移除显式实例化

**错误做法**:
```cpp
// 移除 template struct PaddingPropertyT<CalcLength>;
// 期望编译器自动实例化
```

**为什么错误**:
- `extern template` 声明阻止隐式实例化
- 会导致其他编译单元错误
- 失去显式控制符号生成的机会

## 预防措施

### 判断是否需要类型级导出

需要添加 `ACE_FORCE_EXPORT` 到类定义：
- ✅ 类有 inline 方法（在头文件实现）
- ✅ 类用作模板参数且模板需要显式实例化
- ✅ 模板实例化的符号需要被其他模块使用
- ✅ 模板方法已添加 `ACE_FORCE_EXPORT` 但仍导出失败

不需要类型级导出：
- ❌ 类的所有方法都在 .cpp 实现
- ❌ 类仅内部使用，不用作模板参数
- ❌ 模板不需要显式实例化

### 模板导出检查清单

创建需要显式实例化的模板时：

1. ✅ 模板方法在 .cpp 中有 `ACE_FORCE_EXPORT`
2. ✅ 显式实例化在 .cpp 中（`template struct ClassName<Type>;`）
3. ✅ 如果类型参数有 inline 方法，给类型加 `ACE_FORCE_EXPORT`
4. ✅ 在 libace.map 中添加通配符（如 `PaddingPropertyT*;`）
5. ✅ 用 `nm -D` 验证符号导出
6. ✅ **保持 inline 方法在头文件**（不要移到 .cpp）

### ⚠️ 重要：不要破坏头文件优化

**原则**: 保持 inline 方法在头文件

**理由**:
- 头文件优化是战略性工作（如 StringUtils 重构，commit e0fd3724d21）
- 移动 inline 方法到 .cpp 会：
  - 增加编译时间
  - 增加头文件依赖
  - 降低增量编译效率
  - 浪费之前的优化工作

**正确做法**: 添加类型级 `ACE_FORCE_EXPORT`，保持方法 inline

## 相关案例

- **基础符号导出**: 参见 `symbol-export-ace-force-export.md`
- **libace.map 白名单**: 参见 `symbol-export-libace-map.md`
- **缺少 .cpp 实现**: 参见 `undefined-symbol-missing-cpp.md`

## 参考资料

- **文件**: `interfaces/inner_api/ace_kit/include/ui/properties/ng/calc_length.h:25`
- **文件**: `frameworks/core/components_ng/property/measure_property.cpp:308-309`
- **提交**: StringUtils 头文件优化 (commit e0fd3724d21)
- **日期**: 2026-02-01
