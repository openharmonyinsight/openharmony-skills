# L1 Sample: STM32MP1 HDF GPIO Driver

来源：ohos-lite-helper MCP 域 `hal-driver`（device_soc_st）

| 文件 | 说明 |
|------|------|
| `stm32mp1_gpio.c` | L1 GPIO 驱动：HdfDriverEntry + Bind/Init/Release + OSAL 寄存器操作 + 中断处理 |
| `stm32mp1_gpio.h` | L1 GPIO 驱动头文件：Device 结构体（OSAL 句柄）、寄存器偏移宏、函数声明 |

**展示的 L1 模式**：
- `HdfDriverEntry` 结构体（`.Bind` / `.Init` / `.Release`）+ `HDF_INIT` 宏（Dispatch 通过 `IDeviceIoService` 在 Bind 中设置）
- `Bind` 返回 `HdfDeviceObject` service → `Init` 中注册 GpioMethod → `Release` 中释放
- OSAL 封装寄存器操作：`OSAL_READL(addr)` / `OSAL_WRITEL(addr, val)`
- OsalSpinLock + OsalIrq 中断处理
- HDF_LOGE / HDF_LOGI 日志宏
