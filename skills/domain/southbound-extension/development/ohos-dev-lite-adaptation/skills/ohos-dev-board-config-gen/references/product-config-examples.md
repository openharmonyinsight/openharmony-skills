# 产品配置实例与外设配置项知识库

## L0轻量系统输出产物结构

```
output/hi3861/
├── config.json                   # ★ 产品编译配置
├── include/
│   └── board_config.h            # ★ 板级外设引脚映射头文件
├── src/
│   └── board_init.c              # 板级初始化代码（时钟/GPIO等）
└── validation_report.json        # 配置验证报告
```

## L1小型系统输出产物结构

```
output/hi3516/
├── hdf.hcs                       # 主入口文件（精简版）
├── device_info/
│   └── device_info.hcs           # 设备信息（精简版）
├── gpio/
│   └── gpio_config.hcs           # GPIO控制器配置
├── uart/
│   └── uart_config.hcs           # UART端口配置
├── i2c/
│   └── i2c_config.hcs            # I2C控制器配置
└── validation_report.json        # 配置验证报告
```

## 配置验证报告格式

```json
{
  "version": "1.0",
  "timestamp": "2026-06-08T10:30:00Z",
  "chipName": "RK3568",
  "overallStatus": "warning",
  "summary": {
    "errors": 0,
    "warnings": 3,
    "info": 5,
    "filesChecked": 8,
    "nodesChecked": 45,
    "attributesChecked": 186
  },
  "results": [
    {
      "level": "semantic",
      "severity": "warning",
      "check": "pin_mux_conflict",
      "message": "GPIO0_B3 assigned to both I2C0_SDA and PWM1_OUT",
      "location": {
        "files": ["i2c/i2c_config.hcs", "pwm/pwm_config.hcs"],
        "details": "Check schematic to determine correct function"
      }
    },
    {
      "level": "semantic",
      "severity": "warning",
      "check": "unused_peripheral",
      "message": "UART3 configured in device_info but no uart_3_config node found",
      "location": {
        "file": "device_info/device_info.hcs",
        "line": 87
      }
    }
  ]
}
```

## 需收集的Lite系统芯片/开发板配置实例

| 序号 | 芯片平台 | 开发板 | 系统类型 | 配置方式 | 状态 |
|------|---------|--------|---------|---------|------|
| 1 | Hi3861V100 | HiSpark WiFi IoT | L0轻量系统 | config.json + 头文件 | ⬜ |
| 2 | STM32F407 | Niobe407 | L0轻量系统 | config.json + 头文件 | ⬜ |
| 3 | BES2600W | 欧智通V200Z-R | L0轻量系统 | config.json + 头文件 | ⬜ |
| 4 | ESP32-C3 | ESP32-C3-DevKit | L0轻量系统 | config.json + 头文件 | ⬜ |
| 5 | XR806 | Xradio开发板 | L0轻量系统 | config.json + 头文件 | ⬜ |
| 6 | ASR582X | ASR582X开发板 | L0轻量系统 | config.json + 头文件 | ⬜ |
| 7 | AT32F437 | AT32开发板 | L0轻量系统 | config.json + 头文件 | ⬜ |
| 8 | Hi3516DV300 | HiSpark Taurus | L1小型系统 | 精简版HCS | ⬜ |
| 9 | Hi3518EV300 | HiSpark IPC | L1小型系统 | 精简版HCS | ⬜ |
| 10 | 全志T507 | 全志T507开发板 | L1小型系统 | 精简版HCS | ⬜ |

## 外设配置项知识库

### GPIO配置项

| 配置项 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| match_attr | string | 是 | 匹配属性标识 | "hdf_gpio_config" |
| groupNum | uint32 | 是 | GPIO组数量 | 5 |
| bitNum | uint32 | 是 | 每组GPIO位数 | 32 |
| regBase | uint32[] | 是 | 各组寄存器基地址 | [0xFD8A0000, 0xFD8B0000] |
| regSize | uint32 | 否 | 寄存器映射大小 | 0x1000 |
| irqNum | uint32[] | 否 | 中断号列表 | [48, 49, 50, 51, 52] |

### UART配置项

