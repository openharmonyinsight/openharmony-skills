# HCS配置模板与BUILD.gn编译配置

> 来源：需求分析报告 §7.3-7.4

## device_info.hcs 模板


> **命名说明**：模板中 `hdf_platform_*` 为 HDF 通用命名模式，实际适配时替换为厂商前缀（如海思 `hisi_*`）；字段名用 HCS 标准驼峰式（`regBase`、`irqStart`、`regSize` 等），与真实 .hcs 文件一致。

```hcs
root {
    device_info {
        platform :: host {
            /* ===== GPIO设备节点 ===== */
            device_gpio :: device {
                device0 :: deviceNode {
                    policy = 2;                          /* 发布到管理器+用户态 */
                    priority = 100;                      /* 加载优先级 */
                    preload = 0;                         /* 预加载 */
                    permission = 0644;
                    moduleName = "HDF_PLATFORM_GPIO";    /* 对应驱动moduleName */
                    serviceName = "HDF_PLATFORM_GPIO_0"; /* 对外服务名 */
                    deviceMatchAttr = "hdf_platform_gpio0"; /* 匹配私有配置 */
                }
                device1 :: deviceNode {
                    policy = 2;
                    priority = 100;
                    preload = 0;
                    permission = 0644;
                    moduleName = "HDF_PLATFORM_GPIO";
                    serviceName = "HDF_PLATFORM_GPIO_1";
                    deviceMatchAttr = "hdf_platform_gpio1";
                }
            }

            /* ===== I2C设备节点 ===== */
            device_i2c :: device {
                device0 :: deviceNode {
                    policy = 2;
                    priority = 110;
                    preload = 0;
                    permission = 0644;
                    moduleName = "HDF_PLATFORM_I2C";
                    serviceName = "HDF_PLATFORM_I2C_0";
                    deviceMatchAttr = "hdf_platform_i2c0";
                }
            }

            /* ===== UART设备节点 ===== */
            device_uart :: device {
                device0 :: deviceNode {
                    policy = 2;
                    priority = 90;                       /* UART优先级较高 */
                    preload = 0;
                    permission = 0644;
                    moduleName = "HDF_PLATFORM_UART";
                    serviceName = "HDF_PLATFORM_UART_2";
                    deviceMatchAttr = "hdf_platform_uart2";
                }
            }

            /* ===== ADC设备节点 ===== */
            device_adc :: device {
                device0 :: deviceNode {
                    policy = 2;
                    priority = 120;
                    preload = 0;
                    permission = 0644;
                    moduleName = "HDF_PLATFORM_ADC";
                    serviceName = "HDF_PLATFORM_ADC_0";
                    deviceMatchAttr = "hdf_platform_adc0";
                }
            }

            /* ===== PWM设备节点 ===== */
            device_pwm :: device {
                device0 :: deviceNode {
                    policy = 2;
                    priority = 120;
                    preload = 0;
                    permission = 0644;
                    moduleName = "HDF_PLATFORM_PWM";
                    serviceName = "HDF_PLATFORM_PWM_0";
                    deviceMatchAttr = "hdf_platform_pwm0";
                }
            }

            /* ===== RTC设备节点 ===== */
            device_rtc :: device {
                device0 :: deviceNode {
                    policy = 2;
                    priority = 130;
                    preload = 0;
                    permission = 0644;
                    moduleName = "HDF_PLATFORM_RTC";
                    serviceName = "HDF_PLATFORM_RTC";
                    deviceMatchAttr = "hdf_platform_rtc";
                }
            }

            /* ===== Watchdog设备节点 ===== */
            device_watchdog :: device {
                device0 :: deviceNode {
                    policy = 2;
                    priority = 80;                       /* Watchdog优先级很高 */
                    preload = 0;
                    permission = 0644;
                    moduleName = "HDF_PLATFORM_WATCHDOG";
                    serviceName = "HDF_PLATFORM_WDT";
                    deviceMatchAttr = "hdf_platform_wdt";
                }
            }
        }
    }
}
```

## gpio_config.hcs 模板

