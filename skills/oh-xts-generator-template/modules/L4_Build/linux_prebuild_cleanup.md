# Linux 预编译清理指南

> **模块信息**
> - 层级：L4_Build
> - 优先级：按需加载（编译前必须执行）
> - 适用范围：Linux 环境下的 XTS 测试工程编译
> - 平台：Linux
> - 依赖：L1_Framework
> - 相关：`build_workflow_linux.md`（完整的编译工作流）

> **使用说明**
>
> **⚠️ 强制要求**：在执行编译命令之前，**必须**执行本指南中的清理步骤。
>
> 本指南可独立使用，用户要求清理编译缓存时加载此模块。

---

## 一、清理必要性

### 1.1 为什么必须清理

**⚠️ 重要提示**：在执行编译命令之前，**必须**执行以下清理步骤。

**原因**：
1. **避免缓存问题**：旧的 `.hvigor` 和 `build` 目录可能导致增量编译失败
2. **确保完整编译**：删除 `out` 目录确保所有修改的文件都被重新编译
3. **避免 HAP 包过期**：缓存可能导致生成的 HAP 包包含过时的测试代码

### 1.2 清理目标

| 目录 | 说明 | 操作 |
|------|------|------|
| `.hvigor` | Hvigor 构建缓存 | 删除 |
| `build/` | 模块编译缓存（测试套目录下） | 删除 |
| `entry/build/` | Entry 模块构建缓存 | 删除 |
| `oh_modules/` | OHPM 依赖模块缓存 | 删除 |
| `oh-package-lock.json5` | OHPM 依赖锁文件 | 删除 |
| `local.properties` | 本地配置文件 | 删除 |
| `out/` | 编译输出目录（OH_ROOT 下） | 删除 |
| `test/xts/acts/build/` | 系统编译环境 | **不要删除** |
| `build/`（OH_ROOT 下） | 系统编译环境 | **不要删除** |

### 1.3 清理操作安全注意事项（重要）

**⚠️ 关键警告**：清理操作必须谨慎执行，避免误删系统编译环境。

**安全清理步骤**：
1. **确认当前目录**：在执行清理命令前，必须先确认当前工作目录
   ```bash
   cd {OH_ROOT}/test/xts/acts/testfwk/uitestStatic
   pwd  # 确认在测试套目录
   ```

2. **使用显式路径删除**：删除命令必须使用显式路径（`./` 前缀或绝对路径）
   ```bash
   # ✅ 正确：使用显式相对路径
   rm -rf ./.hvigor ./build ./entry/build ./oh_modules
   rm -f ./oh-package-lock.json5 ./local.properties

   # ❌ 错误：不使用路径前缀（可能误删 OH_ROOT/build）
   rm -rf build
   ```

3. **分步清理**：将清理操作分为两步，避免一次性操作过多目录
   ```bash
   # 步骤1：清理测试套缓存
   cd {OH_ROOT}/test/xts/acts/testfwk/{test_suite}
   rm -rf ./.hvigor ./build ./entry/build ./oh_modules
   rm -f ./oh-package-lock.json5 ./local.properties

   # 步骤2：清理 OH_ROOT/out 目录（单独操作）
   cd {OH_ROOT}
   rm -rf out
   ```

4. **验证系统目录安全**：清理后必须验证 `OH_ROOT/build` 目录仍然存在
   ```bash
   cd {OH_ROOT}
   ls -ld build && echo "✅ OH_ROOT/build 安全" || echo "❌ OH_ROOT/build 被误删"
   ```

**常见错误及后果**：
| 错误操作 | 后果 | 恢复方法 |
|---------|------|---------|
| 在 OH_ROOT 目录执行 `rm -rf build` | 删除系统编译环境 | 需要从 git 恢复或重新同步代码 |
| 在测试套目录执行 `rm -rf build` 但未使用显式路径 | 可能误删 OH_ROOT/build | 需要从 git 恢复或重新同步代码 |
| 一次性清理多个目录 | 容易混淆目录路径 | 分步清理，每步验证 |

