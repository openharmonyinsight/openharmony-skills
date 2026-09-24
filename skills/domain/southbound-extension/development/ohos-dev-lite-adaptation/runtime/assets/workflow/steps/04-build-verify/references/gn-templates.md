# BUILD.gn模板（芯片层/单板层/产品层）

> 来源：需求4分析报告 §8

---

## 1. 分层模板架构

```
┌─────────────────────────────────────────┐
│          产品层模板 (Product Layer)       │
│  • product.json.j2                      │
│  • vendor_config.gni.j2                 │
│  • 产品特定的子系统选择                  │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│          单板层模板 (Board Layer)         │
│  • board_config.gni.j2                  │
│  • board_BUILD.gn.j2                    │
│  • 外设引脚映射                          │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│          芯片层模板 (SoC Layer)           │
│  • soc_config.gni.j2                    │
│  • linker.ld.j2                         │
│  • startup.S.j2                         │
│  • 时钟树、中断控制器配置                │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│          基础层模板 (Base Layer)          │
│  • compiler_flags.gni.j2                │
│  • toolchain_config.gni.j2              │
│  • 通用编译选项和规则                    │
└─────────────────────────────────────────┘
```

## 2. 基础层模板

### 2.1 编译器标志模板

```jinja2
{# build/lite/config/compiler/compiler_flags.gni.j2 #}

# Auto-generated compiler flags for {{ chip.name }}
# Architecture: {{ chip.architecture }}

# C编译选项
cflags_c = [
{% for flag in compiler.c_flags %}
  "{{ flag }}",
{% endfor %}
]

# C++编译选项
cflags_cc = [
{% for flag in compiler.cpp_flags %}
  "{{ flag }}",
{% endfor %}
]

# 汇编选项
asmflags = [
{% for flag in compiler.asm_flags %}
  "{{ flag }}",
{% endfor %}
]

# 链接选项
ldflags = [
{% for flag in linker.flags %}
  "{{ flag }}",
{% endfor %}
]

# 宏定义
defines = [
{% for macro in compiler.defines %}
  "{{ macro }}",
{% endfor %}
]
```

### 2.2 工具链配置模板

```jinja2
{# build/lite/toolchain/{{ toolchain.type }}/toolchain.gni.j2 #}

# Toolchain configuration for {{ toolchain.type }}
# Target: {{ chip.architecture }}

toolchain("{{ toolchain.type }}") {
{% if toolchain.type == "gcc" %}
  prefix = "{{ toolchain.prefix }}"
  cc = "${prefix}gcc"
  cxx = "${prefix}g++"
  ar = "${prefix}ar"
  ld = "${prefix}ld"
  strip = "${prefix}strip"
  nm = "${prefix}nm"
  objcopy = "${prefix}objcopy"
  size = "${prefix}size"
{% elif toolchain.type == "clang" %}
  cc = "clang"
  cxx = "clang++"
  ar = "llvm-ar"
  ld = "lld"
  strip = "llvm-strip"
  nm = "llvm-nm"
  objcopy = "llvm-objcopy"
  size = "llvm-size"
  
  target_triple = "{{ toolchain.target_triple }}"
{% endif %}
  
  toolchain_args = {
    current_os = "{{ system.os }}"
    current_cpu = "{{ chip.core }}"
  }
}
```

## 3. 芯片层模板

### 3.1 SoC配置模板

