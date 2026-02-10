# 编译效率分析 Skill (Compile-Analysis)

用于分析 ACE Engine 项目中单个文件的编译效率，包括编译时间、资源开销和头文件依赖关系。

## 功能特性

- ✅ **编译时间分析** - 精确测量单个文件的编译耗时
- ✅ **资源开销监控** - 统计编译过程中的峰值内存使用
- ✅ **依赖关系可视化** - 以树形结构展示头文件依赖
- ✅ **性能优化建议** - 提供针对性的优化策略
- ✅ **独立编译脚本** - 生成可重复使用的增强编译脚本
  - 文件名格式：`compile_single_file_{file_name}.sh`
  - 保存位置：`out/{product}/`
  - 支持多次重复执行以进行性能对比测试

## ⚠️ 关键要求

1. **脚本执行位置**: `analyze_compile.sh` 可以在当前项目目录执行（会自动查找 OpenHarmony 根目录）
2. **编译命令执行位置**: 抽取好的编译命令**必须在** `out/{product}` 目录下执行（确保相对路径正确）
3. **基于实际运行**: 分析结果必须基于实际编译运行结果，不能进行推测或估算
4. **头文件依赖解析**: 必须通过自带脚本 `parse_ii.py` 解析对应的 `.ii` 文件，不要使用其他方式

## 快速开始

### 基本用法

```bash
# 从 ace_engine 根目录执行
./.claude/skills/compile-analysis/scripts/analyze_compile.sh <源文件路径> [产品名称]

# 示例
./.claude/skills/compile-analysis/scripts/analyze_compile.sh \
  frameworks/core/components_ng/base/frame_node.cpp rk3568
```

### 保存增强编译脚本

生成可重复使用的独立编译脚本（带性能监控）：

```bash
# 使用 --save-script 选项保存增强编译脚本
./.claude/skills/compile-analysis/scripts/analyze_compile.sh \
  frameworks/core/components_ng/base/frame_node.cpp rk3568 --save-script

# 脚本保存位置: out/rk3568/compile_single_file_frame_node.sh
# 后续可独立执行该脚本进行多次编译测试
```

**独立使用生成的脚本**：

```bash
# 进入 out 目录
cd out/rk3568

# 执行编译脚本
bash compile_single_file_frame_node.sh

# 输出:
#   - 编译时间
#   - 峰值内存
#   - 预编译文件 (.ii)
#   - 目标文件 (.o)
```

### 直接使用 Python 脚本

```bash
# 仅获取编译命令（不执行）
python3 ./.claude/skills/compile-analysis/scripts/get_compile_command.py \
  <源文件路径> [out目录]

# 保存原始编译命令
python3 ./.claude/skills/compile-analysis/scripts/get_compile_command.py \
  <源文件路径> --save

# 保存增强编译命令（带性能监控）
python3 ./.claude/skills/compile-analysis/scripts/get_compile_command.py \
  <源文件路径> --save-enhanced
```

### 与 Claude 对话

直接向 Claude 提出请求：

```
"分析 frame_node.cpp 的编译效率"
"查看 js_engine.cpp 的头文件依赖"
"检查这个文件的编译时间和内存开销"
"哪个文件编译最慢？帮我分析一下"
```

## 输出示例

```
========================================
步骤 2: 执行编译并收集性能数据
========================================

编译时间: 0:08.23
峰值内存: 234567 KB
✓ 已生成: obj/arkui/ace_engine/.../frame_node.ii

========================================
步骤 4: 分析头文件依赖
========================================

头文件的依赖关系树：
└── foundation/arkui/ace_engine/frameworks/core/components_ng/base/frame_node.h
    ├── foundation/arkui/ace_engine/frameworks/core/components_ng/base/ui_node.h
    │   ├── foundation/arkui/ace_engine/frameworks/core/pipeline/base/element.h
    │   └── foundation/arkui/ace_engine/base/memory/ace_type.h
    └── foundation/arkui/ace_engine/frameworks/core/components_ng/property/property.h
        └── foundation/arkui/ace_engine/frameworks/core/components_ng/property/property_base.h
```

## 目录结构

```
compile-analysis/
├── SKILL.md                              # Skill 主文件
├── README.md                             # 本文件
├── examples/
│   └── example-workflow.md               # 完整使用示例
├── references/
│   ├── workflow.md                       # 详细工作流程
│   └── optimization.md                   # 优化策略和模式
└── scripts/
    ├── analyze_compile.sh                # 主分析脚本
    ├── get_compile_command.py            # 提取编译命令
    └── parse_ii.py                       # 解析依赖关系
```

