# 日志获取指南

> 本文件指导 OpenHarmony Lite（L0/L1）开发者在各种问题场景下获取诊断信息。
> **诊断的第一步不是分析日志，而是确保你能获取到有用的日志。**

---

## 1. 日志获取场景总览

| 问题场景 | 日志获取难度 | 关键挑战 | 推荐方法 |
|---------|------------|---------|---------|
| 编译/链接错误 | ⭐ 简单 | 获取完整错误信息 | `ninja -v` 完整输出 + map文件 |
| 启动有输出但中途停止 | ⭐⭐ 中等 | 最后几条日志可能丢失 | 串口捕获 + 添加checkpoint |
| 启动完全无输出 | ⭐⭐⭐ 困难 | 串口可能未初始化 | JTAG断点 + GPIO翻转标记 |
| HardFault | ⭐⭐⭐ 困难 | 串口可能已挂死 | Handler内寄存器dump + JTAG读取 |
| 运行时偶发crash | ⭐⭐⭐⭐ 很困难 | 不确定何时发生 | 环形日志缓冲区 + Watchdog复位前flush |
| 外设驱动异常 | ⭐⭐ 中等 | 时序相关 | 串口日志 + 逻辑分析仪辅助 |
| 功耗异常 | ⭐⭐ 中等 | 需要硬件测量 | 电流表 + 低功耗模式日志 |

---

## 2. 串口环境搭建（L0/L1通用）

### 2.1 硬件连接

```
目标板                 USB转TTL模块            PC
┌──────┐            ┌──────────┐         ┌──────┐
│  TX  │────────────│ RX       │         │      │
│  RX  │────────────│ TX       │───USB───│ 终端  │
│  GND │────────────│ GND      │         │ 工具  │
└──────┘            └──────────┘         └──────┘

注意：TX接RX，RX接TX（交叉连接），GND必须共地
```

### 2.2 终端工具选择

| 工具 | 平台 | 特点 | 推荐场景 |
|------|------|------|---------|
| PuTTY | Windows | 轻量、免费 | Windows日常调试 |
| MobaXterm | Windows | 功能丰富、支持SSH | Windows多功能需求 |
| minicom | Linux/Mac | 命令行、脚本化 | Linux开发环境 |
| screen | Linux/Mac | 极简、系统自带 | 快速连接 |
| picocom | Linux/Mac | 轻量、支持多种流控 | 推荐Linux/Mac首选 |

```bash
# Linux/Mac 快速连接
picocom -b 115200 /dev/ttyUSB0

# 或使用screen
screen /dev/ttyUSB0 115200

# 保存日志到文件
picocom -b 115200 /dev/ttyUSB0 | tee boot.log
```

### 2.3 串口配置要点

- **波特率**: 通常 115200bps（确认与固件一致）
- **数据位**: 8
- **停止位**: 1
- **校验**: None
- **流控**: None（硬件流控可能导致无输出）

---

## 3. 启动完全无输出的排查方法

### 3.1 排查思路

启动无输出是最常见也最棘手的问题，可能原因包括：
1. 串口硬件未连接或接线错误
2. 串口波特率不匹配
3. 程序根本没运行（Flash烧录失败、启动地址错误）
4. 程序运行了但在UART初始化前就crash了
5. UART初始化代码有bug

### 3.2 方法一：JTAG断点法（最可靠）

```bash
# 1. 连接JTAG调试器，启动OpenOCD
openocd -f interface/stlink.cfg -f target/stm32f4x.cfg

# 2. GDB连接并设置断点在Reset_Handler
arm-none-eabi-gdb firmware.elf
(gdb) target remote :3333
(gdb) break Reset_Handler
(gdb) continue

# 3. 如果能命中断点 → 程序确实在运行，问题在UART初始化
(gdb) break SystemInit
(gdb) break main
(gdb) break UartInit       # 或你的UART初始化函数名
(gdb) continue
# 逐步跳过，确认在哪一步失败

# 4. 如果无法命中断点 → 程序根本没运行
# 检查：Flash烧录是否成功、启动引脚配置、供电
```

