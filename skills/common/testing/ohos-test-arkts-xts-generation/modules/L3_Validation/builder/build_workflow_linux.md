# Linux 编译工作流

> **模块信息**
> - 层级：L3_Validation
> - 适用范围：Linux 环境下 XTS 测试工程编译
> - 相关：[Windows 编译工作流](./build_workflow_windows.md)

> **⚠️ Linux 编译铁律**
>
> - ✅ **必须使用** `./test/xts/acts/build.sh`
> - ❌ **禁止使用** `hvigorw`（Windows 专用）
> - 编译前**必须**从 BUILD.gn 提取正确的测试套名称
> - 编译前**必须**执行预编译清理

---

## 一、快速参考

### 1.1 编译命令

```bash
# 动态测试套（默认）
cd {OH_ROOT}
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite={测试套名称}

# 静态测试套
cd {OH_ROOT}
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite={测试套名称} xts_suitetype=hap_static
```

### 1.2 异步编译（推荐）

OpenHarmony 编译通常需要 10-30 分钟，异步编译不阻塞主流程。

```bash
# 启动异步编译
{skill_root}/scripts/async_build.sh {OH_ROOT} {测试套名称} rk3568 start

# 静态测试套
{skill_root}/scripts/async_build.sh {OH_ROOT} {测试套名称} rk3568 start xts_suitetype=hap_static

# 查看状态
{skill_root}/scripts/async_build.sh {OH_ROOT} {测试套名称} rk3568 status

# 等待完成
{skill_root}/scripts/async_build.sh {OH_ROOT} {测试套名称} rk3568 wait

# 查看错误
{skill_root}/scripts/async_build.sh {OH_ROOT} {测试套名称} rk3568 errors
```

异步编译临时文件位于 `/tmp/oh_xts_build/`：
```
/tmp/oh_xts_build/
├── {测试套名称}.log      # 编译日志
├── {测试套名称}.pid      # 进程 PID
├── {测试套名称}.status   # 编译状态（RUNNING/SUCCESS/FAILED）
└── {测试套名称}.error    # 错误信息
```

### 1.3 参数说明

| 参数 | 说明 | 必选 | 值 |
|------|------|------|-----|
| `product_name` | 产品名称 | 必选 | rk3568（**固定值**） |
| `system_size` | 系统规格 | 必选 | standard（**固定值**） |
| `suite` | 测试套名称 | 必选 | 从 BUILD.gn 提取 |
| `xts_suitetype` | 测试套类型 | 可选 | `hap_static`（静态时必选） |

### 1.4 编译输出

```
out/{product_name}/suites/acts/acts/testcases/
├── {测试套名称}/
│   └── {测试套名称}.hap
```

---

## 二、测试套名称提取

编译前**必须**从 BUILD.gn 提取正确的测试套名称作为 `suite` 参数值。

### 2.1 BUILD.gn 测试套类型

| 类型 | BUILD.gn 模板 | test_hap | 编译参数 |
|------|--------------|----------|---------|
| 动态测试套 | `ohos_js_app_suite("Name")` | `test_hap = true` | 默认 |
| 静态测试套 | `ohos_js_app_static_suite("Name")` | 不设置 | `xts_suitetype=hap_static` |

> **⚠️ 模板函数必须与 ETS 版本匹配**：1.2 工程必须使用 `ohos_js_app_static_suite`，否则编译环境按 1.1 编译，静态语法测试用例全部编译失败。详见 `references/conventions/ets_version_naming.md` §三。

### 2.1.1 BUILD.gn 模板函数校验（编译前必须执行）

编译前验证 BUILD.gn 模板函数与目标 ETS 版本是否匹配：

```bash
# 提取模板函数名
TEMPLATE=$(grep -E "ohos_(js_app_suite|js_app_static_suite)\(" BUILD.gn | head -1)

# 校验
if echo "$TEMPLATE" | grep -q "ohos_js_app_static_suite"; then
    echo "静态测试套（1.2）"
elif echo "$TEMPLATE" | grep -q "ohos_js_app_suite"; then
    echo "动态测试套（1.1）"
else
    echo "❌ 未找到有效模板函数"
fi
```

