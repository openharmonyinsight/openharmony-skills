# Linux 预编译清理指南

> **模块信息**
> - 层级：L2_Analysis
> - 优先级：按需加载（编译前必须执行）
> - 适用范围：Linux 环境下的 XTS 测试工程编译
> - 平台：Linux
> - 依赖：无
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

---

## 二、清理步骤

### 2.1 重要警告

> **⚠️ 重要警告**
>
> - ✅ **可以删除**：测试套目录下的 `.hvigor`、`build`、`entry/build`、`oh_modules`
> - ✅ **可以删除**：OH_ROOT 目录下的 `out` 目录
> - ❌ **不要删除**：OH_ROOT 目录下的 `build` 目录（系统编译环境，包含预编译库）
> - ❌ **不要删除**：OH_ROOT 目录下的 `test/xts/acts/build` 目录（系统编译环境，包含预编译库）
> - ❌ **不要删除**：任何源代码、配置文件
>
> **重要说明**：
> - `{OH_ROOT}/test/xts/acts` 为 xts 的 acts 仓路径，其下包含各个子系统的测试套集合
> - 例如 `{OH_ROOT}/test/xts/acts/testfwk` 下包含测试框架（testfwk）的测试套集合
> - `{OH_ROOT}/test/xts/acts/testfwk/uitest_errorcode` 是测试框架的测试套之一

### 2.2 步骤 1：删除测试套目录下的缓存目录

```bash
# 切换到测试套目录
cd /path/to/test/xts/acts/testfwk/<test_suite_name>

# 删除 .hvigor 目录（Hvigor 构建缓存）
rm -rf .hvigor

# 删除 build 目录（模块编译缓存，可以安全删除）
rm -rf build

# 删除 entry/build 目录（Entry 模块构建缓存，如果存在）
rm -rf entry/build

# 删除 oh_modules 目录（OHPM 依赖模块缓存，如果存在）
rm -rf oh_modules

# 删除 oh-package-lock.json5（OHPM 依赖锁文件，如果存在）
rm -f oh-package-lock.json5

# 删除 local.properties（本地配置文件，如果存在）
rm -f local.properties
```

**示例**：
```bash
# 对于 uitest_errorcode 测试套
cd /mnt/data/c00810129/oh_0130/test/xts/acts/testfwk/uitest_errorcode
rm -rf .hvigor build entry/build oh_modules
rm -f oh-package-lock.json5 local.properties
```

**路径说明**：
- ✅ **可以删除**：`/mnt/data/c00810129/oh_0130/test/xts/acts/testfwk/uitest_errorcode/build`
- ❌ **不要删除**：`/mnt/data/c00810129/oh_0130/test/xts/acts/build`

### 2.3 步骤 2：删除 OH_ROOT 目录下的 out 目录

```bash
# 切换到 OpenHarmony 根目录
cd /path/to/OH_ROOT

# 删除 out 目录（编译输出目录）
rm -rf out
```

**示例**：
```bash
# 对于 OpenHarmony 根目录为 /mnt/data/c00810129/oh_0130
cd /mnt/data/c00810129/oh_0130
rm -rf out
```

### 2.4 步骤 3：验证清理结果

```bash
# 1. 确认测试套缓存目录已删除
cd /path/to/test/xts/acts/testfwk/<test_suite_name>
ls -la .hvigor 2>/dev/null && echo "❌ .hvigor 仍然存在" || echo "✅ .hvigor 已删除"
ls -la build 2>/dev/null && echo "❌ build 仍然存在" || echo "✅ build 已删除"
ls -la entry/build 2>/dev/null && echo "❌ entry/build 仍然存在" || echo "✅ entry/build 已删除"
ls -la oh_modules 2>/dev/null && echo "❌ oh_modules 仍然存在" || echo "✅ oh_modules 已删除"

# 2. 确认配置文件已删除
ls -la oh-package-lock.json5 2>/dev/null && echo "❌ oh-package-lock.json5 仍然存在" || echo "✅ oh-package-lock.json5 已删除"
ls -la local.properties 2>/dev/null && echo "❌ local.properties 仍然存在" || echo "✅ local.properties 已删除"

# 3. 确认 OH_ROOT 下的 out 目录已删除
cd /path/to/OH_ROOT
ls -la out 2>/dev/null && echo "❌ out 仍然存在" || echo "✅ out 已删除"

# 4. 确认 OH_ROOT 下的 build 目录仍然存在（重要！）
ls -la test/xts/acts/build 2>/dev/null && echo "✅ test/xts/acts/build 仍然存在（正确）" || echo "❌ test/xts/acts/build 被删除（错误）"
```

