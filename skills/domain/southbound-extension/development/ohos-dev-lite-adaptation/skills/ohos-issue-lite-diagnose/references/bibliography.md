# 参考资料汇总 — 问题诊断修复器

---

## 1. OpenHarmony Lite调试相关文档

| 资源 | 链接 | 价值 |
|------|------|------|
| 轻量系统移植指导 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/) | 移植验证方法 |
| LiteOS-M内核文档 | [GitCode](https://gitcode.com/openharmony/kernel_liteos_m) | 内核调试API |
| build_lite文档 | [GitCode](https://gitcode.com/openharmony/build_lite) | 编译构建问题排查 |
| ARM Cortex-M Fault处理 | [ARM Docs](https://developer.arm.com/documentation/) | HardFault诊断参考 |

## 2. MCU调试工具指南

| 资源 | 链接 | 内容 |
|------|------|------|
| OpenOCD用户手册 | [openocd.org](https://openocd.org/doc/) | 开源JTAG调试 |
| ARM Cortex-M Debug Guide | [ARM Developer](https://developer.arm.com/) | Fault寄存器详解 |
| STM32调试指南 | [ST Wiki](https://wiki.st.com/) | ST-Link + CubeProgrammer |
| Hi3861烧录调试 | 润和社区 | HiBurn + 串口调试 |

## 3. Lite系统编译和链接问题案例

| 资源 | 链接 | 案例类型 |
|------|------|---------|
| STM32F407移植分享 | [博客园](https://www.cnblogs.com/openharmony/p/16381164.html) | 编译/链接/启动问题 |
| 从零移植OpenHarmony轻量系统 | [华为开发者联盟](https://developer.huawei.com/consumer/cn/blog/topic/03893164050570049) | 全流程移植问题 |
| 轻量级系统移植准备 | [掘金](https://juejin.cn/post/7506159639635312651) | 环境搭建问题 |
| Hi3861开发实战 | 润和社区 | WiFi/BLE适配问题 |

## 4. HardFault诊断专题

| 资源 | 链接 | 内容 |
|------|------|------|
| ARM Cortex-M HardFault调试 | [ARM Community](https://community.arm.com/) | CFSR寄存器详解 |
| STM32 HardFault排查 | [ST Forum](https://community.st.com/) | 实战案例集 |
| Embedded Fault Handling | [Embedded.fm](https://embedded.fm/) | 通用Fault处理框架 |

## 5. 故障排查决策树（完整版）

```
问题诊断入口
│
├── 编译阶段出错？
│   ├── 是 → 解析arm-gcc/riscv-gcc输出
│   │   ├── 头文件缺失 → 搜索头文件 → 添加include路径/Kconfig
│   │   ├── 语法/类型错误 → 检查CMSIS/HAL版本兼容性
│   │   └── build_lite错误 → 检查GN语法 → 验证deps/config.gni
│   └── 否 ↓
│
├── 链接阶段出错？
│   ├── 是 → 解析链接器输出
│   │   ├── undefined reference → 符号搜索 → 添加deps/修正链接顺序
│   │   ├── RAM溢出 → 分析map文件 → 裁剪组件/减小堆栈/启用LTO
│   │   ├── Flash溢出 → 分析map文件 → 移除未使用代码/-Os优化
│   │   └── multiple definition → 查找重复源 → weak属性/合并模块
│   └── 否 ↓
│
├── 启动阶段失败？
│   ├── 是 → 分析启动情况
│   │   ├── 完全无输出 → JTAG连接 → 检查启动代码/时钟/VTOR
│   │   ├── 部分输出后停 → 检查内存配置/中断初始化
│   │   ├── HardFault → 解析CFSR/HFSR/BFAR → 定位故障代码
│   │   └── 内核OK任务不跑 → 检查任务栈/优先级/调度器
│   └── 否 ↓
│
├── 运行时异常？
│   ├── 是 → 分析异常类型
│   │   ├── HardFault → JTAG读CFSR → backtrace → 修复
│   │   ├── 栈溢出 → 栈分析 → 增大栈/减小程序栈使用
│   │   ├── 看门狗复位 → 喂狗点分析 → 添加喂狗/修复死循环
│   │   └── 内存不足 → 堆统计 → 修复泄漏/增大堆
│   └── 否 ↓
│
└── 性能/功耗问题？
    ├── 中断延迟高 → GPIO计时 → ISR最小化
    ├── 功耗异常 → 电流测量 → 低功耗配置检查
    ├── Flash磨损 → 写入分布分析 → 磨损均衡
    └── 启动慢 → GPIO标记 → 并行化/延迟初始化
```

## 6. 多轮对话诊断示例

```
User: STM32F407移植后串口没有任何输出
Bot:  我来帮您诊断。请问以下信息：
      1. 您使用的是哪个OpenHarmony Lite版本？
      2. JTAG/SWD调试器是否可以连接到芯片？
      3. 串口的TX/RX引脚连接是否确认正确？
      4. 串口工具的波特率设置为多少？

User: OH 4.1 Release，有ST-Link可以连，引脚应该没问题，波特率115200

Bot:  🔍 诊断思路（按概率排序）
      
      **1. [40%] 启动代码中时钟配置错误**
      STM32F407需要正确配置PLL才能达到168MHz主频。
      如果外部晶振(HSE)未正确初始化，系统时钟可能停在默认HSI 16MHz，
      导致UART波特率计算错误。
      
      验证：用ST-Link连接，在SystemClock_Config()入口设断点，
      检查HSE是否ready(RCC_CR.HSERDY)。
      
      **2. [30%] UART引脚复用未配置**
      STM32F407需要配置GPIO的AF模式才能输出UART信号。
      
      验证：检查GPIO_AF配置是否正确（USART1_TX=PA9 AF7）。
      
      **3. [20%] 向量表偏移(VTOR)设置错误**
      如果使用自定义链接脚本，VTOR可能与实际Flash起始地址不匹配。
      
      验证：在JTAG中查看SCB->VTOR值是否与链接脚本中FLASH ORIGIN一致。
      
      **4. [10%] 串口硬件问题**
      TX/RX接反、USB转串口芯片故障等。
      
      ✅ 请先尝试第1项，告诉我JTAG中看到的情况。
```