## 核心脚本

### analyze_compile.sh (主脚本)

整合所有分析功能的主入口脚本，执行完整的分析流程：

1. 提取源文件的编译命令
2. 生成增强编译命令（带性能监控）
3. 执行编译并收集时间/内存数据
4. 解析 .ii 文件提取依赖关系
5. 展示完整的分析结果

**用法**:
```bash
./.claude/skills/compile-analysis/scripts/analyze_compile.sh \
  <源文件路径> [产品名称]
```

### get_compile_command.py

从 ninja 构建系统中提取源文件的完整编译命令。

**功能**:
- 解析 toolchain.ninja 和子 ninja 文件
- 提取编译器标志、宏定义、包含路径
- 生成原始命令和增强命令两个版本
- 支持保存编译命令到独立脚本文件

**用法**:
```bash
# 查看编译命令
python3 ./.claude/skills/compile-analysis/scripts/get_compile_command.py \
  <源文件路径> [out目录]

# 保存原始编译命令
python3 ./.claude/skills/compile-analysis/scripts/get_compile_command.py \
  <源文件路径> --save

# 保存增强编译命令（带性能监控）
python3 ./.claude/skills/compile-analysis/scripts/get_compile_command.py \
  <源文件路径> --save-enhanced
```

**输出文件**:
- `--save`: 生成 `{file}_compile_command.sh`（原始命令，带 ccache）
- `--save-enhanced`: 生成 `compile_single_file_{file}.sh`（增强命令，带性能监控）

### parse_ii.py

解析预编译文件（.ii），提取并可视化头文件依赖关系。

**功能**:
- 解析 .ii 文件中的 `#include` 指令
- 构建依赖树结构
- 以树形图展示包含关系
- 支持保存依赖树到文件

**用法**:
```bash
# 显示依赖树（控制台输出）
python3 ./.claude/skills/compile-analysis/scripts/parse_ii.py <.ii文件路径>

# 解析并保存依赖树到文件
python3 ./.claude/skills/compile-analysis/scripts/parse_ii.py <.ii文件路径> --output <输出文件>
# 或使用 -o 简写
python3 ./.claude/skills/compile-analysis/scripts/parse_ii.py <.ii文件路径> -o <输出文件>
```

**输出文件命名**:
- 格式：`{file_name}_dependency_tree.txt`
- 位置：`out/{product}/`
- 示例：`out/rk3568/frame_node_dependency_tree.txt`

## 性能基准参考

### 编译时间

| 文件类型 | 典型时间 | 状态 |
|---------|---------|------|
| 小型文件 (<200 行) | 1-3 秒 | ✅ 良好 |
| 中型文件 (200-1000 行) | 3-10 秒 | ✅ 正常 |
| 大型文件 (1000-3000 行) | 10-30 秒 | ⚠️ 需关注 |
| 超大文件 (>3000 行) | >30 秒 | ❌ 需优化 |

### 内存使用

| 文件类型 | 典型内存 | 状态 |
|---------|---------|------|
| 小型文件 | 50-150 MB | ✅ 良好 |
| 中型文件 | 150-400 MB | ✅ 正常 |
| 大型文件 | 400-800 MB | ⚠️ 需关注 |
| 超大文件 | >800 MB | ❌ 需优化 |

### 依赖复杂度

| 依赖树深度 | 复杂度 | 建议 |
|-----------|-------|------|
| 1-3 层 | 低 | ✅ 良好 |
| 4-6 层 | 中 | ✅ 可接受 |
| 7-10 层 | 高 | ⚠️ 考虑简化 |
| >10 层 | 很高 | ❌ 需要优化 |

## 常见使用场景

### 1. 调查编译缓慢问题

当发现某个文件编译特别慢时：

```bash
./.claude/skills/compile-analysis/scripts/analyze_compile.sh \
  frameworks/core/components_ng/base/slow_file.cpp
```

查看输出中的：
- 编译时间是否超过 15 秒
- 峰值内存是否超过 500 MB
- 依赖树是否过深或过宽

### 2. 优化头文件依赖

减少不必要的重编译：

