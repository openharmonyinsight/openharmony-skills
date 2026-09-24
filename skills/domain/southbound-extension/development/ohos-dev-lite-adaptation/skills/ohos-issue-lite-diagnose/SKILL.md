---
name: ohos-issue-lite-diagnose
description: OpenHarmony Lite (L0/L1) 问题诊断修复器——环境检测→编译→烧录→抓日志→分析→修复→回归验证全链路诊断，输出带根因分析和修复方案的结构化诊断报告。Use when an OpenHarmony Lite adaptation hits any failure and a structured root-cause analysis is needed; triggers include 编译报错、链接错误、undefined reference、RAM/Flash 溢出、启动失败、烧录后无输出、HardFault、栈溢出、看门狗复位、IoT 组件注册失败、功耗异常、binder EINVAL、samgr 卡死、/dev 节点缺失、XTS 用例失败、良性报错判别、"这个报错要不要管"。解析 ARM Cortex-M CFSR/HFSR/BFAR 故障寄存器和 RISC-V mcause/mtval 异常码。
metadata:
  author: openharmony
  scope: domain
  stage: troubleshooting
  domain: lite
  capability: diagnose
  version: 0.1.0
  status: trial
---

# OpenHarmony Lite 问题诊断修复

## Trigger Signals

出现以下信号时应触发本 skill：

| 信号类型 | 典型表达 |
|---------|---------|
| 拿到报错日志 | "编译报了这个错"、"链接 undefined reference"、"串口打到一半停了"、"HardFault 了"、"0x81 是什么" |
| 现象描述（隐性需求） | "启动没输出"、"烧录后起不来"、"板子反复重启"、"跑着跑着挂了"、"XTS 用例 0/40"、"这个 EACCES 报错要不要管" |
| L1 OH init 阶段卡点 | binder `ioctl EINVAL/-22`、samgr boot step 卡死、`/dev/xxx No such file`、`Error relocating: symbol not found` |
| 单点咨询调试方法 | "怎么抓 HardFault 现场"、"CFSR 怎么解析"、"JTAG 怎么连"、"mcause 含义" |
| 下游 skill 链式调用 | ohos-ci-lite-deploy-burn / ohos-test-lite-adapt-verify 验证失败后转诊断；ohos-dev-kernel-node-adapt 定位缺 /dev 节点 |

**不触发**（明确排除）：环境从零搭建（走 oh-lite-setup / ohos-dev-build-config）；纯代码审查不出故障（走 ohos-dev-driver-review）；健康系统上的功能开发。

---

## Scope

本 SKILL 是 OpenHarmony Lite（L0 轻量系统 / L1 小型系统）芯片适配的**问题诊断修复层**：覆盖从环境准备到修复验证的全链路——自动检测硬件连接和工具就绪状态、执行编译→烧录→串口日志捕获、按故障分类决策树判定问题类型、匹配常见故障速查表（6 大类 30+ 故障模式）定位根因、生成修复方案、修复后自动回归验证。

**本 SKILL 做诊断分析 + 修复方案生成 + 自动化验证闭环，不自动修改代码**（修复由用户确认后在 Agent 辅助下手动完成）。

### 诊断覆盖清单

| 问题大类 | 覆盖子类 | 输入 | 诊断方式 | 适用系统 |
|---------|---------|------|---------|:---:|
| **编译错误** | 头文件缺失/宏未定义/arm-gcc兼容性/GN配置错误/Kconfig依赖缺失 | arm-gcc/riscv-gcc stderr + build_lite 输出 | 规则匹配 + 知识库 | L0/L1 |
| **链接错误** | undefined reference/RAM溢出/Flash溢出/重复定义/C++链接不匹配 | 链接器 stderr + map 文件 | 符号搜索 + 内存布局分析 | L0/L1 |
| **启动失败** | 完全无输出/部分输出后停止/内核init成功但任务不运行 | 串口日志（或无输出） | 启动流程决策树 + JTAG 引导 | L0/L1 |
| **驱动问题** | IoT 组件注册失败/HAL 接口返回错误/CMSIS 接口不兼容 | 串口日志 + 返回值 | 组件状态机分析 + HAL 实现检查 | L0 特有 |
| **运行时异常** | HardFault/栈溢出/看门狗复位/内存不足/BusFault/UsageFault | JTAG 寄存器 + CFSR/HFSR/BFAR + 串口日志 | Fault 类型解析 + 栈分析 + 源码定位 | L0/L1 |
| **性能功耗** | 中断延迟高/功耗异常/Flash 磨损/启动速度慢 | 电流测量/GPIO翻转计时/示波器 | 低功耗配置检查 + ISR 最小化 | L0/L1 |
| **OHOS init/服务启动**（L1） | binder ioctl EINVAL/samgr boot step 卡死/`/dev/xxx` No such file（mknod 陷阱）/musl ld 用错版本全 service 符号缺失 | 串口日志（user 态）+ 内核 vmlinux 验符号 | 协议位宽对齐 + 驱动 device_create + ld/libc 配套 + runtime 证据优先 | L1 |

