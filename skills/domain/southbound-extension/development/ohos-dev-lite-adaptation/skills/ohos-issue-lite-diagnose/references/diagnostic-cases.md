# 真实错误案例库

> 本文件收录了 OpenHarmony Lite 社区实践中遇到的真实错误案例，按问题类型分类。每个案例包含完整的错误现象、诊断过程和修复方案，是问题诊断的核心知识资产。

---

## 1. 编译错误案例

### 案例C001：Hi3861 CMSIS头文件路径错误

**错误日志**：
```
device/soc/hisilicon/hi3861v100/hal/los_tick.c:12:10: fatal error: 
cmsis_os2.h: No such file or directory
   12 | #include "cmsis_os2.h"
      |          ^~~~~~~~~~~~~
```

**诊断过程**：
1. 搜索代码库确认cmsis_os2.h的实际位置
2. 发现在kernel/liteos_m/kal/cmsis/CMSIS/RTOS2/Include/目录下
3. BUILD.gn中的include_dirs未包含该路径

**修复方案**：
```gn
# BUILD.gn
include_dirs += [
    "//kernel/liteos_m/kal/cmsis/CMSIS/RTOS2/Include",
]
```

---

### 案例C002：STM32F407 Kconfig依赖未满足

**错误日志**：
```
device/soc/st/stm32f407/hal/spi.c:34:5: error: 'SPI_HandleTypeDef' undeclared
   34 |     SPI_HandleTypeDef hspi;
      |     ^~~~~~~~~~~~~~~~~
```

**诊断过程**：
1. SPI_HandleTypeDef定义在stm32f4xx_hal_spi.h中
2. 该头文件仅在LOSCFG_DRIVERS_HDF_PLATFORM_SPI=y时被包含
3. Kconfig中未开启SPI平台驱动选项

**修复方案**：
```
# menuconfig中开启
Device Drivers → HDF Platform Driver → SPI Platform Driver → Enable
```

---

## 2. 链接错误案例

### 案例L001：Hi3861 RAM段溢出

**错误日志**：
```
riscv32-unknown-elf-ld: region `RAM' overflowed by 8192 bytes
memory layout:
  FLASH: 0x00400000-0x00480000 (512KB, used 72%)
  RAM:   0x00000000-0x00050000 (320KB, used 103%)
```

**诊断过程**：
1. 分析.map文件找出RAM占用Top模块
2. 发现WiFi协议栈占用了120KB
3. BLE协议栈占用了60KB
4. 应用代码+内核约140KB

**修复方案**：
```
1. 如不需要BLE，在product.json中移除ble组件 (-60KB)
2. 减小WiFi缓冲池大小 (wlan_config.h: WLAN_MEM_POOL_SIZE 64K→48K)
3. 启用LTO: cflags += ["-flto"]
4. 使用-nano-specs减小newlib体积
```

---

## 3. 启动失败案例

### 案例B001：BES2600W启动无输出

**现象**：烧录后串口完全无输出，LED不亮

**诊断过程**：
1. 使用J-Link连接，确认CPU可以halt → 硬件连接正常
2. 查看PC寄存器值：0x00000000 → CPU在执行空地址
3. 检查Flash内容：向量表位置为空（0xFF）
4. 发现烧录工具的目标地址配置错误，固件被写到了错误的Flash偏移

**修复方案**：
```
修正烧录工具的目标地址为0x00000000（BES2600W的Flash起始地址）
重新烧录后正常启动
```

---

### 案例B002：STM32F407内核启动后HardFault

**串口输出**：
```
=== HardFault Handler ===
CFSR:  0x00000200 (UNDEFINSTR)
HFSR:  0x40000000 (FORCED)
PC:    0x08012345
LR:    0x08004567
```

**诊断过程**：
1. CFSR.UNDEFINSTR表示执行了未定义指令
2. PC=0x08012345，通过addr2line定位到FloatCalcTask
3. 该任务使用了浮点运算，但Kconfig中未启用FPU支持
4. Cortex-M4F的FPU未被使能，浮点指令被视为未定义指令

**修复方案**：
```kconfig
# Kconfig中启用FPU
config LOSCFG_ARCH_CORTEX_M4_FPU
    bool "Enable FPU"
    default y
```

---

## 4. IoT组件注册失败案例

### 案例D001：Hi3861 GPIO组件注册失败

**串口日志**：
```
[ERROR] gpio component register failed, ret=-1
[WARN] GpioOpen will not be available
```

**诊断过程**：
1. 检查gpio_component.c中的注册函数
2. 发现IoTGpioRegister()返回-1
3. 追溯发现原因是HAL层的GpioHalInit()失败
4. GpioHalInit()中调用的时钟使能函数使用了错误的时钟ID

**修复方案**：
```c
// hi3861_gpio_hal.c
int32_t GpioHalInit(void) {
    // 修正：使用正确的GPIO时钟使能
    // 原代码: ClockEnable(CLOCK_GPIO);  ← 错误的时钟ID
    ClockEnable(CLOCK_GPIO0);  // ✓ 正确的Hi3861 GPIO时钟ID
    return 0;
}
```

---

## 5. 运行时异常案例

### 案例R001：STM32F407栈溢出导致HardFault

**JTAG调试信息**：
```
CFSR: 0x00020000 (STKERR)
PSP:  0x2003FC00 (低于任务栈底0x2003FE00)
PC:   0x08005678 (SensorProcessTask)
```

**诊断过程**：
1. STKERR表示栈操作错误
2. PSP=0x2003FC00 < 栈底0x2003FE00，确认栈溢出
3. SensorProcessTask栈大小配置为512字节
4. 函数内定义了uint8_t rawBuf[384] + 调用链开销 > 512字节

**修复方案**：
```c
// 方案A: 增大任务栈
TSK_INIT_PARAM_S taskAttr = {0};
taskAttr.uwStackSize = 2048;  // 从512增到2048