```jinja2
{# device/soc/{{ chip.vendor }}/{{ chip.soc_name }}/config.gni.j2 #}

# SoC Configuration for {{ chip.name }}
# Vendor: {{ chip.vendor }}
# Core: {{ chip.core }}

# ==================== 芯片标识 ====================
soc_name = "{{ chip.soc_name }}"
soc_company = "{{ chip.vendor }}"
soc_series = "{{ chip.series }}"

# ==================== 核心参数 ====================
cpu_core = "{{ chip.core }}"
cpu_frequency_mhz = {{ chip.frequency_mhz }}
{% if chip.cache_size %}
cache_size_kb = {{ chip.cache_size }}
{% endif %}

# ==================== 内存映射 ====================
# Flash
flash_base_addr = {{ hex(chip.flash_base) }}
flash_size = {{ hex(chip.flash_size) }}
flash_page_size = {{ chip.flash_page_size }}

# SRAM
sram_base_addr = {{ hex(chip.sram_base) }}
sram_size = {{ hex(chip.sram_size) }}
{% if chip.has_dtcm %}
dtcm_base_addr = {{ hex(chip.dtcm_base) }}
dtcm_size = {{ hex(chip.dtcm_size) }}
{% endif %}

# ==================== 中断控制器 ====================
interrupt_controller = "{{ chip.interrupt_controller }}"
num_irq = {{ chip.num_irq }}
{% if chip.nvic_priority_bits %}
nvic_priority_bits = {{ chip.nvic_priority_bits }}
{% endif %}

# ==================== 时钟系统 ====================
clock_source = "{{ chip.clock_source }}"
{% if chip.pll_frequency %}
pll_frequency_mhz = {{ chip.pll_frequency }}
{% endif %}

# ==================== 外设基地址 ====================
{% for periph in chip.peripherals %}
{{ periph.name }}_BASE = {{ hex(periph.base_addr) }}
{% endfor %}
```

## 4. 单板层模板

### 4.1 单板配置模板

```jinja2
{# device/board/{{ board.vendor }}/{{ board.name }}/liteos_m/config.gni.j2 #}

# Board Configuration for {{ board.name }}
# Based on {{ chip.name }} SoC

# ==================== 单板标识 ====================
board_name = "{{ board.name }}"
board_company = "{{ board.vendor }}"
board_description = "{{ board.description }}"

# ==================== 引用SoC配置 ====================
import("//device/soc/{{ chip.vendor }}/{{ chip.soc_name }}/config.gni")

# ==================== 板级资源 ====================
{% if board.external_sram %}
external_sram_base = {{ hex(board.external_sram.base) }}
external_sram_size = {{ hex(board.external_sram.size) }}
{% endif %}

{% if board.external_flash %}
external_flash_base = {{ hex(board.external_flash.base) }}
external_flash_size = {{ hex(board.external_flash.size) }}
{% endif %}

# ==================== 引脚复用配置 ====================
{% for pin in board.pinmux %}
# {{ pin.function }}: {{ pin.pin }} -> {{ pin.peripheral }}
{{ pin.peripheral }}_{{ pin.function }}_PIN = "{{ pin.pin }}"
{% endfor %}

# ==================== 外设实例映射 ====================
{% for instance in board.peripheral_instances %}
{{ instance.type }}{{ instance.number }}_ENABLED = {{ instance.enabled | lower }}
{% if instance.dma_channel %}
{{ instance.type }}{{ instance.number }}_DMA_CHANNEL = {{ instance.dma_channel }}
{% endif %}
{% endfor %}

# ==================== 调试接口 ====================
debug_uart_instance = {{ board.debug_uart }}
debug_baudrate = {{ board.debug_baudrate }}
```

## 5. 产品层模板

### 5.1 产品配置模板

```jinja2
{# vendor/{{ product.vendor }}/{{ product.name }}/config.json.j2 #}
{# Lite系统产品配置模板 — 不使用inherit继承机制 #}
{
  "product_name": "{{ product.name }}",
  "version": "{{ product.version }}",
  "type": "{{ system.type }}",
  "ohos_version": "{{ product.ohos_version }}",
  "device_company": "{{ board.vendor }}",
  "board_company": "{{ board.vendor }}",
  "kernel_type": "{{ system.kernel }}",
  "kernel_version": "{{ system.kernel_version }}",
  "subsystems": [
{% for subsystem in product.subsystems %}
    {
      "subsystem": "{{ subsystem.name }}",
      "components": [
{% for component in subsystem.components %}
        {
          "component": "{{ component.name }}",
          "features": [
{% for feature in component.features %}
            "{{ feature }}"{% if not loop.last %},{% endif %}

{% endfor %}
          ]
        }{% if not loop.last %},{% endif %}

{% endfor %}
      ]
    }{% if not loop.last %},{% endif %}

{% endfor %}
  ]
}
```
