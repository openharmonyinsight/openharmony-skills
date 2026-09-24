---
name: test-gen
description: 工作流 Phase 5（可选阶段）——为嵌入式 OS 适配生成测试用例、选择测试框架、执行单元测试/集成测试/硬件在环测试。触发症状：用户说"写测试"、"生成测试用例"、"Unity/HCTest"、"跑测试"、"硬件在环测试"。
license: MIT
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: lite
  capability: test-gen
  version: 0.1.0
  status: trial
  category: workflow-step-test-gen
---

# Phase 5: 测试

> **本文件基于设计方法论和 Round-Trip 验证方法论校准。**
> 早期验证轮未实际执行到此阶段（在 P4 编译 PASS 后停止迭代），因此本 SKILL 的**过程验证状态为 DESIGN_ONLY**，但测试策略本身经过 Round-Trip 挖空映射表方法的交叉验证。

## 契约（来自编排器 `skills/ohos-dev-workflow-router/SKILL.md` v0.1.0）

| 属性 | 值 |
|------|-----|
| **输入** | P4 产出的固件 + P3 定义的驱动 Method 接口 + P2 KAL 接口 |
| **产出** | ① 测试框架初始化代码 ② 单元测试用例 ③ 集成测试用例 ④ 测试编译报告 ⑤（可选）硬件运行报告 |
| **门控** | **GATE-T**：测试源码/二进制编译并留存证据；**GATE-HW**：烧录、HIL/XTS 运行需硬件和用户确认 |
| **特殊性** | P5-A 测试生成与编译不可因无硬件跳过；仅可由用户/模式显式跳过整个 P5。P5-B 硬件运行可标记 `SKIPPED_NO_HARDWARE` |

## 知识检索（可用时优先知识检索服务如 project-brain MCP；不可用按 skill 知识检索降级链：本地 references → 联网搜索 → 询问用户）

本步骤的本地代码分析，可用时优先使用（可选）project-brain 等知识检索服务 MCP：
- `get_related_tests` — 找某 HAL/符号的关联测试
- `test_recommendation` — 改完文件推荐跑哪些测试
- `locate_symbol` — 定位被测函数定义

> MCP 调失败或未装 → 按 skill 知识检索降级链回退。

## 子步骤

```
Step 1: 测试框架选择与初始化
    │   决策依据: RAM 预算 / 是否有 HIL 条件 / CI 需求
    │
Step 2: 单元测试用例生成
    │   基于 P3 驱动接口边界 + P2 KAL 接口边界
    │   使用 Round-Trip "挖空-填充-比对" 三元组作为测试设计模式
    │
Step 3: 集成测试
    │   多外设协同场景 (UART+GPIO echo, I2C+sensor pipeline)
    │
Step 4: GATE-T 测试编译与证据归档
    │
Step 5: 硬件在环 HIL / XTS (默认跳过, 仅在有条件时执行)
```

---

## Step 1: 测试框架选择

### 框架对比

| 框架 | 适用场景 | RAM 开销 | Mock 能力 | OH 集成度 | L0 适配性 |
|------|---------|:-------:|:--------:|:-------:|:-------:|
| **HCTest** | OH 原生, L1 推荐 | ~10-30KB | 中 (HDF mock) | ★★★★★ | 🟡 可能超预算 |
| **Unity + CMock** | 第三方, 广泛使用 | ~5-15KB | ★★★★★ (自动生成) | ★★☆☆☆ | ✅ 可裁剪到极简 |
| **轻量自研** | 极端 RAM 约束 | ~1-3KB | 手动 function ptr swap | N/A | ✅ 最灵活 |
| **minunit / Unity lite** | Unity 子集 | ~2-5KB | 手动 | N/A | ✅ |

### 选择决策流程

```
RAM 预算?
├─ > 50KB 可用于测试 → HCTest (OH 原生, 最佳集成)
├─ 10-50KB → Unity + CMock (自动 mock, 社区成熟)
├─ 3-10KB → Unity Lite / minunit (手动 mock)
└─ < 3KB → 自研 assert 宏 (仅 ASSERT/EXPECT 系列)
```

**L0 默认推荐**: Unity (可裁剪) 或轻量自研。HCTest 通常超出 L0 RAM 预算。