| 配置项 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| match_attr | string | 是 | 匹配属性标识 | "hdf_uart_1" |
| num | uint32 | 是 | UART端口号 | 1 |
| baudRate | uint32 | 是 | 波特率 | 115200 |
| iomemBase | uint32 | 是 | 寄存器基地址 | 0xFE650000 |
| iomemRegSize | uint32 | 否 | 寄存器映射大小 | 0x100 |
| irqNum | uint32 | 是 | 中断号 | 117 |
| fifoTxBufferSize | uint32 | 否 | TX FIFO大小 | 116 |
| fifoRxBufferSize | uint32 | 否 | RX FIFO大小 | 12 |
| flags | uint32 | 否 | 标志位 | 0 |
| interruptEnable | bool | 否 | 是否启用中断 | true |
| regSize | uint32 | 否 | 寄存器宽度 | 2 |

### I2C配置项

| 配置项 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| match_attr | string | 是 | 匹配属性标识 | "hdf_i2c_0" |
| id | uint32 | 是 | I2C总线号 | 0 |
| regBase | uint32 | 是 | 寄存器基地址 | 0xFDD40000 |
| regSize | uint32 | 否 | 寄存器映射大小 | 0x1000 |
| irqNum | uint32 | 是 | 中断号 | 46 |
| freq | uint32 | 是 | 总线速率(Hz) | 400000 |
| timeout | uint32 | 否 | 超时时间(ms) | 1000 |

### SPI配置项

| 配置项 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| match_attr | string | 是 | 匹配属性标识 | "hdf_spi_0" |
| busNum | uint32 | 是 | SPI总线号 | 0 |
| regBase | uint32 | 是 | 寄存器基地址 | 0xFE610000 |
| regSize | uint32 | 否 | 寄存器映射大小 | 0x1000 |
| irqNum | uint32 | 是 | 中断号 | 52 |
| maxFreq | uint32 | 是 | 最大频率(Hz) | 50000000 |
| mode | uint32 | 否 | SPI模式(0-3) | 0 |
| transferMode | uint32 | 否 | 传输模式(0=DMA,1=poll) | 0 |

### PWM配置项

| 配置项 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| match_attr | string | 是 | 匹配属性标识，格式 "{vendor}_{chip}_pwm_{N}" | "hisilicon_hi35xx_pwm_0" |
| serviceName | string | 否 | 服务名（template中定义） | "" |
| num | uint32 | 是 | PWM控制器编号 | 0 |
| base | uint32 | 是 | PWM控制器寄存器基地址 | 0x12070000 |

> **参考样本**：`hi3516dv300_pwm_config.hcs` — Hi3516DV300有2个PWM控制器，使用template+pwm_device实例模式。template定义默认base，实例可覆盖num和base。

### ADC配置项

| 配置项 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| match_attr | string | 是 | 匹配属性标识，格式 "{vendor}_{chip}_adc" | "hisilicon_hi35xx_adc" |
| regBasePhy | uint32 | 是 | ADC寄存器物理基地址 | 0x120E0000 |
| regSize | uint32 | 是 | 寄存器映射大小 | 0x34 |
| deviceNum | uint32 | 是 | ADC设备编号 | 0 |
| validChannel | uint32 | 是 | 有效通道位掩码 | 0x1 |
| dataWidth | uint32 | 是 | 数据位宽(bit) | 10 |
| scanMode | uint32 | 否 | 扫描模式(0=单次,1=连续) | 1 |
| delta | uint32 | 否 | 差分模式(0=单端,1=差分) | 0 |
| deglitch | uint32 | 否 | 去毛刺使能 | 0 |
| glitchSample | uint32 | 否 | 毛刺采样周期(ns) | 5000 |
| rate | uint32 | 否 | 采样率(Hz) | 20000 |

> **参考样本**：`hi3516dv300_adc_config.hcs` — 使用template+adc_device实例模式。template定义全部默认参数，实例仅需覆盖deviceNum和validChannel。

### RTC配置项

| 配置项 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| match_attr | string | 是 | 匹配属性标识，格式 "{vendor}_{chip}_rtc" | "hisilicon_hi35xx_rtc" |
| supportAnaCtrl | bool | 否 | 是否支持模拟控制 | false |
| supportLock | bool | 否 | 是否支持锁定功能 | false |
| rtcSpiBaseAddr | uint32 | 是 | RTC SPI基地址 | 0x12080000 |
| regAddrLength | uint32 | 是 | 寄存器地址长度 | 0x100 |
| irq | uint32 | 是 | RTC中断号 | 37 |
| anaCtrlAddr | uint32 | 否 | 模拟控制寄存器地址 | 0xff |
| lock0Addr~lock3Addr | uint32 | 否 | 锁定寄存器地址(4个) | 0xff |

