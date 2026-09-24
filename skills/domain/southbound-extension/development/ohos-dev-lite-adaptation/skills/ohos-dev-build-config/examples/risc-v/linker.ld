/*
 * RISC-V Linker Script for Hi3861V100 (truncated from 597-line hi3861_link.ld.S)
 * Retains: MEMORY regions + core SECTIONS (.init/.text/.data/.bss/.heap/.stack)
 */
OUTPUT_ARCH("riscv")
ENTRY(_start)

STACK_SIZE = 2K;  IRQ_STACK_SIZE = 3K;  EXC_STACK_SIZE = 2K;
#define ROM_RAM_LEN 13856   /* ROM_DATA0 + ROM_DATA1 + ROM_BSS + CHECK_INFO */
#define ROM_RAM_START (0x11DFFF - ROM_RAM_LEN + 1)
#define STACK_LEN (STACK_SIZE + IRQ_STACK_SIZE + EXC_STACK_SIZE)
#define STACK_VMA (ROM_RAM_START - STACK_LEN)
#define PATCH_BSS_START 0x00100000
#define NON_ROM_RAM_START (PATCH_BSS_START + 1024)

MEMORY
{
    ROM_TEXT(rx) : ORIGIN = 0x003b8000, LENGTH = 278K
    ROM_BSS(rwx) : ORIGIN = ROM_RAM_START, LENGTH = 11776
    STACK(rw)    : ORIGIN = STACK_VMA, LENGTH = STACK_LEN
    FLASH(rwx)   : ORIGIN = 0x00400000, LENGTH = 2M
    RAM(rwx)     : ORIGIN = NON_ROM_RAM_START, LENGTH = (1M - ROM_RAM_LEN - 1024 - STACK_LEN)
}

SECTIONS
{
    .text_rom : {
        . = ALIGN(0x20);
        KEEP(*(.text.download_entry))
        KEEP(*(.text.trap_download_vector))
    } > ROM_TEXT

    .text_non_rom : {
        . = ALIGN(0x20);
        KEEP(*(.entry.text))
        *(.init*)  *(.text*)
        . = ALIGN(0x20);
        *(.rodata*)
    } > FLASH

    .zInit : {
        KEEP(*(.zinitcall.*.init))
    } > FLASH

    .data : {
        . = ALIGN(0x20);
        __data_start = .;
        *(.data*)  *(.sdata*)
        . = ALIGN(0x20);
        __data_end = .;
    } > RAM

    .bss (NOLOAD) : ALIGN(0x20) {
        __bss_begin = .;
        *(.bss*)  *(.sbss*)
        . = ALIGN(0x20);
        __bss_end = .;
    } > RAM

    .heap (NOLOAD) : {
        . = ALIGN(64);
        __HEAP_BEGIN__ = ABSOLUTE(.);
    } > RAM

    .stack (NOLOAD) : ALIGN(0x20) {
        __SYSTEM_STACK_BEGIN__ = .;
        . += STACK_SIZE;
        __SYSTEM_STACK_END__ = .;
        . = ALIGN(0x20);
        __irq_stack_bottom = .;
        . += IRQ_STACK_SIZE;
        __irq_stack_top = .;
        . = ALIGN(0x20);
        __exc_stack_bottom = .;
        . += EXC_STACK_SIZE;
        __exc_stack_top = .;
    } > STACK
    end = .;
}
