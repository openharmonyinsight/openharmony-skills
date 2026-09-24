# Linux内核源码路径规律

Linux内核中芯片硬件信息的文件组织有严格规律。掌握这些路径可以直接拼URL读取文件，无需搜索。

## 信息依赖关系

DTS是查询入口，`compatible`属性是枢纽，各文件类型通过引用关系串联：

```
DTS (.dtsi) — 入口，包含所有外设节点
  ├── reg / interrupts        → 寄存器基地址、中断号（芯片规格）
  ├── compatible = "v,dev"    → 反查驱动文件（见linux-driver-lookup.md）
  ├── clocks = <&rcc CLK_X>  → 引用DT bindings头文件中的时钟宏（§DT bindings）
  ├── pinctrl-0 = <&pins>    → 引用pinctrl节点定义（§pinctrl驱动）
  └── dmas = <&dma ...>      → DMA通道映射

DT bindings YAML → 解释DTS节点支持哪些属性（§DT bindings）
Kconfig → 确认驱动编译依赖（§Kconfig和Makefile）
```

**典型查询顺序**（给定芯片+外设）：

```
① DTS (.dtsi)         → 拿到 compatible / reg / interrupts / clocks / pinctrl
② DT bindings YAML    → 理解节点属性含义（按需）
③ compatible 反查驱动 → 查linux-driver-lookup.md，或Sourcegraph搜compatible字符串
④ 驱动源码            → 寄存器操作、中断处理、DMA配置
⑤ Kconfig             → 编译依赖（按需）
⑥ pinctrl驱动         → 引脚AF功能表（按需）
⑦ 时钟驱动            → 时钟树结构（按需）
```

> 步骤①③④是核心路径，②⑤⑥⑦按需求选做。

## URL格式

```
https://raw.githubusercontent.com/torvalds/linux/master/{path}
```

备选（锁定版本，更稳定）：
```
https://raw.githubusercontent.com/torvalds/linux/v6.6/{path}
```

读取命令：
```bash
# 读取文件
curl -sL "https://raw.githubusercontent.com/torvalds/linux/master/{path}"

# 读取特定版本
curl -sL "https://raw.githubusercontent.com/torvalds/linux/v6.6/{path}"

# 检查文件是否存在（看HTTP状态码）
curl -sI "https://raw.githubusercontent.com/torvalds/linux/master/{path}" | head -1
```

---

## 厂商内核树

部分芯片不在Linux主线（`torvalds/linux`），而在厂商维护的GitHub仓库中。路径规律与主线一致，但分支名常为版本分支（如`develop-4.19`）而非`master`。

| 芯片厂商 | GitHub仓库 | 覆盖芯片 | 常用分支 |
|---------|-----------|---------|---------|
| Rockchip | `github.com/rockchip-linux/kernel` | RK3568/RK3588/RV1106 | `develop-4.19` / `develop-5.10` |
| NXP i.MX | `github.com/nxp-imx/linux-imx` | i.MX6/i.MX8/i.MX93 | `lf-6.6.y` |

```bash
# Sourcegraph搜索厂商内核树（需指定分支）
curl -sL "https://sourcegraph.com/.api/search/stream?q=repo:github.com/rockchip-linux/kernel@develop-4.19+rk3568+type:path"

# raw URL读厂商树文件（注意分支名）
curl -sL "https://raw.githubusercontent.com/rockchip-linux/kernel/develop-4.19/arch/arm64/boot/dts/rockchip/rk3568.dtsi"
```

> **判断方法**：先用Sourcegraph搜`torvalds/linux`，无结果 → 查上表找对应厂商仓库 → 用`@分支名`指定分支搜索。

---

## DTS文件（硬件拓扑和外设信息）

### 目录结构

