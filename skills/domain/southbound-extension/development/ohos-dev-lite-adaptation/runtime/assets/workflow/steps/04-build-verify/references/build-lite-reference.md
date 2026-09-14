# build_lite构建系统详解 + 核心配置文件说明

> 来源：需求4分析报告 §3 + §4 + §5 + §12（常见编译错误）

---

## 1. 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│               OpenHarmony Lite Build System (build_lite)          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Product Config│  │ Board Config │  │   SoC Config         │  │
│  │ product.json │  │ config.gni   │  │   config.gni         │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
│         │                 │                      │               │
│         └─────────────────┼──────────────────────┘               │
│                           ↓                                      │
│              ┌────────────────────────┐                         │
│              │  BUILDCONFIG.gn        │                         │
│              │  (顶层构建配置)         │                         │
│              └────────────┬───────────┘                         │
│                           ↓                                      │
│         ┌─────────────────┴─────────────────┐                   │
│         ↓                                   ↓                   │
│  ┌──────────────┐                  ┌──────────────┐            │
│  │  BUILD.gn    │                  │  Toolchain   │            │
│  │ (各子系统)   │                  │  Configuration│            │
│  └──────┬───────┘                  └──────┬───────┘            │
│         │                                 │                     │
│         └─────────────────┬───────────────┘                     │
│                           ↓                                      │
│              ┌────────────────────────┐                         │
│              │      GN Frontend       │                         │
│              │   (generate ninja)     │                         │
│              └────────────┬───────────┘                         │
│                           ↓                                      │
│              ┌────────────────────────┐                         │
│              │     build.ninja        │                         │
│              │   (generated rules)    │                         │
│              └────────────┬───────────┘                         │
│                           ↓                                      │
│              ┌────────────────────────┐                         │
│              │     Ninja Executor     │                         │
│              │  (compile & link)      │                         │
│              └────────────┬───────────┘                         │
│                           ↓                                      │
│              ┌────────────────────────┐                         │
│              │   Output Images        │                         │
│              │  (.bin/.elf/.img)      │                         │
│              └────────────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

## 2. 构建流程详解

### 2.1 Lite系统构建命令

```bash
# 方式1: 使用build.sh脚本（推荐）
./build.sh --product-name <product> --build-target <target>

# 方式2: 直接使用GN+Ninja（build_lite方式）
gn gen out/<board>/<product> --args='product_name="<product>"'
ninja -C out/<board>/<product>

# 方式3: 使用hb工具（旧版本，仅适用于轻量/小型系统）
hb set -p <product>
hb build
```

> ⚠️ **注意**：Lite系统不使用标准系统的`--system-type standard`参数。产品名对应`vendor/<vendor>/<product>/config.json`中的定义。

### 2.2 GN配置加载顺序（Lite系统）

```
1. .gn                          # 根配置文件，指定buildconfig路径
   ↓
2. build/lite/config/BUILDCONFIG.gn  # Lite系统顶层构建配置
   ↓
3. vendor/<vendor>/<product>/config.json  # 产品定义（子系统+部件列表）
   ↓
4. device/board/<vendor>/<board>/liteos_m/config.gni  # 单板配置
   ↓
5. device/soc/<vendor>/<soc>/config.gni  # SoC配置
   ↓
6. 各子系统的BUILD.gn           # 模块构建定义
   ↓
7. 生成 build.ninja
```

> ⚠️ **关键区别**：Lite系统使用`vendor/<vendor>/<product>/config.json`作为产品定义入口，而非标准系统的`productdefine/common/products/<product>.json`和`productdefine/common/inherit/*.json`继承机制。

## 3. 关键目录结构（Lite系统）

