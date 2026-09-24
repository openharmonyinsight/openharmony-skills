# RTOS内核数据源：LiteOS-M / RT-Thread / NuttX / FreeRTOS / 厂商SDK

6/9颗典型MCU芯片没有MMU、RAM只有几百KB，跑不了Linux，运行在RTOS内核上。这些芯片的硬件信息（寄存器地址、中断号、时钟配置）需要从RTOS生态的驱动/适配代码中获取。**硬件规格与Linux驱动中的本质相同**，只是驱动框架和API不同。

| RTOS内核 | 芯片 | 代码仓库 |
|---------|------|---------|
| **LiteOS-M** (OpenHarmony) | Hi3861, BES2600W, XR806, ASR582X | openharmony/device_soc_* |
| **RT-Thread** | STM32F407, AT32F437, ESP32-C3 | RT-Thread/rt-thread |
| **NuttX** | AT32F437 | apache/nuttx |
| **FreeRTOS** (ESP-IDF) | ESP32-C3 | espressif/esp-idf |
| 厂商SDK (裸机) | AT32F437 | ArteryTek |

---

## OpenHarmony仓库

### 关键仓库

| 仓库 | 覆盖芯片 | 主仓地址 |
|------|---------|---------|
| `device_soc_hisilicon` | Hi3861, Hi3516DV300 | [gitcode.com/openharmony/device_soc_hisilicon](https://gitcode.com/openharmony/device_soc_hisilicon) |
| `device_soc_bestechnic` | BES2600W | [gitcode.com/openharmony/device_soc_bestechnic](https://gitcode.com/openharmony/device_soc_bestechnic) |
| `device_soc_esp` | ESP32-C3 | [gitcode.com/openharmony/device_soc_esp](https://gitcode.com/openharmony/device_soc_esp) |
| `device_soc_asrmicro` | ASR582X | [gitcode.com/openharmony/device_soc_asrmicro](https://gitcode.com/openharmony/device_soc_asrmicro) |

### 查找内容

- **SDK头文件**：寄存器定义（基地址、中断号）
- **HCS配置文件**：OpenHarmony的设备配置格式（等价于Linux DTS）
- **Kconfig文件**：内核配置，可揭示CPU类型、外设特性
- **Board config文件**：内存布局、链接脚本
- **驱动实现**：GPIO、UART、SPI等外设驱动代码

### 查询方法

```bash
# 优先用GitCode API（主仓，最新，免认证）

# 列目录（获取文件列表和SHA）
curl -s "https://api.gitcode.com/api/v5/repos/openharmony/device_soc_hisilicon/contents/hi3861v100/sdk_liteos/include?ref=master"

# 下载原始文件（需先从目录列表获取SHA）
curl -s "https://raw.gitcode.com/openharmony/device_soc_hisilicon/blobs/{sha}/hi3861v100/sdk_liteos/include/hi_gpio.h"

# 读单文件（返回JSON含base64编码的content字段，一步到位）
curl -s "https://api.gitcode.com/api/v5/repos/openharmony/device_soc_hisilicon/contents/hi3861v100/sdk_liteos/include/hi_gpio.h?ref=master"

# GitHub镜像（可能过期，作为备选）
curl -sL -H "Accept: application/vnd.github+json" \
  "https://api.github.com/search/code?q={chip_model}+org:openharmony"

# 搜索HCS配置文件（GitHub）
curl -sL -H "Accept: application/vnd.github+json" \
  "https://api.github.com/search/code?q={chip_model}+org:openharmony+extension:hcs"

# 搜索Kconfig（GitHub）
curl -sL -H "Accept: application/vnd.github+json" \
  "https://api.github.com/search/code?q={chip_model}+org:openharmony+filename:Kconfig"
```

### 注意事项

- OpenHarmony已迁移至 [GitCode](https://gitcode.com/openharmony)（2025年9月），Gitee仓已废弃。GitHub镜像可能过期，优先用GitCode
- HCS文件格式类似DTS但语法不同，解析时注意区分
- 部分芯片的SDK以二进制形式分发，源码可能不完整

---

## NuttX仓库

NuttX对部分MCU芯片（如AT32F437）有BSP支持，而这些芯片不在Linux主线中。

### 查询方法

```bash
# 搜索NuttX中芯片的BSP
curl -sL -H "Accept: application/vnd.github+json" \
  "https://api.github.com/search/code?q={chip_model}+repo:apache/nuttx+path:boards"

# 直接访问board support
curl -sL "https://raw.githubusercontent.com/apache/nuttx/master/boards/arm/at32/at32f437-mini/src/board.h"
```

### NuttX关键路径

| 路径模式 | 内容 |
|---------|------|
| `boards/<arch>/<vendor>/<board>/` | Board Support Package（板级支持） |
| `arch/<arch>/src/<chip>/` | 芯片级HAL驱动 |
| `include/nuttx/` | OS头文件（含外设接口定义） |

### 注意事项

- NuttX的BSP通常比Linux精简，但寄存器定义同样准确
- `arch/` 目录下的HAL代码可替代厂商SDK中的CMSIS/CMSIS-Driver
- 若NuttX也没有，说明该芯片生态较封闭，需转向厂商SDK

---

## RT-Thread

RT-Thread是国产开源RTOS，在国内MCU生态覆盖面广，BSP质量高。对STM32F407有8个开发板BSP，对AT32F437有完整板级支持。

### 查询方法

```bash
# 搜索RT-Thread中芯片的BSP
curl -sL -H "Accept: application/vnd.github+json" \
  "https://api.github.com/search/code?q={chip_model}+repo:RT-Thread/rt-thread+path:bsp"

# 直接访问板级头文件（AT32系列在board/inc/下，STM32系列在board/下）
curl -sL "https://raw.githubusercontent.com/RT-Thread/rt-thread/master/bsp/at32/at32f437-start/board/inc/board.h"
curl -sL "https://raw.githubusercontent.com/RT-Thread/rt-thread/master/bsp/stm32/stm32f407-atk-explorer/board/board.h"

# 访问AT32系列共享驱动（所有AT32 BSP共用）
curl -sL "https://raw.githubusercontent.com/RT-Thread/rt-thread/master/bsp/at32/libraries/rt_drivers/drv_usart_v2.c"

# GitHub限速时，用宿主网页抓取能力（WebFetch 或等价物）读GitHub页面获取目录结构
网页抓取（WebFetch 或等价物）("https://github.com/RT-Thread/rt-thread/tree/master/bsp/at32/at32f437-start",
         "列出这个目录下的所有文件和子目录")
```

### RT-Thread关键路径

| 路径模式 | 内容 |
|---------|------|
| `bsp/<vendor>/<board>/` | 板级支持（Kconfig、SConscript、rtconfig.py） |
| `bsp/<vendor>/<board>/board/` | 板级初始化（board.c/board.h、链接脚本）。**注意目录结构因芯片系列而异**：AT32为`board/inc/board.h`+`board/src/board.c`，STM32为`board/board.h`+`board/board.c` |
| `bsp/<vendor>/<board>/applications/` | 应用代码（main.c） |
| `bsp/<vendor>/libraries/rt_drivers/` | **芯片系列共享外设驱动**（ADC/CAN/DAC/DMA/Flash/GPIO/I2C/PWM/SPI/UART/USB/WDT等） |
| `bsp/<vendor>/libraries/` | 厂商固件库（HAL/StdPeriph）、启动文件、链接脚本 |
| `bsp/stm32/` | STM32公共框架（所有STM32 BSP共享的驱动和配置） |
| `drivers/` | RT-Thread通用驱动框架（与BSP无关） |
| `libcpu/<arch>/<chip>/` | CPU架构级代码（中断向量、上下文切换） |

> **注意**：AT32系列的驱动在 `bsp/at32/libraries/rt_drivers/`，不在单个BSP目录内。STM32系列同理，驱动在 `bsp/stm32/` 公共目录下。

### 已知BSP路径

| 芯片 | BSP路径 | 外设驱动位置 |
|------|---------|-------------|
| STM32F407 | `bsp/stm32/stm32f407-*` (8个板级) | `bsp/stm32/` 公共目录（GPIO/UART/SPI/I2C/PWM/ADC/DAC/CAN/USB/SDIO/Flash/WDT/EMAC） |
| AT32F437 | `bsp/at32/at32f437-start/` | `bsp/at32/libraries/rt_drivers/`（ADC/CAN/DAC/DMA/EMAC/Flash/GPIO/I2C/PWM/QSPI/RTC/SDIO/SDRAM/SPI/UART/USB/WDT） |
| ESP32-C3 | `bsp/ESP/ESP32_C3/` | 基于ESP-IDF桥接，依赖乐鑫组件 |

### 注意事项

- STM32系列BSP使用CubeMX `.ioc` 文件定义引脚和时钟配置，可直接读取
- **驱动在系列共享目录**，不在单个BSP内：AT32驱动在 `bsp/at32/libraries/rt_drivers/`，STM32驱动在 `bsp/stm32/`
- 对AT32F437，RT-Thread的驱动覆盖比NuttX更全（20+外设 vs NuttX的基础BSP）
- **GitHub API限速**：未认证搜索API仅10次/分钟。限速时可用宿主网页抓取能力（WebFetch 或等价物）读GitHub页面获取目录结构，或配置`GITHUB_TOKEN`环境变量提高限额

---

## 厂商SDK

### ESP-IDF（ESP32-C3）

```bash
# SoC能力定义（CPU核心数、外设数量、内存大小等）
curl -sL "https://raw.githubusercontent.com/espressif/esp-idf/master/components/soc/esp32c3/include/soc/soc_caps.h"

# 寄存器定义
curl -sL "https://raw.githubusercontent.com/espressif/esp-idf/master/components/soc/esp32c3/register/soc/uart_reg.h"
```

ESP-IDF关键路径：
- `components/soc/{chip}/include/soc/soc_caps.h` — SoC能力宏定义
- `components/soc/{chip}/register/` — 各外设寄存器定义
- `components/hal/{chip}/` — HAL层实现（注意：新版ESP-IDF中uart_hal已移至`components/esp_hal_uart/uart_hal.c`）
- `components/esp_hw_support/include/soc/` — 硬件支持层

### ArteryTek SDK（AT32F437）

```bash
# 搜索AT32F437固件库
curl -sL -H "Accept: application/vnd.github+json" \
  "https://api.github.com/search/code?q=at32f437+repo:ArteryTek/AT32F435_437_Firmware_Library"
```

### 其他厂商SDK参考

| 厂商 | GitHub仓库 | 说明 |
|------|-----------|------|
| Espressif | `espressif/esp-idf` | ESP32全系列 |
| ArteryTek | `ArteryTek/AT32F435_437_Firmware_Library` | AT32F4系列 |
| Bestechnic | 闭源（联系厂商） | BES2600W需通过OpenHarmony间接获取 |
| ASR Micro | 闭源（联系厂商） | ASR582X需通过OpenHarmony间接获取 |
| Allwinner | `linux-sunxi/sunxi-tools` + 官方SDK | T507等 |
