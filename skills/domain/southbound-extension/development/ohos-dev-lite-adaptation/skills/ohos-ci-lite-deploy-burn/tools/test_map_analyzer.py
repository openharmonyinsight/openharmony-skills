#!/usr/bin/env python3
# coding=utf-8
"""map_analyzer.py 回归测试：GNU ld 真实格式 MAP fixture 对账。

覆盖：总量对账（ELF size -A 口径）、输入段不重复计数（缩进区分输出/输入段）、
空段跳过、换行段名、点号段名、未识别段归 other、重复段不双计（后值生效）、
compare 六桶 delta 对账。fixture 按 riscv32-unknown-elf-ld -Map 真实输出格式构造。

运行（两种入口等价）：
  python tools/test_map_analyzer.py
  python -m unittest discover -s skills/ohos-ci-lite-deploy-burn/tools -p "test_*.py"
"""

import importlib.util
import os
import shutil
import sys
import tempfile
import unittest

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("map_analyzer", os.path.join(HERE, "map_analyzer.py"))
ma = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ma)

# fixture：输出段在列 0；输入段缩进 1 格（parser 靠此区分，输入段不得计入总量）
FIXTURE1 = """Archive member included to satisfy reference by file (symbol)

Memory Configuration

Name             Origin             Length             Attributes
FLASH            0x0000000008000000 0x00080000         xr
RAM              0x0000000020000000 0x00010000        xrw


Linker script and memory map

.isr_vector      0x0000000008000000     0x400
 *(.isr_vector)
 .isr_vector     0x0000000008000000     0x400  startup.o

.text            0x0000000008000400    0x1234
 *(.text*)
 .text.startup.main
                    0x0000000008000400     0x100  main.o
 .text.hilink    0x0000000008000500      0xf0  hilink.o
 0x0000000008000400                main

.init           0x0000000008001700      0x34
                0x0000000008001700                __libc_init_array

.very_long_output_section_name
                0x0000000008001800     0x100
 .rom.patch.tab
                    0x0000000008001800     0x100  patch.o

.rom.patch.extra 0x0000000008001900     0x80
 *fill*          0x0000000008001980      0x8

.rodata         0x0000000008002000     0x220
 .rodata.str1.1
                    0x0000000008002000     0x220  main.o

.sdata          0x0000000020000000      0x60
 .sdata.gdt     0x0000000020000000      0x60  gdt.o

.data           0x0000000020000100     0x100
 *(.data*)
 .data.nvram    0x0000000020000100     0x100  nvram.o

.sbss           0x0000000020000300      0x40
 .sbss.dummy    0x0000000020000300      0x40  dummy.o

.bss            0x0000000020000400     0x200
 *(.bss*)
 .bss.extra     0x0000000020000400     0x200  extra.o
 0x0000000020000400                g_idle_task

.bss.empty      0x0000000020000800       0x0
 .bss.zero      0x0000000020000800       0x0  zero.o

.ARM.exidx      0x0000000020001000      0x10
 *(.ARM.exidx*)

Discarded input sections
 .comment        0x0000000000000000      0x2e
"""

# fixture2：.text +0x1000；.bss 0x200→0x180；.sbss 删除；新增 .rom.patch.new 0x400
FIXTURE2 = FIXTURE1.replace('.text            0x0000000008000400    0x1234',
                            '.text            0x0000000008000400    0x2234')
FIXTURE2 = FIXTURE2.replace('.bss            0x0000000020000400     0x200',
                            '.bss            0x0000000020000400     0x180')
FIXTURE2 = FIXTURE2.replace('.sbss           0x0000000020000300      0x40\n .sbss.dummy    0x0000000020000300      0x40  dummy.o\n\n', '')
FIXTURE2 = FIXTURE2.replace('.rodata         0x0000000008002000     0x220',
                            '.rom.patch.new  0x0000000008001a00     0x400\n\n.rodata         0x0000000008002000     0x220')

# 重复段 fixture：.text 出现两次（0x1234 与 0x5678）——总量不得双计（后值生效）
FIXTURE_DUP = FIXTURE1 + '\n.text            0x0000000020002000    0x5678\n'


class MapFixtureTestBase(unittest.TestCase):
    """公共：setUpClass 写 fixture 到临时目录，tearDownClass 清理。"""

    tmpdir = None

    @classmethod
    def write_fixtures(cls):
        cls.tmpdir = tempfile.mkdtemp(prefix="map_analyzer_test_")
        paths = {}
        for name, content in (("v1", FIXTURE1), ("v2", FIXTURE2), ("dup", FIXTURE_DUP)):
            p = os.path.join(cls.tmpdir, "fixture_gnuld_%s.map" % name)
            with open(p, "w", encoding="utf-8") as f:
                f.write(content)
            paths[name] = p
        return paths

    @classmethod
    def cleanup_fixtures(cls):
        if cls.tmpdir:
            shutil.rmtree(cls.tmpdir, ignore_errors=True)
            cls.tmpdir = None


