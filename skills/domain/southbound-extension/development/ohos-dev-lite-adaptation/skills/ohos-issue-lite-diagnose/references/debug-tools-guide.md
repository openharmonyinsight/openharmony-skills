# 调试工具指南

> 本文件介绍 OpenHarmony Lite（L0/L1）开发中可用的全部调试工具和使用方法。由于Lite系统资源受限，调试手段比标准系统有限得多，掌握这些工具是高效排查问题的关键。

---

## 1. 串口调试（L0/L1通用，最基础）

### 1.1 基本用法

```c
// LiteOS-M中使用printf输出调试信息
#include <stdio.h>

void DebugPrint(const char *tag, const char *msg) {
    printf("[%s] %s\n", tag, msg);
}

// 更轻量的方式：直接UART输出（避免printf开销）
void UartDebugPrint(const char *str) {
    while (*str) {
        while (!(READ_REG(UART_LSR) & LSR_THRE));  // 等待发送缓冲区空
        WRITE_REG(UART_THR, *str++);
    }
}
```

### 1.2 串口调试注意事项

- **波特率**: 通常115200bps，确认与终端工具设置一致
- **printf开销**: printf本身占用栈空间和执行时间，ISR中禁止使用
- **输出频率**: 高频输出会影响实时性，生产版本应移除或条件编译
- **缓冲**: 部分实现有缓冲，异常时可能丢失最后几条日志

### 1.3 L1小型系统的hilog

```bash
# L1小型系统可使用hdc和hilog（功能有限）
hdc list targets              # 列出已连接设备
hdc shell                     # 进入设备shell
hdc file send <local> <remote> # 推送文件
hdc shell hilog               # 抓取系统日志
hdc shell hilog -T tag         # 按标签过滤

# 注意：L0轻量系统不支持hdc/hilog
```

---

## 2. JTAG/SWD调试器（L0核心调试手段）

### 2.1 调试器选择

| 调试器 | 适用芯片 | 功能 | 价格 |
|--------|---------|------|------|
| J-Link | ARM Cortex-M全系列 | 断点、单步、内存查看、RTOS感知 | $$$ |
| ST-Link V2 | STM32系列 | 断点、单步、Flash编程 | $$ |
| DAPLink | ARM Cortex-M | 开源、CMSIS-DAP协议 | $ |
| RV-Link | RISC-V | Hi3861/XR806等RISC-V MCU | $$ |
| ESP-Prog | ESP32/RISC-V | 低成本RISC-V调试 | $ |

### 2.2 JTAG/SWD核心调试能力

- 设置硬件断点和观察点
- 查看/修改寄存器和内存
- 读取ARM Fault寄存器（CFSR/HFSR/BFAR/MMFAR）
- RTOS感知调试（查看任务列表、栈使用情况）
- Flash编程和校验
- 实时追踪（ETM/ITM，部分MCU支持）

### 2.3 HardFault标准化调试流程

```yaml
tool_guide:
  name: "JTAG/SWD HardFault调试"
  purpose: "通过JTAG/SWD调试器定位MCU HardFault根因"
  prerequisites:
    - "JTAG/SWD调试器已连接到目标板"
    - "OpenOCD或IDE调试会话已建立"
    - "固件带有调试符号(-g选项)"
  steps:
    - step: 1
      action: "在HardFault_Handler中设置断点"
      command: "break HardFault_Handler"
    - step: 2
      action: "运行程序直到触发HardFault"
      command: "continue"
    - step: 3
      action: "读取Fault状态寄存器"
      command: |
        print/x *(volatile uint32_t*)0xE000ED28  # CFSR
        print/x *(volatile uint32_t*)0xE000ED2C  # HFSR
        print/x *(volatile uint32_t*)0xE000ED38  # BFAR
        print/x *(volatile uint32_t*)0xE000ED34  # MMFAR
    - step: 4
      action: "读取关键CPU寄存器"
      command: "info registers"
    - step: 5
      action: "根据CFSR位域判断Fault类型并定位源码"
      description: "参见fault-knowledge-base.md中的HardFault快速诊断"
    - step: 6
      action: "查看调用栈回溯"
      command: "backtrace"
```

### 2.4 OpenOCD常用命令

```bash
# 启动OpenOCD
openocd -f interface/stlink.cfg -f target/stm32f4x.cfg

# GDB连接
arm-none-eabi-gdb firmware.elf
(gdb) target remote :3333
(gdb) monitor reset halt
(gdb) load
(gdb) continue

# 读取内存
(gdb) x/16xw 0x20000000   # 查看RAM起始16个字
(gdb) print/x SCB->CFSR   # 读取CFSR寄存器

# 设置断点
(gdb) break main
(gdb) break gpio_driver.c:45
(gdb) watch g_rxHead       # 数据观察点
```

---

## 3. arm-gcc/riscv-gcc 工具链分析

### 3.1 size — 分析bin文件各段大小

```bash
# 基本统计
arm-none-eabi-size firmware.elf
# 输出: text  data  bss  dec  hex  filename

# 详细分段统计
arm-none-eabi-size -A firmware.elf
# 输出每个段的独立大小

# 按大小排序
arm-none-eabi-size -A --format=sysv firmware.elf | sort -k2 -n -r
```

### 3.2 nm — 查看符号表和地址

```bash
# 按地址排序
arm-none-eabi-nm -n firmware.elf

# 按大小排序（需要--print-size）
arm-none-eabi-nm --print-size --size-sort firmware.elf

# 查找特定符号
arm-none-eabi-nm firmware.elf | grep GpioOpen
```