// 方案B: 将大数组改为静态分配
static uint8_t g_rawBuf[384];  // .bss段，不占栈空间
```

---

### 案例R002：Hi3861看门狗复位

**现象**：系统运行约30秒后自动重启，周期性重复

**诊断过程**：
1. 在启动代码中添加GPIO翻转标记，确认是看门狗复位（非电源问题）
2. 检查看门狗配置：超时时间设为5秒
3. 检查主循环：发现WiFi扫描过程中有一个阻塞式等待，最长可达8秒
4. 该等待期间无喂狗操作，导致看门狗超时复位

**修复方案**：
```c
// 在WiFi扫描等待循环中添加喂狗
while (scanInProgress) {
    WatchdogFeed();  // ✓ 添加喂狗
    OsalMsleep(100);
    scanInProgress = CheckScanStatus();
}

// 或者增大全局看门狗超时时间
WatchdogSetTimeout(15000);  // 从5秒改为15秒
```

---

## 6. 功耗问题案例

### 案例P001：STM32F407低功耗模式电流异常

**症状**：进入Stop模式后电流为15mA（预期<10μA）

**诊断过程**：
1. 逐个禁用外设，发现禁用UART1后电流降至12μA
2. 检查UART1配置：进入Stop前未关闭UART1时钟
3. UART1在Stop模式下仍在工作，消耗大部分电流

**修复方案**：
```c
// 进入Stop模式前的驱动Suspend
void UartSuspend(void) {
    // 保存UART配置
    g_savedBaud = READ_REG(UART_BRR);
    
    // 关闭UART时钟
    __HAL_RCC_USART1_CLK_DISABLE();
    
    // 配置UART引脚为模拟模式（最低漏电）
    GpioSetMode(UART_TX_PIN, GPIO_MODE_ANALOG);
    GpioSetMode(UART_RX_PIN, GPIO_MODE_ANALOG);
}

