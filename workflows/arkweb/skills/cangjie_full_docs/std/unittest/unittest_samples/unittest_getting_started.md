# Unittest 快速入门

先编写一个简单的仓颉函数：

<!--compile -unittest -->
```cangjie
func add(left: Int64, right: Int64) {
    return left + right
}
```

将这个函数保存在 `add.cj` 文件中，开始编写该函数的测试代码：

<!--compile -unittest -->
```cangjie
@Test
func addTest() {
    @Expect(add(2, 3), 5)
}
```

测试包含如下组件：

- `@Test` 宏，配置在 `addTest` 函数上，表示这是一个测试函数。
- `@Expect` 宏，作为断言，检查输入的两个参数是否相等。在这个例子中，两个参数分别是 `add` 函数的结果 `add(2, 3)` 和预期值 `5` 。

将这个测试函数保存在 `add_test.cj` 文件中，和代码函数一起在 `add.cj` 中运行。

```bash
cjc add.cj add_test.cj --test -o add_test
./add_test
```

在测试执行过程中，将动态显示进度报告：

```text
group example                                0% [-------------------------]      (00:00:01)
test TestCase_addTest.addTest                                                    (00:00:01)

passed: 0, failed: 0                            0% [-------------------------]  0/1 (00:00:01)
```

正常情况下，将得到如下类似输出：

```text
-------------------------------------------------------------------------------------------------
TP: default, time elapsed: 59363 ns, Result:
    TCS: TestCase_addTest, time elapsed: 32231 ns, RESULT:
    [ PASSED ] CASE: addTest (28473 ns)
    Summary: TOTAL: 1
    PASSED: 1, SKIPPED: 0, ERROR: 0
    FAILED: 0
--------------------------------------------------------------------------------------------------
```

至此，我们就完成了测试的构建和运行。
下面我们来详细介绍一下用来构建测试的 `cjc` 命令。

```shell
#   待测试的代码文件
#   ↓
cjc add.cj add_test.cj --test -o add_test
#          ↑           ↑
#          |           --test 表明在测试模式下构建生成二进制文件
#          测试文件
```

注意，对于复杂项目来说，不建议直接运行 `cjc` 编译器。
对于结构庞大的大型项目，建议使用 `cjpm` 包管理器。
以 `cjpm` 项目测试为例。

首先创建一个简单的 `cjpm` 项目，其中包含一个名为 `example` 的包。
项目的文件结构如下所示（借用 `cjc` 示例中的文件）：

```text
- src
  |
  +- example
     |
     +- add.cj
     +- add_test.cj
```

原文件已指明它们属于 `example` 包，因此只需运行以下命令即可初始化 `cjpm` 项目：

```bash
cjpm init --name example
```

`cjpm` 包管理器内置支持运行单元测试，所以直接运行即可：

```bash
cjpm test
```

此命令会运行项目所有包中的测试，统一生成如下类似输出：

```text
--------------------------------------------------------------------------------------------------
TP: example/example, time elapsed: 60989 ns, Result:
    TCS: TestCase_addTest, time elapsed: 32804 ns, RESULT:
    [ PASSED ] CASE: addTest (29195 ns)
    Summary: TOTAL: 1
    PASSED: 1, SKIPPED: 0, ERROR: 0
    FAILED: 0
--------------------------------------------------------------------------------------------------
```

注意，无需指定 `--test` 或任何其他特殊选项。
默认情况下，`cjpm` 使用项目中的文件名来确认文件应该在测试模式还是正常模式下编译。
示例包中， `add_test.cj` 是测试文件，文件名以 `_test.cj` 结尾。
正常构建时，二进制文件或库的构建不包含这些文件。

单元测试框架 API 已经存在于 `std` 模块的 `unittest` 包中，宏也存在于 `std` 模块的 `unittest.testmacro` 包中，因此不需要在测试文件中显式导入。

如需了解更多关于 unittest 框架的基本概念，请参考[单元测试基础](./unittest_basics.md)。
