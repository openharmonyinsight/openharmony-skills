# 编译分析示例工作流

本文档提供完整的使用示例，展示如何在实际开发中使用编译分析技能。

## 示例 1：基本文件分析

**场景**：分析 frame_node.cpp 的编译效率

### 步骤 1：导航到项目根目录

```bash
cd <ace_engine_root>
pwd
# 输出: <ace_engine_root>
```

### 步骤 2：执行分析

```bash
./.claude/skills/compile-analysis/scripts/analyze_compile.sh \
  frameworks/core/components_ng/base/frame_node.cpp
```

### 步骤 3：查看输出

```
========================================
编译效率分析工具
========================================

OpenHarmony 根目录: <openharmony_root>
ACE Engine 根目录: <ace_engine_root>
源文件: frameworks/core/components_ng/base/frame_node.cpp
产品名称: rk3568

========================================
步骤 1: 获取编译命令
========================================
使用out目录: <openharmony_root>/out/rk3568
查找源文件: foundation/arkui/ace_engine/frameworks/core/components_ng/base/frame_node.cpp
找到 5 个ninja文件
CXX模板: rule cxx command = ../../prebuilts/clang/ohos/linux-x86_64/llvm/bin/clang++ ...
找到编译规则在: out/rk3568/obj/arkui/ace_engine/frameworks/core/components_ng/base/ace_engine.ninja
输出文件: obj/arkui/ace_engine/frameworks/core/components_ng/base/frame_node.o

========================================
步骤 2: 执行编译并收集性能数据
========================================

编译时间: 0:08.23
峰值内存: 234567 KB
✓ 已生成: obj/arkui/ace_engine/frameworks/core/components_ng/base/frame_node.ii

========================================
步骤 4: 分析头文件依赖
========================================

头文件的依赖关系树：
└── foundation/arkui/ace_engine/frameworks/core/components_ng/base/frame_node.h
    ├── foundation/arkui/ace_engine/frameworks/core/components_ng/base/ui_node.h
    │   ├── foundation/arkui/ace_engine/frameworks/core/pipeline/base/element.h
    │   │   └── foundation/arkui/ace_engine/frameworks/core/pipeline/base/element_node.h
    │   └── foundation/arkui/ace_engine/base/memory/ace_type.h
    └── foundation/arkui/ace_engine/frameworks/core/components_ng/property/property.h
        └── foundation/arkui/ace_engine/frameworks/core/components_ng/property/property_base.h

========================================
分析完成！
========================================

性能数据总结:
  - 编译时间: 8.23 秒
  - 峰值内存: 234567 KB (约 229 MB)
  - 头文件依赖树: 3 层深度，5 个主要节点
```

### 步骤 4：解读结果

**编译时间**: 8.23 秒 - 中等速度，在可接受范围内
**峰值内存**: 229 MB - 正常范围
**依赖树**: 3 层深度 - 良好，依赖关系清晰

**结论**: 该文件编译效率良好，无需优化。

## 示例 2：识别性能问题

**场景**：分析编译缓慢的文件

### 步骤 1：分析问题文件

```bash
./.claude/skills/compile-analysis/scripts/analyze_compile.sh \
  frameworks/bridge/declarative_frontend/engine/js_engine.cpp
```

### 步骤 2：查看问题输出

```
编译时间: 0:34.56  ⚠️ 超过 30 秒！
峰值内存: 856432 KB  ⚠️ 超过 800 MB！

头文件的依赖关系树：
└── foundation/arkui/ace_engine/frameworks/bridge/declarative_frontend/engine/js_engine.h
    ├── foundation/arkui/ace_engine/frameworks/bridge/declarative_frontend/js_forward.h
    │   ├── base/bind.h
    │   │   ├── base/bind_internal.h
    │   │   │   ├── base/template_util.h
    │   │   │   │   └── ...
    │   │   │   └── base/callback_internal.h
    │   │   │       └── ...
    │   │   └── ...
    │   └── ...
    ├── foundation/arkui/ace_engine/third_party/jsengine/binding.h
    │   └── v8.h  ⚠️ 大型第三方库
    │       ├── v8config.h
    │       ├── v8-internal.h
    │       └── ...
    └── ... (共 42 个头文件，最深 11 层) ⚠️ 依赖树过深！
```

### 步骤 3：诊断问题

**问题 1**: 编译时间过长（34.56 秒）
- 可能原因：依赖树过深（11 层）
- 可能原因：包含大型第三方库（v8.h）

**问题 2**: 内存使用过高（856 MB）
- 可能原因：模板实例化过多
- 可能原因：深层依赖链

### 步骤 4：制定优化方案

