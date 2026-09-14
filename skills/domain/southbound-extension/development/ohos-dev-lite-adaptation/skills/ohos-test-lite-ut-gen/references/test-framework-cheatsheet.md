# Test Framework Cheatsheet

> From ohos-test-lite-ut-gen/SKILL.md (C2 progressive disclosure)

## ③ 测试框架速查

快速回忆用。详细 API 和模板见 `references/hctest-unity-guide.md` 和 `references/test-code-templates.md`。

### 框架选择速判

| 维度 | L0 轻量系统（MCU） | L1 小型系统（MPU） |
|------|------------------|------------------|
| 内核 | LiteOS-M | LiteOS-A / Linux（L1-Linux 路线） |
| 语言 | 纯 C | C++ |
| 推荐框架 | HCTest + iCunit 混合模式 | L1-Linux → HWTest（HWTEST_F + gtest）；L1-LiteOS-A 按平台 acts 范式确认 |
| 框架 RAM 开销 | ~3 KB | ~64 KB+ |
| 测试入口宏 | `RUN_TEST_SUITE(name)` | `HWTEST_F(Class, Name, Tag)`（L1-Linux） |

### L0 HCTest + iCunit 核心宏速查

#### HCTest 结构宏

| 宏 | 作用 |
|----|------|
| `LITE_TEST_SUIT(subsystem, module, name)` | 声明测试套件 |
| `LITE_TEST_CASE(suite, name, flags)` | 定义测试用例 `flags` = `Function \| MediumTest \| Level1` |
| `RUN_TEST_SUITE(name)` | 注册运行入口（系统启动时自动执行） |

#### iCunit 断言宏（仅 L0）

| 宏 | 作用 |
|----|------|
| `ICUNIT_ASSERT_EQUAL(a, b, ret)` | 断言 a == b，失败时记录行号+错误码 |
| `ICUNIT_ASSERT_NOT_EQUAL(a, b, ret)` | 断言 a != b |
| `ICUNIT_ASSERT_EQUAL_VOID(a, b, ret)` | 同上，用于 void 函数（失败时 `return` 无返回值） |
| `ICUNIT_ASSERT_NOT_EQUAL_VOID(a, b, ret)` | 同上，void 版 |

#### Unity 断言宏（L0/L1 通用，HCTest 内置）

| 宏 | 作用 |
|----|------|
| `TEST_ASSERT_EQUAL_INT32(expected, actual)` | int32_t 相等 |
| `TEST_ASSERT_EQUAL_UINT32(expected, actual)` | uint32_t 相等 |
| `TEST_ASSERT_TRUE(condition)` | 条件为真 |
| `TEST_ASSERT_NULL(pointer)` | 指针为 NULL |

### L1-Linux HWTest/gtest 核心宏速查

| 宏 | 作用 |
|----|------|
| `HWTEST_F(TestClass, TestName, TestSize.Level0)` | 定义测试用例 |
| `EXPECT_EQ(expected, actual)` | 非致命断言：相等 |
| `ASSERT_EQ(expected, actual)` | 致命断言：相等（失败则终止当前用例） |
| `EXPECT_NE(val1, val2)` | 非致命断言：不等 |

### L0/L1-Linux BUILD.gn 模板对照

| 构建项 | L0 (HCTest) | L1-Linux (HWTest) |
|-------|-----------|------------|
| import 路径 | `//build/lite/config/component/lite_component.gni` | `//build/lite/config/component/lite_component.gni` |
| 构建模板 | `lite_component()` + `executable()` | `lite_component()` + `executable()` |
| 源文件 | `.c` | `.cpp` |
| 链接 | `-lhctest -lbootstrap`（XTS 模式） | `-fPIE`（位置无关） |

### 五类测试场景速记

| 场景 | 目的 | L0 示例 | L1-Linux 示例 |
|------|------|---------|---------|
| **正向** | 正常调用成功 | `ICUNIT_ASSERT_EQUAL(ret, 0, ret)` | `EXPECT_EQ(0, ret)` |
| **边界** | 参数临界值 | pin=0, pin=MAX → 行为定义明确 | 同上 |
| **异常** | 非法参数 | pin=99 → `ICUNIT_ASSERT_NOT_EQUAL(ret, 0, ret)` | `EXPECT_NE(0, ret)` |
| **ISR安全** | 中断上下文安全 | 不在 ISR 中调用阻塞 API | N/A（L1 ISR 模型不同） |
| **CMSIS** | RTOS 兼容性 | 在 CMSIS 任务中调用 → 行为一致 | N/A（L1 不使用 CMSIS） |
