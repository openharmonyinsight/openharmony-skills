# Fault Quick Reference

> From ohos-issue-lite-diagnose/SKILL.md (C2 progressive disclosure)

## 问题摘要
- **问题类型**: <编译/链接/启动/驱动/运行时/功耗>
- **严重程度**: Critical / High / Medium / Low
- **匹配模式**: <FAULT-xxx-xxx>
- **置信度**: <百分比>

### 根因分析
<从 fault-knowledge-base.md 提取的根因描述 + 结合具体日志的分析>

### 修复方案
**方案 A（推荐）**：
<具体修复代码或配置修改，标注参考来源>

**方案 B**（如适用）：
<替代方案>

### 参考案例
<链接到 diagnostic-cases.md 中最接近的案例>
```

### Step 5: 深度定位（速查表无法覆盖时）

Read `references/debug-tools-guide.md`，使用以下工具链进行深度定位：

| 分析手段 | 适用场景 | 工具/命令 | 参考 |
|---------|---------|---------|------|
| **map 文件分析** | RAM/Flash 溢出定位大户 | `grep "\.o$" firmware.map \| sort -k2 -n -r \| head -20` | debug-tools-guide.md §3.4 |
| **符号表排序** | 找 RAM 占用最大的符号 | `arm-none-eabi-nm --print-size --size-sort firmware.elf \| tail -20` | debug-tools-guide.md §3.2 |
| **反汇编定位** | PC 地址→源码行 | `arm-none-eabi-objdump -d firmware.elf \| grep -A5 <address>` | debug-tools-guide.md §3.3 |
| **栈使用静态分析** | 找栈消耗最大的函数 | `cat *.su \| sort -k2 -n -r \| head -20` | debug-tools-guide.md §3.5 |
| **JTAG 在线调试** | HardFault 现场分析 | `break HardFault_Handler` → `print/x SCB->CFSR` → `backtrace` | debug-tools-guide.md §2.3 |
| **GPIO 翻转计时** | 启动耗时/ISR 延迟测量 | GPIO `BSRR` 翻转 + 示波器/逻辑分析仪 | log-acquisition-guide.md §3.3 |

**HardFault 深度分析**（ARM Cortex-M）：

Read `references/fault-knowledge-base.md` §3.3 和 `references/log-acquisition-guide.md` §4.3，解析 CFSR 寄存器位域：

| CFSR 关键位 | 位 | 含义 | 深度排查方向 |
|-----------|:--:|------|------------|
| **IACCVIOL** | 0 | 指令访问违规 | 检查 MPU 配置、跳转目标地址有效性 |
| **DACCVIOL** | 1 | 数据访问违规 | 检查 MPU 区域权限、外设地址映射 |
| **MUNSTKERR** | 3 | MemManage 出栈错误 | 栈被破坏、出栈时访问受保护区域 |
| **MSTKERR** | 4 | MemManage 入栈错误 | 栈溢出、栈指针越界 |
| **IBUSERR** | 8 | 指令总线错误 | 访问不存在的 Flash 地址、ECC 错误 |
| **PRECISERR** | 9 | 精确数据总线错误 | 访问未映射外设地址，**BFAR 包含故障地址** |
| **IMPRECISERR** | 10 | 非精确数据总线错误 | DMA 访问无效地址，PC 不一定指向出错指令 |
| **STKERR** | 15 | 总线入栈错误 | HardFault 入栈时栈溢出——最常见 |
| **UNSTKERR** | 16 | 总线出栈错误 | 异常返回时栈被破坏 |

> 以上位域定义来自 `log-acquisition-guide.md` §4.3（CFSR 位域表）和 `fault-knowledge-base.md` §3.3（HardFault 快速诊断 yaml）。

### Step 6: 生成修复方案

根据 Step 4/Step 5 的诊断结果，生成修复方案：

```
修复方案结构：
1. 问题定位（精确到文件和代码行或配置项）
2. 修复代码/配置 Before/After 对照
3. 修复原理说明（为什么这样修复）
4. 预防措施（如何防止再次出现）
5. 验证步骤（如何确认修复有效）
```

**各问题类别的修复模板参考**：

| 问题类别 | 修复方案模板来源 | 输出内容 |
|---------|---------------|---------|
| 编译错误 | `fault-knowledge-base.md` §1 + `diagnostic-cases.md` §1 | BUILD.gn include_dirs/deps 修正 / Kconfig 选项开启 / product.json 修改 |
| 链接错误 | `fault-knowledge-base.md` §2 + `diagnostic-cases.md` §2 | 依赖添加/组件裁剪/链接脚本修正/LTO 启用/nano-specs |
| 启动失败 | `fault-knowledge-base.md` §3 + `diagnostic-cases.md` §3 | VTOR 地址修正/时钟配置修正/栈大小调整/向量表重定位 |
| 运行时异常 | `fault-knowledge-base.md` §5 + `diagnostic-cases.md` §5 | 栈增大/静态分配替代/喂狗添加/FPU 启用/MPU 配置 |
| IoT 驱动 | `fault-knowledge-base.md` §4 + `diagnostic-cases.md` §4 | 操作函数表/组件注册补全/时钟 ID 修正/HAL init 修正 |

### Step 7: 修复后回归验证

修复方案生成后，引导用户完成验证闭环：

```
1. 重新编译
   → hb build 或 python build/lite/build.py product=<name>
   → 期望：0 错误 0 警告（或仅预期的 warning）

