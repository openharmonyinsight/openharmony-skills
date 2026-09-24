/*
 * Copyright (c) 2022-2022 Huawei Device Co., Ltd. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice, this list of
 *    conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice, this list
 *    of conditions and the following disclaimer in the documentation and/or other materials
 *    provided with the distribution.
 *
 * 3. Neither the name of the copyright holder nor the names of its contributors may be used
 *    to endorse or promote products derived from this software without specific prior written
 *    permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
 * OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
 * OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
 * ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

OUTPUT_FORMAT("elf32-littlearm", "elf32-bigarm", "elf32-littlearm")
OUTPUT_ARCH(arm)
ENTRY(g_bootVectors)

SVC_IRQ_STACK_SIZE  = 4K;

FLASH_START         = 0x08000000;
FLASH_SIZE          = 1M;

PS_RAM_START        = 0x20000000;
PS_RAM_SIZE         = 128K;

MEMORY
{
    flash(rx) : ORIGIN = FLASH_START, LENGTH = FLASH_SIZE
    ram(rwx) : ORIGIN = PS_RAM_START, LENGTH = PS_RAM_SIZE
}

SECTIONS
{
    _stext = .;
    .vector : {
        KEEP (*(SORT_NONE(.reset)))
    } > flash

    .got : {
        *(.got.plt)
        *(.igot.plt)
        *(.got)
        *(.igot)
    } > flash

    .text : {
        . = ALIGN(0x4);
        __text_start = .;
        *(.text.*)
        . = ALIGN(0x4);
        _etext = .;
        *(.rodata .rodata.* .gnu.linkonce.r.*)
        *(.rodata1)
    } > flash

    .zInit (.) : {
        . = ALIGN(4);
        __zinitcall_bsp_start = .;
        KEEP (*(.zinitcall.bsp0.init))
        KEEP (*(.zinitcall.bsp1.init))
        KEEP (*(.zinitcall.bsp2.init))
        KEEP (*(.zinitcall.bsp3.init))
        KEEP (*(.zinitcall.bsp4.init))
        __zinitcall_bsp_end = .;
        . = ALIGN(4);
        __zinitcall_device_start = .;
        KEEP (*(.zinitcall.device0.init))
        KEEP (*(.zinitcall.device1.init))
        KEEP (*(.zinitcall.device2.init))
        KEEP (*(.zinitcall.device3.init))
        KEEP (*(.zinitcall.device4.init))
        __zinitcall_device_end = .;
        . = ALIGN(4);
        __zinitcall_core_start = .;
        KEEP (*(.zinitcall.core0.init))
        KEEP (*(.zinitcall.core1.init))
        KEEP (*(.zinitcall.core2.init))
        KEEP (*(.zinitcall.core3.init))
        KEEP (*(.zinitcall.core4.init))
        __zinitcall_core_end = .;
        . = ALIGN(4);
        __zinitcall_sys_service_start = .;
        KEEP (*(.zinitcall.sys.service0.init))
        KEEP (*(.zinitcall.sys.service1.init))
        KEEP (*(.zinitcall.sys.service2.init))
        KEEP (*(.zinitcall.sys.service3.init))
        KEEP (*(.zinitcall.sys.service4.init))
        __zinitcall_sys_service_end = .;
        . = ALIGN(4);
        __zinitcall_sys_feature_start = .;
        KEEP (*(.zinitcall.sys.feature0.init))
        KEEP (*(.zinitcall.sys.feature1.init))
        KEEP (*(.zinitcall.sys.feature2.init))
        KEEP (*(.zinitcall.sys.feature3.init))
        KEEP (*(.zinitcall.sys.feature4.init))
        __zinitcall_sys_feature_end = .;
        . = ALIGN(4);
        __zinitcall_run_start = .;
        KEEP (*(.zinitcall.run0.init))
        KEEP (*(.zinitcall.run1.init))
        KEEP (*(.zinitcall.run2.init))
        KEEP (*(.zinitcall.run3.init))
        KEEP (*(.zinitcall.run4.init))
        __zinitcall_run_end = .;
        . = ALIGN(4);
        __zinitcall_app_service_start = .;
        KEEP (*(.zinitcall.app.service0.init))
        KEEP (*(.zinitcall.app.service1.init))
        KEEP (*(.zinitcall.app.service2.init))
        KEEP (*(.zinitcall.app.service3.init))
        KEEP (*(.zinitcall.app.service4.init))
        __zinitcall_app_service_end = .;
        . = ALIGN(4);
        __zinitcall_app_feature_start = .;
        KEEP (*(.zinitcall.app.feature0.init))
        KEEP (*(.zinitcall.app.feature1.init))
        KEEP (*(.zinitcall.app.feature2.init))
        KEEP (*(.zinitcall.app.feature3.init))
        KEEP (*(.zinitcall.app.feature4.init))
        __zinitcall_app_feature_end = .;
        . = ALIGN(4);
        __zinitcall_test_start = .;
        KEEP (*(.zinitcall.test0.init))
        KEEP (*(.zinitcall.test1.init))
        KEEP (*(.zinitcall.test2.init))
        KEEP (*(.zinitcall.test3.init))
        KEEP (*(.zinitcall.test4.init))
        __zinitcall_test_end = .;
        . = ALIGN(4);
        __zinitcall_exit_start = .;
        KEEP (*(.zinitcall.exit0.init))
        KEEP (*(.zinitcall.exit1.init))
        KEEP (*(.zinitcall.exit2.init))
        KEEP (*(.zinitcall.exit3.init))
        KEEP (*(.zinitcall.exit4.init))
        __zinitcall_exit_end = .;
        . = ALIGN(4);
    } > flash

    .data : {
        __data_start = . ;
        g_data_start = . ;
        KEEP (*(SORT_NONE(VECTOR)))

        *(.data .data.* .gnu.linkonce.d.*)

        . = ALIGN(0x4);
        _hdf_drivers_start = .;
        KEEP(*(.hdf.driver))
        _hdf_drivers_end = .; /* define a section for hdf driver */
        
        __data_end = . ;
        g_data_end = . ;
    } > ram AT > flash

    data_load_start = LOADADDR(.data);

    .bss : ALIGN(0x4) {
        __bss_start = .;
        g_bssStart = .;
        *(.dynbss)
        *(.bss .bss.* .gnu.linkonce.b.*)
        *(COMMON)
        . = ALIGN(0x4);
        __bss_end = .;
        g_bssEnd = .;
    } > ram

    _sstack = .;
    .stack : ALIGN(0x8) {
        _stack = .;
        g_stackStart = .;
        __irq_stack_bootom = .;
        . += SVC_IRQ_STACK_SIZE;
        __irq_stack_top = .;
        g_stackEnd = .;
        _estack = .;
    } > ram

    .heap (NOLOAD): ALIGN(0x40) {
        __heap_start = .;
    } > ram

    __heap_size = PS_RAM_SIZE - (__heap_start - __data_start);
    end = .;
    /DISCARD/ : { *(.note.GNU-stack) *(.gnu_debuglink) *(.gnu.lto_*) }
}
