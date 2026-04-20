# CAPI 编译工作流

> **模块信息**
> - 层级：L3_Validation
> - 优先级：按需加载
> - 适用范围：OpenHarmony CAPI XTS 测试工程编译
> - 平台：Linux / Windows (WSL/DevEco Studio/MinGW)
>
> **相关文档**：
> - [编译环境配置参考](../../references/env_setup_reference.md) - 环境搭建详细步骤
> - [Linux 编译工作流](./linux_compile_workflow_c.md) - Linux CAPI 编译工作流
> - [编译环境配置](./linux_compile_env_setup_c.md) - Linux 编译环境配置

> **重要提示**
> - Linux: 必须使用 `./test/xts/acts/build.sh` 编译
> - Windows: 推荐 WSL，DevEco Studio/MinGW 支持有限
> - 编译前必须从 BUILD.gn 提取正确的测试套名称（见第三节）

---

## 一、编译环境对比

| 特性 | Linux 原生 | Windows WSL | Windows DevEco | Windows MinGW |
|------|-----------|------------|----------------|---------------|
| **推荐度** | 最推荐 | 推荐 | 有限支持 | 不推荐 |
| **编译工具** | `build.sh` | `build.sh` | `hvigorw` | `gcc/g++` |
| **CAPI 支持** | 完整 | 完整 | 有限 | 有限 |
| **性能** | 最佳 | 良好 | 中等 | 较差 |

> 环境配置的详细步骤已移至 [references/env_setup_reference.md](../../references/env_setup_reference.md)

---

## 二、编译工作流程

```
步骤1：环境准备 → 步骤2：CAPI 环境配置 → 步骤3：测试套名称提取 → 步骤4：执行编译 → 步骤5：验证结果
```

### 2.1 编译模式对比

| 模式 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| **同步编译** | 简单直接 | 长时间阻塞 | 快速验证、调试 |
| **异步编译（推荐）** | 不阻塞，可并行 | 需轮询状态 | 正式编译、批量编译 |

---

## 三、测试套名称提取（关键步骤）

> **编译前必须先从 BUILD.gn 提取测试套名称**，该名称将作为 `suite` 参数值。
> - 错误做法：直接使用目录名
> - 正确做法：读取 BUILD.gn，提取 `ohos_js_app_suite()` 或 `ohos_js_app_static_suite()` 后面的名称

### 3.1 BUILD.gn 测试套类型

| 类型 | BUILD.gn 模板 | 说明 |
|------|--------------|------|
| 静态 JS 测试套 | `ohos_js_app_static_suite("Name")` | N-API 封装测试（静态编译） |
| 动态 JS 测试套 | `ohos_js_app_suite("Name")` | 纯 JS 或 N-API 封装测试 |
| App Assist 测试套 | `ohos_app_assist_suite("Name")` | 辅助测试套 |

### 3.2 提取步骤

**定位 BUILD.gn 文件**：
```
{OH_ROOT}/test/xts/acts/{子系统}/{模块}/actsxxxtest/BUILD.gn
```

**提取命令**：
```bash
# 方法1：grep + sed
grep -E "ohos_(js_app_suite|js_app_static_suite|native_test_suite)\(" BUILD.gn | \
  sed -n 's/.*("\([^"]*\)").*/\1/p' | head -1

# 方法2：awk
awk -F'"' '/ohos_(js_app_suite|js_app_static_suite|native_test_suite)\(/ {print $2; exit}' BUILD.gn
```

**示例**：
```gni
# BUILD.gn 内容：
ohos_js_app_suite("ActsBmsGetAbilityResourceNdkEnterpriseTest") { ... }
# 提取结果：ActsBmsGetAbilityResourceNdkEnterpriseTest
```

### 3.3 平台编译命令

```bash
# Linux
cd {OH_ROOT} && ./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite={测试套名称}

# Windows WSL
wsl bash -c "cd /mnt/c/openharmony && ./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite={测试套名称}"

# Windows DevEco
hvigorw.bat assembleHap -Pproduct_name=rk3568 -Psystem_size=standard -Psuite={测试套名称}
```

---

## 四、异步编译（推荐）

> OpenHarmony 编译通常需要 10-30 分钟，异步编译可避免阻塞主流程。

### 4.1 架构

```
启动后台编译 (nohup) → 记录 PID/日志到 /tmp/oh_capi_build/ → 轮询检查状态 → 返回结果
```

### 4.2 async_build.sh 命令参考

**脚本位置**: `scripts/async_build.sh`

```bash
# 启动异步编译
./scripts/async_build.sh {OH_ROOT} {测试套名称} rk3568 start

# 检查编译状态
./scripts/async_build.sh {OH_ROOT} {测试套名称} rk3568 status

# 实时查看日志
./scripts/async_build.sh {OH_ROOT} {测试套名称} rk3568 tail

# 等待编译完成
./scripts/async_build.sh {OH_ROOT} {测试套名称} rk3568 wait

# 停止编译
./scripts/async_build.sh {OH_ROOT} {测试套名称} rk3568 stop

# 查看完整日志
./scripts/async_build.sh {OH_ROOT} {测试套名称} rk3568 logs

# 查看错误摘要
./scripts/async_build.sh {OH_ROOT} {测试套名称} rk3568 errors
```

