# 项目管理工具

## 功能简介

`CJPM（Cangjie Project Manager）` 是仓颉语言的官方项目管理工具，用于对仓颉项目模块系统进行管理与维护，涵盖模块初始化、依赖检查与更新等操作。它提供统一的编译入口，支持增量编译、并行编译等，支持自定义编译命令。

## 使用说明

执行 `cjpm -h` 命令，查阅项目管理工具的使用说明，如下所示。

```text
Cangjie Project Manager

Usage:
  cjpm [subcommand] [option]

Available subcommands:
  init             Init a new cangjie module
  check            Check the dependencies
  update           Update cjpm.lock
  tree             Display the package dependencies in the source code
  build            Compile the current module
  run              Compile and run an executable product
  test             Unittest a local package or module
  bench            Run benchmarks in a local package or module
  clean            Clean up the target directory
  install          Install a cangjie binary
  uninstall        Uninstall a cangjie binary

Available options:
  -h, --help       help for cjpm
  -v, --version    version for cjpm

Use "cjpm [subcommand] --help" for more information about a command.
```

基本的使用操作命令如下所示：

```shell
cjpm build --help
```

`cjpm` 是主程序的名称，`build` 是当前执行的可用命令，`--help` 是当前可用命令可用的配置项（配置项通常有长和短两种写法，效果相同）。

成功执行后会显示如下结果：

```text
Compile a local module and all of its dependencies.

Usage:
  cjpm build [option]

Available options:
  -h, --help                    help for build
  -i, --incremental             enable incremental compilation
  -j, --jobs <N>                the number of jobs to spawn in parallel during the build process
  -V, --verbose                 enable verbose
  -g                            enable compile debug version target
  --coverage                    enable coverage
  --cfg                         enable the customized option 'cfg'
  -m, --member <value>          specify a member module of the workspace
  --target <value>              generate code for the given target platform
  --target-dir <value>          specify target directory
  -o, --output <value>          specify product name when compiling an executable file
  -l, --lint                    enable cjlint code check
  --mock                        enable support of mocking classes in tests
  --skip-script                 disable script 'build.cj'.
```

## 命令说明

### init

`init` 用于初始化一个新的仓颉模块或者工作空间。初始化模块时，默认在当前文件夹创建配置文件 `cjpm.toml`，并新建 `src` 源码文件夹。如果该模块的产物为可执行类型，则会在 `src` 下生成默认的 `main.cj` 文件，并在编译后打印输出 `hello world`。初始化工作空间时仅会创建 `cjpm.toml` 文件，默认会扫描该路径下已有的仓颉模块并添加到 `members` 字段中。若已存在 `cjpm.toml` 文件，或源码文件夹内已存在 `main.cj`，则会跳过对应的文件创建步骤。

`init` 有多个可配置项：

- `--workspace` 新建一个工作空间配置文件，指定该选项时以上其它选项无效会自动忽略
- `--name <value>` 指定新建模块的 `root` 包名，不指定时默认为上一级子文件夹名称
- `--path <value>` 指定新建模块的路径，不指定时默认为当前文件夹
- `--type=<executable|static|dynamic>` 指定新建模块的产物类型，缺省时默认为 `executable`

例如：

```text
输入: cjpm init
输出: cjpm init success
```

```text
输入: cjpm init --name demo --path project
输出: cjpm init success
```

```text
输入: cjpm init --type=static
输出: cjpm init success
```

### check

`check` 命令用于检查项目中所需的依赖项，执行成功将会打印有效的包编译顺序。

`check` 有多个可配置项：

- `-m, --member <value>` 仅可在工作空间下使用，可用于指定单个模块作为检查入口
- `--no-tests` 配置后，测试相关的依赖将不会被打印
- `--skip-script` 配置后，将会跳过构建脚本的编译运行

例如：

```text
输入: cjpm check
输出:
The valid serial compilation order is:
    b.pkgA -> b
cjpm check success
```

```text
输入: cjpm check
输出:
Error: cyclic dependency
b.B -> c.C
c.C -> d.D
d.D -> b.B
输出说明：上述输出中，b.B 代表以 b 为 root 包的模块中的一个名为 b.B 的子包
```

```text
输入: cjpm check
输出:
Error: can not find the following dependencies
    pro1.xoo
    pro1.yoo
    pro2.zoo
```

### update

`update` 用于将 `cjpm.toml` 里的内容更新到 `cjpm.lock`。当 `cjpm.lock` 不存在时，将会生成该文件。`cjpm.lock` 文件记录着 `git` 依赖的版本号等元信息，用于下次构建使用。

`update` 有以下可配置项：

- `--skip-script` 配置后，将会跳过构建脚本的编译运行

```text
输入: cjpm update
输出: cjpm update success
```

### tree

`tree` 命令用于可视化地展示仓颉源码中的包依赖关系。

`tree` 有多个可配置项：

- `-V, --verbose` 增加包节点的详细信息，包括包名、版本号和包路径
- `--depth <N>` 指定依赖树的最大深度，可选值是非负整数。指定该选项时，默认会以所有包作为根节点。其中，N 的值代表每个依赖树的子节点最大深度
- `-p, --package <value>` 指定某个包为根节点，从而展示它的子依赖包，需要配置的值是包名
- `--invert <value>` 指定某个包为根节点并反转依赖树，从而展示它被哪些包所依赖，需要配置的值是包名
- `--target <value>` 将指定目标平台的依赖项加入分析，并展示依赖关系
- `--no-tests` 排除 `test-dependencies` 字段的依赖项
- `--skip-script` 配置后，将会跳过构建脚本的编译运行

例如，模块 `a` 的源代码目录结构如下：

```text
src
├── main.cj
├── aoo
│   └── a.cj
├── boo
│   └── b.cj
├── coo
│   └── c.cj
├── doo
│   └── d.cj
└── eoo
    └── e.cj
```

依赖关系为：包 `a` 导入包 `a.aoo`、`a.boo`，子包 `aoo` 导入包 `a.coo`，子包 `boo` 导入包 `coo`，子包 `doo` 导入包 `coo`。

```text
输入: cjpm tree
输出:
|-- a
    └── a.aoo
        └── a.coo
    └── a.boo
        └── a.coo
|-- a.doo
    └── a.coo
|-- a.eoo
cjpm tree success
```

```text
输入: cjpm tree --depth 2 -p a
输出:
|-- a
    └── a.aoo
        └── a.coo
    └── a.boo
        └── a.coo
cjpm tree success
```

```text
输入: cjpm tree --depth 0
输出:
|-- a
|-- a.eoo
|-- a.aoo
|-- a.boo
|-- a.doo
|-- a.coo
cjpm tree success
```

```text
输入: cjpm tree --invert a.coo --verbose
输出:
|-- a.coo 1.2.0 （.../src/coo）
    └── a.aoo 1.1.0 （.../src/aoo）
            └── a 1.0.0 （.../src）
    └── a.boo 1.1.0 （.../src/boo）
            └── a 1.0.0 （.../src）
    └── a.doo 1.3.0 （.../src/doo）
cjpm tree success
```

### build

`build` 用于构建当前仓颉项目，执行该命令前会先检查依赖项，检查通过后调用 `cjc` 进行构建。

`build` 有多个可配置项：

