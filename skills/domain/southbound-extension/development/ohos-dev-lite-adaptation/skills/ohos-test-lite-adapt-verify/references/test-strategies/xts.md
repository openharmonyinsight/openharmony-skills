# XTS 测试策略参考

本文档是 `ohos-test-lite-adapt-verify` skill 的 **verify 阶段** 在选择 **XTS 测试套件**
作为验证策略时的详细操作指南。

> **注意**：XTS 只是可选测试策略之一。用户可在 `init` 阶段选择其他策略。
> 本文档仅在用户选择 XTS 时适用。

## 什么是 XTS

XTS（XTS Test Suite）是 OpenHarmony 的兼容性测试套件，包含：

| 子套件 | 英文 | 说明 |
|--------|------|------|
| ACTS | Application Compatibility Test Suite | 应用兼容性测试（JS/API 级别） |
| DCTS | Device Compatibility Test Suite | 设备兼容性测试（HAL/驱动级别） |
| HATS | Hardware Abstraction Test Suite | 硬件抽象层测试 |

对于 OH Lite（L0/L1）设备，主要涉及 **ACTS** 和 **DCTS**。

## 前置条件

1. 目标芯片的 OH 代码仓中已包含 XTS 测试代码（通常在 `test/xts/` 下）
2. 编译环境支持 XTS 编译（`build_xts=true` 模式）
3. 设备可通过串口输出 XTS 测试结果
4. 烧录工具支持待测芯片

## XTS 编译

### 编译模式

在 `ohos-ci-lite-deploy-burn` 中使用 `build_mode: xts_all`：

```json
{
  "build_modes": {
    "xts_all": {
      "product": "<product_name>",
      "build_xts": true,
      "xts_subset": "full"
    }
  }
}
```

### XTS 子集选择

| xts_subset 值 | 含义 | 编译时间 | 适用场景 |
|---------------|------|---------|---------|
| `full` | 全量 XTS | 长 | 完整验证 |
| `acts` | 仅 ACTS | 中 | 应用层验证 |
| `dcts` | 仅 DCTS | 中 | 驱动/HAL 验证 |
| `<module>` | 指定模块 | 短 | 快速回归 |

用户在 `init` 阶段或在 `verify` 阶段前确认子集范围。

## XTS 执行流程

### Phase 3：烧录

调用 `ohos-ci-lite-deploy-burn` Phase 3，使用 XTS 固件烧录：

- 烧录参数取自设备 profile 的 `burn` 配置
- 确保 XTS 固件大小不超过设备 Flash 上限

### Phase 4：复位 + 串口捕获

1. 复位设备（软复位 AT+RST 或 DTR / 手按）
2. 通过配置的 COM 口串口捕获输出
3. 捕获超时：根据 XTS 用例数量设定（通常 5~30 分钟）
4. 将原始输出保存到 `xts_test/reports/xts_raw_output.log`

## XTS 结果解析

### 输出格式特征

XTS 输出通常包含以下模式：

```
[==========] Running N test(s).
[ RUN      ] test_suite.test_name
[       OK ] test_suite.test_name (N ms)
[  FAILED  ] test_suite.test_name (N ms)
[==========] N test(s) ran.
[  PASSED  ] N test(s).
[  FAILED  ] N test(s).
```

### 解析规则

| 模式 | 含义 |
|------|------|
| `[ PASSED ]` 后跟数字 | 通过数 |
| `[ FAILED ]` 后跟数字 | 失败数 |
| `[ NOT RUN ]` 后跟数字 | 未运行数 |
| `[ RUN ]` + `[ OK ]` | 单条用例通过 |
| `[ RUN ]` + `[ FAILED ]` | 单条用例失败 |

### 结果报告格式

将解析结果写入 `xts_test/reports/verify_result.md`：

```markdown
# XTS 验证结果

## 基本信息
- 测试时间: <timestamp>
- 设备: <chip_name>
- 固件: <build_mode>
- XTS 子集: <subset>

## 统计汇总
| 指标 | 数值 |
|------|------|
| Total | N |
| Passed | N |
| Failed | N |
| Not Run | N |
| 通过率 | N% |

## 失败详情（如有）
| 用例 | 失败原因 | 是否本次改动引起 |
|------|---------|-----------------|

## MAP 对比（optimization 必填；test-only 有基线记参考值，无基线标 N/A）
- 镜像来源: <板上镜像构建时间戳/哈希 vs .map 来源构建；不同源须标注「不可与本次测试结果关联」
- RAM: <baseline> → <final> (<delta>)
- Flash: <baseline> → <final> (<delta>)

## 结论
- ✅ 通过 / ⚠️ 有条件通过（非本次 Fail） / ❌ 不通过
```

## 常见问题

### Q1: XTS 编译报错找不到测试代码
- 确认 `test/xts/` 目录存在于代码仓
- 确认产品配置 (`config.json`) 包含 XTS 子系统编译选项
- L0/L1 设备可能不支持完整 ACTS（JS 运行时限制），考虑只用 DCTS

### Q2: 烧录后设备没有 XTS 输出
- 确认烧录的是 XTS 固件（不是普通 firmware）
- 确认串口波特率正确（通常 115200 或 921600）
- 确认设备启动后触发了 XTS 执行（有些需要手动触发或特定启动参数）

### Q3: XTS 运行超时
- 增加串口捕获超时时间
- 减小 XTS 子集范围（`full` → `acts` 或指定模块）
- 检查设备是否在某个用例上卡死（可能是死锁/等待外设）

### Q4: 有 Fail 但不是本次改动引起的
- 归因分析两模式都做：在报告中标记「非本次改动引起」，记录用例名和失败原因，lessons 中记录以便追踪
- **放行按入口模式**：test-only——有 Fail 即终止并报告，不因归因放行；optimization——按已批准规则回炉，或用户明确接受后将该失败**单独标记为未达标**，不写成「验证通过」

## 与其他测试策略的关系

```
verify 阶段测试策略选择
├── XTS ←── 本文档适用的策略
│   ├── 优点: 标准化、可量化、官方认可
│   └── 缺点: 编译慢、L0/L1 支持有限
├── Unit Test
│   ├── 优点: 快速、精准定位
│   └── 缺点: 需要自行编写测试代码
├── Manual Test
│   ├── 优点: 灵活、无需自动化
│   └── 缺点: 不可复现、依赖人工
└── Custom
    └── 用户自定义
```