```bash
# 分析依赖树
python3 ./.claude/skills/compile-analysis/scripts/parse_ii.py \
  out/rk3568/obj/.../file.ii

# 查找：
# - 深层依赖链（>7 层）
# - 重复的包含路径
# - 不必要的直接包含
```

### 3. 测量优化效果

验证代码优化的实际效果：

```bash
# 优化前
./.claude/skills/compile-analysis/scripts/analyze_compile.sh file.cpp > before.txt

# 应用优化...

# 优化后
./.claude/skills/compile-analysis/scripts/analyze_compile.sh file.cpp > after.txt

# 对比
diff before.txt after.txt
```

### 4. 生成独立编译脚本

生成可重复使用的编译脚本，方便后续进行性能对比测试：

```bash
# 生成增强编译脚本
./.claude/skills/compile-analysis/scripts/analyze_compile.sh \
  frameworks/core/components_ng/base/slow_file.cpp rk3568 --save-script

# 脚本已保存到: out/rk3568/compile_single_file_slow_file.sh

# 后续可以独立使用该脚本，无需重新分析
cd out/rk3568

# 第一次编译（优化前）
bash compile_single_file_slow_file.sh
# 输出: 编译时间: 0:15.23, 峰值内存: 456789 KB

# 应用代码优化...

# 第二次编译（优化后）
bash compile_single_file_slow_file.sh
# 输出: 编译时间: 0:08.45, 峰值内存: 234567 KB

# 对比结果：时间减少约 45%，内存减少约 49%
```

**生成的脚本特性**：

1. **自动环境配置** - 自动切换到正确的执行目录
2. **性能监控** - 统计编译时间和峰值内存
3. **完整输出** - 生成 .ii 和 .o 文件
4. **可重复执行** - 支持多次运行进行性能对比
5. **错误处理** - 内置错误检测和提示

### 5. 单独编译单个文件

使用预生成的编译脚本对单个文件进行独立编译（不触发完整构建）：

```bash
# 用户请求："单独编译 frame_node.cpp"
# Claude 会执行以下流程：

# 步骤 1: 检查是否存在编译脚本
# 如果 out/rk3568/compile_single_file_frame_node.sh 存在 → 直接执行
# 如果不存在 → 先生成脚本

# 步骤 2: 执行编译脚本
cd out/rk3568
bash compile_single_file_frame_node.sh

# 输出:
# ========================================
# 增强编译（带性能监控）
# ========================================
# 源文件: frameworks/core/components_ng/base/frame_node.cpp
# 执行时间: 2025-01-28 10:30:00
# 工作目录: /path/to/out/rk3568
# ========================================
#
# 编译时间: 0:08.23
# 峰值内存: 234567 KB
# ✓ 已生成: obj/.../frame_node.ii obj/.../frame_node.o
#
# ========================================
# ✓ 编译完成！
# ========================================
```

**使用场景**：
- 快速验证单个文件的编译是否正常
- 测试代码修改后的编译结果
- 进行性能基准测试
- 调试编译问题

**触发方式**：
- "单独编译这个文件"
- "编译单个文件"
- "单编文件"
- "独立编译文件"
- "compile single file"

### 6. 分析头文件依赖关系

通过解析 `.ii` 文件来分析源文件的头文件依赖关系：

```bash
# 用户请求："分析 frame_node.cpp 的头文件依赖"
# Claude 会执行以下流程：

# 步骤 1: 检查是否存在 .ii 文件
# 如果 out/rk3568/obj/.../frame_node.ii 存在 → 直接解析
# 如果不存在 → 先通过编译脚本生成

# 步骤 2: 解析 .ii 文件并保存依赖树
python3 ./.claude/skills/compile-analysis/scripts/parse_ii.py \
  out/rk3568/obj/.../frame_node.ii \
  --output out/rk3568/frame_node_dependency_tree.txt

# 输出:
# 头文件的依赖关系树：
# └── foundation/arkui/ace_engine/frameworks/core/components_ng/base/frame_node.h
#     ├── foundation/arkui/ace_engine/frameworks/core/components_ng/base/ui_node.h
#     │   ├── foundation/arkui/ace_engine/frameworks/core/pipeline/base/element.h
#     │   │   ├── foundation/arkui/ace_engine/frameworks/core/pipeline/context.h
#     │   │   └── foundation/arkui/ace_engine/frameworks/core/components_ng/base/view_abstract.h
#     │   └── foundation/arkui/ace_engine/base/memory/ace_type.h
#     └── foundation/arkui/ace_engine/frameworks/core/components_ng/property/property.h
#         └── foundation/arkui/ace_engine/frameworks/core/components_ng/property/property_base.h
#
# ✓ 依赖树已保存到: out/rk3568/frame_node_dependency_tree.txt
```