// 从Stop模式唤醒后的Resume
void UartResume(void) {
    // 恢复UART时钟
    __HAL_RCC_USART1_CLK_ENABLE();
    
    // 恢复引脚复用
    GpioSetAf(UART_TX_PIN, GPIO_AF7_USART1);
    GpioSetAf(UART_RX_PIN, GPIO_AF7_USART1);
    
    // 恢复UART配置
    WRITE_REG(UART_BRR, g_savedBaud);
}
```

---

## 7. 芯片特有问题速查

### 7.1 Hi3861特有问题

| 问题 | 现象 | 根因 | 解决方案 |
|------|------|------|---------|
| WiFi初始化超时 | IotWifiInit()返回失败 | 固件文件未正确放置或SPI通信异常 | 确认firmware.bin位置、检查SPI引脚配置 |
| 编译找不到wifi头文件 | fatal error: iot_wifi.h | WiFi组件未在product.json中启用 | 在subsystems中添加wifi组件 |
| Flash读写异常 | 写入后读回数据不一致 | Flash扇区未擦除就写入 | 写入前先调用FlashErase |
| 低功耗唤醒后GPIO异常 | 唤醒后GPIO状态不确定 | 低功耗退出后未重新初始化GPIO | 在resume回调中重新配置GPIO |

### 7.2 STM32F407特有问题

| 问题 | 现象 | 根因 | 解决方案 |
|------|------|------|---------|
| RAM溢出 | 链接阶段段溢出 | 组件过多超出256KB RAM | 裁剪非必要组件、启用LTO |
| HardFault(STKERR) | 运行时HardFault | 栈溢出或未对齐访问 | 增大栈空间、检查指针操作 |
| FPU相关HardFault | 使用浮点运算后崩溃 | 未启用FPU或未保存FPU上下文 | 在Kconfig中启用FPU支持 |
| DMA传输数据错误 | DMA接收数据不全 | DMA缓冲区不在SRAM区域或未对齐 | 确保DMA缓冲区在正确内存区域 |
| 低功耗唤醒失败 | Stop模式无法唤醒 | EXTI配置错误或HSI恢复时序 | 检查EXTI线配置、确认唤醒源 |

### 7.3 BES2600W特有问题

| 问题 | 现象 | 根因 | 解决方案 |
|------|------|------|---------|
| 显示驱动花屏 | LCD输出异常 | MIPI/SPI时序参数不匹配 | 根据屏幕规格书调整timing |
| BT/WiFi共存干扰 | WiFi连接不稳定 | BT和WiFi共享天线、射频冲突 | 调整共存策略、分时复用 |
| 音频播放断续 | DAC输出卡顿 | DMA缓冲区过小或优先级不够 | 增大DMA缓冲、提高音频任务优先级 |
| 烧录后无法启动 | 烧录成功但不运行 | 启动模式引脚配置错误 | 确认BOOT引脚电平正确 |

---

## 8. 烧录问题案例（实测 Hi3516CV610 实战）

> L1 烧录是硬件操作，失败常卡在 bootrom 阶段。以下案例来自 hi3516cv610 DMEB 板（SPI Nand 默认介质）裸烧实战。完整症状→原因→处置表见 `skills/ohos-ci-lite-deploy-burn/SKILL.md`「烧录失败症状→原因→处置」。

### 8.1 bootrom 阶段报错鉴别速查（烧 boot / 裸烧）

| 控制台日志 | 含义 | 倾向 |
|---|---|---|
| `Failed to send start frame` | 15s 内没重新上电 / COM 错 / 串口接触 | 模式/时序 |
| `Failed to send head frame` | boot_image 与单板不匹配 / DDR 初始化失败 | **镜像内容** |
| `Failed to send data frame` | 串口连接松动 | 串口 |
| `burn gsl code data failed` / `U-Boot is faulty` / timeout / 烧 boot 无响应 | bootrom 没握手成功 | 见 BG001：可能 **GSL 文件用错** 或 模式/时序 |
| `Failed to execute command` | Flash 类型选错（实际 NAND 却走 SPI） | 介质错配 |
| `DDR Training 失败` | reg_info 的 DDR 颗粒配置不匹配 | **镜像内容**（reg_info） |
| uboot `BUG: ... pagesize 8192` / 内核 `cannot found in spi nand id table` + `bsp_spi_nand_probe error -19` | 板载 SPI Nand 颗粒不在 ID 表（两侧独立表） | **驱动适配**（ID 表，见 BG003） |

**关键鉴别**：非 boot 分区（env/kernel/rootfs）能连上有正常报错 = 串口/连接没问题 → 倾向镜像问题，别只查时序。

> **DDR 变体错配排查走 `ohos-dev-soc-spec-parse` skill**：裸烧 uboot 起不来 / DDR Training 失败 → 优先怀疑 SoC 内置 DDR 变体错配（xlsm 选错）。调用 ohos-dev-soc-spec-parse 单点查询"该变体该用哪个 xlsm"（命中 `ddr-variant-guide.md`，如 Hi3516CV610 -10B=DDR2 64MB QFN xlsm，-20S/-20G=DDR3 128MB QFN xlsm，不可互换）。

### 案例BG001：Hi3516CV610 裸烧 boot 报 `burn gsl code data failed`（GSL 文件误用）

**现象**：按分区烧写（FlashType=nand），勾 boot 裸烧，控制台报：
```
burn gsl code data failed
failed to download boot file
U-Boot is faulty
timeout
Failed to send the data frame
```
跳过 boot 只烧 env/kernel/rootfs 则能连上（得到别的正常报错）。

**诊断过程**（含两次误判，教训）：
1. 第一轮：对照 boot_image 结构（有 GSL+u-boot 魔数 0x27051956+entry 0x41700000+"System startup" 串），断言"boot_image 没问题，是裸烧时序/串口"。**错**——结构完整 ≠ 文件用对。
2. 用户反驳：非 boot 能连 = 串口没问题，不该是时序。
3. 第二轮：怀疑 reg_info/DDR 不匹配。但 reg_info 区与参考构建一致，且报错是 data frame 不是 head frame / DDR Training，DDR 嫌疑排除。
4. **报错字面 "gsl"** → 查 image_tool 的 `input/gsl.bin` 来源。参考仓 `boards/dmeb/Makefile` 的 `gslboot_build` 写明：gsl.bin = `components/gsl/pub/gsl.bin`（从 `boards/dmeb/components/gsl` 源码 `make CHIP=hi3516cv610` 产出，~20KB）。
5. 核对发现：实际喂给 image_tool 的是 `u-boot-hi3516cv610.bin`（148KB，u-boot 树产物，**不是 gsl**）。两者完全不同（差 7 倍）。bootrom 拿到错误 GSL → 拒绝 → `burn gsl code data failed`。
6. 结构侧证：错误 gsl 使 boot_image 虚胖（u-boot 被推到 0x28e00、0x824 处 gsl-size 字段=0x24600/148KB）；换成正确 20KB gsl 后结构恢复（u-boot@0x9800、0x824=0x5000/20KB）。

**修复方案**：
```bash
# 正确 gsl.bin 来源（参考仓 boards/dmeb/Makefile: gslboot_build）
cd boards/dmeb/components/gsl && make CHIP=hi3516cv610   # 产出 pub/gsl.bin (~20KB)
# image_tool input/ 填三个文件：
#   gsl.bin              = components/gsl/pub/gsl.bin   ← 之前误用 u-boot-hi3516cv610.bin
#   reg_info.bin         = xlsm_to_bin.py 从 DDR3_2133M_128MB_QFN.xlsm 生成
#   u-boot-original.bin  = hi3516cv610_defconfig 编出的 u-boot.bin
cd tools/pc/image_tool && PYTHONPATH=common python3 oem/oem_quick_build.py
```

**教训**：
- 报错字面提到的组件名（gsl/reg_info/u-boot），先查该组件**来源对不对**，别改判成通用原因（时序/串口）。
- 二进制结构校验只能证"完整"，证不了"正确"。要证正确，对照权威构建流程（Makefile）看每个 input 文件该从哪来。
- 鉴别镜像 vs 时序：非 boot 能连 = 串口没问题 → 倾向镜像。

### 案例BM001：Hi3516CV610 烧 env 报 `no find spi` + `Invalid spi flash block size`（介质错配）

**现象**：非裸烧（跳过 boot）烧 env/kernel/rootfs，板上现有 uboot 启动后控制台报：
```
Loading Environment from NAND... OK     ← 板上现有 uboot 是 NAND 版
getinfo spi → no find spi               ← 找不到 SPI Nor 芯片
Invalid spi flash block size!           ← 拿不到 block size，烧不下去
```

**诊断过程**：
1. 报错 `no find spi` = 板子没有 SPI Nor 芯片。但烧录包目标是 SPI Nor（burn_table FlashType=spi，rootfs=jffs2，env root=/dev/mtdblock3 jffs2）。
2. 查参考仓《Hi3516CV610 Demo 单板使用指南》：明示 "SPI Nand Flash（默认）"，SPI Nor 需换器件 U909。BOOT_SEL[1:0]：00=SPI Nor / 01=SPI Nand / 11=eMMC，默认 01。
3. 板上现有 uboot `Loading Environment from NAND` 印证板子是 SPI Nand。
4. 根因：`boot.medium` 假设成 SPI Nor，没对着实际硬件确认。

**修复方案**：按实际介质（SPI Nand）重做包：
- rootfs：jffs2 → **ubifs**（mkfs.ubifs + ubinize，2k page/128k EB）
- env：nor_env → **nand_env**（root=ubi0:ubifs rootfstype=ubifs ubi.mtd=3，mtdparts=nand:…）
- burn_table：FlashType spi → **nand**，FileSystem 全 none
- u-boot：hi3516cv610_defconfig 同时支持 Nor+Nand（含 FMC_SPI_NAND+ENV_IS_IN_NAND），可复用

**教训**：`boot.medium` 不能假设，必须从硬件确认（板上 uboot `getinfo` / 拨码 / 原理图）。已固化到 01-env-prep Step 0 前置采集。

### 案例BG002：Hi3516CV610 裸烧 boot_image 烧到 100% → `Uncompress Fail! err=0x81`（0x81 根因待确认；defconfig 差异 + 手工拼绕过标准构建为强线索）

**现象**：hi3516cv610 DMEB 板裸烧 boot_image，烧到 100% 后控制台报：
```
Uncompress Fail! err=0x81
```
（GZIP 解压 IP 报错），uboot 起不来。串口/连接没问题——非 boot 分区（env/kernel/rootfs）能连上有正常报错。

**⚠️ 根因待确认**：0x81 的根因**未 100% 确证**。以下为强线索（指向 uboot 内容本身有问题），但用户最终手动换"别的 bin"才启动 uboot（非我们生成的 SDK bin），故 defconfig 差异是定位方向而非已确证的唯一根因。
1. **defconfig 差异（强线索）**：构建 uboot 用了 `hi3516cv610_defconfig`（非 debug，含 `CONFIG_BSP_DISABLE_DOWNLOAD=y` 生产标志），而参考仓标准 `build.sh` 用 `DEBUG=1` → `hi3516cv610_debug_defconfig`。两者 uboot 大小差 24K，内容不同。SDK 标准编译（debug defconfig）产出的 bin 烧出 `Uncompress Ok!`，是强线索。
2. **手工拼绕过标准构建（强线索）**：因服务器 SDK 片段不全跑不了标准 `build.sh dmeb all`，被迫 copy image_tool + 手工喂 3 个 input（gsl.bin/reg_info.bin/u-boot-original.bin）+ oem_quick_build.py，绕过标准 `gslboot_build`。手工拼出的 boot_image ~200K，与 SDK 标准编的 223K 不一致 → 构建流程错了。
3. **reg_info 排除**：reg_info（DDR 参数）经逐字节对比完全一致（排除 DDR 参数不匹配假设——DDR Training 通过也佐证）。
4. **未确证点**：用户手动换"别的 bin"也启动了 uboot，未最终确证 defconfig 是唯一根因。0x81 可能还有其他触发路径。

**诊断过程**（含多轮误判 + 教训）：
1. **加调试打印拿 err=0x81**：在 hw_comp stub 里加打印看 `hw_dec_decompress` 返回值/`crg`/`rtnlen`，拿到 err=0x81。
2. **踩坑——加打印改 stub 布局导致 GZIP IP 挂死**：dbg2/dbg4 位置加打印会让 GZIP 硬件 IP 挂死（板子卡死），dbg1 稳定。教训：打印要放在 `hw_dec_decompress` 返回后的 fail 分支内，不能在 ret-check 前无条件运行——否则改了 stub 布局影响 GZIP IP 时序。
3. **排除 reg_info/gzip/CRC/硬件**：reg_info 对比一致；gzip 数据本身没坏；CRC 校验通过；硬件 DDR Training 通过。逐一排除后，剩下"uboot 内容本身有问题"。
4. **0x81 含义查不到**：0x81 属 HiSilicon NDA TRM（GZIP 解压 IP 的 err_info 寄存器），公开资料查不到含义。靠"走 SDK 标准编译对比"定位（专家建议）。
5. **专家建议——同一 SDK 版本标准编译应一致**：我们手工拼的（~200K）与 SDK 标准编的（223K）不一致，说明构建流程错了。不一致 → 回溯构建流程，别在二进制位级 debug。
6. **发现 defconfig 差异**：对比标准 `build.sh`（`DEBUG=1` → `hi3516cv610_debug_defconfig`）与我们用的 `hi3516cv610_defconfig`（非 debug，含 `CONFIG_BSP_DISABLE_DOWNLOAD=y` 生产标志），两者 uboot 差 24K。SDK 标准编译（debug defconfig）产出烧出 `Uncompress Ok!`，是强线索。

**定位方向（未确证为唯一根因）**：走 SDK 标准编译，不手工拼：
```bash
# 标准 gslboot_build（用 debug defconfig）
make LIB_TYPE=musl CHIP=hi3516cv610 BOOT_MEDIA=spi_nand DEBUG=1 gslboot_build
# 或等价：cd build && ./build.sh dmeb all debug pack
# 产出标准 boot_image（227840B / ~223K），用 hi3516cv610_debug_defconfig
```
SDK 标准编译（debug defconfig）产出的 bin 烧出 `Uncompress Ok!`，uboot 起来——是强线索。但用户手动换"别的 bin"也启动了 uboot（非我们生成的 SDK bin），**0x81 根因未 100% 确证**，defconfig 差异是定位方向而非已确证的唯一根因。保留"待确认"判断。

**教训**：
- ① **同一 SDK 版本标准编译应一致**——编出的 boot_image 应与 SDK 标准一致（大小/md5）。不一致说明构建流程错了，回溯构建流程别在二进制位级 debug。（专家结论，是定位方向）
- ② **裸烧/下载模式该用 debug defconfig**——`hi3516cv610_debug_defconfig`（`DEBUG=1`）；非 debug defconfig 含 `CONFIG_BSP_DISABLE_DOWNLOAD=y` 生产标志，不适合裸烧。（0x81 的强线索，但未 100% 确证——见上"未确证点"）
- ③ **加打印改 stub 布局会导致 GZIP IP 挂死**——打印放 `hw_dec_decompress` 返回后的 fail 分支内，不能在 ret-check 前无条件运行。
- ④ **NDA 寄存器（err_info）查不到含义时，走"标准产物对比"定位**——别死磕寄存器位域，走 SDK 标准编译对比大小/md5。
- ⑤ **服务器 SDK 片段不全 → 补齐完整参考仓跑标准 build.sh**（gitcode 克隆 + submodule），不要手工拼 input 绕过标准 `gslboot_build`。
- ⑥ **命名陷阱**：`u-boot-original.bin` 名字误导（"original"像未压缩 u-boot.bin，实际要 hw_comp stub = `u-boot-hi3516cv610.bin` @0x41700000，≠ `u-boot.bin`）。已固化到 `ohos-ci-lite-deploy-burn` skill 的 input 来源映射。
- ⑦ **强线索 ≠ 确证根因**——SDK 标准编译烧出 `Uncompress Ok!` 是强线索，但用户手动换别的 bin 也启动了，未做严格对照实验确证 defconfig 是唯一根因。诊断结论要区分"已确证"vs"强线索/定位方向"，别把线索写成定论。

> 相关：BG001（GSL 文件误用）是同一裸烧诊断的前序子问题（GSL→uboot code→-10B reg_info→0x81），各自解决=有进展，0x81 卡住多轮=同一问题无进展（触发 N 轮暂停机制，见 `skills/ohos-issue-lite-diagnose/SKILL.md` §N 轮无进展暂停机制）。0x81 最终靠用户手动换 bin 绕过，根因未确证——是 N 轮暂停后用户介入的典型场景。

### 案例BG003：Hi3516CV610 板载 SPI Nand 颗粒不在 ID 表 → uboot `pagesize 8192` BUG / 内核 `bsp_spi_nand_probe error -19`（两侧独立 ID 表）

**现象**：hi3516cv610 DMEB 板载 SPI Nand 颗粒 DS35Q1GB-IB（read id = `0xe5,0xf1`），uboot 与内核两侧表现不同：
- **uboot 侧**：`spi_nand_get_flash_info` 查 ID 表返回 NULL → 回退通用 NAND ID 表误算 pagesize=8192 → `fmc100.c:838 BUG: Driver does not support pagesize 8192`（颗粒实际 2KB page / 128B OOB）。
- **内核侧**：ID 表查不到该颗粒 → `cannot found in spi nand id table` → `bsp_spi_nand_probe error -19` (-ENODEV) → UBI 挂不上 / rootfs 起不来。

**根因**：板载 SPI Nand 颗粒 DS35Q1GB-IB 的 ID（`0xe5,0xf1`）不在海思 SPI Nand ID 表 `fmc_spi_nand_flash_table[]`（表里只有 HY035 `0xe5,0xf2` + HY073 等条目，没有 `0xe5,0xf1`）。颗粒不在表 → uboot 侧回退通用表误算 pagesize / 内核侧直接 probe 失败。

**⚠️ 关键：uboot 与内核是两份独立的 SPI Nand ID 表**：
- uboot 侧：`drivers/mtd/nand/raw/fmc100/fmc_ids_hi3516cv610.c`
- 内核侧：`drivers/mtd/nand/fmc100/fmc_ids_hi3516cv610.c`
两者路径只差一层（`raw/` vs 无），但是**两份独立的源文件**。补颗粒必须**两侧都补**——只补 uboot 侧则 uboot 识别但内核 probe -19 失败；只补内核侧则内核通但 uboot 报 pagesize 8192 BUG。

**诊断过程**：
1. 看报错字面：`pagesize 8192` / `cannot found in spi nand id table` / `bsp_spi_nand_probe error -19` → 倾向 SPI Nand ID 表问题（报错字面提到 id table / probe 失败）。
2. 抓颗粒 ID：uboot 启动早期 `spi nand id: 0xe5 0xf1` 或读 JEDEC ID（`0xe5`=厂商前缀，`0xf1`=颗粒型号）。
3. 查 ID 表：grep `0xe5` 在 `fmc_ids_hi3516cv610.c`（两侧都查），发现只有 `0xe5,0xf2`（HY035）+ `0xe5,0x73`（HY073），没有 `0xe5,0xf1`。
4. 确认颗粒不在表 → 对照同表同规格条目（同 `0xe5` 厂商前缀的 HY035，2KB page/128B OOB）→ 照抄改 id 即可补条目。
5. **两侧都补**（uboot `raw/fmc100/` + 内核 `fmc100/`），重编 uboot + 内核。

**修复方案**（两侧都补，照抄同规格条目改 id）：
```c
// uboot: drivers/mtd/nand/raw/fmc100/fmc_ids_hi3516cv610.c
// 内核: drivers/mtd/nand/fmc100/fmc_ids_hi3516cv610.c
// 在 fmc_spi_nand_flash_table[] 中照抄同 0xe5 厂商前缀的 HY035 条目，
// 把 id 改成 DS35Q1GB-IB 的 0xe5,0xf1，其余参数（pagesize 2048 / oob 128 等）与颗粒规格书对齐：
{
    .name       = "DS35Q1GB-IB",
    .id_data    = {0xe5, 0xf1},       /* ← 改这里：原 HY035 是 0xe5,0xf2 */
    .chipsize   = SZ_128M,            /* 按颗粒规格书填 */
    .pagesize   = SZ_2K,              /* 2KB，不是误算的 8192 */
    .oobsize    = 128,                /* 128B OOB */
    /* ... 其余字段照抄 HY035 条目，按 DS35Q1GB-IB 规格书核对 */
},
```
重编 uboot（`make ... gslboot_build`）+ 内核（`./build.sh ...`），重烧。

**教训**：
- ① **报错字面提到 id table / probe 失败 / pagesize 异常 → 优先查 SPI Nand/NOR ID 表有没有板载颗粒**（颗粒 ID 不在表是常见根因）。颗粒 ID 抓法：uboot 启动早期打印 / 读 JEDEC ID。
- ② **uboot 与内核的 SPI Nand ID 表是两份独立的源文件**（`raw/fmc100/` vs `fmc100/`，路径差一层），补颗粒**两侧都要补**，否则一侧识别另一侧 probe 失败。
- ③ **补条目照抄同表同规格条目改 id**——找同厂商前缀（如 `0xe5`）、同 pagesize/OOB 的现有条目复制，只改 id + name，参数按颗粒规格书核对。别从零写条目（字段多易错）。
- ④ **pagesize 8192 BUG 是 ID 表查不到回退通用表误算的典型症状**——8192 不是颗粒真实 pagesize，是回退路径默认值。看到 `Driver does not support pagesize 8192` 别去改驱动支持 8192，先查颗粒 ID 在不在表。
- ⑤ **关联诊断手段**：先联网搜"报错原文 + 芯片/SDK"看别人遇到过吗（见 `skills/ohos-issue-lite-diagnose/SKILL.md` §诊断先联网搜），再查参考仓源码 + 加打印验证。

---

## 9. OHOS init/服务启动阶段案例（实测 Hi3516CV610 实战）

> 芯片适配过烧录/内核启动关后，会卡在 OHOS init（samgr/foundation/各 service 启动）。这类问题报错日志在 user 态而非内核，常表现为 service 反复重启 + `samgr` boot step 超时。以下案例来自 hi3516cv610 小型系统（L1）rootfs 起来后的 init 阶段。

### 案例OH001：Hi3516CV610 binder ioctl `c0186201 returned -22 EINVAL` ×400 → samgr `Goto next boot step return code:-9`（内核 binder.h 缺 BINDER_IPC_32BIT）

**现象**：rootfs 起来，内核 boot 完进 OHOS init，串口狂刷：
```
binder: 83: 83 ioctl c0186201 returned -22       ← -EINVAL，~400 次
binder: 84: 84 ioctl c0186201 returned -22
...
samgr: Goto next boot step return code:-9         ← samgr 走不到下一步，启动卡死
```
各 service（foundation/appspawn/各 sa）起不来，反复重启。

**诊断过程**：
1. 报错字面 `ioctl c0186201 returned -22`：`c0186201` 是 binder ioctl 命令码（`BINDER_WRITE_READ`），`-22` = `-EINVAL`。binder ioctl 拒绝请求 = binder 协议层参数校验失败。
2. **先联网搜**"binder ioctl returned -22 EINVAL openharmony" → 命中社区线索：内核 binder 驱动与 user 态 binder 库的**数据结构体大小不一致**会导致 `BINDER_WRITE_READ` 校验失败返回 -EINVAL。根因是 32 位 vs 64 位 binder 协议位宽错配。
3. 查参考仓源码确认：Hi3516CV610 是 32 位 ARM（`arm-linux-ohos`，user 态 binder 库按 32 位 binder 协议编译，结构体 24B）；而内核 binder.h 默认走 64 位协议（结构体 48B），`BINDER_IPC_32BIT` 宏未定义 → `ioctl(BINDER_WRITE_READ)` 时内核按 64 位结构体拷贝，与 user 态 32 位结构体大小不匹配 → `-EINVAL`。
4. 对照 OHOS 官方 hispark_taurus_cv610_small.patch（hi3516dv300 同系 CV610 小型系统参考适配）：patch 第 9 行明示内核 binder.h 需加 `#define BINDER_IPC_32BIT 1` 对齐 32 位协议。hi3516cv610 内核漏打这一行 → 错配。

