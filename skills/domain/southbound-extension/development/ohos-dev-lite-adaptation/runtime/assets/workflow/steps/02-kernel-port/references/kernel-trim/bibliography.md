# 参考资料汇总 — 内核裁剪配置器

---

## 1. OpenHarmony官方资料

| 资料 | 链接 | 说明 |
|------|------|------|
| OpenHarmony官方文档 | https://docs.openharmony.cn/ | 系统架构、内核概述、移植指南 |
| LiteOS-M内核仓库 | https://github.com/openharmony/kernel_liteos_m | 源码、Kconfig、README |
| LiteOS-A内核仓库 | https://github.com/openharmony/kernel_liteos_a | 源码、Kconfig、README |
| 内核概述文档 | https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/kernel/kernel-overview.md | 三种内核对比 |
| LiteOS-M概述 | https://gitcode.com/openharmony/docs/blob/master/en/device-dev/kernel/kernel-mini-overview.md | 轻量系统内核详情 |
| LiteOS-A概述 | https://gitcode.com/openharmony/docs/blob/master/en/device-dev/kernel/kernel-small-overview.md | 小型系统内核详情 |
| 产品兼容性规范 | https://oh-compatibility.obs.cn-south-1.myhuaweicloud.com/ | 认证必选组件清单 |

## 2. Kconfig与内核裁剪技术（Lite系统适用）

| 资料 | 链接 | 说明 |
|------|------|------|
| Kconfig语言参考 | https://docs.kernel.org/kbuild/kconfig-language.html | Kconfig语法规范（通用） |
| 鸿蒙轻内核Kconfig笔记 | https://blog.csdn.net/maniuT/article/details/139680572 | LiteOS Kconfig实践 |
| OpenHarmony build_lite仓库 | https://gitcode.com/openharmony/build_lite | Lite构建系统源码 |

## 3. 芯片平台资料（MCU/MPU级）

| 资料 | 链接 | 说明 |
|------|------|------|
| STM32官网 | https://www.st.com.cn/zh/microcontrollers-microprocessors/stm32-mainstream-mcus.html | STM32全系列规格 |
| ESP32-S3数据手册 | https://www.espressif.com/zh-hans/products/socs | 乐鑫SoC规格 |
| OpenHarmony STM32移植 | https://zhuanlan.zhihu.com/p/685230945 | STM32移植实践 |
| OpenHarmony BES2600W移植（GitCode 镜像） | https://gitcode.com/openharmony/docs/blob/master/en/device-dev/porting/porting-bes2600w-on-minisystem-display-demo.md | BES2600W移植指南 |
| **⭐ OpenHarmony BES2600W移植（Gitee 官方 — 中文完整版）** | [gitee.com/openharmony/docs](https://gitee.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/porting-bes2600w-on-minisystem-display-demo.md) | **BES2600W 完整移植教程（含内核裁剪与组件配置章节）** |
| Hi3861 WiFi IoT开发 | https://gitcode.com/openharmony/device_soc_hisilicon | 海思Hi3861 SoC适配 |
| XR806 RISC-V适配 | https://gitcode.com/openharmony/device_soc_allwinner | 全志XR806适配 |

## 4. 学术与行业研究（Lite系统相关）

| 资料 | 链接 | 说明 |
|------|------|------|
| LiteOS-M形式化验证 | https://link.springer.com/chapter/10.1007/978-3-032-26220-2_32 | 17000行C代码验证 |
| HarmonyOS内核核心技术 | https://www.harmonyos.com/resource/ppt/activity/sub-forum2/2021HDC-HarmonyOS-2-5.pdf | HDC2021内核技术演讲 |

## 5. 社区与实践（Lite系统相关）

| 资料 | 链接 | 说明 |
|------|------|------|
| OpenHarmony论坛 | https://forums.openharmony.cn/ | 裁剪讨论、问题解答 |
| LiteOS开发指南 | https://developer.huawei.com/consumer/cn/doc/31002 | 华为LiteOS官方开发指导 |
| HCIA-HarmonyOS培训教材 | https://www.scribd.com/document/699586435/HCIA-HarmonyOS-Device-Developer-V1-0 | 组件大小参考数据 |