```hcs
root {
    gpio_config {
        template gpio_controller {
            match_attr = "";
            serviceName = "";
            regBase = 0;
            reg_size = 0x1000;
            irq_num = 0;
            pin_count = 32;
            start = 0;              /* GPIO起始编号 */
        }

        gpio0 :: gpio_controller {
            match_attr = "hdf_platform_gpio0";
            serviceName = "HDF_PLATFORM_GPIO_0";
            regBase = 0xFD8A0000;
            reg_size = 0x1000;
            irq_num = 51;
            pin_count = 32;
            start = 0;
        }

        gpio1 :: gpio_controller {
            match_attr = "hdf_platform_gpio1";
            serviceName = "HDF_PLATFORM_GPIO_1";
            regBase = 0xFE740000;
            reg_size = 0x1000;
            irq_num = 52;
            pin_count = 32;
            start = 32;
        }

        gpio2 :: gpio_controller {
            match_attr = "hdf_platform_gpio2";
            serviceName = "HDF_PLATFORM_GPIO_2";
            regBase = 0xFE750000;
            reg_size = 0x1000;
            irq_num = 53;
            pin_count = 32;
            start = 64;
        }

        gpio3 :: gpio_controller {
            match_attr = "hdf_platform_gpio3";
            serviceName = "HDF_PLATFORM_GPIO_3";
            regBase = 0xFE760000;
            reg_size = 0x1000;
            irq_num = 54;
            pin_count = 32;
            start = 96;
        }

        gpio4 :: gpio_controller {
            match_attr = "hdf_platform_gpio4";
            serviceName = "HDF_PLATFORM_GPIO_4";
            regBase = 0xFE770000;
            reg_size = 0x1000;
            irq_num = 55;
            pin_count = 32;
            start = 128;
        }
    }
}
```

## uart_config.hcs 模板

```hcs
root {
    uart_config {
        template uart_device {
            match_attr = "";
            serviceName = "";
            baudRate = 115200;
            fifoTxEmpty = 0;
            fifoRxFull = 0;
            num = 0;
            irqNum = 0;
            iomem = 0;
            wlen = 8;
            parity = 0;            /* 0:None, 1:Odd, 2:Even */
            stopBits = 1;          /* 1 or 2 */
            rts = 0;
            cts = 0;
            clkFreq = 24000000;   /* 时钟频率 */
        }

        uart2 :: uart_device {
            match_attr = "hdf_platform_uart2";
            serviceName = "HDF_PLATFORM_UART_2";
            baudRate = 115200;
            num = 2;
            irqNum = 69;
            iomem = 0xFE660000;
            clkFreq = 24000000;
        }
    }
}
```

## hdf.hcs 顶层入口文件

```hcs
#include "device_info/device_info.hcs"
#include "gpio/gpio_config.hcs"
#include "i2c/i2c_config.hcs"
#include "uart/uart_config.hcs"
#include "adc/adc_config.hcs"
#include "pwm/pwm_config.hcs"
#include "rtc/rtc_config.hcs"
#include "watchdog/watchdog_config.hcs"
```

## L0轻量系统驱动 BUILD.gn

```gn
import("//build/lite/config/component/lite_component.gni")

# Hi3861 GPIO驱动 — L0 IoT外设驱动子系统方式
lite_component("hi3861_gpio") {
    features = [
        ":gpio_driver",
    ]
}

static_library("gpio_driver") {
    sources = [
        "gpio_hi3861.c",
    ]
    
    include_dirs = [
        ".",
        "//kernel/liteos_m/kal/cmsis",
        "//device/soc/hisilicon/hi3861v100/sdk_liteos/include",
    ]
    
    cflags = [
        "-Wall",
        "-Wextra",
        "-Wno-unused-parameter",
    ]
}
```

## L1小型系统驱动 BUILD.gn

```gn
import("//build/lite/config/component/lite_component.gni")
import("//drivers/hdf_core/adapter/khdf/khdf.gni")

# Hi3516 GPIO驱动 — L1精简版HDF方式
hdf_driver("hdf_platform_gpio_hi3516") {
    sources = [
        "gpio_hi3516.c",
    ]
    
    deps = [
        "//drivers/hdf_core/adapter/platform:hdf_platform",
    ]
    
    include_dirs = [
        ".",
        "//drivers/hdf_core/framework/include/core",
        "//drivers/hdf_core/framework/include/utils",
        "//drivers/hdf_core/framework/include/osal",
        "//drivers/hdf_core/framework/include/platform",
        "//drivers/hdf_core/framework/include/platform/gpio",
        "//drivers/hdf_core/adapter/platform/include",
    ]
    
    cflags = [
        "-Wall",
        "-Wextra",
        "-Werror",
        "-Wno-unused-parameter",
    ]
}
```

## 测试 BUILD.gn

```gn
import("//build/lite/config/test/lite_test.gni")

lite_test("gpio_driver_test") {
    testonly = true
    
    sources = [
        "gpio_test.c",
    ]
    
    include_dirs = [
        ".",
        "//kernel/liteos_m/kal/cmsis",
    ]
}
```
