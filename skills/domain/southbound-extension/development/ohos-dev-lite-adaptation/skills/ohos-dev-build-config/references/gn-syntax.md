> **Scope**: GN 语法速查（数据类型、作用域、内置函数、构建规则）
> **When**: 编写 BUILD.gn 或 config.gni 时对 GN 语法不确定时读取
> **Size**: ~200 lines

---

## 基本数据类型

```gn
enable_feature = true                       # 布尔值
name = "my_module"                          # 字符串
count = 42                                  # 整数
sources = [ "main.c", "utils.c" ]           # 列表

sources += [ "extra.c" ]                    # 追加
sources -= [ "unused.c" ]                   # 移除
first = sources[0]                          # 索引
full_path = "${root_out_dir}/lib"           # 变量插值
label = ":${module_name}"                   # 动态目标名
```

## 变量作用域

- **import()** 会将 `.gni` 文件的变量注入当前作用域（类似 C 的 `#include`）
- **花括号块** `{}` 创建独立作用域，内部变量不泄漏到外部，但外部变量在块内可见
- **BUILD.gn** 不能被 import，而是通过 `deps` 引用其目标

```gn
import("//device/board/vendor/board/liteos_m/config.gni")
# 此后可直接使用 config.gni 中定义的 board_cpu、board_cflags 等

if (board_cpu == "cortex-m4") {
  local_var = "only visible inside this block"
}
# local_var 在此不可见
```

## GN 内置变量

GN 自动设置的变量，无需手动定义：

| 变量 | 说明 |
|------|------|
| `target_cpu` / `target_os` | 目标 CPU 和 OS（如 `"arm"` / `"liteos_m"`） |
| `current_cpu` / `current_os` | 当前工具链的 CPU 和 OS |
| `current_toolchain` | 当前工具链标签 |
| `root_build_dir` | GN 输出根目录（如 `"out/board/product"`） |
| `root_out_dir` | 当前工具链的输出目录 |
| `ohos_root_path` | OpenHarmony 源码根路径，等价于 `//`（旧代码使用） |

## import() 路径约定

```gn
import("//build/lite/config/component/lite_component.gni")  # // = 源码根目录（推荐）
import("../config.gni")                                      # 相对当前文件目录
```

- `//` 前缀：从源码根目录解析，推荐跨目录引用
- 无前缀：相对当前文件目录，仅用于同目录或相邻目录
- `${ohos_root_path}` 前缀：旧代码写法，效果与 `//` 相同

## 常用内置函数

### get_path_info() — 提取路径组成

```gn
basename = get_path_info("src/main.c", "name")       # → "main.c"
dirname  = get_path_info("src/main.c", "dir")         # → "src"
stem     = get_path_info("src/main.c", "file")        # → "main"
ext      = get_path_info("src/main.c", "extension")   # → ".c"

# 常见用法：获取当前目录名作为模块名
module_name = get_path_info(rebase_path("."), "name")
```

### rebase_path() — 路径基准转换

```gn
abs_path = rebase_path(".", root_build_dir)           # 相对路径 → 绝对路径
rel = rebase_path("//device/soc/st/stm32f407", "//build/lite")  # 相对于另一目录
```

### exec_script() — 执行外部脚本

```gn
result = exec_script("//build/lite/run_shell_cmd.py", [ "echo hello" ], "value")

# 检查文件是否存在
cmd = "if [ -f ${path}/BUILD.gn ]; then echo true; else echo false; fi"
exists = exec_script("//build/lite/run_shell_cmd.py", [ cmd ], "value")
```

### defined() — 检查变量是否已定义

```gn
if (defined(LOSCFG_SOC_COMPANY_BESTECHRIC)) {
  sources += [ "driver_bes.c" ]
}
if (!defined(board_opt_flags)) {
  board_opt_flags = []               # 设置默认值
}
```

### assert() — 条件断言

```gn
assert(defined(board_cpu), "board_cpu must be defined")
assert(board_cpu != "", "board_cpu cannot be empty")
```

### not_needed() — 消除"变量未使用"警告

```gn
sdk_modules_name_list = [ "a.ko", "b.ko" ]
if (defined(ohos_lite)) {
  not_needed(sdk_modules_name_list)   # lite 分支不使用此变量
} else {
  foreach(module, sdk_modules_name_list) { ... }
}
```

### read_file() / write_file() — 文件读写

```gn
content = read_file("//path/to/file.txt", "value")     # 读为字符串
config = read_file("//path/to/config.json", "json")    # 读为 JSON scope
write_file("$root_gen_dir/version.h", "#define V 1\n") # 写入文件
write_file("$root_gen_dir/out.json", data, "json")     # 写入 JSON
```

### print() — 调试输出

```gn
print("Building for: ", board_cpu)
```

## Label（目标标签）语法

每个构建目标通过 label 唯一标识：

```gn
deps = [ "//kernel/liteos_m/utils:utils" ]    # 完整 label: //路径:目标名
deps = [ ":gpio_driver" ]                      # 当前目录下的目标
deps = [ "//device/soc/st/stm32f407" ]         # 省略目标名 = 目录最后一段名
deps = [ "//lib:mylib(//build/lite/toolchain/gcc:gcc)" ]  # 指定工具链
```

## 构建规则

### static_library / executable / group

```gn
static_library("mylib") {
  sources = [ "lib.c" ]
  include_dirs = [ "include" ]
  deps = [ "//other:target" ]
  public_configs = [ ":my_config" ]
}

executable("my_app") {
  sources = [ "main.c" ]
  deps = [ ":mylib" ]
  ldflags = [ "-T${linker_script}", "-nostartfiles" ]
}

group("all") {
  deps = [ ":app", ":lib", "//other/package:target" ]
}
```

### config — 编译配置

```gn
config("my_config") {
  include_dirs = [ "include" ]
  defines = [ "DEBUG=1", "CHIP_STM32" ]
  cflags = [ "-Wall", "-Werror" ]
}
```

### deps vs public_deps vs public_configs

```gn
static_library("mylib") {
  sources = [ "lib.c" ]

  # deps — 私有依赖：仅编译 mylib 时需要，不传递给依赖者
  deps = [ "//internal/helper:helper" ]

  # public_deps — 公共依赖：传递给所有依赖 mylib 的目标
  # 依赖者也需要该依赖的头文件时使用
  public_deps = [ "//third_party/cmsis:cmsis" ]

  # public_configs — 导出 include_dirs / defines 等给依赖者
  public_configs = [ ":mylib_public_config" ]
}

config("mylib_public_config") {
  include_dirs = [ "include" ]
  defines = [ "USE_MYLIB=1" ]
}
```

**选择规则**：仅内部用 → `deps`；头文件被依赖者引用 → `public_deps`；导出编译配置 → `public_configs`

### 条件构建 / foreach

```gn
if (board_cpu == "cortex-m4") {
  sources += [ "arch/arm_cm4/port.c" ]
} else if (board_arch == "rv32imac") {
  sources += [ "arch/riscv/port.c" ]
}

foreach(lib, [ "liba", "libb" ]) {
  copy("${lib}") {
    sources = [ "out/${lib}.so" ]
    outputs = [ "$root_out_dir/${lib}.so" ]
  }
}
```

## 注意事项

- GN 文件末尾**必须有空行**，否则报 `Expected a newline or eof`
- 列表逗号分隔，末尾逗号可选
- 路径分隔符始终用 `/`（Windows 上也一样），不支持转义字符
- `=` 赋值，`+=` 追加，`-=` 移除；`==` 相等比较，`!=` 不等比较