```
arch/
├── arm/boot/dts/           # ARM 32位芯片
│   ├── st/stm32f4*.dts*    # ST STM32F4系列
│   ├── allwinner/sun8i-*.dts*  # 全志A系列
│   ├── hisilicon/hi{series}*.dtsi  # 海思
│   └── nxp/imx/imx{series}*.dtsi   # NXP i.MX
├── arm64/boot/dts/         # ARM 64位芯片
│   ├── allwinner/          # 全志64位（A64/H5/H6/H616/T507）
│   ├── hisilicon/          # 海思64位
│   ├── freescale/          # NXP i.MX8
│   └── rockchip/           # Rockchip RK3xxx
└── riscv/boot/dts/         # RISC-V芯片
    └── sifive/
```

### 各厂商DTS路径

| 厂商 | 架构 | DTS路径 | 示例 |
|------|------|---------|------|
| ST (STM32) | ARM | `arch/arm/boot/dts/st/stm32{series}*.dtsi` | `st/stm32f429.dtsi` |
| 全志 (Allwinner) | ARM | `arch/arm/boot/dts/allwinner/sun{series}*.dtsi` | `allwinner/sun8i-h3.dtsi` |
| 全志 (Allwinner) | ARM64 | `arch/arm64/boot/dts/allwinner/sun{series}*.dtsi` | `allwinner/sun50i-h616.dtsi` |
| 海思 (HiSilicon) | ARM | `arch/arm/boot/dts/hisilicon/hi{series}*.dtsi` | `hisilicon/hi3519.dtsi` |
| 海思 (HiSilicon) | ARM64 | `arch/arm64/boot/dts/hisilicon/hi{series}*.dtsi` | `hisilicon/hi3660.dtsi` |
| NXP (i.MX) | ARM | `arch/arm/boot/dts/nxp/imx/imx{series}*.dtsi` | `nxp/imx/imx6q.dtsi` |
| NXP (i.MX) | ARM64 | `arch/arm64/boot/dts/freescale/imx{series}*.dtsi` | `freescale/imx8mm.dtsi` |
| Rockchip | ARM64 | `arch/arm64/boot/dts/rockchip/rk{series}*.dtsi` | `rockchip/rk3568.dtsi` |
| SiFive | RISC-V | `arch/riscv/boot/dts/sifive/` | `sifive/fu540-c000.dtsi` |

### DTS文件层次

每个芯片通常有3层DTS文件，从通用到具体：

```
stm32f429.dtsi          # SoC级：定义所有外设节点（地址、中断、时钟）
  └── stm32f429i-disco.dts  # 板级：选择启用哪些外设、配置引脚
```

- **`.dtsi`（SoC级）**：包含芯片所有外设的定义 — **芯片规格的主要来源**
- **`.dts`（板级）**：选择启用哪些外设、配置具体引脚 — **反映开发板的硬件连接**

### 关键DTS属性

| 属性 | 含义 | 示例 |
|------|------|------|
| `compatible` | 设备类型标识，格式`"vendor,device"` | `"st,stm32f429-usart"` |
| `reg` | 寄存器基地址 + 大小 | `<0x40011000 0x400>` |
| `interrupts` | 中断号 + 触发方式 | `<37>` (NVIC第37号) |
| `clocks` | 时钟源引用 | `<&rcc 0 STM32F4_APB2_CLOCK(USART1)>` |
| `pinctrl-0` | 引脚配置引用 | `<&usart1_pins_a>` |
| `status` | 设备状态 | `"okay"` = 启用, `"disabled"` = 禁用 |

---

## pinctrl驱动（引脚复用表）

| 厂商 | 路径 |
|------|------|
| ST | `drivers/pinctrl/stm32/pinctrl-stm32*.c` |
| 全志 | `drivers/pinctrl/sunxi/pinctrl-sun*.c` |
| 海思 | `drivers/pinctrl/hisilicon/pinctrl-*.c` |
| NXP | `drivers/pinctrl/freescale/pinctrl-imx*.c` |
| Rockchip | `drivers/pinctrl/pinctrl-rockchip*.c` |

pinctrl驱动文件中包含引脚的完整复用信息：每个引脚的所有AF功能、GPIO端口分组、特殊功能映射（UART TX/RX、I2C SDA/SCL、SPI MOSI/MISO等）。

