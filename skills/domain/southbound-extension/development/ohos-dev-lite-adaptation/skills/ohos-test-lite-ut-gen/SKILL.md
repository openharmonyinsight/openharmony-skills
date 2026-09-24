---
name: ohos-test-lite-ut-gen
description: OpenHarmony Lite (L0/L1) 测试用例生成器——读驱动接口头文件，按 L0（HCTest+iCunit，纯 C）或 L1（L1-Linux：HWTest/gtest；L1-LiteOS-A：按平台 acts 范式确认）生成正向功能/边界值/异常路径/中断安全/CMSIS 兼容五类场景测试代码 + 配套 BUILD.gn。Use when driver unit or compatibility tests are needed for an OpenHarmony Lite adaptation; triggers include 测试用例、生成测试、单元测试、给驱动补测试、HCTest、iCunit、HWTest、gtest、边界值、异常路径测试、ISR 安全测试、CMSIS 兼容性测试、测试 BUILD.gn、烧板测试不跑（zinitcall/gc-sections 排查）。
metadata:
  author: openharmony
  scope: domain
  stage: testing
  domain: lite
  capability: ut-gen
  version: 0.1.0
  status: trial
---

## Trigger Signals

出现以下信号时应触发本 skill：

| 信号类型 | 典型表达 |
|---------|---------|
| 明确生成任务 | "给这个驱动生成测试"、"写单元测试"、"生成 iot_gpio 测试用例"、"出测试 + BUILD.gn" |
| 框架关键词 | "HCTest"、"iCunit"、"HWTest"、"gtest"、"LITE_TEST_CASE"、"HWTEST_F" |
| 场景关键词 | "边界值测试"、"异常路径"、"ISR 安全用例"、"CMSIS 兼容性" |
| 症状词（隐性需求） | "烧板后测试没跑"（gc-sections 丢 initCase，见 Step 7 §抗 gc-sections）、"跑到测试注册就 HardFault"（函数体被 gc 丢，见 Step 7）、"边界断言好像恒真"（Step 6 判别力检查） |
| 下游/上游 skill 链式调用 | ohos-dev-hal-skeleton-gen 产出驱动后补测试；ohos-test-lite-adapt-verify / ohos-ci-lite-deploy-burn 需要测试代码输入 |

**不触发**（明确排除）：直接执行已有测试/跑 XTS（走 ohos-ci-lite-deploy-burn / ohos-test-lite-adapt-verify）；审查已有测试代码质量（可参考本 skill Step 6 检查表，但不是生成任务）。

---

## Scope

本 SKILL 是 OpenHarmony Lite（L0 轻量系统 / L1 小型系统）芯片适配的**测试生成层**：读取驱动接口头文件（.h），分析函数签名、参数约束和返回值，按 L0（HCTest + iCunit 混合模式）或 L1-Linux（HWTest/gtest；L1-LiteOS-A 先按平台 acts 范式确认框架）框架生成完整的测试代码——正向功能测试、边界值测试、异常路径测试、中断安全测试、CMSIS 兼容性测试，以及配套的 BUILD.gn 编译配置。

**本 SKILL 生成测试代码骨架 + 断言逻辑，不执行测试也不烧录固件**（测试执行和烧录由用户在目标硬件上完成）。

### 生成文件清单

| 系统级别 | 本 SKILL 生成的文件 | 测试框架 |
|---------|-------------------|---------|
| **L0** (LiteOS-M) | `<periph>_test.c` + `BUILD.gn` | HCTest（套件结构）+ iCunit（断言）混合模式 |
| **L1-Linux**（kernel_family=linux，如 Hi3516CV610） | `<periph>_test.cpp` + `BUILD.gn` | HWTest（`HWTEST_F` 宏 + gtest 断言）——iter09 实证路线 |
| **L1-LiteOS-A** | `<periph>_test.cpp`/`.c` + `BUILD.gn` | 不默认 HWTest：先按 target profile 与该平台 acts 用例范式确认实际测试框架，未确认前追问用户（线索：kernel_liteos_a 仓自带 HWTest testsuites，见 references/bibliography.md——可用性按目标平台实际确认，不臆断） |