```
OpenHarmony-Lite/
├── build/                          # 构建框架
│   └── lite/                       # ⭐ Lite系统专用构建（build_lite）
│       ├── config/
│       │   ├── BUILDCONFIG.gn     # Lite顶层配置
│       │   ├── compiler/        # 编译器配置（gcc/riscv-gcc）
│       │   └── subsystem/       # 子系统模板
│       ├── toolchain/           # 工具链定义
│       │   ├── gcc/             # arm-none-eabi-gcc
│       │   └── riscv/           # riscv-none-elf-gcc
│       └── components/          # 组件构建脚本
├── device/                         # 设备相关
│   ├── board/                    # 单板配置
│   │   └── <vendor>/<board>/
│   │       └── liteos_m/
│   │           └── config.gni
│   └── soc/                      # SoC配置
│       └── <vendor>/<soc>/
│           ├── config.gni
│           └── ld/
│               └── linker.ld      # MCU级链接脚本
├── vendor/                         # ⭐ 产品定义（Lite格式）
│   └── <vendor>/<product>/
│       └── config.json            # 产品配置（子系统+部件）
├── kernel/                         # 内核源码
│   ├── liteos_m/                 # ⭐ LiteOS-M内核（L0轻量系统）
│   │   ├── arch/                # CPU架构相关（arm/risc-v）
│   │   ├── kernel/              # 内核核心
│   │   ├── utils/               # 内核工具
│   │   └── kal/                 # 内核抽象层（CMSIS/POSIX）
│   └── liteos_a/                 # ⭐ LiteOS-A内核（L1小型系统）
└── drivers/
    └── lite/                     # ⭐ 轻量系统驱动（IoT外设子系统）
```

> ⚠️ **注意**：Lite系统**不使用**以下标准系统目录：
> - `build/ohos/` — 标准系统构建配置
> - `productdefine/common/inherit/*.json` — 标准系统继承配置
> - `kernel/linux/` — Linux内核
> - `device/board/<vendor>/<board>/linux/` — 标准系统单板配置

## 4. 核心配置文件详解

### 4.1 BUILDCONFIG.gn 顶层配置

**文件位置**: `build/lite/config/BUILDCONFIG.gn`

**作用**: 整个构建系统的入口点，负责加载所有基础配置

```gn
# build/lite/config/BUILDCONFIG.gn 示例（Lite系统专用）

# 导入产品配置（Lite格式：vendor/<vendor>/<product>/config.json）
import("//vendor/${device_company}/${product_name}/config.json")

# 导入单板和SoC配置
import("//device/board/${board_company}/${board_name}/liteos_m/config.gni")
import("//device/soc/${soc_company}/${soc_name}/config.gni")

# 设置默认工具链（GCC为主）
if (toolchain == "") {
  if (board_arch == "riscv") {
    toolchain = "//build/lite/toolchain/riscv"
  } else {
    toolchain = "//build/lite/toolchain/gcc"
  }
}

# 设置目标CPU架构
if (target_cpu == "") {
  target_cpu = board_cpu
}

# 设置系统类型（mini 或 small：mini=L0 轻量 / small=L1 小型）
system_type = "mini"  # mini=L0 轻量 / small=L1 小型

# 导入编译器配置
import("//build/lite/config/compiler/compiler.gni")

# 导入子系统构建模板
import("//build/lite/config/subsystem/lite_subsystem.gni")

# 设置全局编译选项（嵌入式优化）
default_compiler_flags = [
  "-Wall",
  "-Werror",
  "-fno-strict-aliasing",
  "-ffunction-sections",   # 每个函数独立段，便于--gc-sections裁剪
  "-fdata-sections",       # 每个数据独立段
]

# L0 轻量系统（mini）始终使用体积优化
if (system_type == "mini") {
  default_compiler_flags += [ "-Os" ]     # MCU级芯片优先体积优化
} else {
  default_compiler_flags += [ "-O2" ]     # 小型系统平衡性能和大小
}
```

### 4.2 config.gni 芯片/单板配置

**文件位置**: `device/board/<vendor>/<board>/liteos_m/config.gni`

**作用**: 定义单板和SoC的具体参数

```gn
# device/board/mycompany/smart_sensor/liteos_m/config.gni

# ==================== 基础信息 ====================
board_name = "smart_sensor"
board_company = "mycompany"
soc_name = "stm32f407"
soc_company = "st"

# ==================== CPU架构配置 ====================
board_cpu = "cortex-m4"
board_arch = "arm"
board_fpu = "fpv4-sp-d16"        # FPU类型
board_float_abi = "hard"          # 硬浮点ABI

# ==================== 内存布局 ====================
board_flash_base = 0x08000000
board_flash_size = 0x100000       # 1MB
board_ram_base = 0x20000000
board_ram_size = 0x30000          # 192KB

# ==================== 内核配置 ====================
kernel_type = "liteos_m"
kernel_version = "3.1.0"

# ==================== 工具链选择 ====================
# 可选: "gcc", "llvm", "iar", "keil"
toolchain = "gcc"

# GCC工具链路径（如果使用自定义工具链）
gcc_toolchain_path = "/opt/gcc-arm-none-eabi-10.3/bin/"

# ==================== 外设使能 ====================
enable_uart = true
enable_spi = true
enable_i2c = true
enable_gpio = true
enable_adc = true
enable_pwm = true
enable_dma = true

# ==================== 调试配置 ====================
enable_debug = true
debug_level = 2                   # 0:无, 1:错误, 2:警告, 3:信息
enable_printf = true
enable_backtrace = false          # 小内存设备通常禁用

# ==================== 电源管理 ====================
enable_low_power = true
tickless_idle = true
```

