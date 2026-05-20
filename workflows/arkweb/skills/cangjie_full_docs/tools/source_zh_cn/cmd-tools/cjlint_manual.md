# 静态检查工具

## 功能简介

`CJLint(Cangjie Lint)`是一款静态检查工具，该工具是基于仓颉语言编程规范开发。通过它可以识别代码中不符合编程规范的问题，帮助开发者发现代码中的漏洞，写出满足 Clean Source 要求的仓颉代码。

## 使用说明

`cjlint -h` 帮助信息，选项介绍。

```text
Options:
   -h                      Show usage
                               eg: ./cjlint -h
   -v                      Show version
                               eg: ./cjlint -v
   -f <value>              Detected file directory, it can be absolute paths or relative paths, if it is directory, default file name is cjReport
                               eg: ./cjlint -f fileDir -c . -m .
                               eg: ./cjlint -f "fileDir1 fileDir2" -c . -m .
   -e <v1:v2:...>          Excluded files, directories or configurations, splitted by ':'. Regular expressions are supported
                               eg: ./cjlint -f fileDir -e fileDir/a/:fileDir/b/*.cj
   -o <value>              Output file path, it can be absolute path or relative path
                               eg: ./cjlint -f fileDir -o ./out
   -r [csv|json]           Report file format, it can be csv or json, default is json
                               eg: ./cjlint -f fileDir -r csv -o ./out
   -c <value>              Directory path where the config directory is located, it can be absolute path or relative path to the executable file
                               eg: ./cjlint -f fileDir -c .
   -m <value>              Directory path where the modules directory is located, it can be absolute path or relative path to the executable file
                               eg: ./cjlint -f fileDir -m .
   --import-path <value>   Add .cjo search path
```

`cjlint -f` 指定检查目录。

```bash
cjlint -f fileDir [option] fileDir...

# 若需要指定多个路径，则在 "" 中以空格相隔
cjlint -f "fileDir1 fileDir2" [option] fileDir...
```

> **注意：**
>
> `-f` 后面指定的是*.cj 文件所在`src`目录。

正例：

```bash
cjlint -f xxx/xxx/src
```

反例：

```bash
cjlint -f xxx/xxx/src/xxx.cj
```

> **说明：**
>
> 当前工具支持目录扫描，暂不支持对单源码文件的独立检查，建议开发者提供单包路径作为输入。

`-r` 指定生成扫描报告的格式，目前支持`json`格式和`csv`格式。

`-r`需要与`-o`选项配合使用，如果没有`-o`指定输出到文件，即使指定了`-r`也不会生成扫描报告。如果指定了`-o`没有指定`-r`，那么默认生成`json`格式的扫描报告。

```bash
cjlint -f ./src -r csv -o ./report         # 生成report.csv文件
cjlint -f ./src -r csv -o ./output/report  # 在output目录下生成report.csv文件
```

`-c`, `-m` 在开发者需要时用以指定`config`和`modules`所在的目录路径。

`cjlint`默认使用其所在目录下的`config`和`modules`作为配置和依赖目录。开发者可通过命令行选项 `-c` 和 `-m` 指定其他目录路径。

例：指定的 config 和 modules 的路径分别为：`./tools/cjlint/config` 和 `./tools/cjlint/modules`。则`config`和`modules`所在的目录路径同为`./tools/cjlint`, 所以命令应为：

```bash
cjlint -f ./src -c ./tools/cjlint -m ./tools/cjlint
```

`--import-path` 在开发者需要时用以指定 `cjo` 所在的目录路径，且支持多个路径。

```bash
cjlint --import-path fileDir

# 若需要指定多个路径，则在 "" 中以空格相隔
cjlint --import-path "fileDir1 fileDir2"
```

## 规则级告警屏蔽

可执行文件`cjlint`同目录下的`config`配置目录中包含`cjlint_rule_list.json`和`exclude_lists.json`两个配置文件。`cjlint_rule_list.json`为规则列表配置文件，用于决定执行哪些规则检查。`exclude_lists.json`为告警屏蔽配置文件，用于屏蔽特定规则的告警。

例：若开发者只想检查如下 5 条规则，则`cjlint_rule_list.json`配置文件中只添加要检查的 5 条规则。

```json
{
    "RuleList": [
        "G.FMT.01",
        "G.ENU.01",
        "G.EXP.03",
        "G.OTH.01",
        "G.OTH.02"
    ]
}
```

例：若开发者想要屏蔽某一条规则的某一条告警，可以在`exclude_lists.json`配置文件中添加屏蔽信息。

> **注意：**
>
> `path`不必填写绝对路径，但必须有`xxx.cj`格式，为模糊匹配。`line`为告警行号，为精确匹配。`colum`为告警列号，可选择性填写进行列号精确匹配。