**同时检查 BUILD.gn 中 `test_hap` 字段是否已注释**（当前 ohosTest 不可用，未注释会编译报错）。

### 2.2 提取命令

```bash
# 方法1：grep + sed
grep -E "ohos_(js_app_suite|js_app_static_suite)\(" BUILD.gn | \
  sed -n 's/.*("\([^"]*\)").*/\1/p' | head -1

# 方法2：awk
awk -F'"' '/ohos_(js_app_suite|js_app_static_suite)\(/ {print $2; exit}' BUILD.gn
```

### 2.3 编译 group

`suite` 参数不支持多个目标，但可以使用 BUILD.gn 中的 `group()` 名称编译该 group 下所有测试套：

```bash
# 编译 testfwk group 下所有测试套
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=testfwk

# 编译 arkui group
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite=arkui
```

group 名称来源于子系统 BUILD.gn 中的 `group("子系统名")` 定义。

---

## 三、编译工作流

### 3.1 动态测试套编译流程

```
环境准备（首次） → 提取 suite 名称 → 预编译清理 → 执行编译 → 验证产物
```

**完整示例**：
```bash
# 步骤1：预编译清理（每次必需）
{skill_root}/scripts/cleanup_group.sh {OH_ROOT} {子系统名}

# 步骤2：提取测试套名称
SUITE_NAME=$(grep -E "ohos_js_app_suite\(" BUILD.gn | sed -n 's/.*("\([^"]*\)").*/\1/p' | head -1)

# 步骤3：启动异步编译（推荐）
{skill_root}/scripts/async_build.sh {OH_ROOT} "$SUITE_NAME" rk3568 start

# 步骤4：等待完成
{skill_root}/scripts/async_build.sh {OH_ROOT} "$SUITE_NAME" rk3568 wait

# 步骤5：验证产物
test -f out/rk3568/suites/acts/acts/testcases/$SUITE_NAME/$SUITE_NAME.hap && echo "✅ 编译成功" || echo "❌ 编译失败"
```

### 3.2 静态测试套编译流程

静态测试套额外需要：**hvigor 版本校验** 和 **`xts_suitetype=hap_static` 参数**。

```
环境准备 → hvigor 版本校验 → 提取 suite 名称 → 预编译清理 → 执行编译（带 hap_static） → 验证产物
```

#### hvigor 版本校验（每次静态编译前必需）

目标版本：`"6.0.0-arkts1.2-ohosTest-25072102"`
位置：`prebuilts/command-line-tools/hvigor/hvigor/package.json`

```bash
# 快速校验
cd {OH_ROOT}
VERSION=$(cat ./prebuilts/command-line-tools/hvigor/hvigor/package.json 2>/dev/null | grep '"version"' | cut -d'"' -f4)
if [ "$VERSION" = "6.0.0-arkts1.2-ohosTest-25072102" ]; then
    echo "✅ 版本匹配"
else
    echo "⚠️ 需要替换 hvigor 工具"
    # 清理 SDK 缓存
    rm -rf prebuilts/ohos-sdk/linux
    # 清理旧工具
    rm -rf ./prebuilts/command-line-tools
    # 下载新工具
    git clone https://gitee.com/laoji-fuli/hvigor0702.git -b debug2 command-line-tools
    # 移动到预置目录
    mv -f command-line-tools ./prebuilts/
fi
```

**完整示例**：
```bash
# 步骤1：hvigor 版本校验（如上述脚本）

# 步骤2：预编译清理
{skill_root}/scripts/cleanup_group.sh {OH_ROOT} {子系统名}

# 步骤3：提取静态测试套名称
SUITE_NAME=$(grep -E "ohos_js_app_static_suite\(" BUILD.gn | sed -n 's/.*("\([^"]*\)").*/\1/p' | head -1)

# 步骤4：启动异步编译（带 hap_static 参数）
{skill_root}/scripts/async_build.sh {OH_ROOT} "$SUITE_NAME" rk3568 start xts_suitetype=hap_static

# 步骤5：等待完成
{skill_root}/scripts/async_build.sh {OH_ROOT} "$SUITE_NAME" rk3568 wait

# 步骤6：验证
test -f out/rk3568/suites/acts/acts/testcases/$SUITE_NAME/$SUITE_NAME.hap && echo "✅ 编译成功" || echo "❌ 编译失败"
```

