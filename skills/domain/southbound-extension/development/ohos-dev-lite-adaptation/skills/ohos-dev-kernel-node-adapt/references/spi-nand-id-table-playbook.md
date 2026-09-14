# SPI Nand ID 表两侧补 playbook

> 板载 SPI Nand 颗粒不在 SoC 厂商 ID 表 → uboot 侧 `pagesize 8192` BUG / 内核侧 `bsp_spi_nand_probe error -19`(-ENODEV) → UBI/rootfs 起不来。**驱动适配层的活**——补 ID 表条目。来源：hi3516cv610 实战（案例 BG003，DS35Q1GB-IB）。

## 症状（两侧不同）

板载 SPI Nand 颗粒 DS35Q1GB-IB（read id = `0xe5,0xf1`），uboot 与内核两侧表现不同：

- **uboot 侧**：`spi_nand_get_flash_info` 查 ID 表返回 NULL → 回退通用 NAND ID 表误算 pagesize=8192 → `fmc100.c:838 BUG: Driver does not support pagesize 8192`（颗粒实际 2KB page / 128B OOB）。
- **内核侧**：ID 表查不到该颗粒 → `cannot found in spi nand id table` → `bsp_spi_nand_probe error -19` (-ENODEV) → UBI 挂不上 / rootfs 起不来。

## 根因

板载颗粒 ID（`0xe5,0xf1`）不在海思 SPI Nand ID 表 `fmc_spi_nand_flash_table[]`（表里只有 HY035 `0xe5,0xf2` + HY073 `0xe5,0x73` 等，没有 `0xe5,0xf1`）。颗粒不在表 → uboot 回退通用表误算 pagesize / 内核直接 probe 失败。

## ⚠️ 关键：uboot 与内核是两份独立的 ID 表

| 侧 | 源文件路径（hi3516cv610） |
|----|------------------------|
| uboot | `drivers/mtd/nand/raw/fmc100/fmc_ids_hi3516cv610.c` |
| 内核 | `drivers/mtd/nand/fmc100/fmc_ids_hi3516cv610.c` |

两者路径只差一层（`raw/` vs 无），但是**两份独立的源文件**。补颗粒必须**两侧都补**：
- 只补 uboot 侧 → uboot 识别但内核 probe -19 失败。
- 只补内核侧 → 内核通但 uboot 报 `pagesize 8192` BUG。

## 适配操作

### 1. 抓颗粒 ID

uboot 启动早期打印 `spi nand id: 0xe5 0xf1`，或读 JEDEC ID。`0xe5`=厂商前缀，`0xf1`=颗粒型号。

### 2. grep 确认不在表（两侧都查）

```bash
# 两侧都 grep
grep -rn "0xe5" drivers/mtd/nand/raw/fmc100/fmc_ids_hi3516cv610.c   # uboot
grep -rn "0xe5" drivers/mtd/nand/fmc100/fmc_ids_hi3516cv610.c        # 内核
```
发现只有 `0xe5,0xf2`（HY035）+ `0xe5,0x73`（HY073），没有 `0xe5,0xf1` → 确认不在表。

### 3. 照抄同规格条目改 id（两侧都补）

找同表同厂商前缀（`0xe5`）、同 pagesize/OOB 的现有条目（如 HY035，2KB page/128B OOB）复制，**只改 id + name**，参数按颗粒规格书核对：

```c
// uboot: drivers/mtd/nand/raw/fmc100/fmc_ids_hi3516cv610.c
// 内核: drivers/mtd/nand/fmc100/fmc_ids_hi3516cv610.c
// 在 fmc_spi_nand_flash_table[] 中照抄同 0xe5 厂商前缀的 HY035 条目，
// 把 id 改成 DS35Q1GB-IB 的 0xe5,0xf1，其余参数与颗粒规格书对齐：
{
    .name       = "DS35Q1GB-IB",
    .id_data    = {0xe5, 0xf1},       /* ← 改这里：原 HY035 是 0xe5,0xf2 */
    .chipsize   = SZ_128M,            /* 按颗粒规格书填 */
    .pagesize   = SZ_2K,              /* 2KB，不是误算的 8192 */
    .oobsize    = 128,                /* 128B OOB */
    /* ... 其余字段照抄 HY035 条目，按 DS35Q1GB-IB 规格书核对 */
},
```

