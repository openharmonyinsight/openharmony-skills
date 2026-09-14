# L1 设备配置实战模式（hi3516cv610 手工产物提炼）

> 来源：Hi3516CV610 DEMB L1 小型系统适配手工产物
> 用途：给 ohos-dev-board-config-gen 单点调用提供实战验证的 config.gni/soc.gni/defconfig/DTS/HCS 生成模式

---

## 一、config.gni（板级编译配置）

实测 hi3516cv610 实战样本（`device/board/hisilicon/hispark_dmeb/linux/config.gni`）：

```gni
# Kernel type, e.g. "linux", "liteos_a", "liteos_m".
kernel_type = "linux"
kernel_version = "5.10"

# Board CPU type.
board_cpu = "cortex-a7"
board_arch = ""

# Toolchain: cv610 uses GCC (openeuler musl ARM32) not clang.
board_toolchain = "arm-openeuler-linux-musleabi-gcc"
board_toolchain_path = "<TOOLCHAIN_ROOT>/bin"  # 实际路径从 workflow_config.yaml.toolchain.path 取
board_toolchain_prefix = "arm-openeuler-linux-musleabi-"
board_toolchain_type = "gcc"

# Board related common compile flags.
board_cflags = [
  "-mfloat-abi=softfp",
  "-mfpu=neon-vfpv4",
]
board_cxx_flags = [
  "-mfloat-abi=softfp",
  "-mfpu=neon-vfpv4",
]
board_ld_flags = []
board_include_dirs = []

# Board adapter dir for OHOS components (shared common hal).
board_adapter_dir = "//device/soc/hisilicon/common/hal"
board_configed_sysroot = ""

# Board storage type: SPI Nand (briefing-confirmed).
storage_type = "spi_nand"
```

**要点**：
- `kernel_type = "linux"`（L1 可用 linux 或 liteos_a；hi3516cv610 走 linux 5.10）
- `board_toolchain_type = "gcc"`（非 clang，hi3516cv610 用 openeuler GCC 12.3.1）
- `board_cflags` 的 `-mfloat-abi`/`-mfpu` 要与 defconfig 的 `CONFIG_VFP`/`CONFIG_NEON` 方向一致（官方 defconfig 用 hard + VFP/NEON，则 cflags 应 `-mfloat-abi=hard`；若用 softfp 则 defconfig 侧也要协调）
- `board_adapter_dir` 指向公共 HAL（`device/soc/hisilicon/common/hal`，多芯片共享）
- `storage_type` 决定启动介质（spi_nand/emmc/spi_nor），影响 defconfig 的 MTD/MMC 配置

---

## 二、soc.gni（SoC 级配置）

实测样本（`device/soc/hisilicon/hi3516cv610/soc.gni`）+ 实测补全版：

```gni
# ---- SoC 标识（来自 SDK autoconf.h） ----
soc_company = "hisilicon"
soc_name = "hi3516cv610"
chip_type = 0x3516c610          # CONFIG_OT_CHIP_TYPE（全小写，别写 0x3516CV610）
arch_type = "smp"               # CONFIG_ARM_ARCH_TYPE
cpu_type = "a7"                 # CONFIG_CPU_TYPE
sub_arch = "hi3516cv610"        # CONFIG_OT_SUBARCH

# ---- 内核 ----
kernel_type = "linux"
kernel_version = "linux-5.10.y" # CONFIG_KERNEL_VERSION
libc_type = "musl"              # CONFIG_LIBC_TYPE
kernel_bit = "KERNEL_BIT_32"    # CONFIG_KERNEL_BIT

# ---- 工具链（来自 autoconf.h CONFIG_OT_CROSS） ----
soc_toolchain = "arm-openeuler-linux-musleabi-gcc"
soc_toolchain_prefix = "arm-openeuler-linux-musleabi-"
soc_toolchain_type = "gcc"
cross_compile = "arm-openeuler-linux-musleabi-"

# ---- SoC 编译选项 ----
soc_cflags = [
  "-mcpu=cortex-a7",
  "-mfloat-abi=softfp",
  "-mfpu=neon-vfpv4",
  "-marm",
  "-mno-unaligned-access",
]
soc_cxx_flags = soc_cflags
soc_ld_flags = []

# ---- SDK 头文件路径 ----
soc_include_dirs = [
  "//device/soc/hisilicon/hi3516cv610/sdk_linux/include",
  "//device/soc/hisilicon/hi3516cv610/sdk_linux/include/ot",
]

# ---- 驱动空间类型 ----
driver_space_type = "user_space"   # CONFIG_DRIVER_SPACE_TYPE

# ---- 平台/板级路径 ----
sdk_platform_dir = "//device/soc/hisilicon/hi3516cv610/sdk_linux"

# ---- 安全子系统（autoconf.h CONFIG_OT_SECURITY_SUBSYS_SUPPORT 等） ----
security_subsys_support = true
cipher_support = true
km_support = true
otp_support = true
trng_support = true

# ---- 媒体子系统（autoconf.h 大量 CONFIG_OT_*） ----
media_audio_support = true
media_video_input_support = true
media_video_process_support = true
media_video_encode_support = true
media_isp_support = true
media_mipirx_support = true
media_svp_support = true
uvc_support = true
```