### 4.3 product.json 产品定义

**文件位置**: `vendor/<vendor>/<product>/config.json`

**作用**: 定义产品的子系统和部件组成（Lite格式，不使用inherit继承机制）

```json
{
  "product_name": "smart_sensor",
  "version": "3.0",
  "type": "lite",
  "ohos_version": "OpenHarmony 3.1",
  "device_company": "mycompany",
  "board_company": "mycompany",
  "kernel_type": "liteos_m",
  "kernel_version": "3.1.0",
  "subsystems": [
    {
      "subsystem": "kernel",
      "components": [
        {
          "component": "liteos_m",
          "features": []
        }
      ]
    },
    {
      "subsystem": "drivers",
      "components": [
        {
          "component": "driver_gpio",
          "features": []
        },
        {
          "component": "driver_uart",
          "features": []
        },
        {
          "component": "driver_i2c",
          "features": []
        }
      ]
    },
    {
      "subsystem": "utils",
      "components": [
        {
          "component": "utils_base",
          "features": []
        }
      ]
    },
    {
      "subsystem": "iot_peripheral",
      "components": [
        {
          "component": "iot_controller",
          "features": []
        }
      ]
    }
  ]
}
```

### 4.4 BUILD.gn 模块构建定义

#### 4.4.1 内核模块BUILD.gn

```gn
# kernel/liteos_m/BUILD.gn

import("//build/lite/config/subsystem/lite_subsystem.gni")
import("//device/board/${board_company}/${board_name}/liteos_m/config.gni")

lite_subsystem("kernel") {
  subsystem_components = [
    "//kernel/liteos_m/kernel:modules",
    "//kernel/liteos_m/utils:utils",
    "//kernel/liteos_m/kal/cmsis:cmsis",
  ]
  
  if (enable_backtrace) {
    subsystem_components += [ "//kernel/liteos_m/debug:backtrace" ]
  }
}

# 内核核心模块
group("modules") {
  deps = [
    ":arch",
    ":base",
    ":extended",
  ]
}

static_library("arch") {
  sources = [
    "arch/arm/cortex-m4/gcc/los_dispatch.S",
    "arch/arm/cortex-m4/gcc/los_interrupt.c",
    "arch/arm/cortex-m4/gcc/los_context.c",
  ]
  
  include_dirs = [
    "arch/arm/cortex-m4/gcc",
    "arch/include",
    "include",
  ]
  
  cflags = [
    "-mcpu=${board_cpu}",
    "-mfloat-abi=${board_float_abi}",
    "-mfpu=${board_fpu}",
  ]
}
```

#### 4.4.2 驱动模块BUILD.gn（IoT外设子系统方式）

```gn
# drivers/lite/gpio/BUILD.gn — L0轻量系统使用IoT外设驱动子系统

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
  
  public_configs = [ ":gpio_public_config" ]
}

config("gpio_public_config") {
  include_dirs = [ "include" ]
}

lite_component("driver_gpio") {
  features = [
    ":gpio_driver",
  ]
}
```

> ⚠️ **关键区别**：L0轻量系统的驱动采用**IoT外设驱动子系统**方式，通过`static_library`+`lite_component`组织，不使用完整HDF框架的`hdf_driver()`模板。L1小型系统可使用精简版HDF。

#### 4.4.3 应用模块BUILD.gn

```gn
# applications/sample/wifi_iot/BUILD.gn

import("//build/lite/config/component/lite_component.gni")

executable("hello_world") {
  sources = [
    "src/main.c",
    "src/hello.c",
  ]
  
  include_dirs = [
    "include",
    "//utils/native/lite/include",
    "//kernel/liteos_m/utils",
  ]
  
  deps = [
    "//kernel/liteos_m/utils:utils",
    "//drivers/peripheral/uart:uart_driver",
  ]
  
  # 链接选项
  ldflags = [
    "-T//device/soc/st/stm32f407/ld/linker.ld",
    "-nostdlib",
    "-lgcc",
  ]
}

lite_component("hello_app") {
  features = [
    ":hello_world",
  ]
}
```

