# 各外设Method接口定义

> 来源：需求分析报告 §4.4

## GPIO — GpioMethod

```c
struct GpioMethod {
    int32_t (*Request)(struct GpioCntlr *cntlr, uint16_t gpio);
    int32_t (*Release)(struct GpioCntlr *cntlr, uint16_t gpio);
    int32_t (*SetDir)(struct GpioCntlr *cntlr, uint16_t gpio, uint16_t dir);
    int32_t (*GetDir)(struct GpioCntlr *cntlr, uint16_t gpio, uint16_t *dir);
    int32_t (*Write)(struct GpioCntlr *cntlr, uint16_t gpio, uint16_t val);
    int32_t (*Read)(struct GpioCntlr *cntlr, uint16_t gpio, uint16_t *val);
    int32_t (*SetIrq)(struct GpioCntlr *cntlr, uint16_t gpio, uint16_t mode);
    int32_t (*UnsetIrq)(struct GpioCntlr *cntlr, uint16_t gpio);
    int32_t (*EnableIrq)(struct GpioCntlr *cntlr, uint16_t gpio);
    int32_t (*DisableIrq)(struct GpioCntlr *cntlr, uint16_t gpio);
};
```

**核心层API**：`GpioCntlrAdd()`, `GpioCntlrRemove()`
**核心头文件**：`gpio_core.h`

## I2C — I2cMethod

```c
struct I2cMethod {
    int32_t (*Read)(struct I2cCntlr *cntlr, struct I2cMsg *msgs, int32_t count);
    int32_t (*Write)(struct I2cCntlr *cntlr, struct I2cMsg *msgs, int32_t count);
    int32_t (*SetConfig)(struct I2cCntlr *cntlr, struct I2cCfg *cfg);
    int32_t (*GetConfig)(struct I2cCntlr *cntlr, struct I2cCfg *cfg);
};
```

**核心层API**：`I2cCntlrAdd()`, `I2cCntlrRemove()`
**核心头文件**：`i2c_core.h`

## SPI — SpiMethod

```c
struct SpiMethod {
    int32_t (*Transfer)(struct SpiCntlr *cntlr, struct SpiMsg *msg);
    int32_t (*SetCfg)(struct SpiCntlr *cntlr, struct SpiCfg *cfg);
    int32_t (*GetCfg)(struct SpiCntlr *cntlr, struct SpiCfg *cfg);
};
```

**核心层API**：`SpiCntlrAdd()`, `SpiCntlrRemove()`
**核心头文件**：`spi_core.h`

## UART — UartHostMethod

```c
struct UartHostMethod {
    int32_t (*Init)(struct UartHost *host);
    int32_t (*Deinit)(struct UartHost *host);
    int32_t (*Read)(struct UartHost *host, uint8_t *data, uint32_t size);
    int32_t (*Write)(struct UartHost *host, uint8_t *data, uint32_t size);
    int32_t (*GetBaud)(struct UartHost *host, uint32_t *baudRate);
    int32_t (*SetBaud)(struct UartHost *host, uint32_t baudRate);
    int32_t (*GetAttribute)(struct UartHost *host, struct UartAttribute *attr);
    int32_t (*SetAttribute)(struct UartHost *host, struct UartAttribute *attr);
    int32_t (*SetTransMode)(struct UartHost *host, enum UartTransMode mode);
};
```

**核心层API**：`UartHostCreate()`, `UartHostDestroy()`
**核心头文件**：`uart_core.h`

## ADC — AdcMethod

```c
struct AdcMethod {
    int32_t (*Read)(struct AdcDevice *device, uint32_t channel, int32_t *val);
    int32_t (*Start)(struct AdcDevice *device);
    int32_t (*Stop)(struct AdcDevice *device);
};
```

**核心层API**：`AdcDeviceAdd()`, `AdcDeviceRemove()`
**核心头文件**：`adc_core.h`

## PWM — PwmMethod

```c
struct PwmMethod {
    int32_t (*SetConfig)(struct PwmDevice *device, struct PwmConfig *cfg);
    int32_t (*GetConfig)(struct PwmDevice *device, struct PwmConfig *cfg);
    int32_t (*Enable)(struct PwmDevice *device);
    int32_t (*Disable)(struct PwmDevice *device);
};
```

**核心层API**：`PwmCntlrAdd()`, `PwmCntlrRemove()`
**核心头文件**：`pwm_core.h`

## RTC — RtcMethod

```c
struct RtcMethod {
    int32_t (*ReadTime)(struct RtcHost *host, struct RtcTime *time);
    int32_t (*WriteTime)(struct RtcHost *host, const struct RtcTime *time);
    int32_t (*ReadAlarm)(struct RtcHost *host, struct RtcTime *alarm);
    int32_t (*WriteAlarm)(struct RtcHost *host, const struct RtcTime *alarm);
    int32_t (*RegisterAlarmInterrupt)(struct RtcHost *host, AlarmCallback cb);
    int32_t (*UnregisterAlarmInterrupt)(struct RtcHost *host);
    int32_t (*AlarmInterruptEnable)(struct RtcHost *host, uint8_t enable);
};
```

**核心层API**：`RtcHostCreate()`, `RtcHostDestroy()`
**核心头文件**：`rtc_core.h`

## Watchdog — WatchdogMethod

```c
struct WatchdogMethod {
    int32_t (*GetStatus)(struct WatchdogCntlr *cntlr, int32_t *status);
    int32_t (*Start)(struct WatchdogCntlr *cntlr);
    int32_t (*Stop)(struct WatchdogCntlr *cntlr);
    int32_t (*SetTimeout)(struct WatchdogCntlr *cntlr, uint32_t seconds);
    int32_t (*GetTimeout)(struct WatchdogCntlr *cntlr, uint32_t *seconds);
    int32_t (*Feed)(struct WatchdogCntlr *cntlr);
};
```

**核心层API**：`WatchdogCntlrAdd()`, `WatchdogCntlrRemove()`
**核心头文件**：`watchdog_core.h`

## 外设优先级汇总

| 优先级 | 外设类型 | Method结构体 | 理由 |
|--------|---------|-------------|------|
| **P0 - 最高** | GPIO | `GpioMethod` | 几乎所有外设驱动的基础依赖 |
| **P0 - 最高** | UART | `UartHostMethod` | 调试串口是最基本的功能 |
| **P1 - 高** | I2C | `I2cMethod` | 传感器、EEPROM等大量器件依赖 |
| **P1 - 高** | SPI | `SpiMethod` | Flash、显示屏等高速外设依赖 |
| **P2 - 中** | ADC | `AdcMethod` | 模拟信号采集常用 |
| **P2 - 中** | PWM | `PwmMethod` | LED调光、电机控制常用 |
| **P3 - 较低** | RTC | `RtcMethod` | 实时时钟，多数SoC内置 |
| **P3 - 较低** | Watchdog | `WatchdogMethod` | 系统可靠性保障 |
| **P4 - 扩展** | Timer | `TimerMethod` | 通用定时器 |
| **P4 - 扩展** | Pin/Mux | `PinMethod` | 引脚复用配置 |
| **P4 - 扩展** | Regulator | `RegulatorMethod` | 电源管理 |
| **P4 - 扩展** | SDIO/MMC | `SdioMethod` | SD卡/eMMC存储 |