## Initial Checks

进入诊断前按以下顺序先做判断（各步结论决定走哪条路径）：

1. **意图判断**（Step 0 决策树）：自动化验证环路 / 单点诊断（已有日志直接从 Step 3 起）/ 调试方法咨询（单点查询 references）/ 不明确 → 追问芯片型号 + L0/L1 + 现象。
2. **系统级别判定（L0/L1）**：决定调试能力差异——L0 无 hdc/hilog（仅串口 + JTAG），L1 hdc/hilog 有限支持 + user 态日志。判错级别会用错诊断手段。
3. **诊断信息完备性盘点**：编译错误要有 `ninja -v` 完整输出 + map；HardFault 要有 CFSR/HFSR/BFAR + PC/LR + 栈指针；启动失败要确认"是否有任何输出"（含 ROM Bootloader 日志）。缺 → 按 Step 2 先取日志，不带病分析。
4. **日志版本核对**（多轮迭代时，Step 2.3）：拿到日志先 grep 烧录件版本标记，对不上/找不到 → 停下先确认烧录件，不分析。
5. **致命 vs 良性预判**（bring-up 末期报错，Step 2.4）：先按 4 条良性判据过滤，良性报错不自动死磕，汇报用户决定。
6. **自动轮次检查**（Step ③）：同一问题累计无进展轮数是否已接近 `diagnostic.max_auto_rounds`（默认 5）——接近则提前准备暂停汇报，不空转。

## Prohibited Practices（问题诊断禁止操作）

| 禁止 | 正确做法 |
|------|---------|
| **凭记忆解析 CFSR/HFSR 寄存器位域而不对照 references** | 对照 `references/fault-knowledge-base.md` §3.3 和 `references/log-acquisition-guide.md` §4.3 的 CFSR 位域表，确认每一位的含义和常见原因 |
| **不区分 L0/L1 调试能力差异就给出诊断建议** | L0 无 hdc/hilog，仅靠串口+JTAG；L1 有 hdc/hilog 有限支持。诊断前先判定系统级别 |
| **对启动完全无输出直接下结论而不做硬件排查** | 先引导用户确认 JTAG 能否连接芯片、Flash 是否正确烧录、串口接线/波特率是否正确——参照 `references/log-acquisition-guide.md` §3 排查流程 |
| **不收集完整诊断信息就开始分析** | 编译错误：捕获 `ninja -v` 完整输出 + map 文件；HardFault：捕获 CFSR/HFSR/BFAR + PC/LR + 栈指针；启动失败：确认是否有任何输出（含 ROM Bootloader 日志） |
| **忽略芯片特有问题的已知模式** | 对照 `references/diagnostic-cases.md` §7（Hi3861/STM32F407/BES2600W 特有问题清单），排除芯片已知的常见坑 |
| **分析完问题不提供回归验证方案** | 每个修复方案必须附带验证步骤：重新编译的命令、烧录命令、期望的串口输出、验证通过标准 |
| **对 ISR 上下文中的问题与任务上下文用同一套分析方法** | ISR 额外检查：无阻塞调用、局部变量 < 256B、无动态内存分配；参考 `references/fault-knowledge-base.md` §5 |
| **编造芯片特定的寄存器地址/时钟 ID/引脚号** | 需要具体硬件参数时，引导用户查阅芯片 Datasheet 或通过 ohos-dev-soc-spec-parse 获取，标注数据来源 |
| **遇到不确定的错误码/机制/报错根因就闷头试错或直接问用户** | 主动联网查：宿主联网检索能力（WebSearch 或等价物；坏用备选联网检索 CLI 如 opencode，或 curl 抓 URL），查错误码含义/机制原理/已知案例，据查到的事实定方案。别等用户提示"搜一下"才搜——自己不确定就该先查 |
| **裸烧 uboot 起不来时只查时序不查 DDR 变体错配** | 烧到 100% 但 `wait boot running! uboot运行失败` / DDR Training 失败 → 优先怀疑 SoC 内置 DDR 变体错配（xlsm 选错）。走 `ohos-dev-soc-spec-parse` 单点查询"该变体该用哪个 xlsm"（命中 `ddr-variant-guide.md`，如 Hi3516CV610 -10B≠-20S 的 xlsm）。非 boot 分区能连上有正常报错 = 串口没问题 → 倾向 boot_image 内 reg_info 错配 |
| **无进展仍无限自动循环（反复重构建/重烧/换假设不收敛）** | 达到 `diagnostic.max_auto_rounds`（config，默认 5）轮仍未定位根因或未解决 → **必须暂停**，向用户汇报：①已尝试的 N 轮和结论 ②当前卡点 ③请用户决定：人工介入（请教专家/换硬件）还是 AI 继续分析。不要无限自动循环。详见下方「N 轮无进展暂停机制」 |
| **拿到报错直接钻源码+加打印多轮，不先联网搜"别人遇到过吗"** | 先联网搜解决方案（联网检索 WebSearch 或等价物 / 备选 CLI 如 opencode，关键词=报错原文+芯片/SDK/场景），再查参考仓源码/加打印验证。网上方案是线索不是定论，搜完必须验证（源码/加打印为准）。也别盲信网上不验证就照搬。详见 Step 2.5 |
| **拿到日志不核对烧录版本就分析（日志和烧录件可能对不上）** | 每轮烧录件必打唯一版本标记到开机日志（rootfs `/etc/rootfs_version` + init.cfg `cat`），拿到日志先 grep 版本标记确认是预期版本；对不上/找不到 → 停下先确认烧录件，别分析。详见 Step 2.3 |