2. 重新烧录
   → 根据芯片型号选择烧录命令（MCP flash_commands_quick_ref）
   → 期望：烧录成功，校验通过

3. 抓取日志验证
   → 串口捕获启动日志
   → 期望：启动正常 + 原有错误不再出现 + 功能正常

4. 回归检查
   → 确认修复未引入新问题
   → 确认相关功能模块仍正常工作
```

**自动化验证闭环**（Agent 通过 Bash 工具执行）：

```bash
# 1. 编译
python build/lite/build.py product=<product_name> 2>&1 | tee verify_build.log

# 2. 检查编译结果
grep -E "error:|Error:" verify_build.log && echo "BUILD FAILED" || echo "BUILD OK"

# 3. 烧录（示例：STM32）
st-flash write firmware.bin 0x08000000

# 4. 抓取串口日志（30 秒超时）
timeout 30 picocom -b 115200 /dev/ttyUSB0 | tee verify_serial.log

# 5. 检查关键日志
grep -E "success|ready|ok|OS start" verify_serial.log
```

---

## ③ 故障速查

快速回忆用。完整知识库和案例见 references/。

### 6 大类故障速查索引

| 类别 ID | 类别名 | 覆盖条目 | 典型故障 ID | references/ 位置 |
|--------|-------|:------:|-----------|----------------|
| **COMP** | 编译错误 | 5 类（头文件/宏/GN/Kconfig/编译器） | FAULT-COMP-001~005 | `fault-knowledge-base.md` §1 + `diagnostic-cases.md` §1 |
| **LINK** | 链接错误 | 4 类（符号/段溢出/重复定义/C++不匹配） | FAULT-LINK-001~004 | `fault-knowledge-base.md` §2 + `diagnostic-cases.md` §2 |
| **BOOT** | 启动失败 | 4 类（无输出/半输出/HardFault启动/任务不跑） | FAULT-BOOT-001~004 | `fault-knowledge-base.md` §3 + `diagnostic-cases.md` §3 |
| **DRV** | 驱动问题 | 3 类（组件注册/HAL错误/CMSIS不兼容） | FAULT-DRV-001~003 | `fault-knowledge-base.md` §4 + `diagnostic-cases.md` §4 |
| **RUNTIME** | 运行时异常 | 6 类（HardFault/栈/看门狗/内存/BusFault/UsageFault） | FAULT-RUNTIME-001~006 | `fault-knowledge-base.md` §5 + `diagnostic-cases.md` §5 |
| **PERF** | 性能功耗 | 4 类（中断延迟/功耗/Flash磨损/启动慢） | FAULT-PERF-001~004 | `fault-knowledge-base.md` §6 + `diagnostic-cases.md` §6 |

### 编译错误速查（Top 5 最高频）

| ID | 错误模式 | 常见原因 | 快速修复 |
|----|---------|---------|---------|
| FAULT-COMP-001 | `fatal error: xxx.h: No such file or directory` | include_dirs 缺少路径；组件未在 product.json 启用 | BUILD.gn 补充 include_dirs；或 product.json 添加子系统 |
| FAULT-COMP-002 | `error: 'XXX_TYPE' undeclared` | Kconfig 选项未开启导致条件编译排除 | 在 Kconfig/menuconfig 中开启对应选项 |
| FAULT-COMP-003 | `implicit declaration of function 'xxx'` | 缺少头文件 60% / CMSIS 路径变更 25% / Kconfig 15% | 添加 `#include <对应头文件>`；更新 CMSIS include 路径 |
| FAULT-COMP-004 | `ERROR at //BUILD.gn:xx: Undefined identifier` | GN 变量未定义或 import 路径错误 | 检查 import 语句、确认 .gni 文件路径存在 |
| FAULT-COMP-005 | 条件编译排除了关键代码 | Kconfig 依赖链不完整 | 对照 06-kernel-trimmer 的 Kconfig 依赖规则补全 |

