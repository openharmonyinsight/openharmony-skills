---
name: harmonyos-doc-search-guide
description: 当 L1 RAG 查询失效或需要更权威的官方文档时，使用此 Skill 进行 L3 本地官方文档搜索。此 Skill
  直接搜索本地下载的官方文档，无需网络，包含最权威的官方信息和完整代码示例。适用于所有类型的问题，特别是UI开发、API参考、语法说明。
descriptionZH: 当 L1 RAG 查询失效或需要更权威的官方文档时，使用此 Skill 进行 L3 本地文档搜索。此 Skill
  直接搜索本地下载的官方文档，无需网络，包含最权威的官方信息和完整代码示例。适用于所有类型的问题，特别是UI开发、API参考、语法说明。
tags:
  - 鸿蒙
  - 文档搜索
  - 本地文档
  - HarmonyOS
---

# 鸿蒙应用 L3 本地文档搜索 Skill

## 目的

当 L1 失效时，直接搜索本地下载的官方文档。无需网络，包含最权威的官方信息和完整代码示例。

## 优势

- **无需网络**: 完全离线工作
- **权威性**: 包含最权威的官方信息
- **完整性**: 包含完整代码示例
- **免费**: 无需 API 调用成本

## 适用场景

所有类型的问题，特别是：
- UI开发
- API参考
- 语法说明
- 构建错误排查

## 🔍 快速定位策略

### 1. UI组件问题 (最常用)

- **Button组件**: 直接查看 `skills/utils/scripts/hm-docs/ui-dev/arkui-cj/cj-common-components-button.md`
- **List列表**: 直接查看 `skills/utils/scripts/hm-docs/ui-dev/arkui-cj/cj-layout-development-create-list.md`
- **Text文本**: 直接查看 `skills/utils/scripts/hm-docs/ui-dev/arkui-cj/cj-common-components-text-display.md`
- **布局问题**: 查看 `skills/utils/scripts/hm-docs/ui-dev/arkui-cj/cj-layout-development-*.md`

### 2. API参考查询

- **组件API**: 查看 `skills/utils/scripts/hm-docs/ui-dev/reference/arkui-cj/` 目录
- **标准库API**: 查看 `skills/utils/scripts/hm-docs/stdlib/std/` 目录

### 3. 语法和语言特性

- **语法问题**: 查看 `skills/utils/scripts/hm-docs/syntax/source_zh_cn/` 目录
- **高级功能**: 查看 `skills/utils/scripts/hm-docs/stdx/libs_stdx/` 目录

### 4. 构建错误排查

**当构建失败时，根据错误类型搜索解决方案**：
- **导入错误** (`import error`): 搜索 `skills/utils/scripts/hm-docs/ui-dev/arkui-cj/` 中的导入示例
- **未定义符号** (`undefined symbol`): 搜索 `skills/utils/scripts/hm-docs/ui-dev/reference/` 中的API定义
- **语法错误** (`syntax error`): 搜索 `skills/utils/scripts/hm-docs/syntax/source_zh_cn/` 中的语法说明
- **权限错误** (`permission denied`): 搜索 `module.json5` 和权限配置相关文档

### 📌 L1→L3 路径映射快捷方式

**利用 L1 输出的本地路径优先快速定位文档**：

L1 查询结果会返回格式化的知识片段，其中包含 `[本地路径]` 字段。

**L1→L3 配合原则**：
- **优先**: 使用 L1 返回的路径快速定位到可能相关的文档
- **补充**: 如果单个文档信息不足或需要更多上下文，扩展到正常的 L3 搜索
- **判断**: 当 L1 结果只有概念描述而缺少具体实现细节，或遇到边界情况时触发扩展搜索

**路径映射表**：
| RAG_Lite 源路径 | 映射后的本地路径 |
|----------------|-----------------|
| `zh-cn/application-dev/` | `skills/utils/scripts/hm-docs/ui-dev/` |
| `docs/dev-guide/` | `skills/utils/scripts/hm-docs/syntax/source_zh_cn/` |
| `std/doc/` | `skills/utils/scripts/hm-docs/stdlib/std/` |
| `doc/` | `skills/utils/scripts/hm-docs/stdx/libs_stdx/` |