**要点**：
- `chip_type` 必须**全小写十六进制**（`0x3516c610`），大写 `V` 非法致 C 编译错误（实测翻车点）
- 字段值来自 SDK `autoconf.h`/`cfg.mak`，别凭记忆编
- `soc_cflags` 与 config.gni `board_cflags` 要一致（三处一致：config.gni + soc.gni + defconfig）
- 媒体/安全开关来自 `autoconf.h` 的 `CONFIG_OT_*` 系列，逐个对应

### device.gni（板级入口，import soc.gni）

```gni
soc_company = "hisilicon"
soc_name = "hi3516cv610"
import("//device/soc/${soc_company}/${soc_name}/soc.gni")

if (!defined(defines)) {
  defines = []
}
product_config_path = "//vendor/hisilicon/${product_name}"
# Headless board (no display/camera/audio).
is_support_mpi = false
is_support_v4l2 = false
```

---

## 三、defconfig（内核配置 + 核依赖链）

### 3.1 核依赖链必检项（实测翻车根因）

生成 defconfig 时必须对照官方 `arch/arm/configs/<chip>_defconfig` 金标准，逐条核对每个 `CONFIG_XXX=y` 的 `depends on` 链。

**实测翻车的依赖断裂**：

| 生成的 CONFIG | 缺的依赖 | 后果 | 修复 |
|--------------|---------|------|------|
| `MTD_SPI_NAND_FMC100=y` | `MFD_BSP_FMC=y`（Kconfig: `depends on MFD_BSP_FMC && MTD_SPI_NAND_BSP`） | SPI Nand 走不到编译分支，探测失败 | 补 `CONFIG_MFD_BSP_FMC=y` + `CONFIG_MFD_SYSCON=y` |
| `BSP_TIMER=y` | `CONFIG_PM=y`（Kconfig: `depends on PM`） | BSP_TIMER 不生效 | 删 BSP_TIMER 或补 `CONFIG_PM=y` |
| `UBIFS_FS=y` | `MTD_UBI=y`（UBIFS 依赖 UBI） | UBIFS 无法挂载 | 补 `CONFIG_MTD_UBI=y` |

**实测中漏的官方 defconfig 必备项**：

| 漏项 | 影响 | 官方值 |
|------|------|--------|
| `POWER_RESET_BSP` | 无法 reboot | `=y` |
| `ARM_APPENDED_DTB` / `ARM_ATAG_DTB_COMPAT` | 启动可能找不到 DTB | `=y` |
| `VFP` / `NEON` | FPU 未使能 | `=y`（官方用 hard float） |
| `MTD_SPI_NOR` | SPI Nor 不工作 | `=y`（官方与 SPI_BSP_SFC 都开） |
| `MTD_UBI` | UBIFS 依赖 | `=y` |

**实测 CONFIG 选错**：
- `EDMAC=y` 应为 `EDMACV310=y`（DTS `compatible="vendor,edmacv310"` 对应 EDMACV310，二者互斥 `depends on !EDMACV310`）

### 3.2 实测修正后的 defconfig 模式（贴近官方金标准）

实测改用 mainline Hisi CONFIG 名 + 补齐依赖，关键段：

