> **Scope**: config.gni 变量清单与填充指南
> **When**: 需要生成 Board 级或 SoC 级 config.gni 时读取
> **Size**: ~120 lines

---

## SoC config.gni vs Board config.gni

OpenHarmony Lite 构建入口是 **Board 级 config.gni**：

```
device/board/<vendor>/<board>/liteos_m/config.gni   ← hb 装配的 Board 级入口（必须）
device/soc/<vendor>/<soc>/config.gni                 ← SoC 级（可选）
```

- **Board 级**：定义板级参数（内核类型、CPU、工具链、编译选项等），hb 装配时首先加载此文件
- **SoC 级**：仅当多块板共享同一 SoC 时才有意义，Board 级通过 `import()` 引用 SoC 级变量
- **简单芯片（单板）**：只需 Board 级 config.gni，所有变量集中在一个文件中
- **多板共享 SoC**：SoC 级放共用变量（如 `soc_name`、内存映射），Board 级放板级差异（如外设配置）

## 变量清单（按 Section 组织）

### 基础信息

| 变量 | 类型 | 说明 |
|------|------|------|
| `kernel_type` | string | 内核类型。L0 填 `"liteos_m"` 或 `"uniproton"`；L1 填 `"liteos_a"` 或 `"linux"` |
| `kernel_version` | string | 内核版本号，如 `"3.0.0"` |
| `board_cpu` | string | CPU 核心类型，如 `"cortex-m4"`、`"cortex-a7"`、`"riscv32"` |
| `board_arch` | string | 架构标识，如 `"arm"`、`"rv32imac"`。ARM Cortex-M 可留空 |

**真实示例**：
- STM32F407：`kernel_type = "uniproton"`, `board_cpu = "cortex-m4"`, `board_arch = ""`
- Hi3861：`kernel_type = "liteos_m"`, `board_cpu = ""`, `board_arch = "rv32imac"`

### 工具链

| 变量 | 类型 | 说明 |
|------|------|------|
| `board_toolchain` | string | 工具链名称。ARM: `"arm-none-eabi-gcc"`；RISC-V: `"riscv32-unknown-elf"` |
| `board_toolchain_path` | string | 工具链安装路径。已加入 PATH 则留空 `""` |
| `board_toolchain_prefix` | string | 编译器前缀。ARM: `"arm-none-eabi-"`；RISC-V: `"riscv32-unknown-elf-"` |
| `board_toolchain_type` | string | 编译器类型：`"gcc"` 或 `"clang"` |
| `use_board_toolchain` | bool | 是否强制使用 board_toolchain（可选，默认不设置） |

### march/mabi 三处一致性（防 ABI 不兼容 / 链接失败）

架构参数必须三处完全一致，否则工具链编出的目标文件与 GN 期望的 ABI 不匹配，链接期出现乱码符号或 undefined reference：

1. **来源**：厂商 SDK / 工具链文档声明的 march/mabi（从 SDK 提取，不凭经验填）
2. **config.gni**：`board_arch` + `board_cflags` 里的 `-march`/`-mabi`/`-mcpu`
3. **BUILD.gn**：import config.gni 自动继承；若 SoC/Board BUILD.gn 单独写 cflags，必须与 config.gni 一致

#### RISC-V 陷阱：不支持 -mcpu

RISC-V GCC 工具链（如 `riscv32-unknown-elf-`）**不接受 `-mcpu`**。ARM 用 `-mcpu=cortex-m4`，RISC-V 必须改用 `-march` + `-mabi`：

```gn
# RISC-V（Hi3861 / rv32imac）
board_cpu = ""                          # RISC-V 留空，不用 -mcpu
board_arch = "rv32imac"
board_cflags = [
  "-march=rv32imac",
  "-mabi=ilp32",
  # ...
]
```

对照 ARM（Cortex-M4）：

```gn
board_cpu = "cortex-m4"
board_cflags = [ "-mcpu=cortex-m4", "-mthumb", ... ]   # ARM 用 -mcpu，无此陷阱
```

#### D 扩展判定

CPU 名含 `fd`/`fdp` → march 含 `d`、mabi=`ilp32d`；仅含 `f` → march 不含 `d`、mabi=`ilp32f`。填错导致硬浮点符号缺失。

### 编译选项（board_cflags）

`board_cflags` 是传递给 C 编译器的标志列表。典型组成：