---

## ① 文件路由表

根据用户意图，读取对应的参考文件。**每次只读一个**，不要一次性加载所有 reference。

### 本地参考文件（references/）

| 用户意图 | Agent 读取 | 预估行数 |
|---------|-----------|:-------:|
| 匹配已知故障模式（编译/链接/启动/驱动/运行时/功耗 6 大类 + OHOS init 服务启动 7 类） | `references/fault-knowledge-base.md` | ~470 |
| 参照已有诊断案例（Hi3861/STM32F407/BES2600W 真实案例 + 芯片特有问题清单 + Hi3516CV610 裸烧/OHOS init 案例） | `references/diagnostic-cases.md` | ~400 |
| 引导用户获取诊断信息（串口环境搭建/无输出排查/HardFault 现场捕获/环形日志/Watchdog flush/LED-GPIO 里程碑编码/add-debug-prints 标准步骤） | `references/log-acquisition-guide.md` | ~470 |
| 使用调试工具（OpenOCD/JTAG/J-Link/ST-Link/arm-gcc size-nm-objdump/-fstack-usage/内核符号验用 vmlinux） | `references/debug-tools-guide.md` | ~280 |
| 故障速查表（精简版，快速对照常见故障模式） | `references/fault-cheatsheet.md` | — |
| 输出诊断报告（按模板） | `references/diagnostic-report-template.md` | ~70 |
| 查外部参考资料链接（官方文档/调试工具手册/HardFault 专著/社区案例） | `references/bibliography.md` | ~120 |

### 本地参考文件续（烧录/串口/编译/Fault/Trap/Kconfig/HAL 实操）

> 本 skill 仅随包分发 references/；原始外部资料通过 references/bibliography.md 中的链接获取。

| 用户意图 | Agent 读取 | 预估行数 |
|---------|-----------|:-------:|
| 查各芯片烧录命令（Hi3861 HiBurn / STM32 st-flash / ESP32-C3 esptool / BES2600W OpenOCD） | `references/log-acquisition-guide.md` §2（串口环境搭建含连接）+ `references/debug-tools-guide.md`（OpenOCD/JTAG/J-Link/ST-Link）+ `references/bibliography.md`（烧录工具手册链接） | ~470 + ~280 + ~120 |
| 查串口工具命令（picocom/minicom/screen/pyserial + 各芯片波特率） | `references/log-acquisition-guide.md` §2.1-2.3（picocom/minicom 命令 + 波特率 + 配置要点） | ~470 |
| 查 build_lite 编译命令和环境检测命令 | `references/debug-tools-guide.md`（arm-gcc size/nm/objdump/-fstack-usage 工具用法）+ `references/bibliography.md`（官方文档链接） | ~280 + ~120 |
| 查 ARM Cortex-M Fault 寄存器完整位域表（MMFSR/BFSR/UFSR/HFSR/MMFAR/BFAR） | `references/fault-knowledge-base.md` §3.3（CFSR/HFSR/BFAR 位域表）+ `references/log-acquisition-guide.md` §4.3（CFSR 位域速查 + Handler dump 模板）+ `references/fault-cheatsheet.md` | ~470 + ~470 + — |
| 查 RISC-V Trap 异常码定义（mcause/mtval/mepc/mstatus 位域） | `references/fault-knowledge-base.md`（运行时异常故障模式）+ `references/fault-cheatsheet.md` | ~470 + — |
| 查 LiteOS-M/A Kconfig 定义（诊断 Kconfig 依赖缺失时参照） | `references/fault-knowledge-base.md` §1（编译错误故障模式，含 Kconfig 依赖缺失）+ `references/diagnostic-cases.md`（真实案例） | ~470 + ~400 |
| 查 Hi3861 HAL 实现（诊断 IoT 驱动注册问题时参照真实代码） | `references/diagnostic-cases.md` §7（Hi3861/STM32F407/BES2600W 特有问题清单 + 芯片特有案例） | ~400 |

---

## ② 工作流

### Step 0: 意图判断

接受用户输入，判断走自动化验证环路还是单点诊断：

