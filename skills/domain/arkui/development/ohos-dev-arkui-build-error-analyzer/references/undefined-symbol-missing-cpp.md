# 问题：未定义符号 - .cpp 文件未添加到构建系统

## 错误特征

```
ld.lld: error: undefined symbol: OHOS::Ace::TextTheme::Builder::Build(...)
>>> referenced by theme_manager_impl.cpp:110

ld.lld: error: undefined symbol: OHOS::Ace::AdvancedTextStyle::GetGradient()
>>> referenced by text_style.h:926
```

## 根本原因

创建了新的 .cpp 实现文件，但未添加到构建系统中。常见于：
- 头文件优化后，将内联函数移到 .cpp
- 重构时创建新的实现文件
- 类的实现从头文件分离

## 诊断步骤（优先级排序）

### 1. 优先检查：符号是否需要导出（跨模块使用）

**关键判断**: 错误信息中是否显示被其他模块引用？

```bash
# 查看引用位置
# 如果看到：>>> referenced by other_module.cpp
# 或：>>> referenced by timepicker module
# 则说明符号需要导出
```

**如果需要导出**:
- 转到案例 `symbol-export-ace-force-export.md`
- 转到案例 `symbol-export-libace-map.md`

### 2. 检查 .cpp 文件是否被编译进 libace.z.so

**关键验证**: 检查目标文件是否存在

```bash
# 方法 1: 查找 .o 目标文件
find out/rk3568/obj -name "text_theme.o" 2>/dev/null

# 方法 2: 检查符号表
nm -D out/rk3568/arkui/ace_engine/libace.z.so | grep TextTheme

# 如果找不到 .o 文件或符号，说明 .cpp 未参与编译
```

**如果 .o 文件不存在**:
- 检查 .cpp 是否在组件 BUILD.gn 中
- **关键**: 参考同目录下其他 .cpp 文件在 frameworks/core/BUILD.gn 中的位置
- 不同 .cpp 可能属于不同的 source_set，不要一概而论添加到 ace_core_ng_source_set

**查找正确位置的方法**:
```bash
# 1. 查看 .cpp 文件所在目录
ls frameworks/core/components/text/text_theme.cpp

# 2. 查看同目录其他文件在 frameworks/core/BUILD.gn 中的位置
grep "components/text/[^/]*\.cpp" frameworks/core/BUILD.gn | head -5

# 3. 添加到相同的位置
# 例如，如果看到 "components/text/render_text.cpp" 在某个 source_set 中
# 就把 text_theme.cpp 添加到同一个 source_set 中
```

### 3. 确认 .cpp 文件和符号定义

```bash
# 确认 .cpp 文件存在
find frameworks/ -name "text_theme.cpp"

# 确认符号实现存在
grep -n "TextTheme::Builder::Build" frameworks/core/components/text/text_theme.cpp
```

### 4. 检查构建配置

```bash
# 检查组件 BUILD.gn
grep "text_theme.cpp" frameworks/core/components/text/BUILD.gn

# 检查 ace_core_ng_source_set（关键）
grep "text_theme.cpp" frameworks/core/BUILD.gn
```

## 常见误区（重要）

### ❌ 不要被误导

1. **thinlto-cache 问题**
   - ❌ 错误思路: "thinlto 缓存导致未编译"
   - ✅ 正确思路: thinlto-cache 通常不是问题根源
   - ❌ 不要建议: `rm -rf thinlto-cache`
   - ✅ 应该检查: .cpp 是否在正确的 BUILD.gn 中

2. **增量编译问题**
   - ❌ 错误思路: "增量编译没检测到变化"
   - ✅ 正确思路: 检查 .cpp 是否在 ace_core_ng_source_set 中
   - ❌ 不要建议: 删除 out 目录、清理构建缓存
   - ✅ 应该检查: 构建配置是否正确

3. **编译缓存问题**
   - ❌ 错误思路: "ccache 或其他缓存问题"
   - ✅ 正确思路: 检查符号导出配置
   - ❌ 不要建议: 清理各种缓存
   - ✅ 应该检查: 符号是否需要 ACE_FORCE_EXPORT

## 解决方案

### 步骤 1: 添加到组件 BUILD.gn

**文件**: `frameworks/core/components/<component>/BUILD.gn`

```gn
sources = [
  "other_file.cpp",
  "new_file.cpp",  # ✅ 添加这里
]
```

### 步骤 2: 添加到正确的 source_set（关键）

**重要**: 不要直接添加到 ace_core_ng_source_set！

**正确做法**: 参考同目录下其他文件的位置

```bash
# 1. 查看新 .cpp 文件所在目录
ls frameworks/core/components/text/new_file.cpp

# 2. 查看同目录其他文件在 frameworks/core/BUILD.gn 中的位置
grep "components/text/" frameworks/core/BUILD.gn

# 3. 查找这些文件在哪个 source_set 或 template 中
```