### 框架初始化产出

```
tests/
├── framework/
│   ├── unity.h / unity.c          # 或 hctest_*.h
│   └── test_runner.c              # main() 入口, 注册所有测试组
├── unit/
│   ├── test_{peripheral}.c         # 每个外设驱动一个
│   └── test_{kal_module}.c        # 每个 KAL 模块一个
├── integration/
│   ├── test_scenario_{name}.c      # 多外设协同场景
│   └── mock/
│       └── mock_hal_{name}.c       # HAL 函数的 mock 实现
└── README.md                       # 如何运行测试
```

---

## Step 2: 单元测试用例生成

### 设计方法: Round-Trip 挖空三元组

> 来自 verifying-workflow SKILL 的核心思想可直接复用为测试设计模式:

| Round-Trip 概念 | 测试等价物 | 说明 |
|-----------------|-----------|------|
| Ground Truth (GT) | **Expected Output** | 正确行为的参考答案 |
| Hollowed Skeleton | **Test Fixture Setup** | 被测函数的输入环境 |
| Regenerated Output | **Actual Output** | 被测函数的实际返回值 |
| Diff Comparison | **Assertion** | Expected == Actual ? |

### 测试覆盖矩阵 (按接口)

对每个 P3 驱动的 HAL 接口:

```c
// test_gpio.c — 以 GPIO 为例 (实测 PASS 驱动)

void Test_GpioWrite_High(void)
{
    // Given: 初始化 GPIO 引脚为输出模式
    int32_t ret = GpioInit(&g_gpioResource);
    TEST_ASSERT_EQUAL_INT32(HDF_SUCCESS, ret);

    // When: 写高电平
    ret = GpioWrite(&g_gpioResource, 1);

    // Then: 返回成功
    TEST_ASSERT_EQUAL_INT32(HDF_SUCCESS, ret);
}

void Test_GpioWrite_InvalidPin(void)
{
    // When: 使用非法引脚号
    g_gpioResource.pin = 255;  // 超出范围
    int32_t ret = GpioWrite(&g_gpioResource, 1);

    // Then: 返回错误码
    TEST_ASSERT_EQUAL_INT32(HDF_ERR_INVALID_PARAM, ret);
}

void Test_GpioRead_AfterWrite(void)
{
    // Given: 写入高电平
    GpioWrite(&g_gpioResource, 1);
    uint16_t val;

    // When: 读回
    int32_t ret = GpioRead(&g_gpioResource, &val);

    // Then: 读回写入的值
    TEST_ASSERT_EQUAL_INT32(HDF_SUCCESS, ret);
    TEST_ASSERT_EQUAL_UINT16(1, val);
}
```

### 必须覆盖的测试维度

| 维度 | 测试内容 | 优先级 |
|------|---------|:------:|
| Happy Path | 正常参数 → 期望正常返回 | 🔴 必须 |
| Boundary | 最大值 / 最小值 / 零值 / 边界值 | 🔴 必须 |
| Invalid Input | NULL 指针 / 越界 ID / 错误枚举 | 🔴 必须 |
| Error Path | 每个错误返回码至少一个触发场景 | 🟡 重要 |
| Sequence | Init → Read/Write × N → Release | 🟡 重要 |
| Concurrency | 多实例同时操作 (如有线程安全要求) | 🟢 可选 |

---

## Step 3: 集成测试

### 典型场景

| 场景 | 涉及外设 | 验证目标 |
|------|---------|---------|
| UART Echo | UART + GPIO (RTS/CTS) | 收发环路正确 |
| Sensor Pipeline | I2C + GPIO (interrupt pin) | I2C 读取 + 中断响应 |
| PWM Output | PWM + GPIO (output compare) | 频率/占空比准确 |
| Watchdog Feed | watchdog + timer | 看门狗不误触发复位 |
| Multi-instance | 同一外设 2 个实例 | 实例间不干扰 |

### L0 现实约束

> **大多数集成测试需要实际硬件。** 在 L0 MCU 上:
> - 无法轻松模拟外设行为 (没有 MMU, 内存极小)
> - Mock 策略: **函数指针替换** (编译时替换 HAL 底层函数)
> - 如果没有硬件: 标记测试为 `#ifdef HARDWARE_IN_LOOP` 并在 host 端 skip

