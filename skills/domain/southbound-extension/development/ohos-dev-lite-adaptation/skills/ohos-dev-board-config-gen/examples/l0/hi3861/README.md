# L0 Sample: Hi3861V100 (HiSpark WiFi IoT)

来源：实测验证通过的真实编译产物提取

| 文件 | 说明 |
|------|------|
| `config.gni` | Board 级构建变量（RISC-V rv32imac, LiteOS-M） |
| `board_config.h` | 板级外设引脚映射（UART/I2C/SPI/PWM/LED） |
| `linker.ld` | 链接脚本（MEMORY + SECTIONS） |
| `target_config.h` | 内核最小骨架配置（LiteOS-M） |
