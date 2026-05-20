# 测试模版

## 入门

测试模板功能有助于将一些常见的测试和基础设施代码提取到可重用的组件中。特别是，它对于测试类层次结构很有用。

要创建测试模板，请将 `@TestTemplate` 宏放在抽象类上：

<!-- compile-test1 -->
```cangjie
public class DbConnection {
    func close() {}
}
@TestTemplate
abstract class DbTest {
    public prop dbConnection: DbConnection

    @TestCase
    func testCommonDbApi1() { /* ... */ }

    @TestCase
    func testCommonDbApi2() { /* ... */ }
}
```

可用这个模板创建多个实际的测试套件，例如测试与不同特定数据库的连接。要使用测试模板，只需继承相应的类：

<!-- compile-test1 -->
```cangjie
@Test
class MySqlTest <: DbTest {
    var dbConnection_: ?DbConnection = None

    public override prop dbConnection: DbConnection {
        get() {
            dbConnection_.getOrThrow()
        }
    }

    @BeforeAll
    func initializeConnection() {
        dbConnection_ = Some(DbConnection())
    }

    @AfterAll
    func closeConnection() {
        dbConnection_?.close()
    }

    @TestCase
    func testSpecificlyMySqlFeatures() {
        /* ... */
    }
}
```

每个测试用例都将像在实际测试类本身中编写一样运行，结果如下：

```text
------------------------------------------------------------
TP: default, time elapsed: 177679 ns, RESULT:
    TCS: MySqlTest, time elapsed: 157163 ns, RESULT:
    [ PASSED ] CASE: testCommonDbApi1 (34704 ns)
    [ PASSED ] CASE: testCommonDbApi2 (8480 ns)
    [ PASSED ] CASE: testSpecificlyMySqlFeatures (8329 ns)
Summary: TOTAL: 3
    PASSED: 3, SKIPPED: 0, ERROR: 0
    FAILED: 0
------------------------------------------------------------
```

测试模板本身可以由其他测试模板构建。

## 生命周期方法

测试模板还可以包含一些生命周期方法： `@BeforeAll`, `@AfterAll`, `@BeforeEach`, `@AfterEach`。生命周期方法按指定顺序执行：

- `@Before_` 生命周期方法按照从基类到继承类的顺序运行。
- `@After_` 生命周期方法按照从继承类到基类的顺序运行。

`@_Each` 派生类的方法也适用于基类的测试用例。

<!-- run -->
```cangjie
@TestTemplate
abstract class BaseTemplate {
    @BeforeEach
    func baseBeforeEach() {
        println("base before each")
    }

    @AfterEach
    func baseAfterEach() {
        println("base after each")
    }
}

@TestTemplate
abstract class Template <: BaseTemplate {
    @TestCase
    func templateCase() {
        println("template case")
    }
}

@Test
class Test <: Template {
    @BeforeEach
    func beforeEach() {
        println("before each")
    }

    @AfterEach
    func afterEach() {
        println("after each")
    }

    @TestCase
    func testCase() {
        println("case")
    }
}
```

输出将为（启用输出捕获时）：

```text
------------------------------------------------------------
TP: default, time elapsed: 456925 ns, RESULT:
    TCS: Test, time elapsed: 456925 ns, RESULT:
    [ PASSED ] CASE: templateCase (38228 ns)
    STDOUT:
    base before each
    before each
    template case
    after each
    base after each
    [ PASSED ] CASE: testCase (16098 ns)
    STDOUT:
    base before each
    before each
    case
    after each
    base after each
Summary: TOTAL: 2
    PASSED: 2, SKIPPED: 0, ERROR: 0
    FAILED: 0
------------------------------------------------------------
```

## 配置

`@Configure` 可以放置在测试模板类上，但是继承类的 `@Configure` 会覆盖为基类放置的值。所有测试用例都在合并后的配置下执行。

## 与其他特性交互的规则

- `@Parallel` 不能与 `@TestTemplate` 同时使用。
- `@Types` 不能与 `@TestTemplate` 同时使用。
- `@Bench` 可在模版中使用, 在指定 `--bench` 时下执行，就像基准被放置在继承类本身中一样。