```ini
# ---- ARM 架构 / Cortex-A7 SMP ----
CONFIG_ARM=y
CONFIG_ARCH_MULTI_V7=y
CONFIG_CPU_V7=y
CONFIG_SMP=y
CONFIG_NR_CPUS=2
CONFIG_HAVE_ARM_ARCH_TIMER=y
CONFIG_ARM_ARCH_TIMER=y
CONFIG_VFP=y              # ← 早期漏配，实测补全
CONFIG_VFPv3=y
CONFIG_NEON=y             # ← 早期漏配，实测补全
# CONFIG_THUMB2_KERNEL is not set   # ← 明确 n，官方用 y，按实际工具链选

# ---- Hisilicon 平台 ----
CONFIG_ARCH_HISI=y
CONFIG_ARCH_HI3516CV610=y
CONFIG_HISILICON_IRQ_MBIGEN=y
CONFIG_RESET_CONTROLLER=y
CONFIG_HISILICON_RESET=y
CONFIG_MFD_SYSCON=y       # ← 实测中漏 MFD_BSP_FMC，实测补 MFD_SYSCON

# ---- DMA ----
CONFIG_DMADEVICES=y
CONFIG_HISILICON_EDMACV310=y   # ← 实测中选错 EDMAC，实测改 EDMACV310

# ---- MTD / FMC（依赖链完整） ----
CONFIG_MTD=y
CONFIG_MTD_BLOCK=y
CONFIG_MTD_SPI_NOR=y           # ← 早期漏配，实测补全
CONFIG_MTD_SPI_NAND=y
CONFIG_SPI_HISI_SFC=y
CONFIG_MTD_HISI_FMC=y          # ← 依赖 MFD_SYSCON，已补

# ---- 电源管理（BSP_TIMER 依赖） ----
CONFIG_PM=y                    # ← 早期漏配，实测补全
CONFIG_PM_SLEEP=y
CONFIG_PM_SLEEP_SMP=y

# ---- 重启/关机 ----
CONFIG_POWER_RESET=y           # ← 早期漏配，实测补全
CONFIG_POWER_RESET_HISI=y

# ---- Watchdog ----
CONFIG_WATCHDOG=y
CONFIG_HISI_WATCHDOG=y

# ---- 文件系统（UBIFS 依赖链完整） ----
CONFIG_UBIFS_FS=y
CONFIG_MTD_UBI=y               # ← 早期漏配，实测补全

# ---- OpenHarmony L1 必需 ----
CONFIG_ANDROID=y
CONFIG_ANDROID_BINDER_IPC=y
CONFIG_ANDROID_BINDERFS=y
CONFIG_ANDROID_BINDER_DEVICES="binder,hwbinder,vndbinder"
CONFIG_DEVTMPFS=y
CONFIG_DEVTMPFS_MOUNT=y
CONFIG_SECURITY=y
CONFIG_SECURITY_SELINUX=y
```

**defconfig 生成检查清单**：
1. 每个 `CONFIG_XXX=y` 的 `depends on` 链全部满足（查 `drivers/**/Kconfig`）
2. 对照官方 `arch/arm/configs/<chip>_defconfig` 逐条核对，偏离项标注原因
3. `CONFIG_XXX` 值合法（bool: y/n/m；hex: 合法十六进制全小写；string: 加引号）
4. OH L1 必需项不漏（binder/hilog/cgroup/devtmpfs/selinux）
5. 启动相关项不漏（POWER_RESET/ARM_APPENDED_DTB/ARM_ATAG_DTB_COMPAT）

---

## 四、DTS（设备树）

实测 hi3516cv610 DTS 关键节点模式（来自 `hi3516cv610-open.dtsi` + `hi3516cv610-demb.dts`）：