### 链接错误速查

| ID | 错误模式 | 常见原因 | 快速修复 |
|----|---------|---------|---------|
| FAULT-LINK-001 | `undefined reference to 'xxx'` | BUILD.gn deps 缺少库；链接顺序错误 | 在 deps 中添加符号所在库；调整链接顺序 |
| FAULT-LINK-002 | `region 'RAM' overflowed by N bytes` | 组件过多超出 MCU RAM | ①移除不需要组件 ②减缓冲池 ③启用 LTO ④nano-specs ⑤减小堆栈 |
| FAULT-LINK-003 | `region 'FLASH' overflowed by N bytes` | 代码+数据超出 Flash | ①-Os 优化 ②启用 LTO ③移除未使用代码 ④nano-specs |
| FAULT-LINK-004 | `multiple definition of 'xxx'` | 同一符号在多个 .o 中定义 | `__attribute__((weak))` 标记弱符号；合并重复模块 |

### HardFault CFSR 快速诊断

| CFSR 位模式 | 诊断结论 | 概率 | 典型场景 |
|-----------|---------|:--:|---------|
| **STKERR == 1** | 栈溢出 — 增大任务栈或减小局部变量 | 最高 | ISR 中定义了过大局部数组、任务栈 < 实际使用 |
| **PRECISERR == 1 && BFAR != 0** | 访问地址 {BFAR} 无效 | 高 | 外设地址映射错误、外设时钟未使能就访问寄存器 |
| **IBUSERR == 1** | 指令获取失败 | 中 | Flash 内容损坏、跳转到空地址、ECC 错误 |
| **UNDEFINSTR == 1** | 未定义指令 | 中 | FPU 未启用但用了浮点运算、函数指针损坏、代码段被覆盖 |
| **DIVBYZERO == 1** | 除零错误 | 低 | 除法运算前未检查除数 |
| **IMPRECISERR == 1** | 非精确总线错误 | 中 | DMA 访问无效地址、写缓冲中的错误 |

> 位域定义来源于 `log-acquisition-guide.md` §4.3 和 `fault-knowledge-base.md` §3.3。

### 启动失败决策树速查