## 🔍 搜索命令示例 (PowerShell)

```powershell
# 搜索Button相关内容
Select-String -Path ".claude\\skills\\utils\\scripts\\hm-docs\\ui-dev\\arkui-cj\\*.md" -Pattern "Button" -Context 1

# 搜索List相关内容
Get-ChildItem -Path ".claude\\skills\\utils\\scripts\\hm-docs\\ui-dev\\arkui-cj" -Filter "*.md" -Recurse | Select-String -Pattern "List" -Context 2

# 搜索Image图片组件
Select-String -Path ".claude\\skills\\utils\\scripts\\hm-docs\\ui-dev\\reference\\arkui-cj\\cj-image-video-image.md" -Pattern "导入|import|@r" -Context 1

# 搜索特定API (递归搜索所有子目录)
Get-ChildItem -Path ".claude\\skills\\utils\\scripts\\hm-docs\\ui-dev" -Filter "*.md" -Recurse | Select-String -Pattern "onClick" -Context 1

# 快速查找包含关键词的文件
Get-ChildItem -Path ".claude\\skills\\utils\\scripts\\hm-docs\\ui-dev\\arkui-cj" -Filter "*.md" -Recurse | Select-String -Pattern "Button" -List

# 构建错误排查示例
# 当出现导入错误时
Get-ChildItem -Path ".claude\\skills\\utils\\scripts\\hm-docs\\ui-dev" -Filter "*.md" -Recurse | Select-String -Pattern "import.*ArkUI" -Context 1

# 当出现权限错误时
Get-ChildItem -Path ".claude\\skills\\utils\\scripts\\hm-docs\\ui-dev" -Filter "*.md" -Recurse | Select-String -Pattern "permission|module.json5" -Context 2

# 搜索JSON处理相关
Select-String -Path ".claude\\skills\\utils\\scripts\\hm-docs\\stdx\\libs_stdx\\encoding\\json\\*.md" -Pattern "JsonValue|parse|stringify" -Context 1

# 搜索并发编程相关
Get-ChildItem -Path ".claude\\skills\\utils\\scripts\\hm-docs\\syntax\\source_zh_cn\\concurrency" -Filter "*.md" -Recurse | Select-String -Pattern "spawn|线程|并发" -Context 2
```

## 📚 本地文档源说明

本地 `skills/utils/scripts/hm-docs/` 文件夹包含从以下官方仓库下载的最新文档：

- **UI开发**: 来自 `openharmony-sig/docs_cangjie` 仓库 → `skills/utils/scripts/hm-docs/ui-dev/`
- **标准扩展库**: 来自 `Cangjie/cangjie_stdx` 仓库 → `skills/utils/scripts/hm-docs/stdx/`
- **语法特性**: 来自 `Cangjie/cangjie_docs` 仓库 → `skills/utils/scripts/hm-docs/syntax/`
- **标准库API**: 来自 `Cangjie/cangjie_runtime` 仓库 → `skills/utils/scripts/hm-docs/stdlib/`
- **工具构建**: 来自 `Cangjie/cangjie_docs` 仓库 → `skills/utils/scripts/hm-docs/tools/`

### 🔍 本地文档搜索优先级

直接搜索本地 `skills/utils/scripts/hm-docs/` 文件夹，按优先级执行：

#### 🥇 UI开发和组件问题 (最高优先级)

**搜索路径**: `skills/utils/scripts/hm-docs/ui-dev/arkui-cj/`

