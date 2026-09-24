# 结构化数据格式设计

## 6.1 芯片规格 JSON Schema（核心数据模型 — OpenHarmony Lite版）

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ChipSpecification",
  "description": "OpenHarmony Lite（L0/L1）芯片规格结构化描述",
  "type": "object",
  "required": ["metadata", "cpu", "memoryMap"],
  "properties": {
    
    "metadata": {
      "type": "object",
      "description": "芯片元信息",
      "required": ["vendor", "chipName", "architecture", "targetSystemLevel"],
      "properties": {
        "vendor": { "type": "string", "description": "芯片厂商", "examples": ["STMicroelectronics", "HiSilicon", "Espressif", "Allwinner", "Bestechnic", "ASR", "Artery"] },
        "chipName": { "type": "string", "description": "芯片型号", "examples": ["STM32F407VGT6", "Hi3861V100", "BES2600W", "XR806", "ESP32-C3", "ASR582X", "AT32F437"] },
        "chipFamily": { "type": "string", "description": "芯片系列" },
        "revision": { "type": "string", "description": "芯片版本", "examples": ["Rev.A", "V2.0"] },
        "architecture": { "type": "string", "enum": ["ARM_Cortex_M", "ARM_Cortex_A", "RISC_V", "Xtensa"] },
        "targetSystemLevel": { "type": "string", "enum": ["L0", "L1"], "description": "目标系统级别：L0轻量系统或L1小型系统" },
        "kernelType": { "type": "string", "enum": ["liteos_m", "LiteOS-A"], "description": "目标内核类型" },
        "coreCount": { "type": "integer", "minimum": 1 },
        "maxFrequency": { "type": "number", "description": "最高主频(MHz)" },
        "processNode": { "type": "string", "description": "制程工艺", "examples": ["40nm", "55nm", "130nm"] },
        "packageType": { "type": "string" },
        "datasheetVersion": { "type": "string" },
        "datasheetDate": { "type": "string", "format": "date" },
        "svdFileAvailable": { "type": "boolean", "description": "是否有CMSIS-SVD文件可用" },
        "cmsisCompatibility": { "type": "string", "enum": ["FULL", "PARTIAL", "NONE"], "description": "CMSIS兼容程度" },
        "halInterfaceVersion": { "type": "string", "description": "HAL接口版本号" },
        "parseTimestamp": { "type": "string", "format": "date-time" },
        "parseConfidence": { "type": "number", "minimum": 0, "maximum": 1, "description": "解析置信度" }
      }
    },

    "cpu": {
      "type": "object",
      "description": "CPU核心信息",
      "properties": {
        "coreType": { "type": "string", "examples": ["Cortex-A55", "Cortex-M4F", "RV32IMAC"] },
        "isaVersion": { "type": "string", "examples": ["ARMv8.2-A", "ARMv7E-M", "RV32IMA"] },
        "features": { "type": "array", "items": { "type": "string" }, "examples": [["NEON", "VFPv4", "TrustZone"]] },
        "cacheL1I": { "type": "string", "description": "L1指令缓存大小" },
        "cacheL1D": { "type": "string", "description": "L1数据缓存大小" },
        "cacheL2": { "type": "string", "description": "L2缓存大小" },
        "fpu": { "type": "boolean" },
        "mmu": { "type": "boolean" },
        "mpu": { "type": "boolean" }
      }
    },

    "memoryMap": {
      "type": "array",
      "description": "存储器映射表",
      "items": {
        "type": "object",
        "required": ["name", "startAddress", "endAddress", "type"],
        "properties": {
          "name": { "type": "string" },
          "startAddress": { "type": "string", "pattern": "^0x[0-9A-Fa-f]+$" },
          "endAddress": { "type": "string", "pattern": "^0x[0-9A-Fa-f]+$" },
          "size": { "type": "string", "description": "人类可读大小", "examples": ["512KB", "2GB"] },
          "type": { "type": "string", "enum": ["FLASH", "SRAM", "DRAM", "PERIPHERAL", "RESERVED", "ROM", "BOOTROM"] },
          "attributes": { "type": "string", "enum": ["RW", "RO", "WO", "XN"], "description": "访问属性" }
        }
      }
    },

    "peripherals": {
      "type": "array",
      "description": "外设列表",
      "items": {
        "type": "object",
        "required": ["name", "type", "baseAddress"],
        "properties": {
          "name": { "type": "string", "examples": ["GPIO0", "UART1", "I2C0", "SPI2", "TIM3"] },
          "type": { "type": "string", "enum": ["GPIO", "UART", "SPI", "I2C", "PWM", "ADC", "DAC", "TIMER", "DMA", "USB", "ETH", "SDIO", "CAN", "WDT", "RTC", "CUSTOM"] },
          "baseAddress": { "type": "string", "pattern": "^0x[0-9A-Fa-f]+$" },
          "addressRange": { "type": "string", "pattern": "^0x[0-9A-Fa-f]+$" },
          "description": { "type": "string" },
          "instances": { "type": "integer", "description": "同类外设实例数" },
          "interrupts": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "irqNumber": { "type": "integer" },
                "name": { "type": "string" },
                "triggerType": { "type": "string", "enum": ["LEVEL_HIGH", "LEVEL_LOW", "EDGE_RISING", "EDGE_FALLING", "EDGE_BOTH"] },
                "priority": { "type": "integer" },
                "description": { "type": "string" }
              }
            }
          },
          "clockGate": {
            "type": "object",
            "description": "时钟门控信息",
            "properties": {
              "register": { "type": "string", "description": "时钟门控寄存器名" },
              "registerAddress": { "type": "string" },
              "bitPosition": { "type": "integer" },
              "enableValue": { "type": "integer" }
            }
          },
          "registers": {
            "type": "array",
            "description": "寄存器列表",
            "items": {
              "type": "object",
              "required": ["name", "offset", "access"],
              "properties": {
                "name": { "type": "string" },
                "offset": { "type": "string", "pattern": "^0x[0-9A-Fa-f]+$" },
                "absoluteAddress": { "type": "string" },
                "access": { "type": "string", "enum": ["R", "W", "RW", "RC", "WO", "RW1C"] },
                "resetValue": { "type": "string", "pattern": "^0x[0-9A-Fa-f]+$" },
                "description": { "type": "string" },
                "fields": {
                  "type": "array",
                  "description": "位域列表",
                  "items": {
                    "type": "object",
                    "required": ["name", "bitRange"],
                    "properties": {
                      "name": { "type": "string" },
                      "bitRange": { "type": "string", "pattern": "^\\d+(:\\d+)?$", "description": "位范围，如'31:24'或'7'" },
                      "msb": { "type": "integer" },
                      "lsb": { "type": "integer" },
                      "width": { "type": "integer" },
                      "access": { "type": "string", "enum": ["R", "W", "RW", "RC", "WO", "RW1C"] },
                      "resetValue": { "type": "string" },
                      "description": { "type": "string" },
                      "enumeratedValues": {
                        "type": "array",
                        "items": {
                          "type": "object",
                          "properties": {
                            "value": { "type": "string" },
                            "name": { "type": "string" },
                            "description": { "type": "string" }
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    },

    "interruptController": {
      "type": "object",
      "properties": {
        "type": { "type": "string", "enum": ["NVIC", "GIC-400", "GIC-600", "PLIC", "CLINT", "ECLIC"] },
        "totalIrqCount": { "type": "integer" },
        "priorityBits": { "type": "integer" },
        "vectorTableBase": { "type": "string" },
        "interrupts": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "id": { "type": "integer" },
              "name": { "type": "string" },
              "source": { "type": "string" },
              "peripheral": { "type": "string", "description": "关联外设名" },
              "triggerType": { "type": "string" },
              "defaultPriority": { "type": "integer" },
              "description": { "type": "string" }
            }
          }
        }
      }
    },

    "clockSystem": {
      "type": "object",
      "properties": {
        "clockSources": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": { "type": "string", "examples": ["HSI", "HSE", "LSE", "PLL1", "EXT_CLK"] },
              "type": { "type": "string", "enum": ["INTERNAL_RC", "EXTERNAL_CRYSTAL", "PLL", "EXTERNAL_INPUT"] },
              "frequency": { "type": "number", "description": "频率(Hz)" },
              "frequencyMin": { "type": "number" },
              "frequencyMax": { "type": "number" },
              "accuracy": { "type": "string", "description": "精度，如±1%" }
            }
          }
        },
        "pllConfigurations": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": { "type": "string" },
              "inputSource": { "type": "string" },
              "divM": { "type": "integer", "description": "输入分频" },
              "mulN": { "type": "integer", "description": "倍频系数" },
              "divP": { "type": "integer", "description": "输出分频" },
              "divQ": { "type": "integer" },
              "divR": { "type": "integer" },
              "vcoMinFreq": { "type": "number" },
              "vcoMaxFreq": { "type": "number" },
              "controlRegister": { "type": "string" },
              "controlRegisterAddress": { "type": "string" }
            }
          }
        },
        "busClocks": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": { "type": "string", "examples": ["AHB", "APB1", "APB2"] },
              "source": { "type": "string" },
              "prescalerRegister": { "type": "string" },
              "prescalerBits": { "type": "string" },
              "prescalerOptions": { "type": "array", "items": { "type": "integer" } }
            }
          }
        },
        "peripheralClockGates": {
          "type": "array",
          "description": "外设时钟门控映射",
          "items": {
            "type": "object",
            "properties": {
              "peripheralName": { "type": "string" },
              "gateRegister": { "type": "string" },
              "gateRegisterAddress": { "type": "string" },
              "enableBit": { "type": "integer" },
              "resetBit": { "type": "integer" },
              "busDomain": { "type": "string" }
            }
          }
        }
      }
    },

    "pinMux": {
      "type": "array",
      "description": "引脚复用表",
      "items": {
        "type": "object",
        "required": ["pinNumber", "pinName"],
        "properties": {
          "pinNumber": { "type": "integer" },
          "pinName": { "type": "string", "examples": ["PA0", "PB6", "GPIO2_3"] },
          "port": { "type": "string" },
          "bit": { "type": "integer" },
          "functions": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "afNumber": { "type": "integer", "description": "复用功能编号" },
                "function": { "type": "string", "examples": ["UART0_TX", "SPI1_SCK", "TIM2_CH1", "ADC_IN0"] },
                "peripheral": { "type": "string" },
                "signal": { "type": "string" },
                "isDefault": { "type": "boolean" }
              }
            }
          },
          "electricalProperties": {
            "type": "object",
            "properties": {
              "pullUp": { "type": "boolean" },
              "pullDown": { "type": "boolean" },
              "openDrain": { "type": "boolean" },
              "maxDriveCurrent": { "type": "string" },
              "voltageLevel": { "type": "string", "examples": ["3.3V", "1.8V"] },
              "ftTolerant": { "type": "boolean", "description": "5V容忍" }
            }
          }
        }
      }
    },

    "gpioController": {
      "type": "object",
      "description": "GPIO控制器信息（用于HCS生成）",
      "properties": {
        "groupCount": { "type": "integer", "description": "GPIO组数" },
        "pinsPerGroup": { "type": "integer", "description": "每组引脚数" },
        "physicalBaseAddress": { "type": "string" },
        "registerStep": { "type": "string", "description": "组间寄存器步进" },
        "interruptStart": { "type": "integer" },
        "realPinMap": { "type": "array", "items": { "type": "string" } }
      }
    },

    "ddrVariant": {
      "type": "object",
      "description": "SoC 内置 DDR 变体信息（仅内置 DDR SoC 需要，如 Hi3516CV610 -10B/-20S/-20G/-00S/-00G）。同型号 SoC 因内置 DDR 颗粒不同存在多变体，裸烧 bootrom 阶段 reg_info/xlsm 必须按变体选。详见 references/ddr-variant-guide.md",
      "properties": {
        "variantSuffix": { "type": "string", "description": "变体后缀", "examples": ["-10B", "-20S", "-20G", "-00S", "-00G"] },
        "ddrType": { "type": "string", "enum": ["DDR2", "DDR3", "DDR3L", "LPDDR4", "EXTERNAL"], "description": "DDR 类型，EXTERNAL=外置 DDR" },
        "ddrRate": { "type": "string", "description": "DDR 速率", "examples": ["1333Mbps", "2133Mbps"] },
        "ddrCapacity": { "type": "string", "description": "DDR 容量", "examples": ["64MB", "128MB", "512MB"] },
        "packageType": { "type": "string", "description": "封装", "examples": ["QFN9x9", "TFBGA"] },
        "busWidth": { "type": "string", "description": "DDR 总线位宽", "examples": ["16-bit"] },
        "xlsmFile": { "type": "string", "description": "对应 .xlsm 文件名（reg_info 生成输入）" },
        "kolXlsmFile": { "type": "string", "description": "KOL 量产变体的 .xlsm 文件名（带 _24M 后缀）" },
        "regInfoMagic": { "type": "string", "description": "reg_info.bin header magic（xlsm_to_bin.py -magic 参数）" },
        "notes": { "type": "string", "description": "备注（如与哪个变体共享 DDR 参数）" }
      }
    },

    "fieldSources": {
      "type": "object",
      "description": "字段溯源表——每个非 null 字段的来源路径（datasheet §/DTS 路径/SDK 头文件/MCP 命中等）。必须 100% 覆盖非 null 字段，禁止凭记忆填",
      "additionalProperties": { "type": "string", "description": "字段路径 → 来源描述（如 'metadata.coreType': 'DTS cpu@0 compatible + SDK CONFIG_A7=1'）" }
    },

    "crossValidation": {
      "type": "object",
      "description": "交叉验证——地址重叠/中断冲突/内存映射合理性检查结论 + 数据矛盾记录",
      "required": ["addressOverlapCheck", "interruptConflictCheck"],
      "properties": {
        "addressOverlapCheck": { "type": "string", "description": "地址重叠检查结论（如 'PASS — 各外设基地址区间无重叠'）" },
        "interruptConflictCheck": { "type": "string", "description": "中断冲突检查结论（如 'PASS — 各外设 IRQ 号无冲突'，含共享 IRQ 说明）" },
        "memoryMapSanityCheck": { "type": "string", "description": "内存映射合理性检查结论（DDR/SRAM/外设区/GIC 地址空间布局是否合理）" },
        "discrepancies": {
          "type": "array",
          "description": "数据矛盾记录（如 quick-ref 与 SDK 不一致处，标注以哪个为准）",
          "items": {
            "type": "object",
            "properties": {
              "field": { "type": "string", "description": "矛盾字段路径" },
              "issue": { "type": "string", "description": "矛盾描述" },
              "resolution": { "type": "string", "description": "取舍结论（如 '以 SDK 实际配置为准'）" }
            }
          }
        }
      }
    },

    "gapList": {
      "type": "array",
      "description": "缺口清单——诚实标注未能获取的字段 + 原因 + 优先级",
      "items": {
        "type": "object",
        "required": ["field", "status", "reason"],
        "properties": {
          "field": { "type": "string", "description": "缺口字段路径" },
          "priority": { "type": "string", "enum": ["必须有", "高频使用", "按需使用"], "description": "checklist 优先级分级" },
          "status": { "type": "string", "enum": ["missing", "partial"], "description": "missing=完全缺失，partial=部分获取" },
          "reason": { "type": "string", "description": "缺口原因（如 '厂商未公开 datasheet' / '需板级原理图'）" }
        }
      }
    },

    "completenessReport": {
      "type": "object",
      "description": "完整性报告——checklist 三级填充统计 + 置信度",
      "required": ["checklist", "confidence"],
      "properties": {
        "chip": { "type": "string", "description": "芯片型号" },
        "systemLevel": { "type": "string", "enum": ["L0", "L1"] },
        "functionalCapability": { "type": "string", "description": "功能能力（通用/WiFi/视频/多变体 SoC 等）" },
        "checklist": {
          "type": "object",
          "description": "三级 checklist 填充统计",
          "properties": {
            "必须有": {
              "type": "object",
              "description": "必选项（L0 全适用 7 项；L1 移除寄存器位域降 6 项；+WiFi RF / +视频 ISP / +多变体 DDR）",
              "properties": {
                "total": { "type": "integer", "description": "必选项总数" },
                "filled": { "type": "integer", "description": "已填充数（filled/total 必须 ≥ 1）" },
                "items": { "type": "array", "items": { "type": "object", "properties": { "item": {"type":"string"}, "status": {"type":"string","enum":["filled","partial","missing"]}, "value": {"type":"string"} } } }
              }
            },
            "高频使用": {
              "type": "object",
              "description": "高频项（DMA 通道映射/引脚复用/时钟树/启动模式，4 项）",
              "properties": {
                "total": { "type": "integer" },
                "filled": { "type": "integer" },
                "items": { "type": "array", "items": { "type": "object", "properties": { "item": {"type":"string"}, "status": {"type":"string","enum":["filled","partial","missing"]}, "value": {"type":"string"} } } }
              }
            },
            "按需使用": {
              "type": "object",
              "description": "按需项（低功耗/JTAG/调试接口/PLL 参数/cache 容量，5 项）",
              "properties": {
                "total": { "type": "integer" },
                "filled": { "type": "integer" },
                "items": { "type": "array", "items": { "type": "object", "properties": { "item": {"type":"string"}, "status": {"type":"string","enum":["filled","partial","missing"]}, "value": {"type":"string"} } } }
              }
            }
          }
        },
        "confidence": { "type": "number", "minimum": 0, "maximum": 1, "description": "解析置信度（score = 必须×0.6 + 高频×0.3 + 按需×0.1，可按数据来源可靠性上调）" },
        "confidenceCalculation": { "type": "string", "description": "置信度计算过程说明" },
        "outputFile": { "type": "string", "description": "输出文件路径" }
      }
    }
  }
}
```

## 6.2 输出映射关系（L0/L1差异化）

### L0轻量系统：JSON → LiteOS-M HAL头文件

解析器输出的JSON直接生成LiteOS-M HAL接口所需的头文件和数据结构，不涉及HCS/DTS。

| JSON 字段 | HAL头文件内容 | 说明 |
|-----------|-------------|------|
| `peripherals[n].baseAddress` | `#define GPIO0_BASE 0x40020000U` | 外设基地址宏定义 |
| `peripherals[n].registers[m]` | `typedef struct { ... } GPIO_TypeDef;` | 寄存器结构体定义 |
| `peripherals[n].registers[m].fields[k]` | `#define GPIO_CR_MODE_Pos 0` | 位域宏定义 |
| `interruptController.interrupts[n]` | `IRQn_Type` 枚举 | NVIC中断号枚举 |
| `clockSystem.peripheralClockGates[n]` | 时钟使能函数参数 | RCC时钟门控信息 |

### L1小型系统：JSON → 精简版HCS配置

L1使用精简版HDF框架，JSON可映射到精简版HCS配置字段：

| JSON 字段 | HCS 配置字段 | 说明 |
|-----------|-------------|------|
| `gpioController.groupCount` | `groupNum` | GPIO组数 |
| `gpioController.pinsPerGroup` | `bitNum` | 每组引脚数 |
| `gpioController.physicalBaseAddress` | `phyBase` / `regBase` | 寄存器基地址 |
| `gpioController.registerStep` | `regStep` | 组间步进 |
| `gpioController.interruptStart` | `irqStart` | 中断起始号 |
| `peripherals[n].baseAddress` | `regBase` (UART/I2C等) | 外设基地址 |
| `peripherals[n].interrupts[0].irqNumber` | `irq` | 中断号 |