**根因**：内核 `drivers/android/binder.h`（或对应 vendor binder 头）缺 `#define BINDER_IPC_32BIT 1`，导致内核 binder 驱动用 64 位协议（48B 结构体），与 OHOS 32 位 user 态 binder 库（24B 结构体）不匹配，`BINDER_WRITE_READ` ioctl 校验失败返回 `-EINVAL`（-22），samgr 与各 service 无法完成 binder 通信 → `Goto next boot step return code:-9` 卡死。

**修复方案**：内核 binder.h 加一行对齐 32 位协议（对齐 OHOS hispark_taurus_cv610_small.patch:9）：
```c
// drivers/android/binder.h（或 vendor binder 头，按实际路径）
#ifndef BINDER_IPC_32BIT
#define BINDER_IPC_32BIT 1        /* ← 加这一行：32 位 ARM 对齐 OHOS user 态 binder 库 */
#endif
```
重编内核，重烧 kernel 分区，OHOS init 起来 binder ioctl 不再 -22，samgr 走到下一步。

**教训**：
- ① **binder ioctl returned -22 EINVAL + samgr boot step 卡死 → 优先怀疑内核/user 态 binder 协议位宽错配**（32 位 vs 64 位结构体大小不一致）。报错字面提到 binder ioctl + samgr 走不下去是典型症状。
- ② **同 SoC 系列参考适配的 patch 是权威**——hi3516cv610 与 hispark_taurus_cv610 同系（CV610 小型系统），官方 patch（如 `BINDER_IPC_32BIT` 一行）直接照打。别从零排查 binder 协议位宽。
- ③ **`-22` = `-EINVAL` 是协议/参数校验失败通用码**——ioctl 返回 -22 常是结构体大小/字段错配，不是简单的权限/路径问题。对照 user 态与内核两侧同名结构体的 sizeof。
- ④ **关联诊断手段**：先联网搜"报错原文 + openharmony"，再查参考仓 patch 源码确认（hispark_taurus_cv610_small.patch:9）。

