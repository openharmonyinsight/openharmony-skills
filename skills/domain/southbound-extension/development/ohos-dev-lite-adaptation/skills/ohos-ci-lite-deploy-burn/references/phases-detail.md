# Phase 0-5 Detail

> From ohos-ci-lite-deploy-burn/SKILL.md (C2)

## Phase 0：环境检测

> 所有后续阶段的前提。首次运行必须执行，后续可跳过。

### 0.0 根据连接方法路由

```
读取 config.json → connection.method
  │
  ├─ "ssh"   → 执行 §0.1 (SSH 免密 + 远程工具链)
  │
  ├─ "local" → 执行 §0.2 (本地工具链 + 路径验证)
  │
  └─ "custom" → 执行 §0.3 (运行用户自定义 connect_cmd 验证)
```

### 0.1 SSH 模式环境检测

详见 `references/connection-methods/ssh.md`。

#### 0.1.1 SSH 免密登录

```powershell
ssh -o BatchMode=yes -o ConnectTimeout=5 -p ${SSH_PORT} -i ${SSH_IDENTITY} ${SSH_TARGET} "echo SSH_OK"
```

- **退出码 0** → ✅ 免密已配好，继续
- **退出码非 0** → 需要配置免密：

```powershell
# 方式 A: 手动配置（推荐提前做）
ssh-copy-id -p ${SSH_PORT} -i ${SSH_IDENTITY} ${SSH_TARGET}

# 方式 B: 提示用户提供密码后一次性推送公钥
# （由 Agent 在对话中引导执行）
```

#### 0.1.2 远程工具链检测

通过 SSH 在远程服务器上检查：

```powershell
ssh -p ${SSH_PORT} -i ${SSH_IDENTITY} ${SSH_TARGET} "
  ls ${CODE_DIR}/build.sh >/dev/null 2>&1 && echo BUILD_SH_OK || echo BUILD_SH_MISSING
  which ${TOOLCHAIN_PREFIX}gcc >/dev/null 2>&1 && echo TOOLCHAIN_OK || echo TOOLCHAIN_MISSING
  python3 --version 2>/dev/null && echo PYTHON_OK || echo PYTHON_MISSING
  ninja --version 2>/dev/null && echo NINJA_OK || echo NINJA_MISSING
"
```

**关键检查项**（按优先级）：

| 检查项 | 预期结果 | 失败处理 |
|--------|---------|---------|
| `build.sh` 存在 | BUILD_SH_OK | 检查 code_dir 是否正确 |
| 工具链可用 | TOOLCHAIN_OK | 检查 toolchain_prefix 是否正确；参考 compiler_fix_playbook.md F19 |
| Python 3.8+ | PYTHON_OK | `python3 --version` 或安装 |
| Ninja 可用 | NINJA_OK | `pip install ninja` 或确认在 PATH |

#### 0.1.3 本地工具检测（所有模式共用）

```powershell
python --version                              # Python 3.7+
python -c "import serial; print('OK')"      # pyserial（烧录需要）
python -c "import xmodem; print('OK')"      # xmodem（部分烧录协议）
```

缺失时一键安装：`pip install pyserial xmodem`

### 0.2 Local 模式环境检测

详见 `references/connection-methods/local.md`。

```powershell
# 验证源码目录存在且包含 build.sh
Test-Path "${LOCAL_CODE_DIR}\build.sh"

# 工具链检测
${TOOLCHAIN_PREFIX}gcc --version
ninja --version
python3 --version
```

### 0.3 Custom 模式

运行用户在 `connection.custom.connect_cmd` 中定义的命令。
- 成功时输出 `CONNECT_OK`
- 失败时非零退出码 + stderr 说明原因

---
## Phase 1：编译

### 前置条件

跳过 Phase 0 时，先做快速验证：

```powershell
# SSH 模式
ssh -o BatchMode=yes -o ConnectTimeout=5 -p ${SSH_PORT} ${SSH_TARGET} "echo OK"

# Local 模式
Test-Path "${CODE_DIR}\build.sh"
```

### 构建模式

如果设备的 `build_modes` 定义了多个模式（如 firmware / xts_all / xts_acts），**必须弹出选项让用户选择**。只有一个模式时直接使用。