```
用户输入
  │
  ├── "验证一下"/"帮我跑一下"/"测试这个功能"
  │   → 走完整自动化验证环路（Step 1 → Step 2 → ... → Step 7）
  │
  ├── 提供具体错误日志/现象描述（"编译报了这个错"/"HardFault了"/"启动没输出"）
  │   → 跳过环境检测，直接从 Step 3 问题分类开始
  │
  ├── 询问调试方法（"怎么用JTAG"/"HardFault是什么"/"怎么抓日志"）
  │   → 单点查询，直接读 references/ 对应章节回答
  │
  └── 不明确
      → 追问用户：芯片型号 + 系统级别(L0/L1) + 问题现象描述
```

### Step 1: 环境就绪检测（一次性）

自动化验证前，检测以下三项就绪状态。**首次使用时执行，后续可跳过。**

| 检测项 | 命令/方法 | 就绪标准 | 未就绪引导 |
|--------|---------|---------|----------|
| **串口设备** | `ls /dev/ttyUSB*`（Linux）或 `ls /dev/cu.*`（Mac）或设备管理器（Windows） | 至少一个串口设备存在 | 引导用户连接 USB 转 TTL 模块，确认 TX→RX/RX→TX/GND→GND 交叉连接 |
| **烧录工具** | `<tool> --version`（esptool/st-flash/openocd） | 工具已安装且可执行 | 引导用户安装对应芯片的烧录工具——查可用知识检索工具（MCP 等）收录的烧录命令速查，回退读 `references/log-acquisition-guide.md` §2 + `references/debug-tools-guide.md` |
| **编译环境** | `python build/lite/build.py --help` 或 `hb --help` | build_lite 环境就绪 | 引导用户参照 ohos-dev-build-config SKILL 完成编译环境搭建 |

**检测流程**：

```
1. 检测串口设备 → 未就绪 → Read log-acquisition-guide.md §2（串口环境搭建）
2. 检测烧录工具 → 未就绪 → 读 `references/log-acquisition-guide.md` §2 + `references/debug-tools-guide.md` 查对应芯片的烧录命令和安装指南
3. 检测编译环境 → 未就绪 → 引导用户使用 ohos-dev-build-config SKILL
4. 全部就绪 → 记录环境状态，进入 Step 2
```

### Step 2: 获取诊断信息

根据问题阶段，自动获取或引导用户提供诊断信息。**这是诊断中最关键的一步——没有完整的日志，分析无从谈起。**

```
问题阶段
  │
  ├── 编译/链接阶段
  │   └── Agent 执行编译命令，自动捕获完整输出
  │       ```bash
  │       ninja -v -C out/ 2>&1 | tee build.log
  │       arm-none-eabi-size -A firmware.elf  # 各段大小
  │       ```
  │       产出: build.log + map 文件 + 各段 size 统计
  │
  ├── 启动阶段
  │   ├── 有串口输出但中途停止 → 捕获完整串口输出 + 标注最后一条日志位置
  │   ├── 完全无输出 → Read log-acquisition-guide.md §3（三种排查方法）
  │   │   ├── 有 JTAG → 断点 Reset_Handler 逐步排查（debug-tools-guide.md §2.3）
  │   │   ├── 无 JTAG → GPIO 翻转标记法（log-acquisition-guide.md §3.3）
  │   │   │   └── UART 未通时用 LED/GPIO blink count 编码启动阶段（log-acquisition-guide.md §3.3.1）
  │   │   └── 检查 ROM Bootloader 日志（log-acquisition-guide.md §3.4）
  │   └── 内核 init 成功但任务不运行 → 串口输出 + 检查 LOS_Start() 是否被调用
  │
  ├── 运行时异常
  │   ├── HardFault → Read log-acquisition-guide.md §4（HardFault 现场捕获）
  │   │   ├── 有 Fault Handler dump → 解析 CFSR/HFSR/BFAR 寄存器值
  │   │   ├── 无 dump → 引导用户在 HardFault_Handler 中添加寄存器 dump 代码
  │   │   └── JTAG 在线读取（log-acquisition-guide.md §4.2）
  │   └── 偶发 crash → Read log-acquisition-guide.md §5（环形日志缓冲区 + Watchdog flush）
  │
  └── 功能/性能问题
      ├── 外设异常 → 串口日志 + 逻辑分析仪辅助（debug-tools-guide.md §4）
      ├── 功耗异常 → 电流表测量 + 逐个禁用外设定位（fault-knowledge-base.md §6.2）
      └── 启动慢 → GPIO 标记 + 示波器测量各阶段耗时（log-acquisition-guide.md §3.3）
```

> **卡在某阶段拿不到日志时** → 走「add-debug-prints 标准步骤」（log-acquisition-guide.md §8）：定位该阶段代码最早处 → 用早期串口函数 → 打印三件套（返回值+寄存器读回值+阶段 entry 标记）→ 放死循环前阻塞输出 → 解码 ret/寄存器读回值。打印必须放在返回后的 fail 分支内，不能在 ret-check 前无条件运行（实测教训：改 stub 布局会导致 GZIP IP 挂死）。

