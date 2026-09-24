# 参考资料汇总 — 适配参考资料检索助手

---

## 1. OpenHarmony 官方移植文档（最核心）

### 1.1 轻量系统 (L0) 移植指导

| 资源 | 链接 | 说明 |
|------|------|------|
| 移植总入口 (Readme-CN.md) | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/Readme-CN.md) | 设备分类、代码获取、全部移植指导导航 |
| 轻量系统移植概述 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-minichip-overview.md) | 适配流程四步走：准备→内核→子系统→验证 |
| 轻量系统移植准备 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-minichip-prepare.md) | 环境搭建、源码获取、目录规划、编译框架 |
| 轻量系统内核移植 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-minichip-kernel.md) | arch适配、SDK集成、链接脚本 |
| 轻量系统子系统概述 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-minichip-subsys-overview.md) | 常见子系统列表和作用说明 |
| 启动恢复子系统移植 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-minichip-subsys-startup.md) | bootstrap/syspara适配 |
| 文件子系统移植 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-minichip-subsys-filesystem.md) | 文件读写能力适配 |
| 安全子系统移植 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-minichip-subsys-security.md) | token/设备认证/密钥管理 |
| 通信子系统移植 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-minichip-subsys-communication.md) | WiFi/BLE适配 |
| 外设驱动子系统移植 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-minichip-subsys-driver.md) | IoT外设API（iot_gpio.h等）和驱动适配方式 |
| 其他子系统配置 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-minichip-subsys-others.md) | 分布式调度、测试等子系统 |
| 移植验证 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-minichip-verification.md) | XTS兼容性测试方法 |
| 移植常见问题 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-chip-faqs.md) | 堆内存配置等FAQ |

### 1.2 小型系统 (L1) 移植指导

| 资源 | 链接 | 说明 |
|------|------|------|
| 小型系统移植须知 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-smallchip-prepare-needs.md) | 已适配开发板、内核信息、ROM/RAM要求 |
| 小型系统编译构建 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-smallchip-prepare-building.md) | 编译环境搭建 |
| LiteOS-A内核移植 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-smallchip-kernel-a.md) | LiteOS-A内核适配 |
| Linux内核移植 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-smallchip-kernel-linux.md) | Linux内核适配 |
| 驱动移植概述 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-smallchip-driver-overview.md) | 平台驱动和器件驱动分类 |
| 平台驱动移植 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-smallchip-driver-plat.md) | GPIO/I2C/SPI等平台驱动移植方法 |

### 1.3 三方库移植

| 资源 | 链接 | 说明 |
|------|------|------|
| CMake方式移植 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-thirdparty-cmake.md) | CMake组织的三方库移植 |
| Makefile方式移植 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-thirdparty-makefile.md) | Makefile组织的三方库移植 |

## 2. 移植案例

| 芯片 | 系统级别 | 链接 | 核心价值 |
|------|---------|------|---------|
| STM32F407 | L0 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-stm32f407-on-minisystem-eth.md) | ARM Cortex-M4，Board/SoC分离方案，步骤最详细 |
| BES2600W | L0 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-bes2600w-on-minisystem-display-demo.md) | Cortex-M33带屏方案，WiFi/BT双模 |
| ASR582X | L0 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-asr582x-combo-demo.md) | WiFi Combo方案 |
| CST85F01 | L0 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-cst85f01-combo-demo.md) | 物联网Combo方案 |
| STM32MP15 | L1 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-stm32mp15xx-on-smallsystem.md) | 小型系统移植案例 |

## 3. IoT外设API文档

> 头文件位于源码路径：`base/iot_hardware/peripheral/interfaces/kits/`

| 头文件 | 功能 | 关键API |
|--------|------|---------|
| `iot_gpio.h` | GPIO通用输入输出 | IoTGpioInit/SetDir/SetOutput/GetInput/SetPull/SetIsrMask |
| `iot_i2c.h` | I2C总线通信 | IoTI2cInit/Deinit/Write/Read/SetBaudrate |
| `iot_uart.h` | UART串口通信 | IoTUartOpen/Close/Read/Write/SetBaud/GetBaud |
| `iot_pwm.h` | PWM脉宽调制 | IoTPwmInit/Deinit/Start/Stop |
| `iot_adc.h` | ADC模数转换 | IoTAdcInit/Deinit/Read |
| `iot_watchdog.h` | 看门狗 | IoTWatchDogInit/Deinit/Start/Stop |
| `iot_flash.h` | Flash存储 | Flash读写/擦除接口 |
| `iot_errno.h` | 通用错误码 | IOT_SUCCESS/IOT_FAILURE等错误码定义 |

