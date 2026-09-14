> **Scope**: ARM Cortex-M 和 RISC-V MCU 链接脚本模板
> **When**: 需要生成 linker.ld 链接脚本时读取
> **Size**: ~210 lines

---

## 栈/堆大小默认值策略

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `__stack_size` | 0x1000 (4KB) | 栈空间，从 RAM 高地址向低地址增长 |
| `__heap_size` | 0x2000 (8KB) | 堆空间，用于 malloc 动态分配 |

**小内存设备调整建议（RAM < 64KB）**：
- 栈：降至 0x800 (2KB)，需确保无深层递归和大型局部数组
- 堆：降至 0x1000 (4KB)，减少动态内存分配频率
- 参考公式：`栈 ≥ max(2048, RAM/16)`，`堆 ≥ max(4096, RAM/8)`

**向量表大小计算公式**：
```
向量表大小 = (中断数量 + 16) × 4 字节
例：STM32F407 有 82 个中断 → (82 + 16) × 4 = 392 字节
```

---

## ARM Cortex-M 链接脚本模板

```ld
/*
 * Linker Script for {{chip_name}}
 * Architecture: ARM Cortex-M ({{cpu_type}})
 */

/* ==================== 内存区域定义 ==================== */
MEMORY
{
    /* Flash 存储区 (只读+可执行) */
    FLASH (rx)  : ORIGIN = {{flash_base}}, LENGTH = {{flash_size}}

    /* RAM 读写区 (可读+可写+可执行) */
    RAM (xrw)   : ORIGIN = {{ram_base}}, LENGTH = {{ram_size}}
}

/* ==================== 栈和堆大小 ==================== */
__stack_size = {{stack_size | "0x1000"}};  /* 默认 4KB */
__heap_size = {{heap_size | "0x2000"}};    /* 默认 8KB */

/* ==================== 入口点 ==================== */
ENTRY(Reset_Handler)

/* ==================== 段定义 ==================== */
SECTIONS
{
    /* ===== 中断向量表 (必须位于 Flash 起始) ===== */
    .vectors :
    {
        . = ALIGN(4);
        KEEP(*(.vectors))
        KEEP(*(.reset))
        . = ALIGN(4);
    } > FLASH

    /* ===== 代码段 ===== */
    .text :
    {
        . = ALIGN(4);
        __text_start = .;

        *(.text)
        *(.text*)
        *(.glue_7)
        *(.glue_7t)

        KEEP(*(.init))
        KEEP(*(.fini))

        . = ALIGN(4);
        __text_end = .;
    } > FLASH

    /* ===== 只读数据段 ===== */
    .rodata :
    {
        . = ALIGN(4);
        *(.rodata)
        *(.rodata*)
        . = ALIGN(4);
    } > FLASH

    /* ===== ARM 异常展开表 ===== */
    .ARM.extab :
    {
        *(.ARM.extab* .gnu.linkonce.armextab.*)
    } > FLASH

    .ARM.exidx :
    {
        __exidx_start = .;
        *(.ARM.exidx* .gnu.linkonce.armexidx.*)
        __exidx_end = .;
    } > FLASH

    /* ===== 已初始化数据段 (运行时在 RAM，加载时在 Flash) ===== */
    _sidata = LOADADDR(.data);
    .data :
    {
        . = ALIGN(4);
        __data_start__ = .;
        _sdata = .;

        *(.data)
        *(.data*)

        . = ALIGN(4);
        __data_end__ = .;
        _edata = .;
    } > RAM AT > FLASH

    /* ===== 未初始化数据段 (BSS) ===== */
    .bss :
    {
        . = ALIGN(4);
        __bss_start = .;
        _sbss = .;

        *(.bss)
        *(.bss*)
        *(COMMON)

        . = ALIGN(4);
        __bss_end = .;
        _ebss = .;
    } > RAM

    /* ===== 堆区 ===== */
    .heap :
    {
        . = ALIGN(8);
        __heap_start = .;
        PROVIDE(end = .);
        PROVIDE(_end = .);
        . = . + __heap_size;
        __heap_end = .;
    } > RAM

    /* ===== 栈区 (从高地址向低地址增长) ===== */
    .stack :
    {
        . = ALIGN(8);
        __stack_bottom = .;
        . = . + __stack_size;
        __stack_top = .;
        _estack = .;
    } > RAM

    /DISCARD/ :
    {
        libc.a(*)
        libm.a(*)
        libgcc.a(*)
    }

    .ARM.attributes 0 : { *(.ARM.attributes) }
}

/* ==================== 断言检查 ==================== */
ASSERT(__stack_top <= ORIGIN(RAM) + LENGTH(RAM),
       "ERROR: Stack overflows RAM boundary")
ASSERT(__heap_end <= __stack_bottom,
       "ERROR: Heap collides with stack")
```

