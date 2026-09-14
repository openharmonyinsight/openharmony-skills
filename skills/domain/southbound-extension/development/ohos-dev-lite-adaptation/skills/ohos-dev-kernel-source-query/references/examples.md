# 使用示例

## 例1：读取STM32F4的DTS（Linux主线，路径已知）

```bash
# 已知ST芯片，直接拼路径
curl -sL "https://raw.githubusercontent.com/torvalds/linux/master/arch/arm/boot/dts/st/stm32f429.dtsi"
```

## 例2：查找全志T507的pinctrl（Linux主线，路径已知）

```bash
# T507 ≈ H616，已知全志路径
curl -sL "https://raw.githubusercontent.com/torvalds/linux/master/drivers/pinctrl/sunxi/pinctrl-sun50i-h616.c"
```

## 例3：用Sourcegraph定位文件（路径未知时）

```bash
# 场景：想找RT-Thread中AT32F437的board.h，但不确定具体路径

# Sourcegraph路径搜索（~200ms，不限速）
# 注意：搜索词用芯片名即可，不要在搜索词中加文件名（会限制过严）
curl -sL "https://sourcegraph.com/.api/search/stream?q=repo:github.com/RT-Thread/rt-thread+at32f437+type:path"
# 返回JSON中 "path" 字段:
#   "bsp/at32/at32f437-start/board/inc/board.h"
#   "bsp/at32/at32f437-start/board/src/board.c"
#   "bsp/at32/at32f437-start/board/Kconfig"

# 拿到正确路径后，直接读文件
curl -sL "https://raw.githubusercontent.com/RT-Thread/rt-thread/master/bsp/at32/at32f437-start/board/inc/board.h"
```

## 例4：查找AT32F437的BSP（NuttX，Sourcegraph定位）

```bash
# 第1步：Sourcegraph搜索AT32F437相关文件
curl -sL "https://sourcegraph.com/.api/search/stream?q=repo:github.com/apache/nuttx+at32f437+type:path"
# 发现: boards/arm/at32/at32f437-mini/include/board.h
# 发现: boards/arm/at32/at32f437-mini/src/at32_gpio.c（GPIO驱动）
# 发现: boards/arm/at32/at32f437-mini/src/at32_ethernet.c（以太网驱动）

# 第2步：读取目标文件
curl -sL "https://raw.githubusercontent.com/apache/nuttx/master/boards/arm/at32/at32f437-mini/include/board.h"
```

## 例5：查找Hi3861的SDK头文件（OpenHarmony，GitCode API）

```bash
# OpenHarmony已迁移至GitCode，GitHub镜像可能过期
# 注意：Hi3861 SDK头文件在 include/ 目录，不是 platform/include/

# 用GitCode API列目录（免认证）
curl -s "https://api.gitcode.com/api/v5/repos/openharmony/device_soc_hisilicon/contents/hi3861v100/sdk_liteos/include?ref=master"
# 返回JSON数组，包含 hi_gpio.h, hi_uart.h, hi_io.h, hi_mux.h 等文件及SHA

# 用SHA下载原始文件
curl -s "https://raw.gitcode.com/openharmony/device_soc_hisilicon/blobs/{sha}/hi3861v100/sdk_liteos/include/hi_gpio.h"

# 或一步到位（返回base64编码内容）
curl -s "https://api.gitcode.com/api/v5/repos/openharmony/device_soc_hisilicon/contents/hi3861v100/sdk_liteos/include/hi_gpio.h?ref=master"
```

## 例6：查找ESP32-C3的SoC能力定义（ESP-IDF，路径已知）

```bash
# ESP32-C3优先查ESP-IDF，路径规律明确
curl -sL "https://raw.githubusercontent.com/espressif/esp-idf/master/components/soc/esp32c3/include/soc/soc_caps.h"
```

## 例7：查找未知芯片ASR582X（多级回退）

