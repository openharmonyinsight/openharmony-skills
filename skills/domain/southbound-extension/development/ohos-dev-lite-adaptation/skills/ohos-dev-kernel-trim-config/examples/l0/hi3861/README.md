# L0 Sample: Hi3861V100 (HiSpark WiFi IoT) — LiteOS-M 内核裁剪配置

来源：resources/target-config-samples/（原始：device_soc_hisilicon）+ resources/los-config-samples/（原始：kernel_liteos_m）

| 文件 | 说明 |
|------|------|
| `hi3861v100_target_config.h` | Hi3861 L0 芯片真实 target_config.h：展示 LOSCFG_* 裁剪宏的标准写法、内核特性开关、外设配置项 |
| `los_config.h` | LiteOS-M 内核标准配置头文件：展示完整的 LOSCFG_* 宏命名约定、默认值、依赖关系 |

**展示的裁剪相关模式**：
- L0：`LOSCFG_BASE_CORE_*` / `LOSCFG_BASE_IPC_*` / `LOSCFG_KERNEL_*` — target_config.h 中的宏开关
- L1 子系统级裁剪示例见 `examples/l1/hi3516dv300/`
