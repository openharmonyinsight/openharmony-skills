# 问题：符号导出配置 - libace.map 白名单

## 问题描述

符号已添加 ACE_FORCE_EXPORT，但链接时仍报 "undefined symbol"。

## 错误特征

```
ld.lld: error: undefined symbol: OHOS::Ace::NG::ClassName::MethodName
>>> referenced by other_module.cpp
```

同时：
- .cpp 文件已添加到构建系统
- 符号声明前有 ACE_FORCE_EXPORT
- 但其他模块仍然找不到符号

## 根本原因

libace.map 版本脚本控制 libace.z.so 导出的符号。未在白名单的符号即使有 ACE_FORCE_EXPORT 也不会导出。

## libace.map 作用

### 什么是 libace.map？

libace.map 是链接器版本脚本，控制哪些符号从 libace.z.so 导出到动态符号表。

**作用**:
1. **限制导出**: 只导出白名单中的符号
2. **版本控制**: 管理符号的 ABI 版本
3. **减少符号表**: 只暴露必要的公共接口

### 符号过滤流程

```
源代码
  ↓
编译 (生成符号)
  ↓
ACE_FORCE_EXPORT (标记可见性)
  ↓
libace.map (过滤) ← 关键步骤
  ↓
libace.z.so 动态符号表
  ↓
其他模块可以导入
```

## 诊断步骤

### 1. 确认 ACE_FORCE_EXPORT 存在

```bash
# 查找头文件声明
grep -r "ClassName::MethodName" --include="*.h" frameworks/ | grep ACE_FORCE_EXPORT
```

期望：找到带有 ACE_FORCE_EXPORT 的声明。

### 2. 检查符号是否在 libace.map

```bash
# 查找符号白名单
grep "ClassName::MethodName" build/libace.map
```

如果找不到，就是问题所在。

### 3. 检查符号是否实际导出

```bash
# 检查 libace.z.so 符号表
nm -D out/rk3568/arkui/ace_engine/libace.z.so | grep MethodName
```

如果没有输出，说明符号未导出。

### 4. 查看完整符号名

```bash
# 使用 c++filt 解码符号名
nm -D out/rk3568/arkui/ace_engine/libace.z.so | grep MethodName | c++filt
```

这会显示可读的符号名。

## 解决方案

### 修改 build/libace.map

**文件**: `build/libace.map`

**位置**: `global: extern "C++"` 区块内

**修改前**:
```
global:
  extern "C++" {
    OHOS::Ace::NG::DialogView::CreateDialogNode*;
    OHOS::Ace::PixelMap::*;
    # ... 其他符号 ...
  }
}
```

**修改后**:
```
global:
  extern "C++" {
    OHOS::Ace::NG::DialogView::CreateDialogNode*;
    OHOS::Ace::NG::ClassName::MethodName*;  # ✅ 添加这一行
    OHOS::Ace::PixelMap::*;
    # ... 其他符号 ...
  }
}
```

## 符号格式规则

### 基本格式

```
OHOS::Ace::[NG::]ClassName::MethodName*;
```

### 各部分说明

1. **命名空间**: 完整的命名空间路径
   ```
   OHOS::Ace::NG::           # NG 子命名空间
   OHOS::Ace::               # Ace 命名空间
   ```

2. **类名**: 包含所有嵌套类
   ```
   ClassName                 # 简单类
   Outer::Inner::ClassName   # 嵌套类
   ```

3. **方法名**: 方法的名称
   ```
   MethodName                # 简单方法
   ~ClassName                # 析构函数
   operator=                 # 运算符
   ```

4. **通配符**: 以 `*;` 结尾
   ```
   ClassName::MethodName*;  # 必须以 *; 结尾
   ```

### 示例

| C++ 声明 | libace.map 格式 |
|---------|----------------|
| `void DialogTypeMargin::UpdateDialogMargin(...)` | `OHOS::Ace::NG::DialogTypeMargin::UpdateDialogMargin*;` |
| `DialogView* DialogView::CreateDialogNode(...)` | `OHOS::Ace::NG::DialogView::CreateDialogNode*;` |
| `TextTheme::~TextTheme()` | `OHOS::Ace::TextTheme::~TextTheme*;` |
| `RefPtr<Theme> ThemeManager::CreateTheme(...)` | `OHOS::Ace::ThemeManager::CreateTheme*;` |

## 特殊情况

### 1. 模板实例化

```cpp
// 显式实例化
template class Pattern<DialogType>;
```

libace.map 格式:
```
OHOS::Ace::Pattern<OHOS::Ace::DialogType>*;
```

### 2. 运算符

```cpp
void operator=(const TextStyle&);
```

libace.map 格式:
```
OHOS::Ace::TextStyle::operator=*;
```

### 3. 嵌套类