> 测试代码使用被测驱动的**公开 HAL 接口**（如 `GpioOpen`/`I2cWrite`/`UartRead`），不直接访问寄存器。HAL 接口头文件由 upstream（ohos-dev-hal-skeleton-gen 或用户）提供。

## Initial Checks

生成前按以下顺序先做判断（缺失项需追问用户，见 Step 1 输入表）：

1. **系统级别判定（L0/L1 + L1 路线）**：决定测试框架与语言——L0（LiteOS-M，无 MMU）→ HCTest + iCunit 纯 C；L1（有 MMU）→ C++，框架按路线分：**L1-Linux**（kernel_family=linux）→ HWTest/gtest（iter09 实证）；**L1-LiteOS-A** → 按平台 acts 范式确认，不默认 HWTest。用户未给 → 追问，不默认。
2. **头文件可用性**：被测驱动 HAL 接口头文件（.h）是否已给出/可读？拿不到签名就无法分析参数约束 → 追问用户提供。
3. **API 级别判定**：头文件是 IoT API（`iot_gpio.h` 等，L0 `iot_hardware`）还是 HDF API（`gpio_if.h` 等，L1 `drivers/peripheral`）？API 级别必须与系统级别匹配（见 Step 6 硬伤检查）。
4. **五类场景适用性裁剪**：ISR 安全 / CMSIS 兼容两类仅 L0 适用（L1 无 ISR 直调/CMSIS 环境）——L1 改覆盖正向/边界/异常/生命周期，不硬凑五类（L1-Linux watchdog，iter09 实证 = 6+4+6+1=17 用例）。
5. **板上运行链预估**（L0）：烧板后测试要靠 HCTest zinitcall 机制自动跑（见 Step 5.5）——生成时即提醒用户 linker.ld 需要 KEEP `.zinitcall.test*` / `.zinitcall.run*` / `.zinitcall.sys.service*`，否则烧板测试不跑/HardFault（实测真坑）。

## Prohibited Practices（测试生成禁止操作）

| 禁止 | 正确做法 |
|------|---------|
| **L0 测试生成 C++/HWTest 代码** | L0 = 纯 C（HCTest + iCunit），MCU 无 C++ 运行时；L1-Linux 才用 HWTest/gtest（L1-LiteOS-A 按平台 acts 范式确认） |
| **L1 测试生成 iCunit 断言** | iCunit 仅限 L0；断言体系按框架走：L1-Linux（及已确认 HWTest 的平台）用 gtest 断言（`EXPECT_EQ`/`ASSERT_TRUE` 等），L1-LiteOS-A 未确认框架前不预设断言体系 |
| 凭记忆使用测试宏名（如"大概是 TEST_ASSERT_EQ"） | 对照 `references/hctest-unity-guide.md` §2-4 的精确宏名：`TEST_ASSERT_EQUAL_INT32`（不是 `TEST_ASSERT_EQ`） |
| **ISR 注册用例传 NULL callback 期望 SUCCESS** | HAL `IoTGpioRegisterIsrFunc` 传 NULL callback 返回 `HI_ERR_GPIO_INVALID_PARAMETER`(`0x80001040`)，不会走注册路径。ISR 用例必须传真 callback 函数（`GpioIsrCallbackFunc` 类型，签名 `typedef void (*GpioIsrCallbackFunc)(char *arg)`），传 NULL 是参数校验测试不是 ISR 功能测试，且会假红 |
| 生成不区分正向/异常/边界的扁平测试 | 必须按 Step 3 五类场景分别生成，每类有独立的测试函数和注释 |
| 忽略测试标签（TestFlag） | L0: `Function \| MediumTest \| Level1`；L1: `TestSize.Level0` |
| 生成测试代码带有芯片特定的硬编码引脚号 | 使用 `#define TEST_PIN_VALID` 宏定义，由用户根据实际板级配置修改 |
| 跳过 BUILD.gn 只生成测试 .c/.cpp | L0/L1 均使用 `import("//build/lite/config/component/lite_component.gni")` + `lite_component()` 模板 |
| 取不到的接口语义/预期返回值直接标 TODO 留空 | **先上网查（用宿主联网检索能力，WebSearch 或等价物；坏用备选联网检索 CLI，如 opencode）**，查到填值并注明来源；确实查不到才标 TODO 并注明来源/查询关键词，禁止凭记忆编造或留空 |