**工作流程**：

```
用户请求 → 检查 .ii 文件 →
  ├─ 存在：直接用 parse_ii.py 解析并保存
  └─ 不存在：
      ├─ 检查编译脚本
      │   ├─ 存在：运行脚本生成 .ii
      │   └─ 不存在：先生成脚本，再运行生成 .ii
      └─ 解析 .ii 并保存依赖树
```

**触发方式**：
- "分析这个文件的头文件依赖"
- "头文件依赖关系"
- "这个文件依赖了多少头文件"
- "analyze header dependencies"

**输出文件**：
- 文件名：`{file_name}_dependency_tree.txt`
- 位置：`out/{product}/`
- 内容：完整的头文件依赖关系树

**使用场景**：
- 识别重编译的传播路径
- 发现循环依赖
- 优化头文件包含结构
- 减少不必要的依赖

### 7. 批量分析组件

分析整个组件的所有文件：

```bash
for file in frameworks/core/components_ng/base/*.cpp; do
  echo "分析: $file"
  ./.claude/skills/compile-analysis/scripts/analyze_compile.sh "$file" 2>&1 | \
    grep -E "编译时间|峰值内存"
done
```

## 优化建议

### 减少编译时间

1. **使用前置声明** - 代替完整包含头文件
2. **拆分大文件** - 将超过 3000 行的文件拆分
3. **减少模板使用** - 避免不必要的模板实例化
4. **使用预编译头** - 对稳定的依赖使用 PCH

### 减少内存使用

1. **减少依赖深度** - 避免超过 7 层的依赖链
2. **使用 PIMPL 模式** - 隐藏实现细节
3. **避免循环依赖** - 使用接口类解耦

### 优化依赖关系

1. **消除不必要的包含** - 只包含真正需要的头文件
2. **使用接口隔离** - 通过接口类减少耦合
3. **前置声明优先** - 指针和引用尽量使用前置声明

详细的优化策略请参考：`references/optimization.md`

## 故障排除

### 问题：找不到编译规则

**错误**: `错误: 找不到源文件的编译规则`

**原因**:
- 文件路径不正确
- 文件未被编译过
- out 目录不存在

**解决**:
```bash
# 1. 确保已编译过
./build.sh --product-name rk3568 --build-target ace_engine

# 2. 使用正确的路径格式
./.claude/skills/compile-analysis/scripts/analyze_compile.sh \
  frameworks/core/components_ng/base/frame_node.cpp
```

### 问题：找不到 .ii 文件

**错误**: `错误: 找不到生成的 .ii 文件`

**原因**:
- 增强编译命令执行失败
- 编译器不支持 `-save-temps` 选项

**解决**:
```bash
# 手动查找 .ii 文件
find out/rk3568/obj -name "*.ii" -type f

# 检查编译器版本
../../prebuilts/clang/ohos/linux-x86_64/llvm/bin/clang++ --version
```

### 问题：依赖树为空

**原因**: parse_ii.py 只显示包含 `foundation/arkui/` 的头文件

**这是正常行为**：系统头文件被有意排除

如需查看所有依赖，修改 parse_ii.py 中的 `target_prefix` 变量。

## 技术细节

### 工作原理

1. **提取编译命令** - 从 ninja 构建文件中提取完整的编译命令
2. **增强命令** - 修改命令以包含：
   - `-save-temps=obj` - 生成预编译文件
   - `/usr/bin/time` - 统计时间和内存
   - 去除 ccache - 获得真实性能数据
3. **执行编译** - 运行增强命令生成 .ii 和 .o 文件
4. **解析依赖** - 从 .ii 文件中提取 `#include` 指令
5. **构建树形** - 将依赖关系组织成树形结构

### 集成点

- **构建系统**: GN/Ninja
- **编译器**: Clang (OpenHarmony 工具链)
- **输出目录**: `out/<product>/obj/`
- **日志文件**: build.log, ninja log

## 参考文档

- **详细工作流程**: `references/workflow.md`
- **优化策略**: `references/optimization.md`
- **使用示例**: `examples/example-workflow.md`

