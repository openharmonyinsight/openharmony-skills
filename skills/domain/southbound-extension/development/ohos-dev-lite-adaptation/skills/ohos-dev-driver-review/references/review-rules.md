# 审查规则库

> 本文件定义了 OpenHarmony Lite 驱动代码审查的完整规则体系。每条规则包含ID、严重度、检测方法、修复建议和示例代码。Agent在审查时应按此规则逐条检查。

---

## 1. 规则分类体系

```
审查规则库（Lite版）
├── FUNC_功能正确性规则 (FUNC-001 ~ FUNC-030)
├── SEC_安全规则 (SEC-001 ~ SEC-060)
├── EMB_嵌入式优化规则 (EMB-001 ~ EMB-040)
├── MAINT_可维护性规则 (MAINT-001 ~ MAINT-020)
├── STYLE_规范规则 (STYLE-001 ~ STYLE-040)
└── MISRA_C_嵌入式安全规则 (MISRA-001 ~ MISRA-200)
```

---

## 2. FUNC — 功能正确性规则

### FUNC-001: HAL接口实现与声明一致性
- **严重度**: HIGH
- **描述**: 驱动的HAL接口实现必须与头文件声明完全一致（参数类型、返回值、const修饰）
- **检测方法**: 对比.c实现和.h声明的函数签名
- **修复**: 统一函数签名，以头文件为准

### FUNC-002: CMSIS接口合规性检查
- **严重度**: HIGH
- **描述**: L0系统的CMSIS接口实现必须符合CMSIS-RTOS2/CMSIS-Driver标准
- **检测方法**: 检查返回值类型(osStatus_t)、参数类型是否符合CMSIS定义
- **修复**: 参照CMSIS标准修正接口

### FUNC-003: 组件注册完整性
- **严重度**: MEDIUM
- **描述**: IoT外设驱动组件的方法表(Method结构体)中所有必需接口都已实现
- **检测方法**: 检查方法表中是否有NULL指针或未赋值的成员
- **修复**: 补全缺失的接口实现

### FUNC-004: 设备生命周期状态机完整性
- **严重度**: MEDIUM
- **描述**: 设备的Init/Deinit/Open/Close操作应形成完整的状态机，不允许非法状态转换
- **检测方法**: 分析状态转换路径，检查是否存在未初始化就使用、重复初始化等问题
- **修复**: 添加状态检查和状态转换保护

### FUNC-005: 返回值检查
- **严重度**: HIGH
- **描述**: 所有非void返回值的HAL/CMSIS API调用必须被检查
- **检测方法**: 搜索忽略返回值的函数调用
- **修复**: 添加返回值检查和错误处理

---

## 3. SEC — 安全规则

### SEC-001: 缓冲区边界校验
- **严重度**: CRITICAL
- **描述**: 所有memcpy/strcpy/数组访问前必须校验长度和索引范围
- **检测方法**: 数据流分析，检查数组索引是否有上界检查
- **修复**: 添加边界检查代码

### SEC-002: 栈溢出风险检测
- **严重度**: CRITICAL
- **描述**: 检测可能导致栈溢出的代码模式：局部大数组(>256字节)、深层递归、大量局部变量
- **分析方法**: `-fstack-usage` + 模式匹配
- **检测模式**:
  - `local_array_size > 256 in_function`
  - `recursive_call detected`
  - `function_stack_usage > task_stack_size * 0.5`
  - `isr_function with large_local_variables`
- **自动修复**: false（需要人工判断）

**违规示例：**
```c
void ProcessSensorData(void) {
    // BUG: 1KB局部数组在2KB栈的任务中将导致溢出
    uint8_t buffer[1024];
    ReadSensor(buffer, sizeof(buffer));
    Analyze(buffer, sizeof(buffer));
}
```