```bash
# 第1步：Sourcegraph搜Linux主线（~200ms）
curl -sL "https://sourcegraph.com/.api/search/stream?q=repo:github.com/torvalds/linux+asr582x+type:path"
# 返回空 → 不在Linux主线

# 第2步：OpenHarmony → 用GitCode API（Sourcegraph未索引OpenHarmony GitHub镜像）
curl -s "https://api.gitcode.com/api/v5/repos/openharmony/device_soc_asrmicro/contents/?ref=master"
# 找到 asr582x/ 目录 → 用GitCode API导航并获取文件
```

## 例8：compatible字符串反查驱动（Sourcegraph内容搜索）

```bash
# 场景：在DTS中看到 compatible = "snps,dw-apb-uart"，想知道哪个驱动处理它

# Sourcegraph内容搜索（替代GitHub API，不限速）
curl -sL "https://sourcegraph.com/.api/search/stream?q=repo:github.com/torvalds/linux+%22snps,dw-apb-uart%22+lang:c&patternType=literal"
# 返回: drivers/tty/serial/8250/8250_dw.c（主驱动）
# 返回: drivers/tty/serial/8250/8250_early.c（early console）

# 读取驱动源码
curl -sL "https://raw.githubusercontent.com/torvalds/linux/master/drivers/tty/serial/8250/8250_dw.c"
```

## 例9：完整驱动查询流程（DTS → compatible → 驱动源码）

```bash
# 场景：想知道全志T507的I2C驱动实现细节

# 第1步：读DTS，找到I2C节点的compatible值
curl -sL "https://raw.githubusercontent.com/torvalds/linux/master/arch/arm64/boot/dts/allwinner/sun50i-h616.dtsi" \
  | grep -B2 -A10 "i2c@"
# 发现: compatible = "allwinner,sun6i-a31-i2c"

# 第2步：Sourcegraph内容搜索匹配的驱动
curl -sL "https://sourcegraph.com/.api/search/stream?q=repo:github.com/torvalds/linux+%22allwinner,sun6i-a31-i2c%22+lang:c&patternType=literal"
# 发现: drivers/i2c/busses/i2c-mv64xxx.c

# 第3步：读取驱动源码
curl -sL "https://raw.githubusercontent.com/torvalds/linux/master/drivers/i2c/busses/i2c-mv64xxx.c"

# 结论：全志T507的I2C实际使用的是Marvell MV64xxx IP核驱动
```

## 例10：读取STM32 UART驱动实现（直接读已知路径）

```bash
# 路径已知，直接读驱动源码
curl -sL "https://raw.githubusercontent.com/torvalds/linux/master/drivers/tty/serial/stm32-usart.c" \
  | head -100
# 可看到：寄存器偏移定义、波特率计算、中断处理、DMA配置
```

## 例11：查找不在Linux主线的芯片（厂商内核树）

```bash
# 场景：想查RK3568的DTS，Linux主线不完整

# 第1步：先搜Linux主线（确认是否有）
curl -sL "https://sourcegraph.com/.api/search/stream?q=repo:github.com/torvalds/linux+rk3568.dtsi+type:path"
# 无结果 → 进入第2步

# 第2步：搜Rockchip厂商内核树（注意用@指定分支）
curl -sL "https://sourcegraph.com/.api/search/stream?q=repo:github.com/rockchip-linux/kernel@develop-4.19+rk3568+type:path"
# 找到: arch/arm64/boot/dts/rockchip/rk3568.dtsi（在develop-4.19分支）

# 第3步：用正确的分支名读取DTS
curl -sL "https://raw.githubusercontent.com/rockchip-linux/kernel/develop-4.19/arch/arm64/boot/dts/rockchip/rk3568.dtsi"
```

## 例12：查找驱动的Kconfig配置项