从 `config.json` 或设备配置文件的 `build_modes` 读取可用模式。

### 执行编译

#### SSH 模式

```powershell
ssh -p ${SSH_PORT} -i ${SSH_IDENTITY} ${SSH_TARGET} "
  cd ${CODE_DIR} &&
  ${BUILD_COMMAND}
"
```

**输出处理**：
- 编译成功 → 提取关键信息（产物大小、编译耗时），进入 Phase 2
- 编译失败 → 捕获错误输出，参照 `../ohos-dev-build-config/references/error-cheatsheet.md` 诊断

#### Local 模式

```powershell
cd ${LOCAL_CODE_DIR}; ${BUILD_COMMAND}
```

### 编译超时建议

| 场景 | 建议超时 | 原因 |
|------|---------|------|
| firmware clean build | 10-15 min | 取决于代码量和服务器性能 |
| xts_all (含 XTS 框架) | 30-60 min | 含 XTS 框架编译 |
| 增量编译 (非 clean) | 2-5 min | 仅变更部分重新编译 |

---

## Phase 2：产物下载

> **仅 SSH 模式需要此阶段。Local 模式产物已在本地。**

### 2.0 用户交互点：下载目录

下载产物前，向用户确认本地存放目录：

> 产物（固件 .bin / .map / acts.zip 等）下载到哪个本地目录？
> - 直接给路径（如 `D:\flash`）
> - 或回车用默认：`~/Downloads/oh-lite-adapt/burn/`（下载文件夹下的 oh-lite-adapt/burn）

- 用户指定 → 用该路径（不存在则创建）
- 用户未指定/回车 → 默认 `~/Downloads/oh-lite-adapt/burn/`（Windows: `C:\Users\<user>\Downloads\oh-lite-adapt\burn\`；Linux/Mac: `~/Downloads/oh-lite-adapt/burn/`）
- 记录到 `local.artifacts_dir`，后续 Phase 3-5（烧录/测试/MAP）都用此目录

### 2.1 发现产物

**自动发现**（当 `remote_bin_files` 为空或未配置时）：

```powershell
ssh -p ${SSH_PORT} -i ${SSH_IDENTITY} ${SSH_TARGET} "
  find ${CODE_DIR}/out -name '*.bin' -type f -exec ls -lh {} \;
"
```

**使用配置列表**（当 `remote_bin_files` 已配置时）：直接使用列表中的路径。

### 2.2 下载到本地

```powershell
foreach ($bin in $REMOTE_BIN_FILES) {
    $localName = Split-Path $bin -Leaf
    scp -P ${SSH_PORT} -i ${SSH_IDENTITY} `
        ${SSH_TARGET}:${CODE_DIR}/${bin} `
        "${LOCAL_ARTIFACTS}\${localName}"
}

# 下载 MAP 文件
scp -P ${SSH_PORT} -i ${SSH_IDENTITY} `
    ${SSH_TARGET}:${CODE_DIR}/${REMOTE_MAP_PATH} `
    "${LOCAL_ARTIFACTS}\$(Split-Path ${REMOTE_MAP_PATH} -Leaf)"
```

### 2.3 验证产物

```powershell
Get-ChildItem "${LOCAL_ARTIFACTS}\*.bin" | Select-Object Name, @{N='SizeKB';E={[math]::Round($_.Length/1KB)}}
```

---

## Phase 3：烧录

> **依赖设备配置 (`device` 段)。无烧录功能的芯片可跳过此阶段。**

### 3.1 根据烧录工具路由

```
读取 device.burn_tool
  │
  ├─ "hibern"   → §3.2 (HiSilicon HiBurn)
  ├─ "openocd"  → §3.3 (OpenOCD + ST-Link/J-Link/DAPLink)
  ├─ "jlink"    → §3.4 (J-Link SEGGER 命令行)
  ├─ "esptool"  → §3.5 (espressif ESP32 烧录)
  ├─ "custom"   → 运行 device.burn_custom_cmd
  └─ "none"     → 跳过，提示用户手动烧录
