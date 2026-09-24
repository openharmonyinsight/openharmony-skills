# ARM Cortex-M Sample: STM32F407

**芯片**: STM32F407ZG (Cortex-M4, L0 轻量系统)
**产品**: `uniproton_stm32f407zg`（device_company=st, board=stm32f407zg）
**内核**: UniProton（OpenHarmony 第三方内核，可选 LiteOS-M；kernel_is_prebuilt=false，内核参与构建）
**Flash**: 1MB @ 0x08000000
**RAM**: 128KB @ 0x20000000

## 文件清单（对应 SKILL.md Step 3 的 8 文件工作流）

文件名前缀标注归属层级（实际源码树中文件名仅为 `BUILD.gn`，此处加前缀仅为在样本目录内区分三级）：

| 样本文件 | 实际路径 | 层级 | 用途 |
|---------|---------|------|------|
| `config.gni` | `device/board/st/stm32f407zg/liteos_m/config.gni` | Board | 构建变量（构建入口） |
| `board-BUILD.gn` | `device/board/st/stm32f407zg/BUILD.gn` | Board | Board 构建入口 |
| `BUILD.gn` | `device/soc/st/stm32f407zg/BUILD.gn` | SoC | SoC 构建入口（壳 + SDK 接入点） |
| `linker.ld` | `device/soc/st/stm32f407zg/ld/linker.ld` | SoC | 链接脚本（仅 L0） |
| `config.json` | `vendor/st/stm32f407zg/config.json` | Product | 产品定义（完整 schema） |
| `ohos.build` | `vendor/st/stm32f407zg/ohos.build` | Product | 部件/子系统注册 |
| `vendor-BUILD.gn` | `vendor/st/stm32f407zg/BUILD.gn` | Product | 产品构建 target |
| `hals-BUILD.gn` | `vendor/st/stm32f407zg/hals/BUILD.gn` | Product | HAL 适配目录占位 |

## 关键适配要点

- `kernel_type = "uniproton"` — UniProton 内核（与 config.json 一致；若用 LiteOS-M 改为 `"liteos_m"`）
- `board_cpu = "cortex-m4"` — CPU 核心类型，决定 `-mcpu` 编译标志
- `board_cflags` 中 `-mfloat-abi=softfp` + `-mfpu=vfpv4-d16` — FPU 配置，STM32F407 有单精度 FPU
- `-mthumb` — Cortex-M 必须使用 Thumb 指令集
- `-DSTM32F40XX` — 芯片 SDK 头文件宏，选择正确的寄存器定义
- `board_adapter_dir` 指向 `//device/soc/st/stm32f407zg/uniproton` — 内核适配层位置
- `storage_type = "spinor"` — SPI Flash 存储

## 适配你的 Cortex-M 芯片

1. 修改 `board_cpu` 为你的芯片核心（如 cortex-m33、cortex-m7）
2. 修改 FPU 标志（`-mfloat-abi`、`-mfpu`），无 FPU 的芯片删除这两行
3. 替换 `-D` 宏为你的芯片 SDK 要求的宏
4. 更新 `board_include_dirs` 为你的 SDK 头文件路径
5. linker.ld 中修改 Flash/RAM 地址和大小
6. config.json 改为你的 product_name/device_company/board，kernel_type 与 config.gni 一致
7. ohos.build 的 part 名改为 `product_` + 你的 product_name，module_list target 名与 vendor BUILD.gn 的 group 名一致