**建议**：
- 优先使用 `cleanup_group.sh` 脚本（如果存在）
- 手动清理时严格按照上述安全步骤执行
- 清理后务必验证系统目录完整性

---

## 二、清理方案

### 2.1 编译对象类型判断

| 编译对象类型 | 识别方式 | 示例 | 说明 |
|-------------|---------|------|------|
| **单个测试套** | BUILD.gn中存在 `ohos_js_app_suite()` 或 `ohos_js_app_static_suite()` | `ActsUiTestErrorCodeTest` | 编译单个测试套 |
| **Group** | BUILD.gn中存在 `group()` 定义 | `testfwk`, `arkui` | 编译整个子系统 |

### 2.2 统一清理方案：cleanup_group.sh

**使用内置清理脚本**（适用于所有场景）：
```bash
# 清理 testfwk group
./cleanup_group.sh /mnt/data/c00810129/oh_0130 testfwk

# 清理 arkui group
./cleanup_group.sh /mnt/data/c00810129/oh_0130 arkui

# 使用默认参数（清理 testfwk）
./cleanup_group.sh
```

### 2.3 cleanup_group.sh 脚本内容

```bash
#!/bin/bash

# Group 编译对象清理脚本
# 用法: ./cleanup_group.sh <OH_ROOT> <子系统名>

OH_ROOT="${1:-/mnt/data/c00810129/oh_0130}"
SUBSYSTEM="${2:-testfwk}"

if [ ! -d "$OH_ROOT/test/xts/acts/$SUBSYSTEM" ]; then
    echo "❌ 子系统目录不存在: $OH_ROOT/test/xts/acts/$SUBSYSTEM"
    exit 1
fi

echo "🧹 开始清理 Group: $SUBSYSTEM"
echo "📂 OH_ROOT: $OH_ROOT"
echo "📁 子系统: $SUBSYSTEM"

# 1. 解析 BUILD.gn 获取所有测试套路径
BUILD_GN_FILE="$OH_ROOT/test/xts/acts/$SUBSYSTEM/BUILD.gn"

if [ ! -f "$BUILD_GN_FILE" ]; then
    echo "❌ BUILD.gn 文件不存在: $BUILD_GN_FILE"
    exit 1
fi

echo "📋 解析 $BUILD_GN_FILE 中的测试套..."

# 提取 deps 中的测试套路径（简化版）
TEST_SUITES=$(grep -A 50 "group(\"$SUBSYSTEM\")" "$BUILD_GN_FILE" | \
              grep 'deps =' -A 30 | \
              grep '"' | \
              sed 's/.*"\([^"]*\)".*/\1/' | \
              grep -v '^$' | \
              cut -d':' -f1 | \
              sort | uniq)

# 过滤掉非目录的依赖
TEST_SUITES=$(echo "$TEST_SUITES" | grep -v "^[[:space:]]*#" | grep -v "^$")

if [ -z "$TEST_SUITES" ]; then
    echo "❌ 未找到测试套配置，请检查 BUILD.gn 文件格式"
    exit 1
fi

echo "🔍 发现以下测试套："
echo "$TEST_SUITES" | nl

# 2. 逐个清理测试套
cd "$OH_ROOT/test/xts/acts/$SUBSYSTEM"

CLEANED_COUNT=0
FAILED_COUNT=0

while IFS= read -r suite; do
    if [ -n "$suite" ] && [ -d "$suite" ]; then
        echo "🗂️  清理测试套: $suite"

        cd "$suite" 2>/dev/null

        if [ $? -eq 0 ]; then
            # 清理缓存目录
            echo "  🗑️  删除 .hvigor, build, entry/build, oh_modules..."
            rm -rf .hvigor build entry/build oh_modules 2>/dev/null

            # 清理配置文件
            echo "  🗑️  删除 oh-package-lock.json5, local.properties..."
            rm -f oh-package-lock.json5 local.properties 2>/dev/null

            echo "  ✅ 清理完成: $suite"
            CLEANED_COUNT=$((CLEANED_COUNT + 1))
        else
            echo "  ❌ 无法进入目录: $suite"
            FAILED_COUNT=$((FAILED_COUNT + 1))
        fi

        cd "$OH_ROOT/test/xts/acts/$SUBSYSTEM" 2>/dev/null
    else
        echo "⚠️  跳过不存在的测试套: $suite"
    fi
done <<< "$TEST_SUITES"

echo ""
echo "📊 清理统计："
echo "  ✅ 成功清理: $CLEANED_COUNT 个测试套"
echo "  ❌ 清理失败: $FAILED_COUNT 个测试套"

# 3. 清理 OH_ROOT 目录下的 out 目录
echo ""
echo "🗂️  清理 OH_ROOT 下的 out 目录..."
cd "$OH_ROOT"
rm -rf out 2>/dev/null

if [ $? -eq 0 ]; then
    echo "  ✅ out 目录已删除"
else
    echo "  ⚠️  out 目录不存在或删除失败"
fi

echo ""
echo "🎉 Group 清理完成！"
```