**修复示例：**
```c
// ✓ 使用静态缓冲区
static uint8_t g_sensorBuf[1024];

void ProcessSensorData(void) {
    ReadSensor(g_sensorBuf, sizeof(g_sensorBuf));
    Analyze(g_sensorBuf, sizeof(g_sensorBuf));
}

// ✓ 或使用堆分配（需检查返回值）
void ProcessSensorData_v2(void) {
    uint8_t *buf = OsalMemAlloc(1024);
    if (buf == NULL) {
        return;
    }
    ReadSensor(buf, 1024);
    Analyze(buf, 1024);
    OsalMemFree(buf);
}
```

### SEC-003: ISR安全（禁止阻塞调用）
- **严重度**: CRITICAL
- **描述**: 在中断服务程序(ISR)中调用可能阻塞的API将导致系统崩溃或死锁
- **适用文件**: `*.c`
- **禁止在ISR中使用的API**:
  - `OsalMsleep` / `LOS_TaskDelay` / `osDelay`
  - `OsalMutexLock` / `OsalMutexTimedLock` / `osMutexAcquire`
  - `OsalSemWait` / `osSemaphoreAcquire` (with timeout != 0)
  - `malloc` / `OsalMemAlloc`
  - `printf` / `HDF_LOGI` / `HDF_LOGW` / `HDF_LOGE`
  - 任何可能触发任务调度的API
- **替代方案**:
  - 使用 `OsalSpinLockIrqSave` 代替 mutex
  - 使用原子操作代替互斥锁
  - 使用信号量post(非wait)通知任务处理
  - 使用环形缓冲区暂存数据

**违规示例：**
```c
void UartRxIsr(uint32_t irq, void *data) {
    uint8_t byte = READ_REG(UART_RBR);
    
    // BUG: ISR中获取mutex → 系统崩溃
    OsalMutexLock(&g_rxLock);
    g_rxBuf[g_rxHead++] = byte;
    OsalMutexUnlock(&g_rxLock);
    
    // BUG: ISR中打印日志 → 可能阻塞
    HDF_LOGI("Received: 0x%02x", byte);
}
```

**修复示例：**
```c
void UartRxIsr(uint32_t irq, void *data) {
    uint8_t byte = READ_REG(UART_RBR);
    
    // ✓ 使用临界区或原子操作
    uint32_t next = (g_rxHead + 1) % RX_BUF_SIZE;
    if (next != g_rxTail) {
        g_rxBuf[g_rxHead] = byte;
        g_rxHead = next;
    }
    
    // ✓ 仅通知任务处理
    OsalSemPost(&g_rxSem);
}
```

### SEC-004: 共享数据保护（ISR↔Task）
- **严重度**: CRITICAL
- **描述**: ISR与任务间共享的变量必须有适当保护（volatile修饰+临界区或原子操作）
- **检测方法**: 数据流分析+上下文标注，识别ISR写入且任务读取的变量
- **修复**: 添加volatile修饰符和使用临界区/原子操作

### SEC-005: 中断优先级配置检查
- **严重度**: HIGH
- **描述**: 关键中断优先级配置正确，不存在优先级反转
- **检测方法**: NVIC配置分析
- **修复**: 调整NVIC优先级分组

### SEC-006: DMA缓冲区对齐检查
- **严重度**: HIGH
- **描述**: DMA传输缓冲区必须地址对齐且在正确的内存区域
- **检测方法**: 检查DMA缓冲区声明的对齐属性和内存区域
- **修复**: 使用`__attribute__((aligned(N)))`和正确的内存段

### SEC-007: Flash操作安全检查
- **严重度**: HIGH
- **描述**: Flash写入前必须先擦除；注意磨损均衡
- **检测方法**: 检查Flash写入前是否有对应的擦除调用
- **修复**: 添加擦除步骤和写入计数

### SEC-008: 看门狗配置检查
- **严重度**: HIGH
- **描述**: 确认看门狗已正确配置并在长循环中喂狗
- **检测模式**:
  - `while_loop without_watchdog_feed`
  - `for_loop_long_iteration without_watchdog_feed`
  - `watchdog_not_enabled_at_init`