---

## 时钟驱动

| 厂商 | 路径 |
|------|------|
| ST | `drivers/clk/clk-stm32*.c` |
| 全志 | `drivers/clk/sunxi-ng/ccu-sun*.c` |
| 海思 | `drivers/clk/hisilicon/clk-hi*.c` |
| NXP | `drivers/clk/imx/clk-imx*.c` |
| Rockchip | `drivers/clk/rockchip/clk-rk*.c` |

时钟驱动使用Common Clock Framework（CCF）描述时钟树：时钟源 → PLL → 分频器 → 外设门控。

---

## DT bindings

### 头文件（宏定义）

```
include/dt-bindings/clock/{vendor}-*.h      # 时钟宏
include/dt-bindings/pinctrl/{vendor}-*.h    # 引脚宏
include/dt-bindings/reset/{vendor}-*.h      # 复位宏
include/dt-bindings/interrupt-controller/   # 中断类型
```

### YAML说明文档（节点属性规范）

`Documentation/devicetree/bindings/` 下有每个`compatible`字符串的官方YAML文档，描述该外设节点支持哪些属性、每个属性的含义和格式。读YAML比读驱动C代码更快理解节点结构。

路径规律：`Documentation/devicetree/bindings/<subsystem>/<vendor>,<device>.yaml`

```bash
# 搜索某compatible字符串的binding文档（注意文件名不含's'：stm32-uart而非stm32-usart）
curl -sL "https://sourcegraph.com/.api/search/stream?q=repo:github.com/torvalds/linux+stm32+path:bindings/serial+type:path"

# 直接读取YAML文档
curl -sL "https://raw.githubusercontent.com/torvalds/linux/master/Documentation/devicetree/bindings/serial/st,stm32-uart.yaml"
```

YAML文件中`properties:`字段列出节点支持的所有属性（`reg`/`interrupts`/`clocks`/`dmas`等），`required:`列出必填属性。

---

## 外设驱动路径

从DTS的`compatible`属性反查驱动文件。完整查找表见 [linux-driver-lookup.md](linux-driver-lookup.md)（含UART/I2C/SPI/GPIO/PWM/ADC/Watchdog/Ethernet/DMA × 5+厂商）。

---

## Kconfig和Makefile

Kconfig回答"这个驱动依赖哪些配置项"，Makefile回答"哪些文件会被编译"。

### 路径规律

```
drivers/<subsystem>/Kconfig              # 各子系统驱动配置
arch/<arch>/Kconfig                      # 架构级配置（CPU特性、FPU等）
arch/<arch>/boot/dts/<vendor>/Makefile   # 哪些板级DTS会被编译
drivers/<subsystem>/Makefile             # 驱动文件编译规则（与源码同目录）
```

### Kconfig示例

```bash
# 直接读取某子系统的Kconfig（Sourcegraph不支持lang:Kconfig，用raw URL）
curl -sL "https://raw.githubusercontent.com/torvalds/linux/master/drivers/tty/serial/Kconfig" | grep -A 15 "config SERIAL_STM32"

# 用Sourcegraph路径搜索找到Kconfig文件位置
curl -sL "https://sourcegraph.com/.api/search/stream?q=repo:github.com/torvalds/linux+Kconfig+path:drivers/tty/serial+type:path"
```

关键字段：`depends on`（依赖条件）、`default`（默认值）、`select`（自动启用的相关选项）。

### Makefile示例

```bash
# 查看某驱动目录编译哪些文件
curl -sL "https://raw.githubusercontent.com/torvalds/linux/master/drivers/tty/serial/Makefile"
```

关键格式：`obj-$(CONFIG_SERIAL_STM32) += stm32-usart.o` — 配置项启用时编译对应.o文件。

---

> **搜索工具**：路径不确定时用Sourcegraph（首选，不限速）→ GitHub API（兜底，限速10次/分）→ Elixir Bootlin（符号交叉引用）。详见SKILL.md §查询工具。