### 4.3 编译参数

| 参数 | 说明 | 必选 | 可选值 |
|------|------|------|--------|
| `product_name` | 产品名称 | 必选 | rk3568（固定值） |
| `system_size` | 系统规格 | 必选 | standard（固定值） |
| `suite` | 测试套名称 | 必选 | 从 BUILD.gn 获取 |
| `xts_suitetype` | 测试套类型 | 可选 | hap_static, hap_dynamic |

**重要说明**：
- `product_name=rk3568` 和 `system_size=standard` 是固定值，不可修改
- 默认编译动态 CAPI 测试套，无需指定 `xts_suitetype`
- 只有编译静态 CAPI 测试套时才需要 `xts_suitetype=hap_static`

### 4.4 临时文件结构

```
/tmp/oh_capi_build/
├── {测试套名称}.log      # 编译日志
├── {测试套名称}.pid      # 进程 PID
├── {测试套名称}.status   # 编译状态（RUNNING/SUCCESS/FAILED）
└── {测试套名称}.error    # 错误信息
```

### 4.5 状态文件格式

```
[BUILD] start_time: 2026-03-24 10:00:00
[BUILD] suite_name: ActsCameraManagerCapiTest
[BUILD] status: RUNNING
[BUILD] end_time: 2026-03-24 10:25:30
[BUILD] status: SUCCESS
[BUILD] exit_code: 0
```

### 4.6 Python API（async_build_manager.py）

```python
from async_build_manager import AsyncBuildManager

manager = AsyncBuildManager("/path/to/openharmony")

# 异步启动
result = manager.start_build("ActsCameraManagerCapiTest")
status = manager.get_status("ActsCameraManagerCapiTest")

# 阻塞等待
result = manager.start_build("ActsCameraManagerCapiTest", blocking=True, timeout=3600)

# 命令行
# python scripts/async_build_manager.py {OH_ROOT} {suite} --action start|status|wait|logs|progress
```

---

## 五、同步编译

```bash
# 标准编译命令
cd {OH_ROOT}
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite={测试套名称}

# 编译静态测试套
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite={测试套名称} xts_suitetype=hap_static

# 编译前清理
rm -rf .hvigor build entry/build entry/.cxx oh_modules
```

---

## 六、编译验证

```bash
# 检查编译产物
ls out/rk3568/suites/acts/acts/testcases/*.hap

# 验证 HAP 文件
find out/rk3568/suites/acts/acts/testcases -name "*.hap" -exec ls -lh {} \;
```

---

## 七、故障排除

### 7.1 常见问题速查

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 编译失败 | 依赖缺失 | 检查并安装所需依赖 |
| HAP 不生成 | BUILD.gn 配置错误 | 检查 BUILD.gn 中测试套名称和类型 |
| 静态编译超时 | SDK 编译耗时 | 增加超时时间 |
| 类型检查失败 | TS 语法错误 | 运行 `verify_napi_triple.sh` 检查 |
| suite 参数无效 | 名称不匹配 | 从 BUILD.gn 重新提取名称 |

### 7.2 调试方法

```bash
# 启用详细输出
./test/xts/acts/build.sh product_name=rk3568 system_size=standard suite={名称} verbose

# 查看编译日志
tail -f out/rk3568/suites/acts/acts/testcases/build.log

# 清理编译缓存
./test/xts/acts/build.sh clean

# WSL 环境检查
wsl.exe --version && cat /etc/os-release | grep PRETTY_NAME

# DevEco Studio 缓存清理
# File → Invalidate Caches / Restart

# MinGW 工具链检查
gcc --version && g++ --version
```

### 7.3 推荐工作流

```bash
# 1. 清理历史产物
bash scripts/cleanup_group.sh {OH_ROOT} {子系统名}

# 2. 从 BUILD.gn 提取测试套名称
SUITE_NAME=$(grep -E "ohos_js_app_suite\(" BUILD.gn | sed -n 's/.*("\([^"]*\)").*/\1/p' | head -1)

# 3. 启动异步编译
./scripts/async_build.sh {OH_ROOT} "$SUITE_NAME" rk3568 start

# 4. 监控进度
./scripts/async_build.sh {OH_ROOT} "$SUITE_NAME" rk3568 status

# 5. 等待完成
./scripts/async_build.sh {OH_ROOT} "$SUITE_NAME" rk3568 wait

# 6. 验证结果
ls out/rk3568/suites/acts/acts/testcases/*.hap
```

---

**版本**: 1.2.0
**更新日期**: 2026-03-28
**兼容性**: OpenHarmony API 10+
