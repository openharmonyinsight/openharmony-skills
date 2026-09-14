# ARM Cortex-A Sample: Hi3516DV300

**芯片**: Hi3516DV300 (Cortex-A7, L1 小型系统)
**产品**: `hispark_taurus_linux`（device_company=hisilicon, board=hispark_taurus）
**内核**: Linux 4.19（kernel_is_prebuilt=false，内核源码参与构建，由 SoC BUILD.gn 的 `//kernel/linux/build:linux_kernel` 编译）
**存储**: eMMC

## 文件清单（对应 SKILL.md Step 3 的 8 文件工作流）

文件名前缀标注归属层级（实际源码树中文件名仅为 `BUILD.gn`，此处加前缀仅为在样本目录内区分三级）：

| 样本文件 | 实际路径 | 层级 | 用途 |
|---------|---------|------|------|
| `config.gni` | `device/board/hisilicon/hispark_taurus/liteos_a/config.gni` | Board | 构建变量（构建入口） |
| `board-BUILD.gn` | `device/board/hisilicon/hispark_taurus/BUILD.gn` | Board | Board 构建入口 |
| `BUILD.gn` | `device/soc/hisilicon/hi3516dv300/BUILD.gn` | SoC | SoC 构建入口（壳 + SDK 接入点，含 linux_kernel 依赖） |
| `config.json` | `vendor/hisilicon/hispark_taurus_linux/config.json` | Product | 产品定义（完整 schema，type=small=L1 小型） |
| `ohos.build` | `vendor/hisilicon/hispark_taurus_linux/ohos.build` | Product | 部件/子系统注册 |
| `vendor-BUILD.gn` | `vendor/hisilicon/hispark_taurus_linux/BUILD.gn` | Product | 产品构建 target |
| `hals-BUILD.gn` | `vendor/hisilicon/hispark_taurus_linux/hals/BUILD.gn` | Product | HAL 适配目录占位 |

> L1 小型系统（Cortex-A + Linux）**不使用 MCU 级链接脚本**：Linux 内核有自己的链接脚本（`arch/arm/boot/` 下），用户空间应用由内核加载。只有 L0 轻量系统（Cortex-M / RISC-V MCU）才需要手动编写 linker.ld，故本样本无 linker.ld。

## 关键适配要点

- `kernel_type = "linux"` — L1 小型系统使用 Linux 内核（与 config.json 一致）
- `board_cpu = "cortex-a7"` — Cortex-A 系列 CPU
- `board_toolchain_type = "clang"` — L1 默认使用 Clang 工具链（L0 默认 GCC）
- `board_cflags` 中 `-mfpu=neon-vfpv4` — Cortex-A 使用 NEON SIMD 扩展
- `storage_type = "emmc"` — L1 通常使用 eMMC 而非 SPI Flash
- config.json 为 `type = "small"` 完整 schema，subsystems 比 L0 更丰富（含 hdf、arkui、multimedia 等）；Linux 内核不经 "kernel" 子系统装配，而由 SoC BUILD.gn 编译

## 适配你的 Cortex-A 芯片

1. 修改 `kernel_type` 和 `kernel_version` 匹配你的内核
2. 修改 `board_cpu` 为你的核心类型（如 cortex-a53、cortex-a55）
3. 如果使用 LiteOS-A 而非 Linux，改 `kernel_type = "liteos_a"`，并在 config.json subsystems 中加 `kernel`/`liteos_a`
4. config.json 改为你的 product_name/device_company/board，subsystems 按目标功能增减（参考 references/config-json-guide.md）
5. ohos.build 的 part 名改为 `product_` + 你的 product_name，module_list target 名与 vendor BUILD.gn 的 group 名一致