> **别从零写条目**——ID 表字段多（chipsize/pagesize/oobsize/blocksize/...）易错，照抄同规格现有条目只改 id + name 最稳。

### 4. 颗粒无 datasheet 时以 runtime print 为权威

颗粒 datasheet 不公开 / 查不到 page/OOB/容量时，**以能跑的 bin 的 runtime print 为权威**，别猜：
1. 找一个在该颗粒上**能正常跑**的 u-boot / 内核 bin（厂商 SDK / 参考板 / 同颗粒别的板子）。
2. 烧上去启动，看 runtime 打印的颗粒规格（`Page:2KB OOB:128B` / `pagesize 2048 oobsize 128`）。
3. 以 runtime print 的实际值为权威填进 ID 表。datasheet 查不到就别查了，runtime 实测 > datasheet（datasheet 也可能印错/版本不符）。

### 5. 重编两侧 + 重烧

```bash
# 重编 uboot（含 gslboot_build）
make LIB_TYPE=musl CHIP=hi3516cv610 BOOT_MEDIA=spi_nand DEBUG=1 gslboot_build
# 重编内核
./build.sh ...
```
重烧 boot + kernel 分区。两侧识别该颗粒，UBI/rootfs 起来。

## 原则

- **报错字面提到 id table / probe 失败 / pagesize 异常 → 优先查 SPI Nand/NOR ID 表有没有板载颗粒**（颗粒 ID 不在表是常见根因）。
- **uboot 与内核的 ID 表是两份独立的源文件**（`raw/fmc100/` vs `fmc100/`，路径差一层），补颗粒**两侧都要补**。
- **补条目照抄同表同规格条目改 id**——同厂商前缀、同 pagesize/OOB 的现有条目复制，只改 id + name，参数按规格书核对。别从零写。
- **pagesize 8192 BUG 是 ID 表查不到回退通用表误算的典型症状**——8192 不是颗粒真实 pagesize，是回退路径默认值。看到 `Driver does not support pagesize 8192` 别去改驱动支持 8192，先查颗粒 ID 在不在表。
- **runtime print 优先于 datasheet**——颗粒规格查不到时以能跑的 bin 的 runtime print 为权威，别猜。关联 `../ohos-issue-lite-diagnose/references/fault-knowledge-base.md` §7.3。
- **先联网搜再查源码**：搜「报错原文 + 芯片/SDK」看别人遇到过吗，再查参考仓源码 + 加打印验证。关联 memory `search-then-verify-in-source`、`add-debug-prints-for-diagnosis`。
- **改烧录件记 changelog**：重编 boot/kernel 烧录后更新 `CHANGES_*.md`，关联 memory `update-changelog-after-burnfile-change`。

## SPI Nor 同理

SPI Nor 颗粒不在 ID 表（如 `spi_nor_ids[]`）同样 probe 失败，补法相同：抓 JEDEC ID → grep 确认不在表 → 照抄同厂商前缀同规格条目改 id。uboot 与内核两侧 ID 表同样独立，两侧都补。

## 关联

- `../ohos-issue-lite-diagnose/references/diagnostic-cases.md` §8 案例BG003（DS35Q1GB ID 表完整诊断）
- `../ohos-issue-lite-diagnose/references/fault-knowledge-base.md` §7.3 颗粒规格 runtime 证据优先
- `{{ASSET_ROOT}}/workflow/steps/03-driver-device/SKILL.md` §SPI Nand 驱动适配（板载颗粒 ID 表补条目两侧）
- `../ohos-ci-lite-deploy-burn/SKILL.md`「板载 SPI Nand 颗粒不在 ID 表」（烧录症状处置）