---

## ① 文件路由表

根据用户意图，读取对应的参考文件。**每次只读一个**，不要一次性加载所有 reference。

| 用户意图 | Agent 读取 | 预估行数 |
|---------|-----------|:-------:|
| 选择测试框架（L0 vs L1）、理解 HCTest/iCunit/Unity/HWTest 关系 | `references/hctest-unity-guide.md` §1 | ~100 |
| 查 HCTest 套件注册宏（`LITE_TEST_SUIT`/`LITE_TEST_CASE`/`RUN_TEST_SUITE`） | `references/hctest-unity-guide.md` §2 | ~60 |
| 查 iCunit 断言宏（`ICUNIT_ASSERT_EQUAL` 等，仅 L0） | `references/hctest-unity-guide.md` §3 | ~50 |
| 查 Unity 断言宏（`TEST_ASSERT_EQUAL_INT32` 等） | `references/hctest-unity-guide.md` §2.3 | ~30 |
| 查 HWTest/gtest 用法（`HWTEST_F` + `EXPECT_EQ`，L1-Linux 路线） | `references/hctest-unity-guide.md` §4 | ~60 |
| 查 L0/L1 测试 BUILD.gn 模板 | `references/hctest-unity-guide.md` §7 | ~80 |
| 查 GPIO 驱动完整测试示例（Hi3861 L0 — 正向/异常/边界） | `references/test-code-templates.md` §2 | ~230 |
| 查 I2C 驱动完整测试示例（STM32F407 L0 — 含 CMSIS 兼容性） | `references/test-code-templates.md` §3 | ~90 |
| 查其他外设测试模板（SPI/UART/ADC/PWM/CMSIS/WiFi） | `references/test-code-templates.md` §4-9 | 按需 |
| 了解三种测试写法对比（L0混合/L0纯Unity/L1-Linux HWTest） | `references/hctest-unity-guide.md` §1.3 | ~20 |

---

## ② 工作流

### Step 1: 收集测试输入

生成测试代码前，必须收集以下信息（缺失项需追问用户）：

| 必填项 | 说明 | 示例 |
|-------|------|------|
| 驱动头文件 | 被测驱动的 HAL 接口头文件（.h） | `gpio_if.h` |
| 系统级别 | L0 (LiteOS-M) / L1 (LiteOS-A / L1-Linux) | L0 |
| 外设类型 | GPIO / I2C / SPI / UART / ADC / PWM / RTC / Watchdog / WiFi | GPIO |
| 驱动接口函数列表 | 从头文件中提取的函数签名 | `int32_t GpioOpen(uint16_t gpio)` |
| 芯片型号（选填） | 用于参照已有芯片的测试示例 | Hi3861 |

### Step 2: 选择测试框架

Read `references/hctest-unity-guide.md` §1（框架总览 + 选择决策），根据系统级别确定框架：

```
系统级别判定：
├── L0（MCU, LiteOS-M, 纯 C）
│   └── 框架: HCTest + iCunit 混合模式
│       结构: LITE_TEST_SUIT / LITE_TEST_CASE / RUN_TEST_SUITE（HCTest）
│       断言: ICUNIT_ASSERT_EQUAL / ICUNIT_ASSERT_NOT_EQUAL 等（iCunit）
│       语言: 纯 C
│       RAM: ~3KB（HCTest ~2KB + iCunit ~1KB）
│       C++: 不需要
│
└── L1（MPU, LiteOS-A / L1-Linux, 支持 C++）
    └── 框架: L1-Linux → HWTest（HWTEST_F + gtest 断言，实证）；
              L1-LiteOS-A → 按平台 acts 范式确认（不默认 HWTest）
        结构: class TestSuite : testing::Test {} + HWTEST_F 宏
        断言: EXPECT_EQ / ASSERT_TRUE / EXPECT_NE 等（gtest）
        语言: C++
        RAM: ~64KB+（gtest 引擎）
        C++: 必须
```

