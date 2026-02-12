# 编译分析详细工作流程

本文档提供编译效率分析的详细工作流程和高级用法。

## 完整工作流程

### 1. 准备阶段

#### 1.1 确保项目已编译

在执行分析之前，确保目标产品已经完成至少一次完整编译：

```bash
cd <openharmony_root>
./build.sh --product-name rk3568 --build-target ace_engine --ccache
```

这将生成必要的 ninja 构建文件和编译数据库。

#### 1.2 定位源文件

确定要分析的源文件路径。源文件可以以以下方式指定：

- 相对于 ace_engine 根目录：`frameworks/core/components_ng/base/frame_node.cpp`
- 包含完整路径：`foundation/arkui/ace_engine/frameworks/core/components_ng/base/frame_node.cpp`
- 绝对路径：`<openharmony_root>/foundation/arkui/ace_engine/frameworks/core/components_ng/base/frame_node.cpp`

### 2. 执行分析

#### 2.1 基本分析

从 ace_engine 根目录执行主分析脚本：

```bash
cd <ace_engine_root>
./.claude/skills/compile-analysis/scripts/analyze_compile.sh frameworks/core/components_ng/base/frame_node.cpp
```

#### 2.2 指定产品名称

如果使用非默认产品（rk3568），指定产品名称：

```bash
./.claude/skills/compile-analysis/scripts/analyze_compile.sh \
  frameworks/core/components_ng/base/frame_node.cpp \
  rk3588
```

### 3. 输出解读

#### 3.1 步骤 1：获取编译命令

脚本首先提取源文件的编译命令：

```
========================================
步骤 1: 获取编译命令
========================================
使用out目录: <openharmony_root>/out/rk3568
查找源文件: foundation/arkui/ace_engine/frameworks/core/components_ng/base/frame_node.cpp
找到 5 个ninja文件
CXX模板: rule cxx command = ../../prebuilts/clang/ohos/linux-x86_64/llvm/bin/clang++...
找到编译规则在: out/rk3568/obj/arkui/ace_engine/frameworks/core/components_ng/base/ace_engine.ninja
输出文件: obj/arkui/ace_engine/frameworks/core/components_ng/base/frame_node.o
源文件路径: ../../foundation/arkui/ace_engine/frameworks/core/components_ng/base/frame_node.cpp
```

**关键信息**：
- ninja 文件位置
- 输出 .o 文件路径
- 源文件在构建系统中的路径

#### 3.2 步骤 2：执行编译

脚本执行增强编译命令，包含性能监控：

```
========================================
步骤 2: 执行编译并收集性能数据
========================================

编译时间: 0:12.45
峰值内存: 287456 KB
✓ 已生成: obj/arkui/ace_engine/frameworks/core/components_ng/base/frame_node.ii obj/arkui/ace_engine/frameworks/core/components_ng/base/frame_node.o
```

**性能指标**：
- **编译时间**: `0:12.45` 表示 12.45 秒
- **峰值内存**: `287456 KB` 表示约 287 MB

#### 3.3 步骤 3：依赖分析

脚本解析 .ii 文件，显示头文件依赖树：

```
========================================
步骤 4: 分析头文件依赖
========================================

头文件的依赖关系树：
└── foundation/arkui/ace_engine/frameworks/core/components_ng/base/frame_node.h
    ├── foundation/arkui/ace_engine/frameworks/core/components_ng/base/ui_node.h
    │   ├── foundation/arkui/ace_engine/frameworks/core/pipeline/base/element.h
    │   │   └── ...
    │   └── foundation/arkui/ace_engine/base/memory/ace_type.h
    └── foundation/arkui/ace_engine/frameworks/core/components_ng/property/property.h
        └── ...
```

**依赖树解读**：
- 每个缩进级别表示一个 `#include` 层级
- 多个子节点表示一个文件包含多个头文件
- 深度显示依赖链的长度

## 高级用法

### 批量分析多个文件

创建脚本分析多个文件：

```bash
#!/bin/bash
# batch_analyze.sh

files=(
  "frameworks/core/components_ng/base/frame_node.cpp"
  "frameworks/core/components_ng/base/ui_node.cpp"
  "frameworks/bridge/declarative_frontend/engine/js_engine.cpp"
)

for file in "${files[@]}"; do
  echo "========================================"
  echo "分析: $file"
  echo "========================================"
  ./.claude/skills/compile-analysis/scripts/analyze_compile.sh "$file" rk3568
  echo ""
done
```

### 提取最慢的文件

从构建日志中提取编译最慢的文件：

```bash
# 从 ninja log 中提取编译时间
grep "CXX" out/rk3568/.ninja_log | \
  awk '{print $1, $2}' | \
  sort -nr | \
  head -20
```

然后对这些文件执行详细分析。

### 比较优化前后

创建对比脚本：

```bash
#!/bin/bash
# compare_optimization.sh

SOURCE_FILE="$1"

# 优化前
echo "=== 优化前 ==="
./.claude/skills/compile-analysis/scripts/analyze_compile.sh "$SOURCE_FILE" > before.txt

# 应用优化...
echo "应用优化后..."

# 优化后
echo "=== 优化后 ==="
./.claude/skills/compile-analysis/scripts/analyze_compile.sh "$SOURCE_FILE" > after.txt

# 对比
echo "=== 对比结果 ==="
diff -u before.txt after.txt
```