---

## 四、预编译清理

编译前**必须**执行清理，确保编译结果包含最新代码。

### 4.1 使用 cleanup_group.sh（推荐）

```bash
# 清理指定子系统 group 下所有测试套
{skill_root}/scripts/cleanup_group.sh {OH_ROOT} {子系统名}

# 示例
{skill_root}/scripts/cleanup_group.sh /mnt/data/c00810129/oh_0130 testfwk
```

该脚本会自动：
1. 解析 BUILD.gn 获取所有测试套路径
2. 逐个清理 `.hvigor`、`build`、`entry/build`、`oh_modules` 等缓存目录
3. 清理 `oh-package-lock.json5`、`local.properties`
4. 清理 `{OH_ROOT}/out` 目录

### 4.2 手动清理单个测试套

```bash
# 步骤1：进入测试套目录
cd {OH_ROOT}/test/xts/acts/{子系统}/{测试套目录}

# 步骤2：删除缓存（使用显式路径前缀避免误删）
rm -rf ./.hvigor ./build ./entry/build ./oh_modules
rm -f ./oh-package-lock.json5 ./local.properties

# 步骤3：清理 out 目录
cd {OH_ROOT} && rm -rf out
```

**⚠️ 安全警告**：
- 使用 `./` 前缀防止误删 `{OH_ROOT}/build` 或 `{OH_ROOT}/test/xts/acts/build`
- **永远不要删除** `{OH_ROOT}/build` 或 `{OH_ROOT}/test/xts/acts/build`（这些目录包含所有测试套共享的编译基础设施，删除后需要重新编译整个 XTS 套件，耗时数小时）

---

## 五、编译环境准备

首次编译前需确认环境：

| 组件 | 版本要求 |
|------|---------|
| 操作系统 | Ubuntu 18.04+ / OpenEuler 20.03+ |
| Node.js | 14.x+（推荐 16.x） |
| npm | 6.x+ |
| Python | 3.x |
| Git | 2.x |
| 磁盘 | 20GB+ 可用空间 |

验证命令：
```bash
node --version && npm --version && python3 --version && git --version
```

SDK 下载：
```bash
cd {OH_ROOT} && ./build/prebuilts_download.sh
```

---

## 六、错误自动处理（v1.16.0+）

使用 general subagent 执行编译时，自动处理以下错误：

| 错误类型 | 处理策略 | 说明 |
|---------|---------|------|
| **语法错误** | 自动修复 | 分析错误日志 → 定位问题 → 修改代码 → 重试（最多 3 次） |
| **类型错误** | 自动修复 | 添加类型注解、修正 API 调用 |
| **导入错误** | 自动修复 | 添加缺失的 import |
| **配置错误** | 确认后修改 | BUILD.gn、证书、环境变量等需用户确认 |
| **依赖/环境错误** | 手动处理 | 依赖缺失、磁盘空间不足等 |

---

## 七、故障排除速查

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| BUILD FAILED | 语法/依赖/配置错误 | `grep -i "error" out/rk3568/suites/acts/acts/build.log` |
| HAP 不生成 | BUILD.gn 名称不匹配 | 从 BUILD.gn 重新提取 suite 名称 |
| 静态编译失败 | hvigor 版本不匹配 | 执行版本校验和替换（第三章） |
| 证书未找到 | 证书文件缺失 | 检查 `signature/` 目录 |
| Node.js 版本过低 | 版本不满足要求 | `nvm install 16 && nvm use 16` |
| 权限不足 | 文件被占用或权限问题 | 关闭 IDE，检查 `ls -la` |
| 磁盘空间不足 | 编译产物过大 | `rm -rf out/`，`df -h` 检查 |

> 详细排查指南：[build_troubleshooting.md](./build_troubleshooting.md)

---

**版本**: 2.0.0
**更新日期**: 2026-04-01
**兼容性**: OpenHarmony API 10+
