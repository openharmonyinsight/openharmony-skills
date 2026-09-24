# 参考资料汇总

## Linux内核文档与规范

> 01芯片规格解析器的主要数据来源：Linux内核源码中的DTS、pinctrl/clk驱动、dt-bindings头文件。

### Device Tree规范

| 材料 | 链接 |
|------|------|
| Device Tree规范（官方） | [devicetree-specification.readthedocs.io](https://devicetree-specification.readthedocs.io/en/latest/) |
| Linux内核DTS文档 | [kernel.org/doc/html/latest/devicetree](https://www.kernel.org/doc/html/latest/devicetree/) |
| DT bindings编写指南 | [kernel.org/doc/devicetree/bindings](https://www.kernel.org/doc/Documentation/devicetree/bindings/) |
| ePAPR规范（嵌入式平台） | [devicetree.org/specifications](https://www.devicetree.org/specifications/) |

### Linux内核源码镜像

| 材料 | 链接 |
|------|------|
| Linux主线内核（GitHub镜像） | [github.com/torvalds/linux](https://github.com/torvalds/linux) |
| linux-next（最新开发分支） | [git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git](https://git.kernel.org/pub/scm/linux/kernel/git/next/linux-next.git) |
| Elixir Cross Referencer（在线代码浏览） | [elixir.bootlin.com](https://elixir.bootlin.com/linux/latest/source) |
| STM32 DTS文件（在线浏览） | [elixir.bootlin.com/.../arch/arm/boot/dts/st/](https://elixir.bootlin.com/linux/latest/source/arch/arm/boot/dts/st) |
| 全志DTS文件（在线浏览） | [elixir.bootlin.com/.../arch/arm64/boot/dts/allwinner/](https://elixir.bootlin.com/linux/latest/source/arch/arm64/boot/dts/allwinner) |

### pinctrl/clk子系统文档

| 材料 | 链接 |
|------|------|
| pinctrl子系统文档 | [kernel.org/doc/pinctrl](https://www.kernel.org/doc/html/latest/driver-api/pinctl.html) |
| Common Clock Framework文档 | [kernel.org/doc/clk](https://www.kernel.org/doc/html/latest/driver-api/clk.html) |
| pinctrl bindings格式 | [kernel.org/pinctl-bindings](https://www.kernel.org/doc/Documentation/devicetree/bindings/pinctrl/) |

---

## 各芯片的源码与文档

### STM32F407（Cortex-M4）— Linux主线完整支持

| 材料 | 链接 |
|------|------|
| Linux DTS（stm32f429.dtsi等） | [elixir.bootlin.com/.../stm32f429.dtsi](https://elixir.bootlin.com/linux/latest/source/arch/arm/boot/dts/st/stm32f429.dtsi) |
| Linux pinctrl驱动 | [elixir.bootlin.com/.../pinctrl-stm32f429.c](https://elixir.bootlin.com/linux/latest/source/drivers/pinctrl/stm32/pinctrl-stm32f429.c) |
| Linux clk驱动 | [elixir.bootlin.com/.../clk-stm32f4.c](https://elixir.bootlin.com/linux/latest/source/drivers/clk/st/clk-stm32f4.c) |
| DT bindings头文件 | [elixir.bootlin.com/.../stm32f4-clock.h](https://elixir.bootlin.com/linux/latest/source/include/dt-bindings/clock/stm32f4-clock.h) |
| CMSIS-SVD文件（备选） | [github.com/modm-io/cmsis-svd-stm32](https://github.com/modm-io/cmsis-svd-stm32) |
| STM32CubeF4 SDK | [github.com/STMicroelectronics/STM32CubeF4](https://github.com/STMicroelectronics/STM32CubeF4) |
| STM32F407 Reference Manual (PDF) | [st.com RM0090](https://www.st.com/resource/en/reference_manual/rm0090.pdf) |

### 全志T507（Cortex-A53, L1）— Linux主线支持好

| 材料 | 链接 |
|------|------|
| Linux DTS（sun50i-h616.dtsi） | [elixir.bootlin.com/.../sun50i-h616.dtsi](https://elixir.bootlin.com/linux/latest/source/arch/arm64/boot/dts/allwinner/sun50i-h616.dtsi) |
| Linux pinctrl驱动 | [elixir.bootlin.com/.../pinctrl-sun50i-h616.c](https://elixir.bootlin.com/linux/latest/source/drivers/pinctrl/sunxi/pinctrl-sun50i-h616.c) |
| Linux clk驱动（CCU） | [elixir.bootlin.com/.../ccu-sun50i-h616.c](https://elixir.bootlin.com/linux/latest/source/drivers/clk/sunxi-ng/ccu-sun50i-h616.c) |
| DT bindings头文件 | [elixir.bootlin.com/.../sun50i-h616-ccu.h](https://elixir.bootlin.com/linux/latest/source/include/dt-bindings/clock/sun50i-h616-ccu.h) |

### Hi3861（RISC-V, L0）— 需SDK头文件

| 材料 | 链接 |
|------|------|
| OpenHarmony SoC适配仓库（含SDK头文件） | [gitcode.com/openharmony/device_soc_hisilicon](https://gitcode.com/openharmony/device_soc_hisilicon) — `hi3861v100/sdk_liteos/platform/include/` |
| Hi3861 芯片产品页 | [hisilicon.com/cn/products/hi3861v100](https://www.hisilicon.com/cn/products/connectivity/short-range-iot/wifi-nearlink-ble/hi3861v100) |
| Hi3861 社区资料汇总 | [github.com/SoCXin/Hi3861](https://github.com/SoCXin/Hi3861) |

### ESP32-C3（RISC-V, L0）— ESP-IDF头文件

| 材料 | 链接 |
|------|------|
| ESP-IDF寄存器定义 | [github.com/espressif/esp-idf/.../register/soc/](https://github.com/espressif/esp-idf/tree/master/components/soc/esp32c3/register/soc/) |
| SoC能力头文件 | [github.com/espressif/esp-idf/.../soc_caps.h](https://github.com/espressif/esp-idf/blob/master/components/soc/esp32c3/include/soc/soc_caps.h) |
| GPIO信号映射 | [github.com/espressif/esp-idf/.../gpio_sig_map.h](https://github.com/espressif/esp-idf/blob/master/components/soc/esp32c3/include/soc/gpio_sig_map.h) |
| ESP32-C3 Datasheet (PDF) | [espressif.com/esp32-c3_datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-c3_datasheet_en.pdf) |

### Hi3516DV300（Cortex-A7, L1）— 需海思SDK

| 材料 | 链接 |
|------|------|
| OpenHarmony SoC适配仓库 | [gitcode.com/openharmony/device_soc_hisilicon](https://gitcode.com/openharmony/device_soc_hisilicon) — `hi3516dv300/` |
| HiSpark Taurus开发板仓库 | [github.com/openharmony/device_hisilicon_hispark_taurus](https://github.com/openharmony/device_hisilicon_hispark_taurus) |
| kernel_liteos_a内核（含DTS） | [gitcode.com/openharmony/kernel_liteos_a](https://gitcode.com/openharmony/kernel_liteos_a) — `arch/arm/boot/dts/` |

### BES2600W（Cortex-M33, L0）— 需贝斯SDK

| 材料 | 链接 |
|------|------|
| OpenHarmony BES2600适配仓库 | [gitcode.com/openharmony/device_soc_bestechnic](https://gitcode.com/openharmony/device_soc_bestechnic) |
| BES2600W 移植案例 | [gitcode.com/openharmony/docs/.../porting-bes2600w](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-bes2600w-on-minisystem-display-demo.md) |

### XR806（RISC-V, L0）— 需全志SDK

| 材料 | 链接 |
|------|------|
| XR806 文档 | [docs.aw-ol.com/xr806/study/soft_dig/](https://docs.aw-ol.com/xr806/study/soft_dig/) |

### ASR582X（RISC-V, L0）— 需翱捷SDK

| 材料 | 链接 |
|------|------|
| OpenHarmony ASR适配仓库 | ⚠️ 需确认（ASR SDK公开程度有限） |

### AT32F437（Cortex-M4, L0）— 兼容STM32

| 材料 | 链接 |
|------|------|
| ArteryTek SDK（含头文件） | [github.com/ArteryTek/sdk-csp-at32f4](https://github.com/ArteryTek/sdk-csp-at32f4) |
| AT32F437 产品页 | [arterytek.com/cn/product/AT32F437](https://www.arterytek.com/cn/product/AT32F437.jsp) |

---

## 通用标准规范

| 材料 | 链接 |
|------|------|
| Device Tree规范 | [devicetree-specification.readthedocs.io](https://devicetree-specification.readthedocs.io/en/latest/chapter2-devicetree-basics.html) |
| CMSIS-SVD格式规范（备选方案） | [arm-software.github.io/CMSIS_5/SVD](https://arm-software.github.io/CMSIS_5/SVD/html/index.html) |
| RISC-V规范 | [riscv.org/specifications/ratified/](https://riscv.org/specifications/ratified/) |
| ARM Architecture Reference Manual | [developer.arm.com/architectures/cpu-architecture](https://developer.arm.com/architectures/cpu-architecture/cortex-m) |

---

## OpenHarmony Lite 参考

1. [OpenHarmony 轻量系统移植指导 (GitCode)](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/Readme-CN.md) — 官方L0移植文档
2. [kernel_liteos_m 内核源码](https://gitcode.com/openharmony/kernel_liteos_m) — LiteOS-M内核
3. [kernel_liteos_a 内核源码](https://gitcode.com/openharmony/kernel_liteos_a) — LiteOS-A内核
4. [build_lite 构建系统](https://gitcode.com/openharmony/build_lite) — 编译构建系统
5. [drivers_lite 轻量系统驱动](https://gitcode.com/openharmony/drivers_lite) — L0驱动实现
6. [device_soc_hisilicon](https://gitcode.com/openharmony/device_soc_hisilicon) — 海思芯片SoC适配

## 社区适配经验

7. [OpenHarmony 轻量系统芯片适配关键流程 (知乎)](https://zhuanlan.zhihu.com/p/2029119790535521768)
8. [OpenHarmony 小型系统芯片移植指南 (腾讯云)](https://cloud.tencent.com/developer/article/2533992)
9. [STM32 轻量系统移植分享 (CSDN)](https://laval.csdn.net/edu/a92078035a78abe9c5b11533159f4069)
10. [Hi3861 启动流程分析 (博客园)](https://www.cnblogs.com/openharmony/p/16598114.html)

---

## 备选方案：无Linux适配时的替代来源

> 当芯片没有Linux主线支持时，退回到以下来源。

### CMSIS-SVD（仅ARM Cortex-M生态）

| 材料 | 链接 |
|------|------|
| CMSIS-SVD官方文档 | [arm-software.github.io/CMSIS_5/SVD](https://arm-software.github.io/CMSIS_5/SVD/html/index.html) |
| SVDConv验证工具 | [developer.arm.com/SVDConv](https://developer.arm.com/documentation/101407/0543/Utilities/System-View-Description-Converter) |
| ST CMSIS-SVD使用实践 | [wiki.st.com/stm32mpu/wiki/CMSIS-SVD](https://wiki.st.com/stm32mpu/wiki/CMSIS-SVD_environment_and_scripts) |

### PDF解析工具（最后手段）

| 材料 | 链接 |
|------|------|
| Docling (IBM) | [github.com/DS4SD/docling](https://github.com/DS4SD/docling) |
| Marker: PDF to Markdown | [github.com/datalab-to/marker](https://github.com/datalab-to/marker) |
| Camelot: PDF Table Extraction | [camelot-py.readthedocs.io](https://camelot-py.readthedocs.io/) |

### LLM结构化数据提取

| 材料 | 链接 |
|------|------|
| LLM结构化提取指南 (Simon Willison) | [simonw.substack.com/p/structured-data-extraction](https://simonw.substack.com/p/structured-data-extraction-from-unstructured) |
| LLM PDF提取工作流 (Firecrawl) | [firecrawl.dev/glossary/llm-pdf-data-extraction](https://www.firecrawl.dev/glossary/web-extraction-apis/llm-pdf-data-extraction) |