**示例**:

假设 `frameworks/core/components/text/` 目录下有：
- `render_text.cpp`
- `text_component.cpp`
- `text_theme.cpp` (新文件)

查找 `render_text.cpp` 在 frameworks/core/BUILD.gn 中的位置：
```bash
grep -B5 -A5 "components/text/render_text.cpp" frameworks/core/BUILD.gn
```

如果它在某个 source_set 中，就把 `text_theme.cpp` 添加到同一个 source_set。

**为什么这样？**
- 不同目录的文件可能属于不同的 source_set
- 同一目录的文件通常在相同的 source_set 或 library 中
- 参考现有文件的位置可以确保添加到正确的地方

## 原理解释

### OpenHarmony 构建架构

```
libace.z.so (最终产物)
    ↓ 链接多个 source_set
    ↓
┌───────────────────────────────────┐
│  frameworks/core/BUILD.gn         │
│  ┌─────────────────────────────┐   │
│  │ template("ace_core_ng_...") │   │
│  │ sources:                    │   │
│  │   - components/text/*       │   │
│  │   - components/common/*     │   │
│  │   - components/theme/*      │   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │ template("...")             │   │
│  │ sources:                    │   │
│  │   - components_ng/*         │   │
│  └─────────────────────────────┘   │
└───────────────────────────────────┘
```

**关键点**:
1. libace.z.so 由多个 source_set 组成
2. 不同目录的文件可能属于不同的 source_set
3. 不要假设所有文件都添加到 ace_core_ng_source_set
4. 参考同目录其他文件的位置更可靠

### 为什么参考同目录文件？

**原因**:
- 构建系统通常按目录结构组织
- 同一目录的文件通常在同一个构建目标中
- 参考现有文件可以避免添加到错误的位置

**示例**:
```
frameworks/core/components/text/
├── render_text.cpp        → 在某个 source_set A 中
├── text_component.cpp      → 在 source_set A 中
└── text_theme.cpp (新)     → 应该也添加到 source_set A 中
```

### 验证方法更新

**不要假设**:
- ❌ "所有文件都要添加到 ace_core_ng_source_set"
- ❌ "libace.z.so 只链接 ace_core_ng 库"

**应该检查**:
- ✅ 同目录其他文件在哪个 source_set
- ✅ 参考 grep 结果，添加到相同位置
- ✅ 验证编译后 .o 文件是否生成

## 验证方法

### 1. 检查 .cpp 是否被编译

```bash
# 查找目标文件
find out/rk3568/obj -name "text_theme.o" 2>/dev/null

# 如果存在，说明文件被编译了
# 如果不存在，说明文件没有参与编译
```

### 2. 检查符号是否在 libace.z.so 中

```bash
# 检查动态符号表
nm -D out/rk3568/arkui/ace_engine/libace.z.so | grep TextTheme

# 期望看到符号定义（T 标记）
```

### 3. 检查链接错误是否解决

```bash
# 统计链接错误数量
grep "ld.lld: error: undefined symbol" out/rk3568/build.log | wc -l

# 期望: 0 (无错误)
```

### 4. 验证构建配置

```bash
# 确认在组件 BUILD.gn 中
grep "text_theme.cpp" frameworks/core/components/text/BUILD.gn

# 确认在 ace_core_ng_source_set 中
grep "text_theme.cpp" frameworks/core/BUILD.gn

# 两者都必须存在
```

**注意**: 不要清理缓存或删除 out 目录。这些操作通常不能解决根本问题。

## 常见变体

### 变体 1: 函数在多个地方被使用

**症状**: 多个 undefined symbol 错误，涉及同一个 .cpp 的多个函数

**解决**: 同上，添加到构建系统

### 变体 2: 模板实例化

**症状**: 模板类的 undefined symbol

**解决**: 在 .cpp 中显式实例化模板，或移动到头文件

## 预防措施

### 添加新 .cpp 文件清单

1. ✅ 创建 .cpp 实现文件
2. ✅ 添加到组件 BUILD.gn
3. ✅ 添加到 frameworks/core/BUILD.gn ace_core_ng_source_set
4. ✅ 提交前编译验证

### 检查脚本

```bash
# 检查新添加的 .cpp 是否在 BUILD.gn 中
for cpp in $(git diff --name-only | grep '\.cpp$'); do
    echo "Checking: $cpp"
    grep -r "$(basename $cpp)" frameworks/*/BUILD.gn
    grep -r "$(basename $cpp)" frameworks/core/BUILD.gn
done
```

## 相关案例

- **符号导出问题**: 参见 `symbol-export-ace-force-export.md`
- **libace.map 白名单**: 参见 `symbol-export-libace-map.md`