### 3.3 方法二：GPIO翻转标记法（无JTAG时）

在代码最早的执行位置添加GPIO翻转，用逻辑分析仪或LED观察：

```c
// 在 Reset_Handler 或 SystemInit 的最开始添加
#define DEBUG_GPIO_PIN    (1 << 5)   // 例如 PA5
#define DEBUG_GPIO_PORT   GPIOA

// 最早的代码入口 — 翻转一次表示"程序开始运行"
DEBUG_GPIO_PORT->BSRR = DEBUG_GPIO_PIN;         // 置高

// UART初始化前 — 再翻转一次表示"即将初始化UART"
DEBUG_GPIO_PORT->BSRR = DEBUG_GPIO_PIN << 16;   // 置低

// UART初始化后 — 翻转表示"UART初始化完成"
DEBUG_GPIO_PORT->BSRR = DEBUG_GPIO_PIN;         // 置高

// 观察结果：
// - 如果PA5始终无变化 → 程序根本没运行（检查Flash/启动）
// - 如果PA5翻转一次后停止 → 跑到UART初始化前crash了
// - 如果PA5翻转两次 → UART初始化代码有bug
```

#### 3.3.1 LED/GPIO 里程碑定位法 — UART 未通时用 blink count 编码启动阶段

> **背景**：UART 还没通（或 UART 初始化前就 crash）时，GPIO 翻转标记法只能看"翻了几次"，信息量少。**用 GPIO blink count 编码启动里程碑**，一眼看出卡在哪个阶段，不用逻辑分析仪数翻转（LED 肉眼/万用表即可）。实测 hi3516cv610 裸烧/启动诊断用此法定位 bootrom → kernel → OHOS init 卡点。

**原理**：给每个启动阶段分配一个 blink count 编码，跑到该阶段就 blink 对应次数后停住（或继续）。数 LED 闪烁次数 = 卡点阶段。

```c
// 阶段编码（按启动顺序，count 递增）
#define STAGE_RESET         1   // reset entry / SystemInit 最早
#define STAGE_MAIN_ENTRY    2   // main() 入口
#define STAGE_KERNEL_INIT   3   // 内核初始化完成（LiteOS start）
#define STAGE_OHOS_INIT     4   // OHOS init / samgr 起来
#define STAGE_SCHEDULER     5   // 调度器跑起来，首个任务运行

// blink N 次编码阶段（阻塞式，确保肉眼可数）
void BlinkStage(uint8_t count) {
    for (uint8_t i = 0; i < count; i++) {
        GPIOx->BSRR = DEBUG_GPIO_PIN;        // 亮
        BusyDelay(200000);                    // ~200ms，肉眼可数
        GPIOx->BSRR = DEBUG_GPIO_PIN << 16;  // 灭
        BusyDelay(200000);
    }
    BusyDelay(800000);                        // 间隔 ~800ms 区分阶段
}

// 在各阶段 entry 调用：
// Reset_Handler 最早:    BlinkStage(STAGE_RESET);
// main():                BlinkStage(STAGE_MAIN_ENTRY);
// LOS_Start() 后:        BlinkStage(STAGE_KERNEL_INIT);
// OHOS init 入口:        BlinkStage(STAGE_OHOS_INIT);
// 首个任务运行:          BlinkStage(STAGE_SCHEDULER);
```

**HardFault 编码抓 crash 位置**：HardFault_Handler 里 blink 一个**特殊大数**（如 20 次）+ 把 PC/LR 的低 8 位也 blink 出来，区分"卡在某阶段"vs"crash 了"+ 抓 crash 地址：

