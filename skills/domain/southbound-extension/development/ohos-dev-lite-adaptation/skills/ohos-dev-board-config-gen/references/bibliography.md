# 参考资料汇总

## OpenHarmony Lite官方文档

| 文档 | 链接 | 说明 |
|------|------|------|
| 轻量系统移植指导 | [docs/porting/Readme-CN.md](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/Readme-CN.md) | L0/L1芯片移植流程，含配置目录结构 |
| HDF驱动开发流程（L1参考） | [driver-hdf-manage.md](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/driver/driver-hdf-manage.md) | HCS语法、配置管理概述（L1精简版适用） |
| 平台驱动开发示例 | [device-driver-demo.md](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/guide/device-driver-demo.md) | 完整的驱动开发示例 |
| build_lite构建系统 | [gitcode.com/openharmony/build_lite](https://gitcode.com/openharmony/build_lite) | 轻量级编译构建系统源码 |
| drivers_lite轻量系统驱动 | [gitcode.com/openharmony/drivers_lite](https://gitcode.com/openharmony/drivers_lite) | L0轻量系统驱动实现参考 |
| OpenHarmony官方文档站 | [docs.openharmony.cn](https://docs.openharmony.cn/) | 最新文档索引 |

## 技术社区文章

| 文章 | 链接 | 重点内容 |
|------|------|---------|
| HCS配置语法详解 | [juejin.cn/post/7459013216112754738](https://juejin.cn/post/7459013216112754738) | delete、template、match_attr详解 |
| HDF驱动框架-驱动配置(2) | [zhuanlan.zhihu.com/p/715598798](https://zhuanlan.zhihu.com/p/715598798) | 节点复制、属性引用、模板继承完整示例 |
| HDF配置管理分析及使用 | [51cto.com/article/681341](https://www.51cto.com/article/681341.html) | hc-gen实现原理、HCB编译过程 |
| OpenHarmony 3.2 HCS新特性 | [cnblogs.com/openharmony/p/17445423](https://www.cnblogs.com/openharmony/p/17445423.html) | 宏式解析、配置生成新特性 |
| HDF驱动框架介绍及加载分析 | [zhuanlan.zhihu.com/p/716011047](https://zhuanlan.zhihu.com/p/716011047) | 设备信息与设备资源配置详解 |
| HDF驱动框架概览 | [zhuanlan.zhihu.com/p/675734693](https://zhuanlan.zhihu.com/p/675734693) | HCS→HCB→Parser完整流程 |
| 硬件适配之HCS应用 | [blog.csdn.net/m0_64420071/article/details/137246929](https://blog.csdn.net/m0_64420071/article/details/137246929) | 实际适配案例 |
| HDF平台驱动框架及适配 | [elecfans.com/d/1710381](https://www.elecfans.com/d/1710381.html) | 平台驱动适配方法论 |

## 代码仓库

| 仓库 | 链接 | 说明 |
|------|------|------|
| drivers_framework | [gitcode.com/openharmony/drivers_framework](https://gitcode.com/openharmony/drivers_framework) | HDF框架源码，含hc-gen和HCS Parser（L1参考） |
| drivers_lite | [gitcode.com/openharmony/drivers_lite](https://gitcode.com/openharmony/drivers_lite) | L0轻量系统驱动实现 |
| device_soc_hisilicon | [gitcode.com/openharmony/device_soc_hisilicon](https://gitcode.com/openharmony/device_soc_hisilicon) | 海思芯片SoC适配（Hi3861/Hi3516等） |
| device_board_hisilicon | [gitcode.com/openharmony/device_board_hisilicon](https://gitcode.com/openharmony/device_board_hisilicon) | 海思开发板适配 |
| build_lite | [gitcode.com/openharmony/build_lite](https://gitcode.com/openharmony/build_lite) | 轻量级编译构建系统 |

## OpenHarmony 移植案例（完整工作流参考）

| 案例 | 链接 | 覆盖内容 |
|------|------|---------|
| **⭐ BES2600W Mini系统带屏移植（官方完整教程）** | [Gitee 官方](https://gitee.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-bes2600w-on-minisystem-display-demo.md) / [GitHub 镜像](https://github.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-bes2600w-on-minisystem-display-demo.md) | 内核移植→HCS配置→设备树→构建配置（含 config.json/BUILD.gn 实例） |

## MCU设备配置技术参考

| 工具/资料 | 链接 | 参考价值 |
|-----------|------|---------|
| CMSIS-SVD标准 | [arm-software.github.io/CMSIS_5/SVD](https://arm-software.github.io/CMSIS_5/SVD/html/index.html) | MCU外设描述标准，可辅助配置生成 |
| STM32CubeMX | [st.com/stm32cubemx](https://www.st.com/en/development-tools/stm32cubemx.html) | ST官方引脚配置工具，设计理念参考 |
| Zephyr Devicetree | [docs.zephyrproject.org/devicetree](https://docs.zephyrproject.org/latest/build/dts/) | RTOS设备树方案，与L0场景类似 |

## 视频教程

| 教程 | 链接 | 说明 |
|------|------|------|
| HDF驱动开发教程 | [bilibili.com/video/BV1sTdWYQEvD](https://www.bilibili.com/video/BV1sTdWYQEvD/) | 含HCS配置文件详解 |
