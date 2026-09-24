> **Scope**: BUILD.gn 三种核心模板（static_library / lite_component / hdf_driver）
> **When**: 需要生成 SoC 级 BUILD.gn 或驱动 BUILD.gn 时读取
> **Size**: ~160 lines

---

## 模板概览

L0 轻量系统使用三种 BUILD.gn 模板构建模块：

| 模板 | 用途 | 导入依赖 |
|------|------|---------|
| `static_library` | 编译源文件为静态库（.a） | 无需额外导入 |
| `lite_component` | 将目标打包为部件（供 config.json 引用） | `import("//build/lite/config/component/lite_component.gni")` |
| `hdf_driver` | HDF 平台驱动（精简版 HDF） | `import("//drivers/hdf_core/adapter/khdf/liteos_m/hdf.gni")` |

---

## 1. static_library 模板

### 语法格式

```gn
static_library("<target_name>") {
  sources = [
    "src/file1.c",
    "src/file2.c",
  ]

  include_dirs = [
    "include",                                    # 相对路径：当前目录下
    "//kernel/liteos_m/kal/cmsis",               # 绝对路径：// 表示源码根目录
    "//device/soc/<vendor>/<soc>/hal/include",
  ]

  cflags = [                                      # 额外的编译标志（可选）
    "-DCHIP_SPECIFIC_MACRO",
  ]

  deps = [                                        # 依赖的其他目标（可选）
    "//kernel/liteos_m/utils:utils",
  ]

  public_configs = [ ":<config_name>" ]           # 导出配置（可选）
}
```

### 参数说明

- **sources**：要编译的 .c/.S 源文件列表
- **include_dirs**：头文件搜索路径，支持相对路径和 `//` 开头的绝对路径
- **deps**：依赖目标，格式为 `"//path/to:target_name"`，冒号后是目标名
- **public_configs**：导出给依赖者的配置（include_dirs、defines 等）

### 真实示例（STM32 SoC BUILD.gn）

```gn
# device/soc/st/stm32f407zg/BUILD.gn
group("stm32f407zg") {
  # 简单 SoC 可以只用一个 group 将多个子目标打包
}
```

### 真实示例（Hi3861 SoC BUILD.gn）

```gn
# device/soc/hisilicon/hi3861v100/BUILD.gn
group("hi3861v100") {
  deps = [ "sdk_liteos:run_wifiiot_scons" ]
}
```

---

## SoC BUILD.gn 与厂商 SDK 接入点

**关键边界**：SoC BUILD.gn 通常是"壳"，真正的芯片 SDK 本体（寄存器级底层代码、厂商驱动、二进制库）由**芯片厂商提供**，不由本 SKILL 生成。本 SKILL 只生成"壳 + 接入点"，让用户挂自己的 SDK。

SoC SDK 的常见构建方式有三种，接入点写法各不同：

### 方式 1：SDK 用 scons/make 编译（壳调用脚本）

真机 Hi3861 即此模式——SDK 用 scons 编译，GN 只是通过一个 `action`/`group` target 触发 scons：

```gn
# device/soc/<vendor>/<soc>/BUILD.gn
group("<soc>") {
  deps = [ "sdk_liteos:run_wifiiot_scons" ]   # ← 接入点：厂商 scons 构建目标
}
# 厂商在 device/soc/<vendor>/<soc>/sdk_liteos/BUILD.gn 里定义 run_wifiiot_scons
```

### 方式 2：SDK 源码用 GN 编译（壳 deps 子目录）

```gn
# device/soc/<vendor>/<soc>/BUILD.gn
group("<soc>") {
  deps = [
    ":hal",            # SoC HAL 适配层（用户提供源码）
    "sdk:libs",        # 厂商 SDK 源码编译目标
  ]
}
```

### 方式 3：SDK 为预编二进制库（壳引用 prebuilt）

```gn
# device/soc/<vendor>/<soc>/BUILD.gn
group("<soc>") {
  deps = [ "prebuilt:vendor_sdk" ]   # 预编 .a/.so 库
}
```

### 生成时的处理

生成 SoC BUILD.gn 时，**按用户是否已有 SDK 决定接入点**：
- 已有 SDK（scons/make/GN/预编库）：用对应方式预留 `deps` 接入点，注释标明用户需补的子 BUILD.gn
- 暂无 SDK：生成空壳 `group("<soc>") { deps = [] }`，注释 `# TODO: 接入厂商 SDK 构建目标`

> 本 SKILL **不生成** `sdk_liteos/`、`hal/`、`prebuilt/` 等子目录的源码与 BUILD.gn——这些是厂商私有内容。本 SKILL 只在顶层 SoC BUILD.gn 预留 deps 接入点并写清注释，把"挂 SDK"这一步明确留给用户。

### 真实 SoC BUILD.gn 参考

本模板描述接入点模式。如需参照真实 SoC BUILD.gn：
- 本项目 `ohos-dev-board-config-gen/examples/` 目录有多个芯片的 BUILD.gn 样本
- 也可在项目中搜索 `BUILD.gn` 文件或联网查找对应芯片的 OpenHarmony 适配仓库

