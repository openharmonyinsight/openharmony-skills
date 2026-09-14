# 代码审查示例集

> 本文件包含真实的OpenHarmony Lite驱动代码审查案例，展示完整的审查流程、问题分析和修复方案。Agent在生成审查报告时应参考这些示例的格式和深度。

---

## 1. 示例1：Hi3861 GPIO驱动审查（L0 IoT外设方式）

### 1.1 被审查代码

```c
/* hi3861_gpio.c - Hi3861 GPIO IoT外设驱动 */
#include "gpio_if.h"
#include "iot_gpio.h"
#include "los_typedef.h"

#define GPIO_MAX_PIN 22

static uint8_t g_gpioState[GPIO_MAX_PIN];
static uint8_t g_gpioDir[GPIO_MAX_PIN];

int32_t Hi3861GpioSetDir(uint16_t pin, enum GpioDir dir) {
    // 直接操作寄存器
    volatile uint32_t *reg = (volatile uint32_t *)(0x40005000 + pin * 4);
    *reg = dir;
    g_gpioDir[pin] = dir;
    return 0;
}

int32_t Hi3861GpioRead(uint16_t pin, uint8_t *val) {
    volatile uint32_t *reg = (volatile uint32_t *)(0x40005100 + pin * 4);
    *val = (*reg) & 0x1;
    return 0;
}

void Hi3861GpioIsr(uint32_t pin) {
    // 读取GPIO状态
    uint8_t val;
    Hi3861GpioRead(pin, &val);
    
    // BUG: ISR中打印日志
    printf("GPIO%d IRQ: %d\n", pin, val);
    
    // 更新状态
    g_gpioState[pin] = val;
}
```

### 1.2 审查报告

```markdown
# Hi3861 GPIO驱动代码审查报告

## 质量评分: 45/100 (F - 不合格)

| 维度 | 得分 | 问题数 |
|------|------|--------|
| 安全性 | 30/100 | 4 |
| 功能正确性 | 50/100 | 2 |
| 嵌入式优化 | 60/100 | 1 |
| 可维护性 | 55/100 | 2 |
| 规范性 | 40/100 | 2 |

---

## 🔴 BLOCKER (1)

### SEC-003: ISR中调用printf [Line 28]
**问题**: `printf`是阻塞式I/O函数，在ISR中使用将导致系统崩溃或严重延迟。
**修复**: 移除printf，使用标志位+任务处理模式。

---

## 🟠 CRITICAL (3)

### SEC-001: pin参数未校验 [Line 12, 19]
**问题**: `pin`参数未做范围检查，若pin≥22将越界访问g_gpioState/g_gpioDir数组和寄存器。
**修复**:
```c
if (pin >= GPIO_MAX_PIN) {
    return -1;
}
```

### SEC-004: ISR与任务共享g_gpioState未保护 [Line 31]
**问题**: `g_gpioState`在ISR中写入，可能在任务中被读取，存在竞态条件。
**修复**: 使用volatile修饰+临界区或原子操作。

### SEC-002: 寄存器地址硬编码 [Line 13, 20]
**问题**: 物理地址0x40005000硬编码，不利于跨平台移植。
**修复**: 通过头文件或设备配置传入基地址。

---

## 🟡 HIGH (2)

### FUNC-005: Hi3861GpioRead未检查val指针 [Line 19]
**问题**: val为NULL时将导致HardFault。
**修复**: 添加NULL检查。

### EMB-001: 未使用const优化 [Line 6-7]
**问题**: g_gpioState/g_gpioDir如果部分元素只读，可使用const放入Flash节省RAM。

---

## 🔵 MEDIUM (2)

### STYLE-001: 魔法数字0x40005000 [Line 13]
**问题**: 应定义为有意义的宏。

### MAINT-002: 缺少文件头版权注释
**问题**: 缺少OpenHarmony要求的Apache License文件头。
```

---

## 2. 示例2：STM32 UART驱动ISR安全审查

### 2.1 被审查代码

```c
/* stm32_uart.c - STM32F407 UART驱动 */
#include "uart_if.h"
#include "osal_mutex.h"

static struct OsalMutex g_uartLock;
static uint8_t g_rxBuf[256];
static volatile uint32_t g_rxHead = 0;

void Stm32UartRxIsr(uint32_t irq, void *data) {
    uint8_t byte = READ_REG(UART_DR);
    
    // BUG: ISR中获取mutex!
    OsalMutexLock(&g_uartLock);
    g_rxBuf[g_rxHead++] = byte;
    if (g_rxHead >= sizeof(g_rxBuf)) {
        g_rxHead = 0;
    }
    OsalMutexUnlock(&g_uartLock);
}
```