## 5. Lite系统两种类型的构建差异（L0 + L1）

### 5.1 对比总览

| 特性 | L0 轻量系统 (Mini) | L1 小型系统 (Small) |
|------|-------------------|-------------------|
| **内核** | LiteOS-M | LiteOS-A |
| **最小内存** | 128 KB | 1 MB |
| **处理器** | Cortex-M / RISC-V MCU | Cortex-A MPU |
| **典型芯片** | Hi3861, STM32F407, BES2600W, XR806, ESP32-C3 | Hi3516DV300, Hi3518, 全志T507, STM32MP1 |
| **构建系统** | build_lite (GN + Ninja) | build_lite (GN + Ninja) |
| **工具链** | arm-none-eabi-gcc / riscv-none-elf-gcc | arm-none-eabi-gcc / LLVM(可选) |
| **C库** | Newlib-nano / Musl-lite | Musl |
| **文件系统** | 无 / LittleFS / FAT（可选） | VFS / JFFS2 / LittleFS |
| **动态链接** | ❌ 不支持 | ⚠️ 部分支持 |
| **驱动框架** | IoT外设驱动子系统 | 精简版HDF |
| **图形UI** | 无 / 简易GUI | Lite UI |
| **优化重点** | 极致代码密度(-Os/-Oz) | 平衡性能和大小(-O2) |

### 5.2 L0轻量系统构建特点

#### 配置重点
- **极致代码密度**：使用`-Os`或`-Oz`优化，禁用不必要的特性
- **静态链接**：所有代码静态链接为单一固件镜像
- **最小依赖**：仅包含必要的内核和IoT外设驱动
- **自定义启动**：需要芯片特定的启动代码（startup.S）和MCU级链接脚本（linker.ld）
- **Thumb指令集**：ARM Cortex-M默认使用`-mthumb`减少代码大小
- **段裁剪**：`-ffunction-sections -fdata-sections` + `--gc-sections`移除未使用代码
- **Newlib-nano**：使用`--specs=nano.specs`减小C库体积

#### 典型构建配置（ARM Cortex-M）
```gn
# L0轻量系统专用编译选项（ARM Cortex-M系列，system_type="mini"）
if (system_type == "mini") {
  cflags_c = [
    "-mcpu=${board_cpu}",           # 如 cortex-m4, cortex-m33
    "-mthumb",                      # Thumb指令集减少代码大小
    "-mfloat-abi=${board_float_abi}", # hard/soft浮点ABI
    "-mfpu=${board_fpu}",           # FPU类型（如fpv4-sp-d16）
    "-Os",                          # 体积优化
    "-ffunction-sections",          # 每个函数独立段，便于裁剪
    "-fdata-sections",              # 每个数据独立段
    "-fno-common",                  # 禁止未初始化变量的common段
    "-specs=nano.specs",            # 使用newlib-nano减小体积
    "-specs=nosys.specs",           # 不使用系统调用
  ]
  
  ldflags = [
    "-Wl,--gc-sections",            # 移除未使用的段
    "-Wl,--print-memory-usage",     # 打印内存使用情况
    "-nostartfiles",                # 不使用标准启动文件
    "-T${linker_script}",           # 指定MCU级链接脚本
  ]
}
```

#### 典型构建配置（RISC-V）
```gn
# L0轻量系统专用编译选项（RISC-V MCU，system_type="mini"）
if (system_type == "mini" && board_arch == "riscv") {
  cflags_c = [
    "-march=${board_march}",        # 如 rv32imac, rv32imc
    "-mabi=${board_mabi}",          # 如 ilp32, ilp32e
    "-Os",
    "-ffunction-sections",
    "-fdata-sections",
    "-fno-common",
    "-mcmodel=medlow",              # RISC-V代码模型
  ]
  
  ldflags = [
    "-Wl,--gc-sections",
    "-Wl,--print-memory-usage",
    "-nostartfiles",
    "-T${linker_script}",
  ]
}
```

### 5.3 L1小型系统构建特点