- `soc-configs/hi3861_BUILD.gn` — Hi3861，scons 接入点：`group { deps = ["sdk_liteos:run_wifiiot_scons"] }`
- `soc-configs/stm32f407zg_BUILD.gn` — STM32F407，空壳：`group {} `
- `soc-configs/bes2600_BUILD.gn` — BES2600，多模块：`module_group { modules = ["hals"] }`

真实示例展示了 scons 接入、空壳、多模块三种典型模式，与本模板描述一致。

---

## Board 级 BUILD.gn

Board 目录也需一个 BUILD.gn 作为入口（config.json 的 `device_build_path` 指向它）：

```gn
# device/board/<vendor>/<board>/BUILD.gn
group("<board>") {
  deps = []
  # 如有板级驱动/配置模块，在此引用：
  # "//device/board/<vendor>/<board>/liteos_m:hdf_config",
}
```

> target 名约定用 `<board>`。Board 级 BUILD.gn 通常更轻，仅作 hb 装配入口。

---

## 2. lite_component 模板

### 语法格式

```gn
import("//build/lite/config/component/lite_component.gni")

lite_component("<component_name>") {
  features = [
    ":<local_target>",                            # 引用本文件中的目标
    "//path/to/other:target",                     # 引用其他目录的目标
  ]
}
```

### 参数说明

- **features**：部件包含的目标列表。`config.json` 中的 component 名称必须与此处的 `<component_name>` 完全一致

### 真实示例（IoT 外设驱动）

```gn
import("//build/lite/config/component/lite_component.gni")

static_library("gpio_driver") {
  sources = [
    "src/gpio_core.c",
    "src/gpio_hal.c",
  ]
  include_dirs = [
    "include",
    "//kernel/liteos_m/kal/cmsis",
    "//device/soc/${soc_company}/${soc_name}/hal/include",
  ]
  deps = [
    "//kernel/liteos_m/utils:utils",
  ]
}

lite_component("driver_gpio") {
  features = [
    ":gpio_driver",
  ]
}
```

---

## 3. hdf_driver 模板

### 语法格式

```gn
import("//drivers/hdf_core/adapter/khdf/liteos_m/hdf.gni")

module_switch = defined(LOSCFG_DRIVERS_HDF_PLATFORM_<TYPE>)
module_name = get_path_info(rebase_path("."), "name")

hdf_driver(module_name) {
  sources = [ "src/driver.c" ]
  include_dirs = [ "." ]
  deps = []
}
```

### 条件编译模式（多平台源文件选择）

hdf_driver 常用 `if (defined(...))` 按芯片平台选择不同源文件：

```gn
import("//drivers/hdf_core/adapter/khdf/liteos_m/hdf.gni")

module_switch = defined(LOSCFG_DRIVERS_HDF_PLATFORM_GPIO)
module_name = get_path_info(rebase_path("."), "name")

hdf_driver(module_name) {
  sources = []

  if (defined(LOSCFG_SOC_COMPANY_BESTECHRIC)) {
    sources += [ "gpio_bes.c" ]
  }
  if (defined(LOSCFG_SOC_COMPANY_GOODIX)) {
    sources += [ "gpio_gr5xx.c" ]
  }
  if (defined(LOSCFG_SOC_SERIES_STM32F4xx)) {
    sources += [ "gpio_stm32f4xx.c" ]
  }

  include_dirs = [ "." ]

  if (defined(LOSCFG_DRIVERS_HDF_CONFIG_MACRO)) {
    deps = [ "//device/board/$device_company/$device_name/liteos_m/hdf_config" ]
  }
}
```

**关键模式**：
- `LOSCFG_SOC_COMPANY_<VENDOR>`：按芯片厂商选择源文件
- `LOSCFG_SOC_SERIES_<SERIES>`：按芯片系列选择源文件
- 这些宏在 SoC 的 Kconfig 中定义，由内核适配层导出到 GN 构建环境

---

## deps 依赖写法

### 引用内核模块

```gn
deps = [
  "//kernel/liteos_m/utils:utils",               # 内核工具库
  "//kernel/liteos_m/kal/cmsis:cmsis",            # CMSIS 适配层
]
```

格式：`"//<目录路径>:<目标名>"` — 目录路径从源码根目录开始，冒号后是 BUILD.gn 中定义的目标名。

### 引用其他子系统组件

```gn
deps = [
  "//drivers/peripheral/uart:uart_driver",        # 外设驱动
  "//commonlibrary/utils_lite:utils",             # 公共库
]
```

### 使用 group() 打包依赖

```gn
group("my_soc_all") {
  deps = [
    ":hal_library",                               # 本目录内的目标用 ":target"
    ":driver_library",
    "//kernel/liteos_m/utils:utils",              # 其他目录的目标用完整路径
  ]
}
```

`group()` 是虚拟目标，不编译任何文件，仅将多个依赖打包为一个统一入口。

### config() 导出配置

```gn
config("my_public_config") {
  include_dirs = [ "include" ]                    # 头文件路径
  defines = [ "MY_MACRO=1" ]                     # 宏定义
  cflags = [ "-Wall" ]                           # 编译标志
}

static_library("mylib") {
  sources = [ "mylib.c" ]
  public_configs = [ ":my_public_config" ]        # 导出给依赖者
}
```

依赖 `mylib` 的目标会自动继承 `my_public_config` 中的 include_dirs 和 defines。