```c
void HardFault_Handler(void) {
    uint32_t pc = get_stacked_pc();   // 从栈帧取 PC
    BlinkStage(20);                   // 20 次 = HardFault 标志
    BlinkStage((pc >> 0)  & 0xFF);    // PC 低 8 位
    BlinkStage((pc >> 8)  & 0xFF);    // PC 次 8 位
    BlinkStage((pc >> 16) & 0xFF);    // PC 高 8 位
    while (1);
}
// 观察：20 次闪烁 = crash 了；后面 3 组 0-255 闪烁 = PC 地址三段
```

**观察结果判读**：
| LED 现象 | 含义 | 下一步 |
|---------|------|-------|
| 完全不亮 | 程序根本没跑（Flash/启动/供电） | 查烧录/启动引脚/供电 |
| 闪 1 次停 | 卡在 reset entry（最早代码就挂） | 查启动代码/时钟/SP |
| 闪 2 次停 | 卡在 main entry 之前 | 查 SystemInit/时钟/外设初始化 |
| 闪 3 次停 | 内核 init 挂了 | 查内核 Kconfig/内存配置 |
| 闪 4 次停 | OHOS init 挂了 | 查 init.cfg/samgr/各 service |
| 闪 5 次后正常跑 | 启动全过，问题在运行时 | 查运行时异常 |
| 闪 20 次 | HardFault 了 | 后 3 组数字 = PC 地址，addr2line 定位 |

**教训**：
- ① **UART 未通时用 GPIO blink count 编码启动阶段**——比裸翻转信息量大，LED 肉眼/万用表可数，不用逻辑分析仪。
- ② **HardFault 编码特殊大数（如 20）+ blink PC 三段**——区分"卡阶段"vs"crash"+ 抓 crash 地址，UART 没通也能拿到 PC。
- ③ **blink 延迟要肉眼可数（~200ms 亮/灭，~800ms 阶段间隔）**——太快数不清，太慢浪费时间。
- ④ **关联**：见 `references/fault-knowledge-base.md` §5.3 看门狗复位诊断（也用 GPIO 翻转标记）；见 `skills/ohos-issue-lite-diagnose/SKILL.md` Step 2「add-debug-prints 标准步骤」。

### 3.4 方法三：ROM内固化的Bootloader日志

部分芯片（如Hi3861、STM32系统Bootloader）在上电时会自动输出固定格式的日志，与用户程序无关：

```
# Hi3861 上电时的ROM Bootloader输出（固定存在）
Bootrom start:
Bootrom Time: xxx
...

# 如果连这个都看不到 → 硬件问题（供电/复位/串口接线）
# 如果看到这个但没有LiteOS-M的输出 → 用户程序加载或初始化失败
```

---

## 4. HardFault现场捕获

### 4.1 方法一：在HardFault_Handler中dump寄存器

在启动代码或内核异常处理中添加以下代码，将关键寄存器值通过串口输出：

```c
// ARM Cortex-M HardFault Handler — 寄存器dump模板
void HardFault_Handler(void)
{
    // 1. 读取Fault状态寄存器
    volatile uint32_t cfsr  = SCB->CFSR;
    volatile uint32_t hfsr  = SCB->HFSR;
    volatile uint32_t dfsr  = SCB->DFSR;
    volatile uint32_t mmfar = SCB->MMFAR;
    volatile uint32_t bfar  = SCB->BFAR;

    // 2. 获取异常发生时的PC和LR（需要内联汇编）
    uint32_t stacked_pc, stacked_lr, stacked_psp;
    __asm volatile(
        "TST LR, #4        \n"
        "ITE EQ            \n"
        "MRSEQ R0, MSP     \n"
        "MRSNE R0, PSP     \n"
        "MOV %0, R0        \n"
        : "=r"(stacked_psp)
    );
    stacked_pc = ((uint32_t*)stacked_psp)[6];  // PC在栈帧偏移24
    stacked_lr = ((uint32_t*)stacked_psp)[5];  // LR在栈帧偏移20

    // 3. 通过串口输出（使用最底层的UART写，避免printf依赖）
    // 注意：此时系统可能已不稳定，直接UART输出最可靠
    UartDebugPrint("===== HARDFAULT =====\r\n");
    UartPrintHex("CFSR:  ", cfsr);
    UartPrintHex("HFSR:  ", hfsr);
    UartPrintHex("MMFAR: ", mmfar);
    UartPrintHex("BFAR:  ", bfar);
    UartPrintHex("PC:    ", stacked_pc);
    UartPrintHex("LR:    ", stacked_lr);
    UartDebugPrint("=====================\r\n");

    // 4. 死循环等待JTAG连接（不要复位，保留现场）
    while (1) {
        __NOP();
    }
}

// 辅助函数：直接UART输出32位十六进制值
void UartPrintHex(const char* label, uint32_t value)
{
    UartDebugPrint(label);
    char buf[12];
    // 简单实现：手动转hex
    buf[0] = '0'; buf[1] = 'x';
    for (int i = 9; i >= 2; i--) {
        buf[i] = "0123456789ABCDEF"[value & 0xF];
        value >>= 4;
    }
    buf[10] = '\r'; buf[11] = '\n';
    for (int i = 0; i < 12; i++) {
        while (!(READ_REG(UART_LSR) & LSR_THRE));
        WRITE_REG(UART_THR, buf[i]);
    }
}
```