```gn
board_cflags = [
  # 1. CPU 架构标志（必须与 board_cpu 一致）
  "-mcpu=cortex-m4",           # ARM 架构
  # 或 "-mabi=ilp32",          # RISC-V 架构
  #    "-march=rv32imac",

  # 2. 优化和代码生成标志
  "-fno-common",
  "-fdata-sections",
  "-ffunction-sections",
  "-mthumb",                   # ARM Cortex-M Thumb 指令集
  "-O2",                       # 优化等级

  # 3. 浮点标志（ARM 有 FPU 的芯片）
  "-mfloat-abi=softfp",        # softfp 或 hard
  "-mfpu=vfpv4-d16",           # FPU 类型

  # 4. -D 宏定义（见下方说明）
  "-D__RTOS__",
  "-DSTM32F40XX",
]
```

#### -D 宏定义的来源

`board_cflags` 中的 `-D` 标志来自三个来源：

1. **芯片 SDK 头文件宏**：芯片厂商 SDK 中 `#ifdef` 依赖的宏。如 STM32 的 `-DSTM32F40XX`（选择正确的寄存器定义头文件），Hi3861 的 `-DCHIP_VER_Hi3861`
2. **RTOS 标识宏**：内核和适配层代码中用于区分操作系统的宏。如 `-D__RTOS__`、`-D__LITEOS__`、`-DCMSIS_OS_VER=2`
3. **产品特性开关**：启用或禁用特定功能的宏。如 `-DLOS_CONFIG_IPERF3`（启用 iperf3 测试）、`-DCONFIG_AT_COMMAND`（启用 AT 命令）

**确定方法**：查看芯片 SDK 的头文件和 Makefile，找出所有 `#ifdef` 条件宏；查看内核适配层代码中的 `#if defined()` 条件。

### board_asmflags / board_cxx_flags

- `board_asmflags`：汇编器标志，通常包含 CPU 架构标志（`-mcpu`、`-mfloat-abi`、`-mfpu`）
- `board_cxx_flags`：C++ 编译标志，通常直接赋值 `board_cxx_flags = board_cflags`

### board_ld_flags

链接器标志列表。通常留空 `[]`，链接脚本通过 BUILD.gn 中的 `ldflags` 指定。

### board_include_dirs

全局头文件搜索路径列表。包含：
- 内核头文件路径（如 `//kernel/liteos_m/kal/cmsis`）
- SoC SDK 头文件路径（如 `//device/soc/<vendor>/<soc>/sdk/include`）
- 第三方库路径（如 `//third_party/cmsis`）

**注意**：路径中 `//` 表示 OpenHarmony 源码根目录。Hi3861 使用 `${ohos_root_path}` 前缀，效果相同。

### board_adapter_dir

**含义**：指向 SoC HAL 适配目录，决定 KAL（Kernel Abstraction Layer）和 CMSIS 适配层的位置。

**设置方法**：
```gn
# 格式：//device/soc/<vendor>/<soc>/<adapter_subdir>
board_adapter_dir = "//device/soc/st/stm32f407zg/uniproton"
# Hi3861 示例：
board_adapter_dir = "//device/soc/hisilicon/hi3861v100/hi3861_adapter"
```

构建系统通过此路径查找内核适配层代码（CMSIS 接口实现、HAL 封装等）。如果路径错误，编译时会报找不到 `cmsis_os2.h` 等适配层头文件。

### 其他可选变量

| 变量 | 类型 | 说明 |
|------|------|------|
| `board_configed_sysroot` | string | Sysroot 路径，通常留空 `""` |
| `storage_type` | string | 存储类型：`"spinor"`（SPI Flash）、`"emmc"`、`""`（无文件系统） |
| `board_opt_flags` | list | Debug 编译优化标志（可选，用于覆盖默认优化等级） |

## 真实示例参考

本指南是变量清单与规则说明。如需参照真实芯片的 config.gni：
- 本 SKILL 的 `examples/l0/` 目录有 Hi3861 / STM32F407 的 config.gni 样本
- 也可在项目中搜索 `config.gni` 文件或联网查找对应芯片的 OpenHarmony 适配仓库

- `board-configs/hispark_pegasus_config.gni` — Hi3861（RISC-V，liteos_m）
- `soc-configs/hi3516_config.gni` — Hi3516（ARM Cortex-A7，linux）
- `soc-configs/stm32f407_config.gni` — STM32F407（ARM Cortex-M4，uniproton）

真实示例的 `board_cflags` 通常包含 30+ 行（含大量 `-D` 宏定义），比本指南示例更完整，适合参照。