### Step 3: 分析驱动接口 + 按五类场景生成测试

Read `references/test-code-templates.md`（找到对应外设的模板），分析头文件中的每个接口函数，按五类场景生成：

```
对头文件中每个 HAL 接口函数 F：
  ├── 正向功能测试: F 正常调用 → 预期返回值 = 成功
  │   例: GpioOpen(VALID_PIN) → 预期返回 0
  │
  ├── 边界值测试: F 在参数边界上的行为
  │   例: GpioOpen(0) / GpioOpen(MAX_PIN) → 预期返回 0 或明确的错误码
  │
  ├── 异常路径测试: F 传入非法参数 → 预期返回错误码
  │   例: GpioOpen(INVALID_PIN) → 预期返回非 0
  │
  ├── 中断安全测试（仅 L0 MCU）:
  │   验证驱动函数在 ISR 上下文中的安全性
  │   例: 不在 ISR 中调用可能阻塞的 API（如带超时的信号量等待）
  │
  └── CMSIS 兼容性测试（仅 L0 Cortex-M）:
      验证驱动在 CMSIS-RTOS2 环境下的行为一致性
      例: 在 CMSIS 任务中调用 GpioOpen → 预期行为与裸机一致
```

**不硬编码引脚号**——使用宏定义，由用户根据实际板级配置修改：

```c
#define TEST_PIN_VALID     5    /* 用户修改为实际可用引脚 */
#define TEST_PIN_INVALID   99   /* 用户修改为超出范围的引脚号 */
```

### Step 4: 生成测试套件注册代码

#### L0 代码结构（HCTest + iCunit 混合模式）

Read `references/hctest-unity-guide.md` §2-3 + `references/test-code-templates.md` §2：

```c
#include "hctest.h"
#include "<periph>_if.h"

/* 测试常量 — 用户按板级修改 */
#define TEST_PIN_VALID     5
#define TEST_PIN_INVALID   99

/* ===== 正向功能测试 ===== */
LITE_TEST_SUIT(Peripheral, <Periph>, <Periph>TestSuite);

LITE_TEST_CASE(<Periph>TestSuite, Test<Function>Normal, 
    Function | MediumTest | Level1)
{
    int32_t ret = <Periph><Function>(<valid_params>);
    ICUNIT_ASSERT_EQUAL(ret, 0, ret);  /* 期望成功 */
}

/* ===== 边界值测试 ===== */
LITE_TEST_CASE(<Periph>TestSuite, Test<Function>Boundary, ...)
{ ... }

/* ===== 异常测试 ===== */
LITE_TEST_CASE(<Periph>TestSuite, Test<Function>InvalidParam, ...)
{
    int32_t ret = <Periph><Function>(<invalid_params>);
    ICUNIT_ASSERT_NOT_EQUAL(ret, 0, ret);  /* 期望失败 */
}

RUN_TEST_SUITE(<Periph>TestSuite);
```

#### L1-Linux 代码结构（HWTest/gtest）

Read `references/hctest-unity-guide.md` §4：

```cpp
#include <gtest/gtest.h>
#include "<periph>_if.h"

using namespace testing::ext;

class <Periph>Test : public testing::Test {
protected:
    static void SetUpTestCase() { /* 初始化 */ }
    static void TearDownTestCase() { /* 清理 */ }
};

HWTEST_F(<Periph>Test, Test<Function>Normal, TestSize.Level0)
{
    int32_t ret = <Periph><Function>(<valid_params>);
    EXPECT_EQ(0, ret);
}
```

### Step 5: 生成 BUILD.gn