### 4.2 方法二：JTAG在线读取（程序已挂死时）

```bash
# 当HardFault发生后，通过JTAG连接并读取寄存器
arm-none-eabi-gdb firmware.elf
(gdb) target remote :3333
(gdb) monitor halt

# 读取Fault寄存器
(gdb) print/x *(volatile uint32_t*)0xE000ED28   # CFSR
(gdb) print/x *(volatile uint32_t*)0xE000ED2C   # HFSR
(gdb) print/x *(volatile uint32_t*)0xE000ED34   # MMFAR
(gdb) print/x *(volatile uint32_t*)0xE000ED38   # BFAR

# 读取CPU寄存器
(gdb) info registers

# 查看调用栈
(gdb) backtrace

# 根据PC值定位源码
(gdb) list *0x08001234    # 替换为实际PC值
```

### 4.3 CFSR位域速查

| 位 | 名称 | 含义 | 常见原因 |
|----|------|------|---------|
| CFSR[0] | IACCVIOL | 指令访问违规 | 跳转到无效地址、MPU配置错误 |
| CFSR[1] | DACCVIOL | 数据访问违规 | MPU区域权限不匹配 |
| CFSR[3] | MUNSTKERR | MemManage出栈错误 | 栈被破坏、出栈时访问受保护区域 |
| CFSR[4] | MSTKERR | MemManage入栈错误 | 栈溢出、栈指针越界 |
| CFSR[7] | MMARVALID | MMFAR地址有效 | MMFAR包含触发fault的地址 |
| CFSR[8] | IBUSERR | 指令总线错误 | 访问不存在的Flash地址 |
| CFSR[9] | PRECISERR | 精确数据总线错误 | 访问未映射的外设地址 |
| CFSR[10] | IMPRECISERR | 非精确数据总线错误 | DMA访问无效地址 |
| CFSR[13] | BFARVALID | BFAR地址有效 | BFAR包含触发fault的地址 |
| CFSR[15] | STKERR | 总线入栈错误 | HardFault入栈时栈溢出 |
| CFSR[16] | UNSTKERR | 总线出栈错误 | 异常返回时栈被破坏 |
| CFSR[17] | IMPRECISERR | 非精确错误 | 非精确数据中止 |
| CFSR[31] | HARDFAULT | 强制HardFault | 上述错误的升级 |

---

## 5. 运行时crash的持续日志捕获

### 5.1 环形日志缓冲区

在RAM中维护一个环形缓冲区，记录最近的N条日志，crash时dump出来：