```json
{
    "G.OTH.01" : [
        {"path":"xxx/example.cj", "line":"42"},
        {"path":"xxx/example.cj", "line":"42", "colum": "2"},
        {"path":"example.cj", "line":"42", "colum": "2"}
    ]
}
```

## 源代码注释告警屏蔽

**特殊注释 BNF**

```text
<content of cjlint-ignore comment> ::=  "cjlint-ignore"  [-start] <ignore-rule>{...} [description] | cjlint-ignore  <-end> [description]
<ignore-rule> ::="!"<rule-name>
<rule-name> ::= <letters>
```

> **注意：**
>
> - 特殊注释的 `cjlint-ignore` 与选项 `-start` 和 `-end` 以及屏蔽的规则需要写在同一行上，否则无法进行告警屏蔽。描述信息可以写在不同行。
> - 单行屏蔽，屏蔽规则与屏蔽规则间需要用空格隔开，`cjlint` 会将特殊注释所在行的对应规则告警进行屏蔽。
> - 多行屏蔽，`cjlint` 会以含有 `-start` 的特殊注释为起始行，以含有 `-end` 的特殊注释为结束行，将其间对应的规则进行屏蔽。含有 `-end` 的特殊注释会与其上方最近的含有 `-start` 的特殊注释相匹配。

**单行屏蔽正确示例 1**，屏蔽 G.FUN.02 告警

<!-- compile -->

```cangjie
func foo(a: Int64, b: Int64, c: Int64, d: Int64) { /* cjlint-ignore !G.FUN.02 */
    return a + b + c
}
```

**单行屏蔽正确示例 2**，屏蔽 G.FUN.02 告警

<!-- compile -->

```cangjie
func foo(a: Int64, b: Int64, c: Int64, d: Int64) { // cjlint-ignore !G.FUN.02 description
    return a + b + c
}
```

**多行屏蔽正确示例 1**，屏蔽 G.FUN.02 告警

<!-- compile -->

```cangjie
/*cjlint-ignore -start !G.FUN.02 description */
func foo(a: Int64, b: Int64, c: Int64, d: Int64) {
    return a + b + c
}
/* cjlint-ignore -end description */
```

**多行屏蔽正确示例 2**，屏蔽 G.FUN.02 告警

<!-- compile -->

```cangjie
// cjlint-ignore -start !G.FUN.02 description
func foo(a: Int64, b: Int64, c: Int64, d: Int64) {
    return a + b + c
}
// cjlint-ignore -end description
```

**多行屏蔽正确示例 3**，屏蔽 G.FUN.02 告警

<!-- compile -->

```cangjie
/**
 *  cjlint-ignore -start !G.FUN.02 description
 */
func foo(a: Int64, b: Int64, c: Int64, d: Int64) {
    return a + b + c
}
// cjlint-ignore -end description
```

**单行屏蔽错误示例 1**，屏蔽 G.FUN.02 告警

<!-- compile -->

```cangjie
func foo(a: Int64, b: Int64, c: Int64, d: Int64) { /*cjlint-ignore !G.FUN.02!G.FUN.01*/
    return a + b + c                               // ERROR: 规则间没用空格隔开，屏蔽告警失败
}
```

**单行屏蔽错误示例 2**，屏蔽 G.FUN.02 告警

<!-- compile -->

```cangjie
func foo(a: Int64, b: Int64, c: Int64, d: Int64) { /*cjlint-ignore !G.FUN.02description*/
    return a + b + c                               // ERROR: 规则与描述信息没用空格隔开，屏蔽告警失败
}
```

**多行屏蔽错误示例 1**，屏蔽 G.FUN.02 告警

<!-- compile -->

```cangjie
/* cjlint-ignore -start
 * !G.FUN.02 description */
func foo(a: Int64, b: Int64, c: Int64, d: Int64) {
    return a + b + c
}
/* cjlint-ignore -end description */
// ERROR: 屏蔽规则没与 'cjlint-ignore' 在同一行，屏蔽告警失败
```

## 文件级告警屏蔽

1. `cjlint` 可以通过 `-e` 选项支持文件级别的告警屏蔽。

    通过在 `-e` 后添加屏蔽规则，即可将规则匹配的仓颉文件屏蔽，不会产生关于这些文件的告警。输入的规则为相对 `-f` 源码目录的相对路径（支持正则），输入字符串需要用双引号包含，多条屏蔽规则用空格分隔。例如，下面这条命令屏蔽了 `src/dir1/` 目录内的所有仓颉文件， `src/dir2/a.cj` 文件和 `src/` 目录下所有形如 `test*.cj` 的仓颉文件。

    ```bash
    cjlint -f src/ -e "dir1/ dir2/a.cj test*.cj"
    ```

