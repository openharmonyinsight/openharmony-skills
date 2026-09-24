# L1 Sample: Hi3516DV300 (HiSpark Taurus)

来源：公开资料整理（待 ITER 验证）

| 文件 | 说明 |
|------|------|
| `config.gni` | Board 级构建变量（ARM Cortex-A7, LiteOS-A） |
| `hdf.hcs` | HCS 主入口（#include 所有子配置） |
| `device_info.hcs` | 设备节点树（host→device→deviceNode + match_attr） |
| `gpio_config.hcs` | GPIO 控制器寄存器配置 |
| `uart_config.hcs` | UART 端口配置（端口号、波特率、引脚） |
| `i2c_config.hcs` | I2C 总线配置 |
| `spi_config.hcs` | SPI 总线配置 |
| `pwm_config.hcs` | PWM 配置 |
| `adc_config.hcs` | ADC 配置 |