---

## Step 3.5: XTS fail 分类回溯表（通用方法）

> **背景**：XTS 跑出 fail 后不能只看 fail 用例本身——fail 的根因常在更早阶段（驱动没适配/init.cfg 错/.so 缺）。按 fail 现象分类回溯到对应工作流阶段定位，迭代直到目标 pass 率。

**XTS fail 分类 → 回溯阶段**：

| fail 现象 | 回溯阶段 | 定位方向 |
|---|---|---|
| 服务没起（某 SA 进程不存在/启动即退） | P4 init.cfg | 查 init.cfg 该 service 的 path/uid/importance/critical + `/dev` 节点是否齐 |
| 驱动缺节点（`open /dev/xxx failed`） | P3 ohos-dev-kernel-node-adapt | 查内核 defconfig + DTS 有无开对应驱动 + 驱动有无 `device_create` |
| IPC 协议错（binder ioctl -EINVAL / samgr boot step 卡） | P2 binder 适配 | 查内核/user 态 binder 协议位宽对齐（如 32/64 位结构体） |
| uid 权限失败（SA 起来报 EPERM/EACCES） | P4 init.cfg | 查该 SA 的 uid 是否够（核心 SA 常需 root/0 + CAP_SYS_NICE 等能力） |
| `.so` 缺失（`Error relocating: symbol not found`） | P4 rootfs | 查 rootfs/lib 的 .so 依赖闭包 + ld-musl 是否用对版本 |
| 子系统未发布（GetFeatureApi 重试超时返回 -2 等） | P3 + P4 | 查服务注册链（注册 OK 但不分发？任务分发配置错？依赖 SA 没起？） |

**迭代流程**：
```
XTS 跑出 fail
  │
  ├── 按 fail 现象分类 → 回溯到对应阶段（上表）
  │     → 定位根因 → 修复（改 init.cfg / defconfig / DTS / rootfs .so / uid）
  │     → 重编相关产物（uImage/rootfs）→ 重烧 → 重跑 XTS
  │
  └── 迭代直到目标 pass 率（如全过 / 核心用例全过）
        │
        └── 残留 fail 判良性/致命（见 ohos-issue-lite-diagnose Step 2.4）
              ├── 致命 → 继续定位
              └── 良性 → 汇报用户决定接受残留还是继续
```

> **通用方法**——fail 现象到回溯阶段的映射适用任意芯片适配。具体某芯片的 XTS 迭代案例（如从 N fail 迭代到全过）进 references 案例库。关联 `skills/ohos-issue-lite-diagnose` Step 2.4（良性报错判据）。

---

## Step 4: GATE-T — 测试编译与证据归档

P5-A 必须完成测试源码生成、构建和产物记录。无硬件不影响该门控。

- [ ] 记录实际构建命令和工具链版本
- [ ] 记录测试源码、测试二进制路径及 SHA256
- [ ] 记录测试用例总数、编译成功数和编译失败数
- [ ] 保存完整构建日志
- [ ] 编译失败时进入 P7，不得把“已生成源码”标记为 P5 完成

测试编译状态只能使用：`PASS`、`FAIL`、`SKIPPED_USER`、`SKIPPED_MODE`。`SKIPPED_*` 仅在用户或工作流模式显式跳过整个 P5 时使用；无硬件不是跳过 P5-A 的理由。硬件未参与时不得写成 XTS 运行通过。

GATE-T 结束时必须更新 `verification_manifest`：测试源码快照、构建命令、工具链版本、测试二进制 SHA256、日志路径、用例计数和 `PASS`/`FAIL`/`SKIPPED_USER`/`SKIPPED_MODE` 状态。无此记录不得把 P5-A 标记完成；`SKIPPED_*` 还必须记录触发它的用户决定或模式配置及风险。

## Step 5: 硬件在环 (HIL) / XTS（GATE-HW 硬件确认门）

> **GATE-HW**: HIL/XTS 是硬件操作（需 P4 已烧录固件到板子 + 串口捕获）。执行者到此**必须停下**，向用户确认"现在要开始跑 XTS 吗？"，获准后才执行。无硬件条件时将 P5-B 标记为 `SKIPPED_NO_HARDWARE`，不能影响已通过的 GATE-T。

