# Chip Spec Quick Reference

> From ohos-dev-soc-spec-parse/SKILL.md (C2 progressive disclosure)

## ③ 速查

### JSON Schema 核心字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| `metadata.vendor` | string | ✅ | 芯片厂商 |
| `metadata.chipName` | string | ✅ | 芯片型号 |
| `metadata.architecture` | enum | ✅ | ARM_Cortex_M / ARM_Cortex_A / RISC_V / Xtensa |
| `metadata.targetSystemLevel` | enum | ✅ | L0 / L1 |
| `cpu.coreType` | string | — | Cortex-M4F / Cortex-A7 / RV32IMAC |
| `cpu.fpu` | boolean | — | 是否有 FPU |
| `cpu.mmu` | boolean | — | 是否有 MMU |
| `memoryMap[]` | array | ✅ | 存储器映射（Flash/RAM/外设区） |
| `peripherals[]` | array | — | 外设列表（name/type/baseAddress/interrupts） |
| `interruptController.type` | enum | — | NVIC / GIC-400 / PLIC / CLINT |
| `clockSystem.clockSources[]` | array | — | 时钟源（HSI/HSE/PLL 等） |
| `clockSystem.peripheralClockGates[]` | array | — | 外设时钟门控映射 |
| `pinMux[]` | array | — | 引脚复用表 |
| `ddrVariant` | object | — | 内置 DDR 变体（variantSuffix/ddrType/ddrCapacity/packageType/xlsmFile/regInfoMagic），仅多变体 SoC |
| `fieldSources` | object | ✅ | 字段来源追溯（key=路径, value=来源） |

### 芯片分类速查

**系统级别**：

| 系统级别 | CPU 特征 | 代表芯片 | checklist 差异 |
|----------|---------|---------|---------------|
| **L0** | Cortex-M / RISC-V 无MMU | STM32F407 / Hi3861 / ESP32-C3 / BES2600W | 需要寄存器位域 |
| **L1** | Cortex-A / RISC-V 有MMU | Hi3516DV300 / 全志T507 | 不需要寄存器位域 |

**功能能力**（可叠加）：

| 功能能力 | 代表芯片 | 额外 checklist 项 |
|----------|---------|------------------|
| **WiFi/BLE** | ESP32-C3 / Hi3861 / XR806 / ASR582X | RF 校准/天线配置 |
| **视频处理** | Hi3516DV300 | ISP/MIPI CSI/视频编解码 |
| **通用** | STM32F407 / AT32F437 / 全志T507 | — |
| **内置 DDR 多变体** | Hi3516CV610 (-10B/-20S/-20G/-00S/-00G) | DDR 变体鉴别 → xlsm → reg_info（见 ddr-variant-guide.md） |