2. `cjlint` 可以通过后缀为 `.cfg` 的配置文件批量导入屏蔽规则。

    通过 `-e` 选项导入配置文件，与其他屏蔽规则或配置文件用空格分隔。例如，下面这条命令屏蔽了 `src/dir1` 目录和 `src/exclude_config_1.cfg`、`src/dir2/exclude_config_2.cfg` 内配置的所有屏蔽规则对应的文件。

    ```bash
    cjlint -f src/ -e "dir1/ exclude_config_1.cfg dir2/exclude_config_2.cfg"
    ```

    `.cfg` 配置文件中可以配置多条屏蔽规则，每行均为一条屏蔽规则，屏蔽规则为相对该配置文件所在目录的相对路径（支持正则），无需双引号包含。例如在 `src/dir2/exclude_config_2.cfg` 中有以下配置，则上述的命令会将 `src/dir2/subdir1/` 目录和 `src/dir2/subdir2/a.cj` 文件加入屏蔽。

    ```text
    subdir1/
    subdir2/a.cj
    ```

3. `cjlint` 可以通过默认配置文件批量导入屏蔽规则。

    `cjlint` 屏蔽功能的默认配置文件名为 `cjlint_file_exclude.cfg`，位置在 `-f` 源码目录下。例如，当 `src/` 目录下存在 `src/cjlint_file_exclude.cfg` 这一配置文件时，`cjlint -f src/` 命令会屏蔽 `src/cjlint_file_exclude.cfg` 内配置的屏蔽规则对应的文件。如果开发者已经在 `-e` 选项中配置了其他有效的 `.cfg` 配置文件，则 `cjlint` 不会检查默认配置文件。

## 支持检查的规范列表（持续新增中）

`cjlint` 默认启用的规范列表：

- G.NAM.01 包名采用全小写单词，允许包含数字和下划线。
- G.NAM.02 源文件名采用全小写加下划线风格。
- G.NAM.03 接口，类，struct、枚举类型和枚举成员构造，类型别名，采用大驼峰命名。
- G.NAM.04 函数名称应采用小驼峰命名。
- G.NAM.05 let 的全局变量和 static let 变量的名称采用全大写。
- G.FMT.01 源文件编码格式（包括注释）必须是 UTF-8。
- G.FMT.15 禁止省略浮点数小数点前的 0。
- G.DCL.01 避免遮盖（shadow）。
- G.DCL.02 显式声明 public 变量的类型和 public 函数的返回类型。
- G.FUN.01 函数功能要单一。
- G.FUN.02 禁止函数有未被使用的参数。
- G.FUN.03 避免在无关的函数之间重用名字，构成重载。
- G.CLS.01 override 父类函数时不要增加函数的可访问性。
- G.ITF.01 对于需要原地修改对象自身的抽象函数，尽量使用 mut 修饰，以支持 struct 类型实现或扩展该接口。
- G.ITF.02 尽量在类型定义处就实现接口，而不是通过扩展实现接口。
- G.ITF.03 类型定义时避免同时声明实现父接口和子接口。
- G.ITF.04 尽量通过泛型约束使用接口，而不是直接将接口作为类型使用。
- G.OPR.01 尽量避免违反使用习惯的操作符重载。
- G.OPR.02 尽量避免在枚举类型内定义`()`操作符重载函数。
- G.ENU.01 避免枚举的构造成员与顶层元素同名。
- G.ENU.02 尽量避免不同的 enum 的 constructor 之间不必要的重载。
- G.VAR.01 优先使用不可变变量。
- G.VAR.02 保持变量的作用域尽可能小。
- G.TYP.03 判断变量是否为 NaN 时必须使用 isNaN() 方法。
- G.EXP.01 match 表达式同一层尽量避免不同类别的 pattern 混用。
- G.EXP.02 不要期望浮点运算得到精确的值。
- G.EXP.03 && 、 ||、? 和 ?? 操作符的右侧操作数不要包含副作用。
- G.EXP.04 尽量避免副作用发生依赖于操作符的求值顺序。
- G.EXP.05 用括号明确表达式的操作顺序，避免过分依赖默认优先级。
- G.EXP.06 Bool 类型比较应避免多余的 == 或 !=。
- G.EXP.07 比较两个表达式时，左侧倾向于变化，右侧倾向于不变。
- G.ERR.01 恰当地使用异常或错误处理机制。
- G.ERR.02 防止通过异常抛出的内容泄露敏感信息。
- G.ERR.03 避免对 Option 类型使用 getorthrow 函数。
- G.ERR.04 不要使用 return、break、continue 或抛出异常使 finally 块非正常结束。
- G.PKG.01 避免在 import 声明中使用通配符*。
- G.CON.01 禁止将系统内部使用的锁对象暴露给不可信代码。
- P.01 使用相同的顺序请求锁，避免死锁。
- G.CON.02 在异常可能出现的情况下，保证释放已持有的锁。
- G.CON.03 禁止使用非线程安全的函数来覆写线程安全的函数。
- P.02 避免数据竞争（data race）。
- G.CHK.01 跨信任边界传递的不可信数据使用前必须进行校验。
- G.CHK.02 禁止直接使用外部数据记录日志。
- G.CHK.03 使用外部数据构造的文件路径前必须进行校验，校验前必须对文件路径进行规范化处理。
- G.CHK.04 禁止直接使用不可信数据构造正则表达式。
- G.FIO.01 临时文件使用完毕必须及时删除。
- G.SER.01 禁止序列化未加密的敏感数据。
- G.SER.02 防止反序列化被利用来绕过构造方法中的安全操作。
- G.SER.03 保证序列化和反序列化的变量类型一致。
- G.SEC.01 进行安全检查的方法禁止声明为`open`。
- P.03 对外部对象进行安全检查时需要进行防御性拷贝。
- G.OTH.01 禁止在日志中保存口令、密钥和其他敏感数据。
- G.OTH.02 禁止将敏感信息硬编码在程序中。
- G.OTH.03 禁止代码中包含公网地址。
- G.OTH.04 不要使用 String 存储敏感数据，敏感数据使用结束后应立即清 0。
- FFI.C.7 强制进行指针类型转换时避免出现截断错误。