```bash
# 场景：想知道STM32 UART驱动需要启用哪些内核配置

# Sourcegraph不支持lang:Kconfig，直接用raw URL读取对应子系统的Kconfig
curl -sL "https://raw.githubusercontent.com/torvalds/linux/master/drivers/tty/serial/Kconfig" \
  | grep -A 15 "config SERIAL_STM32"
# 输出：depends on ARCH_STM32 || COMPILE_TEST, select SERIAL_CORE, select SERIAL_MCTRL_GPIO if GPIOLIB

# 如果不知道Kconfig在哪个目录，先用Sourcegraph路径搜索
curl -sL "https://sourcegraph.com/.api/search/stream?q=repo:github.com/torvalds/linux+Kconfig+path:drivers/tty/serial+type:path"
```

## 例13：查找DT bindings YAML文档

```bash
# 场景：想知道 compatible = "st,stm32-uart" 节点支持哪些属性

# 搜索YAML binding文档（用子系统目录+芯片名缩小范围）
curl -sL "https://sourcegraph.com/.api/search/stream?q=repo:github.com/torvalds/linux+stm32+path:bindings/serial+type:path"
# 找到: Documentation/devicetree/bindings/serial/st,stm32-uart.yaml

# 读取YAML，查看properties字段列出所有支持的属性（reg/interrupts/clocks/dmas等）
curl -sL "https://raw.githubusercontent.com/torvalds/linux/master/Documentation/devicetree/bindings/serial/st,stm32-uart.yaml"
```

## 例14：GitCode列目录 + 下载文件（OpenHarmony Hi3861 SDK头文件）

```bash
# 场景：想读取Hi3861的GPIO头文件，仓库在GitCode（非GitHub）

# 步骤1：列目录，找到目标文件的SHA
curl -s "https://api.gitcode.com/api/v5/repos/openharmony/device_soc_hisilicon/contents/hi3861v100/sdk_liteos/include?ref=master"
# 返回JSON数组，找到 hi_gpio.h 的 sha: "fd7a9aab83f783ed2b5ad4d621d3d3d76d778145"

# 步骤2：用SHA下载原始文件
curl -s "https://raw.gitcode.com/openharmony/device_soc_hisilicon/blobs/fd7a9aab83f783ed2b5ad4d621d3d3d76d778145/hi3861v100/sdk_liteos/include/hi_gpio.h"
# 返回原始C头文件内容

# 或者一步到位：直接读单文件（返回JSON含base64编码的content）
curl -s "https://api.gitcode.com/api/v5/repos/openharmony/device_soc_hisilicon/contents/hi3861v100/sdk_liteos/include/hi_gpio.h?ref=master"
# 返回JSON，其中 "content" 字段是base64编码的文件内容
```

## 例15：GitCode导航目录结构（查找HCS配置文件）

```bash
# 场景：想找Hi3516DV300的GPIO HCS配置文件，不确定具体路径

# 从仓库根目录开始导航
curl -s "https://api.gitcode.com/api/v5/repos/openharmony/device_soc_hisilicon/contents/hi3516dv300?ref=master"
# 看到子目录: sdk_linux, sdk_liteos, uboot

# 进入sdk_liteos
curl -s "https://api.gitcode.com/api/v5/repos/openharmony/device_soc_hisilicon/contents/hi3516dv300/sdk_liteos?ref=master"
# 看到: hdf_config, include, mpp

# 进入hdf_config
curl -s "https://api.gitcode.com/api/v5/repos/openharmony/device_soc_hisilicon/contents/hi3516dv300/sdk_liteos/hdf_config?ref=master"
# 看到: adc, dmac, gpio, i2c, pin, pwm, spi, timer, uart, watchdog... 以及 hdf.hcs

# 进入gpio子目录，获取SHA后下载
curl -s "https://api.gitcode.com/api/v5/repos/openharmony/device_soc_hisilicon/contents/hi3516dv300/sdk_liteos/hdf_config/gpio?ref=master"
# 找到 gpio_config.hcs 的 SHA，然后下载
```
