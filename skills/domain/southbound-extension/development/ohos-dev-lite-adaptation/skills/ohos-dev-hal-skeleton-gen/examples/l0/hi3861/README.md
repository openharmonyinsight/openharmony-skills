# L0 Sample: Hi3861 IoT Peripheral Driver Subsystem

来源：ohos-lite-helper MCP 域 `hal-driver`（openharmony-output-samples）

| 文件 | 说明 |
|------|------|
| `hi3861_hal_iot_gpio.c` | L0 GPIO 驱动：实现 `iot_gpio.h` IoT API，封装 Hi3861 厂商 HAL（`hi_gpio.h`） |
| `hi3861_hal_iot_uart.c` | L0 UART 驱动：实现 `iot_uart.h` IoT API，封装 Hi3861 厂商 HAL（`hi_uart.h`） |

**展示的 L0 模式**：
- IoT API 适配层：实现标准 `IoTGpioInit` / `IoTUartInit` 等接口，内部调用厂商 HAL（`hi_gpio_*` / `hi_uart_*`）
- L0 不使用 HDF 框架（无 HdfDriverEntry / HCS / OSAL），直接函数调用
- L0 不使用 GpioMethod / GpioCntlrAdd（那是 L1 HDF 核心层机制）
- 另一种 L0 注册方式见 `references/driver-code-templates.md` §L0（GpioOperations + GpioRegisterOps 组件化注册）
