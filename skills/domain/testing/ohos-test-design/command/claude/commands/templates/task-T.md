# 测试任务规格

> 测试实现的最小可执行单元。可由 AI Agent 或开发者据此独立完成测试代码编写。
> 基于 task.md 结构扩展，增加工具调用指令段。

## 任务元数据

| 字段 | 内容 |
|------|------|
| Task ID | TASK-T-{XXXX} |
| 标题 | [测试任务标题] |
| 任务类型 | 测试实现 |
| 关联 Feature | [FEAT-XXXX] |
| 关联 Test Design | test-design.md |
| 关联 Dev Task | [TASK-XXXX]（前置开发任务） |
| 目标仓库 | [仓库名] |
| 目标模块 | [模块路径] |
| 实现方式 | 手写 / 自动生成 / 混合 |
| 对接工具 | ohos-test-arkts-xts-generation / ohos-test-capi-xts-generation / gtest / Hypium / 无 |
| 优先级 | P0 / P1 / P2 |
| 状态 | Draft / Ready / Blocked / InProgress / Done |

## 任务描述

### 做什么

1. [具体步骤1]
2. [具体步骤2]

### 不做什么

- [明确排除项]
- [明确排除项]

## AC 与用例映射

| AC编号 | 用例编号 | 用例摘要 | 实现方式 | 验证方式 |
|--------|----------|----------|----------|----------|
| AC-1.1 | TC-1.1-01 | [摘要] | 自动生成 / 手写 | [断言/比对] |
| AC-1.1 | TC-1.1-02 | [摘要] | 手写 | [断言/比对] |

### 用例覆盖校验

> 分组完成后必须填写此表，确保 test-design.md 中的每条 TC 都有归属。

| 实现方式 | 用例数量 | 用例编号 |
|----------|:--------:|----------|
| 自动生成 | [数量] | [编号列表] |
| 手写补充 | [数量] | [编号列表] |
| **本任务合计** | **[总数]** | |
| test-design.md 总计 | [总数] | |

**覆盖率校验:** ∑(所有 task-T 的合计) = test-design.md 总用例数

### 前置依赖

| 类型 | 编号 | 原因 |
|------|------|------|
| Dev Task | [TASK-XXXX] | [开发实现完成才能测试] |
| Test Design | test-design.md | [用例定义来源] |
| 环境 | [依赖] | [需要的服务/配置] |

### 完成判据

- [ ] 所有覆盖用例已实现
- [ ] 所有测试执行通过
- [ ] 覆盖率达标
- [ ] 代码质量检查通过

## 受影响文件

| 操作 | 文件路径 | 说明 |
|------|----------|------|
| 新增 | [测试文件路径] | [测试用途] |
| 修改 | [BUILD.gn / 配置文件] | [修改内容] |

## 环境路径

> `/ohos-test-gen` 执行时会读取此段。如果路径未填写，会向用户询问后回填。

| 参数 | 值 | 说明 |
|------|-----|------|
| output_target_path | [XTS 目标工程路径，如 `D:\xts_acts_0414\graphic\graphic3D`] | 测试用例生成的目标目录 |
| d.ts_path | [.d.ts 文件完整路径] | API 定义文件绝对路径 |
| build_method | `linux_build_sh` / `windows_hvigorw` | 编译验证方式 |
| oh_root | N/A（Windows 环境） | Linux 平台 OpenHarmony 源码根目录 |
| xts_acts_path | [XTS 测试套根目录] | 如 `D:\xts_acts` |
| sdk_path | [SDK 路径] | OpenHarmony SDK 路径 |
| deveco_studio_path | [DevEco 路径] | DevEco Studio 安装路径 |

## 工具调用指令

> 根据实现方式填写对应段落。自动生成方式由工具产出代码；手写方式由开发者编写。

### 模式 A：自动生成（ohos-test-arkts-xts-generation）

**触发命令:** 使用 `/ohos-test-gen` 或直接触发 `ohos-test-arkts-xts-generation` skill

**输入参数:**
```yaml
subsystem: [子系统名]
d.ts_path: [.d.ts 文件完整路径]
output_target_path: [测试用例生成的目标工程路径]
target_apis:
  - [API 名称1]
  - [API 名称2]
syntax_type: dynamic / static
generation_scope:
  - positive          # 有效值正向测试
  - negative          # 无效值测试（负值、NaN、超范围）
  - boundary          # 边界值测试（0、默认值、精确边界）
  - combination       # 因子组合测试（参数交互）
coverage_baseline: [无 / 覆盖率报告路径]
tc_list: [本 task-T 覆盖的 TC 编号列表，来自 test-design.md]
env:
  oh_root: [OpenHarmony 源码根目录，Linux 平台]
  xts_acts_path: [XTS 测试套根目录]
  sdk_path: [OpenHarmony SDK 路径]
  deveco_studio_path: [DevEco Studio 安装路径]
```

**补充说明:**
> 工具根据 generation_scope 和 tc_list 生成用例。以下场景如果工具未能覆盖，需手动补充：
> - TC-{X.Y}-{NN}: [用例摘要] — [工具未能覆盖的原因]
> - TC-{X.Y}-{NN}: [用例摘要] — [需要特殊前置条件]