### 仅生成编译命令（不执行）

如果只需要查看编译命令而不执行：

```bash
python3 ./.claude/skills/compile-analysis/scripts/get_compile_command.py \
  frameworks/core/components_ng/base/frame_node.cpp \
  out/rk3568
```

### 分析现有 .ii 文件

如果已有 .ii 文件，直接分析依赖：

```bash
python3 ./.claude/skills/compile-analysis/scripts/parse_ii.py \
  out/rk3568/obj/arkui/ace_engine/frameworks/core/components_ng/base/frame_node.ii
```

## 性能基准

### 典型编译时间参考

| 文件类型 | 典型时间 | 说明 |
|---------|---------|------|
| 小型文件 (<200 行) | 1-3 秒 | 简单工具类、辅助函数 |
| 中型文件 (200-1000 行) | 3-10 秒 | 常规组件实现 |
| 大型文件 (1000-3000 行) | 10-30 秒 | 复杂组件、模板密集 |
| 超大文件 (>3000 行) | >30 秒 | 需要优化，考虑拆分 |

### 典型内存使用参考

| 文件类型 | 典型内存 | 说明 |
|---------|---------|------|
| 小型文件 | 50-150 MB | 正常范围 |
| 中型文件 | 150-400 MB | 正常范围 |
| 大型文件 | 400-800 MB | 注意模板实例化 |
| 超大文件 | >800 MB | 可能需要优化 |

### 依赖复杂度参考

| 依赖树深度 | 复杂度 | 建议 |
|-----------|-------|------|
| 1-3 层 | 低 | 良好 |
| 4-6 层 | 中 | 可接受 |
| 7-10 层 | 高 | 考虑简化 |
| >10 层 | 很高 | 需要优化 |

## 优化建议

### 减少编译时间

1. **前置声明**：使用前置声明代替完整包含
   ```cpp
   // 不好
   #include "my_class.h"

   // 好
   class MyClass;
   ```

2. **头文件守卫**：确保使用 `#pragma once` 或 include guards

3. **减少模板使用**：模板会增加编译时间

4. **拆分大文件**：将大文件拆分为多个小文件

### 减少内存使用

1. **避免深层包含**：检查依赖树深度
2. **预编译头文件**：对稳定依赖使用 PCH
3. **减少模板实例化**：使用显式实例化

### 优化依赖关系

1. **消除循环依赖**：使用接口类解耦
2. **使用 PIMPL 模式**：隐藏实现细节
3. **避免包含在头文件中**：尽可能在 .cpp 中包含

## 故障排除

### 错误：找不到 .ii 文件

**可能原因**：
1. 编译命令执行失败
2. `-save-temps` 选项不支持
3. 文件路径不匹配

**解决方法**：
```bash
# 手动查找 .ii 文件
find out/rk3568/obj -name "*.ii" -type f

# 检查编译器版本
../../prebuilts/clang/ohos/linux-x86_64/llvm/bin/clang++ --version
```

### 错误：依赖树为空

**可能原因**：
1. 源文件没有包含 foundation/arkui/ 头文件
2. .ii 文件格式不正确

**解决方法**：
```bash
# 检查 .ii 文件内容
head -50 out/rk3568/obj/.../file.ii

# 查看 #include 指令
grep "^#" out/rk3568/obj/.../file.ii | grep "#include"
```

### 编译时间异常长

**可能原因**：
1. 头文件依赖过多
2. 模板实例化过多
3. 宏展开复杂

**诊断步骤**：
```bash
# 1. 查看依赖树宽度（子节点数量）
# 2. 检查是否包含大型的第三方库头文件
# 3. 查看编译器输出的行数
wc -l out/rk3568/obj/.../file.ii
```

## 自动化脚本

### 每日性能监控

创建 cron 任务，每天监控关键文件：

```bash
#!/bin/bash
# daily_compile_monitor.sh

DATE=$(date +%Y%m%d)
OUTPUT_DIR="/tmp/compile_analysis/$DATE"
mkdir -p "$OUTPUT_DIR"

cd <ace_engine_root>

files=(
  "frameworks/core/components_ng/base/frame_node.cpp"
  "frameworks/bridge/declarative_frontend/engine/js_engine.cpp"
)

for file in "${files[@]}"; do
  name=$(basename "$file" .cpp)
  ./.claude/skills/compile-analysis/scripts/analyze_compile.sh "$file" \
    > "$OUTPUT_DIR/${name}.txt" 2>&1
done

echo "分析完成：$OUTPUT_DIR"
```

### 性能回归检测

创建脚本检测性能退化：

```bash
#!/bin/bash
# detect_regression.sh

SOURCE_FILE="$1"
BASELINE_FILE="$2" # 之前的分析结果

# 当前分析
./.claude/skills/compile-analysis/scripts/analyze_compile.sh "$SOURCE_FILE" \
  | grep "编译时间" > current.txt

# 对比
if diff -q "$BASELINE_FILE" current.txt > /dev/null; then
  echo "✓ 性能稳定"
else
  echo "⚠ 检测到性能变化"
  echo "基线: $(cat $BASELINE_FILE)"
  echo "当前: $(cat current.txt)"
fi
```