### 2.2 审查发现

```
🔴 BLOCKER SEC-003: ISR中使用OsalMutexLock
   → Mutex可能睡眠，在中断上下文中使用将导致HardFault
   → 修复: 使用环形缓冲区(lock-free)或spinlock

🟠 CRITICAL SEC-002: g_rxBuf[256]在ISR中操作
   → 若g_rxHead溢出将导致缓冲区越界
   → 修复: 使用取模运算确保head不越界
```

### 2.3 修复后代码

```c
/* 修复后：使用无锁环形缓冲区 */
#define RX_BUF_SIZE 256

static uint8_t g_rxBuf[RX_BUF_SIZE];
static volatile uint32_t g_rxHead = 0;  // ISR写入
static volatile uint32_t g_rxTail = 0;  // Task读取

void Stm32UartRxIsr(uint32_t irq, void *data) {
    uint8_t byte = READ_REG(UART_DR);
    
    uint32_t next = (g_rxHead + 1) % RX_BUF_SIZE;
    if (next != g_rxTail) {  // 环未满
        g_rxBuf[g_rxHead] = byte;
        g_rxHead = next;
    }
    // else: 环满丢弃，可设置溢出标志
}
```

---

## 3. 审查报告标准格式模板

Agent生成审查报告时应遵循以下结构：

```markdown
# [文件名] 代码审查报告

## 质量评分: XX/100 (等级)

| 维度 | 得分 | 问题数 |
|------|------|--------|
| 安全性 | XX/100 | N |
| 功能正确性 | XX/100 | N |
| 嵌入式优化 | XX/100 | N |
| 可维护性 | XX/100 | N |
| 规范性 | XX/100 | N |

---

## 🔴 BLOCKER (N)

### [规则ID]: [问题简述] [Line XX]
**问题**: [详细描述问题和风险]
**修复**: [具体修复方案和代码示例]

---

## 🟠 CRITICAL (N)

### [规则ID]: [问题简述] [Line XX]
...

---

## 🟡 HIGH (N)

### [规则ID]: [问题简述] [Line XX]
...

---

## 🔵 MEDIUM (N)

### [规则ID]: [问题简述] [Line XX]
...

---

## 💡 优化建议

### [EMB-XXX]: [优化简述]
**当前状况**: [描述现状]
**优化方案**: [具体建议和预期收益]
```

### 3.1 质量等级定义

| 分数范围 | 等级 | 含义 |
|---------|------|------|
| 90-100 | A | 优秀，可直接合入 |
| 80-89 | B | 良好，小幅修改后可合入 |
| 70-79 | C | 合格，需要修改后重新审查 |
| 60-69 | D | 不合格，需要较大改动 |
| <60 | F | 严重不合格，需要重写 |

### 3.2 严重度级别定义

| 级别 | 标记 | 含义 | 处理要求 |
|------|------|------|---------|
| BLOCKER | 🔴 | 必须修复才能合入 | 立即修复 |
| CRITICAL | 🟠 | 强烈建议修复 | 本次PR修复 |
| HIGH | 🟡 | 应该修复 | 本次或下次PR修复 |
| MEDIUM | 🔵 | 建议改进 | 视情况修复 |
| LOW | ⚪ | 可选优化 | 有空时改进 |

---

## 4. CI/CD集成配置示例

```yaml
# .ci/lite-code-review.yml
name: Lite Driver Code Review

on:
  pull_request:
    types: [opened, synchronize]
    paths:
      - 'device/soc/**/*.c'
      - 'device/board/**/*.c'
      - 'drivers/lite/**/*.c'
      - 'kernel/liteos_m/**/*.c'

jobs:
  lite-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install ARM Toolchain
        run: |
          sudo apt-get install gcc-arm-none-eabi
      - name: Compile with Stack Analysis
        run: |
          python build/lite/build.py product=${PRODUCT} \
            --gn-args enable_stack_usage=true
      - name: Run Lite Code Review
        run: |
          lite-review --mode=deep \
                     --system-level=L0 \
                     --misra-check \
                     --stack-analysis \
                     --memory-report \
                     --output=json,html,sarif \
                     device/soc/${VENDOR}/${CHIP}/
      - name: Quality Gate
        run: |
          SCORE=$(jq '.total_score' ./review-report/score.json)
          BLOCKERS=$(jq '.blocker_count' ./review-report/summary.json)
          STACK_ISSUES=$(jq '.stack_warnings' ./review-report/memory.json)
          if [ "$BLOCKERS" -gt 0 ] || [ "$SCORE" -lt 70 ] || [ "$STACK_ISSUES" -gt 0 ]; then
            echo "::error::Quality gate failed"
            exit 1
          fi
```