> **参考样本**：`hi3516dv300_rtc_config.hcs` — Hi3516DV300只有1个RTC控制器，无template实例模式，直接在节点中定义全部属性。

### Watchdog配置项

| 配置项 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| match_attr | string | 是 | 匹配属性标识，格式 "{vendor}_{chip}_watchdog_{N}" | "hisilicon_hi35xx_watchdog_0" |
| id | uint32 | 是 | Watchdog控制器编号 | 0 |
| regBase | uint32 | 是 | 寄存器基地址 | 0x12050000 |
| regStep | uint32 | 否 | 寄存器步进(多控制器间隔) | 0x1000 |

> **参考样本**：`hi3516dv300_watchdog_config.hcs` — 使用template+watchdog_controller实例模式。Hi3516DV300有2个Watchdog控制器（0x12050000和0x12051000），template定义默认regBase和regStep。

### Timer配置项

| 配置项 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| match_attr | string | 是 | 匹配属性标识，格式 "{vendor}_{chip}_timer" | "hisilicon_hi35xx_timer" |
| number | uint32 | 是 | Timer编号 | 0 |
| regBase | uint32 | 是 | Timer寄存器基地址 | 0x12000000 |
| bus_clock | uint32 | 是 | 总线时钟频率(MHz) | 30 |
| mode | uint32 | 否 | 定时模式(0=周期,1=单次) | 1 |
| init_count_val | uint32 | 否 | 初始计数值 | 0 |
| irq | uint32 | 是 | Timer中断号 | 33 |

> **参考样本**：`hi3516dv300_timer_config.hcs` — Hi3516DV300有8个Timer控制器（device_timer_0到7），使用template+timer_controller实例模式。每个timer覆盖number、regBase、bus_clock和irq。

### MMC/SDIO配置项

| 配置项 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|
| match_attr | string | 是 | 匹配属性标识 | "hi3516_mmc_emmc" / "hi3516_mmc_sd" / "hi3516_mmc_sdio" |
| voltDef | uint32 | 否 | 默认电压(0=3.3V) | 0 |
| freqMin | uint32 | 否 | 最小频率(Hz) | 50000 |
| freqMax | uint32 | 否 | 最大频率(Hz) | 100000000 |
| freqDef | uint32 | 否 | 默认频率(Hz) | 400000 |
| maxBlkNum | uint32 | 否 | 最大块数量 | 2048 |
| maxBlkSize | uint32 | 否 | 最大块大小(B) | 512 |
| ocrDef | uint32 | 否 | 默认OCR值 | 0x300000 |
| caps | uint32 | 否 | 能力标志位(bitmask) | 0xd001e045 |
| caps2 | uint32 | 否 | 扩展能力标志位 | 0x60 |
| regSize | uint32 | 否 | 寄存器映射大小 | 0x118 |
| hostId | uint32 | 是 | Host编号(0=emmc, 1=sd, 2=sdio) | 0 |
| regBasePhy | uint32 | 是 | 控制器物理基地址 | 0x10100000 |
| irqNum | uint32 | 是 | 中断号 | 96 |
| devType | uint32 | 是 | 设备类型(0=emmc, 1=sd, 2=sdio) | 0 |

> **参考样本**：`hi3516dv300_mmc_config.hcs` — Hi3516DV300有3个MMC host（emmc/sd/sdio），使用template+mmc_controller实例模式。每个host覆盖match_attr、hostId、regBasePhy、irqNum、devType和caps。

## 常见HCS配置错误及修复方案

