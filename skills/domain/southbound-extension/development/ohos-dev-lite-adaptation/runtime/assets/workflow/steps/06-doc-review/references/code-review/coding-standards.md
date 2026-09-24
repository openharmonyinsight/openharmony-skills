# LiteOS-M/A 编码规范 + MISRA-C 规则

> 本文件汇总了 OpenHarmony Lite（L0/L1）驱动代码应遵循的全部编码规范，包括OpenHarmony通用C语言规范、LiteOS-M/A特有规范和MCU级安全编码规范。

---

## 1. C语言编程规范（Lite通用）

来源：[OpenHarmony C语言编程规范](https://gitcode.com/openharmony/docs/blob/master/zh-cn/contribute/OpenHarmony-c-coding-style-guide.md)

### 1.1 命名规范

| 规则编号 | 规则描述 | 级别 | 示例 |
|---------|---------|------|------|
| R-1 | 标识符使用英文单词或公认缩写，禁止拼音 | 必须 | `GpioOpen` ✅ / `DaKaiGpio` ❌ |
| R-2 | 结构体名使用大驼峰（UpperCamelCase） | 必须 | `struct GpioMethod` ✅ |
| R-3 | 函数名使用小驼峰（lowerCamelCase） | 必须 | `GpioSetDir()` ✅ |
| R-4 | 宏/常量使用全大写+下划线分隔 | 必须 | `GPIO_MAX_PIN` ✅ |
| R-5 | 局部变量使用小写+下划线或驼峰 | 建议 | `pin_count` / `pinCount` |
| R-6 | 全局变量加`g_`前缀 | 建议 | `g_gpioState[]` |
| R-7 | 静态变量加`s_`或`g_`前缀 | 建议 | `static uint8_t g_buf[256]` |

### 1.2 格式规范

| 规则编号 | 规则描述 | 级别 |
|---------|---------|------|
| R-5 | 缩进使用4个空格，禁止Tab | 必须 |
| R-6 | 单行不超过120字符 | 必须 |
| R-8 | 大括号独占一行（Allman风格） | 必须 |
| R-9 | 运算符两侧加空格 | 必须 |
| R-10 | 逗号后加空格 | 必须 |

### 1.3 注释规范

| 规则编号 | 规则描述 | 级别 |
|---------|---------|------|
| R-7 | 文件头注释必须包含版权许可声明 | 必须 |
| R-11 | 函数头使用Doxygen风格注释 | 建议 |
| R-12 | 复杂逻辑添加行内注释说明意图 | 建议 |
| R-13 | TODO/FIXME/HACK标记需附带负责人和日期 | 建议 |

### 1.4 函数规范

| 规则编号 | 规则描述 | 级别 |
|---------|---------|------|
| R-8 | 单个函数不超过50行 | 必须 |
| R-9 | 嵌套层级不超过4层 | 必须 |
| R-14 | 参数个数不超过6个 | 建议 |
| R-15 | 所有非void返回值必须被检查 | 必须 |

### 1.5 文件头模板

```c
/*
 * Copyright (c) 2024 OpenHarmony Contributors
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
```

---

## 2. LiteOS-M/A 特有编码规范

### 2.1 栈管理规范

| 规则 | 描述 | 审查要点 |
|------|------|---------|
| 栈大小检查 | 每个任务的栈大小必须合理设置 | 检查LOSCFG_TASK_STACK_SIZE配置 |
| 局部数组限制 | 局部数组不超过256字节，超过应使用静态分配 | 搜索函数内大数组声明 |
| 禁止递归 | MCU上应避免递归调用 | 检测函数自调用或间接递归 |
| ISR栈最小化 | ISR中局部变量尽量少 | ISR函数栈使用<128字节 |

### 2.2 中断安全规范

| 规则 | 描述 | 审查要点 |
|------|------|---------|
| ISR禁阻塞 | ISR中只能使用ISR-safe的API | 检查ISR中的函数调用黑名单 |
| 共享数据保护 | ISR与任务间共享变量必须有适当保护 | 检查volatile/critical section/spinlock |
| ISR最短原则 | ISR仅做数据暂存和标志设置 | ISR代码行数<20行 |
| 中断优先级 | 关键中断优先级配置正确 | 检查NVIC优先级分组 |

**ISR禁止调用的API黑名单：**
- `OsalMsleep` / `LOS_TaskDelay` / `osDelay`
- `OsalMutexLock` / `osMutexAcquire`
- `OsalSemWait` / `osSemaphoreAcquire` (timeout != 0)
- `malloc` / `OsalMemAlloc` (某些实现中可能阻塞)
- `printf` / `HDF_LOGI/W/E` (串口输出可能阻塞)
- 任何可能触发任务调度的API

**ISR替代方案：**
- 使用 `OsalSpinLockIrqSave` 代替 mutex
- 使用原子操作代替互斥锁
- 使用信号量post(非wait)通知任务处理
- 使用环形缓冲区暂存数据

### 2.3 内存管理规范

| 规则 | 描述 | 审查要点 |
|------|------|---------|
| 优先静态分配 | MCU上优先使用静态分配 | 检查malloc/OsalMemAlloc使用 |
| 动态分配检查 | 动态分配必须检查返回值 | 检查NULL判断 |
| 配对释放 | 每次分配必须有对应的释放 | 数据流分析 |
| 避免碎片化 | 固定大小分配使用内存池 | 检查频繁不同大小的malloc |

### 2.4 Kconfig规范

| 规则 | 描述 | 审查要点 |
|------|------|---------|
| 功能开关 | 功能开关通过Kconfig控制 | 检查硬编码的条件编译 |
| 依赖声明 | Kconfig选项必须声明依赖 | 检查depends on语句 |
| 默认值 | 合理的默认值设置 | 检查default值 |

### 2.5 CMSIS合规规范

| 规则 | 描述 | 审查要点 |
|------|------|---------|
| L0接口标准 | L0系统接口应符合CMSIS标准 | 检查是否直接使用私有API |
| 返回值检查 | CMSIS API返回值(osStatus_t)必须检查 | 检查osOK判断 |
| 类型一致 | 使用CMSIS定义的类型 | 检查osThreadId_t等类型使用 |

### 2.6 低功耗兼容规范

| 规则 | 描述 | 审查要点 |
|------|------|---------|
| suspend/resume | 驱动应支持低功耗模式进入/退出 | 检查suspend/resume实现 |
| 时钟管理 | 低功耗前关闭外设时钟 | 检查ClockDisable调用 |
| 引脚状态 | 低功耗时配置引脚为最低漏电模式 | 检查GPIO模拟模式设置 |
| 状态保存 | 保存外设配置以便恢复 | 检查寄存器值保存/恢复 |

### 2.7 看门狗友好规范

| 规则 | 描述 | 审查要点 |
|------|------|---------|
| 喂狗覆盖 | 长循环中应有喂狗操作 | 检查while(1)等无限循环 |
| 超时合理 | 看门狗超时时间不应太短 | 检查WatchdogSetTimeout值 |
| 阻塞等待 | 阻塞式等待中需要喂狗 | 检查等待循环 |

---

## 3. MCU级安全编码规范

| 安全域 | 规则 | 违规风险 |
|--------|------|---------|
| 缓冲区安全 | 所有memcpy/strcpy前必须校验长度 | 缓冲区溢出→HardFault |
| 栈安全 | 局部数组大小不超过栈空间限制 | 栈溢出→HardFault |
| 整数安全 | 乘法运算前检测溢出 | 内存分配错误→越界访问 |
| 指针安全 | 所有外部传入指针使用前检查NULL | NULL解引用→HardFault |
| 中断优先级 | 关键中断优先级配置正确 | 优先级反转→实时性丢失 |
| DMA安全 | DMA缓冲区地址对齐、非缓存区域 | 数据不一致→功能异常 |
| Flash安全 | Flash写入前擦除，注意磨损均衡 | 数据丢失→系统不可用 |
| 寄存器安全 | 使用volatile修饰外设寄存器指针 | 编译器优化导致读写丢失 |
| 位操作安全 | 使用位掩码而非硬编码数值 | 可维护性差、易出错 |

---

## 4. MISRA-C:2012 核心规则摘要

以下为嵌入式MCU代码最关键的MISRA-C规则子集：

### 4.1 强制规则（Must）

| 规则ID | 描述 | Lite相关性 |
|--------|------|-----------|
| Rule 11.3 | 不在指向不同类型的指针之间进行转换 | ⭐⭐⭐ DMA/寄存器操作常见违规 |
| Rule 11.4 | 不在指向对象的指针和整数类型之间转换 | ⭐⭐⭐ 物理地址映射需注意 |
| Rule 11.5 | 不将void指针转换为对象指针 | ⭐⭐ 驱动回调参数常见 |
| Rule 12.1 | 表达式中运算符优先级明确 | ⭐⭐⭐ 位运算必须加括号 |
| Rule 13.5 | &&和\|\|右操作数无持久性副作用 | ⭐⭐⭐ 短路求值安全 |
| Rule 14.3 | 不变表达式不应用于控制条件 | ⭐⭐ 死代码检测 |
| Rule 15.6 | if/else/for/while/do体必须是复合语句(花括号) | ⭐⭐⭐ 防止悬挂else |
| Rule 15.7 | else if终止必须有最终else | ⭐⭐ 完整性检查 |
| Rule 17.2 | 函数不应直接或间接调用自身 | ⭐⭐⭐ MCU禁止递归 |
| Rule 17.7 | 非void返回值不应被丢弃 | ⭐⭐⭐ HAL返回值必须检查 |

### 4.2 建议规则（Should）

| 规则ID | 描述 | Lite相关性 |
|--------|------|-----------|
| Rule 8.7 | 仅在一个翻译单元中使用的对象/函数应为static | ⭐⭐⭐ 减小链接体积 |
| Rule 8.13 | 指针参数尽可能声明为const | ⭐⭐ 防御性编程 |
| Rule 10.1 | 不使用基本类型的隐式转换 | ⭐⭐ 类型安全 |
| Rule 11.9 | NULL宏应用于空指针常量 | ⭐⭐ 可读性 |
| Rule 12.2 | 移位量不超过操作数位宽 | ⭐⭐⭐ 32位MCU常见 |
| Rule 14.4 | 控制表达式应为布尔类型 | ⭐⭐ 可读性 |
| Rule 16.2 | switch标签仅在复合语句最外层 | ⭐⭐ 防止fall-through |
| Rule 17.3 | 函数应有原型声明 | ⭐⭐⭐ 类型检查 |

---

## 5. 代码质量评分模型（Lite版）

```
                    Lite代码质量评分模型
                    
    ┌─────────────────────────────────────────┐
    │           总分 = Σ(维度分 × 权重)         │
    ├─────────────┬────────┬──────────────────┤
    │ 维度         │ 权重   │ 评分要素          │
    ├─────────────┼────────┼──────────────────┤
    │ 安全性       │ 30%   │ ISR安全通过率     │
    │             │        │ 栈安全达标率       │
    │             │        │ 缓冲区安全检查     │
    ├─────────────┼────────┼──────────────────┤
    │ 功能正确性   │ 25%   │ HAL接口合规率     │
    │             │        │ CMSIS接口合规率   │
    │             │        │ 错误处理完备度     │
    ├─────────────┼────────┼──────────────────┤
    │ 嵌入式优化   │ 20%   │ 代码大小合理性    │
    │             │        │ RAM使用效率       │
    │             │        │ 低功耗兼容性       │
    ├─────────────┼────────┼──────────────────┤
    │ 可维护性     │ 15%   │ 圈复杂度达标率     │
    │             │        │ MISRA-C合规率     │
    │             │        │ 注释覆盖率         │
    ├─────────────┼────────┼──────────────────┤
    │ 规范性       │ 10%   │ Lite编码规范通过率 │
    │             │        │ L0/L1正确区分     │
    │             │        │ 文档完整度         │
    └─────────────┴────────┴──────────────────┘
```