### 案例OH002：Hi3516CV610 HUKS `ActsHuksLiteFunctionTest` 0/40 → GetFeatureApi 9s 重试返回 -2（samgr_lite `GetTaskConfig` SINGLE_TASK 异步排队无消费者，DEFAULT_Initialize 永不执行）

> **实测收尾确认根因（huksfix14 实测闭环）**。14 轮 huksfix 才定位，命门是"注册 OK 但不分发"。

**现象**：rootfs 起来，OHOS init 进到 samgr，HUKS 测试 `ActsHuksLiteFunctionTest` 0/40 全 fail。客户端日志：
```
GetFeatureApi retry ... (重试约 9 秒)
GetFeatureApi return -2        ← -2 = 超时，等不到 HUKS feature 发布
```
服务端 `huks_server` 进程在，但 `huks_server` 从未走到 `OP_PUT`（feature 发布操作）。

**诊断过程（14 轮 huksfix 调试链）**：
1. **huksfix1-3 retry patch 证伪**：参考某 retry patch（c575897d）加客户端重试，以为能解决超时——证伪，仍 0/40，retry 只是多等 9 秒还是 -2。根因不在客户端重试。
2. **huksfix4-7 NO_TASK 同步分发假设**：查 samgr_lite 源码，发现 `huks_server` 服务的 `GetTaskConfig` 用 `SINGLE_TASK`（异步排队模式）。假设：消息进队列但无消费者线程 dispatch → `DEFAULT_Initialize` 永不执行 → feature 永不发布。改 `taskFlags` 从 `SINGLE_TASK` 到 `NO_TASK`（同步分发，注册时立即执行）。
3. **huksfix8 验证 NO_TASK**：改 NO_TASK 后 `huks_server` 走到 `DEFAULT_Initialize` → feature 发布 → 客户端 `GetFeatureApi` 成功 → `ActsHuksLiteFunctionTest` 40/40 全过。**NO_TASK 同步分发是真根因**。
4. **huksfix9-13 engine .so + uid 连环**：NO_TASK 修了分发但还有残留——engine `.so` 没打进 rootfs/lib（-14→-31）+ huks/foundation uid 非 root 导致 `SCHED_RR` 失败（见 OH003/OH004）。逐个修。
5. **huksfix14 收尾确证**：foundation uid 0 → `BINDER_SET_CONTEXT_MGR ret=0` → samgr 就绪 → HUKS 发布 → XTS 426/426（HUKS 40/40 + deviceattest 3/3）。残留 EACCES 来自非 root SA 良性（见 OH005）。