**违规示例：**
```c
void MainLoop(void) {
    while (1) {
        ProcessData();    // 可能耗时很长
        WaitForEvent();   // 等待事件
        // BUG: 长时间无喂狗操作
    }
}
```

**修复示例：**
```c
void MainLoop(void) {
    WatchdogEnable(5000);  // 5秒超时
    
    while (1) {
        ProcessData();
        WatchdogFeed();     // ✓ 定期喂狗
        
        WaitForEventWithTimeout(1000);
        WatchdogFeed();     // ✓ 每次循环喂狗
    }
}
```

---

## 4. EMB — 嵌入式优化规则

### EMB-001: 代码大小优化（.text段）
- **严重度**: MEDIUM
- **描述**: MCU Flash空间有限，应关注代码大小优化
- **检查项**:
  - cflags是否包含`-Os`
  - cflags是否包含`-ffunction-sections -fdata-sections`
  - ldflags是否包含`-Wl,--gc-sections`
  - 是否存在未使用的函数
  - printf格式化字符串占用是否过大
- **建议**:
  - 启用`-Os`编译优化
  - 启用LTO (`-flto`)
  - 使用`-nano-specs`减小newlib体积
  - 移除未使用的printf格式化支持
  - 使用内联函数替代复杂宏

### EMB-002: RAM使用优化（.bss/.data段）
- **严重度**: MEDIUM
- **描述**: 检测RAM使用优化机会
- **建议**:
  - 将大数组改为const放入Flash (.rodata)
  - 使用位域(bitfield)压缩标志变量
  - 减小任务栈大小（基于栈分析结果）
  - 使用内存池替代动态分配
  - 裁剪非必要组件

### EMB-003: 栈使用优化
- **严重度**: HIGH
- **描述**: 基于-fstack-usage分析结果，优化函数栈消耗
- **检测方法**: 解析.su文件，对比任务栈大小

### EMB-004: 启动速度优化
- **严重度**: LOW
- **描述**: 减少不必要的初始化操作，支持延迟初始化
- **检测方法**: 分析Init函数中的操作

### EMB-005: 低功耗兼容性检查
- **严重度**: MEDIUM
- **描述**: 驱动未实现低功耗suspend/resume
- **修复模板**:
```c
// 进入低功耗前
int32_t DriverSuspend(struct Device *dev) {
    dev->savedConfig = READ_REG(CONFIG_REG);
    ClockDisable(dev->clockId);
    GpioSetLowPowerMode(dev->pin);
    return 0;
}

// 从低功耗唤醒后
int32_t DriverResume(struct Device *dev) {
    ClockEnable(dev->clockId);
    WRITE_REG(CONFIG_REG, dev->savedConfig);
    ReinitHardware(dev);
    return 0;
}
```

### EMB-006: Flash使用优化
- **严重度**: LOW
- **描述**: 检查只读数据是否放在Flash而非RAM
- **检测方法**: 检查缺少const修饰的只读数据

### EMB-007: 编译优化选项检查
- **严重度**: MEDIUM
- **描述**: 检查BUILD.gn中的编译优化选项是否合理

### EMB-008: ISR最小化
- **严重度**: HIGH
- **描述**: ISR仅做数据暂存和标志设置，耗时操作移至任务
- **修复模板**:
```c
// 优化后：ISR最小化
void SensorIsr(uint32_t irq, void *data) {
    struct SensorDev *dev = (struct SensorDev *)data;
    dev->rawValue = READ_REG(SENSOR_DATA);  // 仅读取寄存器
    dev->irqPending = true;                  // 设置标志
    OsalSemPost(&dev->processSem);           // 通知任务
}

// 任务中处理
void SensorTask(void *arg) {
    struct SensorDev *dev = (struct SensorDev *)arg;
    while (1) {
        OsalSemWait(&dev->processSem, OSAL_WAIT_FOREVER);
        ProcessSensorValue(dev->rawValue);   // 耗时处理在任务中
    }
}
```