Read `references/hctest-unity-guide.md` §7：

**L0 BUILD.gn**（HCTest 依赖）：
```gn
import("//build/lite/config/component/lite_component.gni")

lite_component("{{test_target_name}}") {
  features = [ ":{{test_target_name}}_bin" ]
}

executable("{{test_target_name}}_bin") {
  sources = [ "{{TEST_SOURCE_FILE}}" ]
  include_dirs = [
    "//kernel/liteos_m/kal/cmsis",
    "//drivers/lite/include",
    "//test/xts/acts/kernel_lite/kernelcmsis_hal",
  ]
  deps = [
    "//drivers/lite/{{PERIPHERAL_TYPE}}:{{peripheral_lib}}",
    "//kernel/liteos_m:liteos_m",
  ]
  ldflags = [ "-Wl,--gc-sections" ]
}
```
> 作为 XTS 兼容性测试运行时，`config.json` 需注册 `xts_acts` + `xts_tools` 组件，链接选项含 `-lhctest`。

**L1-Linux BUILD.gn**（HWTest 依赖）：
```gn
import("//build/lite/config/component/lite_component.gni")

local_flags = [ "-fpermissive", "-O2", "-fPIE" ]

config("public_config_for_smoke") {
  include_dirs = [
    "//kernel/liteos_a/testsuites/include",
    "//drivers/peripheral/{{PERIPHERAL_TYPE}}/hal",
  ]
}

executable("{{test_target_name}}") {
  sources = [ "{{TEST_SOURCE_CPP}}" ]
  configs = [ ":public_config_for_smoke" ]
  cflags = local_flags
  deps = [ "//drivers/peripheral/{{PERIPHERAL_TYPE}}/hal:{{peripheral_lib}}" ]
}
```

### Step 5.5: HCTest 自动运行机制（L0，实测沉淀）

生成的测试用例**不会自己跑**——靠 HCTest + samgr 启动期自动遍历 zinitcall 段触发。生成测试代码前必须理解这条链，否则烧板后"测试没跑"会误判为驱动 bug。

**注册链**（`LITE_TEST_SUIT` → 段 → runner 遍历）：

```
LITE_TEST_SUIT(subsystem, module, TestSuiteName)
   └─ 宏展开经 SYS_SERVICE_INIT / LAYER_INITCALL_DEF → 把套件注册函数指针放进 .zinitcall.test2.init 段
   └─ samgr 启动期 INIT_TEST_CALL 遍历 .zinitcall.test2.init 段 → 逐个调用注册函数 → 把 suite 加进 runner
   └─ RUN_TEST_SUITE(Suite) 经 TEST_INIT → 同样进 .zinitcall.test2.init → runner 遍历时触发 suite 执行
```

**关键约束**：
- **linker.ld 必须 `KEEP(*(SORT_BY_NAME(.zinitcall.test*)))`**（含 `.zinitcall.test2.init`）。若只 KEEP 了 `.zinitcall.{bsp,device,core,sys,app}{0..4}.init` 而漏掉 `.zinitcall.test*`，gc-sections 会丢掉 test 注册指针 → 烧板测试不跑（看似驱动无响应，实为测试根本没注册进 runner）。这是 gc-sections 坑的 test 段特例——见 Step 7 §抗 gc-sections。
- `config.json` 须注册 `xts_acts` + `xts_tools` 组件，链接选项含 `-lhctest -lbootstrap -lbroadcast`，否则 zinitcall.test2 段虽在但 runner 不被拉进镜像。

> 该机制是 Step 7 §抗 gc-sections 的前置：test 段被丢 = 测试不跑 = 烧板无测试输出，不是驱动/烧录问题。

### Step 6: 交叉验证

对照 `references/hctest-unity-guide.md` 逐条检查：