```

> **⚠️ 安全模式**：若 `workflow_config.yaml.intake.security.secure_mode=secure`，烧录前确认镜像已签名（按芯片厂商签名流程）+ 用安全烧录流程（可能与非安全模式不同）。**问用户确认安全/非安全模式后再烧**，不要自己猜。

### 3.2 HiBurn (HiSilicon 系列)

适用于：Hi3861V100 / Hi3861V100 等使用 HiBurn 烧录引擎的芯片。

**前置条件**：
- HiBurn.exe 就绪（用户自备路径，plugin 不分发；路径经 `device.burn_tool_path` → `HIBURN_EXE` 以 `--hiburn` 传入，不依赖脚本同目录默认值）
- `tools/burn_one.py` 存在
- COM 端口可访问（Phase 0 已检测）

**烧录固件**：

```powershell
python "${SKILL_DIR}\tools\burn_one.py" `
  "<BIN_FILE_PATH>" `
  -com ${COM_PORT} -baud ${BAUD_RATE} `
  --hiburn "${HIBURN_EXE}" `
  --reset-mode ${RESET_MODE} `
  --timeout 90 `
  --log "${LOCAL_ARTIFACTS}\burn_<timestamp>.log"
```

**burn_one.py 参数速查**：

| 参数 | 默认值 | 说明 |
|------|--------|------|
|  COM 端口 | COM 端口（自动检测或 -com 指定） | COM 端口 |
| `--reset-mode` | at | at(软复位) / dtr(硬复位) / none(手动) |
| `--timeout` | 90 | 烧录超时(秒) |
| `--log` | 无 | 日志文件路径 |
| `--retries` | 5 | 重试次数 |
| `--probe` | - | 诊断模式：探测当前固件类型 |
| `--run-only` | - | 仅复位+捕获输出，不烧录 |
| `--burn-only` | - | 烧完即停，不进 XTS 回读循环 |

**burn_one.py 退出码**（脚本化 / CI 调用可程序化判定结果）：

| 退出码 | 含义 | 处置提示 |
|-------|------|---------|
| 0 | 成功：烧录完成 / 测试全过 | — |
| 1 | 超时或无结束标志；烧录失败；COM 端口锁被其他任务持有 | 先看输出中的 `[中止]`（锁占用，并发冲突非故障）或 `[烧录失败]`（按其提示排查 AT/复位）区分 |
| 2 | 测试有失败用例 | 按统计行（`X Tests, Y Failures`）定位失败用例 |
| 3 | 零测试用例 | 检查固件是否编入 XTS/测试代码 |
| 4 | 烧录完成但启动未确认（`--burn-only` 的 5s 未见输出） | 手动复位或用 `--run-only` 验证 |

**烧录安全注意事项**：

> ⚡ **烧录中途严禁中断！**
> Flash 写入是非原子操作，中断会导致芯片变砖。
> - 超时设置要充足（≥ 300s for firmware）
> - 看到 Entry loader / 进度条走动时耐心等待
> - 只有回读阶段可以安全中断

### 3.3 OpenOCD (ARM Cortex-M)

适用于：STM32 / NXP i.MX RT / GD32 等 ARM 芯片，使用 ST-Link/J-Link/DAPLink 调试器。

```powershell
openocd -f <interface.cfg> -f <target.cfg> -c "program <BIN_FILE> verify reset exit"
```

### 3.4 J-Link (SEGGER)

适用于：有 SEGGER J-Link 硬件调试器的任意芯片。

```powershell
JLinkExe -device <DEVICE_NAME> -if SWD -JTAGAuto -speed 4000 -command "loadfile <BIN_FILE>, <ADDR>" -command "go", "r"
```

### 3.5 esptool (ESP32 系列)

适用于：ESP32 / ESP32-S2 / ESP32-C3 / ESP32-S3 等 Espressif 芯片。

```powershell
esptool.py -p <COM_PORT> -b <BAUD> chip_id && esptool.py -p <COM_PORT> write_flash 0x0 <BIN_FILE>
```

---

## Phase 4：测试运行

> 烧录后自动复位芯片，捕获串口输出 + 统计 PASSED/FAILED。用于 XTS/ACTS 测试结果收集。
>
> `burn_one.py` 已集成 WAKE_MAGIC 唤醒 + AT 探测降级 + PASS/FAIL 统计（学 DeepRust pipeline）：
> - 发 AT+RST 前先探 AT，静默则 WAKE_MAGIC 唤醒，唤醒失败降级为仅监听 + 提示手按 RST。
> - 抓输出时累计 PASSED/FAILED，退出打印 `[统计] X Tests Y Failures 通过率 Z%`。

### 4.1 使用 burn_one.py run-only 模式（镜像已烧好，仅重跑 XTS）

适用于 AT 框架的芯片（如 Hi3861）：

```powershell
python "${SKILL_DIR}\tools\burn_one.py" --run-only `
  -com ${COM_PORT} -baud ${BAUD_RATE} `
  --reset-mode ${RESET_MODE} `
  --timeout ${XTS_TIMEOUT:-600} `
  --log "${LOCAL_ARTIFACTS}\test_run_<timestamp>.log"