### Step 2.3: 烧录件版本标记核对（每轮必打，MUST DO，实测教训）

> **适用范围**：**仅限问题定位环节**（多轮迭代调试，如 huksfix2-14）。第一稿适配产出若一次通过、没问题，**不打标记**——别污染正式产出。
>
> **背景**：多轮迭代调试时，每轮重烧后日志和烧录件容易对不上——烧了旧版以为是最新的、几轮日志混在一起分不清哪份对应哪版、分析方（人或自动化执行代理）拿错版本的日志分析一通。教训：**每轮烧录件必须打唯一版本标记到开机日志，拿到日志先核对版本再分析**。

**每轮改烧录件时必做（产出侧）**：
1. rootfs 写版本标记文件 `/etc/rootfs_version`，内容 `{project}-{iter}-{date}`（如 `oh-lite-rootfs huksfix14-20260724`）
2. init.cfg post-init job 里 `exec /bin/busybox cat /etc/rootfs_version` 打印到串口——**必打**（放 init.cfg 保证每次开机都打，不靠人记得 echo）
3. **高亮告知用户：此版本标记是调试临时标记，问题定位完成、回归验证通过后必须从 init.cfg + rootfs 删掉，不永久留存于正式产出**
4. 标记随烧录件一起更 changelog

**拿到日志先核对（消费侧，分析前第一步）**：
```
拿到串口日志
  │
  ├── grep 版本标记（如 "rootfs_version" / "huksfix"）
  │   ├── 命中且 = 预期版本 → 确认日志↔烧录件对应，继续分析
  │   ├── 命中但 ≠ 预期版本 → 烧错版本了，停下，重烧正确版再抓日志
  │   └── 找不到标记 → 旧版（没加标记时的）/ 日志抓错，停下先确认烧录件
  │
  └── 不核对直接分析 → ❌ 可能拿旧版日志分析新改动，南辕北辙
```

**实测**：huksfix14 用 `/etc/rootfs_version` + init.cfg cat，4 次启动日志都带 `oh-lite-rootfs huksfix14-20260724`，一眼确认烧的是 huksfix14；huksfix12 加诊断打印后靠标记区分哪轮的日志，避免混轮。之前没标记时混过几轮（以为烧了新版实际是旧版，分析全白费）。

**禁忌**：
- ❌ 每轮改完不打版本标记就烧（几轮后日志分不清哪份是哪版）
- ❌ 版本标记靠手动 echo（人会忘，必须放 init.cfg 每次开机必打）
- ❌ 拿到日志不核对版本直接分析（日志和烧录件可能对不上）
- ❌ 第一稿适配一次通过就打标记（标记是调试期工具，正式产出不留）
- ❌ 调试完忘了删标记（init.cfg cat + /etc/rootfs_version 要在回归通过后清除）

> 关联 memory：update-changelog-after-burnfile-change（改烧录件更 changelog，版本标记是日志侧的版本锚点）、add-debug-prints-for-diagnosis。版本标记位构建侧写法见 `{{ASSET_ROOT}}/workflow/steps/04-build-verify/SKILL.md` Step 4.5。

### Step 2.4: 良性报错判据（致命 vs 良性区分，MUST DO）

> **背景**：bring-up 末期日志常残留一批报错（权限失败/EACCES/-32 spam/某 SA 起不来重试）。不是所有报错都要死磕——有的来自非关键路径、瞬时自愈、不影响核心功能。但也不能把致命报错当良性放过。诊断定位到某报错后，**先判致命还是良性**，再决定是否继续定位。

**良性报错判据**（满足全部）：
1. **不影响核心功能**：核心 SA（如系统服务管理/能力发布）已起、核心 IPC 通路已通、XTS 目标用例全过
2. **来自非关键路径**：报错来自非 root SA / 辅助组件 / 非阻断路径（如某 SA open 驱动 EACCES，但该 SA 不需要 context mgr，重试成功）
3. **瞬时自愈或重试成功**：报错后重试通过 / 有限次后停止 / 不累积放大
4. **不导致重启或挂死**：无 reboot loop、无看门狗复位、系统持续运行不卡死

**致命报错判据**（满足任一即致命，不能当良性）：
1. **阻断核心功能**：核心 SA 起不来 / 核心 IPC（如 binder）不通 / 子系统无法发布
2. **导致 reboot loop 或看门狗复位**：系统反复重启、看门狗触发
3. **服务起不来连锁**：A 服务挂导致 B/C 连锁起不来
4. **XTS fail**：目标用例不通过

**★ 判良性后不自动死磕——汇报给用户决定**：
判为良性后**不要自作主张继续死磕**，也不要默写"无问题"。向用户汇报：
- 良性依据（4 条判据各满足什么）
- 残留风险评估（会不会在量产/长跑/边界场景翻车）
- 是否影响交付（XTS 是否全过、核心功能是否可用）
- 由用户决定：**接受残留收工** 还是 **继续定位该报错**

