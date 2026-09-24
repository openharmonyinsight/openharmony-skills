# 参考资料汇总 — RTOS迁移助手

> 来源：需求5分析报告 §11

---

## 1. 官方文档

| 资料 | 链接 | 说明 |
|------|------|------|
| OpenHarmony官方文档 | https://docs.openharmony.cn/ | 最新版本文档 |
| HDF驱动框架README | https://gitcode.com/openharmony/drivers_framework/blob/master/README.md | 框架概述 |
| HDF驱动编程规范 | https://gitcode.com/openharmony/docs/blob/master/zh-cn/contribute/OpenHarmony-hdf-coding-guide.md | 编码标准 |
| HDF Kernel/User Adapter | https://github.com/openharmony/drivers_adapter | 内核适配层 |
| Khdf Linux Adapter | https://gitcode.com/openharmony/drivers_adapter_khdf_linux | Linux内核HDF适配 |
| FreeRTOS官方文档 | https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/ | 内核特性文档 |
| RT-Thread文档中心 | https://www.rt-thread.org/document/site/ | 编程手册+API参考 |
| RT-Thread API参考 | https://www.rt-thread.org/document/api/ | 完整API列表 |
| Zephyr Device Model | https://docs.zephyrproject.org/latest/doxygen/html/group__device__model.html | 设备模型API |
| Zephyr Devicetree Guide | https://docs.zephyrproject.org/latest/build/dts/index.html | DT使用指南 |
| Linux Driver API Guide | https://www.kernel.org/doc/html/v5.8/driver-api/index.html | 驱动API参考 |

## 2. 技术文章与教程

| 资料 | 链接 | 说明 |
|------|------|------|
| OpenHarmony HDF OSAL详解 | https://cloud.tencent.com/developer/article/2532255 | OSAL接口完整分析 |
| HDF OSAL移植案例与原理 | https://zhuanlan.zhihu.com/p/715391676 | 知乎专栏深度分析 |
| HDF驱动加载过程分析 | https://zhuanlan.zhihu.com/p/716011047 | 驱动生命周期 |
| OpenHarmony外设驱动开发汇总 | https://laval.csdn.net/694a6147836da32144871712.html | GPIO/I2C/SPI等驱动 |
| 小型系统芯片移植指南 | https://cloud.tencent.com/developer/article/2534173 | LCD/TP/WLAN移植 |
| HDF GPIO驱动开发详解 | https://edu.51cto.com/article/note/9170.html | 标准系统GPIO实战 |
| HDC2021: HDF驱动框架解读 | https://developer.huawei.com/consumer/cn/blog/topic/03713165100620066 | 华为官方分享 |
| Porting RTOS Drivers to Linux | https://www.linuxjournal.com/article/7355 | RTOS↔Linux迁移经典文章 |
| FOSDEM 2026: Bringing OH to Phones | https://fosdem.org/2026/events/attachments/SYBWKY-bringing_openharmony_to_phones_lessons_from_the_oniro_porting_effort/slides/266916/fosdem_26_qczu0e8.pdf | Oniro移植经验 |

## 3. 代码转换技术研究

| 资料 | 链接 | 说明 |
|------|------|------|
| Leveraging ASTs for LLM-Assisted Code Manipulation | https://generativeai.pub/leveraging-asts-for-llm-assisted-source-code-manipulation-f06bd2f58ea1 | AST+LLM协同 |
| Code vs Serialized AST for LLM Summarization (2026) | https://paul-harvey.org/publication/2026-llm-ast-code-summary/2026-llm-ast-code-summary.pdf | LLM4Code 2026论文 |
| Improving LLM-Assisted Code Generation (ICSE 2026) | https://conf.researchr.org/details/icse-2026/designing-2026-papers/2/ | 架构文档辅助生成 |
| Ideas for LLM-Driven Code Migration | https://medium.com/@monojitchoudhury/ideas-for-llm-driven-code-migration-0455faa7a070 | LLM迁移实践 |
| Awesome Code LLM | https://github.com/codefuse-ai/awesome-code-llm | 代码LLM研究汇总 |

## 4. RTOS对比资料

| 资料 | 链接 | 说明 |
|------|------|------|
| FreeRTOS vs ThreadX vs Zephyr | https://www.iiot-world.com/industrial-iot/connected-industry/freertos-vs-threadx-vs-zephyr-the-fight-for-true-open-source-rtos/ | IIoT视角对比 |
| RT-Thread vs FreeRTOS核心差异 | https://openvela.csdn.net/69c3bc9854b52172bc6437d5.html | 国内视角对比 |
| RTOS Comparison (PDF) | https://sol.sbc.org.br/index.php/wso/article/download/36126/35913/ | 学术定量对比 |
| Switching to VxWorks from QNX | https://www.windriver.com/blog/Switching-Gears-Moving-Systems-to-VxWorks-from-QNX | Wind River迁移指南 |
| Zephyr Migration Guide v4.2 | https://docs.zephyrproject.org/latest/releases/migration-guide-4.2.html | Zephyr自身迁移经验 |
| Zephyr Device Driver Tutorial (2025) | https://www.digikey.fr/en/maker/tutorials/2025/introduction-to-zephyr-part-6-device-driver-development | DigiKey实战教程 |