```c
// 环形日志缓冲区 — crash时保留最近的日志
#define RING_LOG_SIZE  1024  // 1KB环形缓冲区
static char g_ringLog[RING_LOG_SIZE];
static volatile uint16_t g_ringLogHead = 0;

// 写入环形日志（ISR安全，无锁）
void RingLog_Write(const char* msg)
{
    uint16_t len = 0;
    while (msg[len] && len < 64) len++;  // 限制单条最大64字节

    for (uint16_t i = 0; i < len; i++) {
        g_ringLog[g_ringLogHead] = msg[i];
        g_ringLogHead = (g_ringLogHead + 1) % RING_LOG_SIZE;
    }
    g_ringLog[g_ringLogHead] = '\n';
    g_ringLogHead = (g_ringLogHead + 1) % RING_LOG_SIZE;
}

// crash时dump环形缓冲区（在HardFault_Handler中调用）
void RingLog_Dump(void)
{
    UartDebugPrint("===== RING LOG DUMP =====\r\n");
    // 从head开始顺序输出（最近的日志在后面）
    for (uint16_t i = 0; i < RING_LOG_SIZE; i++) {
        uint16_t idx = (g_ringLogHead + i) % RING_LOG_SIZE;
        if (g_ringLog[idx]) {
            while (!(READ_REG(UART_LSR) & LSR_THRE));
            WRITE_REG(UART_THR, g_ringLog[idx]);
        }
    }
    UartDebugPrint("\r\n========================\r\n");
}
```

### 5.2 Watchdog复位前flush日志

```c
// 在Watchdog超时中断中，先flush日志再复位
void WDT_IRQHandler(void)
{
    // 1. 先输出关键状态
    UartDebugPrint("!!! WATCHDOG TIMEOUT !!!\r\n");
    UartPrintHex("Task: ", (uint32_t)LOS_CurTaskIDGet());

    // 2. dump环形日志
    RingLog_Dump();

    // 3. 再触发系统复位
    NVIC_SystemReset();
}
```

---

## 6. 编译链接错误的完整日志获取

```bash
# 获取完整编译日志（包含每条gcc命令）
ninja -v -C out/

# 保存编译日志
ninja -v -C out/ 2>&1 | tee build.log

# 获取map文件（链接器自动生成）
# 在BUILD.gn或链接脚本中确保有 -Wl,-Map=output.map

# 获取各段大小统计
arm-none-eabi-size -A firmware.elf

# 获取符号表（按大小排序，找RAM大户）
arm-none-eabi-nm --print-size --size-sort firmware.elf | tail -20

# 获取每函数栈使用量（编译时添加-fstack-usage）
cat *.su | sort -k2 -n -r | head -20
```

---

## 7. L0 vs L1 日志能力对比

| 日志能力 | L0 轻量系统 | L1 小型系统 |
|---------|-----------|-----------|
| printf/串口 | ✅ 主要手段 | ✅ 可用 |
| hdc | ❌ 不支持 | ⚠️ 有限支持 |
| hilog | ❌ 不支持 | ⚠️ 有限支持 |
| JTAG/SWD | ✅ 核心手段 | ✅ 可用 |
| crash dump | ❌ 无内核dump | ⚠️ 有限 |
| 环形日志 | ✅ 需要自己实现 | ⚠️ 可用hilog替代 |
| core dump | ❌ 不支持 | ❌ 不支持 |

> **关键建议**：L0系统必须在项目初期就搭建好串口日志 + JTAG调试环境，这是唯一可靠的诊断手段。不要等到出问题再临时搭建。

---

## 8. add-debug-prints 标准步骤 — 卡某阶段时拿错误码/寄存器值

> **背景**：启动/烧录卡在某阶段（bootrom/GSL/uboot 解压/uboot 运行/kernel 启动/OHOS init 任何阶段），静态排查 + 参数推断推不动时，在**该阶段对应的代码**加最小调试打印，重构建重烧看串口定位。这是通用诊断手段，不限 Uncompress Fail。实测 hi3516cv610 裸烧 0x81 靠加 `ret/err_info/PERI_CRG_GZIP 读回值` 三件套定位。