| 检查项 | 方法 | 级别 |
|--------|------|:----:|
| **L0/L1 框架不混用** | L0 不含 `HWTEST_F`/`EXPECT_EQ`/C++ class；L1-Linux（及已确认 HWTest 的平台）不含 `ICUNIT_ASSERT`/`LITE_TEST_CASE`；L1-LiteOS-A 框架确认前跳过此检查，确认后按实际框架校验 | ERROR |
| **API 级别校验** | L0 测试只用 IoT API（`IoTGpio*`/`IoTI2c*` 等 `iot_hardware` 接口），L1 测试只用 HDF API（`GpioCntlr*`/`I2cCntlr*` 等 `drivers/peripheral` 接口），**不混用**。mini-only API（仅小型系统支持的接口）**不能当全量 L1 接口测**——若被测接口在 L0/L1 通用集外，须标注适用范围，别把 mini-only 当 L1 全量。L0 测试出现 HDF/mini-only API 或 L1 测试出现 IoT API 均为硬伤 | ERROR |
| **测试标签完整** | L0: 每个 `LITE_TEST_CASE` 有 `Function \| MediumTest \| Level1` 标签；L1-Linux: 每个 `HWTEST_F` 有 `TestSize.Level0`（L1-LiteOS-A 按确认后的实际框架校验标签） | ERROR |
| **断言宏名正确** | 对照 `hctest-unity-guide.md`：`ICUNIT_ASSERT_EQUAL` 不是 `ICUNIT_ASSERT_EQ`；`TEST_ASSERT_EQUAL_INT32` 不是 `TEST_ASSERT_EQ` | ERROR |
| **边界断言不能退化恒真** | 边界值测试的断言必须有**判别力**——禁止 `TEST_ASSERT_UINT32_WITHIN(1, 0, ret)` 这类对 unsigned 等于 `ret∈{0,1}` 而 0/1 恰是全部可能返回值的退化断言（等于"不崩测试"不是边界测试）；禁止 `assert(常量)`/`TEST_ASSERT_TRUE(1)` 等恒真断言。边界测试应断言**具体预期值**（如 `TEST_ASSERT_EQUAL_INT32(IOT_SUCCESS, ret)` 对合法边界 pin、`TEST_ASSERT_EQUAL_INT32(IOT_FAILURE, ret)` 对非法边界），否则没判别力 | ERROR |
| **异常断言不基于未文档化假设** | 如"未 Init 即失败"——头文件未承诺该语义时，实现可能直接写寄存器返回 SUCCESS，断言 `!= IOT_SUCCESS` 会**假红**。头文件未规定的内部状态机行为不能硬断，应改为"记录实际返回值"或删除该用例 | WARNING |
| **ISR 安全用例名副其实** | ISR 安全测试不能只同步调 callback 验 flag（那只测了"callback 函数能跑"）——须验证真 ISR 上下文约束（中断触发、callback 内无阻塞 HAL 调用）。名实不符的 ISR 用例须重构或改名 | WARNING |
| **BUILD.gn include 路径核对** | L0 `include_dirs` 的 `iot_hardware` 路径用**正确名**：`//base/iot_hardware/peripheral/...`（带下划线），**不是** `//base/iothardware/...`（无下划线会编译失败，除非有 symlink 兜底）。L1 `//drivers/peripheral/...` 路径同理核对 | ERROR |
| **BUILD.gn 依赖完整** | L0 `deps` 含 `//kernel/liteos_m:liteos_m` + `//drivers/lite/...`；L1 含 `//drivers/peripheral/...` | ERROR |
| **五类场景覆盖** | 正向 / 边界 / 异常 / ISR安全（仅 L0 MCU）/ CMSIS（仅 L0 Cortex-M）— 每类至少一个测试用例 | ERROR |
| **用例去重** | 同类用例不重复（如边界用例与正向用例逻辑几乎一致、没带来新边界信息则合并或删一个）；用例计数与声明一致 | WARNING |
| **不硬编码引脚号** | 使用 `#define TEST_PIN_VALID` 宏，不直接写 `GpioOpen(5)` | WARNING |
| **HAL 接口仅使用公开头文件** | 测试代码不 `#include` 驱动内部头文件或直接访问寄存器 | ERROR |
| **测试函数体抗 gc-sections**（L0 关键坑）| 每个测试用例函数（`initCase*`/`*_runTest`）的函数体必须真编进镜像，不能被 `--gc-sections` 当未引用丢弃。验证：编完后 `nm OHOS_Image \| grep initCase` 每个函数地址非 0、size 非零；map 文件里 `.text.initCase*` 段地址非 `0x0000000000000000`。**只留悬挂 zinitcall 指针、函数体被丢 = 烧板 HardFault**（实测暴露真坑）。见 Step 7 §抗 gc-sections | ERROR |

