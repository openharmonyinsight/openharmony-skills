# 方式 B：直接编译开源 LiteOS-M（kernel_is_prebuilt: false）

> **此样本演示"直接用开源 LiteOS-M"的构建配置**（方式 B）。
> 与方式 A（厂商预编译内核 + KAL 适配层）的区别：
> - `import("//kernel/liteos_m/liteos.gni")` —— 把开源内核源码拉入编译
> - `kernel_is_prebuilt: false`（或不填）—— OH 构建系统编译内核
> - **不需要 KAL 适配层** —— 内核原生提供 CMSIS-RTOS2 + POSIX
> - 板级只需提供 BSP（main.c + 硬件初始化 hooks + HAL 驱动）

## 参考来源
- QEMU esp32: `device/qemu/esp32/liteos_m/board/BUILD.gn`（最纯的方式 B 样本）
- rk2206/neptune100: `device/board/hihope/neptune100/liteos_m/BUILD.gn`（真实芯片，混合模式）

## 关键文件

| 文件 | 作用 |
|------|------|
| `BUILD.gn` | 板级构建入口，`import("//kernel/liteos_m/liteos.gni")` + `kernel_module("bsp_config")` |
| `config.json` | 产品配置，`kernel_is_prebuilt: false` |
| `main.c` | 板级入口（`LOS_KernelInit()` + 硬件初始化 hooks），**不是 startup_S.s** |

## 与方式 A 的 BUILD.gn 对比

| | 方式 B（本样本） | 方式 A（risc-v/Hi3861 样本） |
|---|---|---|
| kernel_is_prebuilt | false | true |
| BUILD.gn import | `import("//kernel/liteos_m/liteos.gni")` | 无（内核是预编译 .a） |
| kernel_module | `kernel_module("bsp_config") { sources = [main.c, hal_*.c] }` | 无（内核不参与编译） |
| KAL 适配层 | **不需要** | 需要 `*_adapter/kal/` |
| 启动代码 | `main.c`（`LOS_KernelInit()` + hooks） | `startup_S.s` + `system_init.c` |