```
完全无输出
├── 时钟配置错误（HSE/HSI/PLL 未正确初始化；检查 SystemClock_Config、外部晶振连接）
├── 向量表偏移 (VTOR) 设置错误（VTOR 与链接脚本中 FLASH ORIGIN 不匹配）
├── 串口引脚/波特率不匹配（TX 引脚复用、AF 模式配置、波特率与终端工具一致）
├── 固件烧录失败（Flash 目标地址错误、向量表为空 0xFF）
└── 硬件连接问题（供电/复位/接线；确认 JTAG 能否连接芯片）

部分输出后停止
├── 内存区域配置错误（LD 脚本中 RAM/FLASH 地址与实际硬件不匹配）
├── 中断控制器初始化失败（NVIC/PLIC 配置异常）
├── 堆初始化失败（HEAP 大小超过可用 RAM）
└── 内核对象初始化失败（Kconfig 配置不完整）
```

> 来源于 `fault-knowledge-base.md` §3.1（启动失败决策树）和 `diagnostic-cases.md` B001/B002。

### 芯片特有问题速判（3 颗芯片）

| 芯片 | 最高频问题 | 次高频 | 参考案例 |
|------|----------|--------|---------|
| **Hi3861** | WiFi 初始化超时（固件位置/SPI 异常） | Flash 读写异常（扇区未擦除） | diagnostic-cases.md §7.1 + D001 |
| **STM32F407** | RAM 溢出（启组件太多） | HardFault(STKERR) 栈溢出 / FPU 未启用 | diagnostic-cases.md §7.2 + B002 + R001 |
| **BES2600W** | 烧录后无法启动（BOOT 引脚错误） | 显示花屏（MIPI 时序不匹配） | diagnostic-cases.md §7.3 + B001 |

> 来源于 `diagnostic-cases.md` §7 芯片特有问题清单。

### L0 vs L1 调试能力对比

| 调试能力 | L0 轻量系统（MCU） | L1 小型系统（MPU） |
|---------|:---:|:---:|
| printf/串口 | ✅ 主要手段 | ✅ 可用 |
| JTAG/SWD | ✅ 核心手段 | ✅ 可用 |
| hdc | ❌ 不支持 | ⚠️ 有限支持（shell + file send） |
| hilog | ❌ 不支持 | ⚠️ 有限支持（基本日志过滤） |
| gdb 远程调试 | ✅ via OpenOCD | ✅ |
| ASan/Valgrind | ❌ | ❌ |
| perf | ❌ | ❌ |
| 内核 crash dump | ❌ | ⚠️ 有限 |
| 环形日志缓冲区 | ✅ 需自行实现 | ⚠️ 可用 hilog 替代 |

> 来源于 `log-acquisition-guide.md` §7 和 `debug-tools-guide.md` §5.2。

### 常用调试命令速查

| 用途 | 命令 | 参考 |
|------|------|------|
| 完整编译日志 | `ninja -v -C out/ 2>&1 \| tee build.log` | log-acquisition-guide.md §6 |
| 各段大小 | `arm-none-eabi-size -A firmware.elf` | debug-tools-guide.md §3.1 |
| 符号按大小排 | `arm-none-eabi-nm --print-size --size-sort firmware.elf \| tail -20` | debug-tools-guide.md §3.2 |
| 反汇编函数 | `arm-none-eabi-objdump -d firmware.elf \| sed -n '/<func>:/,/^$/p'` | debug-tools-guide.md §3.3 |
| 找 RAM 大户 | `grep "\.o$" firmware.map \| sort -k2 -n -r \| head -20` | debug-tools-guide.md §3.4 |
| 栈使用分析 | `cat *.su \| sort -k2 -n -r \| head -20`（需 `-fstack-usage` 编译） | debug-tools-guide.md §3.5 |
| CFSR 读取 | `print/x *(volatile uint32_t*)0xE000ED28`（JTAG GDB） | debug-tools-guide.md §2.3 |
| JTAG HardFault 断点 | `break HardFault_Handler` → `continue` → `backtrace` | debug-tools-guide.md §2.3 |
| 串口捕获 | `picocom -b 115200 /dev/ttyUSB0 \| tee boot.log` | log-acquisition-guide.md §2.2 |