GATE-HW 无论执行、失败还是跳过，都必须更新同一份 `verification_manifest`，记录用户确认、板卡/固件标识、实际命令、串口日志、测试计数及 `PASS`/`FAIL`/`SKIPPED_NO_HARDWARE` 状态。

用 `ohos-test-lite-adapt-verify` skill 执行 XTS（6 阶段：init→explore→analyze→implement→verify→summary）。其中 verify 阶段需烧录 XTS 固件 + 串口捕获 pass/fail。

### 默认: `SKIPPED_NO_HARDWARE`

**仅在以下条件全部满足时才执行**:
1. 用户明确要求（GATE-HW 确认）
2. P4 烧录已完成（板上有固件）
3. 有可用的调试器/烧录器 (JTAG / SWD / serial bootloader)
4. 有串口连接用于捕获测试输出
5. 时间预算允许 (HIL 调试耗时远大于纯软件测试)

### HIL 执行清单

- [ ] 固件已通过 P4 编译验证 (使用同一个 .bin/.elf)
- [ ] 测试框架已链接进固件 (或作为独立 app 加载)
- [ ] 串口捕获已配置 (baudrate 匹配)
- [ ] 自动化脚本就绪 (flash → boot → capture output → parse → assert)
- [ ] 回归基线已建立 (首次运行的输出作为 baseline)

---

## 引用的 tools/

| 工具 | 用途 | 路径 |
|------|------|------|
| ohos-test-lite-ut-gen | 测试用例生成（HCTest/iCunit/HWTest/gtest） | `skills/ohos-test-lite-ut-gen/` |

## Agent Dispatch Spec

### 分发规格

| 属性 | 值 |
|------|-----|
| **agent_role** | `test-expert` |
| **category** | `unspecified-high` |
| **load_skills** | `[ohos-test-lite-ut-gen, ohos-test-lite-adapt-verify]` |
| **dispatch_mode** | **顺序流水线** (框架→单元→集成→HIL) |
| **parallel_groups** | Step 2 内部各测试文件可并行生成 |

### Agent Prompt 模板

```
1. TASK:
   为 {chip_model} 嵌入式 OS 适配项目生成测试套件。
   注意: P5-B 硬件运行是可选阶段；P5-A 测试编译仍是强制阶段。本步骤过程验证状态仍为 DESIGN_ONLY。

2. 框架选择:
   L0 目标 → 默认推荐 Unity (可裁剪) 或轻量自研
   L1 目标 → HCTest (OH 原生集成)
   如用户指定 → 使用用户选择的框架

3. 测试范围:
   - P3 驱动接口: 每个 Init/Read/Write/Release 至少 happy path + boundary + invalid
   - P2 KAL 接口: pthread/time/file 至少关键路径
   - 集成: 2-3 个多外设协同场景

4. Round-Trip 集成:
   使用 "hollow-template-ground_truth" 三元组思想设计测试:
   - hollowed skeleton = test fixture setup
   - template = expected behavior spec
   - ground truth = reference implementation (if available from GT or docs)

5. EXPECTED OUTCOMES:
   ① tests/framework/ (框架代码)
   ② tests/unit/test_*.c (单元测试, 每个模块至少 3 个 case)
   ③ tests/integration/test_*.c (集成测试, 2-3 个场景)
   ④ docs/test_report.md (运行后的报告模板)

6. MUST DO:
   - [ ] 根据 RAM 预算选择合适框架 (L0 不要默认 HCTest)
   - [ ] 每个 public API 至少: happy path + 1 boundary + 1 invalid input
   - [ ] 错误返回码全覆盖 (每个 error code 至少 1 个 test)
   - [ ] 测试可独立于完整固件运行 (提供 mock 方案)
   - [ ] HIL 默认标记为 skip, 不假设硬件可用

7. MUST NOT DO:
   - [ ] 不要假设有 HIL 环境
   - [ ] 不要只测 happy path (error path 更容易暴露 bug)
   - [ ] 不要修改被测驱动源码 (只写测试代码)
   - [ ] 不要声称实测验证了此阶段 (它没有)