#### 配置重点
- **平衡性能和大小**：使用`-O2`优化
- **支持动态库**：可以加载共享库（部分支持）
- **精简版HDF框架**：支持HDF驱动模型（精简版，非完整HDF）
- **用户空间隔离**：区分内核空间和用户空间
- **LiteOS-A内核**：编译路径为`kernel/liteos_a/`

#### 典型构建配置
```gn
# L1小型系统专用编译选项（ARM Cortex-A系列）
if (system_type == "small") {
  cflags_c = [
    "-mcpu=${board_cpu}",          # 如 cortex-a7, cortex-a53
    "-O2",                         # 平衡优化
    "-fPIC",                       # 位置无关代码（支持动态库）
    "-ffunction-sections",
    "-fdata-sections",
  ]
  
  # 用户空间和内核空间使用不同的编译选项
  if (is_user_space) {
    cflags_c += [ "-DUSER_SPACE" ]
  } else {
    cflags_c += [ "-DKERNEL_SPACE" ]
  }
}
```

## 6. 工具链配置（Lite系统以GCC为主）

### 6.1 ARM GCC工具链（L0/L1主要工具链）
```gn
# build/lite/toolchain/gcc/BUILD.gn
toolchain("gcc") {
  prefix = "arm-none-eabi-"       # ⭐ ARM嵌入式GCC，非标准系统的LLVM clang
  
  cc = "${prefix}gcc"
  cxx = "${prefix}g++"
  ar = "${prefix}ar"
  ld = "${prefix}ld"
  strip = "${prefix}strip"
  nm = "${prefix}nm"
  objcopy = "${prefix}objcopy"
  size = "${prefix}size"          # 用于检查固件大小
  
  toolchain_args = {
    current_os = "liteos_m"
    current_cpu = target_cpu
  }
}
```

### 6.2 RISC-V GCC工具链（L0 RISC-V芯片）
```gn
# build/lite/toolchain/riscv/BUILD.gn
toolchain("riscv_gcc") {
  prefix = "riscv-none-elf-"      # ⭐ RISC-V嵌入式GCC
  
  cc = "${prefix}gcc"
  cxx = "${prefix}g++"
  ar = "${prefix}ar"
  ld = "${prefix}ld"
  strip = "${prefix}strip"
  nm = "${prefix}nm"
  objcopy = "${prefix}objcopy"
  size = "${prefix}size"
  
  toolchain_args = {
    current_os = "liteos_m"
    current_cpu = target_cpu
  }
}
```

### 6.3 LLVM工具链（可选，主要用于L1）
```gn
# build/lite/toolchain/clang/BUILD.gn — 仅作为可选项
toolchain("clang") {
  cc = "clang"
  cxx = "clang++"
  ar = "llvm-ar"
  ld = "lld"
  
  if (target_cpu == "arm") {
    target_triple = "arm-none-eabi"
  } else if (target_cpu == "riscv32") {
    target_triple = "riscv32-none-elf"
  }
  
  toolchain_args = {
    current_os = "liteos_m"
    current_cpu = target_cpu
  }
}
```

## 7. 常见编译错误及修复方案

### 7.1 GN阶段错误

| 错误类型 | 错误信息 | 原因 | 修复方案 |
|---------|---------|------|---------|
| **语法错误** | `ERROR Expected a newline or eof` | 缺少换行符或文件末尾格式问题 | 运行`gn format`自动格式化 |
| **未定义变量** | `Undefined variable: board_cpu` | 变量在使用前未定义或未导入 | 检查import语句，确认变量已在config.gni中定义 |
| **导入失败** | `Can't load input file` | import路径错误或文件不存在 | 验证路径是否正确，使用`//`表示根目录 |
| **循环依赖** | `Dependency cycle detected` | 配置文件互相导入 | 重构配置，消除循环引用 |
| **类型错误** | `Expected string but got int` | 变量类型不匹配 | 使用字符串转换或修正赋值类型 |

### 7.2 Ninja编译阶段错误

| 错误类型 | 错误信息 | 原因 | 修复方案 |
|---------|---------|------|---------|
| **头文件缺失** | `fatal error: xxx.h: No such file` | include_dirs配置不完整 | 添加缺失的头文件搜索路径 |
| **符号未定义** | `undefined reference to 'xxx'` | 缺少库链接或源文件 | 在deps中添加缺失的库或模块 |
| **重定义** | `multiple definition of 'xxx'` | 同一符号在多个文件中定义 | 使用extern声明，保留唯一定义 |
| **内存溢出** | `region 'RAM' overflowed` | 代码/数据超出RAM容量 | 优化代码大小、减少缓冲区、增大RAM（如可能） |
| **对齐错误** | `misaligned pointer dereference` | 数据结构对齐不正确 | 使用`__attribute__((aligned))`或#pragma pack |