```dts
/ {
    memory {
        reg = <0x40000000 0x08000000>;   /* 128MB DDR */
    };

    cpus {
        #address-cells = <1>;
        #size-cells = <0>;
        cpu@0 { device_type = "cpu"; compatible = "arm,cortex-a7"; reg = <0>; };
        cpu@1 { device_type = "cpu"; compatible = "arm,cortex-a7"; reg = <1>; };
    };

    gic: interrupt-controller@12400000 {
        compatible = "arm,cortex-a7-gic";
        #interrupt-cells = <3>;
        #address-cells = <0>;
        interrupt-controller;
        reg = <0x12401000 0x1000>, <0x12402000 0x2000>;
    };

    timer { /* armv7-timer PPI */
        compatible = "arm,armv7-timer";
        interrupts = <1 13 0xf08>;   /* PPI 13，首字段=1 */
    };

    uart0: uart@0x11040000 {   /* PL011 */
        compatible = "arm,primecell";
        reg = <0x11040000 0x1000>;
        interrupts = <0 10 4>;      /* GIC SPI 10，首字段=0 */
    };

    gpio_chip0: gpio_chip@11090000 {   /* PL061 */
        compatible = "arm,pl061";
        reg = <0x11090000 0x1000>;
        interrupts = <0 23 4>;      /* GIC SPI 23 → Linux IRQ 55（+32） */
        #gpio-cells = <2>;
    };

    wdg: wdg@0x11030000 {
        compatible = "vendor,wdg";
        reg = <0x11030000 0x1000>;
        interrupts = <0 3 4>;
    };

    i2c_bus0: i2c_bus@0x11060000 {
        compatible = "vendor,i2c";
        reg = <0x11060000 0x1000>;
        /* 无 interrupts 属性 → 轮询模式 */
        clock-frequency = <400000>;
    };
};
```

**DTS 生成要点**：
- `interrupts` 三元组：`<SPI/PPI 编号 触发类型>`，首字段 0=SPI，1=PPI
- HCS 的 `irqStart`/`irqNum` 是 **Linux IRQ 号**（SPI+32），不是 DTS 原始 SPI 号
- `compatible` 字符串决定走哪个内核驱动（`arm,pl061` → pl061 驱动；`vendor,i2c` → 厂商 i2c-bsp 驱动）
- I2C 轮询模式：DTS 不写 `interrupts`，HCS `irqNum=0`
- `reg` 地址与 HCS `regBase`/`regPbase` 一致

---

## 五、HCS（device_info.hcs + *_config.hcs）

### 5.1 device_info.hcs（实测案例，含 linux_*_adapter 并存）

```hcs
root {
    device_info {
        match_attr = "hdf_manager";
        template host {
            hostName = "";
            priority = 100;
            template device {
                template deviceNode {
                    policy = 0;
                    priority = 100;
                    preload = 0;
                    permission = 0664;
                    moduleName = "";
                    serviceName = "";
                    deviceMatchAttr = "";
                }
            }
        }
        platform :: host {
            hostName = "platform_host";
            priority = 50;

            device_gpio :: device {
                device0 :: deviceNode {
                    policy = 2;
                    priority = 10;
                    permission = 0644;
                    moduleName = "HDF_PLATFORM_GPIO_MANAGER";
                    serviceName = "HDF_PLATFORM_GPIO_MANAGER";
                }
                device1 :: deviceNode {       /* linux_gpio_adapter 走内核 gpiolib */
                    policy = 0;
                    priority = 10;
                    permission = 0644;
                    moduleName = "linux_gpio_adapter";
                    deviceMatchAttr = "linux_gpio_adapter";
                }
            }

            device_watchdog :: device {
                device0 :: deviceNode {
                    policy = 2;
                    priority = 20;
                    permission = 0644;
                    moduleName = "HDF_PLATFORM_WATCHDOG";
                    serviceName = "HDF_PLATFORM_WATCHDOG_0";
                    deviceMatchAttr = "hisilicon_hi35xx_watchdog_0";
                }
            }

            device_uart :: device {
                device0 :: deviceNode {
                    policy = 1;
                    priority = 40;
                    permission = 0644;
                    moduleName = "HDF_PLATFORM_UART";
                    serviceName = "HDF_PLATFORM_UART_0";
                    deviceMatchAttr = "hisilicon_hi35xx_uart_0";
                }
            }

            device_i2c :: device {
                device0 :: deviceNode {
                    policy = 2;
                    priority = 50;
                    permission = 0644;
                    moduleName = "HDF_PLATFORM_I2C_MANAGER";
                    serviceName = "HDF_PLATFORM_I2C_MANAGER";
                    deviceMatchAttr = "hdf_platform_i2c_manager";
                }
                device1 :: deviceNode {       /* linux_i2c_adapter 走内核 i2c-dev */
                    policy = 0;
                    priority = 55;
                    permission = 0644;
                    moduleName = "linux_i2c_adapter";
                    deviceMatchAttr = "linux_i2c_adapter";
                }
            }
        }
    }
}
```