**方案 1：使用前置声明**
```cpp
// js_engine.h
// 不好
#include "v8.h"
class JSEngine { v8::Isolate* isolate_; };

// 好
class v8::Isolate;  // 前置声明
class JSEngine { v8::Isolate* isolate_; };
```

**方案 2：使用 PIMPL 模式**
```cpp
// js_engine.h
class JSEngine {
public:
    JSEngine();
    ~JSEngine();
    void Initialize();

private:
    class Impl;
    Impl* impl_;
};

// js_engine.cpp
#include "v8.h"  // 只在实现中包含
class JSEngine::Impl {
    v8::Isolate* isolate_;
    // ... v8 相关实现
};
```

**方案 3：提取接口**
```cpp
// js_engine_interface.h
class JSEngineInterface {
public:
    virtual ~JSEngineInterface() = default;
    virtual void Execute(const std::string& script) = 0;
};

// js_engine_v8.h (实现细节)
#include "v8.h"
class JSEngineV8 : public JSEngineInterface {
    // v8 特定实现
};
```

## 示例 3：批量分析组件

**场景**：分析整个组件目录的编译效率

### 步骤 1：创建批量分析脚本

```bash
cat > batch_analyze.sh << 'EOF'
#!/bin/bash

COMPONENT_DIR="$1"
OUTPUT_DIR="compile_analysis_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"

echo "开始批量分析: $COMPONENT_DIR"
echo "输出目录: $OUTPUT_DIR"
echo ""

# 查找所有 .cpp 文件
find "$COMPONENT_DIR" -name "*.cpp" -type f | while read file; do
    # 转换为相对路径
    rel_path="${file#$PWD/}"
    filename=$(basename "$file" .cpp)

    echo "分析: $rel_path"

    # 执行分析
    ./.claude/skills/compile-analysis/scripts/analyze_compile.sh "$rel_path" \
        > "$OUTPUT_DIR/${filename}.txt" 2>&1

    # 提取关键指标
    grep -E "编译时间|峰值内存" "$OUTPUT_DIR/${filename}.txt" | \
        tee -a "$OUTPUT_DIR/summary.txt"

    echo ""
done

echo ""
echo "批量分析完成！"
echo "摘要文件: $OUTPUT_DIR/summary.txt"
EOF

chmod +x batch_analyze.sh
```

### 步骤 2：执行批量分析

```bash
./batch_analyze.sh frameworks/core/components_ng/base
```

### 步骤 3：查看摘要

```bash
cat compile_analysis_*/summary.txt | sort -t: -k2 -nr
```

输出示例：

```
ui_node.cpp: 编译时间: 0:18.45
ui_node.cpp: 峰值内存: 456789 KB

frame_node.cpp: 编译时间: 0:08.23
frame_node.cpp: 峰值内存: 234567 KB

view_abstract.cpp: 编译时间: 0:05.12
view_abstract.cpp: 峰值内存: 156789 KB
```

### 步骤 4：识别热点

```bash
# 找出最慢的 10 个文件
cat compile_analysis_*/summary.txt | \
    grep "编译时间" | \
    sort -t: -k2 -nr | \
    head -10
```

## 示例 4：优化验证

**场景**：验证优化的效果

### 步骤 1：建立基线

```bash
# 优化前分析
./.claude/skills/compile-analysis/scripts/analyze_compile.sh \
  frameworks/bridge/declarative_frontend/engine/js_engine.cpp \
  > baseline.txt

grep -E "编译时间|峰值内存" baseline.txt
```

输出：
```
编译时间: 0:34.56
峰值内存: 856432 KB
```

### 步骤 2：应用优化

（进行代码优化...）

### 步骤 3：测量改进

```bash
# 优化后分析
./.claude/skills/compile-analysis/scripts/analyze_compile.sh \
  frameworks/bridge/declarative_frontend/engine/js_engine.cpp \
  > optimized.txt

grep -E "编译时间|峰值内存" optimized.txt
```

输出：
```
编译时间: 0:15.23  ✓ 改进 56%！
峰值内存: 423456 KB  ✓ 改进 51%！
```

### 步骤 4：详细对比

```bash
diff -u baseline.txt optimized.txt
```

或者创建对比脚本：

```bash
cat > compare.sh << 'EOF'
#!/bin/bash

echo "=== 编译时间对比 ==="
baseline_time=$(grep "编译时间" baseline.txt | awk '{print $2}')
optimized_time=$(grep "编译时间" optimized.txt | awk '{print $2}')
echo "基线: $baseline_time"
echo "优化后: $optimized_time"

echo ""
echo "=== 峰值内存对比 ==="
baseline_mem=$(grep "峰值内存" baseline.txt | awk '{print $2}')
optimized_mem=$(grep "峰值内存" optimized.txt | awk '{print $2}')
echo "基线: $baseline_mem"
echo "优化后: $optimized_mem"

echo ""
echo "=== 依赖树对比 ==="
echo "基线依赖数:"
grep -c "^├──\|^└──" baseline.txt || echo 0
echo "优化后依赖数:"
grep -c "^├──\|^└──" optimized.txt || echo 0
EOF

chmod +x compare.sh
./compare.sh
```

