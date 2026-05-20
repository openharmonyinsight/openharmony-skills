---
name: cangjie-std-unittest
description: "仓颉单元测试框架使用说明。"
---

# 仓颉语言单元测试 Skill

## 1. 快速入门

### 1.1 编译与运行
```bash
# 基于 cjc 使用（处理简单文件或包）
cjc code.cj test.cj --test -o test_binary
./test_binary

# 基于 cjpm 使用（标准项目）
cjpm test
cjpm test src src/koo   # 测试指定包
```

### 1.2 测试文件约定
- 测试文件命名为 `xxx_test.cj`，与 `xxx.cj` 并列
- 测试模式下 `unittest` 和 `unittest.testmacro` 自动导入，无需显式 import

---

## 2. 测试实体

### 2.1 测试函数
```cangjie
@Test
func addTest() {
    @Expect(add(2, 3), 5)
}
```
- 顶层函数标记 `@Test`，包含单个测试用例

### 2.2 测试类
```cangjie
@Test
class AddTests {
    @TestCase
    func addPositive() { @Expect(add(2, 3), 5) }

    @TestCase
    func addZero() { @Expect(add(2, 0), 2) }
}
```
- 类标记 `@Test`，须有无参构造函数
- 方法标记 `@TestCase`，每个方法为一个测试用例

---

## 3. 断言

### 3.1 断言宏列表
| 宏 | 失败行为 | 说明 |
|----|----------|------|
| `@Assert(a, b)` | 快速失败：立即停止测试 | 相等性断言 |
| `@Expect(a, b)` | 软失败：记录失败，继续执行 | 相等性断言 |
| `@Assert(condition)` | 快速失败 | 布尔断言 |
| `@Expect(condition)` | 软失败 | 布尔断言 |
| `@AssertThrows[ExType](expr)` | 快速失败 | 期望抛出异常 |
| `@ExpectThrows[ExType](expr)` | 软失败 | 期望抛出异常 |
| `@Fail("msg")` | 强制失败，停止测试 | 强制标记失败 |
| `@FailExpect("msg")` | 强制失败，继续执行 | 强制标记失败 |
| `@PowerAssert(expr)` | 快速失败 | 详细中间值图示 |

- **`@Assert(a, b)` / `@Expect(a, b)` 要求 `a` 的类型实现 `Equatable<B>`**（`B` 为 `b` 的类型）。若类型未实现 `Equatable`（如自定义枚举），须先通过 `@Derive[Equatable]` 或手动实现 `Equatable` 接口

### 3.2 近似相等（浮点数）
```cangjie
@Expect(1.0, 1.001, delta: 0.001)
```
- 类型须实现 `NearEquatable<CT, D>`，内置支持 Float16/32/64
- 也支持 `RelativeDelta` 相对误差：
  ```cangjie
  @Expect(1.0 != 1.901, delta: RelativeDelta(absoluteDelta: 0.001, relativeDelta: 0.02))
  ```
- 若 `delta` 参数不可用（取决于框架版本），可使用布尔断言替代：
  ```cangjie
  import std.math.*
  @Expect(abs(actual - expected) < 0.001)
  ```

### 3.3 自定义断言
```cangjie
@CustomAssertion
public func checkNotNone<T>(ctx: AssertionCtx, value: ?T): T {
    match (value) {
        case Some(v) => v
        case None => ctx.fail("Expected non-None")
    }
}
// 使用：@Assert[checkNotNone](myValue)
```

---

## 4. 测试生命周期（仅限测试类）

| 宏 | 执行时机 |
|----|----------|
| `@BeforeAll` | 所有测试用例执行前，执行一次 |
| `@BeforeEach` | 每个测试用例执行前 |
| `@AfterEach` | 每个测试用例执行后 |
| `@AfterAll` | 所有测试用例执行后，执行一次 |

执行顺序：`BeforeAll` → (`BeforeEach` → `TestCase` → `AfterEach`)* → `AfterAll`

---

## 5. 参数化测试

### 5.1 值驱动
```cangjie
@Test[x in [1, 2, 3]]
func squareTest(x: Int64) {
    @Expect(square(x), x * x)
}

@Test[x in 0..10]
func rangeTest(x: Int64) { ... }
```