---

## RISC-V 链接脚本模板

```ld
/*
 * Linker Script for {{chip_name}}
 * ISA: {{isa_string}} (e.g. rv32imac)
 */

OUTPUT_ARCH(riscv)
ENTRY(_start)

/* ==================== 内存区域定义 ==================== */
MEMORY
{
    FLASH (rxai!w) : ORIGIN = {{flash_base}}, LENGTH = {{flash_size}}
    RAM (wxa!ri)   : ORIGIN = {{ram_base}}, LENGTH = {{ram_size}}
}

/* ==================== 段定义 ==================== */
SECTIONS
{
    /* ===== 启动代码和向量表 ===== */
    .init :
    {
        KEEP(*(.init))
        KEEP(*(.vector_table))
    } > FLASH

    /* ===== 代码段 ===== */
    .text : ALIGN(4)
    {
        __text_start = .;
        *(.text.unlikely .text.*_unlikely .text.unlikely.*)
        *(.text.exit .text.exit.*)
        *(.text.startup .text.startup.*)
        *(.text.hot .text.hot.*)
        *(.text .stub .text.* .gnu.linkonce.t.*)
        KEEP(*(.text.*personality*))
        *(.gnu.warning)
        . = ALIGN(4);
        __text_end = .;
    } > FLASH

    /* ===== 只读数据段 ===== */
    .rodata : ALIGN(4)
    {
        *(.rodata .rodata.* .gnu.linkonce.r.*)
        *(.rodata1)
        . = ALIGN(4);
    } > FLASH

    /* ===== 已初始化数据段 ===== */
    .data : ALIGN(4)
    {
        __DATA_BEGIN__ = .;
        *(.data .data.* .gnu.linkonce.d.*)
        SORT(CONSTRUCTORS)
        . = ALIGN(4);
        __DATA_END__ = .;
    } > RAM AT > FLASH

    __DATA_LOAD__ = LOADADDR(.data);

    /* ===== 未初始化数据段 (BSS) ===== */
    .bss (NOLOAD) : ALIGN(4)
    {
        __BSS_BEGIN__ = .;
        *(.dynbss)
        *(.bss .bss.* .gnu.linkonce.b.*)
        *(COMMON)
        . = ALIGN(4);
        __BSS_END__ = .;
    } > RAM

    /* ===== 堆区 ===== */
    .heap (NOLOAD) : ALIGN(8)
    {
        __heap_start = .;
        . += {{heap_size | "0x2000"}};
        __heap_end = .;
    } > RAM

    /* ===== 栈区 (RISC-V 要求 16 字节对齐) ===== */
    .stack (NOLOAD) : ALIGN(16)
    {
        __stack_bottom = .;
        . += {{stack_size | "0x1000"}};
        __stack_top = .;
    } > RAM
}
```

---

## 段对齐策略参考

| 段类型 | ARM 对齐 | RISC-V 对齐 | 说明 |
|-------|---------|-----------|------|
| `.vectors` / `.init` | 4 字节 | 4 字节 | 向量表/启动代码 |
| `.text` | 4 字节 | 4 字节 | 指令对齐 |
| `.rodata` | 4 字节 | 4 字节 | 只读数据 |
| `.data` | 4 字节 | 4 字节 | 已初始化数据 |
| `.bss` | 4 字节 | 4 字节 | 未初始化数据 |
| `.stack` | 8 字节 | **16 字节** | RISC-V 要求 16 字节栈对齐 |
| `.heap` | 8 字节 | 8 字节 | 动态内存分配对齐 |

## 真实链接脚本参考

本模板是通用格式。如需参照真实芯片的链接脚本：
- 本 SKILL 的 `examples/l0/hi3861/` 目录有 Hi3861 真实 linker.ld / link.ld.S
- 也可在项目中搜索 `.ld` 文件或联网查找对应芯片的 OpenHarmony 适配仓库

- `linker-scripts/stm32f407_rtos.ld` — STM32F407 ARM Cortex-M，含 MEMORY/SECTIONS/向量表
- `linker-scripts/hi3861_link.ld.S` — Hi3861 RISC-V，含 `#ifdef` 条件编译
- `linker-scripts/hi3861_system_config.ld.S` — Hi3861 系统配置段（zinitcall 等）

真实示例展示了 ARM/RISC-V 两种架构的完整链接脚本，与本模板格式一致。