**实测案例**（hi3516cv610）：binder `OpenDriver EACCES errno=13` 来自非 root SA（某些辅助 SA），这些 SA 不需要 BINDER_SET_CONTEXT_MGR；核心 SA（root）`BINDER_SET_CONTEXT_MGR ret=0` 成功 → samgr 就绪 → HUKS 发布；残留 EACCES 重试成功；`-32` spam 15 行瞬时自愈；4 次启动不重启；XTS 426/426（HUKS 40/40 + deviceattest 3/3）→ 判良性，残留可接受。具体 SA 名/日志见 `references/diagnostic-cases.md` §9 OH005。

**禁忌**：
- ❌ 把良性报错当 bug 死磕浪费轮次（良性依据已足还反复定位）
- ❌ 把致命报错当良性放过留隐患（核心功能没验通就判良性）
- ❌ 拍脑袋判良性——4 条判据逐条核对，有实测证据（核心 SA 起没起/XTS 过没过/重启没重启）
- ❌ 判良性后不汇报用户直接收工（残留风险要用户知情决定）

> 关联 memory：dont-claim-rootcause-before-verification（良性判定也要有依据不是拍脑袋，标"假设良性"→实测确认 4 条判据→才说"确认良性可接受"）。

### Step 2.5: 诊断先联网搜 + 再查源码/加打印验证（MUST DO，实测教训）

> **背景**：实测 hi3516cv610 裸烧诊断（0x81 / fmc100 pagesize 8192 / DS35Q1GB ID 表 / bootm Usage）曾直接钻源码 + 加打印折腾多轮，没先联网搜"别人遇到过吗"，绕远路。教训：**先联网搜，再查源码/加打印验证**——网上方案是线索不是定论，搜完必须验证。

**流程**：
```
拿到报错日志（Step 2 产出）
  │
  ├── ① 先联网搜解决方案（联网检索 WebSearch 或等价物 / 备选 CLI 如 opencode）
  │     关键词：报错原文（verbatim，如 "BUG: Driver does not support pagesize 8192"）
  │            + 芯片/SDK/场景（如 "hi3516cv610 spi nand fmc100"）
  │     → 看"别人遇到过吗 / 官方怎么说 / 社区怎么解"
  │     → 有现成方案就参考，省时间（避免重复造轮子）
  │     ⚠️ 联网检索失败（占位套话）→ 换备选联网检索 CLI（如 opencode）搜，或 curl 抓指定 URL
  │        （见 skill 知识检索降级链兜底）
  │
  ├── ② 再查参考仓源码 + 加打印验证
  │     网上方案不一定全对，也不一定适配本项目（芯片型号/SDK 版本/板子硬件可能不同）
  │     → 查参考仓源码确认（grep 报错字面提到的组件名/符号在源码的位置）
  │     → 必要时加最小调试打印拿错误码/寄存器读回值（见 references/log-acquisition-guide.md §8）
  │     → 确证根因后再修
  │
  └── ③ 网上方案与本项目源码/实测冲突时，以源码/加打印为准
        网上方案是线索不是定论；别钻牛角尖（直接源码+加打印多轮不搜），
        也别盲信网上（不验证就照搬）。
```

**禁忌**：
- ❌ 直接钻源码 + 加打印多轮，没先联网搜"别人遇到过吗"（绕远路）
- ❌ 盲信网上方案不验证就照搬（芯片/SDK 版本不同可能不适配）
- ❌ 联网检索失败就静默跳过不搜（要降装备选 CLI 如 opencode/curl，见 skill 知识检索降级链兜底）

> 关联 memory：search-then-verify-in-source（先搜再验证）、add-debug-prints-for-diagnosis（加打印验证）、opencode-websearch-fallback（联网搜用 opencode）。

### Step 3: 问题分类（故障决策树）

Read `references/fault-knowledge-base.md` 和 `references/bibliography.md` §5（故障排查决策树完整版），按以下决策树判定问题类型：