| 错误类型 | 错误现象 | 原因分析 | 修复方案 |
|----------|---------|---------|---------|
| 语法错误 | hc-gen报"parse error at line X" | 缺少分号、括号不匹配、非法字符 | 检查指定行附近的语法完整性 |
| 模板违反 | "cannot add new attribute in template instance" | 在template实例中添加了模板未定义的属性 | 移除多余属性或在模板中预定义 |
| match_attr不匹配 | 驱动初始化失败，读不到配置 | device_info.hcs中的deviceMatchAttr与config.hcs中的match_attr不一致 | 确保两处字符串完全一致 |
| include路径错误 | "file not found" | include路径不在搜索路径中 | 调整-I参数或使用相对路径 |
| 节点名冲突 | "duplicate node name" | 同一父节点下定义了同名子节点 | 重命名冲突的节点 |
| delete无效 | "cannot delete non-included node" | 尝试删除非include引入的节点 | 仅对include引入的内容使用delete |
| 类型不匹配 | 运行时读取配置返回HDF_FAILURE | HCS中值的类型与驱动代码期望的类型不一致 | 核对驱动源码中的读取API类型 |
| 中断号冲突 | 多个设备注册同一中断号失败 | 两个外设配置了相同的irqNum | 查阅芯片手册确认正确的中断号 |
| 地址重叠 | 内存映射失败 | 多个外设的iomemBase+regSize范围重叠 | 核实芯片手册中的地址空间分配 |
| 权限不足 | 用户态无法访问设备服务 | permission设置过严或policy不正确 | 调整permission和policy值 |

## 配置验证层次模型

```
┌──────────────────────────────────────────────┐
│           Level 4: 运行时验证                  │
│   驱动加载测试、配置读取验证、功能测试            │
├──────────────────────────────────────────────┤
│           Level 3: 交叉验证                    │
│   DTS↔HCS一致性、多文件间引用完整性              │
├──────────────────────────────────────────────┤
│           Level 2: 语义验证                    │
│   地址冲突、中断冲突、引脚冲突、依赖完整性         │
├──────────────────────────────────────────────┤
│           Level 1: 语法验证                    │
│   hc-gen编译检查、模板合规性、数据类型正确性       │
└──────────────────────────────────────────────┘
```

### Level 1 - 语法验证

| 检查项 | 方法 | 严重级别 |
|--------|------|---------|
| hc-gen编译通过 | 调用hc-gen编译，检查返回值和stderr | ERROR |
| 括号匹配 | 静态分析`{}`配对 | ERROR |
| 分号完整性 | 检查每个属性语句以`;`结尾 | ERROR |
| 模板合规 | 检查template实例未新增/删除属性 | ERROR |
| include可达 | 检查所有include文件存在 | ERROR |
| 数据类型合法 | 检查值的类型符合预期(int/string/bool/array) | WARNING |
| 命名规范 | 检查节点名/属性名符合HDF命名约定 | INFO |

### Level 2 - 语义验证

| 检查项 | 方法 | 严重级别 |
|--------|------|---------|
| 寄存器地址冲突 | 检查所有外设的[iomemBase, iomemBase+regSize)区间无重叠 | ERROR |
| 中断号冲突 | 检查所有外设的irqNum无重复 | ERROR |
| 引脚复用冲突 | 检查同一物理引脚未被分配给多个外设的不同功能 | ERROR |
| match_attr唯一性 | 检查所有match_attr值全局唯一 | ERROR |
| match_attr配对 | 检查device_info中的deviceMatchAttr都有对应的config节点 | ERROR |
| moduleName存在 | 检查引用的moduleName在已知驱动模块列表中 | WARNING |
| 必填项完整 | 检查每种外设的必要配置项均已填写 | ERROR |
| 数值范围合法 | 检查波特率、频率等在合理范围内 | WARNING |
| 时钟源有效 | 检查引用的时钟源名称存在于芯片时钟树中 | WARNING |

### Level 3 - 交叉验证

| 检查项 | 方法 | 严重级别 |
|--------|------|---------|
| DTS↔HCS地址一致 | 解析DTS和HCS，比对相同外设的基地址 | WARNING |
| DTS↔HCS中断一致 | 比对相同外设的中断号 | WARNING |
| include链完整性 | 验证hdf.hcs包含了所有必要的子配置文件 | WARNING |
| 设备节点↔资源配置对应 | 每个deviceNode都有对应的资源配置 | ERROR |

---

## 真实示例参考

完整真实芯片配置样本见本 SKILL 的 `examples/` 目录：
- L0: `examples/l0/`（Hi3861 / STM32F407 等）
- L1: `examples/l1/`（Hi3516DV300 等）