### 5.2 随机参数
```cangjie
@Test[x in random()]
func randomTest(x: Int64) { ... }
```
- 生成约 200 个随机值，偏向边界值

### 5.3 多参数（笛卡尔积）
```cangjie
@Test[x in [1, 2], y in ["a", "b"]]
func multiParamTest(x: Int64, y: String) { ... }
```

### 5.4 类型参数化
```cangjie
@Types[T in <Int64, Float64, String>]
@Test
func genericTest<T>() { ... }
```

### 5.5 可复用策略
```cangjie
@Strategy[param in source]
func myStrategy(param: SomeType): ReturnType { ... }

@Test[data in myStrategy]
func strategyTest(data: ReturnType) { ... }
```

---

## 6. 基准测试

### 6.1 基本用法
```cangjie
@Test
class MyBench {
    @Bench
    func sortBenchmark() {
        let arr = generateArray(10000)
        arr.sort()
    }

    @Bench[size in [1000, 10000, 100000]]
    func paramBench(size: Int64) {
        let arr = generateArray(size)
        arr.sort()
    }
}
```
- 使用 `cjpm bench` 运行
- 框架自动处理预热、GC 噪声、统计分析（中位数、均值、置信区间）

### 6.2 测量源
```cangjie
@Measure[TimeNow(Nanos), CpuCycles()]
@Bench
func measuredBench() { ... }
```
- 可用测量源：`TimeNow`、`CpuCycles`、`Perf`（Linux 性能计数器）

---

## 7. 动态测试

```cangjie
@TestBuilder
func dynamicTests(): TestSuite {
    TestSuite.builder("DynTests")
        .add(UnitTestCase.create("case1") { @Expect(1, 1) })
        .add(UnitTestCase.create("case2") { @Expect(2, 2) })
        .build()
}
```
- 编程方式构建测试套件

---

## 8. 测试模板

```cangjie
@TestTemplate
abstract class BaseTests {
    @BeforeEach
    func setup() { ... }

    @TestCase
    func commonTest() { ... }
}

@Test
class MyTests <: BaseTests {
    @TestCase
    func specificTest() { ... }
}
```
- 定义可复用的测试用例和生命周期方法
- 生命周期顺序：基类 `@Before*` 先执行，派生类 `@After*` 先执行

---

## 9. 测试配置与标记

### 9.1 配置
```cangjie
@Configure[randomSeed: 42, generationSteps: 1000]
@Test
class ConfiguredTests { ... }
```

### 9.2 标签过滤
```cangjie
@Tag["fast"]
@TestCase
func fastTest() { ... }
```
命令行：`cjpm test --include-tags "fast" --exclude-tags "slow"`

### 9.3 跳过测试
```cangjie
@Skip
@TestCase
func skippedTest() { ... }
```

### 9.4 超时
```cangjie
@Timeout[Duration.second * 5]
@TestCase
func timeoutTest() { ... }
```

### 9.5 并行
```cangjie
@Parallel
@Test
class ParallelTests { ... }
```

---

## 10. Mock 框架

### 10.1 创建 Mock/Spy 对象
```cangjie
let repo = mock<Repository>()                    // 骨架对象，无默认行为
let repo2 = mock<Repository>([ReturnsDefaults])   // 自动返回默认值
let spyObj = spy<Service>(realService)             // 包装真实对象
```
- **mock**：所有成员未实现 — 未配桩的调用抛出错误
- **spy**：包装真实实例，未配桩的调用委托给原始实现
- `ReturnsDefaults`：自动返回默认值（0、false、""、None、空集合）
- `SyntheticFields`：将可变属性当作真实字段处理

### 10.2 配桩（`@On` 宏）
```cangjie
// 返回值
@On(repo.getData(testId, _)).returns(testResponse)

// 抛出异常
@On(repo.getData(_)).throws(TimeoutException())

// 调用失败
@On(repo.getData(_)).fails()

// 连续返回
@On(repo.getData(_)).returnsConsecutively([v1, v2, v3])

// 属性 getter/setter
@On(foo.name).returns("test")
@On(foo.name = _).doesNothing()

// 委托到真实实现（spy）
@On(spyObj.method()).callsOriginal()

// 顶层/静态函数
@On(loadEntry()).returns(entry)
@On(Entry.parse()).returns(testEntry)
```