### 2.4 单个测试套清理（备选方案）

如果只需要清理单个测试套，可以直接手动执行：

**⚠️ 重要**：严格按照以下步骤执行，避免误删系统编译环境。

```bash
# 步骤1：切换到测试套目录并确认
cd {OH_ROOT}/test/xts/acts/testfwk/<test_suite_name>
pwd  # 必须确认当前目录

# 步骤2：删除缓存目录和文件（使用显式路径）
rm -rf ./.hvigor ./build ./entry/build ./oh_modules
rm -f ./oh-package-lock.json5 ./local.properties

# 步骤3：验证测试套清理完成
ls -la | grep -E "\.hvigor|build|oh_modules|local.properties|oh-package-lock" || echo "✅ 测试套缓存清理完成"

# 步骤4：清理 out 目录（单独操作）
cd /mnt/data/c00810129/oh_0130
rm -rf out

# 步骤5：验证系统目录安全
ls -ld build && echo "✅ OH_ROOT/build 安全" || echo "❌ OH_ROOT/build 被误删"
```

---

## 三、清理执行时机

### 3.1 必须执行清理的情况

- ✅ 修改了测试代码（.ets 文件）后重新编译
- ✅ 修改了配置文件（BUILD.gn、module.json5 等）后重新编译
- ✅ 添加或删除了测试文件后重新编译
- ✅ HAP 包时间戳显示为旧时间（非最新编译时间）
- ✅ 编译成功但测试用例未更新
- ✅ 出现无法解释的编译错误
- ✅ Group 编译时，任何测试套有修改都需要清理整个group

### 3.2 编译对象与清理策略

| 编译对象 | 清理策略 | 推荐方式 |
|---------|---------|---------|
| **单个测试套** | 仅清理该测试套 | 手动执行清理命令 |
| **Group** | 清理整个group下所有测试套 | `cleanup_group.sh OH_ROOT 子系统名` |
| **多个Group** | 分别清理每个group | 批量执行cleanup_group.sh |

---

## 四、清理失败排查

### 4.1 常见问题

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| 权限不足 | 文件被其他进程占用 | 关闭 IDE 或编辑器后重试 |
| 目录不存在 | 首次编译或已清理过 | 忽略错误，继续编译 |
| 路径错误 | 工作目录不正确 | 使用绝对路径或检查 `pwd` |
| Group 清理部分失败 | 部分测试套不存在或权限问题 | 检查 BUILD.gn 配置 |
| 脚本执行失败 | 脚本语法错误或权限不足 | 检查脚本权限，使用 bash -x 调试 |

### 4.2 排查步骤