**根因**：samgr_lite `GetTaskConfig` 用 `SINGLE_TASK`（异步排队模式），消息进队列但无消费者线程 dispatch → `DEFAULT_Initialize` 永不执行 → HUKS feature 永不发布 → 客户端 `GetFeatureApi` 重试 9s 超时返回 -2。改 `NO_TASK`（同步分发，注册时立即执行初始化和分发）后 `DEFAULT_Initialize` 执行 → feature 发布 → 客户端拿到 feature。

**修复方案**（OH samgr_lite 源码）：
- `GetTaskConfig` 的 `taskFlags`：`SINGLE_TASK` → `NO_TASK`(0xFF)
- `AddTaskPool` 的 `NO_TASK` case：走同步分发路径
- 构造器 `Init()` 只注册不做重活（重活放 `DEFAULT_Initialize`，由同步分发触发）

**收尾结论（huksfix14 确证 + 残留良性）**：
- foundation uid 0 → `BINDER_SET_CONTEXT_MGR ret=0` → samgr 就绪 → HUKS 发布（实测闭环）
- 残留 `OpenDriver EACCES errno=13` 来自非 root SA（appspawn/bundle_daemon），这些 SA 不需要 context mgr，重试成功 → 良性
- `-32` spam 15 行瞬时自愈 → 良性
- 4 次启动不重启 → 良性
- XTS 426/426（HUKS 40/40 + deviceattest 3/3）→ 判良性，残留可接受（见 ohos-issue-lite-diagnose Step 2.4）

