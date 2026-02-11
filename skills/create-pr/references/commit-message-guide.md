# Commit Message Guide

Commit 信息编写指南，遵循通用的提交信息规范。

## Commit Message 结构

```
<type>: <subject>

<body>

<footer>
```

## Type (类型)

| Type | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | feat: add sheet selection support |
| `fix` | Bug 修复 | fix: resolve memory leak in MenuPattern |
| `refactor` | 重构（不改变功能） | refactor: extract common layout logic |
| `perf` | 性能优化 | perf: optimize Grid layout algorithm |
| `test` | 测试相关 | test: add unit tests for sheet selection |
| `docs` | 文档更新 | docs: update Grid component API docs |
| `style` | 代码风格（格式化等） | style: fix code formatting issues |
| `chore` | 构建过程、工具链 | chore: update build configuration |

## Subject (主题)

- **不超过 50 个字符**
- 使用祈使句（"add" 而非 "added" 或 "adds"）
- 首字母小写
- 不要以句号结尾
- 简洁描述做了什么和为什么

**好的示例**：
```
feat: add sheet selection support to Grid component
fix: resolve crash in MenuPattern initialization
refactor: extract validation logic to helper function
```

**不好的示例**：
```
Added sheet selection feature  ❌ (首字母大写)
Adding new feature for Grid  ❌ (使用进行时)
Add sheet selection support.  ❌ (以句号结尾)
fix some bugs  ❌ (不够具体)
```

## Body (正文)

- **说明 what 和 why**，而非 how
- **每行不超过 72 个字符**
- 解释修改的动机和上下文
- 对比与之前的行为差异
- 列出任何破坏性更改

**示例**：
```
feat: add sheet selection support to Grid component

Implement sheet-based selection mode allowing users to select
entire sheets of items at once, improving UX for grid layouts
with spatial grouping.

The new API includes:
- SelectSheet(sheetIndex): Select all items in a sheet
- DeselectSheet(sheetIndex): Deselect all items in a sheet
- IsSheetSelected(sheetIndex): Query sheet selection state

This change is backward compatible - existing item-level
selection APIs continue to work as before.
```

## Footer (脚注)

### 关联 Issue

使用 `Fixes` 或 `Closes` 自动关闭 Issue：

```
Fixes #12345
Closes #67890
```

### Breaking Changes

标注破坏性更改：

```
BREAKING CHANGE: Grid selection API now requires explicit
initialization of SelectionModel before use.
```

### Co-Authored-By

多作者协作时使用：

```
Co-Authored-By: Name <email@example.com>
```

## 完整示例

### 新功能
```
feat: add sheet selection support to Grid component

Implement sheet-based selection mode allowing users to select
entire sheets of items at once. This improves UX for grid
layouts with spatial grouping of items.

New API methods:
- SelectSheet(int32_t sheetIndex): Select all items in sheet
- DeselectSheet(int32_t sheetIndex): Deselect all items
- IsSheetSelected(int32_t sheetIndex): Query selection state

Implementation details:
- Added selectedSheets_ member to track selected sheet indices
- Integrated with existing selection event system
- Maintains backward compatibility with item-level selection

Fixes #12345
```

### Bug 修复
```
fix: resolve memory leak in MenuPattern cleanup

MenuPattern failed to release submenu references in
OnDetachFromTree, causing accumulated memory leaks in
applications with dynamic menu creation/destruction.

Root cause: submenu_ smart pointer was not being reset
after menu destruction.

Fix: Explicitly reset submenu_ in OnDetachFromTree
and add null check before submenu operations.

Memory profiling shows 100% of leaked submenu references
now properly released.
```

### 重构
```
refactor: extract common layout logic from Grid and List

Grid and List components had duplicated layout calculation
logic for measuring children with flex properties.

Extracted common logic to FlexLayoutAlgorithm base class:
- CalculateChildConstraints()
- MeasureChildrenWithFlex()
- DistributeRemainingSpace()

Benefits:
- Reduced code duplication by ~150 lines
- Single source of truth for flex layout logic
- Easier to maintain and fix bugs
- Improved testability

No functional changes - layout behavior remains identical.
```

### 性能优化
```
perf: optimize Grid layout calculation for large datasets

Grid layout performance degraded with O(n²) complexity
when measuring items with span properties.

Optimized by:
- Caching span calculations per row/column
- Using hash map instead of linear search for span lookups
- Pre-calculating layout constraints before measurement

Performance improvements:
- 1000-item grid: 120ms → 15ms (8x faster)
- 10000-item grid: 12s → 180ms (67x faster)
- Memory usage unchanged
```

### 测试
```
test: add comprehensive unit tests for sheet selection

Add GridPatternSheetSelectionTest suite covering:
- SelectSheet with valid/invalid indices
- DeselectSheet functionality
- IsSheetSelected query operations
- Edge cases (empty grid, single sheet, boundary indices)
- Selection state persistence across operations

Test coverage increased from 45% to 82% for sheet
selection related code.

All tests pass: 89/89
```

## 常见错误

### ❌ 不好的示例

**太模糊**：
```
fix: fix some bugs
```
**改进为**：
```
fix: resolve crash in MenuPattern when submenu is null
```

**描述实现而非目的**：
```
feat: add selectedSheets_ member variable
```
**改进为**：
```
feat: add sheet selection support to Grid component
```

**混合多个不相关的更改**：
```
feat: add Grid sheet selection and fix Menu crash
```
**改进为**：拆分为两个独立的 commit

**Subject 太长**：
```
feat: add comprehensive sheet selection support with full API coverage including selection state management
```
**改进为**：
```
feat: add sheet selection support to Grid component
```

（详细内容放在 body 中）

## Commit Message 检查清单

提交前检查：

- [ ] Type 选择正确（feat/fix/refactor 等）
- [ ] Subject 不超过 50 字符
- [ ] Subject 使用祈使句，首字母小写
- [ ] Subject 不以句号结尾
- [ ] Body 解释动机和对比，而非实现细节
- [ ] 关联相关 Issue（Fixes #xxx）
- [ ] 添加 Co-Authored-By 脚注
- [ ] 没有 trailing whitespace
- [ ] 没有混合多个不相关的更改

## 查看项目实际风格

在提交前，查看项目的实际 commit 风格：

```bash
# 查看最近的 commit
git log --oneline -20

# 查看完整的 commit message
git log -4 --format=fuller

# 搜索特定类型的 commit
git log --grep="feat:" --oneline
git log --grep="fix:" --oneline
```

## 自动生成 Commit Message

使用 create-pr skill 自动生成：

```bash
python scripts/create-pr/repo_api.py analyze
```

脚本将：
1. 分析 `git diff`
2. 识别修改类型和范围
3. 生成符合项目风格的 commit message
4. 包含 Co-Authored-By 脚注（如果配置）