```
诊断信息
  │
  ├── 编译阶段出错？
  │   └── 是 → 解析 arm-gcc/riscv-gcc 输出
  │       ├── fatal error: xxx.h → 头文件缺失 → Step 4 匹配 FAULT-COMP-001
  │       ├── error: 'XXX' undeclared → 宏/类型未定义 → Step 4 匹配 FAULT-COMP-002
  │       ├── implicit declaration → 隐式函数声明 → Step 4 匹配 FAULT-COMP-003
  │       ├── ERROR at //BUILD.gn:xx → GN/build_lite 错误 → Step 4 匹配 FAULT-COMP-004
  │       └── Kconfig 条件编译排除 → Step 4 匹配 FAULT-COMP-005
  │
  ├── 链接阶段出错？
  │   └── 是 → 解析链接器输出
  │       ├── undefined reference to → 缺少库/符号 → Step 4 匹配 FAULT-LINK-001
  │       ├── region 'RAM' overflowed → Step 4 匹配 FAULT-LINK-002
  │       ├── region 'FLASH' overflowed → Step 4 匹配 FAULT-LINK-003
  │       └── multiple definition of → Step 4 匹配 FAULT-LINK-004
  │
  ├── 启动阶段失败？
  │   └── 是 → 分析启动情况
  │       ├── 完全无输出 → Step 4 匹配 FAULT-BOOT-001（4 类子原因）
  │       ├── 部分输出后停止 → Step 4 匹配 FAULT-BOOT-002（4 类子原因）
  │       ├── HardFault 启动 → Step 4 匹配 FAULT-BOOT-003（解析 CFSR/HFSR）
  │       └── 内核 OK 任务不跑 → Step 4 匹配 FAULT-BOOT-004（任务栈/优先级/调度器）
  │
  ├── 运行时异常？
  │   └── 是 → 分析异常类型
  │       ├── HardFault → Step 4 匹配 FAULT-RUNTIME-001（解析 CFSR 位域细分 6 种）
  │       ├── 栈溢出 → Step 4 匹配 FAULT-RUNTIME-002（栈水位 + map 文件分析）
  │       ├── 看门狗复位 → Step 4 匹配 FAULT-RUNTIME-003（喂狗点分析 + GPIO 翻转）
  │       └── 内存不足 → Step 4 匹配 FAULT-RUNTIME-004（堆统计 + 内存泄漏检测）
  │
  └── 性能/功耗问题？
      └── 是 → 匹配 FAULT-PERF-001~004（中断延迟/功耗/Flash 磨损/启动慢）

  └── OHOS init/服务启动失败？（L1：内核 boot 完进 OHOS init 后卡）
      └── 是 → Read fault-knowledge-base.md §7 + diagnostic-cases.md §9
          ├── binder ioctl returned -22 EINVAL + samgr boot step 卡死
          │   → 内核/user 态 binder 协议位宽错配（缺 BINDER_IPC_32BIT）
          │   → 用 vmlinux 验符号（debug-tools-guide.md §3.6），对齐参考 patch
          ├── /dev/xxx No such file（如 apphilogcat hilog fd failed）
          │   → 驱动未 device_create → init.cfg exec /bin/busybox mknod 应急
          ├── 全 service Error relocating: __fd_chk: symbol not found
          │   → musl ld 用错版本 → rootfs ld-musl = OH sysroot libc.so 拷贝
          └── 颗粒规格 datasheet 查不到 → 以能跑的 bin 的 runtime print 为权威
```

### Step 4: 匹配故障模式

Read `references/fault-knowledge-base.md`（故障知识库）和 `references/diagnostic-cases.md`（真实案例），将 Step 3 分类的问题匹配已知故障模式→根因→修复方案。

**匹配优先级**：

```
1. 精确匹配（日志内容包含已知错误模式字符串）
   → 查 fault-knowledge-base.md 对应 §1-6 的表格和 yaml 规则
   → 例: "fatal error: cmsis_os2.h: No such file or directory"
     → fault-knowledge-base.md §1.1 头文件缺失表第 1 行
     → 匹配 diagnostic-cases.md C001（Hi3861 CMSIS 路径错误）

2. 芯片特定匹配（同芯片的已知问题）
   → 查 diagnostic-cases.md §7（Hi3861/STM32F407/BES2600W 特有问题清单）
   → 例: STM32F407 + HardFault(UNDEFINSTR) + 有浮点运算
     → diagnostic-cases.md §7.2 第 3 行（FPU 相关 HardFault）
     → diagnostic-cases.md B002（同场景真实案例）

3. 模糊匹配（日志包含部分关键词）
   → 搜索 fault-knowledge-base.md 全文，匹配最相关的故障类别
   → 输出多个候选诊断（按概率排序），引导用户提供更多信息确认

4. 无匹配 → 进入 Step 5 深度定位
```

**诊断报告输出格式**（参考 `references/diagnostic-cases.md` 的案例格式）：

```markdown

---

> 诊断报告: `references/diagnostic-report-template.md`
```

---

## ③ N 轮无进展暂停机制（MUST DO）

> **背景**：裸烧 boot_image 诊断曾跑 10+ 轮 agent（GSL→uboot code→-10B reg_info→0x81→加打印挂死…）陷入反复重构建重烧循环。用户决定：设阈值，N 轮无进展就暂停问用户，避免 AI 无限自动循环。

### 规则

- **阈值来源**：`workflow_config.yaml` → `diagnostic.max_auto_rounds`（默认 5，用户可调；0 = 禁用但不推荐）。
- **"一轮"定义**：完成一次「假设→验证（编译/烧录/抓日志）→结论」闭环算一轮。纯查资料/读代码不算独立轮次，但若连续多轮只查不验证且无新结论，也算无进展。
- **"无进展"判据 = 卡在同一个问题上无进展**（满足任一即算当轮无进展，且必须针对**同一个未解决的问题**计数）：
  - 未定位根因，且本轮假设与已排除假设无实质区别
  - 根因已定位但修复后问题依旧（修复未命中）
  - 连续 2 轮引入新错误（级联失败）
  - 本轮无新证据（日志/现象与上轮一致，无新增信息）
