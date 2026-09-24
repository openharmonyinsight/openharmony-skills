# 参考资料汇总 — 代码审查与优化器

---

## 1. OpenHarmony Lite官方文档

| # | 文档名称 | 链接 |
|---|---------|------|
| 1 | OpenHarmony C语言编程规范 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/contribute/OpenHarmony-c-coding-style-guide.md) |
| 2 | OpenHarmony C&C++安全编程指南 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/contribute/OpenHarmony-c-cpp-secure-coding-guide.md) |
| 3 | LiteOS-M内核源码 | [GitCode](https://gitcode.com/openharmony/kernel_liteos_m) |
| 4 | 轻量系统移植指导 | [GitCode](https://gitcode.com/openharmony/docs/blob/master/zh-cn/device-dev/porting/) |
| 5 | drivers_lite仓库 | [GitCode](https://gitcode.com/openharmony/drivers_lite) |

## 2. 嵌入式安全编码参考

| # | 资料 | 链接 |
|---|------|------|
| 6 | MISRA C:2012 Guidelines | https://www.misra.org.uk/misra-c/ |
| 7 | CERT C Coding Standard | https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard |
| 8 | ARM Cortex-M Programming Guide to Memory Barriers | https://developer.arm.com/documentation/ |
| 9 | Embedded C Coding Standard (Barr Group) | https://barrgroup.com/embedded-systems/books/embedded-c-coding-standard |

## 3. 静态分析工具

| # | 工具 | 链接/说明 |
|---|------|----------|
| 10 | Cppcheck Manual | http://cppcheck.net/manual.pdf |
| 11 | Clang Static Analyzer | https://clang-analyzer.llvm.org/ |
| 12 | GCC Stack Usage Analysis | https://gcc.gnu.org/onlinedocs/gcc/Developer-Options.html |
| 13 | ARM Code Size Optimization Guide | https://developer.arm.com/documentation/ |

## 4. CMSIS接口标准

| 资源 | 链接 |
|------|------|
| CMSIS-RTOS2文档 | https://arm-software.github.io/CMSIS_6/latest/RTOS2/ |

## 5. 嵌入式C语言静态分析工具对比

| 工具 | 适用场景 | 规则数量 | Lite相关能力 |
|------|---------|---------|-------------|
| **Cppcheck** | 开源轻量级 | 400+ | MISRA C合规、缓冲区溢出、未初始化变量 |
| **Clang Static Analyzer** | LLVM生态 | 100+ | 数据流分析、NULL检查、自定义Checker |
| **MISRA-C Checker** | 嵌入式安全 | 200+ | MISRA C:2012/C:2023合规检查 |
| **PC-lint Plus** | 嵌入式专用 | 500+ | 轻量级、适合MCU项目、MISRA支持 |
| **Polyspace** | 形式化验证 | - | 运行时错误证明、适合安全关键MCU代码 |
| **Coverity** | 企业级 | 1000+ | 内存泄漏、竞态条件、NULL解引用 |

> ⚠️ **重要补充**：对于Lite系统（尤其是L0），应增加以下嵌入式专用检查工具：
> - **MISRA-C检查器**：确保代码符合汽车/医疗/工业级嵌入式安全标准
> - **栈分析工具**：GCC `-fstack-usage` 生成每函数栈使用量
> - **代码大小分析**：`arm-none-eabi-size` / `riscv32-unknown-elf-size` 分析各段大小