---

## 三、清理命令汇总

### 3.1 一键清理命令

```bash
# 一键清理命令（替换路径为实际路径）
cd /path/to/test/xts/acts/testfwk/<test_suite_name> && rm -rf .hvigor build entry/build oh_modules && rm -f oh-package-lock.json5 local.properties
cd /path/to/OH_ROOT && rm -rf out
```

**完整示例**：
```bash
# uitest_errorcode 测试套清理示例
cd /mnt/data/c00810129/oh_0130/test/xts/acts/testfwk/uitest_errorcode
rm -rf .hvigor build entry/build oh_modules
rm -f oh-package-lock.json5 local.properties
cd /mnt/data/c00810129/oh_0130
rm -rf out
```

### 3.2 清理脚本（可选）

创建清理脚本 `cleanup.sh`：

```bash
#!/bin/bash

# 清理脚本示例
TEST_SUITE_PATH="/mnt/data/c00810129/oh_0130/test/xts/acts/testfwk/uitest_errorcode"
OH_ROOT="/mnt/data/c00810129/oh_0130"

echo "开始清理编译缓存..."

# 清理测试套目录
cd "$TEST_SUITE_PATH"
rm -rf .hvigor build entry/build oh_modules
rm -f oh-package-lock.json5 local.properties

# 清理 OH_ROOT 目录
cd "$OH_ROOT"
rm -rf out

echo "清理完成！"
```

使用方法：
```bash
chmod +x cleanup.sh
./cleanup.sh
```

---

## 四、清理执行时机

### 4.1 必须执行清理的情况

- ✅ 修改了测试代码（.ets 文件）后重新编译
- ✅ 修改了配置文件（BUILD.gn、module.json5 等）后重新编译
- ✅ 添加或删除了测试文件后重新编译
- ✅ HAP 包时间戳显示为旧时间（非最新编译时间）
- ✅ 编译成功但测试用例未更新
- ✅ 出现无法解释的编译错误

### 4.2 可以跳过清理的情况（不推荐）

- 仅修改注释或文档
- 确认没有影响编译产物的修改

---

## 五、清理失败排查

### 5.1 常见问题

| 问题 | 可能原因 | 解决方案 |
|------|---------|---------|
| 权限不足 | 文件被其他进程占用 | 关闭 IDE 或编辑器后重试 |
| 目录不存在 | 首次编译或已清理过 | 忽略错误，继续编译 |
| 路径错误 | 工作目录不正确 | 使用绝对路径或检查 `pwd` |

### 5.2 排查步骤

```bash
# 1. 检查当前工作目录
pwd

# 2. 检查目录权限
ls -la

# 3. 检查文件占用情况
lsof | grep <filename>

# 4. 强制删除（谨慎使用）
sudo rm -rf <directory>
```

---

## 六、清理检查清单

在编译之前，确保完成以下检查：

- [ ] 已删除测试套目录下的 `.hvigor` 目录
- [ ] 已删除测试套目录下的 `build` 目录
- [ ] 已删除测试套目录下的 `entry/build` 目录（如果存在）
- [ ] 已删除测试套目录下的 `oh_modules` 目录（如果存在）
- [ ] 已删除 `oh-package-lock.json5` 文件（如果存在）
- [ ] 已删除 `local.properties` 文件（如果存在）
- [ ] 已删除 OH_ROOT 目录下的 `out` 目录
- [ ] 已确认 `test/xts/acts/build` 目录仍然存在

---

## 七、参考资源

### 7.1 相关文档

- [Linux 编译工作流](./build_workflow_linux.md)
- [Linux 编译环境准备](./linux_compile_env_setup.md)
- [编译问题排查](./linux_compile_troubleshooting.md)

### 7.2 路径说明

| 路径 | 说明 |
|------|------|
| `{OH_ROOT}` | OpenHarmony 代码根目录 |
| `{OH_ROOT}/test/xts/acts` | XTS 的 acts 仓路径 |
| `{OH_ROOT}/test/xts/acts/testfwk` | 测试框架测试套集合 |
| `{OH_ROOT}/test/xts/acts/testfwk/<test_suite_name>` | 具体测试套目录 |
| `{OH_ROOT}/out` | 编译输出目录（可删除） |
| `{OH_ROOT}/test/xts/acts/build` | 系统编译环境（不要删除） |

---

## 八、版本历史

- **v1.0.0** (2026-02-06): 从 `build_workflow_linux.md` 中抽取预编译清理相关内容，创建独立模块