class TestAnalyzeSingleMap(MapFixtureTestBase):
    """单 MAP 对账：期望值按输出段 size -A 口径手算自 fixture 输出段表。"""

    @classmethod
    def setUpClass(cls):
        cls.paths = cls.write_fixtures()
        cls.a1 = ma.analyze_single_map(cls.paths["v1"])

    @classmethod
    def tearDownClass(cls):
        cls.cleanup_fixtures()

    def test_summary_buckets_and_total(self):
        # code  = .text 0x1234 + .init 0x34 = 0x1268；data = .data 0x100 + .sdata 0x60 = 0x160
        # bss   = .bss 0x200 + .sbss 0x40 = 0x240；rodata = .rodata 0x220
        # other = .isr_vector 0x400 + .very_long... 0x100 + .rom.patch.extra 0x80 + .ARM.exidx 0x10 = 0x590
        s = self.a1["summary"]
        self.assertEqual(s["code"], 0x1268)
        self.assertEqual(s["data"], 0x160)
        self.assertEqual(s["bss"], 0x240)
        self.assertEqual(s["rodata"], 0x220)
        self.assertEqual(s["other"], 0x590, "未识别段应全量归入 other")
        self.assertEqual(s["total"], 0x1DB8, "总量与输出段 size -A 口径对账")

    def test_section_inventory(self):
        sec = self.a1["sections"]
        self.assertEqual(len(sec), 11, "空段 .bss.empty 不计")
        self.assertEqual(sec.get(".very_long_output_section_name", {}).get("size"), 0x100,
                         "换行段名必须计入")
        self.assertEqual(sec.get(".rom.patch.extra", {}).get("size"), 0x80, "点号段名必须计入")
        self.assertNotIn(".bss.empty", sec, "空段不记录")
        self.assertNotIn(".text.startup.main", sec, "输入段（缩进）不得计入")
        self.assertNotIn(".bss.extra", sec, "输入段不得计入")

    def test_total_invariant(self):
        self.assertEqual(self.a1["summary"]["total"],
                         sum(i["size"] for i in self.a1["sections"].values()),
                         "对账核心不变量：total == sum(sections.size)")


class TestCompareMaps(MapFixtureTestBase):
    """compare 对账：v1 → v2 已知 delta。"""

    @classmethod
    def setUpClass(cls):
        cls.paths = cls.write_fixtures()
        cls.cmp = ma.compare_maps(cls.paths["v1"], cls.paths["v2"])

    @classmethod
    def tearDownClass(cls):
        cls.cleanup_fixtures()

    def test_summary_deltas(self):
        d = self.cmp["summary_diff"]
        self.assertEqual(d["code"], 0x1000, ".text +0x1000")
        self.assertEqual(d["data"], 0)
        self.assertEqual(d["bss"], -0xC0, ".bss -0x80 与 .sbss 删除 -0x40")
        self.assertEqual(d["rodata"], 0)
        self.assertEqual(d["other"], 0x400, "新增 .rom.patch.new")
        self.assertEqual(d["total"], 0x1340, "+0x1000 -0xC0 +0x400 = 0x1340")

    def test_added_removed_sections(self):
        self.assertEqual(self.cmp["added_sections"], [".rom.patch.new"])
        self.assertEqual(self.cmp["removed_sections"], [".sbss"])

    def test_section_changes(self):
        ch = {x["section"]: x["diff"] for x in self.cmp["changes"]}
        self.assertEqual(ch.get(".text"), 0x1000)
        self.assertEqual(ch.get(".bss"), -0x80)


class TestDuplicateSections(MapFixtureTestBase):
    """重复段：不双计（后值生效，行为记录在案）。"""

    @classmethod
    def setUpClass(cls):
        cls.paths = cls.write_fixtures()
        cls.ad = ma.analyze_single_map(cls.paths["dup"])

    @classmethod
    def tearDownClass(cls):
        cls.cleanup_fixtures()

    def test_no_double_count(self):
        self.assertEqual(self.ad["sections"][".text"]["size"], 0x5678,
                         "重复 .text 取后值，不双计")

    def test_total_invariant_with_dup(self):
        self.assertEqual(self.ad["summary"]["total"],
                         sum(i["size"] for i in self.ad["sections"].values()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
