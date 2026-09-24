/*
 * Hi3861V100 (HiSpark WiFi IoT) 板级外设配置
 * 来源：ohos-lite-helper MCP 域 device-config（l0-config-samples）
 * 系统级别：L0 (LiteOS-M)
 * 芯片：Hi3861V100, RISC-V rv32imac
 */

#ifndef BOARD_CONFIG_H
#define BOARD_CONFIG_H

/* ========== UART引脚映射 ========== */
#define BOARD_UART0_TX_PIN          9       /* GPIO0_9 */
#define BOARD_UART0_RX_PIN          10      /* GPIO0_10 */
#define BOARD_UART0_BAUDRATE        115200
#define BOARD_UART0_ENABLE          1

/* ========== I2C引脚映射 ========== */
#define BOARD_I2C0_SDA_PIN          14      /* GPIO0_14 */
#define BOARD_I2C0_SCL_PIN          13      /* GPIO0_13 */
#define BOARD_I2C0_SPEED            400000
#define BOARD_I2C0_ENABLE           1

/* ========== SPI引脚映射 ========== */
#define BOARD_SPI0_SCK_PIN          7       /* GPIO0_7 */
#define BOARD_SPI0_MOSI_PIN         11      /* GPIO0_11 */
#define BOARD_SPI0_MISO_PIN         10      /* GPIO0_10 */
#define BOARD_SPI0_CS_PIN           8       /* GPIO0_8 */
#define BOARD_SPI0_ENABLE           0       /* 默认不使能 */

/* ========== PWM通道映射 ========== */
#define BOARD_PWM0_PIN              9       /* GPIO0_9 */
#define BOARD_PWM0_CHANNEL          0
#define BOARD_PWM0_ENABLE           1

/* ========== LED/按键引脚 ========== */
#define BOARD_LED1_PIN              2       /* GPIO0_2, Hi3861 板载 LED */
#define BOARD_KEY1_PIN              0       /* GPIO0_0, 用户按键 */

#endif /* BOARD_CONFIG_H */