**教训**：
- ① **注册 OK 但不分发是命门**——`huks_server` 进程在、注册链路全 OK，但 `DEFAULT_Initialize` 从未执行（任务没 dispatch）。14 轮才定位就是因为早期盯着注册链/客户端重试，没查任务分发配置。
- ② **GetFeatureApi 超时返回 -2 + 服务端进程在 → 查服务端任务分发配置**（`GetTaskConfig` 是同步还是异步排队无消费者）。
- ③ **retry patch 是症状治疗不是根因修复**——加客户端重试只是多等，服务端不分发还是 -2。别把 retry 当根因修。
- ④ **关联**：通用模式见 `references/fault-knowledge-base.md` §7.4（服务注册 OK 但不分发）。memory `samgr-lite-no-task-sync-dispatch`、`huks-server-samgr-publish-path`、`huks-samgr-publish-chain`、`huks-minus2-rootcause`。

### 案例OH003：Hi3516CV610 HUKS -14 → -31（engine .so 缺失，没打进 rootfs/lib）

**现象**：NO_TASK 修了分发后，HUKS 测试从 -2（超时）变成 -14，再变成 -31。

**根因**：HUKS 的 engine `.so`（加密引擎库）没打进 rootfs/lib。huks_server 起来后 dlopen/链接 engine .so 失败 → 返回 -14（某阶段）→ 进一步缺符号返回 -31。

