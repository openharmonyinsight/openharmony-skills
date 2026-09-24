# 外设驱动路径查找表

> **重要：IP核复用现象** — 许多SoC厂商不自己写驱动，而是购买第三方IP核授权。全志T507的UART用的是Synopsys DesignWare 8250，I2C用的是Marvell MV64xxx。**从DTS的`compatible`属性反查驱动是最可靠的方法**，不要只看芯片型号猜测驱动。

## UART/串口

| 厂商/芯片 | 驱动路径 | DTS compatible | 说明 |
|-----------|---------|----------------|------|
| ST STM32 | `drivers/tty/serial/stm32-usart.c` | `"st,stm32-uart"` | STM32自研UART IP |
| 全志 sunxi | `drivers/tty/serial/8250/8250_dw.c` | `"snps,dw-apb-uart"` | Synopsys DW 8250 IP核 |
| 海思 HiSilicon | `drivers/tty/serial/amba-pl011.c` | `"arm,pl011"` | ARM PL011 IP核 |
| NXP i.MX | `drivers/tty/serial/imx.c` | `"fsl,imx6q-uart"` | NXP自研UART |
| Rockchip | `drivers/tty/serial/8250/8250_dw.c` | `"snps,dw-apb-uart"` | 同全志，Synopsys DW |
| SiFive | `drivers/tty/serial/sifive.c` | `"sifive,uart0"` | SiFive自研 |

## I2C总线

| 厂商/芯片 | 驱动路径 | DTS compatible | 说明 |
|-----------|---------|----------------|------|
| ST STM32 | `drivers/i2c/busses/i2c-stm32f4.c` / `i2c-stm32f7.c` | `"st,stm32f4-i2c"` | STM32自研I2C |
| 全志 sunxi | `drivers/i2c/busses/i2c-mv64xxx.c` | `"allwinner,sun6i-a31-i2c"` | Marvell MV64xxx IP核 |
| 海思 HiSilicon | `drivers/i2c/busses/i2c-designware-*.c` | `"snps,designware-i2c"` | Synopsys DW I2C（注意：平台驱动文件名为`i2c-designware-platdrv.c`，不是`i2c-designware-platform.c`） |
| NXP i.MX | `drivers/i2c/busses/i2c-imx.c` | `"fsl,imx21-i2c"` | NXP自研I2C |
| Rockchip | `drivers/i2c/busses/i2c-rk3x.c` | `"rockchip,rk3399-i2c"` | Rockchip自研 |

## SPI总线

| 厂商/芯片 | 驱动路径 | DTS compatible | 说明 |
|-----------|---------|----------------|------|
| ST STM32 | `drivers/spi/spi-stm32.c` | `"st,stm32f4-spi"` | STM32自研SPI |
| 全志 sunxi | `drivers/spi/spi-sun6i.c` | `"allwinner,sun6i-a31-spi"` | 全志自研SPI |
| 海思 HiSilicon | `drivers/spi/spi-dw-mmio.c` | `"snps,dw-apb-ssi"` | Synopsys DW SPI |
| NXP i.MX | `drivers/spi/spi-imx.c` | `"fsl,imx51-ecspi"` | NXP eCSPI |
| Rockchip | `drivers/spi/spi-rockchip.c` | `"rockchip,rk3066-spi"` | Rockchip自研 |

## GPIO控制器

| 厂商/芯片 | 驱动路径 | DTS compatible | 说明 |
|-----------|---------|----------------|------|
| ST STM32 | `drivers/gpio/gpio-stm32.c` (由pinctrl管理) | `"st,stm32mp157-gpio"` | pinctrl子节点 |
| 全志 sunxi | `drivers/pinctrl/sunxi/pinctrl-sunxi.c` | `"allwinner,sun6i-a31-r-pinctrl"` | pinctrl内含GPIO |
| 海思 HiSilicon | `drivers/gpio/gpio-pl061.c` | `"arm,pl061"` | ARM PL061 IP核 |
| NXP i.MX | `drivers/gpio/gpio-mxc.c` | `"fsl,imx35-gpio"` | NXP自研GPIO |
| Rockchip | `drivers/pinctrl/pinctrl-rockchip.c` | `"rockchip,gpio-bank"` | pinctrl内含GPIO |