### 5.2 *_config.hcs（实测案例）

**gpio_config.hcs**（对应 linux_gpio_adapter）：
```hcs
root {
    platform {
        gpio_config {
            controller_0x120d0000 {
                match_attr = "linux_gpio_adapter";   /* ← 与 device_info.hcs device1 配对 */
                groupNum = 12;
                bitNum = 8;
                regBase = 0x120d0000;
                regStep = 0x1000;
                irqStart = 48;          /* Linux IRQ 号（SPI 16+32） */
                irqShare = 0;
            }
        }
    }
}
```

**uart_config.hcs**（多实例 + template 继承）：
```hcs
root {
    platform {
        template uart_controller {
            match_attr = "";
            num = 0;
            baudrate = 115200;
            fifoRxEn = 1;
            fifoTxEn = 1;
            flags = 4;
            regPbase = 0x120a0000;
            interrupt = 38;       /* Linux IRQ 号 */
            iomemCount = 0x48;
        }
        controller_0x120a0000 :: uart_controller {
            match_attr = "hisilicon_hi35xx_uart_0";
        }
        controller_0x120a1000 :: uart_controller {
            num = 1;
            baudrate = 9600;
            regPbase = 0x120a1000;
            interrupt = 39;
            match_attr = "hisilicon_hi35xx_uart_1";
        }
    }
}
```

**watchdog_config.hcs**：
```hcs
root {
    platform {
        template watchdog_controller {
            id = 0;
            match_attr = "";
            regBase = 0x12050000;
            regStep = 0x1000;
        }
        controller_0x12050000 :: watchdog_controller {
            match_attr = "hisilicon_hi35xx_watchdog_0";
        }
    }
}
```

### 5.3 hdf.hcs（顶层入口）

```hcs
#include "device_info/device_info.hcs"
#include "gpio/gpio_config.hcs"
#include "uart/uart_config.hcs"
#include "i2c/i2c_config.hcs"
#include "spi/spi_config.hcs"
#include "pwm/pwm_config.hcs"
#include "adc/adc_config.hcs"
#include "watchdog/watchdog_config.hcs"
#include "rtc/rtc_config.hcs"
#include "mmc/mmc_config.hcs"
```

---

## 六、实测翻车根因（device-config 正确性缺口）

### 6.1 实测翻车点

| 翻车点 | 根因 | 修正 |
|--------|------|------|
| defconfig 依赖断裂 | 缺 `MFD_BSP_FMC` 致 `MTD_SPI_NAND_FMC100` 编译不进 | 补 `MFD_BSP_FMC=y` + `MFD_SYSCON=y` |
| BSP_TIMER 不生效 | 缺依赖 `CONFIG_PM=y` | 删 BSP_TIMER 或补 PM |
| 非法十六进制 | `0x3516CV610` 大写 V 非法致 C 编译错误 | 改 `0x3516c610` 全小写 |
| 无法 reboot | 缺 `POWER_RESET_BSP` | 补 `=y` |
| UBIFS 挂载失败 | 有 `UBIFS_FS` 无 `MTD_UBI` | 补 `MTD_UBI=y` |
| EDMAC 选错 | DTS compatible=edmacv310 应配 `EDMACV310` 非 `EDMAC` | 改 `EDMACV310=y` |
| 多项偏离官方 | 未对照官方 defconfig 金标准 | 逐条对照 `arch/arm/configs/hi3516cv610_defconfig` |

### 6.2 实测翻车点

| 翻车点 | 根因 | 修正 |
|--------|------|------|
| HCS 文件完全漏生成 | L1 产出只有 config.gni/soc.gni/defconfig/dts/target_config.h，无 HCS | L1 必生成 hdf.hcs + device_info.hcs + 各 *_config.hcs |

### 6.3 共性教训

- **defconfig 生成必须对照官方金标准**：只核 CONFIG 名存在于 Kconfig 不够，要核 `depends on` 链 + 对照官方 defconfig
- **L1 必生成 HCS**：config.gni/soc.gni/defconfig/DTS 是内核侧，HCS 是 HDF 框架侧——两套都要，漏 HCS 则 HDF 驱动无设备节点树
- **hex 值全小写**：`0x3516CV610` 的 V 非法，C 编译错误