## Skill 触发条件

当用户提出以下请求时，Claude 会自动加载此 Skill：

**中文触发词**：
- "分析编译效率"
- "分析编译时间"
- "查看头文件依赖"
- "保存编译命令"
- "提取编译命令"
- "生成编译脚本"
- "保存这个文件的编译命令"
- "单独编译这个文件"
- "编译单个文件"
- "单编文件"
- "独立编译文件"
- "分析这个文件的头文件依赖"
- "头文件依赖关系"
- "这个文件依赖了多少头文件"
- "分析文件编译开销"

**英文触发词**：
- "analyze compilation"
- "check header dependencies"
- "save compile command"
- "extract compile command"
- "generate compile script"
- "compile single file"
- "compile individual file"
- "standalone compile"
- "analyze header dependencies"
- "header dependency tree"
- "how many header files"

或者提到分析编译性能、构建时间、包含依赖、提取/保存编译命令、生成独立编译脚本、单独编译文件、分析头文件依赖关系等相关话题。

### 独立编译功能说明

当用户请求"单独编译这个文件"或类似请求时：

1. **优先使用现有脚本** - 检查是否存在 `out/{product}/compile_single_file_{name}.sh`
2. **按需生成脚本** - 如果脚本不存在，先使用 `--save-enhanced` 生成
3. **执行编译** - 运行脚本进行编译，显示性能数据

**重要约束**：
- ✅ 必须通过预生成的编译脚本来编译
- ✅ 如果脚本不存在，先生成再执行
- ❌ 不使用 ninja、make 等其他构建工具
- ❌ 不尝试手动构造编译命令

### 头文件依赖分析功能说明

当用户请求"分析这个文件的头文件依赖"或类似请求时：

1. **检查 .ii 文件** - 查找 `out/{product}/obj/` 目录下是否存在对应的 `.ii` 文件
2. **按需生成** - 如果 `.ii` 不存在，使用编译脚本生成
   - 优先使用已存在的编译脚本
   - 如果脚本也不存在，先生成脚本再执行
3. **解析并保存** - 使用 `parse_ii.py` 解析 `.ii` 文件
4. **保存结果** - 将依赖树保存到 `out/{product}/{file_name}_dependency_tree.txt`

**重要约束**：
- ✅ 必须通过解析 `.ii` 文件来分析依赖
- ✅ 必须使用编译脚本来生成 `.ii` 文件（如果不存在）
- ✅ 必须将依赖树保存到 `out/{product}/{file_name}_dependency_tree.txt`
- ❌ 不使用其他依赖分析工具（如 clang -E、gcc -M 等）
- ❌ 不尝试手动解析依赖关系

## 开发信息

- **位置**: `ace_engine/.claude/skills/compile-analysis/`
- **版本**: 0.1.0
- **依赖**: OpenHarmony 编译环境 (GN/Ninja, Clang)
- **支持产品**: rk3568, rk3588, ohos-sdk 等

## 更新日志

### v0.2.0 (2025-01-28)
- ✅ 新增：保存增强编译脚本功能（`--save-enhanced`）
- ✅ 新增：生成独立编译脚本 `compile_single_file_{file}.sh`
- ✅ 新增：单独编译单个文件功能（通过预生成的脚本）
- ✅ 新增：头文件依赖分析功能（解析 .ii 文件）
- ✅ 新增：parse_ii.py 支持 `--output` 参数保存依赖树
- ✅ 改进：依赖树自动保存到 `out/{product}/{file_name}_dependency_tree.txt`
- ✅ 改进：支持重复执行脚本进行性能对比测试
- ✅ 改进：analyze_compile.sh 添加 `--save-script` 选项
- ✅ 触发词：添加"单独编译"、"单编文件"、"头文件依赖关系"等触发词
- ✅ 文档：更新使用示例和场景说明
- ✅ 约束：依赖分析必须使用 .ii 文件，独立编译必须使用预生成脚本

### v0.1.0 (2025-01-25)
- ✅ 初始版本发布
- ✅ 支持编译时间分析
- ✅ 支持内存使用监控
- ✅ 支持依赖关系可视化
- ✅ 完整的文档和示例
- ✅ 优化策略指南

## 许可证

本 Skill 作为 OpenHarmony ACE Engine 项目的一部分，遵循项目许可证。