### Step 7: 编译验证

告知用户将测试文件加入工程后运行编译：

```bash
# 在 OpenHarmony 仓库根目录
./build.sh --product <product_name>
```

常见测试编译错误：
- `ICUNIT_ASSERT_EQUAL undeclared` → 缺少 `#include "iCunit.h"` 或 `#include "osTest.h"`（L0 iCunit 模式）
- `HWTEST_F undeclared` → 缺少 `#include <gtest/gtest.h>`（L1-Linux HWTest 模式）

#### §抗 gc-sections（L0 必读，实测暴露的真坑）

**问题**：LiteOS-M L0 镜像默认开 `-Wl,--gc-sections` 丢弃"未引用"段。HCTest 的 `LITE_TEST_CASE` 宏（pristine 模式）经 `SYS_RUN(initCase##case_object)` → `LAYER_INITCALL_DEF(func, test, "test")` 把 `initCase*` 函数指针放进 `.zinitcall.run2.init` 段，`LITE_TEST_SUIT` 经 `SYS_SERVICE_INIT` 放进 `.zinitcall.sys.service2.init`，`RUN_TEST_SUITE` 经 `TEST_INIT` 放进 `.zinitcall.test2.init`。**若芯片 linker.ld 只 KEEP 了 `.zinitcall.{bsp,device,core,sys,app,test}{0..4}.init` 而没 KEEP `.zinitcall.run*` / `.zinitcall.sys.service*`，gc-sections 会丢掉 initCase 指针 → initCase 函数体因无引用被连带丢弃 → 镜像里只剩 `runSuite` 的 zinitcall.test 指针（悬挂）→ 烧板跑到测试注册时解引用空/错指针 HardFault。**

**症状**（任一命中即此坑）：
- `nm OHOS_Image | grep initCase` 输出空，或函数地址全 0
- map 文件里 `.text.initCase*` 行地址为 `0x0000000000000000`、且后面无分配地址
- 只有 `__zinitcall_test_runSuite*` 在符号表，无 `__zinitcall_run_initCase*`

**修法**（按优先级，选第一个能落地的）：
1. **linker.ld 加 KEEP（最对，HCTest 标准机制本应如此）**：在 `.zInit` 段内追加
   ```ld
   __zinitcall_run_start = .;
   KEEP (*(SORT_BY_NAME(.zinitcall.run*)))
   __zinitcall_run_end = .;
   . = ALIGN(4);
   __zinitcall_sys_service_start = .;
   KEEP (*(SORT_BY_NAME(.zinitcall.sys.service*)))
   __zinitcall_sys_service_end = .;
   . = ALIGN(4);
   __zinitcall_test_start = .;
   KEEP (*(SORT_BY_NAME(.zinitcall.test*)))
   __zinitcall_test_end = .;
   . = ALIGN(4);
   ```
   覆盖 `SYS_RUN`（`.zinitcall.run*`）、`SYS_SERVICE_INIT`（`.zinitcall.sys.service*`）和 `LITE_TEST_SUIT`/`RUN_TEST_SUITE`（`.zinitcall.test*` 含 `.zinitcall.test2.init`）三套 initcall 段。**漏 `.zinitcall.test*` = 测试不注册 = 烧板无测试输出**（实测暴露）。改完**必须强制重链**（`touch linker.ld` + ninja 显式 rebuild kernel image target，ninja 默认可能不把 `-Wl,-T` 传的 ld 文件算进依赖图，增量构建会跳过重链）。