```

`--run-only` 自动：AT 探测 → 静默则 WAKE_MAGIC 唤醒 → 发 AT+RST 软复位重跑 XTS → 抓输出 + 统计 PASS/FAIL。AT 唤醒失败时降级为仅监听（提示手按 RST）。

### 4.2 烧录并测试（Phase 3→4 一气呵成）

```powershell
python "${SKILL_DIR}\tools\burn_one.py" "${LOCAL_ARTIFACTS}\Hi3861_wifiiot_app_burn.bin" `
  -com ${COM_PORT} -baud ${BAUD_RATE} `
  --hiburn "${HIBURN_EXE}" `
  --reset-mode at --retries 5 --timeout ${XTS_TIMEOUT:-600} `
  --log "${LOCAL_ARTIFACTS}\test_run_<timestamp>.log"
```

烧完自动：发复位魔字节启动新固件 → 抓 XTS 输出 → 统计 PASS/FAIL。烧录成功后（at 模式）自动发 WAKE_MAGIC 唤醒 AT，保证下一轮可重复烧录。

### 4.3 通用串口捕获

适用于任意芯片（不用 burn_one.py 时）：

```powershell
python -c "
import serial, time
s = serial.Serial('${COM_PORT}', ${BAUD_RATE}, timeout=1)
start = time.time()
while time.time() - start < ${CAPTURE_TIMEOUT:-120}:
    line = s.readline().decode('utf-8', errors='replace').strip()
    if line: print(line)
s.close()
"
```

### 4.4 XTS/ACTS 结果解析

`burn_one.py` 自动统计 `PASSED` / `FAILED` 标记出现次数。手动解析时：XTS 输出里 `PASSED` / `FAILED` 两个标记各出现次数即为通过/失败用例数；结束标志 `All the test suites finished`。

---

## Phase 5：MAP 分析

> 独立于其他阶段的工具。分析 GNU ld 生成的 `.map` 文件，了解内存布局和代码分布。

### 5.1 触发与前置检查

用户说 "map分析"、"结果分析"、"对比 map" 时触发。

确认 MAP 文件存在于 `${LOCAL_ARTIFACTS}`：

```powershell
$mapFile = Get-ChildItem "${LOCAL_ARTIFACTS}\*.map" | Select-Object -First 1
if (-not $mapFile) { Write-Output "未找到 MAP 文件，请先执行 Phase 1+2"; return }
```

### 5.2 单个 MAP 分析

```powershell
python ${SKILL_DIR}\tools\map_analyzer.py analyze "<MAP_FILE>" -o "<OUTPUT_MD>"
```

**输出**：内存使用汇总（CODE/DATA/BSS/RODATA 占比）、Top-N 最大段、符号统计。

### 5.3 对比 MAP 分析

```powershell
python ${SKILL_DIR}\tools\map_analyzer.py compare "<MAP_FILE_1>" "<MAP_FILE_2>" -o "<OUTPUT_MD>"
```

**输出**：两版内存布局差异、段大小变化、可用于评估优化效果。

### 5.4 支持格式

| 格式 | 支持 |
|------|:----:|
| GNU ld 默认 MAP | ✅ |
| `-Map=` 生成 | ✅ |
| 带符号信息的 MAP | ✅ |
| IAR/Keil MAP | ❌ |

---