**标准步骤**：

```
卡在某阶段
  │
  ├── ① 定位该阶段代码最早处
  │     bootrom GSL → main.c / hw_compressed startup.c
  │     uboot       → board_init / start.S
  │     kernel      → start_kernel / 对应 init 函数
  │     OHOS init   → samgr / foundation entry
  │     找到该阶段"入口函数"或"返回值检查点"
  │
  ├── ② 用早期串口函数打印（不依赖后续初始化）
  │     uart_early_puts（bootrom/uboot 早期）
  │     printascii（kernel earlycon）
  │     printf（init 阶段，UART 已通）
  │     ❌ 别用依赖后续初始化的打印（如 hilog/完整 console）
  │
  ├── ③ 打印三件套：返回值 + 寄存器读回值 + 阶段 entry 标记
  │     uart_early_puts("STAGE: xxx entry\n");        // 阶段标记
  │     uart_early_puts_hex("ret=", ret);              // 函数返回值（十六进制）
  │     uart_early_puts_hex("reg=", READ_REG(PERI_CRG_GZIP));  // 关键寄存器读回值
  │
  ├── ④ 放死循环 while(1) 之前，阻塞式确保输出完
  │     uart_early_puts(...);   // 打印
  │     while (1);               // 死循环停住，确保串口输出完不丢
  │     ❌ 别在 ret-check 前无条件运行打印（可能改 stub 布局/时序导致 IP 挂死，见案例BG002 教训③）
  │
  ├── ⑤ 重构建重烧，串口读错误码
  │     ret=-1 → 超时类（时钟/路径/握手没成功）
  │     ret=-2+err 码 → CRC/格式错
  │     寄存器读回值 ≠ 写入值 → 时钟/配置没生效
  │     对照源码/解码表/NDA TRM 定位
  │
  └── ⑥ 解码 ret / 寄存器读回值 → 对照源码定位根因
        ret 对照 errno.h / 驱动返回码定义
        寄存器读回值对照 TRM 位域（NDA 寄存器查不到含义时走"标准产物对比"，见案例BG002 教训④）
```

**打印放置禁忌**（实测教训）：
- ❌ 在 ret-check 前无条件运行打印 — 可能改 stub 布局影响硬件 IP 时序（如 GZIP IP 挂死，见案例BG002 教训③）。
- ✅ 打印放在**返回后的 fail 分支内** — 只在失败时触发，不影响正常路径时序。
- ❌ 用依赖后续初始化的打印函数 — 阶段早期还没初始化，打印不出来。
- ✅ 用早期串口函数（`uart_early_puts` / `printascii`），和 `System startup` 同串口通路。

**关联**：
- `references/diagnostic-cases.md` §8 案例BG002（0x81 靠加打印三件套定位 + 打印放置踩坑）
- `skills/ohos-issue-lite-diagnose/SKILL.md` Step 2（获取诊断信息时卡阶段 → 走本标准步骤）

---

## 9. 日志获取决策树

```
问题发生
  │
  ├─ 有编译/链接错误？
  │   └─ 是 → ninja -v 获取完整日志 + map文件 + size -A
  │
  ├─ 启动无输出？
  │   └─ 是 → 有JTAG? ─是→ 断点Reset_Handler逐步排查
  │                  ─否→ GPIO翻转标记法 + 检查硬件接线
  │
  ├─ 启动有输出但中途停止？
  │   └─ 是 → 串口捕获完整输出 + 在最后打印位置后添加checkpoint
  │
  ├─ HardFault？
  │   └─ 是 → 有Handler dump代码? ─是→ 查看串口输出的寄存器值
  │                                 ─否→ JTAG连接读取CFSR/BFAR
  │
  ├─ 运行时偶发crash？
  │   └─ 是 → 部署环形日志缓冲区 + Watchdog复位前dump
  │
  └─ 外设/时序问题？
      └─ 是 → 串口日志 + 逻辑分析仪/示波器抓信号波形
```