### 3.3 objdump — 反汇编分析

```bash
# 完整反汇编
arm-none-eabi-objdump -d firmware.elf > disassembly.txt

# 带源码的反汇编（需要-g编译）
arm-none-eabi-objdump -S firmware.elf > source_disasm.txt

# 反汇编特定函数
arm-none-eabi-objdump -d firmware.elf | sed -n '/<GpioOpen>:/,/^$/p'
```

### 3.4 map文件分析

```bash
# map文件由链接器生成，包含：
# - 每个段的起始地址和大小
# - 每个符号的地址和大小
# - 内存区域使用情况

# 查找最大的.o文件贡献者
grep "\.o$" firmware.map | sort -k2 -n -r | head -20

# 查找特定符号的位置
grep "GpioOpen" firmware.map
```

### 3.5 GCC -fstack-usage — 静态栈分析

```bash
# 编译时添加-fstack-usage
arm-none-eabi-gcc -fstack-usage -c gpio_driver.c -o gpio_driver.o
# 生成 gpio_driver.su 文件

# .su文件格式:
# gpio_driver.c:45:13:GpioProcessData  256  static
# gpio_driver.c:78:13:GpioIsrHandler   64   static
# gpio_driver.c:120:6:GpioInit         32   static

# 找出栈消耗最大的函数
cat *.su | sort -k2 -n -r | head -20
```

### 3.6 内核符号验用 — vmlinux 而非 zImage/uImage

> **背景**：裸烧/启动诊断常需验证内核某符号是否存在、地址是多少（如对照 `BINDER_IPC_32BIT` 是否编进内核、binder ioctl 符号、某驱动 init 函数地址）。**必须用未压缩的 `vmlinux`，不能用 `zImage`/`uImage`**。

**为什么不能用 zImage/uImage**：
- `zImage`/`uImage` 是压缩产物（gzip/lz4 + 自解压 stub），`strings` / `nm` / `addr2line` 在压缩数据上**验不全**——符号表被压缩，`nm` 查不到符号、`strings` 抓不到符号名、`addr2line` 解不出源码行。
- 只有未压缩的 `vmlinux`（ELF，带完整 .symtab/.strtab）才能完整 `nm` / `addr2line` / `objdump -t` 验符号。

**正确做法**：

```bash
# 用 vmlinux（ELF，未压缩，带符号表）验内核符号
arm-linux-ohos-nm vmlinux | grep binder_ioctl          # 验符号是否存在 + 地址
arm-linux-ohos-nm vmlinux | grep BINDER_IPC_32BIT      # 验宏/符号是否编进
arm-linux-ohos-addr2line -e vmlinux 0xc0186201         # ioctl 命令码/地址 → 源码行
arm-linux-ohos-objdump -t vmlinux | grep -i binder     # 完整符号表查 binder 相关

# ❌ 错误：用 zImage/uImage（压缩产物，验不全）
arm-linux-ohos-nm zImage       # 查不到符号（符号表被压缩）
strings zImage | grep binder   # 抓不全（压缩数据里 strings 不连续）
```

**vmlinux 在哪**：内核构建产物里，通常在 `out/<product>/kernel/` 或 `kernel/linux-<ver>/vmlinux`（未压缩 ELF）。zImage/uImage 是 vmlinux 经 `objcopy` + 压缩后的烧录镜像。诊断时**保留 vmlinux 别删**，是验内核符号的唯一可靠输入。

**教训**：
- ① **验内核符号/地址 → 用 vmlinux（ELF 未压缩）**，别用 zImage/uImage（压缩产物 `nm`/`strings`/`addr2line` 验不全）。
- ② **zImage 压缩导致 strings 验不全**——看到 `strings zImage` 抓不到某符号别断定"内核没编这个"，换 vmlinux 再验。
- ③ **关联**：见 `references/diagnostic-cases.md` §9 案例OH001（验 `BINDER_IPC_32BIT` 是否编进内核）—— 这类验证必须用 vmlinux。

---

## 4. 其他Lite调试辅助工具

| 工具 | 用途 | 适用系统 |
|------|------|---------|
| 逻辑分析仪 | 外设信号时序分析（I2C/SPI/UART波形） | L0/L1 |
| 电流表/功率计 | 功耗测量、低功耗模式验证 | L0/L1 |
| 万用表 | 引脚电平验证、电源检查 | L0/L1 |
| 示波器 | 信号完整性、时序精确测量 | L0/L1 |

---

## 5. 调试策略总结

### 5.1 问题定位优先级

```
1. 串口日志 → 最快获取信息，但可能不完整
2. JTAG/SWD → 最强大，可查看所有寄存器和内存
3. GPIO翻转标记 → 简单有效的时序分析手段
4. 编译工具链分析 → size/nm/map/su静态分析
5. 逻辑分析仪/示波器 → 外设信号级问题
6. 电流表 → 功耗问题专用
```

### 5.2 L0 vs L1 调试能力对比

| 调试能力 | L0轻量系统 | L1小型系统 |
|---------|-----------|-----------|
| printf/串口 | ✅ | ✅ |
| JTAG/SWD | ✅ | ✅ |
| hdc | ❌ | ⚠️ 有限支持 |
| hilog | ❌ | ⚠️ 有限支持 |
| gdb远程调试 | ✅ (via OpenOCD) | ✅ |
| ASan/Valgrind | ❌ | ❌ |
| perf | ❌ | ❌ |
| 内核crash dump | ❌ | ⚠️ 有限 |