**预期产出:**
| 产出物 | 路径 |
|--------|------|
| 测试设计文档 | [路径] |
| .test.ets 文件 | [路径] |
| 覆盖率报告 | [路径] |

### 模式 B：自动生成（ohos-test-capi-xts-generation）

**触发命令:** 使用 `/ohos-test-gen` 或直接触发 `ohos-test-capi-xts-generation` skill

**输入参数:**
```yaml
subsystem: [子系统名]
h_file_path: [.h 头文件路径]
target_functions:
  - [C API 函数名1]
  - [C API 函数名2]
```

**N-API 三重校验（必须执行）:**
1. C++ 注册完整性：所有 `static napi_value` 函数 → `napi_property_descriptor desc[]`
2. TypeScript ↔ C++ 一致性：`desc[]` 中的函数 → `index.d.ts` 的 `export const`
3. ETS ↔ TypeScript 一致性：`.test.ets` 中的 `testNapi.xxx` → `index.d.ts` 的 `export const`

**预期产出:**
| 产出物 | 路径 |
|--------|------|
| NapiTest.cpp | entry/src/main/cpp/NapiTest.cpp |
| index.d.ts | entry/src/main/cpp/types/libentry/index.d.ts |
| .test.ets 文件 | entry/src/ohosTest/ets/test/*.test.ets |
| 构建配置 | BUILD.gn, CMakeLists.txt, Test.json |

### 模式 C：手写（gtest / Hypium）

**测试文件:** [文件路径]

**用例实现:**

```cpp
// TC-{X.Y}-{NN}: [用例标题]
// 关联 AC: AC-{X.Y}
TEST(TestSuiteName, TestCaseName) {
    // 前置条件
    // ...
    // 执行
    // ...
    // 断言
    EXPECT_EQ(expected, actual);
}
```

```typescript
// TC-{X.Y}-{NN}: [用例标题]
// 关联 AC: AC-{X.Y}
import { describe, it, expect } from '@ohos/hypium'

export default function TestSuiteName() {
  describe('TestSuiteName', () => {
    it('TestCaseName', 0, async () => {
      // 前置条件
      // 执行
      // 断言
      expect(result).assertEqual(expected)
    })
  })
}
```

### 质量检查（所有模式必执行）

**触发命令:**
```bash
/check-test-code-quality [测试文件路径] --level critical
```

**必查规则:**
| 规则 | 说明 | 适用 |
|------|------|------|
| R003 | 禁止恒真断言 | 全部 |
| R004 | 测试用例缺少断言 | 全部 |
| R008 | 用例声明格式 | XTS / Hypium |
| R009 | @tc.number 命名 | XTS |
| R016 | 用例命名规范 | 全部 |

**不通过处理:** 按质量报告修复后重新扫描，直到 0 Critical 问题。

## BUILD.gn 变更

```
文件路径: [路径]
变更说明: [新增测试目标/新增依赖]
```

## 实现阶段可调用能力

> 按 Task 复杂度和实际情况选择调用，非强制。引用自 workflow.md 插件能力集成。

| 场景 | 推荐能力 | 来源 | 说明 |
|------|----------|------|------|
| 测试方案不确定 | `/opsx:explore` | OpenSpec | 自由讨论后再实现 |
| 需要快速生成测试草案 | `/opsx:propose` | OpenSpec | 一键生成 proposal → 细化为测试代码 |
| 按任务列表逐步执行 | `/opsx:apply` | OpenSpec | 按 task-T 逐步推进实现 |
| 先写测试再写代码 | `superpowers:test-driven-development` | Superpowers | RED-GREEN-REFACTOR 流程 |
| 多个 task-T 独立可并行 | `superpowers:dispatching-parallel-agents` | Superpowers | 并行实现多个测试任务 |
| 按 task-T 逐步实现 | `superpowers:executing-plans` | Superpowers | 带检查点的有序执行 |
| 测试执行失败需排查 | `superpowers:systematic-debugging` | Superpowers | 系统化排查，不盲目试错 |
| 准备声称完成前 | `superpowers:verification-before-completion` | Superpowers | 证据先于声明，必须跑命令验证 |
| 测试代码需要审查 | `superpowers:requesting-code-review` | Superpowers | 测试代码质量把关 |

### 调用记录

> 记录本 task 实际调用的能力（便于复盘）。

| 能力 | 调用时机 | 效果 |
|------|----------|------|
| [能力名] | [何时调用] | [结果] |

## 验证检查清单

- [ ] 所有覆盖用例已实现并执行
- [ ] P0 用例全部通过
- [ ] AC 追溯矩阵中对应项已更新
- [ ] 工具产出文件完整（自动生成模式）
- [ ] N-API 三重校验通过（CAPI 模式）
- [ ] 代码质量检查通过（0 Critical）
- [ ] 覆盖率达标
- [ ] 构建通过
- [ ] 未修改文件范围外的内容

**完成证据:**

| 证据 | 命令/路径 | 结果 |
|------|-----------|------|
| 测试执行 | [命令] | PASS/FAIL |
| 覆盖率 | [报告路径] | [百分比] |
| 质量检查 | /check-test-code-quality [路径] | [Critical数] |
| 构建 | [命令] | PASS/FAIL |
