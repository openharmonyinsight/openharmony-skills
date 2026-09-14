# 参考资料汇总 — 测试用例生成器

---

## 1. 测试框架源码仓库

| 资料 | 链接 | 核心价值 | 适用系统 |
|------|------|---------|:--------:|
| xts_tools（HCTest） | [GitCode](https://gitcode.com/openharmony/xts_tools) | HCTest框架源码（L0/L1套件结构+Unity断言） | L0/L1 |
| kernel_liteos_m testsuites（iCunit） | [GitCode](https://gitcode.com/openharmony/kernel_liteos_m) | iCunit断言引擎 + CMSIS/POSIX/IO测试套件 | L0 |
| kernel_liteos_a testsuites（HWTest） | [GitCode](https://gitcode.com/openharmony/kernel_liteos_a) | HWTest/gtest测试套件 + IO/驱动/异常测试 | L1 |
| Unity测试框架 | [GitHub](https://github.com/ThrowTheSwitch/Unity) | Unity源码和文档（380+ TEST_ASSERT_* 宏） | L0/L1 |
| Google Test | [GitHub](https://github.com/google/googletest) | HWTest的底层引擎 | L1 |

## 2. OpenHarmony 官方测试文档

| 资料 | 链接 | 核心价值 | 适用系统 |
|------|------|---------|:--------:|
| 轻量系统移植验证 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/Readme-CN.md) | 移植后XTS配置、库链接、测试结果查看 | L0/L1 |
| 开发自测试框架指南 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/device-test/developer_test.md) | HCTest使用指南（Python执行框架） | L0/L1 |
| XTS开发指南 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/readme/XTS子系统.md) | XTS兼容性测试套件概述 | L0/L1 |
| XTS Acts Lite | [GitCode](https://gitcode.com/openharmony/xts_acts/tree/master) | 官方ACTS测试用例（含Lite版） | L0/L1 |

## 3. Lite 驱动开发实践

| 资料 | 链接 | 核心价值 | 适用系统 |
|------|------|---------|:--------:|
| STM32F407轻量系统移植 | [博客园](https://www.cnblogs.com/openharmony/p/16381164.html) | STM32驱动测试参考 | L0 |
| 从零移植OpenHarmony轻量系统 | [华为开发者联盟](https://developer.huawei.com/consumer/cn/blog/topic/03893164050570049) | 完整移植和验证流程 | L0 |
| Hi3861开发实战 | 润和社区 | Hi3861驱动开发和测试 | L0 |
| BES2600W适配分享 | OpenHarmony社区 | BES2600W驱动适配 | L0 |
| RK3568适配指南 | OpenHarmony社区 | RK3568 L1系统驱动测试 | L1 |

## 4. IoT外设驱动文档和示例

| 材料名称 | 来源 | 用途 | 适用系统 |
|---------|------|------|:--------:|
| drivers_lite 仓库 | [GitCode](https://gitcode.com/openharmony/drivers_lite) | 轻量系统驱动源码 | L0 |
| drivers_framework 仓库 | [GitCode](https://gitcode.com/openharmony/drivers_framework) | HAL平台驱动接口定义（gpio_if.h等） | L0/L1 |
| IoT外设驱动子系统文档 | [GitCode](https://gitcode.com/openharmony/docs/) | IoT驱动开发指南 | L0 |
| device_soc_hisilicon | [GitCode](https://gitcode.com/openharmony/device_soc_hisilicon) | Hi3861 SoC适配参考 | L0 |

## 5. HAL接口定义

| 材料名称 | 来源 | 用途 | 适用系统 |
|---------|------|------|:--------:|
| kernel/liteos_m/kal/cmsis | [GitCode](https://gitcode.com/openharmony/kernel_liteos_m) | CMSIS-RTOS2接口定义 | L0 |
| foundation/lite | [GitCode](https://gitcode.com/openharmony/foundation_lite) | Lite系统基础服务接口 | L0 |
| 平台驱动头文件 | `drivers_framework/framework/include/platform/` | GPIO/I2C/SPI/UART等核心HAL接口 | L0/L1 |

## 6. 已有Lite驱动测试代码

| 仓库/目录 | 路径 | 内容 | 适用系统 |
|----------|------|------|:--------:|
| xts_tools/tests | `tests/hctest/` | HCTest框架自带测试用例 | L0/L1 |
| kernel_liteos_m/testsuites | `testsuites/cmsis/posix/io/` | CMSIS、POSIX、IO官方测试套件（iCunit断言） | L0 |
| kernel_liteos_a/testsuites | `testsuites/posix/drivers/` | IO、驱动、HID、存储测试（HWTest C++） | L1 |

## 7. 测试环境搭建指南

| 材料名称 | 来源 | 用途 | 归属需求 |
|---------|------|------|---------|
| DevEco Device Tool使用指南 | [华为开发者](https://developer.huawei.com/consumer/cn/doc/) | IDE + 烧录 + 串口调试 | → 08 适配文档生成器 |
| HiBurn烧录工具 | 海思官方 | Hi3861固件烧录 | → 08 |
| OpenOCD/J-Link调试 | 开源社区 | JTAG/SWD在线调试 | → 08 |
| build_lite编译指南 | [GitCode](https://gitcode.com/openharmony/build_lite) | 轻量系统编译构建 | → 04 编译构建配置器 |

## 8. 嵌入式测试技术

| 技术方向 | 代表工具/方法 | 适用性评估 |
|---------|-------------|-----------|
| **HCTest + iCunit** | L0混合模式（C，极低开销） | ⭐⭐⭐⭐⭐ L0首选 |
| **HWTest / gtest** | L1-Linux C++模式（HWTEST_F + EXPECT_*） | ⭐⭐⭐⭐⭐ L1-Linux 路线首选；L1-LiteOS-A 先按平台 acts 范式确认 |
| **Unity** | 超轻量C测试框架 | ⭐⭐⭐⭐ RAM极度受限时备选 |
| **基于模型的测试** | 状态机测试 | ⭐⭐⭐ 适合有明确状态机的驱动 |
| **模糊测试** | AFL++ (主机端) | ⭐⭐⭐ 主机端编译后Fuzz |
| **LLM辅助生成** | Claude/GPT | ⭐⭐⭐⭐ 理解接口语义生成测试 |
| **硬件在环(HIL)** | JTAG + 自动化 | ⭐⭐⭐⭐ 真机自动化验证 |

## 9. 术语表

| 缩写/术语 | 全称 | 说明 |
|----------|------|------|
| **LiteOS-M** | LiteOS Microcontroller | 轻量级微控制器内核（L0） |
| **LiteOS-A** | LiteOS Application | 轻量级应用处理器内核（L1） |
| **HCTest** | Harmony C Test | OpenHarmony 轻量/小型系统 C 测试框架（套件结构） |
| **iCunit** | — | LiteOS-M 内核自带的 C 单元测试框架（断言引擎） |
| **HWTest** | Huawei Test | OpenHarmony L1 测试框架（HWTEST_F = gtest TEST_F + 标签注册）；本包实证于 L1-Linux 路线，L1-LiteOS-A 需按平台确认 |
| **Unity** | Unity Test Framework | ThrowTheSwitch 超轻量C单元测试框架（380+ TEST_ASSERT_* 宏） |
| **gtest** | Google Test | Google C++测试框架（HWTest的底层引擎） |
| **CMSIS** | Cortex Microcontroller Software Interface Standard | ARM MCU软件接口标准 |
| **HAL** | Hardware Abstraction Layer | 硬件抽象层 |
| **IoT** | Internet of Things | 物联网（OpenHarmony IoT外设驱动子系统） |
| **HDI** | Hardware Device Interface | 硬件设备接口 |
| **XTS** | X Test Suite | OpenHarmony 生态认证测试套件 |
| **JTAG** | Joint Test Action Group | 联合测试行动组（调试接口） |
| **SWD** | Serial Wire Debug | 串行线调试（ARM调试协议） |
| **ISR** | Interrupt Service Routine | 中断服务程序 |
| **MCU** | Microcontroller Unit | 微控制器 |
| **MPU** | Microprocessor Unit | 微处理器 |
| **build_lite** | Build Lite | OpenHarmony轻量级编译构建系统 |
| **GN** | Generate Ninja | 构建系统元语言 |
| **LTO** | Link-Time Optimization | 链接时优化（减小代码体积） |
| **HIL** | Hardware In the Loop | 硬件在环测试 |
| **混合模式** | Hybrid Pattern | L0测试中HCTest提供结构 + iCunit提供断言的组合方式 |