- **不算无进展（不累计，计数按"同一问题"归零重计）**：跨不同子问题各有进展——每个子问题在推进（定位了根因/消除了一个错误/排除了一个假设）或已解决。不同子问题之间不累计算"无进展"轮数；只有**同一个问题反复尝试 N 轮无实质突破**才累计触发阈值。
- **判别示例**（本会话裸烧诊断）：
  - GSL 用错（解决）→ uboot code 用错（解决）→ -10B reg_info 误判（解决）：三个不同子问题各有进展，**不算无进展**，计数归零重计
  - 0x81 卡住多轮无突破（同一问题反复尝试无新结论）：**算无进展**，按此计数，达到阈值触发暂停

### 达到阈值必须做的（MUST DO）

当**同一问题**累计无进展轮数 ≥ `diagnostic.max_auto_rounds` 时，**立即停止自动尝试**，向用户输出：

```markdown
## ⏸ 诊断暂停 — 同一问题已达 N 轮无进展阈值

**卡住的问题**：{具体哪个子问题——不是整体诊断，是当前反复尝试无突破的那个问题}
**该问题无进展轮数**：{N} / {max_auto_rounds}（注：跨子问题各有进展的轮数不累计，仅同一问题无突破才计数）
**已尝试假设与结论**：
1. {假设 1} → {验证方式} → {结论（排除/部分/未验证）}
2. {假设 2} → ...
...

**当前卡点**：{为什么继续自动尝试无意义——缺什么信息/卡在哪个未知}

**已解决的前序子问题**（供参考，说明整体在推进）：{如 GSL→uboot code→-10B 已解决，仅 0x81 卡住}

**请决定下一步**：
- [ ] **人工介入** — 如请教人类专家 / 换硬件 / 查厂商支持
- [ ] **AI 继续分析** — 我换个方向重试（请说明：继续是同一方向还是新方向？）
- [ ] **调整阈值** — 把 max_auto_rounds 调大继续自动跑
```

### 禁止（MUST NOT DO）

- ❌ 达到阈值仍自动发起下一轮编译/烧录/验证
- ❌ 把"查资料/读代码"反复计入轮次充数（不算进展）
- ❌ 把跨子问题各有进展的轮数累计算"无进展"（只有同一问题反复无突破才累计）
- ❌ 暂停汇报时隐瞒已试过的假设（必须完整列出，避免用户重复建议）
- ❌ 用"再试一次可能就好了"作为继续自动循环的理由

---

## Exceptions and Fallbacks（异常与兜底）

| 场景 | 处理 |
|------|------|
| **拿到日志但无版本标记 / 版本不符** | 停下先确认烧录件（重烧正确版或确认日志归属），不分析——旧版日志分析新改动 = 南辕北辙（Step 2.3） |
| **联网搜 + 源码查询都拿不到错误码含义**（如 NDA TRM 位域，0x81 实例） | 不死磕寄存器位域——转走标准产物对比（标准构建 vs 手工拼装 diff、历史案例差异对比），根因标「未确证」，列出下一步排查清单（0x81 实测） |
| **根因定位后修复未命中（修了问题依旧）** | 该假设标"已证伪/未命中"，回假设清单换方向；同一问题连续 N 轮无进展 → 触发 Step ③ 暂停机制问用户，不无限循环 |
| **知识检索服务不可用**（MCP 未配置/连接失败） | 降级链：本地 references/ → 联网搜索 → 询问用户。禁止以"工具不可用"为由跳过诊断 |
| **联网检索返回占位/套话** | 降级备选联网检索 CLI（如 opencode）或 curl 抓 URL，不静默跳过搜索（Step 2.5） |
| **烧录 100% 但 uboot 起不来** | 先怀疑 SoC 内置 DDR 变体错配（xlsm 选错）——走 ohos-dev-soc-spec-parse 单点查询；非 boot 分区能连上有正常报错 = 串口没问题 → 倾向 boot_image 内 reg_info 错配 |
| **完全无输出且无 JTAG** | GPIO 翻转标记法 / LED blink count 编码启动阶段（log-acquisition-guide.md §3.3），不死等串口 |
| **诊断需真机烧录而当前环境没有板子** | 输出诊断假设清单 + 加打印方案 + 抓日志清单，交用户上板执行后回报，不凭静态分析直接下根因结论 |
| **报错被判良性** | 不自动死磕也不默写"无问题"——汇报 4 条判据逐条依据 + 残留风险 + 交付影响，由用户决定收工还是继续（Step 2.4） |
| **用户输入芯片型号/系统级别不明** | 追问（芯片型号 + L0/L1 + 现象），不猜级别瞎给诊断建议 |

---
