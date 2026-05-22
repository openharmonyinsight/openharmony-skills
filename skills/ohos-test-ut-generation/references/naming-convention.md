# 命名规范（推荐新规则 vs 兼容历史风格）

---

## 一、推荐新生成规则（标准格式）

**生成新测试时必须遵循以下规范**。

### 测试文件命名

**格式**：`[Module]Test.cpp`

**规则**：
- 使用CamelCase（驼峰命名）
- 以`Test`结尾
- 模块名对应被测模块名称

**示例**：
| 被测文件 | 测试文件 |
|----------|----------|
| `calculator.cpp` | `CalculatorTest.cpp` |
| `state_registry.cpp` | `StateRegistryTest.cpp` |
| `dmabuf_heap.cpp` | `DmabufHeapTest.cpp` |

### 测试套/类命名

**格式**：`[Module]Test`

**规则**：
- 与测试类名一致
- 使用CamelCase
- 以`Test`结尾

**示例**：
```cpp
// 测试套名：CalculatorTest
class CalculatorTest : public testing::Test { ... };

HWTEST_F(CalculatorTest, Add_001, TestSize.Level1)
```

### 测试用例命名

**格式**：`[FunctionName]_[SequenceNumber]`

**规则**：
- 函数名使用CamelCase
- 序号为**3位数字**，从`001`开始
- 同一函数的多个测试场景递增序号

**示例**（推荐生成格式）：
```cpp
HWTEST_F(CalculatorTest, Add_001, TestSize.Level1)  // 正常情况
HWTEST_F(CalculatorTest, Add_002, TestSize.Level2)  // 边界情况
HWTEST_F(CalculatorTest, Add_003, TestSize.Level2)  // 异常情况

HWTEST_F(CalculatorTest, Divide_001, TestSize.Level1)  // 正常除法
HWTEST_F(CalculatorTest, Divide_002, TestSize.Level2)  // 除零异常
```

### @tc.name命名

**规则**：
- 与HWTEST宏第2参数完全一致
- 格式：`[FunctionName]_[SequenceNumber]`

**示例**：
```cpp
/*
 * @tc.name: Add_001        // 与HWTEST第2参数一致 ✓
 */
HWTEST_F(CalculatorTest, Add_001, TestSize.Level1)
```

---

## 二、兼容历史存量风格（仅分析时参考）

**历史存量代码可能使用不同命名格式，生成新测试时不要模仿**。

### 常见历史格式

| 历史格式 | 示例 | 说明 |
|----------|------|------|
| `[TestSuite][FunctionName]_[Seq]` | `BBoxDetectorUnitTest001` | hiviewdfx仓库历史格式 |
| `[TestSuite]Test[Seq]` | `TraceStrategyTest001` | trace测试历史格式 |
| `Test[FunctionName]_[Seq]` | `TestSysEventDaoInsert_001` | 数据库测试历史格式 |

### 识别历史存量风格

使用 `scripts/analyze-existing-tests.py` 分析存量命名风格：
```bash
python scripts/analyze-existing-tests.py <test_directory> --output style_report.md
```

**分析结果用途**：
- 参考存量代码主要使用HWTEST还是HWTEST_F
- 参考存量代码使用`TestSize.Level1`还是`Level1`
- 参考存量代码的用例命名模式
- **生成新测试时仍遵循推荐新规则**

---

## 三、命名对照表（推荐新规则）

| 类型 | 格式 | 示例 |
|------|------|------|
| 测试文件 | `[Module]Test.cpp` | `CalculatorTest.cpp` |
| 测试套/类 | `[Module]Test` | `CalculatorTest` |
| 测试用例 | `[Func]_[001-999]` | `Add_001` |
| @tc.name | 与用例名一致 | `Add_001` |
| BUILD.gn目标 | `[module]_test`（小写） | `calculator_test` |
| 输出路径 | `[subsys]/[module]` | `hiview/bbox_detector` |

---

## 四、常见命名错误

### ❌ 错误示例

```cpp
// 错误：序号不是3位
HWTEST_F(Test, Add_1, TestSize.Level1)

// 错误：未使用CamelCase
HWTEST_F(Test, add_001, TestSize.Level1)

// 错误：测试文件命名不规范
// calculator_test.cpp（应使用CamelCase）
// test_calculator.cpp（Test应在末尾）

// 错误：@tc.name与用例名不一致
/*
 * @tc.name: add_001  // 小写，应大写
 */
HWTEST_F(Test, Add_001, TestSize.Level1)

// 错误：模仿历史存量格式
HWTEST_F(Test, TestAdd_001, TestSize.Level1)  // 不要用Test前缀
```

### ✅ 正确示例（遵循推荐新规则）

```cpp
// 正确：序号3位，CamelCase
HWTEST_F(CalculatorTest, Add_001, TestSize.Level1)

// 正确：测试文件命名
CalculatorTest.cpp
StateRegistryTest.cpp

// 正确：@tc.name一致
/*
 * @tc.name: Add_001
 */
HWTEST_F(CalculatorTest, Add_001, TestSize.Level1)
```

---

## 五、BUILD.gn目标命名

**格式**：`[module]_test`（小写）

**示例**：
```python
ohos_unittest("calculator_test") {
    module_out_path = "calculator/calculator_test"
    sources = [ "CalculatorTest.cpp" ]
}

ohos_unittest("state_registry_test") {
    module_out_path = "telephony/state_registry_test"
    sources = [ "StateRegistryTest.cpp" ]
}
```

---

## 六、输出路径命名

**格式**：`[subsystem]/[module]`

**规则**：
- 子系统名：OpenHarmony子系统（如hiviewdfx、telephony）
- 模块名：测试模块名

**示例**：
```python
module_output_path = "hiview/bbox_detector"
module_output_path = "telephony/state_registry_test"
module_output_path = "memory/dmabuf_heap_test"
```

---

## 相关文档

- [framework-quickref.md](framework-quickref.md) - 测试框架速查表
- [real-patterns.md](real-patterns.md) - 真实仓库示例（标注历史格式）
- [test-case-spec.md](test-case-spec.md) - 测试文件完整结构