`cjlint` 能够检测，但默认不启用的规范列表（开发者可通过将规范添加至 `cjlint_rule_list.json` 以启用这类规则）：

- G.NAM.06 变量的名称采用小驼峰。
- G.VAR.03 避免使用全局变量。
- G.FMT.13 文件头注释应该包含版权许可。

## 规格说明

- G.CON.02 在异常可能出现的情况下，保证释放已持有的锁。

    lock() 函数和 unlock() 函数赋值给变量，赋值后的变量再去加解锁的场景，该规则检查不覆盖。

- G.OTH.03 暂不支持宏检查。
- 只有当宏包在正确的路径下时，`cjlint`才能支持宏检查。

    例：a.cj 为宏包源码，其正确路径应为 xxx/src/a/a.cj。

- `cjlint`只有在宏被调用时才能对其进行检查，且无法对宏包中的冗余代码进行检查。

## 支持语法禁用检查

1. `cjlint` 可以通过将 G.SYN.01 添加至 `cjlint_rule_list.json` 以启用禁用语法的检查。如果使用了禁用的语法元素，`cjlint` 将会报错。

2. 当前`cjlint`所支持检查的禁止使用语法如表中所示:

   | 禁用语法     | 关键词          | 说明                                             |
   | ------------ | --------------- | ------------------------------------------------ |
   | 导入包       | Import          | 不允许随意导入包                                 |
   | let 变量     | Let             | 只用 var 变量，不引入不可写变量的概念            |
   | 创建线程     | Spawn           | 不允许创建线程                                   |
   | 线程同步     | Synchronized    | 防止死锁                                         |
   | 主函数       | Main            | 禁止提供入口主函数                               |
   | 定义宏       | MacroQuote      | 禁止定义宏（但允许使用宏）                       |
   | 跨语言       | Foreign         | 禁止跨语言混合编程                               |
   | while 循环   | While           | 防止复杂循环和死循环                             |
   | 扩展         | Extend          | 禁止使用扩展语法                                 |
   | 类型别名     | Type            | 禁止自行定义类型别名                             |
   | 操作符重载   | Operator        | 禁止重载操作符                                   |
   | 全局变量     | GlobalVariable  | 禁止声明和使用全局变量，防止副作用和内存泄漏     |
   | 定义枚举     | Enum            | 禁用 Enum，避免复杂代码                          |
   | 定义类       | Class           | 禁用 Class，避免复杂代码                         |
   | 定义接口     | Interface       | 禁用 Interface，避免复杂代码                     |
   | 定义结构     | Struct          | 禁用 Struct，避免复杂代码                        |
   | 定义泛型     | Generic         | 禁用 Generic，避免复杂代码                       |
   | 条件编译     | When            | 禁止平台相关代码                                 |
   | 模式匹配     | Match           | 函数式编程范式，开发者不易掌握                   |
   | 捕获异常     | TryCatch        | 避免自行处理异常，易导致错误被忽略               |
   | 高阶函数     | HigherOrderFunc | 函数类型的参数或返回值, 避免复杂代码             |
   | 其他基础类型 | PrimitiveType   | 不应使用 Int64、float64、bool 之外的其他基础类型 |
   | 其他容器类型 | ContainerType   | 应使用 List，Map，Set                            |

3. 通过将上述表格中的关键字添加到 `structural_rule_G_SYN_01.json` 中启用对应语法的禁用检查。举例：禁用导入包

```json
{
  "SyntaxKeyword": [
    "Import"
  ]
}
```
