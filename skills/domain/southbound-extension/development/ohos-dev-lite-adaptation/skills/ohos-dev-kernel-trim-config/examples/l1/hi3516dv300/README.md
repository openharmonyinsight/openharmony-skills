# L1 Sample: Hi3516DV300 — LiteOS-A 内核裁剪配置

来源：resources/target-config-samples/（原始：device_soc_hisilicon）

| 文件 | 说明 |
|------|------|
| `hi3516dv300_board_config.gni` | Hi3516DV300 L1 板级 config.gni：展示 `board_arch` / `board_toolchain` / `board_cflags` 等内核构建变量与裁剪的关系 |
| `hi3516dv300_config.json` | Hi3516DV300 L1 产品定义 JSON：展示 `subsystems` + `components` 列表中与内核裁剪相关的子系统选择（kernel_liteos_a / hdf / drivers 等） |

**展示的裁剪相关模式**：
- L1：config.json 中子系统/部件级别的裁剪选择 — 决定哪些子系统参与编译
- L0 宏级裁剪示例见 `examples/l0/hi3861/`