## 示例 5：持续监控

**场景**：在开发过程中持续监控编译性能

### 步骤 1：创建监控脚本

```bash
cat > monitor_compile.sh << 'EOF'
#!/bin/bash

FILE="$1"
HISTORY_DIR="compile_history"
mkdir -p "$HISTORY_DIR"

DATE=$(date +%Y%m%d_%H%M%S)
OUTPUT="$HISTORY_DIR/${DATE}_$(basename "$FILE" .cpp).txt"

echo "监控: $FILE"
echo "输出: $OUTPUT"

./.claude/skills/compile-analysis/scripts/analyze_compile.sh "$FILE" > "$OUTPUT"

# 提取关键指标
{
    echo "=== $(date) ==="
    grep -E "编译时间|峰值内存" "$OUTPUT"
} | tee -a "$HISTORY_DIR/timeline.txt"

echo ""
echo "历史趋势:"
tail -10 "$HISTORY_DIR/timeline.txt"
EOF

chmod +x monitor_compile.sh
```

### 步骤 2：定期监控

```bash
# 每次修改后运行
./monitor_compile.sh frameworks/core/components_ng/base/frame_node.cpp
```

### 步骤 3：查看趋势

```bash
cat compile_history/timeline.txt
```

输出示例：

```
=== 2025-01-20 10:30 ===
编译时间: 0:08.23
峰值内存: 234567 KB

=== 2025-01-21 14:15 ===
编译时间: 0:09.12  ← 性能下降！
峰值内存: 245678 KB

=== 2025-01-22 09:45 ===
编译时间: 0:07.45  ← 优化后
峰值内存: 223456 KB
```

## 示例 6：与构建系统集成

**场景**：在 CI/CD 中集成编译分析

### 步骤 1：创建 CI 脚本

```bash
cat > ci_compile_check.sh << 'EOF'
#!/bin/bash

set -e

# 配置
MAX_COMPILE_TIME=30  # 最大允许编译时间（秒）
MAX_MEMORY=800000    # 最大允许内存（KB）
FILE="$1"

echo "CI 编译效率检查: $FILE"

# 执行分析
OUTPUT=$(./.claude/skills/compile-analysis/scripts/analyze_compile.sh "$FILE" 2>&1)

# 提取指标
COMPILE_TIME=$(echo "$OUTPUT" | grep "编译时间" | awk -F: '{print $2}' | awk '{print $1}')
MEMORY_KB=$(echo "$OUTPUT" | grep "峰值内存" | awk '{print $2}')

# 转换时间为秒
MINUTES=$(echo "$COMPILE_TIME" | cut -d: -f1)
SECONDS=$(echo "$COMPILE_TIME" | cut -d: -f2)
TOTAL_SECONDS=$((MINUTES * 60 + SECONDS))

# 检查阈值
if (( TOTAL_SECONDS > MAX_COMPILE_TIME )); then
    echo "❌ CI 失败: 编译时间超过阈值 ($TOTAL_SECONDS > $MAX_COMPILE_TIME 秒)"
    exit 1
fi

if (( MEMORY_KB > MAX_MEMORY )); then
    echo "❌ CI 失败: 内存使用超过阈值 ($MEMORY_KB > $MAX_MEMORY KB)"
    exit 1
fi

echo "✓ CI 通过: 编译效率检查"
echo "  编译时间: $TOTAL_SECONDS 秒 (阈值: $MAX_COMPILE_TIME)"
echo "  内存使用: $MEMORY_KB KB (阈值: $MAX_MEMORY)"
EOF

chmod +x ci_compile_check.sh
```

### 步骤 2：在 CI 中使用

```yaml
# .github/workflows/compile-check.yml 示例
name: Compile Efficiency Check

on: [pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check Compile Efficiency
        run: |
          ./ci_compile_check.sh \
            frameworks/core/components_ng/base/frame_node.cpp
```

## 常见使用模式总结

### 快速检查

```bash
# 快速检查单个文件
./.claude/skills/compile-analysis/scripts/analyze_compile.sh <file>
```

### 深度分析

```bash
# 深度分析依赖树
python3 ./.claude/skills/compile-analysis/scripts/parse_ii.py <file.ii>
```

### 批量处理

```bash
# 批量分析目录
./batch_analyze.sh <directory>
```

### 对比验证

```bash
# 对比优化前后
./compare.sh baseline.txt optimized.txt
```

### 持续监控

```bash
# 监控编译性能
./monitor_compile.sh <file>
```
