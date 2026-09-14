# L0 Sample: STM32F407ZG (Niobe407)

来源：公开资料整理（待 ITER 验证）

| 文件 | 说明 |
|------|------|
| `config.gni` | Board 级构建变量（ARM Cortex-M4, Uniproton） |
| `board_config.h` | 板级外设引脚映射（UART/I2C/SPI/PWM/ADC/LED） |
| `linker.ld` | 链接脚本（MEMORY + SECTIONS） |
| `target_config.h` | 内核最小骨架配置（Uniproton, 168MHz） |