```bash
# 1. 检查当前工作目录
pwd

# 2. 检查目录权限
ls -la

# 3. 检查 BUILD.gn 文件是否存在
ls -la /path/to/test/xts/acts/{子系统}/BUILD.gn

# 4. 使用调试模式运行清理脚本
bash -x cleanup_group.sh /path/to/OH_ROOT 子系统名

# 5. 强制删除（谨慎使用）
sudo rm -rf <directory>
```

---

## 五、清理检查清单

在编译之前，确保完成以下检查：

### 5.1 清理前检查
- [ ] 已确认编译对象（单个测试套或Group）
- [ ] 已检查子系统BUILD.gn文件存在且可读（Group清理）
- [ ] 已确认子系统目录存在且有访问权限（Group清理）
- [ ] 已准备好清理脚本（`cleanup_group.sh`）

### 5.2 清理后验证
- [ ] 已删除 OH_ROOT 目录下的 `out` 目录
- [ ] 已确认 `test/xts/acts/build` 目录仍然存在
- [ ] 已确认所有测试套的缓存目录已清理
- [ ] 已检查清理输出，确认无严重错误

---

## 六、参考资源

### 6.1 相关文档

- [Linux 编译工作流](./build_workflow_linux.md)
- [Linux 编译环境准备](./linux_compile_env_setup.md)
- [编译问题排查](./linux_compile_troubleshooting.md)

### 6.2 路径说明

| 路径 | 说明 |
|------|------|
| `{OH_ROOT}` | OpenHarmony 代码根目录 |
| `{OH_ROOT}/test/xts/acts` | XTS 的 acts 仓路径 |
| `{OH_ROOT}/test/xts/acts/testfwk` | 测试框架测试套集合 |
| `{OH_ROOT}/test/xts/acts/testfwk/<test_suite_name>` | 具体测试套目录 |
| `{OH_ROOT}/out` | 编译输出目录（可删除） |
| `{OH_ROOT}/test/xts/acts/build` | 系统编译环境（不要删除） |

---

## 七、版本历史

- **v2.1.0** (2026-02-11): **强化清理操作安全注意事项**
  - **核心更新**：
     * 新增 1.3 节：清理操作安全注意事项
     * 强调清理操作的潜在风险
     * 提供详细的安全清理步骤
  - **重要警告**：
     * 明确禁止在 OH_ROOT 目录执行 `rm -rf build`
     * 强制要求使用显式路径删除（`./` 前缀或绝对路径）
     * 强制要求分步清理，每步验证
  - **错误处理**：
     * 新增常见错误及后果对照表
     * 新增恢复方法说明
     * 提供验证系统目录安全的命令
  - **单个测试套清理更新**：
     * 更新清理步骤为5步严格流程
     * 每步都添加验证命令
     * 强调必须确认当前目录
  - **优化效果**：
     * 避免误删系统编译环境
     * 提高清理操作的安全性
     * 降低人为错误风险
   - 版本号升级至 v2.1.0

- **v2.0.0** (2026-02-10): **重大精简**：统一使用 cleanup_group.sh 清理方案
  - **移除内容**：
    - 删除 verify_group_cleanup.sh 脚本（功能重复）
    - 删除多种清理方案的复杂选择
    - 删除高级清理方案和带日志的脚本
    - 删除手动清理的复杂步骤描述
  - **保留和优化**：
    - 仅保留 cleanup_group.sh 作为统一清理方案
    - 保留单个测试套的手动清理作为备选方案
    - 简化文档结构，减少冗余内容
    - 保留核心的清理失败排查和检查清单
  - **用户体验提升**：
    - 提供单一、可靠的清理解决方案
    - 减少用户选择困惑
    - 提高执行效率和维护便利性

- **v1.1.0** (2026-02-10): 新增Group编译对象清理支持
- **v1.0.0** (2026-02-06): 从 `build_workflow_linux.md` 中抽取预编译清理相关内容，创建独立模块