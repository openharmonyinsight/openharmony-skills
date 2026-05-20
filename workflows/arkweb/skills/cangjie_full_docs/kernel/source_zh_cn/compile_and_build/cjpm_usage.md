# `cjpm` 介绍

`CJPM（Cangjie Project Manager）` 是仓颉语言的官方项目管理工具，用来管理、维护仓颉项目的模块系统，并且提供更简易统一的编译入口，支持自定义编译命令。通过自动依赖管理，实现对引入的多版本三方依赖软件进行分析合并，无需开发者担心多版本依赖冲突问题，大大减轻开发者的负担。同时提供基于仓颉语言原生的自定义构建机制，允许开发者在构建的不同阶段增加预处理和后处理流程，实现构建流程可灵活定制，能够满足开发者不同业务场景下的编译构建需求。

## `cjpm` 基本使用方法

通过 `cjpm -h` 即可查看主界面，由几个板块组成，从上到下分别是： 当前命令说明、使用示例（Usage）、支持的可用命令（Available subcommands）、支持的配置项（Available options）、更多提示内容。

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

`cjpm init` 用来初始化一个新的仓颉模块或工作空间。初始化模块时会默认在当前文件夹创建 `cjpm.toml` 文件，并且新建 `src` 源码文件夹，在 `src` 下生成默认的 `main.cj` 文件。自定义参数初始化功能支持可以通过 `cjpm init -h` 查看。

例如：

```text
输入: cjpm init
输出: cjpm init success
```

`cjpm build` 用来构建当前仓颉项目，执行该命令前会先检查依赖项，检查通过后调用 `cjc` 进行构建。支持全量编译、增量编译、交叉编译、并行编译等，更多编译功能支持可以通过 `cjpm build -h` 查看。通过 `cjpm build -V` 命令可以打印所有的编译过程命令。

例如：

```text
输入: cjpm build -V
输出:
compile package module1.package1: cjc --import-path target -p "src/package1" --output-type=staticlib -o target/release/module1/libmodule1.package1.a
compile package module1: cjc --import-path target -L target/release/module1 -lmodule1.package1 -p "src" --output-type=exe --output-dir target/release/bin -o main

cjpm build success
```

## `cjpm.toml` 配置文件说明

配置文件 `cjpm.toml` 用来配置一些基础信息、依赖项、编译选项等内容，`cjpm` 主要通过这个文件进行解析执行。

配置文件代码如下所示：

```text
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
  coo = { git = "xxx", branch = "dev" } # 导入 `git` 依赖
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