**修复方案**：把 HUKS engine `.so` 从 OH `out/{product}/` 拷进 rootfs/lib，跑 B11 依赖闭包校验确认无 missing。

**教训**：
- ① **HUKS -14/-31 常是 engine .so 缺失**——不是协议错，是 rootfs 没放全 .so。查 rootfs/lib 有无 huks engine 相关 .so。
- ② **关联**：见 `04-build-verify` Step 4.7 B11 烧前依赖闭包校验（readelf -d 递归查 NEEDED）——engine .so 缺失本该在烧前被 B11 抓住。

### 案例OH004：Hi3516CV610 HUKS uid 非 root 导致 SCHED_RR 失败（huks uid 12→0、foundation uid 7→0）

**现象**：engine .so 补齐后 HUKS 还是不发布。服务端日志：`SCHED_RR` 设置失败 `EPERM`。

**根因**：`SCHED_RR`（实时调度策略）需要 root 或 `CAP_SYS_NICE` 能力。huks_server uid=12、foundation uid=7（非 root）→ `sched_setscheduler(SCHED_RR)` 返回 `EPERM` → boss 线程起不来 → 无 `Receive` 线程消费消息 → feature 不发布。

**修复方案**：init.cfg 把 `huks_server` uid 改 0、`foundation` uid 改 0（核心 SA 需 root 才能 `SCHED_RR` + `BINDER_SET_CONTEXT_MGR`）。

**教训**：
- ① **核心 SA 的 uid 要 root（0）**——huks_server/foundation 这类需要 `SCHED_RR` + `BINDER_SET_CONTEXT_MGR` 的 SA，uid 非 root → `EPERM` → 起不来。
- ② **`SCHED_RR EPERM` → 查 uid 是不是 root / 有没有 CAP_SYS_NICE**，不是查调度策略本身。
- ③ **关联**：见 `skills/ohos-ci-lite-deploy-burn/references/l1-init-cfg-reference.md`（uid 稳态值表）。

### 案例OH005：Hi3516CV610 binder `OpenDriver EACCES errno=13` 1st boot（ueventd chmod /dev/binder 与 foundation open 时序竞争 → init.cfg pre-init 显式 chmod 0666）

**现象**：1st boot 串口日志：
```
binder: 83: 83 OpenDriver EACCES errno=13         ← open /dev/binder 权限失败
binder: BINDER_SET_CONTEXT_MGR failed             ← context mgr 起不来
... OP_POST retry storm ... -32 spam ×15 ...      ← 连锁：context mgr 没有 → OP_POST 重试风暴
watchdog reset                                    ← 最终看门狗复位
```

**根因**：`/dev/binder` 的权限由 ueventd 在收到 binder 设备 uevent 时 `chmod 0666`，但 ueventd 的 chmod 与 foundation 启动 open /dev/binder 存在**时序竞争**——foundation 起来时 ueventd 还没 chmod 完 → foundation open `/dev/binder` → `EACCES`（默认权限不允许非 root open）→ `BINDER_SET_CONTEXT_MGR` 失败 → context mgr 没有 → 其他 SA 的 OP_POST 重试风暴 → -32 spam → 看门狗复位。

**修复方案**：init.cfg pre-init job 显式 `chmod 0666 /dev/binder`，**在 foundation start 前执行**（见 `04-build-verify` B6.1 时序约束）。这样 foundation 起来时 `/dev/binder` 权限已就绪，不依赖 ueventd 的异步 chmod。

**收尾结论（huksfix14 确证 + 残留良性）**：
- huksfix14：foundation uid 0 + init.cfg pre-init chmod 0666 /dev/binder → foundation `BINDER_SET_CONTEXT_MGR ret=0` 一次成功
- 残留 `OpenDriver EACCES errno=13` 来自非 root SA（appspawn/bundle_daemon），这些 SA 不需要 context mgr，重试成功 → 良性（见 ohos-issue-lite-diagnose Step 2.4 判据）
- XTS 426/426，4 boot 不重启 → 残留可接受

**教训**：
- ① **binder EACCES + BINDER_SET_CONTEXT_MGR failed → 查 /dev/binder 权限 + foundation uid**。权限不足或 uid 非 root 都会导致 context mgr 起不来。
- ② **ueventd 异步 chmod 有时序竞争**——别依赖 ueventd 给 /dev/binder 设权限，init.cfg pre-init 显式 chmod 更可靠（在 service start 前同步执行）。
- ③ **context mgr 起不来会连锁**——OP_POST retry storm + -32 spam + 看门狗复位，根因都是 context mgr 没有，别盯着 -32 spam 查。
- ④ **残留 EACCES 来自非 root SA 是良性的**——这些 SA 不需要 context mgr，重试成功。别当 bug 死磕（见 ohos-issue-lite-diagnose Step 2.4）。