### 10.3 参数匹配器
| 匹配器 | 说明 | 简写 |
|--------|------|------|
| `any()` | 任意参数 | `_` |
| `eq(value)` | 结构相等 | 字面量/标识符 |
| `same(ref)` | 引用相等 | — |
| `ofType<T>()` | 类型检查 | — |
| `argThat(predicate)` | 自定义谓词 | — |
| `none()` | Option None | — |
| `capture(listener)` | 捕获参数值 | — |

### 10.4 期望次数
```cangjie
@On(foo.bar()).returns().once()           // 恰好 1 次
@On(foo.bar()).returns().times(3)          // 恰好 3 次
@On(foo.bar()).returns().atLeastOnce()     // 至少 1 次
@On(foo.bar()).returns().anyTimes()        // 任意次数（不调用也不失败）
@On(foo.bar()).returns().atLeastTimes(2)   // 至少 2 次
```

### 10.5 桩链
```cangjie
@On(service.request())
    .throws(TimeoutException()).times(2)
    .then().returns(response).once()
```

### 10.6 Synthetic Fields
```cangjie
let field = SyntheticField.create(initialValue: "initial")
@On(foo.bar).getsField(field)
@On(foo.bar = _).setsField(field)
```

### 10.7 参数捕获
```cangjie
let captor = ValueListener<String>.new()
@On(renderer.renderBold(capture(captor))).callsOriginal()
// 测试后：
let args = captor.allValues()
let last = captor.lastValue()
```

---

## 11. 验证（Verify）

### 11.1 基本验证
```cangjie
Verify.that(@Called(foo.bar()))               // 至少调用一次
Verify.that(@Called(foo.bar()).once())         // 恰好一次
Verify.that(@Called(foo.bar()).never())        // 从未调用
Verify.noInteractions(mockObj)                 // 无任何调用
```

### 11.2 有序验证
```cangjie
Verify.ordered(
    @Called(foo.step1()),
    @Called(foo.step2()),
    @Called(foo.step3())
)
```

### 11.3 无序验证
```cangjie
Verify.unordered(
    @Called(foo.bar(0)).times(2),
    @Called(foo.bar(1)).times(2)
)

Verify.unordered(Partial, ...)   // 忽略未列出的调用
```

### 11.4 动态验证
```cangjie
Verify.ordered { v =>
    for (i in 0..n) {
        v.checkThat(@Called(foo.bar(i)))
    }
}
```

### 11.5 清除调用日志
```cangjie
Verify.clearInvocationLog()
```

---

## 12. CLI 选项

| 选项 | 说明 |
|------|------|
| `--bench` | 运行基准测试 |
| `--filter=pattern` | 过滤测试（通配符） |
| `--dry-run` | 打印测试列表 |
| `--include-tags`/`--exclude-tags` | 按标签过滤 |
| `--show-tags` | 显示标签 |
| `--timeout-each=10s` | 单个测试超时 |
| `--parallel` | 并行执行 |
| `--report-path`/`--report-format` | 报告输出（xml/csv/html） |
| `--no-capture-output` | 不捕获输出 |
| `--show-all-output` | 显示所有输出 |
| `--coverage-guided` | 覆盖率引导测试 |

---

## 13. 关键类型参考

### 核心类
| 类 | 用途 |
|----|------|
| `TestSuite` | 构建和执行测试套件 |
| `UnitTestCase` | 创建/执行单个测试用例 |
| `Benchmark` | 创建/运行单个基准测试 |
| `ConsoleReporter` / `XmlReporter` | 输出报告器 |
| `Configuration` | 测试配置存储 |

### Mock 相关类
| 类 | 用途 |
|----|------|
| `ConfigureMock` | 配置 mock 对象 |
| `Matchers` | 参数匹配器工厂 |
| `SyntheticField<T>` | 模拟可变字段 |
| `Verify` | 验证 API 入口 |
| `ValueListener<T>` | 参数捕获 |

### 关键接口
| 接口 | 用途 |
|------|------|
| `TestClass` | 提供 `asTestSuite()` 方法 |
| `NearEquatable<CT, D>` | 近似相等比较 |
| `Measurement` | 自定义基准测量 |
| `Arbitrary<T>` / `Shrink<T>` | 随机测试数据生成 |
