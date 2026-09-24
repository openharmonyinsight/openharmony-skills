/*
 * STM32F407ZG (Niobe407) 板级外设配置
 * 来源：ohos-lite-helper MCP 域 device-config（l0-config-samples）
 * 系统级别：L0 (Uniproton / LiteOS-M)
 * 芯片：STM32F407ZG, ARM Cortex-M4
 */

#ifndef BOARD_CONFIG_H
#define BOARD_CONFIG_H

/* ========== UART引脚映射 ========== */
#define BOARD_UART0_TX_PIN          GPIO_PIN(0, 9)   /* PA9  - USART1_TX */
#define BOARD_UART0_RX_PIN          GPIO_PIN(0, 10)  /* PA10 - USART1_RX */
#define BOARD_UART0_BAUDRATE        115200
#define BOARD_UART0_ENABLE          1

/* ========== I2C引脚映射 ========== */
#define BOARD_I2C0_SDA_PIN          GPIO_PIN(1, 7)   /* PB7  - I2C1_SDA */
#define BOARD_I2C0_SCL_PIN          GPIO_PIN(1, 6)   /* PB6  - I2C1_SCL */
#define BOARD_I2C0_SPEED            400000
#define BOARD_I2C0_ENABLE           1

/* ========== SPI引脚映射 ========== */
#define BOARD_SPI0_SCK_PIN          GPIO_PIN(0, 5)   /* PA5  - SPI1_SCK */
#define BOARD_SPI0_MOSI_PIN         GPIO_PIN(0, 7)   /* PA7  - SPI1_MOSI */
#define BOARD_SPI0_MISO_PIN         GPIO_PIN(0, 6)   /* PA6  - SPI1_MISO */
#define BOARD_SPI0_CS_PIN           GPIO_PIN(0, 4)   /* PA4  - SPI1_NSS */
#define BOARD_SPI0_ENABLE           1

/* ========== PWM通道映射 ========== */
#define BOARD_PWM0_PIN              GPIO_PIN(0, 1)   /* PA1  - TIM2_CH2 */
#define BOARD_PWM0_CHANNEL          2
#define BOARD_PWM0_ENABLE           1

/* ========== ADC通道映射 ========== */
#define BOARD_ADC_TEMP_CHANNEL      16               /* 内部温度传感器 */
#define BOARD_ADC_VREF_CHANNEL      17               /* 内部参考电压 */

/* ========== LED/按键引脚 ========== */
#define BOARD_LED1_PIN              GPIO_PIN(2, 13)  /* PC13, 板载 LED */
#define BOARD_KEY1_PIN              GPIO_PIN(0, 0)   /* PA0,  用户按键 */

#endif /* BOARD_CONFIG_H */
