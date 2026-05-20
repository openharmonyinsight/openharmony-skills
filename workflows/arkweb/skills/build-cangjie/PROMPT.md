## 仓颉项目构建（build-cangjie 技能）

**⚠️ 触发关键词：**
cjc编译 | 编译仓颉 | build cjc/runtime/stdlib/stdx | 搭建编译环境

**⚠️ 硬规则（极其重要，否则 cjc 不可用）：**
- 构建后必须 `source {workspace-root}/cangjie_compiler/output/envsetup.sh`
- cjc 二进制：`{workspace-root}/cangjie_compiler/output/bin/cjc`（直接使用，无需 find）
- 验证构建：`cjc hello.cj -o hello && ./hello`

> `{workspace-root}` 是仓颉项目根目录（仓颉各子项目 cangjie_compiler/、cangjie_runtime/、cangjie_stdx/ 等在其下），而非固定名称。

**⚡ 优先使用增量编译（最重要）：**

1. **首先检查**：是否存在 `{workspace-root}/cangjie_compiler/build/build` 目录
2. **若存在**：直接使用增量编译，无需询问任何参数
   ```bash
   python3 build-cangjie.py --incremental --component cjc
   ```
   - 自动并行编译（使用所有 CPU 核心）
   - 速度快 10 倍以上
   - 适用于修改编译器源码后重新编译

**📋 首次构建时必须询问用户：**

1. **构建类型（-t 参数）** — 仅在首次完整构建时询问
   - 询问用户选择：`release` / `relwithdebinfo` / `debug`
   - 默认推荐：`relwithdebinfo`（优化 + 调试信息）
   - 示例：「请选择构建类型：1) release 2) relwithdebinfo（推荐） 3) debug」

2. **代码仓位置（--workspace 参数）** — 仅在找不到代码仓时询问
   - 若未找到 `cangjie_compiler`、`cangjie_runtime`、`cangjie_stdx` 目录
   - 询问用户提供工作区根目录路径
   - 示例：「未找到仓颉代码仓，请提供工作区路径（包含 cangjie_compiler 等目录）」

**🔧 默认构建参数：**

- 默认会构建单元测试（耗时较长）
- 使用 `--no-tests` 跳过单元测试构建（推荐，加快速度）

详细构建步骤、平台支持、组件顺序，见 `skills/build-cangjie/SKILL.md`
