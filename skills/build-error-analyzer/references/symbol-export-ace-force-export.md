# 问题：跨模块符号未导出 - ACE_FORCE_EXPORT

## 错误特征

```
ld.lld: error: undefined symbol: OHOS::Ace::NG::DialogTypeMargin::UpdateDialogMargin(...)
>>> referenced by dialog_button.cpp (timepicker module)

clang-15: error: linker command failed with exit code 1 (use -v to see invocation)
ninja: build stopped: subcommand failed.
```

**关键特征**: 符号在一个模块中定义，被另一个模块（如 timepicker）使用，但链接时找不到。

## 根本原因

符号被其他模块使用，但没有从 libace.z.so 导出。跨模块使用的符号需要显式标记为导出。

## 诊断步骤

### 1. 确认符号定义存在

```bash
# 查找符号定义
grep -r "UpdateDialogMargin" --include="*.cpp" frameworks/

# 应该找到实现文件
```

### 2. 确认被其他模块使用

```bash
# 查看错误信息中的引用位置
# >>> referenced by dialog_button.cpp (timepicker module)

# 确认引用模块
grep -r "UpdateDialogMargin" foundation/arkui/ace_engine/../timepicker/
```

### 3. 检查符号是否导出

```bash
# 检查 libace.z.so 符号表
nm -D out/rk3568/arkui/ace_engine/libace.z.so | grep DialogTypeMargin
```

如果没有输出，说明符号未导出。

### 4. 检查是否有 ACE_FORCE_EXPORT

```bash
# 查找声明位置
grep -r "UpdateDialogMargin" --include="*.h" frameworks/
```

检查声明前是否有 `ACE_FORCE_EXPORT`。

## 解决方案

### 步骤 1: 添加 ACE_FORCE_EXPORT 到声明

**文件**: `<module>/<class>.h`（头文件，不是 .cpp）

**位置**: 类声明中的方法声明

**修改前**:
```cpp
class DialogTypeMargin {
public:
    static void UpdateDialogMargin(bool isRtl, MarginProperty& margin,
        const RefPtr<DialogTheme>& dialogTheme, bool isLessThanTwelve,
        ModuleDialogType type);
};
```

**修改后**:
```cpp
class DialogTypeMargin {
public:
    ACE_FORCE_EXPORT static void UpdateDialogMargin(bool isRtl, MarginProperty& margin,
        const RefPtr<DialogTheme>& dialogTheme, bool isLessThanTwelve,
        ModuleDialogType type);
};
```

**关键点**:
- ✅ 添加到**头文件** (.h) 的**声明**
- ❌ 不是添加到实现文件 (.cpp)
- ✅ 添加在返回类型之前

### 步骤 2: 添加到 libace.map 白名单

**文件**: `build/libace.map`

**位置**: `global: extern "C++"` 区块内

**修改**:
```
global:
  extern "C++" {
    # ... 其他符号 ...
    OHOS::Ace::NG::DialogView::CreateDialogNode*;
    OHOS::Ace::NG::DialogTypeMargin::UpdateDialogMargin*;  # ✅ 添加这一行
    OHOS::Ace::PixelMap::*;
    # ...
  }
}
```

**符号格式**:
```
OHOS::Ace::[NG::]ClassName::MethodName*;
```

关键部分：
- 命名空间：完整的命名空间路径
- 类名：包含所有嵌套类
- 方法名：方法名后加 `*;`
- 不包含参数类型

## 原理解释

### 为什么需要导出？

1. **符号可见性**：
   - 默认情况下，C++ 符号是隐藏的（不可被其他动态库使用）
   - ACE_FORCE_EXPORT 将符号标记为可见

2. **动态链接**：
   - timepicker.so 需要在运行时从 libace.z.so 导入符号
   - 如果符号未导出，链接器会报 "undefined symbol"

3. **版本脚本**：
   - libace.map 控制哪些符号从 libace.z.so 导出
   - 未在白名单的符号即使有 ACE_FORCE_EXPORT 也不会导出

### 导出流程

```
1. 源代码
   ↓
2. ACE_FORCE_EXPORT（标记可见性）
   ↓
3. 编译器生成符号
   ↓
4. libace.map（过滤可导出符号）
   ↓
5. libace.z.so（只包含白名单中的符号）
   ↓
6. 其他模块可以导入使用
```

## 验证方法

### 1. 检查符号已导出

```bash
# 检查 libace.z.so 符号表
nm -D out/rk3568/arkui/ace_engine/libace.z.so | grep DialogTypeMargin
```

**期望输出**:
```
00eb4dd1 T _ZN4OHOS3Ace2NG16DialogTypeMargin18UpdateDialogMargin...
```

- `T` 表示符号在代码段（已导出）
- 如果没有输出，说明导出失败

### 2. 检查符号被正确导入

```bash
# 检查使用该符号的动态库
nm -D out/rk3568/arkui/libarkui_timepicker.z.so | grep DialogTypeMargin
```

**期望输出**:
```
         U _ZN4OHOS3Ace2NG16DialogTypeMargin18UpdateDialogMargin...
```

- `U` 表示符号未定义（从其他库导入）

### 3. 重新构建验证

```bash
# 清理并重新构建
rm -rf out/rk3568/arkui/ace_engine/
./build.sh --product-name rk3568 --build-target ace_engine --ccache

# 检查链接错误
grep "ld.lld: error:" out/rk3568/build.log | grep DialogTypeMargin
```

**期望**: 无输出（0 个错误）

## 常见错误

### 错误 1: 添加到 .cpp 而非 .h

**症状**: 添加 ACE_FORCE_EXPORT 后仍然报 undefined symbol

**原因**: 添加到了实现文件而非头文件声明

**解决**: 移到头文件的方法声明上

### 错误 2: libace.map 格式错误

**症状**: 编译错误 "syntax error in version script"

**原因**: libace.map 中的符号格式不正确

**解决**: 检查格式，确保以 `*;` 结尾

### 错误 3: 符号名不完整

**症状**: 符号表中有符号，但其他模块仍找不到

**原因**: libace.map 中的符号名不完整（缺少命名空间）

**解决**: 使用完整的命名空间路径

## 预防措施

### 判断是否需要导出的规则

需要导出（添加 ACE_FORCE_EXPORT + libace.map）：
- ✅ 方法被其他模块（非 ace_engine）使用
- ✅ 类被其他模块继承或实例化
- ✅ 全局变量/常量被其他模块访问

不需要导出：
- ❌ 仅在 ace_engine 内部使用
- ❌ private/protected 成员
- ❌ 内部实现细节

### 添加导出的清单

1. 确认符号被其他模块使用
2. 在头文件声明前添加 ACE_FORCE_EXPORT
3. 在 libace.map 添加符号白名单
4. 编译验证
5. 用 nm -D 检查符号表
6. 测试其他模块链接

## 相关案例

- **未定义符号（缺少 .cpp）**: 参见 `undefined-symbol-missing-cpp.md`
- **libace.map 白名单**: 参见 `symbol-export-libace-map.md`
