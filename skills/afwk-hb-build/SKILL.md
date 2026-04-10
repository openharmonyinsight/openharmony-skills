---
name: hb-build
description: 智能编译 ability_runtime 组件，通过检测修改的文件自动确定编译目标。支持多目标一起编译、自动重试判断、智能错误分析。触发关键词："编译"、"构建"、"compile"、"build"、"make"、"make file"。
---

# hb-build - Ability Runtime 智能编译工具

自动检测修改的文件并智能编译 ability_runtime 组件，支持多目标编译和自动重试。

## 快速开始

### 自动检测并编译（推荐）

```bash
python3 scripts/helper.py
```

### 编译特定服务

```bash
# SO 名称（推荐）
python3 scripts/helper.py --target libupms      # UriPermissionManager
python3 scripts/helper.py --target abilityms    # AbilityManagerService
python3 scripts/helper.py --target appms        # AppManagerService

# 完整路径
python3 scripts/helper.py --target \
  //foundation/ability/ability_runtime/services/uripermmgr:libupms
```

### 编译多个服务

```bash
python3 scripts/helper.py --target libupms abilityms appms
```

### 整仓编译

```bash
python3 scripts/helper.py --target full
```

## 工作流程

```
1. 切换到项目根目录（包含 build.py）
2. 检测修改文件 → git status --short
3. 过滤无关文件 → 排除 .claude/, build/, out/, *.md 等
4. 推断编译目标 → 统计每个服务的修改文件数
5. 智能决策 →
   • 目标数量 > 5 → 使用整仓编译
   • 目标数量 > 1 → 一起编译多个目标
   • 目标数量 = 1 → 编译单个目标
6. 执行编译 → hb build ability_runtime -i --build-target <TARGET>
7. 处理结果 → 成功或失败（支持智能重试）
```

## 参数概览

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--target` | 编译目标（支持多个） | `auto` |
| `--type` | 编译类型（`-i` 功能代码 / `-t` 测试套） | `-i` |
| `--fast` | 启用快速编译（`--fast-rebuild`） | `false` |
| `--max-retries` | 最大重试次数 | `3` |
| `--auto-retry` | 启用自动重试模式 | `false` |

## 支持的编译目标

- `abilityms` - AbilityManagerService (services/abilitymgr)
- `appms` - AppManagerService (services/appmgr)
- `libupms` - UriPermissionManager (services/uripermmgr)
- `dataobsms` - DataObserverManager (services/dataobsmgr)
- `quickfixmgr` - QuickFix Manager (services/quickfixmgr)
- `auto` - 自动检测修改文件并推断编译目标
- `full` - 编译整个 ability_runtime 组件

## 自动忽略的文件

以下文件和目录不会被检测为需要编译的修改：

- `.claude/`, `.hvigor/`, `build/`, `out/`, `.git/`
- `services/dialog_ui/ams_system_dialog/.hvigor/`
- `local.properties`
- `*.md` 文档文件

## 使用要求

**必须满足的条件**：
- 必须在 ability_runtime Git 仓库中运行
- 项目根目录必须包含 build.py 文件
- hb 命令必须在 PATH 中可用

**已知的限制**：
- 全仓编译（`--target full`）耗时较长（10-30 分钟）
- 首次编译需要下载依赖包
- ccache 未安装时会禁用编译缓存

## 详细文档

- **API 参考**: [references/api.md](references/api.md) - 完整的 API、参数说明和技术细节
- **使用示例**: [references/examples.md](references/examples.md) - 常见使用场景和实际案例
- **工作流程**: [references/workflow.md](references/workflow.md) - 详细的工作流程和算法说明

## 核心脚本

- [scripts/helper.py](scripts/helper.py) - 编译脚本实现

## 外部资源

- [OpenHarmony 独立编译指南](https://gitee.com/csliutt-private/component_indep_build/blob/master/cases/case19.md)