## PWM

| 厂商/芯片 | 驱动路径 | DTS compatible | 说明 |
|-----------|---------|----------------|------|
| ST STM32 | `drivers/pwm/pwm-stm32.c` | `"st,stm32-pwm"` | TIM定时器PWM |
| 全志 sunxi | `drivers/pwm/pwm-sun4i.c` | `"allwinner,sun8i-h3-pwm"` | 全志自研PWM |
| 海思 HiSilicon | `drivers/pwm/pwm-hibvt.c` | `"hisilicon,hibvt-pwm"` | 海思BVT PWM |
| NXP i.MX | `drivers/pwm/pwm-imx27.c` | `"fsl,imx27-pwm"` | NXP PWM |
| Rockchip | `drivers/pwm/pwm-rockchip.c` | `"rockchip,rk3328-pwm"` | Rockchip PWM |

## ADC

| 厂商/芯片 | 驱动路径 | DTS compatible | 说明 |
|-----------|---------|----------------|------|
| ST STM32 | `drivers/iio/adc/stm32-adc.c` | `"st,stm32f4-adc"` | IIO子系统 |
| 全志 sunxi | `drivers/iio/adc/sun4i-gpadc-iio.c` | `"allwinner,sun8i-a33-gpadc-iio"` | GPADC |
| NXP i.MX | `drivers/iio/adc/imx7d_adc.c` | `"fsl,imx7d-adc"` | IIO ADC |

## 看门狗 (Watchdog)

| 厂商/芯片 | 驱动路径 | DTS compatible | 说明 |
|-----------|---------|----------------|------|
| ST STM32 | `drivers/watchdog/stm32_iwdg.c` | `"st,stm32-iwdg"` | 独立看门狗 |
| 全志 sunxi | `drivers/watchdog/sunxi_wdt.c` | `"allwinner,sun6i-a31-wdt"` | 全志WDT |
| ARM通用 | `drivers/watchdog/arm_sbsa_watchdog.c` | `"arm,sbsa-gwdt"` | ARM SBSA标准 |

## 以太网 MAC

| 厂商/芯片 | 驱动路径 | DTS compatible | 说明 |
|-----------|---------|----------------|------|
| ST STM32 | `drivers/net/ethernet/stmicro/stmmac/` | `"snps,dwmac-4.10"` | Synopsys DW MAC |
| 全志 sunxi | `drivers/net/ethernet/stmicro/stmmac/dwmac-sunxi.c` | `"allwinner,sun7i-a20-gmac"` | DW MAC + 全志glue |
| 海思 HiSilicon | `drivers/net/ethernet/hisilicon/hns/` | `"hisilicon,hns-mac-v1"` | 海思HNS |
| NXP i.MX | `drivers/net/ethernet/freescale/fec_main.c` | `"fsl,imx6q-fec"` | NXP FEC |
| Rockchip | `drivers/net/ethernet/stmicro/stmmac/dwmac-rk.c` | `"rockchip,rk3399-gmac"` | DW MAC + RK glue |

## DMA控制器

| 厂商/芯片 | 驱动路径 | DTS compatible | 说明 |
|-----------|---------|----------------|------|
| ST STM32 | `drivers/dma/stm32/stm32-dma.c` | `"st,stm32-dma"` | STM32 DMA（注意：在`stm32/`子目录下） |
| 全志 sunxi | `drivers/dma/sun6i-dma.c` | `"allwinner,sun8i-h3-dma"` | 全志DMA |
| ARM通用 | `drivers/dma/pl330.c` | `"arm,pl330"` | ARM PL330 DMA IP核 |