2. **HCTEST_NEW_RUNNER 模式 + linker.ld KEEP `.xts_init*`**：若产品开了 `xts_overlay`/`hctest_rodata_opt`，`LITE_TEST_CASE` 走 `.xts_init.MODULE_NAME` 段 + `__attribute__((used))`——此时 linker.ld 须 `KEEP(*(SORT_BY_NAME(.xts_init*)))`，否则同样被丢。
3. **给 initCase 函数加 `__attribute__((used))`**：仅在宏展开不自动加 `used` 时手动补（pristine 模式 `SYS_RUN` 已隐式走 section 属性，但函数体本身没 `used`，靠 section KEEP 兜底；若改不了 linker.ld 可作兜底）。
4. **关 `--gc-sections`**：最暴力，镜像变大，**不推荐**（影响全镜像体积、可能超 flash 预算）。

**编后必验**（3 条全过才算修好）：
```bash
# 1. initCase 函数地址非 0、计数 = LITE_TEST_CASE 数
$TOOLCHAIN-nm OHOS_Image | grep -cE '^[0-9a-f]+ t initCase'   # 应 = 用例数
# 2. __zinitcall_run_initCase* 指针非 0
$TOOLCHAIN-nm OHOS_Image | grep -cE '^[0-9a-f]+ r __zinitcall_run_initCase'  # 应 = 用例数
# 3. linker 段边界符号存在
$TOOLCHAIN-nm OHOS_Image | grep -E '__zinitcall_run_(start|end)'
```
任一为 0/空即未真修。**不要只看"build success"就报完成**——ninja 不重链时旧 OHOS_Image 仍在，build success 但镜像没变。

---

## Exceptions and Fallbacks（异常与兜底）

| 场景 | 处理 |
|------|------|
| **接口语义/预期返回值不确定** | 先用宿主联网检索能力（WebSearch 或等价物，坏用备选联网检索 CLI 如 opencode 兜底）查头文件注释/OpenHarmony 源码用法；查到填值并注明来源；确实查不到才标 TODO + 注明查询关键词，禁止凭记忆编造或留空 |
| **头文件缺失/不可读** | 追问用户提供 HAL 接口头文件，不凭记忆猜测函数签名 |
| **系统级别（L0/L1）未知** | 追问；不默认猜（框架选错是全量返工） |
| **被测接口疑似 mini-only**（仅 L0 轻量系统支持，L1 小型可能没有） | 不当全量 L1 接口测；标注适用范围，提示用户核实接口适用性 |
| **ISR 用例拿不到真中断触发条件** | 不降级为"只同步调 callback 验 flag"冒充 ISR 测试（名不副实坑）——改为标注"需真 ISR 触发条件，TODO"或重构为参数校验用例并改名 |
| **编译报 `ICUNIT_ASSERT_EQUAL undeclared` / `HWTEST_F undeclared`** | 按 Step 7 常见错误表补 `#include`（`iCunit.h`/`osTest.h` 或 `<gtest/gtest.h>`） |
| **烧板后测试不跑（无测试输出）** | 不是驱动 bug——按 Step 5.5/Step 7 §抗 gc-sections 排查：linker.ld KEEP `.zinitcall.test*`、config.json 注册 xts_acts/xts_tools、nm 验 initCase 计数 |
| **烧板跑到测试注册就 HardFault** | initCase 函数体被 gc-sections 丢弃（悬挂 zinitcall 指针）——按 Step 7 §抗 gc-sections 修法 1 加 KEEP + 强制重链，nm 三条验证 |
| **ISR callback 传 NULL 导致烧板 HardFault** | 实测 v1 真坑——ISR 用例必须传真 callback 函数（`GpioIsrCallbackFunc` 类型），见禁止操作表 |
| **用例计数与声明不一致** | 生成后 grep 实数（`LITE_TEST_CASE`/`HWTEST_F` 个数）核对声明数，对不上先修正再交付（实测计数偏差教训） |

---

> 测试框架速查: `references/test-framework-cheatsheet.md`
