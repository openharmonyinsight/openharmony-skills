# RISC-V Sample: Hi3861

**芯片**: Hi3861V100 (RISC-V rv32imac, L0 轻量系统)
**产品**: `wifiiot_hispark_pegasus`（device_company=hisilicon, board=hispark_pegasus）
**内核**: LiteOS-M（kernel_is_prebuilt=true，内核预编）
**Flash**: 2MB @ 0x00400000
**RAM**: 1MB @ 0x00100000 (FPGA) / 280KB @ 0x000d8000 (ASIC)

## 文件清单（对应 SKILL.md Step 3 的 8 文件工作流）

本样本为完整产品骨架，文件名后缀标注其归属层级与目标路径（实际源码树中文件名仅为 `BUILD.gn`，此处加 `board-`/`vendor-`/`hals-` 前缀仅为在样本目录内区分三级）：

| 样本文件 | 实际路径 | 层级 | 用途 |
|---------|---------|------|------|
| `config.gni` | `device/board/hisilicon/hispark_pegasus/liteos_m/config.gni` | Board | 构建变量（构建入口） |
| `board-BUILD.gn` | `device/board/hisilicon/hispark_pegasus/BUILD.gn` | Board | Board 构建入口（config.json device_build_path 指向） |
| `BUILD.gn` | `device/soc/hisilicon/hi3861v100/BUILD.gn` | SoC | SoC 构建入口（壳 + SDK 接入点） |
| `linker.ld` | `device/soc/hisilicon/hi3861v100/ld/linker.ld` | SoC | 链接脚本（仅 L0） |
| `config.json` | `vendor/hisilicon/hispark_pegasus/config.json` | Product | 产品定义（完整 schema，含元数据 + subsystems） |
| `ohos.build` | `vendor/hisilicon/hispark_pegasus/ohos.build` | Product | 部件/子系统注册（module_list → vendor BUILD.gn） |
| `vendor-BUILD.gn` | `vendor/hisilicon/hispark_pegasus/BUILD.gn` | Product | 产品构建 target（ohos.build module_list 指向） |
| `hals-BUILD.gn` | `vendor/hisilicon/hispark_pegasus/hals/BUILD.gn` | Product | HAL 适配目录占位（product_adapter_dir 指向） |

## 关键适配要点

- `board_arch = "rv32imac"` — RISC-V ISA 字符串，决定 `-march` 编译标志
- `board_toolchain = "riscv32-unknown-elf"` — RISC-V 工具链（非 ARM 的 arm-none-eabi）
- `board_cflags` 中 `-mabi=ilp32` — RISC-V ABI（整数+长整数都是 32 位）
- `-mcmodel=medlow` — RISC-V 代码模型（小内存用 medlow，>2GB 用 medany）
- `-D` 宏包含大量 Hi3861 特有定义：`-D__LITEOS__`、`-DCHIP_VER_Hi3861`、`-DHI_BOARD_ASIC` 等
- linker.ld 使用 ROM+RAM 混合布局（Hi3861 有片上 ROM），比通用 RISC-V 模板复杂
- `config.json` 的 `kernel_is_prebuilt = true`：Hi3861 SDK 用 scons 编译（见 SoC `BUILD.gn` 的 `sdk_liteos:run_wifiiot_scons`），内核不参与 GN 源码构建

## 适配你的 RISC-V 芯片

1. 修改 `board_arch` 为你的 ISA 字符串（如 rv32imc、rv32imafc）
2. 修改 `-mabi` 匹配 ISA（rv32imac → ilp32，rv32imafdc → ilp32d）
3. 简化 linker.ld 为通用 RISC-V 模板（参考 references/linker-templates.md），去掉 ROM 段
4. 替换 `-D` 宏为你的芯片 SDK 要求的宏
5. 更新 `board_include_dirs` 为你的 SDK 头文件路径
6. config.json 改为你的 product_name/device_company/board，subsystems 按目标功能选取（参考 references/config-json-guide.md）
7. ohos.build 的 part 名改为 `product_` + 你的 product_name，module_list target 名与 vendor BUILD.gn 的 group 名一致

## 关于 linker.ld 截取说明

原始 hi3861_link.ld.S 有 597 行，包含大量 `#ifdef` 条件编译和 ROM 段定义。本文件截取了 MEMORY 区域定义和核心 SECTIONS（.text/.data/.bss/.heap/.stack），控制在 100 行以内。适配简单 RISC-V 芯片时，建议使用 references/linker-templates.md 中的通用模板，而非直接复用此文件。