## 4. 内核和构建系统仓库

| 资源 | 链接 | 说明 |
|------|------|------|
| OpenHarmony 官方文档 | https://docs.openharmony.cn/ | 官方文档站入口 |
| LiteOS-M 内核仓库 | https://gitcode.com/openharmony/kernel_liteos_m | L0内核源码、API头文件、CMSIS实现 |
| LiteOS-A 内核仓库 | https://gitcode.com/openharmony/kernel_liteos_a | L1内核源码 |
| build_lite 构建框架 | https://gitcode.com/openharmony/build_lite | GN模板、工具链定义、平台配置 |
| drivers_lite 轻量驱动 | https://gitcode.com/openharmony/drivers_lite | L0驱动实现、HAL接口 |
| drivers_framework | https://gitcode.com/openharmony/drivers_framework | L1 HDF驱动框架、OSAL接口 |
| productdefine_common | https://gitcode.com/openharmony/productdefine_common | 产品定义JSON格式 |

## 5. 社区资源

| 资源 | 链接 | 说明 |
|------|------|------|
| OpenHarmony 芯片移植文章汇总 | [Laval社区](https://laval.csdn.net/694a6558bf6b0e4b285dbeb7.html) | ARM/RISC-V架构移植文章汇总 |
| 轻量系统芯片移植指南(一) | [知乎](https://zhuanlan.zhihu.com/p/6190572549) | 系统>子系统>部件逐级展开 |
| OpenHarmony外设驱动移植指南 | [Laval社区](https://laval.csdn.net/69689b07b7c94a4713690591.html) | 外设驱动移植方法 |
| 设备开发常用接口汇总 | [InfoQ](https://xie.infoq.cn/article/b1b588572054ea57a01b43494) | GPIO/I2C/UART等API汇总 |
| OpenHarmony 设备开发第一版(PDF) | [电子发烧友](https://file.elecfans.com/web2/M00/93/4C/poYBAGP2xdOAfv1HADnu2qsoNGg110.pdf) | 完整设备开发教材 |
| sig_devboard SIG组 | [Gitee](https://gitee.com/openharmony/community/blob/master/sig/sig_devboard/sig_devboard_cn.md) | 第三方开发板适配SIG组 |
| 标准系统芯片适配指南 | [Laval社区](https://laval.csdn.net/64afc2bb8e3f043cd26d8082.html) | 完整适配流程参考（标准系统） |
| 轻量级系统移植准备 | [掘金](https://juejin.cn/post/7506159639635312651) | 环境搭建参考 |
| Hi3861嵌入式应用入门 | [CSDN](https://blog.csdn.net/andylauren/article/details/139860098) | Hi3861入门教程 |
| XR806系统框图 | [全志](https://docs.aw-ol.com/xr806/study/soft_dig/) | XR806软件架构 |

## 6. OpenHarmony Lite 文档目录结构

```
docs/zh-cn/device-dev/
├── quick-start/                    # 快速入门
├── porting/                        # 移植适配（核心目录）
│   ├── Readme-CN.md                # 总入口
│   ├── porting-minichip-*.md       # L0轻量系统移植（12个文档）
│   ├── porting-smallchip-*.md      # L1小型系统移植（7个文档）
│   ├── porting-stm32f407-*.md      # STM32F407移植案例
│   ├── porting-bes2600w-*.md       # BES2600W移植案例
│   ├── porting-asr582x-*.md        # ASR582X移植案例
│   └── porting-chip-faqs.md        # 常见问题
├── driver/                         # 驱动开发
├── kernel/                         # 内核文档
├── reference/                      # 参考文档
└── get-code/                       # 代码获取
```