### 7.3 链接阶段错误

| 错误类型 | 错误信息 | 原因 | 修复方案 |
|---------|---------|------|---------|
| **段溢出** | `section .text will not fit in region 'FLASH'` | 代码超出Flash容量 | 启用LTO、使用-Os、裁剪未用功能 |
| **入口点缺失** | `undefined reference to 'Reset_Handler'` | 启动代码未链接 | 确认startup.S在链接列表中且符号名正确 |
| **向量表位置错误** | Hard Fault at boot | 向量表不在Flash起始位置 | 检查链接脚本.vectors段的位置 |
| **BSS初始化失败** | 变量值异常 | BSS段未正确清零 | 检查启动代码中BSS清零逻辑 |
| **栈溢出** | Hard Fault during runtime | 栈空间不足或递归过深 | 增大栈大小、优化递归、检查局部变量大小 |

### 7.4 运行时错误（配置相关）

| 错误类型 | 现象 | 原因 | 修复方案 |
|---------|------|------|---------|
| **Hard Fault** | 启动后立即崩溃 | 内存映射错误、时钟未初始化 | 检查链接脚本、验证时钟配置 |
| **外设不工作** | UART/GPIO无响应 | 引脚复用未配置、时钟未使能 | 检查config.gni中的外设配置 |
| **中断不触发** | 中断服务程序未执行 | NVIC优先级配置错误、向量表偏移 | 检查中断控制器配置 |
| **DMA传输失败** | 数据传输不完整 | DMA通道冲突、对齐问题 | 检查DMA通道分配和数据对齐 |

## 8. GN语法速查

### 8.1 基本数据类型

```gn
# 布尔值
enable_feature = true

# 字符串
name = "my_module"

# 整数
count = 42

# 列表
sources = [ "main.c", "utils.c" ]

# 范围（Scope）
config("my_config") {
  include_dirs = [ "include" ]
}
```

### 8.2 常用内置函数

```gn
# 导入文件
import("//build/lite/config/config.gni")

# 条件判断
if (target_cpu == "arm") { ... }

# 字符串操作
basename = get_path_info(source, "name")
dirname = get_path_info(source, "dir")

# 列表操作
sources += [ "extra.c" ]
sources -= [ "unused.c" ]

# 打印调试信息
print("Building for: ", target_cpu)
```

### 8.3 常用构建规则

```gn
# 可执行文件
executable("my_app") {
  sources = [ "main.c" ]
  deps = [ "//lib:mylib" ]
}

# 静态库
static_library("mylib") {
  sources = [ "lib.c" ]
  public = [ "include/lib.h" ]
}

# 共享库（仅小型/标准系统）
shared_library("myso") {
  sources = [ "lib.c" ]
}

# 分组（虚拟目标）
group("all") {
  deps = [ ":app", ":lib" ]
}

# 配置
config("my_config") {
  include_dirs = [ "include" ]
  defines = [ "DEBUG=1" ]
  cflags = [ "-Wall" ]
}
```

## 9. 配置检查清单

### 9.1 移植前检查

- [ ] 芯片数据手册已获取并阅读
- [ ] 内存映射（Flash/RAM地址和大小）已确认
- [ ] 时钟树结构和频率已明确
- [ ] 外设基地址和中断号已整理
- [ ] 开发板和调试器已准备
- [ ] 交叉编译工具链已安装并验证

### 9.2 配置生成后检查

- [ ] config.gni中所有变量已正确赋值
- [ ] 链接脚本内存区域与芯片手册一致
- [ ] 启动代码的向量表地址正确
- [ ] product.json中所有部件名称拼写正确
- [ ] BUILD.gn中的include路径都存在
- [ ] 编译选项与芯片架构匹配

### 9.3 编译验证检查

- [ ] `gn gen`成功无报错
- [ ] `ninja`编译通过无错误
- [ ] 生成的镜像大小在预期范围内
- [ ] 烧录后能正常启动
- [ ] 基本外设功能验证通过
- [ ] 内存使用在安全范围内