---

## 5. MAINT — 可维护性规则

### MAINT-001: 圈复杂度超限
- **严重度**: MEDIUM
- **描述**: 函数圈复杂度超过10应拆分
- **检测方法**: AST分析计算圈复杂度

### MAINT-002: 函数过长
- **严重度**: MEDIUM
- **描述**: 单个函数不超过50行
- **检测方法**: 行数统计

### MAINT-003: 嵌套过深
- **严重度**: MEDIUM
- **描述**: 嵌套层级不超过4层
- **检测方法**: AST深度分析

### MAINT-004: 代码重复检测
- **严重度**: LOW
- **描述**: 检测高度相似的代码片段，建议提取公共函数
- **检测方法**: 文本相似度分析

---

## 6. STYLE — 规范规则

### STYLE-001: 命名规范检查
- **严重度**: LOW
- **描述**: 检查标识符命名是否符合OpenHarmony C语言编程规范
- **检测方法**: 正则匹配命名模式

### STYLE-002: 注释完整性检查
- **严重度**: LOW
- **描述**: 文件头版权注释、函数Doxygen注释完整性
- **检测方法**: 注释模板匹配

### STYLE-003: 文件格式规范
- **严重度**: LOW
- **描述**: 缩进4空格、行宽120字符、Allman大括号风格
- **检测方法**: 格式化检查

### STYLE-004: MISRA-C合规检查
- **严重度**: MEDIUM
- **描述**: 检查代码是否符合MISRA-C:2012核心规则子集
- **检测方法**: 规则引擎匹配

---

## 7. 常见Lite驱动Bug模式库

### 7.1 内存管理类（MCU特有）

| Bug模式 | 触发条件 | 检测方法 | 严重度 |
|---------|---------|---------|--------|
| 栈溢出 | 大数组/深递归/ISR嵌套 | `-fstack-usage` + 栈水位标记 | Critical |
| 堆耗尽 | 频繁malloc未释放 | 堆使用统计 + 数据流分析 | Critical |
| 内存踩踏 | 缓冲区溢出覆盖相邻变量 | 边界值分析 + Guard Pattern | Critical |
| 未初始化变量 | 局部变量未赋初值就使用 | 编译器-Wuninitialized + DFA | High |
| 静态数据过大 | .bss/.data段超出RAM | map文件分析 | High |

### 7.2 中断安全类（MCU特有）

| Bug模式 | 触发条件 | 检测方法 | 严重度 |
|---------|---------|---------|--------|
| ISR中调用阻塞API | OsalMsleep/mutex_lock等在ISR中 | API标注+上下文分析 | Critical |
| ISR过长 | ISR执行时间超过允许值 | 代码行数+复杂度估算 | High |
| 共享数据未保护 | ISR与任务间共享变量无critical section | 数据流+上下文标注 | Critical |
| 中断优先级错误 | 高优先级中断被低优先级阻塞 | NVIC配置分析 | High |
| 中断嵌套过深 | 多级中断嵌套导致栈溢出 | 中断优先级图分析 | High |

### 7.3 MCU硬件相关类

| Bug模式 | 触发条件 | 检测方法 | 严重度 |
|---------|---------|---------|--------|
| 看门狗未喂狗 | 长循环中无喂狗操作 | 循环分析+WDT API检查 | High |
| Flash磨损不均 | 频繁写入同一Flash扇区 | Flash写入点分析 | Medium |
| DMA缓冲区未对齐 | DMA传输到非对齐地址 | 地址对齐检查 | High |
| 时钟未使能 | 外设使用前未开启对应时钟 | 外设初始化序列检查 | High |
| 引脚复用冲突 | 多个外设共用同一引脚 | 引脚分配表交叉检查 | Medium |
| 低功耗唤醒失败 | 唤醒源未正确配置 | 低功耗进入/退出配对检查 | Medium |