```cpp
class Outer {
    class Inner {
        void Method();
    };
};
```

libace.map 格式:
```
OHOS::Ace::Outer::Inner::Method*;
```

## 常见错误

### 错误 1: 缺少命名空间

**错误**:
```
ClassName::MethodName*;  # ❌ 缺少 OHOS::Ace::
```

**正确**:
```
OHOS::Ace::NG::ClassName::MethodName*;  # ✅ 完整命名空间
```

### 错误 2: 缺少 NG 子命名空间

**错误**:
```
OHOS::Ace::DialogTypeMargin::UpdateDialogMargin*;  # ❌ 缺少 NG::
```

**正确**:
```
OHOS::Ace::NG::DialogTypeMargin::UpdateDialogMargin*;  # ✅ 包含 NG::
```

### 错误 3: 缺少通配符

**错误**:
```
OHOS::Ace::ClassName::MethodName;  # ❌ 缺少 *;
```

**正确**:
```
OHOS::Ace::ClassName::MethodName*;  # ✅ 以 *; 结尾
```

### 错误 4: 包含参数类型

**错误**:
```
OHOS::Ace::ClassName::MethodName(bool, int)*;  # ❌ 不需要参数
```

**正确**:
```
OHOS::Ace::ClassName::MethodName*;  # ✅ 只需要方法名
```

## 验证方法

### 1. 语法检查

```bash
# 检查 libace.map 语法
python3 -c "
import re
with open('build/libace.map') as f:
    content = f.read()
    # 简单语法检查
    if 'extern \"C++\"' in content:
        print('✅ C++ export block found')
    # 检查符号格式
    symbols = re.findall(r'OHOS::Ace::[\w:]+::\w+\*;', content)
    print(f'Found {len(symbols)} symbols')
"
```

### 2. 重新构建

```bash
# 清理并重新构建
rm -rf out/rk3568/arkui/ace_engine/
./build.sh --product-name rk3568 --build-target ace_engine --ccache
```

### 3. 检查符号导出

```bash
# 使用 nm 检查符号表
nm -D out/rk3568/arkui/ace_engine/libace.z.so | grep -i methodname

# 使用 c++filt 解码
nm -D out/rk3568/arkui/ace_engine/libace.z.so | grep MethodName | c++filt
```

期望：看到符号名（T 标记，表示在代码段）。

### 4. 检查链接

```bash
# 检查是否还有 undefined symbol 错误
grep "ld.lld: error: undefined symbol" out/rk3568/build.log | grep MethodName
```

期望：无输出（0 个错误）。

## 高级技巧

### 1. 查找相似符号作为参考

```bash
# 查找同一类的其他导出符号
grep "ClassName::" build/libace.map
```

这样可以确保格式一致。

### 2. 从符号表反推格式

```bash
# 查看当前符号表
nm -D out/rk3568/arkui/ace_engine/libace.z.so | grep DialogType

# 解码符号名
nm -D out/rk3568/arkui/ace_engine/libace.z.so | grep DialogType | head -1 | c++filt
```

输出会显示完整的符号名称，参考格式添加到 libace.map。

### 3. 验证导出后其他模块能使用

```bash
# 检查使用该符号的模块
nm -D out/rk3568/arkui/libarkui_timepicker.z.so | grep MethodName

# 应该看到 'U' 标记（undefined，表示导入）
```

## 维护建议

### 1. 按字母顺序组织

libace.map 中的符号按字母顺序组织，便于查找：

```
global:
  extern "C++" {
    OHOS::Ace::NG::ButtonPattern::*;
    OHOS::Ace::NG::DialogTypeMargin::UpdateDialogMargin*;
    OHOS::Ace::NG::TextPattern::*;
  }
}
```

### 2. 按模块分组注释

```
global:
  extern "C++" {
    # Dialog module
    OHOS::Ace::NG::DialogTypeMargin::UpdateDialogMargin*;
    OHOS::Ace::NG::DialogView::CreateDialogNode*;

    # Text module
    OHOS::Ace::TextTheme::Builder::*;
    OHOS::Ace::TextStyle::*;

    # Button module
    OHOS::Ace::NG::ButtonPattern::*;
  }
}
```

### 3. 定期清理

检查是否有废弃的符号：
```bash
# 查找 libace.map 中有但代码中不存在的符号
for symbol in $(grep "OHOS::Ace::" build/libace.map | sed 's/\*;$//'); do
    if ! grep -r "$(echo $symbol | sed 's/::/::/g')" frameworks/ --include="*.h" > /dev/null; then
        echo "Potential obsolete symbol: $symbol"
    fi
done
```

## 相关案例

- **ACE_FORCE_EXPORT**: 参见 `symbol-export-ace-force-export.md`
- **未定义符号**: 参见 `undefined-symbol-missing-cpp.md`