- `-i, --incremental` 用于指定增量编译，默认情况下是全量编译
- `-j, --jobs <N>` 用于指定并行编译的最大并发数，最终的最大并发数取 `N` 和 `2倍 CPU 核数` 的最小值
- `-V, --verbose` 用于展示编译日志
- `-g` 用于生成 `debug` 版本的输出产物
- `--coverage` 用于生成覆盖率信息，默认情况下不开启覆盖率功能
- `--cfg` 指定后，能够透传 `cjpm.toml` 中的自定义 `cfg` 选项，`cjpm.toml` 中的配置可参考 profile.customized-option 章节
- `-m, --member <value>` 仅可在工作空间下使用，可用于指定单个模块作为编译入口
- `--target <value>` 指定后，可交叉编译代码到目标平台，`cjpm.toml` 中的配置可参考 [target](#target) 章节
- `--target-dir <value>` 用于指定输出产物的存放路径
- `-o, --output <value>` 用于指定输出可执行文件的名称，默认名称为 `main`（`Windows` 系统下则默认为 `main.exe`）。注意，当前不支持编译名称为 `cjc` 的可执行文件
- `-l, --lint` 用于在编译时调用仓颉语言静态检查工具进行代码检查
- `--mock` 带有此选项的构建版本中的类可用于在测试中进行 `mock` 测试
- `--skip-script` 配置后，将会跳过构建脚本的编译运行

> **注意：**
>
> - `-i, --incremental` 选项仅会开启 `cjpm` 包级别的增量编译。开发者可以在配置文件的 `compile-option` 字段自行透传 `--incremental-compile` 和 `--experimental` 编译选项，从而开启 `cjc` 编译器提供的函数粒度增量功能。
> - `-i, --incremental` 选项目前仅支持基于源码的增量分析。如果导入的库内容有变更，需要开发者重新使用全量方式构建。

编译生成的中间文件默认会存放在 `target` 文件夹，而可执行文件会根据编译模式存放到 `target/release/bin` 或 `target/debug/bin` 文件夹。运行可执行文件的方式可参考 `run`。

为了提供可复制的构建，此命令会创建 `cjpm.lock` 文件，该文件包含所有可传递依赖项的确切版本，这些依赖项将用于所有后续构建，需要更新该文件时请使用 `update` 命令。如果有必要保证每个项目参与者都有可复制的构建，那么此文件应提交到版本控制系统中。

例如：

```text
输入: cjpm build -V
输出:
compile package module1.package1: cjc --import-path "target/release" --output-dir "target/release/module1" -p "src/package1" --output-type=staticlib -o libmodule1.package1.a
compile package module1: cjc --import-path "target/release" --output-dir "target/release/bin" -p "src" --output-type=exe -o main
cjpm build success
```

```text
输入: cjpm build
输出: cjpm build success
```

> **注意：**
>
> 根据仓颉包管理规格，只有符合要求的有效源码包才能被正确纳入编译范围。如果编译时出现 `no '.cj' file` 相关的告警，很可能是因为对应包不符合规范导致源码文件不被编译。如果出现这种情况，请参考[仓颉包管理规格说明](#仓颉包管理规格说明)修改代码目录结构。

在执行 `cjpm build` 之前，`cjpm` 会对当前模块或工作空间进行包依赖关系检查。若发现包之间存在相互导入关系形成依赖闭环，构建将被中止并返回错误信息，提示循环依赖路径。

例如，模块 `demo` 的源代码目录结构如下：

```text
src
├── main.cj
├── aoo
│   └── a.cj
├── boo
│   └── b.cj
└── coo
    └── c.cj
```

依赖关系为：包 `demo.aoo` 导入包 `demo.boo`，包 `demo.boo` 导入包 `demo.coo`，包 `demo.coo` 导入包 `demo.aoo`，三个包之间的依赖导入形成闭环，导致循环依赖：

```text
输入: cjpm build
输出:
cyclic dependency:
demo.boo -> demo.coo
demo.coo -> demo.aoo
demo.aoo -> demo.boo

Error: cjpm build failed
```

出现循环依赖后，开发者可以基于报错信息进行依赖关系排查。上例中，导入关系为 `demo.aoo -> demo.boo -> demo.coo -> demo.aoo`，开发者可依次从各包对应的目录下找到导入点并分析是否可以删除导入，从而解决循环依赖。例如，开发者可先从 `demo.aoo` 开始分析，在该包对应的代码目录中，查询哪些源码文件存在 `demo.boo` 包的导入，若这些文件实际上并没有功能依赖 `demo.boo`，则可以删除对应的导入。用同样的方法依次排查 `demo.boo` 和 `demo.coo`，删除冗余导入，从而尝试解决循环依赖问题。

若经过上述排查，发现确实存在功能上的循环依赖情况，可以尝试下面的几个解决方法：

- 重构导入顺序：尽量让依赖关系保持单向，避免回环，例如上例中 `demo.coo` 中依赖 `demo.aoo` 的部分可独立实现，即可拆解闭环；
- 拆分模块：将相互引用的代码拆分到独立包，例如上例中可将三个子包合成一个包。

在涉及到包依赖关系解析的其他命令中（例如 `tree`），若存在循环依赖，也会有相同的报错出现，也可以基于上述处理方式解决。

### run

`run` 用于运行当前项目构建出的二进制产物。`run` 命令会默认执行 `build` 命令的流程，以生成最终用于运行的二进制文件。

`run` 有多个可配置项：

- `--name <value>` 指定运行的二进制名称，不指定时默认为 `main`，工作空间下的二进制产物默认存放在 `target/release/bin` 路径下
- `--build-args <value>` 控制 `build` 编译流程的参数
- `--skip-build` 跳过编译流程，直接运行
- `--run-args <value>` 透传参数给本次运行的二进制产物
- `--target-dir <value>` 用于指定运行产物的存放路径
- `-g` 用于运行 `debug` 版本的产物
- `-V, --verbose` 用于展示运行日志
- `--skip-script` 配置后，将会跳过构建脚本的编译运行

例如：

```text
输入: cjpm run
输出: cjpm run success
```

```text
输入: cjpm run -g // 此时会默认执行 cjpm build -i -g 命令
输出: cjpm run success
```

```text
输入: cjpm run --build-args="-s -j16" --run-args="a b c"
输出: cjpm run success
```

### test

`test` 用于编译并运行仓颉文件的单元测试用例，运行后打印测试结果，编译产物默认存放在 `target/release/unittest_bin` 文件夹。单元测试用例代码的写法可参考《仓颉编程语言标准库 API》中 `std.unittest` 库的说明。

该命令可以指定待测试的单包路径（支持指定多个单包，形如 `cjpm test path1 path2`），不指定路径时默认执行模块级别的单元测试。执行模块级别的单元测试时，默认只进行当前模块的单元测试，直接或间接依赖的其他所有模块内的测试均不会被执行。`test` 执行前提是当前项目能够 `build` 编译成功。

模块的单元测试代码结构如下所示，其中 `xxx.cj` 存放该包的源码，`xxx_test.cj` 存放单元测试代码：

```text
└── src
│    ├── koo
│    │    ├── koo.cj
│    │    └── koo_test.cj
│    ├── zoo
│    │    ├── zoo.cj
│    │    └── zoo_test.cj
│    ├── main.cj
│    └── main_test.cj
└── cjpm.toml
```

1. 单模块测试场景

    ```text
    输入: cjpm test
    进度报告：
    group test.koo                                    100% [||||||||||||||||||||||||||||] ✓    (00:00:01)
    group test.zoo                                      0% [----------------------------]      (00:00:00)
    test TestZ.sayhi                                                                           (00:00:00)

    passed: 1, failed: 0                                  33% [|||||||||-------------------]  1/3 (00:00:01)

    输出:
    --------------------------------------------------------------------------------------------------
    TP: test, time elapsed: 177921 ns, RESULT:
        TCS: TestM, time elapsed: 177921 ns, RESULT:
        [ PASSED ] CASE: sayhi (177921 ns)
        Summary: TOTAL: 1
        PASSED: 1, SKIPPED: 0, ERROR: 0
        FAILED: 0
    --------------------------------------------------------------------------------------------------
    TP: test.koo, time elapsed: 134904 ns, RESULT:
        TCS: TestK, time elapsed: 134904 ns, RESULT:
        [ PASSED ] CASE: sayhi (134904 ns)
        Summary: TOTAL: 1
        PASSED: 1, SKIPPED: 0, ERROR: 0
        FAILED: 0
    --------------------------------------------------------------------------------------------------
    TP: test.zoo, time elapsed: 132013 ns, RESULT:
        TCS: TestZ, time elapsed: 132013 ns, RESULT:
        [ PASSED ] CASE: sayhi (132013 ns)
        Summary: TOTAL: 1
        PASSED: 1, SKIPPED: 0, ERROR: 0
        FAILED: 0
    --------------------------------------------------------------------------------------------------
    Project tests finished, time elapsed: 444838 ns, RESULT:
    TP: test.*, time elapsed: 312825 ns, RESULT:
        PASSED:
        TP: test.zoo, time elapsed: 132013 ns
        TP: test.koo, time elapsed: 312825 ns
        TP: test, time elapsed: 312825 ns
    Summary: TOTAL: 3
        PASSED: 3, SKIPPED: 0, ERROR: 0
        FAILED: 0
    --------------------------------------------------------------------------------------------------
    cjpm test success
    ```

2. 单包测试场景

    ```text
    输入: cjpm test src/koo
    输出:
    --------------------------------------------------------------------------------------------------
    TP: test.koo, time elapsed: 160133 ns, RESULT:
        TCS: TestK, time elapsed: 160133 ns, RESULT:
        [ PASSED ] CASE: sayhi (160133 ns)
        Summary: TOTAL: 1
        PASSED: 1, SKIPPED: 0, ERROR: 0
        FAILED: 0
    --------------------------------------------------------------------------------------------------
    Project tests finished, time elapsed: 160133 ns, RESULT:
    TP: test.*, time elapsed: 160133 ns, RESULT:
        PASSED:
        TP: test.koo, time elapsed: 160133 ns
    Summary: TOTAL: 1
        PASSED: 1, SKIPPED: 0, ERROR: 0
        FAILED: 0
    --------------------------------------------------------------------------------------------------
    cjpm test success
    ```

3. 多包测试场景

    ```text
    输入: cjpm test src/koo src
    输出:
    --------------------------------------------------------------------------------------------------
    TP: test.koo, time elapsed: 168204 ns, RESULT:
        TCS: TestK, time elapsed: 168204 ns, RESULT:
        [ PASSED ] CASE: sayhi (168204 ns)
        Summary: TOTAL: 1
        PASSED: 1, SKIPPED: 0, ERROR: 0
        FAILED: 0
    --------------------------------------------------------------------------------------------------
    TP: test, time elapsed: 171541 ns, RESULT:
        TCS: TestM, time elapsed: 171541 ns, RESULT:
        [ PASSED ] CASE: sayhi (171541 ns)
        Summary: TOTAL: 1
        PASSED: 1, SKIPPED: 0, ERROR: 0
        FAILED: 0
    --------------------------------------------------------------------------------------------------
    Project tests finished, time elapsed: 339745 ns, RESULT:
    TP: test.*, time elapsed: 339745 ns, RESULT:
        PASSED:
        TP: test.koo, time elapsed: 339745 ns
        TP: test, time elapsed: 339745 ns
    Summary: TOTAL: 2
        PASSED: 2, SKIPPED: 0, ERROR: 0
        FAILED: 0
    --------------------------------------------------------------------------------------------------
    cjpm test success
    ```

`test` 有多个可配置项：

- `-j, --jobs <N>` 用于指定并行编译的最大并发数，最终的最大并发数取 `N` 和 `2倍 CPU 核数` 的最小值
- `-V, --verbose` 配置项开启后，会输出单元测试的日志
- `-g` 用于生成 `debug` 版本的单元测试产物，此时的产物存放在 `target/debug/unittest_bin` 文件夹
- `-i, --incremental` 用于指定测试代码的增量编译，默认情况下是全量编译
- `--no-run` 用于仅编译单元测试产物
- `--skip-build` 用于仅运行单元测试产物
- `--coverage` 用于生成覆盖率原始数据。使用 `cjpm test --coverage` 统计覆盖率时，源代码中的 `main` 不会再作为程序入口执行，因此会显示为未被覆盖。建议使用 `cjpm test` 之后，不再手写多余的 `main`
- `--cfg` 指定后，能够透传 `cjpm.toml` 中的自定义 `cfg` 选项
- `--module <value>` 用于指定目标测试模块，指定的模块需要被当前模块直接或间接依赖（或者是该模块本身），也可以通过 `--module "module1 module2"` 的方式指定多个符合要求的模块。不指定时默认只测试当前模块
- `-m, --member <value>` 仅可在工作空间下使用，可用于指定测试单个模块
- `--target <value>` 指定后，可交叉编译生成目标平台的单元测试结果，`cjpm.toml` 中的配置可参考 [target](#target) 章节
- `--target-dir <value>` 用于指定单元测试产物的存放路径
- `--dry-run` 配置后，将不执行用例，仅打印
- `--filter <value>` 用于过滤测试的子集，`value` 的形式如下所示：
    - `--filter=*` 匹配所有测试类
    - `--filter=*.*` 匹配所有测试类的所有测试用例（结果和*相同）
    - `--filter=*.*Test,*.*case*` 匹配所有测试类中以 `Test` 结尾的用例，或者所有测试类中名字中带有 `case` 的测试用例
    - `--filter=MyTest*.*Test,*.*case*,-*.*myTest` 匹配所有 `MyTest` 开头测试类中以 `Test` 结尾的用例，或者名字中带有 `case` 的用例，或者名字中不带有 `myTest` 的测试用例
- `--include-tags <value>` 用于获取由 `@Tag` 宏指定的测试类别的子集。`value` 的形式如下：
    - `--include-tags=Unittest` 运行所有标记为 `@Tag[Unittest]` 的测试
    - `--include-tags=Unittest,Smoke` 运行所有标记为 `@Tag[Unittest]`、`@Tag[Smoke]` 任一或同时都有的测试
    - `--include-tags=Unittest+Smoke` 运行所有标记为 `@Tag[Unittest]`、`@Tag[Smoke]` 同时都有的测试
    - `--include-tags=Unittest+Smoke+JiraTask3271,Backend` 运行所有标记为 `@Tag[Backend]`、`@Tag[Unittest, Smoke, JiraTask3271]`其一的测试
- `--exclude-tags <value>` 用于排除由 `@Tag` 宏指定的测试类别的子集。`value` 的形式如下：
    - `--exclude-tags=Unittest` 运行所有未被标记为 `@Tag[Unittest]` 的测试
    - `--exclude-tags=Unittest,Smoke` 运行所有未被标记为 `@Tag[Unittest]`、`@Tag[Smoke]` 其一或同时都有的测试
    - `--exclude-tags=Unittest+Smoke+JiraTask3271` 运行所有未被标记为 `@Tag[Unittest, Smoke, JiraTask3271]` 同时都有的测试
    - `--include-tags=Unittest --exclude-tags=Smoke` 运行所有被标记为 `@Tag[Unittest]` 且不带有 `@Tag[Smoke]` 的测试
- `--no-color` 关闭控制台颜色显示
- `--random-seed <N>` 用于指定随机种子的值
- `--timeout-each <value>` value 的格式为 `%d[millis|s|m|h]`，为每个测试用例指定默认的超时时间
- `--parallel` 用于指定测试用例并行执行的方案，`value` 的形式如下所示：
    - `<BOOL>` 可为 `true` 或 `false`，指定为 `true` 时，测试类可被并行运行，并行进程个数将受运行系统上的 CPU 核数控制
    - `nCores` 指定了并行的测试进程个数应该等于可用的 CPU 核数
    - `NUMBER` 指定了并行的测试进程个数值。该数值应该为正整数
    - `NUMBERnCores` 指定了并行的测试进程个数值为可用的 CPU 核数的指定数值倍。该数值应该为正数（支持浮点数或整数）
- `--show-tags` 用于在测试报告中显示测试用例中 `@Tag` 的信息。在 `--dry-run` 模式下，并且测试报告为 `xml` 格式时，将始终包含 `Tag` 信息
- `--show-all-output` 启用测试输出打印，包括通过的测试用例
- `--no-capture-output` 禁用测试输出捕获，输出将在测试执行期间立即打印
- `--report-path <value>` 指定测试执行后的报告生成路径
- `--report-format <value>` 指定报告输出格式，当前单元测试报告仅支持 `xml` 格式（可忽略大小写），使用其它值将会抛出异常
- `--skip-script` 配置后，将会跳过构建脚本的编译运行
- `--no-progress` 禁用进度报告。如果指定选项 `--dry-run`，则隐含选项 `--no-progress`
- `--progress-brief` 显示简短（单行）进度报告而不是详细进度报告
- `--progress-entries-limit <value>` 限制进度报告中显示的条目数量。默认值：`0`。允许的值：
    - `0` 不限制条目数
    - `n` 其中 `n` 是正整数，指定终端上可以同时显示的最大条目

`cjpm test` 参数选项使用示例:

```text
输入：
cjpm test src --coverage
cjcov --root=./ --html-details -o html_output
输出：cjpm test success
覆盖率生成：在 html_output 目录下会生成 html 文件，总的覆盖率报告文件名固定为 index.html
```

```text
输入: cjpm test --filter=*
输出: cjpm test success
```

```text
输入: cjpm test src --report-path=reports --report-format=xml
输出: cjpm test success
```

> **注意：**
>
> `cjpm test` 会自动构建所有带有 `mock` 支持的包，因此在测试中，开发者可以对自定义的类或依赖源模块的类进行 `mock` 测试。为了能够从一些二进制依赖中 `mock` 类，应该通过 `cjpm build --mock` 来构建带有 `mock` 支持的类。

### bench

`bench` 用于执行测试文件的性能用例并直接打印测试结果。编译产物默认存放在 `target/release/unittest_bin` 文件夹中。性能用例由 `@Bench` 宏标注。更多关于如何编写性能用例代码的详细信息，请参见《仓颉编程语言标准库 API》中对 `std.unittest` 库的描述。

该命令可以指定待测试的单包路径（支持指定多个单包，形如 `cjpm bench path1 path2`），不指定路径时默认执行模块级别的单元测试。与 `test` 一样，执行模块级别的单元测试时，默认只进行当前模块的单元测试。`bench` 执行前提是当前项目能够 `build` 编译成功。

与 `test` 子命令类似，如果您有 `xxx.cj` 文件，则 `xxx_test.cj` 也可以包含性能测试用例。

```text
输入: cjpm bench
输出:
TP: bench, time elapsed: 8107939844 ns, RESULT:
    TCS: Test_UT, time elapsed: 8107939844 ns, RESULT:
    | Case       |   Median |         Err |   Err% |     Mean |
    |:-----------|---------:|------------:|-------:|---------:|
    | Benchmark1 | 5.438 ns | ±0.00439 ns |  ±0.1% | 5.420 ns |
Summary: TOTAL: 1
    PASSED: 1, SKIPPED: 0, ERROR: 0
    FAILED: 0
--------------------------------------------------------------------------------------------------
Project tests finished, time elapsed: 8107939844 ns, RESULT:
TP: bench.*, time elapsed: 8107939844 ns, RESULT:
    PASSED:
    TP: bench, time elapsed: 8107939844 ns, RESULT:
Summary: TOTAL: 1
    PASSED: 1, SKIPPED: 0, ERROR: 0
    FAILED: 0
```

`bench` 有多个可配置项：

- `-j, --jobs <N>` 用来指定并行编译的最大并发数，最终的最大并发数取 `N` 和 `2倍 CPU 核数` 的最小值
- `-V, --verbose` 配置项开启后，会输出单元测试的日志
- `-g` 用来生成 `debug` 版本的单元测试产物，此时的产物存放在 `target/debug/unittest_bin` 文件夹
- `-i, --incremental` 用于指定测试代码的增量编译，默认情况下是全量编译
- `--no-run` 用来仅编译单元测试产物
- `--skip-build` 用来仅执行单元测试产物
- `--cfg` 指定后，能够透传 `cjpm.toml` 中的自定义 `cfg` 选项
- `--module <value>` 用于指定目标测试模块，指定的模块需要被当前模块直接或间接依赖（或者是该模块本身），也可以通过 `--module "module1 module2"` 的方式指定多个符合要求的模块。不指定时默认只测试当前模块
- `-m, --member <value>` 仅可在工作空间下使用，可用来指定测试单个模块
- `--target <value>` 指定后，可交叉编译生成目标平台的单元测试结果，`cjpm.toml` 中的配置可参考 `cross-compile-configuration` 部分
- `--target-dir <value>` 用来指定单元测试产物的存放路径
- `--dry-run` 配置后，将不执行用例，仅打印
- `--filter <value>` 用于过滤测试的子集，`value` 的形式如下所示：
    - `--filter=*` 匹配所有测试类
    - `--filter=*.*` 匹配所有测试类所有测试用例（结果和*相同）
    - `--filter=*.*Test,*.*case*` 匹配所有测试类中以 `Test` 结尾的用例，或者所有测试类中名字中带有 `case` 的测试用例
    - `--filter=MyTest*.*Test,*.*case*,-*.*myTest` 匹配所有 `MyTest` 开头测试类中以 `Test` 结尾的用例，或者名字中带有 `case` 的用例，或者名字中不带有 `myTest` 的测试用例
- `--include-tags <value>` 用于获取由 `@Tag` 宏指定的测试类别的子集。`value` 的形式如下：
    - `--include-tags=Unittest` 运行所有标记为 `@Tag[Unittest]` 的测试
    - `--include-tags=Unittest,Smoke` 运行所有标记为 `@Tag[Unittest]`、`@Tag[Smoke]` 任一或同时都有的测试
    - `--include-tags=Unittest+Smoke` 运行所有标记为 `@Tag[Unittest, Smoke]` 同时都有的测试
    - `--include-tags=Unittest+Smoke+JiraTask3271,Backend` 运行所有标记为 `@Tag[Backend]`、`@Tag[Unittest, Smoke, JiraTask3271]`其一的测试
- `--exclude-tags <value>` 用于排除由 `@Tag` 宏指定的测试类别的子集。`value` 的形式如下：
    - `--exclude-tags=Unittest` 运行所有未被标记为 `@Tag[Unittest]` 的测试
    - `--exclude-tags=Unittest,Smoke` 运行所有未被标记为 `@Tag[Unittest]`、`@Tag[Smoke]` 其一或同时都有的测试
    - `--exclude-tags=Unittest+Smoke+JiraTask3271` 运行所有未被标记为 `@Tag[Unittest, Smoke, JiraTask3271]` 同时都有的测试
    - `--include-tags=Unittest --exclude-tags=Smoke` 运行所有被标记为 `@Tag[Unittest]` 且不带有 `@Tag[Smoke]` 的测试
- `--no-color` 关闭控制台颜色显示
- `--show-tags` 用于在测试报告中显示测试用例中 `@Tag` 的信息。在 `--dry-run` 模式下，并且测试报告为 `xml` 格式时，将始终包含 `Tag` 信息
- `--random-seed <N>` 用来指定随机种子的值
- `--report-path <value>` 指定执行后生成报告的路径。与 `test` 子命令不同，它具有默认值 `bench_report`
- `--report-format <value>` 性能测试报告仅支持 `csv` 和 `csv-raw` 格式
- `--baseline-path <value>` 与当前性能结果进行比较的现有报告的路径。默认情况下它使用 `--report-path` 值
- `--skip-script` 配置后，将会跳过构建脚本的编译运行

`cjpm bench` 参数选项使用示例:

```text
输入: cjpm bench
输出: cjpm bench success

输入: cjpm bench src
输出: cjpm bench success

输入: cjpm bench src --filter=*
输出: cjpm bench success

输入: cjpm bench src --report-format=csv
输出: cjpm bench success
```

> **注意：**
>
> 带有 `cjpm bench` 并不包含完全的 `mock` 支持，以避免在基准测试中由于在编译器中的 `mock` 处理而增加的任何开销。
> 使用 `cjpm bench` 选项时，如果使用 `mock`，编译器不会报错，以便能够将常规测试和基准测试一起编译。但是要避免运行使用 `mock` 的基准测试，否则会抛出运行时异常。

### clean

`clean` 用于清理构建过程中的临时产物（`target` 文件夹）。该命令支持短选项 `-g` 指定仅清理 `debug` 版本的产物，以及长选项 `--target-dir <value>` 用于指定清理的产物存放路径（开发者需自行保证清理该目录行为的安全性）。如果使用了 `cjpm build --coverage` 或 `cjpm test --coverage` 功能，还会清除 `cov_output` 文件夹以及当前目录下的 `*.gcno` 和 `*.gcda` 文件。同时，该命令也支持 `--skip-script` 配置来跳过构建脚本的编译运行。

例如：

```text
输入: cjpm clean
输出: cjpm clean success
```

```text
输入: cjpm clean --target-dir temp
输出: cjpm clean success
```

> **注意：**
>
> 在 `Windows` 平台上，在子进程执行完成后立即清理子进程的可执行文件或父目录可能会失败。如果遇到该问题，可以在一小段延迟后重新尝试 `clean` 命令。

### install

`install` 用于安装仓颉项目，执行该命令前会先进行编译，然后将编译产物安装到指定路径，安装产物以仓颉项目名命名（`Windows` 系统上会有 `.exe` 后缀）。`install` 安装的项目产物类型需要是 `executable`。

`install` 有多个可配置项：

- `-V, --verbose` 用于展示安装日志。
- `-m, --member <value>` 仅可在工作空间下使用，可用于指定单个模块作为编译入口以安装单一模块。
- `-g` 用于生成 `debug` 版本的安装产物。
- `--path <value>` 用于指定本地安装项目的路径，默认为当前路径下的项目。
- `--root <value>` 用于指定可执行文件的安装路径。不配置时 `Linux` / `macOS` 系统下默认为 `$HOME/.cjpm`，`Windows` 系统下默认为 `%USERPROFILE%/.cjpm`；配置时将会安装于 `value`。
- `--git <value>` 用于指定 `git` 安装的项目 `url`。
- `--branch <value>` 用于指定 `git` 安装的项目分支。
- `--tag <value>` 用于指定 `git` 安装的项目 `tag`。
- `--commit <value>` 用于指定 `git` 安装的项目 `commit ID`。
- `-j, --jobs <N>` 用于指定并行编译的最大并发数，最终的最大并发数取 `N` 和 `2倍 CPU 核数` 的最小值。
- `--cfg` 指定后，能够透传 `cjpm.toml` 中的自定义 `cfg` 选项。
- `--target-dir <value>` 用于指定编译产物的存放路径。
- `--name <value>` 用于指定最终安装的产物名。
- `--skip-build` 用于跳过编译阶段以直接安装产物，需要项目处于编译完成状态，且仅在本地安装场景下生效。
- `--list` 用于打印已安装产物列表。
- `--skip-script` 配置后，将会跳过待安装模块的构建脚本的编译运行。

`install` 功能有如下注意事项：

- `install` 共有两种安装方式：安装本地项目（通过 `--path` 配置项目路径）和安装 `git` 项目（通过 `--git` 配置项目 `url`）。这两种安装方式至多只能配置一种，否则 `install` 将报错。任意一种均未配置时，默认安装当前目录下的本地项目。
- `install` 编译项目时，默认开启增量编译。
- `git` 相关配置仅在配置 `--git` 后生效，否则会被忽略，包括 `--branch`, `--tag` 和 `--commit`。当配置多个 `git` 相关配置时，仅会生效优先级更高的配置，优先级排序为 `--commit` > `--branch` > `--tag`。
- 若已存在同名可执行文件被安装，则原来的文件将被替换。
- 假设安装路径为 `root`（`root` 为配置的安装路径，不配置则为默认路径），则可执行文件将被安装于 `root/bin`。
- 若项目存在动态库依赖，可执行程序所需动态库会被安装到 `root/libs`，按程序名分隔为若干目录，开发者需要将对应目录加入相应路径（`Linux` 中为 `LD_LIBRARY_PATH`，`Windows` 中为 `PATH`，`macOS` 中为 `DYLD_LIBRARY_PATH`）方可使用。
- 默认安装路径（`Linux` / `macOS` 系统下默认为 `$HOME/.cjpm`，`Windows` 系统下默认为 `%USERPROFILE%/.cjpm`）会在 `envsetup` 中被加入 `PATH`。
- `install` 在安装 `git` 项目后，对应的编译产物目录会被清除。
- 在待安装项目仅存在一个可执行文件产物时，指定 `--name` 会将其更名后安装；若存在多个可执行文件产物，指定 `--name` 会仅安装对应名称的产物。
- 配置 `--list` 时，`install` 会打印已安装产物列表，此时除 `--root` 以外的所有配置项均会被忽略。配置 `--root` 后，`--list` 会打印配置路径下已安装的产物列表，否则会打印默认路径下的列表。

例如：

```text
cjpm install --path path/to/project # 从本地路径 path/to/project 中安装
cjpm install --git url              # 从 git 对应地址安装
```

### uninstall

`uninstall` 用于卸载仓颉项目，清除对应的可执行文件和依赖文件。

`uninstall` 需要配置参数 `name`，以卸载名为 `name` 的产物，配置多个 `name` 时会依次删除。`uninstall` 可以通过 `--root <value>` 指定卸载的可执行文件路径，不配置时 `Linux` / `macOS` 系统下默认为 `$HOME/.cjpm`，`Windows` 系统下默认为 `%USERPROFILE%/.cjpm`，配置时将会卸载安装于 `value/bin` 的产物和安装于 `value/libs` 的依赖。

> **注意：**
>
> `cjpm` 在 `Windows` 平台暂不支持在中文路径下使用，如果遇到问题，请通过修改目录名规避。

## 模块配置文件说明

模块配置文件 `cjpm.toml` 用于配置一些基础信息、依赖项、编译选项等内容，`cjpm` 主要通过这个文件进行解析执行。其中，模块名可以在 `cjpm.toml` 中进行重命名，但是包名不能在 `cjpm.toml` 中进行重命名。

配置文件代码如下所示：

```toml
[package] # 单模块配置字段，与 workspace 字段不能同时存在
  cjc-version = "1.0.0" # 所需 `cjc` 的最低版本要求，必需
  name = "demo" # 模块名及模块 root 包名，必需
  description = "nothing here" # 描述信息，非必需
  version = "1.0.0" # 模块版本信息，必需
  compile-option = "" # 额外编译命令选项，非必需
  override-compile-option = "" # 额外全局编译命令选项，非必需
  link-option = "" # 链接器透传选项，可透传安全编译命令，非必需
  output-type = "executable" # 编译输出产物类型，必需
  src-dir = "" # 指定源码存放路径，非必需
  target-dir = "" # 指定产物存放路径，非必需
  package-configuration = {} # 单包配置选项，非必需

[workspace] # 工作空间管理字段，与 package 字段不能同时存在
  members = [] # 工作空间成员模块列表，必需
  build-members = [] # 工作空间编译模块列表，需要是成员模块列表的子集，非必需
  test-members = [] # 工作空间测试模块列表，需要是编译模块列表的子集，非必需
  compile-option = "" # 应用于所有工作空间成员模块的额外编译命令选项，非必需
  override-compile-option = "" # 应用于所有工作空间成员模块的额外全局编译命令选项，非必需
  link-option = "" # 应用于所有工作空间成员模块的链接器透传选项，非必需
  target-dir = "" # 指定产物存放路径，非必需

[dependencies] # 源码依赖配置项，非必需
  coo = { git = "xxx"，branch = "dev" } # 导入 `git` 依赖
  doo = { path = "./pro1" } # 导入源码依赖

[test-dependencies] # 测试阶段的依赖配置项，格式和 dependencies 相同，非必需

[script-dependencies] # 构建脚本的依赖配置项，格式和 dependencies 相同，非必需

[replace] # 依赖替换配置项，格式和 dependencies 相同，非必需

[ffi.c] # 导入 C 语言的库依赖，非必需
  clib1.path = "xxx"

[profile] # 命令剖面配置项，非必需
  build = {} # build 命令配置项
  test = {} # test 命令配置项
  bench = {} # bench 命令配置项
  customized-option = {} # 自定义透传选项

[target.x86_64-unknown-linux-gnu] # 后端和平台隔离配置项，非必需
  compile-option = "value1" # 额外编译命令选项，适用于特定 target 的编译流程和指定该 target 作为交叉编译目标平台的编译流程，非必需
  override-compile-option = "value2" # 额外全局编译命令选项，适用于特定 target 的编译流程和指定该 target 作为交叉编译目标平台的编译流程，非必需
  link-option = "value3" # 链接器透传选项，适用于特定 target 的编译流程和指定该 target 作为交叉编译目标平台的编译流程，非必需

[target.x86_64-w64-mingw32.dependencies] # 适用于对应 target 的源码依赖配置项，非必需

[target.x86_64-w64-mingw32.test-dependencies] # 适用于对应 target 的测试阶段依赖配置项，非必需

[target.x86_64-unknown-linux-gnu.bin-dependencies] # 仓颉二进制库依赖，适用于特定 target 的编译流程和指定该 target 作为交叉编译目标平台的编译流程，非必需
  path-option = ["./test/pro0", "./test/pro1"] # 以文件目录形式配置二进制库依赖
[target.x86_64-unknown-linux-gnu.bin-dependencies.package-option] # 以单文件形式配置二进制库依赖
  "pro0.xoo" = "./test/pro0/pro0.xoo.cjo"
  "pro0.yoo" = "./test/pro0/pro0.yoo.cjo"
  "pro1.zoo" = "./test/pro1/pro1.zoo.cjo"
```

当以上字段在 `cjpm.toml` 中没有使用时，默认为空（对于路径，默认为配置文件所在的路径）。

### "cjc-version"

仓颉编译器最低版本要求，必须和当前环境版本兼容才可以执行。一个合法的仓颉版本号是由三段数字组成，中间使用 `.` 隔开，每个数字均为自然数，且没有多余的前缀 `0`。例如：

- `1.0.0` 是一个有效的版本号；
- `1.00.0` 不是一个有效的版本号，因为 `00` 中含有多余的前缀 `0`；
- `1.2e.0` 不是一个有效的版本号，因为 `2e` 不是自然数。

### "name"

当前仓颉模块名称，同时也是模块 `root` 包名。

一个合法的仓颉模块名称必须是一个合法的标识符。标识符可由字母、数字、下划线组成，标识符的开头必须是字母，例如 `cjDemo` 或者 `cj_demo_1`。

> **注意：**
>
> 当前仓颉模块名暂不支持使用 Unicode 字符，仓颉模块名必须是一个仅含 ASCII 字符的合法的标识符。

### "description"

当前仓颉模块描述信息，仅作说明用，不限制格式。

### "version"

当前仓颉模块版本号，由模块所有者管理，主要供模块校验使用。模块版本号的格式同 `cjc-version`。

### "compile-option"

传给 `cjc` 的额外编译选项。多模块编译时，每个模块设置的 `compile-option` 对该模块内的所有包生效。

例如：

```text
compile-option = "-O1 -V"
```

这里填入的命令会在 `build` 执行时插入到编译命令中间，多个命令可以用空格隔开。可用的命令参考《仓颉编程语言开发指南》的[编译选项](../../../dev-guide/source_zh_cn/Appendix/compile_options.md)章节内容。

### "override-compile-option"

传给 `cjc` 的额外全局编译选项。多模块编译时，编译入口模块设置的 `override-compile-option` 对该模块及依赖的所有其他模块的包生效。

例如：

```text
override-compile-option = "-O1 -V"
```

这里填入的命令会在 `build` 执行时插入到编译命令中间，并且拼接于模块配置的 `compile-option` 内容之后，优先级高于 `compile-option`。可用的命令参考《仓颉编程语言开发指南》的[编译选项](../../../dev-guide/source_zh_cn/Appendix/compile_options.md)章节内容。

> **注意：**
>
> - `override-compile-option` 会生效于依赖模块内的包，开发者需保证配置的 `cjc` 编译选项与依赖模块内配置的 `compile-option` 没有冲突，否则编译过程中执行 `cjc` 将出现相应报错。对于不冲突的同类 `cjc` 编译选项，`override-compile-option` 内的选项优先级高于 `compile-option`。
> - 在工作空间编译场景下，仅 `workspace` 内配置的 `override-compile-option` 选项会应用于工作空间内所有模块所有包的编译；即使使用 `-m` 指定以单模块为入口模块进行编译，也不会使用入口模块的 `override-compile-option`。

### "link-option"

传给链接器的编译选项，可用于透传安全编译命令，如下所示:

```text
link-option = "-z noexecstack -z relro -z now --strip-all"
```

> **注意：**
>
> `link-option` 中配置的命令在编译时只会自动透传给动态库和可执行产物对应的包。

### "output-type"

编译输出产物的类型，包含可执行程序和库两种形式，相关的输入如下表格所示。如果想生成 `cjpm.toml` 时该字段自动填充为 `static`，可使用命令 `cjpm init --type=static --name=modName`，不指定类型时默认生成为 `executable`。只有主模块的该字段可以为 `executable`。

|     输入     |                 说明 |
| :----------: | :------------------: |
| "executable" |           可执行程序 |
|   "static"   | 静态库 |
|  "dynamic"   | 动态库 |
|     其它     |                 报错 |

### "src-dir"

该字段可以指定源码的存放路径，不指定时默认为 `src` 文件夹。

### "target-dir"

该字段可以指定编译产物的存放路径，不指定时默认为 `target` 文件夹。若该字段不为空，执行 `cjpm clean` 时会删除该字段所指向的文件夹，开发者需自身保证清理该目录行为的安全性。

> **注意：**
>
> 若在编译时同时指定了 `--target-dir` 选项，则该选项的优先级会更高。

```text
target-dir = "temp"
```

### "package-configuration"

每个模块的单包可配置项。该选项是个 `map` 结构，需要配置的包名作为 `key`，单包配置信息作为 `value`。当前可配置的信息包含：

- `output-type`：包编译产物类型，取值同 [`output-type`](#output-type)
- `compile-option`：仅用于该包的额外编译选项
- `combine-all-deps`：工程级编译产物合并开关，取值为 `true/false`，仅可配置于 `root` 包

上述选项均可按需配置。

如下所示，`demo` 模块中的 `demo.aoo` 包的输出类型会被指定为动态库类型，`-g` 命令会在编译时透传给 `demo.aoo` 包。

```text
[package.package-configuration."demo.aoo"]
  output-type = "dynamic"
  compile-option = "-g"
```

如果在不同字段配置了相互兼容的编译选项，生成命令的优先级如下所示。

```text
[package]
  compile-option = "-O1"
[package.package-configuration.demo]
  compile-option = "-O2"

# profile字段会在下文介绍
[profile.customized-option]
  cfg1 = "-O0"

输入: cjpm build --cfg1 -V
输出: cjc --import-path build -O0 -O1 -O2 ...
```

通过配置这个字段，可以同时生成多个二进制产物（生成多个二进制产物时，`-o, --output <value>` 选项将会失效），示例如下：

源码结构的示例，模块名为 `demo`：

```text
src
├── aoo
│    └── aoo.cj
├── boo
│    └── boo.cj
├── coo
│    └── coo.cj
└──  main.cj
```

配置方式的示例：

```text
[package.package-configuration."demo.aoo"]
  output-type = "executable"
[package.package-configuration."demo.boo"]
  output-type = "executable"
```

多个二进制产物的示例：

```text
输入：cjpm build
输出：cjpm build success

输入：tree target/release/bin
输出：target/release/bin
|-- demo.aoo
|-- demo.boo
`-- demo
```

`combine-all-deps = true` 配置后，可以开启工程级别的编译产物合并。该配置仅在以下条件下生效：

- 开启模块级动态库合并 `profile.build.combined` 和 `LTO` 编译优化 `profile.build.lto` （参考 `profile.build` 字段）；
- 配置的模块为当前执行的 `cjpm build` 命令对应的模块，并且配置的包为该模块的 `root` 包。配置在当前模块的非 `root` 包中，或配置在被依赖的模块中的该字段将被忽略。

在满足上述配置条件后，该模块会按照如下方式编译：

- 除该模块 `root` 包以外的所有包（该模块下的所有子包，以及该模块直接、间接依赖的其他模块的包含 `root` 包的所有包），会以 `LTO` 优化编译模式编译成 `.bc` 文件；
- 该模块的 `root` 包会被编译成动态库，并且链入上述所有 `.bc` 文件，无论对应的包是否被该 `root` 包导入。

### "workspace"

该字段可管理多个模块作为一个工作空间，支持以下配置项：

- `members = ["aoo", "path/to/boo"]`：列举包含在此工作空间的本地源码模块，支持绝对路径和相对路径。该字段的成员必须是一个模块，不允许是另一个工作空间
- `build-members = []`：本次编译的模块，不指定时默认编译该工作空间内的所有模块。该字段的成员必须被包含在 `members` 字段中
- `test-members = []`：本次测试的模块，不指定时默认单元测试该工作空间内的所有模块。该字段的成员必须被包含在 `build-members` 字段中
- `compile-option = ""`：工作空间的公共编译选项，非必需
- `override-compile-option = ""`：工作空间的公共全局编译选项，非必需
- `link-option = ""`：工作空间的公共链接选项，非必需
- `target-dir = ""`：工作空间的产物存放路径，非必需，默认为 `target`

工作空间内的公共配置项，对所有成员模块生效。例如：配置了 `[dependencies] xoo = { path = "path_xoo" }` 的源码依赖，则所有成员模块可以直接使用 `xoo` 模块，无需在每个子模块的 `cjpm.toml` 中再配置。

> **注意：**
>
> `package` 字段用于配置模块的通用信息，不允许和 `workspace` 字段出现在同一个 `cjpm.toml` 中，除 `package` 外的其它字段均可在工作空间中使用。

工作空间目录举例：

```text
root_path
├── aoo
│    ├── src
│    └── cjpm.toml
├── boo
│    ├── src
│    └── cjpm.toml
├── coo
│    ├── src
│    └── cjpm.toml
└── cjpm.toml
```

工作空间的配置文件使用举例：

```text
[workspace]
members = ["aoo", "boo", "coo"]
build-members = ["aoo", "boo"]
test-members = ["aoo"]
compile-option = "-Woff all"
override-compile-option = "-O2"

[dependencies]
xoo = { path = "path_xoo" }

[ffi.c]
abc = { path = "libs" }
```

### "dependencies"

该字段通过源码方式导入依赖的其它仓颉模块，里面配置了当前构建所需要的其它模块的信息。目前，该字段支持本地路径依赖和远程 `git` 依赖。

要指定本地依赖项，请使用 `path` 字段，并且它必须包含有效的本地路径。例如，下面的两个子模块 `pro0` 和 `pro1` 和主模块的代码结构如下：

```text
├── pro0
│    ├── cjpm.toml
│    └── src
│         └── zoo
│              └── zoo.cj
├── pro1
│    ├── cjpm.toml
│    └── src
│         ├── xoo
│         │    └── xoo.cj
│         └── yoo
│              └── yoo.cj
├── cjpm.toml
└── src
     ├── aoo
     │    └── aoo.cj
     ├── boo
     │    └── boo.cj
     └── main.cj
```

在主模块的 `cjpm.toml` 中进行如下配置后，即可在源码中使用 `pro0` 和 `pro1` 模块：

```text
[dependencies]
  pro0 = { path = "./pro0" }
  pro1 = { path = "./pro1" }
```

要指定远程 `git` 依赖项，请使用 `git` 字段，并且它必须包含 `git` 支持的任何格式的有效 `url`。要配置 `git` 依赖关系，最多可以有一个 `branch`、`tag` 和 `commitId` 字段，这些字段允许分别选择特定的分支、标记或提交哈希，若配置多个此类字段则仅会生效优先级最高的配置，优先级顺序为 `commitId` > `branch` > `tag`。例如，进行如下配置后，即可在源码中使用特定 `git` 仓库地址的 `pro0` 和 `pro1` 模块：

```text
[dependencies]
  pro0 = { git = "https://github.com/example", tag = "v1.0.0"}
  pro1 = { git = "https://gitee.com/example", branch = "dev"}
```

在这种情况下，`cjpm` 将下载对应存储库的最新版本，并将当前 `commit-hash` 保存在 `cjpm.lock` 文件中。所有后续的 `cjpm` 调用都将使用保存的版本，直到使用 `cjpm update`。

通常需要一些身份验证才能访问 `git` 存储库。`cjpm` 不要求提供所需的凭据，因此应使用现有的 `git` 身份验证支持。如果用于 `git` 的协议是 `https`，则需要使用一些现有的 git 凭据帮助程序。在 `Windows` 上，可在安装 `git` 时一起安装凭据帮助程序，默认使用。在 `Linux/macOS` 上，请参见 `git` 官方文档中 `git-config` 的配置说明，了解有关设置凭据帮助程序的详细信息。如果协议是 `ssh` 或 `git`，则应使用基于密钥的身份验证。如果密钥受密码短语保护，则开发者应确保 `ssh-agent` 正在运行，并且在使用 `cjpm` 之前通过 `ssh-add` 添加密钥。

`dependencies` 字段可以通过 `output-type` 属性指定编译产物类型，指定的类型可以与源码依赖自身的编译产物类型不一致，且仅能为 `static` 或者 `dynamic`，如下所示：

```text
[dependencies]
  pro0 = { path = "./pro0", output-type = "static" }
  pro1 = { git = "https://gitee.com/example", output-type = "dynamic" }
```

进行如上配置后，将会忽略 `pro0` 和 `pro1` 的 `cjpm.toml` 中的 `output-type` 配置，将这两个模块的产物分别编译成 `static` 和 `dynamic` 类型。

### "test-dependencies"

具有与 `dependencies` 字段相同的格式。它用于指定仅在测试过程中使用的依赖项，而不是构建主项目所需的依赖项。模块开发者应将此字段用于此模块的下游用户不需要感知的依赖项。

`test-dependencies` 内的依赖仅可用于文件名形如 `xxx_test.cj` 的测试文件，在编译时这些依赖将不会被编译。`test-dependencies` 在 `cjpm.toml` 中的配置格式与 `dependencies` 相同。

### "script-dependencies"

具有与 `dependencies` 字段相同的格式。它用于指定仅在编译构建脚本中使用的依赖项，而不是构建主项目所需的依赖项。构建脚本相关功能将在[其他-构建脚本](#构建脚本)章节中详述。

### "replace"

具有与 `dependencies` 字段相同的格式。它用于指定间接依赖的同名替换项，配置的依赖项会作为编译该模块时最终使用的依赖版本。

例如，如下模块 `aaa` 依赖了一个本地模块 `bbb`：

```text
[package]
  name = "aaa"

[dependencies]
  bbb = { path = "path/to/bbb" }
```

主模块 `demo` 依赖 `aaa` 的情况下，`bbb` 即成为 `demo` 的间接依赖模块。在这种情况下，主模块 `demo` 若想替换 `bbb` 为另一个同名模块，例如在另一个路径 `new/path/to/bbb` 下的 `bbb` 模块，则可以进行如下配置：

```text
[package]
  name = "demo"

[dependencies]
  aaa = { path = "path/to/aaa" }

[replace]
  bbb = { path = "new/path/to/bbb" }
```

配置后，编译 `demo` 模块时，实际使用的间接依赖 `bbb` 为 `new/path/to/bbb` 下的 `bbb` 模块。`aaa` 中配置的 `path/to/bbb` 下的 `bbb` 模块不会被编译。

> **注意：**
>
> 仅入口模块的 `replace` 字段会在编译时生效。

### "ffi.c"

当前仓颉模块外部依赖 `c` 库的配置。该字段配置了依赖该库所需要的信息，包含库名和路径。

开发者需要自行编出动态库或静态库放到设置的 `path` 下，可参考下面的例子。

仓颉调用外部 `c` 动态库的方法说明：

- 自行将相应的 `hello.c` 文件编成 `.so`库（在该文件路径执行 `clang -shared -fPIC hello.c -o libhello.so`）
- 修改该项目的 `cjpm.toml` 文件，配置 `ffi.c` 字段，如下面的例子所示。其中，`./src/` 是编出的 `libhello.so` 相对当前目录的地址，`hello` 为库名。
- 执行 `cjpm build`，即可编译成功。

```text
[ffi.c]
hello = { path = "./src/" }
```

### "profile"

`profile` 作为一种命令剖面配置项，用于控制某个命令执行时的默认配置项。目前支持如下场景：`build`、`test`、`bench`、`run` 和 `customized-option`。

#### "profile.build"

```text
[profile.build]
lto = "full"  # 是否开启 `LTO` （Link Time Optimization 链接时优化）优化编译模式，仅 `Linux` 平台支持该功能
performance_analysis = true # 开启编译性能分析功能
incremental = true # 是否默认开启增量编译
[profile.build.combined]
demo = "dynamic" # 将模块整体编译成一个动态库文件，key 值为模块名
```

编译流程的控制项，所有字段均可缺省，不配置时不生效，顶层模块设置的 `profile.build` 项才会生效。

`lto` 配置项的取值为 `full` 或 `thin`，对应 `LTO` 优化支持的两种编译模式：`full LTO` 将所有编译模块合并到一起，在全局上进行优化，这种方式可以获得最大的优化潜力，同时也需要更长的编译时间；`thin LTO` 在多模块上使用并行优化，同时默认支持链接时增量编译，编译时间比 `full LTO` 短，但是因为失去了更多的全局信息，所以优化效果不如 `full LTO`。

`performance_analysis` 配置项的取值为 `true` 或 `false`，代表是否开启编译性能分析功能。当开启此功能时，`cjpm` 会在编译产物目录下的 `performance_analysis` 目录中生成 `.prof` 和 `.json` 文件，这些文件记录了编译过程中的时间和内存消耗。例如，编译产物目录默认为 `target` 目录，且编译模式为 `debug`，则产物目录结构如下：

```text
demo
├── cjpm.toml
├── src
|   └── demo.cj
└── target
    └── debug
        └── performance_analysis
            ├── xxx1.prof
            ├── ...
            ├── xxxN.prof
            ├── xxx1.json
            ├── ...
            └── xxxN.json
```

`combined` 配置项是一个键值对，其中键为模块名，即 `package.name`，值为 `dynamic`。配置该配置项之前，该模块会根据 `package.output-type` 配置将各个包编译成独立的动态库或静态库文件；配置后，该模块的编译方式改为：

- 模块内除 `root` 包以外的子包以静态库形式编译；
- `root` 包以动态库形式编译，并且链接所有子包的静态库，无论子包是否被 `root` 包依赖。其他模块以二进制依赖形式依赖该动态库时，可以使用所有子包内的符号。

例如，假设模块 `demo` 的结构如下：

```text
demo
├── cjpm.toml
└── src
     ├── aoo
     |    └── aoo.cj
     ├── boo
     |    └── boo.cj
     └── demo.cj
```

模块配置文件 `cjpm.toml` 内配置如下：

```text
[package]
name = "demo"

[profile.build.combined]
demo = "dynamic"
```

在编译之后，最终的编译产物目录 `target/release/demo` 中的产物列表如下（以 `Linux` 为例）：

```text
|-- libdemo.so
|-- libdemo.aoo.a
|-- libdemo.boo.a
|-- demo.cjo
|-- demo.aoo.cjo
|-- demo.boo.cjo
```

模块开发者可以将上述产物列表中的所有 `cjo` 文件和 `root` 包动态库 `libdemo.so` 提供给其他模块作为二进制依赖，无需提供子包的静态库文件。其他模块依赖该动态库之后，可以在代码中依赖其所有子包，例如可以通过 `import demo.aoo` 的方式依赖 `demo.aoo` 包。

> **注意：**
>
> - 在应用此配置时，编译 `root` 包动态库需要使用其所有子包的静态库，因此需要保证 `root` 包不被其子包直接或间接导入。
> - 目前 `profile.build.combined` 配置项为实验特性，暂不稳定，开发者若想启用该配置，需要注意如下限制：
>     - 如果配置了该字段的模块直接或间接依赖了其他源码模块，那么这些依赖模块也需要配置该字段；
>     - 构建脚本依赖的源码模块中，若配置了 `profile.build.combined`，不会生效；
>     - `profile.build.combined` 选项仅支持 `Linux/OpenHarmonyOS/Windows` 平台。

若启用了 `combined` 配置，可能会出现无法通过导入关系识别的循环依赖，导致出现 `cyclic dependency` 循环依赖报错，解决方式如下：

- 若报错信息中包含形如 `because of combined module 'demo'` 的报错，说明模块 `demo` 被配置成了 `combined` 模块，并且存在 `demo` 的子包直接或间接依赖 `demo` 包的情况，开发者可以查找并删去该模块子包中存在的对 `root` 包的导入，或者直接去除 `combined` 配置，从而解决此类循环依赖；
- 若报错信息中包含形如 `between combined modules` 的报错，说明该条目中两个 `root` 包对应模块都被配置成了 `combined` 模块，且存在模块间（包括子包之间）的相互依赖，开发者可以查找并删去其中一个 `combined` 模块对另一个 `combined` 模块的包导入，或者直接去除两个模块的 `combined` 配置，从而解决此类循环依赖。

#### "profile.test"

```text
[profile.test] # 使用举例
parallel=true
filter=*.*
no-color = true
timeout-each = "4m"
random-seed = 10
bench = false
report-path = "reports"
report-format = "xml"
verbose = true
[profile.test.build]
  compile-option = ""
  lto = "thin"
  mock = "on"
[profile.test.env]
MY_ENV = { value = "abc" }
cjHeapSize = { value = "32GB", splice-type = "replace" }
PATH = { value = "/usr/bin", splice-type = "prepend" }
```

测试配置支持指定编译和运行测试用例时的选项，所有字段均可缺省，不配置时不生效，顶层模块设置的 `profile.test` 项才会生效。选项列表与 `cjpm test` 提供的控制台执行选项一致。如果选项在配置文件和控制台中同时被配置，则控制台中的选项优先级高于配置文件中的选项。`profile.test` 支持的运行时选项：

- `filter` 指定用例过滤器，参数值类型为字符串，格式与 [test 命令说明](#test)中 `--filter` 的值格式一致
- `timeout-each <value>` 中 `value` 的格式为 `%d[millis|s|m|h]`，为每个测试用例指定默认的超时时间
- `parallel` 指定测试用例并行执行的方案，`value` 的形式如下所示：
    - `<BOOL>` 值为 `true` 或 `false`，指定为 `true` 时，测试类可被并行运行，并行进程个数将受运行系统上的 CPU 核数控制
    - `nCores` 指定并行的测试进程个数应该等于可用的 CPU 核数
    - `NUMBER` 指定并行的测试进程个数值。该数值应该为正整数
    - `NUMBERnCores` 指定并行的测试进程个数值为可用的 CPU 核数的指定数值倍。该数值应该为正数（支持浮点数或整数）
- `option:<value>` 与 `@Configure` 协同定义运行选项。例如，如下选项：
    - `random-seed` 用来指定随机种子的值，参数值类型为正整数
    - `no-color` 指定执行结果在控制台中是否无颜色显示，值为 `true` 或 `false`
    - `report-path` 指定测试执行后的报告生成路径（不能通过 `@Configure` 配置）
    - `report-format` 指定报告输出格式，当前单元测试报告仅支持 `xml` 格式（可忽略大小写），使用其它值将会抛出异常（不能通过 `@Configure` 配置），性能测试报告仅支持 `csv` 和 `csv-raw` 格式
    - `verbose` 指定显示编译过程详细信息，参数值类型为 `BOOL`，即值可为 `true` 或 `false`

#### "profile.test.build"

用于指定支持的编译选项，其列表如下:

- `compile-option` 是一个包含附加 `cjc` 编译选项的字符串。为顶级 `compile-option` 字段做补充
- `lto` 指定是否开启 `LTO` 优化编译模式，该值可为 `thin` 或 `full` ，仅 `Linux` 平台支持该功能
- `mock` 显式设置 `mock` 模式，可能的选项：`on`、`off`、`runtime-error` 。对 `test` / `build` 子命令默认值为 `on`，对于 `bench` 子命令默认值为 `runtime-error`

#### "profile.test.env"

用于在 `test` 命令时运行可执行文件时配置临时环境变量，`key` 值为需要配置的环境变量的名称，有如下配置项:

- `value` 指定配置的环境变量值
- `splice-type` 指定环境变量的拼接方式，非必填，不配置时默认为 `absent`，共有以下四种取值：
    - `absent`: 该配置仅在环境内不存在同名环境变量时生效，若存在同名环境变量则忽略该配置
    - `replace`: 该配置会替代环境中已有的同名环境变量
    - `prepend`: 该配置会拼接在环境中已有的同名环境变量之前
    - `append`: 该配置会拼接在环境中已有的同名环境变量之后

#### "profile.bench"

```text
[profile.bench] # 使用举例
no-color = true
random-seed = 10
report-path = "bench_report"
baseline-path = ""
report-format = "csv"
verbose = true
```

测试配置支持指定编译和运行测试用例时的选项，所有字段均可缺省，不配置时不生效，顶层模块设置的 `profile.bench` 项才会生效。选项列表与 `cjpm bench` 提供的控制台执行选项一致。如果选项在配置文件和控制台中同时被配置，则控制台中的选项优先级高于配置文件中的选项。`profile.bench` 支持的运行时选项:

- `filter` 指定用例过滤器，参数值类型为字符串, 格式与 [bench 命令说明](#bench)中 `--filter` 的值格式一致
- `option:<value>` 与 `@Configure` 协同定义运行选项。例如，如下选项：
    - `random-seed` 用来指定随机种子的值, 参数值类型为正整数
    - `no-color` 指定执行结果在控制台中是否无颜色显示，值为 `true` 或 `false`
    - `report-path` 指定测试执行后的报告生成路径（不能通过 `@Configure` 配置）
    - `report-format` 指定报告输出格式，当前单元测试报告仅支持 `xml` 格式（可忽略大小写），使用其它值将会抛出异常（不能通过 `@Configure` 配置）, 性能测试报告仅支持 `csv` 和 `csv-raw` 格式
    - `verbose` 指定显示编译过程详细信息，参数值类型为 `BOOL`, 即值可为 `true` 或 `false`
    - `baseline-path` 与当前性能结果进行比较的现有报告的路径。默认情况下它使用 `--report-path` 值。

#### "profile.bench.build"

用于指定为 `cjpm bench` 构建可执行文件时使用的附加编译选项。配置与 `profile.test.build` 相同。

#### "profile.bench.env"

支持配置在 `bench` 命令时运行可执行文件时的环境变量配置，配置方式同 `profile.test.env`。

#### "profile.run"

运行可执行文件时的选项，支持配置在 `run` 命令时运行可执行文件时的环境变量配置 `env`，配置方式同 `profile.test.env`。

#### "profile.customized-option"

```text
[profile.customized-option]
cfg1 = "--cfg=\"feature1=lion, feature2=cat\""
cfg2 = "--cfg=\"feature1=tiger, feature2=dog\""
cfg3 = "-O2"
```

自定义透传给 `cjc` 的选项，通过 `--cfg1 --cfg3` 使能，每个模块设置的 `customized-option` 对该模块内的所有包生效。例如，执行 `cjpm build --cfg1 --cfg3` 命令时，透传给 `cjc` 的命令则为 `--cfg="feature1=lion, feature2=cat" -O2`。

> **注意：**
>
> 这里的条件值必须是一个合法的标识符。

### "target"

多后端、多平台隔离选项，用于配置不同后端、不同平台情况下的一系列不同配置项。以 `Linux` 系统为例，`target` 配置方式如下：

```text
[target.x86_64-unknown-linux-gnu] # Linux 系统的配置项
  compile-option = "value1" # 额外编译命令选项
  override-compile-option = "value2" # 额外全局编译命令选项
  link-option = "value3" # 链接器透传选项
  [target.x86_64-unknown-linux-gnu.dependencies] # 源码依赖配置项
  [target.x86_64-unknown-linux-gnu.test-dependencies] # 测试阶段依赖配置项
  [target.x86_64-unknown-linux-gnu.bin-dependencies] # 仓颉二进制库依赖
    path-option = ["./test/pro0", "./test/pro1"]
  [target.x86_64-unknown-linux-gnu.bin-dependencies.package-option]
    "pro0.xoo" = "./test/pro0/pro0.xoo.cjo"
    "pro0.yoo" = "./test/pro0/pro0.yoo.cjo"
    "pro1.zoo" = "./test/pro1/pro1.zoo.cjo"

[target.x86_64-unknown-linux-gnu.debug] # Linux 系统的 debug 配置项
  [target.x86_64-unknown-linux-gnu.debug.test-dependencies]

[target.x86_64-unknown-linux-gnu.release] # Linux 系统的 release 配置项
  [target.x86_64-unknown-linux-gnu.release.bin-dependencies]
```

开发者可以通过配置 `target.target-name` 字段为某个 `target` 添加一系列配置项。`target` 的名称可以在相应的仓颉环境下通过命令 `cjc -v` 获取，命令输出中的 `Target` 项目即为该环境对应的 `target` 名称。上述用例应用于 `Linux` 系统，其他平台也适用，同样可以通过命令 `cjc -v` 获取 `target` 名称。

为特定 `target` 配置的专用配置项，将作用于该 `target` 的编译流程，也能被其他以该 `target` 为目标平台的交叉编译流程使用。配置项列表如下：

- `compile-option`：额外编译命令选项
- `override-compile-option`：额外全局编译命令选项
- `link-option`：链接器透传选项
- `dependencies`：源码依赖配置项，结构同 `dependencies` 字段
- `test-dependencies`：测试阶段依赖配置项，结构同 `test-dependencies` 字段
- `bin-dependencies`：仓颉二进制库依赖，结构在下文中介绍
- `compile-macros-for-target`：交叉编译时的宏包控制项，该选项不支持区分下述的 `debug` 和 `release` 编译模式

开发者可以通过配置 `target.target-name.debug` 和 `target.target-name.release` 字段为该 `target` 额外配置在 `debug` 和 `release` 编译模式下特有的配置，可配置的配置项同上。配置于此类字段的配置项将仅应用于该 `target` 的对应编译模式。

#### "target.target-name[.debug/release].bin-dependencies"

该字段用于导入已编译好的、适用于指定 `target` 的仓颉库产物文件，以导入下述的 `pro0` 模块和 `pro1` 模块的三个包来举例说明。

> **注意：**
>
> 非特殊需求场景，不建议使用该字段，请使用上文介绍的 `dependencies` 字段导入模块源码。

```text
├── test
│    ├── pro0
│    │    ├── libpro0.xoo.so
│    │    ├── pro0.xoo.cjo
│    │    ├── libpro0.yoo.so
│    │    └── pro0.yoo.cjo
│    └── pro1
│         ├── libpro1.zoo.so
│         └── pro1.zoo.cjo
├── src
│    └── main.cj
└── cjpm.toml
```

方式一，通过 `path-option` 导入：

```text
[target.x86_64-unknown-linux-gnu.bin-dependencies]
  path-option = ["./test/pro0", "./test/pro1"]
```

`path-option` 选项为字符串数组结构，每个元素代表待导入的路径名称。`cjpm` 会自动导入该路径下所有符合规则的仓颉库包，这里的合规性是指库名称的格式为 `完整包名`。例如，上述例子中的 `pro0.xoo.cjo` 对应的库名称应为 `libpro0.xoo.so` 或 `libpro0.xoo.a`。库名称不满足该规则的包只能通过 `package-option` 选项进行导入。

方式二，通过 `package-option` 导入：

```text
[target.x86_64-unknown-linux-gnu.bin-dependencies.package-option]
  "pro0.xoo" = "./test/pro0/pro0.xoo.cjo"
  "pro0.yoo" = "./test/pro0/pro0.yoo.cjo"
  "pro1.zoo" = "./test/pro1/pro1.zoo.cjo"
```

`package-option` 选项为 `map` 结构，`pro0.xoo` 名称作为 `key` (`toml` 配置文件中含有 `.` 的字符串作为整体时，需要用 `""` 包含)，所以 `key` 的值为 `libpro0.xoo.so` 。前端文件 `cjo` 的路径作为 `value`，对应于该 `cjo` 的 `.a` 或 `.so` 需放置在相同路径下。

> **注意：**
>
> 如果同时通过 `package-option` 和 `path-option` 导入了相同的包，则 `package-option` 字段的优先级更高。

其中，源码 `main.cj` 调用 `pro0.xoo`、`pro0.yoo`、`pro1.zoo` 包的代码示例如下所示。

```cangjie
import pro0.xoo.*
import pro0.yoo.*
import pro1.zoo.*

main(): Int64 {
    var res = x + y + z // x, y, z 分别为 pro0.xoo, pro0.yoo, pro1.zoo 中定义的值
    println(res)
    return 0
}
```

> **注意：**
>
> 依赖的仓颉动态库文件可能是其他模块通过配置 `profile.build.combined` 生成的 `root` 包编译产物，包含其所有子包的符号。因此，在依赖检查时，如果找不到某个包对应的仓颉库，会使用该包对应的 `root` 包作为依赖，并打印告警提示。开发者需要保证以此方式导入的 `root` 包是通过对应方式生成的仓颉库文件，否则该库文件可能不会包含子包的符号，导致编译报错。
> 例如，源码中通过 `import demo.aoo` 导入了 `demo.aoo` 包，在二进制依赖中没有找到该包对应的仓颉库，`cjpm` 会尝试寻找该包对应的 `root` 包的动态库，即 `libdemo.so`，如果找到则使用该库作为依赖。

#### "target.target-name.compile-macros-for-target"

该字段用于配置宏包的交叉编译方式，有如下三种情况：

方式一：宏包在交叉编译时默认仅编译本地平台的产物，不编译目标平台的产物，对该模块内的所有宏包生效

```text
[target.目标平台]
  compile-macros-for-target = ""
```

方式二：在交叉编译时同时编译本地平台和目标平台的产物，对该模块内的所有宏包生效

```text
[target.目标平台]
  compile-macros-for-target = "all" # 配置项为字符串形式，可选值必须为 all
```

方式三：指定该模块内的某些宏包在交叉编译时同时编译本地平台和目标平台的产物，其它未指定的宏包采取方式一的默认模式

```text
[target.目标平台]
  compile-macros-for-target = ["pkg1", "pkg2"] # 配置项为字符串数字形式，可选值是宏包名
```

#### "target" 相关字段合并规则

`target` 配置项中的内容可能同时存在于 `cjpm.toml` 的其他选项中，例如 `compile-option` 字段在 `package` 字段中也可以存在，区别在于 `package` 中的该字段会应用于全部 `target`。`cjpm` 对这些重复的字段会按照特定的方式将所有可应用的配置合并。以 `x86_64-unknown-linux-gnu` 的 `debug` 编译模式为例，有如下的 `target` 配置：

```text
[package]
  compile-option = "compile-0"
  override-compile-option = "override-compile-0"
  link-option = "link-0"

[dependencies]
  dep0 = { path = "./dep0" }

[test-dependencies]
  devDep0 = { path = "./devDep0" }

[target.x86_64-unknown-linux-gnu]
  compile-option = "compile-1"
  override-compile-option = "override-compile-1"
  link-option = "link-1"
  [target.x86_64-unknown-linux-gnu.dependencies]
    dep1 = { path = "./dep1" }
  [target.x86_64-unknown-linux-gnu.test-dependencies]
    devDep1 = { path = "./devDep1" }
  [target.x86_64-unknown-linux-gnu.bin-dependencies]
    path-option = ["./test/pro1"]
  [target.x86_64-unknown-linux-gnu.bin-dependencies.package-option]
    "pro1.xoo" = "./test/pro1/pro1.xoo.cjo"

[target.x86_64-unknown-linux-gnu.debug]
  compile-option = "compile-2"
  override-compile-option = "override-compile-2"
  link-option = "link-2"
  [target.x86_64-unknown-linux-gnu.debug.dependencies]
    dep2 = { path = "./dep2" }
  [target.x86_64-unknown-linux-gnu.debug.test-dependencies]
    devDep2 = { path = "./devDep2" }
  [target.x86_64-unknown-linux-gnu.debug.bin-dependencies]
    path-option = ["./test/pro2"]
  [target.x86_64-unknown-linux-gnu.debug.bin-dependencies.package-option]
    "pro2.xoo" = "./test/pro2/pro2.xoo.cjo"
```

`target` 配置项在与 `cjpm.toml` 公共配置项或者相同 `target` 的其他级别的配置项共存时，按照如下的优先级合并：

1. `debug/release` 模式下对应 `target` 的配置
2. `debug/release` 无关的对应 `target` 的配置
3. 公共配置项

以上述的 `target` 配置为例，`target` 各个配置项按照以下规则合并：

- `compile-option`：将所有适用的同名配置项按照优先级拼接，优先级更高的配置拼接在后方。在本例中，在 `x86_64-unknown-linux-gnu` 的 `debug` 编译模式下，最终生效的 `compile-option` 值为 `compile-0 compile-1 compile-2`，在 `release` 编译模式下为 `compile-0 compile-1`，在其他 `target` 中为 `compile-0`。
- `override-compile-option`：同上。由于 `override-compile-option` 优先级高于 `compile-option`，在最后的编译命令中，拼接完成的 `override-compile-option` 会整体置于拼接完成的 `compile-option` 之后。
- `link-option`：同上。
- `dependencies`：源码依赖将被直接合并，如果其中存在依赖冲突则会报错。在本例中，在 `x86_64-unknown-linux-gnu` 的 `debug` 编译模式下，最终生效的 `dependencies` 为 `dep0`, `dep1` 和 `dep2`，而在 `release` 编译模式下仅有 `dep0` 和 `dep1` 生效。在其他 `target` 中，仅有 `dep0` 生效。
- `test-dependencies`：同上。
- `bin-dependencies`：二进制依赖将按照优先级合并，如果有冲突则仅有优先级更高的依赖将会被加入，同优先级的配置先加入 `package-option` 配置。在本例中，在 `x86_64-unknown-linux-gnu` 的 `debug` 编译模式下，`./test/pro1` 和 `./test/pro2` 内的二进制依赖将被加入，而在 `release` 模式下仅会加入 `./test/pro1`。由于 `bin-dependencies` 没有公共配置，因此在其他 `target` 中不会有二进制依赖生效。

在本例的交叉编译场景中，若在其他平台中指定了 `x86_64-unknown-linux-gnu` 作为目标 `target`，则 `target.x86_64-unknown-linux-gnu` 的配置也会按照上述规则与公共配置项合并并应用；如果处于 `debug` 编译模式，也将应用 `target.x86_64-unknown-linux-gnu.debug` 的配置项。

### 环境变量配置

在 `cjpm.toml` 中可以用环境变量配置字段值，`cjpm` 会从当前运行环境中获取对应的环境变量值，并替换到实际的配置值中。例如，以下的 `dependencies` 字段中使用环境变量进行了路径配置：

```text
[dependencies]
aoo = { path = "${DEPENDENCY_PATH}/aoo" }
```

则在读取模块 `aoo` 时，`cjpm` 会获取 `DEPENDENCY_PATH` 变量值并进行替换，得到模块 `aoo` 的最终路径。

支持使用环境变量配置的字段列表如下：

- 单模块配置字段 `package` 中的如下字段：
    - 单包配置项 `package-configuration` 中的单包编译选项 `compile-option`
- 工作空间管理字段 `workspace` 中的如下字段：
    - 成员模块列表 `members`
    - 编译模块列表 `build-members`
    - 测试模块列表 `test-members`
- `package` 与 `workspace` 中均存在的如下字段：
    - 编译选项 `compile-option`
    - 全局编译选项 `override-compile-option`
    - 链接选项 `link-option`
    - 编译产物存放路径 `target-dir`
- 构建依赖列表 `dependencies` 中本地依赖项的 `path` 字段
- 测试依赖列表 `test-dependencies` 中本地依赖项的 `path` 字段
- 构建脚本依赖列表 `script-dependencies` 中本地依赖项的 `path` 字段
- 命令剖面配置项 `profile` 中的自定义透传选项 `customized-option`
- 外部 `c` 库配置项 `ffi.c` 中的 `path` 字段
- 平台隔离选项 `target` 中的如下字段：
    - 编译选项 `compile-option`
    - 全局编译选项 `override-compile-option`
    - 链接选项 `link-option`
    - 构建依赖列表 `dependencies` 中本地依赖项的 `path` 字段
    - 测试依赖列表 `test-dependencies` 中本地依赖项的 `path` 字段
    - 构建脚本依赖列表 `script-dependencies` 中本地依赖项的 `path` 字段
    - 二进制依赖字段 `bin-dependencies` 中的 `path-option` 和 `package-option` 字段

## 配置和缓存文件夹

`cjpm` 通过 `git` 下载文件的存储路径可以通过 `CJPM_CONFIG` 环境变量指定。如果未指定，则 `Linux/macOS` 上的默认位置为 `$HOME/.cjpm`，`Windows` 上的默认位置为 `%USERPROFILE%/.cjpm` 。

## 仓颉包管理规格说明

在仓颉包管理规格中，对于一个文件目录，被识别为一个有效源码包的要求如下：

1. 必须直接包含至少一个仓颉代码文件；
2. 其父包（包括父包的父包，直至 `root` 包）也为有效源码包。其中，模块 `root` 包不存在父包，因此仅需满足条件 1。

例如，有如下名为 `demo` 的 `cjpm` 项目：

```text
demo
├──src
│   ├── main.cj
│   └── pkg0
│        ├── aoo
│        │    └── aoo.cj
│        └── boo
│             └── boo.cj
└── cjpm.toml
```

其中，`demo.pkg0` 对应目录内没有直接包含仓颉代码，因此 `demo.pkg0` 不是一个有效源码包；`demo.pkg0.aoo` 和 `demo.pkg0.boo` 包虽然直接包含仓颉代码文件 `aoo.cj` 和 `boo.cj`，但由于其上游包 `demo.pkg0` 不是有效源码包，因此这两个包也不是有效源码包。

当 `cjpm` 识别到 `demo.pkg0` 这样的不直接包含仓颉文件的包时，会将其视为非源码包，忽略其所有子包，并打印如下告警：

```text
Warning: there is no '.cj' file in directory 'demo/src/pkg0', and its subdirectories will not be scanned as source code
```

因此，如果开发者需要配置一个有效的源码包，则该包内必须直接包含至少一个仓颉代码文件，并且其上游包都需要是有效源码包。以上述项目 `demo` 为例，如果想要让 `demo.pkg0`,`demo.pkg0.aoo` 和 `demo.pkg0.boo` 均被识别为有效源码包，则可以在 `demo/src/pkg0` 内添加一个仓颉代码文件，如下所示：

```text
demo
├── src
│    ├── main.cj
│    └── pkg0
│         ├── pkg0.cj
│         ├── aoo
│         │    └── aoo.cj
│         └── boo
│              └── boo.cj
└── cjpm.toml
```

`demo/src/pkg0/pkg0.cj` 需要是一个符合包管理规格的仓颉代码文件，可以不包含功能代码，例如如下形式：

```cangjie
package demo.pkg0
```

## 命令扩展

`cjpm` 提供命令扩展机制，开发者可以通过文件名形如 `cjpm-xxx(.exe)` 的可执行文件扩展 `cjpm` 的命令。

针对可执行文件 `cjpm-xxx`（`Windows` 系统中为 `cjpm-xxx.exe`），若系统环境变量 `PATH` 中配置了该文件所在的路径，则可以使用如下的命令运行该可执行文件：

```shell
cjpm xxx [args]
```

其中 `args` 为可能需要的输入给 `cjpm-xxx(.exe)` 的参数列表。上述命令等价于：

```shell
cjpm-xxx(.exe) [args]
```

运行 `cjpm-xxx(.exe)` 可能会依赖某些动态库，在这种情况下，开发者需要手动将需要使用的动态库所在的目录添加到环境变量中。

下面以 `cjpm-demo` 为例，该可执行文件由以下仓颉代码编译得到：

```cangjie
import std.process.*
import std.collection.*

main(): Int64 {
    var args = ArrayList<String>(Process.current.arguments)

    if (args.size < 1) {
        eprintln("Error: failed to get parameters")
        return 1
    }

    println("Output: ${args[0]}")

    return 0
}
```

则在将其目录添加到 `PATH` 之后，运行对应命令，会运行该可执行文件并获得对应的输出。

```text
输入：cjpm demo hello,world
输出：Output: hello,world
```

`cjpm` 内部已有的命令优先级更高，因此无法用此方式扩展这些命令。例如，即使系统环境变量中存在名为 `cjpm-build` 的可执行文件，`cjpm build` 也不会运行该文件，而是运行 `cjpm` 并将 `build` 作为参数输入 `cjpm`。

## 构建脚本

`cjpm` 提供构建脚本机制，开发者可以在构建脚本中定义需要 `cjpm` 在某个命令前后的行为。

构建脚本源文件固定命名为 `build.cj`，位于仓颉项目主目录下，即与 `cjpm.toml` 同级。执行 `init` 命令新建仓颉项目时，`cjpm` 默认不创建 `build.cj`，开发者若有相关需求，可以自行按如下的模板格式在指定位置新建并编辑 `build.cj`。

```cangjie
// build.cj

import std.process.*

// Case of pre/post codes for 'cjpm build'.
/* called before `cjpm build`
 * Success: return 0
 * Error: return any number except 0
 */
// func stagePreBuild(): Int64 {
//     // process before "cjpm build"
//     0
// }

/*
 * called after `cjpm build`
 */
// func stagePostBuild(): Int64 {
//     // process after "cjpm build"
//     0
// }

// Case of pre codes for 'cjpm clean'.
/* called before `cjpm clean`
 * Success: return 0
 * Error: return any number except 0
 */
// func stagePreClean(): Int64 {
//     // process before "cjpm clean"
//     0
// }

// For other options, define stagePreXXX and stagePostXXX in the same way.

/*
 * Error code:
 * 0: success.
 * other: cjpm will finish running command. Check target-dir/build-script-cache/module-name/script-log for error outputs defind by user in functions.
 */

main(): Int64 {
    match (Process.current.arguments[0]) {
        // Add operation here with format: "pre-"/"post-" + optionName
        // case "pre-build" => stagePreBuild()
        // case "post-build" => stagePostBuild()
        // case "pre-clean" => stagePreClean()
        case _ => 0
    }
}
```

`cjpm` 针对一系列命令支持使用构建脚本定义命令前后行为。例如，针对 `build` 命令，可在 `main` 函数中的 `match` 内定义 `pre-build`，执行想要在 `build` 命令执行前需要执行的功能函数 `stagePreBuild`（功能函数的命名不做要求）。`build` 命令后的行为可以以相同的方式通过添加 `post-build` 的 `case` 选项定义。针对其他命令的命令前后行为的定义类似，只需要添加相应的 `pre/post` 选项和对应的功能函数即可。

在定义某一命令前后的行为后，`cjpm` 在执行该命令时会首先编译 `build.cj`，并在执行前后执行对应的行为。同样以 `build` 为例，在定义了 `pre-build` 和 `post-build` 后运行 `cjpm build`，则会按照如下步骤运行整个 `cjpm build` 流程：

1. 进行编译流程前，首先编译 `build.cj`；
2. 执行 `pre-build` 对应的功能函数；
3. 进行 `cjpm build` 编译流程；
4. 编译流程顺利结束后，`cjpm` 会执行 `post-build` 对应的功能函数。

构建脚本支持的命令如下：

- `build`, `test`, `bench`：同时支持执行依赖模块构建脚本中定义的 `pre` 和 `post` 流程
- `run`, `install`：仅支持运行对应模块的 `pre` 和 `post` 构建脚本流程，或者在进行编译时执行依赖模块的 `pre-build` 和 `post-build` 流程
- `check`, `tree`, `update`：仅支持运行对应模块的 `pre` 和 `post` 构建脚本流程
- `clean`：仅支持运行对应模块的 `pre` 构建脚本流程

在执行这些命令时，若配置了 `--skip-script` 选项，则会跳过所有构建脚本的编译运行，包括依赖模块的构建脚本。

构建脚本的使用说明如下：

- 功能函数的返回值需要满足一定要求：当功能函数执行成功时，需要返回 `0`；执行失败时返回除 `0` 以外的任意 `Int64` 类型变量。
- `build.cj` 中的所有输出都将被重定向到项目目录下，路径为 `build-script-cache/[target|release]/[module-name]/bin/script-log`。开发者如果在功能函数中添加了一些输出内容，可在该文件中查看。
- 若项目根目录下不存在 `build.cj`，则 `cjpm` 将按正常流程执行；若存在 `build.cj` 并定义了某一命令的前后行为，则在 `build.cj` 编译失败或者功能函数返回值不为 `0` 时，即使该命令本身能够顺利执行，命令也将异常中止。
- 多模块场景下，被依赖模块的 `build.cj` 构建脚本会在编译和单元测试流程中生效。被依赖模块构建脚本中的输出同样重定向到 `build-script-cache/[target|release]` 下对应模块名目录中的日志文件。

例如，下面的构建脚本 `build.cj` 定义了 `build` 前后的行为：

```cangjie
import std.process.*

func stagePreBuild(): Int64 {
    println("PRE-BUILD")
    0
}

func stagePostBuild(): Int64 {
    println("POST-BUILD")
    0
}

main(): Int64 {
    match (Process.current.arguments[0]) {
        case "pre-build" => stagePreBuild()
        case "post-build" => stagePostBuild()
        case _ => 0
    }
}
```

则在执行 `cjpm build` 命令时，`cjpm` 将会执行 `stagePreBuild` 和 `stagePostBuild`。`cjpm build` 执行完成后，`script-log` 日志文件内会有如下输出：

```text
PRE-BUILD
POST-BUILD
```

构建脚本可以通过 `cjpm.toml` 中的 `script-dependencies` 字段导入依赖模块，格式同 `dependencies`。例如，在 `cjpm.toml` 中有如下配置，导入了 `aoo` 模块，并且 `aoo` 模块内有一个名为 `aaa()` 的方法：

```text
[script-dependencies]
aoo = { path = "./aoo" }
```

则可以在构建脚本中导入该依赖，使用依赖中的接口 `aaa()`：

```cangjie
import std.process.*
import aoo.*

func stagePreBuild(): Int64 {
    aaa()
    0
}

func stagePostBuild(): Int64 {
    println("POST-BUILD")
    0
}

main(): Int64 {
    match (Process.current.arguments[0]) {
        case "pre-build" => stagePreBuild()
        case "post-build" => stagePostBuild()
        case _ => 0
    }
}
```

构建脚本依赖 `script-dependencies` 与源码相关依赖（源码依赖项 `dependencies` 和测试依赖项 `test-dependencies`）相互独立，源码和测试代码无法使用 `script-dependencies` 中的依赖模块，构建脚本也无法使用 `dependencies` 和 `test-dependencies` 中的依赖模块。若需要在构建脚本和源码/测试代码中使用同一模块，需要在 `script-dependencies` 和 `dependencies/test-dependencies` 中同时配置。

## 使用示例

以下面仓颉项目的目录结构为例，介绍 `cjpm` 的使用方法，该目录下对应的源码文件示例可见[源代码](#示例的源代码)。该仓颉项目的模块名为 `test`。

```text
cj_project
├── pro0
│    ├── cjpm.toml
│    └── src
│         ├── zoo
│         │    ├── zoo.cj
│         │    └── zoo_test.cj
│         └── pro0.cj
├── src
│    ├── koo
│    │    ├── koo.cj
│    │    └── koo_test.cj
│    ├── main.cj
│    └── main_test.cj
└── cjpm.toml
```

### init、build 的使用

- 新建仓颉项目并编写源码 `xxx.cj` 文件，如示例结构所示的 `koo` 包和 `main.cj` 文件。

    ```shell
    cjpm init --name test --path ./cj_project
    cd cj_project
    mkdir src/koo
    ```

    此时，会在当前执行命令的目录下创建 `cj_project` 目录，并在该目录中自动生成 `src` 文件夹和默认的 `cjpm.toml` 配置文件。开发者可以自行在源码目录 `src` 中新建子包（如 `src/koo`），或是自行在各包中新增源码文件和测试文件。

- 当前模块需要依赖外部的 `pro0` 模块时，可以新建 `pro0` 模块及该模块的配置文件，接下来编写该模块的源码文件，需要自行在 `pro0` 下新建 `src` 文件夹，在 `src` 下新建 `pro0` 的 root 包 `pro0.cj`，并将编写的仓颉包放置在 `src` 下，如示例结构所示的 `zoo` 包。

    ```shell
    mkdir pro0 && cd pro0
    cjpm init --name pro0 --type=static
    mkdir src/zoo
    ```

- 主模块依赖 `pro0` 时，需要按照手册说明去配置主模块配置文件的 `dependencies` 字段。配置无误后，执行 `cjpm build` 即可，生成的可执行文件在 `target/release/bin/` 目录下。

    ```shell
    cd cj_project
    vim cjpm.toml
    cjpm build
    cjpm run
    ```

### test、clean 的使用

- 按示例结构，编写完每个文件对应的 `xxx_test.cj` 单元测试文件后，可以执行下述代码进行单元测试，生成的文件在 `target/release/unittest_bin` 目录下。

    ```shell
    cjpm test
    ```

    或者

    ```shell
    cjpm test src src/koo pro0/src/zoo
    ```

- 想要手动删除 `target` 、`cov_output` 文件夹、`*.gcno` 、`*.gcda` 等中间件时，执行如下命令：

    ```shell
    cjpm clean
    ```

### 示例的源代码

```cangjie
// cj_project/src/main.cj
package test

import pro0.zoo.*
import test.koo.*

main(): Int64 {
    let res = z + k
    println(res)
    let res2 = concatM("a", "b")
    println(res2)
    return 0
}

func concatM(s1: String, s2: String): String {
    return s1 + s2
}
```

```cangjie
// cj_project/src/main_test.cj
package test

import std.unittest.* // testfame
import std.unittest.testmacro.* // macro_Defintion

@Test
public class TestM{
    @TestCase
    func sayhi(): Unit {
        @Assert(concatM("1", "2"), "12")
        @Assert(concatM("1", "3"), "13")
    }
}
```

```cangjie
// cj_project/src/koo/koo.cj
package test.koo

public let k: Int32 = 12

func concatk(s1: String, s2: String): String {
    return s1 + s2
}
```

```cangjie
// cj_project/src/koo/koo_test.cj
package test.koo

import std.unittest.* // testfame
import std.unittest.testmacro.* // macro_Defintion

@Test
public class TestK{
    @TestCase
    func sayhi(): Unit {
        @Assert(concatk("1", "2"), "12")
        @Assert(concatk("1", "3"), "13")
    }
}
```

```cangjie
// cj_project/pro0/src/pro0.cj
package pro0
```

```cangjie
// cj_project/pro0/src/zoo/zoo.cj
package pro0.zoo

public let z: Int32 = 26

func concatZ(s1: String, s2: String): String {
    return s1 + s2
}
```

```cangjie
// cj_project/pro0/src/zoo/zoo_test.cj
package pro0.zoo

import std.unittest.* // testfame
import std.unittest.testmacro.* // macro_Defintion

@Test
public class TestZ{
    @TestCase
    func sayhi(): Unit {
        @Assert(concatZ("1", "2"), "12")
        @Assert(concatZ("1", "3"), "13")
    }
}
```

```toml
# cj_project/cjpm.toml
[package]
cjc-version = "1.0.0"
description = "nothing here"
version = "1.0.0"
name = "test"
output-type = "executable"

[dependencies]
pro0 = { path = "pro0" }
```

```toml
# cj_project/pro0/cjpm.toml
[package]
cjc-version = "1.0.0"
description = "nothing here"
version = "1.0.0"
name = "pro0"
output-type = "static"
```