**常用组件快速定位**：
- **Button组件**: `skills/utils/scripts/hm-docs/ui-dev/arkui-cj/cj-common-components-button.md`
- **Text显示**: `skills/utils/scripts/hm-docs/ui-dev/arkui-cj/cj-common-components-text-display.md`
- **TextInput输入**: `skills/utils/scripts/hm-docs/ui-dev/arkui-cj/cj-common-components-text-input.md`
- **Image图片**: `skills/utils/scripts/hm-docs/ui-dev/reference/arkui-cj/cj-image-video-image.md`
- **List列表**: `skills/utils/scripts/hm-docs/ui-dev/arkui-cj/cj-layout-development-create-list.md`
- **Grid网格**: `skills/utils/scripts/hm-docs/ui-dev/arkui-cj/cj-layout-development-create-grid.md`

#### 🥈 标准扩展库 (高级功能)

**搜索路径**: `skills/utils/scripts/hm-docs/stdx/libs_stdx/`

#### 🥉 语法和语言特性

**搜索路径**: `skills/utils/scripts/hm-docs/syntax/source_zh_cn/`

#### 📚 标准库API

**搜索路径**: `skills/utils/scripts/hm-docs/stdlib/std/`

## 🛑 Phase 2 评估

- ✅ 在本地文档中找到相关信息 -> 基于本地官方文档编码
- ❌ 本地文档中无相关信息 -> **明确告知"该功能可能不支持或文档未包含"，请求用户提供相关知识或文档**

## ✅ L3 搜索最佳实践

### 1. 优先级顺序
UI 开发问题优先查 `ui-dev/`，避免在语法文档中浪费时间

### 2. 路径提示
L1 查询结果包含 `[本地路径]` 时优先使用该路径

### 3. 上下文扩展
如果单个文档信息不足，扩展搜索相关联的其他文档

### 4. 构建错误处理
- `import error` → 搜索导入示例
- `undefined symbol` → 搜索 API 定义
- `syntax error` → 搜索语法说明
- `permission error` → 搜索 module.json5

## 常见问题类型对应的搜索路径

| 问题类型 | 优先路径 | 备用路径 |
|---------|---------|---------|
| Button/Text/List 等组件 | `skills/utils/scripts/hm-docs/ui-dev/arkui-cj/cj-common-components-*.md` | `skills/utils/scripts/hm-docs/ui-dev/reference/arkui-cj/cj-*-*.md` |
| 布局问题 | `skills/utils/scripts/hm-docs/ui-dev/arkui-cj/cj-layout-development-*.md` | - |
| 事件处理 | `skills/utils/scripts/hm-docs/ui-dev/arkui-cj/cj-common-events-*.md` | - |
| HTTP/TLS | `skills/utils/scripts/hm-docs/stdx/libs_stdx/net/http/` | `skills/utils/scripts/hm-docs/stdx/libs_stdx/net/tls/` |
| JSON/Base64 | `skills/utils/scripts/hm-docs/stdx/libs_stdx/encoding/json/` | `skills/utils/scripts/hm-docs/stdx/libs_stdx/encoding/base64/` |
| 加密/摘要 | `skills/utils/scripts/hm-docs/stdx/libs_stdx/crypto/` | - |
| 数据库 | `skills/utils/scripts/hm-docs/stdlib/std/database_sql/` | - |
| 并发/线程 | `skills/utils/scripts/hm-docs/syntax/source_zh_cn/concurrency/` | - |
| 泛型/宏 | `skills/utils/scripts/hm-docs/syntax/source_zh_cn/generic/` 或 `/Macro/` | - |
| 构建错误 | `skills/utils/scripts/hm-docs/syntax/source_zh_cn/compile_and_build/` | `skills/utils/scripts/hm-docs/tools/source_zh_cn/` |

## 工作流程

1. **需求分析**（已完成）- 使用 `harmonyos-requirement-analysis` skill
2. **使用 skill-B skills**（已完成）- 先使用 `skills/` 中的仓颉语言 skills
3. **L1 查询**（已完成）- 如需进一步查询，使用 `harmonyos-vec-retriever-guide` skill
4. **L3 查询**（本 Skill）- 如需本地文档搜索，使用本 Skill
5. **构建** - 使用 `harmonyos-build` skill 进行项目构建
6. **迭代进化** - 使用 `harmonyos-evolution` skill 记录和解决问题
