---
name: ohos-dev-mmi-ram-rom-measurement
description: Use when measuring RAM/ROM impact of OpenHarmony multimodal input (MMI) subsystem changes on DAYU200 (RK3568). Covers ROM measurement via readelf section analysis and file size comparison, RAM measurement via /proc/PID/smaps, smaps_rollup, hidumper --mem, and baseline/current .so swap methodology.
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: mmi
  capability: ram-rom-measurement
  version: 0.1.0
  status: draft
  tags:
    - multimodalinput
    - ram
    - rom
    - performance
    - binary-size
  related-skills:
    - ohos-dev-mmi-device-test-harness
---

# MMI RAM/ROM 影响度量

衡量 multimodalinput 子系统代码变更前后的 ROM（二进制体积）和 RAM（运行时内存）占用变化。

**前置 skill**: 编译部署、设备连接等基础设施见 `ohos-dev-mmi-device-test-harness`。

## When to Use

- 提交 PR 前需要量化代码变更对二进制体积的影响
- 需要证明重构/新特性不引入内存膨胀
- 评审要求提供 RAM/ROM 数据

## 度量目标库

multimodalinput 进程加载的核心 .so：

| 库 | 角色 | 部署路径 |
|----|------|---------|
| `libmmi-server.z.so` | 服务端主逻辑 | `/system/lib/` |
| `libmmi-server-common.z.so` | 服务端公共 | `/system/lib/` |
| `libmmi-util.z.so` | 工具库 | `/system/lib/` |
| `libmmi-client.z.so` | 客户端库（不在 server 进程中） | `/system/lib/` |

**注意**：`libmmi-client.z.so` 不在 multimodalinput 服务端进程中加载，ROM 变化不影响服务端 RAM。

## ROM 度量方法

### 1. 文件级对比（快速）

```bash
# 构建输出路径
BUILD_OUT="code/out/rk3568/multimodalinput/input"

# 基线文件来自设备上的 .bak 备份或 CI 基线构建
ls -la $BUILD_OUT/libmmi-*.z.so
```

### 2. 段级对比（精确，推荐）

使用 `readelf -S` 分析关键段：

```bash
readelf -S libmmi-server.z.so | grep -E '\.text|\.rodata|\.data|\.bss'
```

| 段 | 含义 | 影响 |
|----|------|------|
| `.text` | 可执行代码 | 直接影响 ROM；映射为 shared clean 影响 RAM PSS |
| `.rodata` | 只读数据（字符串常量等） | 影响 ROM 和 shared clean PSS |
| `.data` | 已初始化全局变量 | 影响 ROM 和 private dirty |
| `.bss` | 零初始化全局变量 | 不影响 ROM；影响 anonymous RAM |
| `.data.rel.ro` | 重定位后只读 | 影响 ROM |

### 3. 基线获取策略

**方案 A：设备 .bak 文件**（推荐）

部署修改版 .so 前，先备份原始 .so：

```bash
$HDC shell "cp /system/lib/libmmi-server.z.so /data/local/tmp/libmmi-server.z.so.bak"
# 部署新 .so...
# 之后拉取基线
$HDC file recv /data/local/tmp/libmmi-server.z.so.bak ./libmmi-server.z.so.bak
```

**方案 B：CI 基线构建**

从 CI 每日构建镜像中提取同版本 .so 作为基线。

## RAM 度量方法

### 1. 找到进程 PID

```bash
$HDC shell "pidof multimodalinput"
```

### 2. smaps_rollup（进程级汇总）

```bash
$HDC shell "cat /proc/<PID>/smaps_rollup"
```

关键字段：
- **Pss**: 按共享比例分摊后的实际物理内存（最能反映真实占用）
- **Rss**: 驻留物理内存（包含共享页全量）
- **Size**: 虚拟地址空间大小

### 3. smaps per-library PSS

```bash
# 提取 libmmi 相关库的 PSS
$HDC shell "cat /proc/<PID>/smaps" > smaps.txt
# 解析：每个 mapping 的 header 行包含 .so 路径，后续行有 Pss
```

解析脚本：

```python
import re
current_lib = None
pss_by_lib = {}
for line in open("smaps.txt"):
    m = re.search(r'(/system/lib\S*libmmi\S+\.so)', line)
    if m:
        current_lib = m.group(1).split('/')[-1]
    m = re.match(r'Pss:\s+(\d+)\s+kB', line)
    if m and current_lib:
        pss_by_lib[current_lib] = pss_by_lib.get(current_lib, 0) + int(m.group(1))
for lib, pss in sorted(pss_by_lib.items()):
    print(f"  {lib}: {pss} kB")
```

### 4. hidumper --mem（系统级）

```bash
$HDC shell "hidumper --mem <PID>"
```

输出包含：native heap、.so mmap PSS、total PSS 等分类。

### 5. 基线 RAM 获取

**精确方法**：临时恢复 .bak .so → 重启服务 → 采集 → 恢复修改版 .so

```bash
# 1. 备份当前修改版
$HDC shell "mount -o rw,remount /system"
$HDC shell "cp /system/lib/libmmi-server.z.so /data/local/tmp/libmmi-server.z.so.new"

# 2. 恢复基线
$HDC shell "cp /data/local/tmp/libmmi-server.z.so.bak /system/lib/libmmi-server.z.so"
$HDC shell "reboot"
# 等待重启...

# 3. 采集基线 RAM
$HDC shell "pidof multimodalinput"  # 获取新 PID
$HDC shell "cat /proc/<PID>/smaps_rollup"

# 4. 恢复修改版
$HDC shell "mount -o rw,remount /system"
$HDC shell "cp /data/local/tmp/libmmi-server.z.so.new /system/lib/libmmi-server.z.so"
$HDC shell "reboot"
```

**估算方法**（不需要重启）：

基于段级分析推算 RAM 变化：
- `.text` + `.rodata` 差值 → 影响 shared clean PSS
- `.bss` 差值 → 影响 anonymous 内存
- `.data` 差值 → 影响 private dirty

当段差值很小（< 1%）且 `.bss` 无变化时，可以直接用估算方法而无需重启。

## 输出报告模板

```
## ROM 影响

| 库 | 基线(bytes) | 当前(bytes) | 差值 | 比例 |
|----|------------|------------|------|------|
| libmmi-server.z.so | X | Y | +/-Z | +/-N% |
| ... | | | | |
| **合计** | | | | |

### libmmi-server.z.so 段级分析

| 段 | 基线 | 当前 | 差值 |
|----|------|------|------|
| .text | X | Y | +/-Z |
| .rodata | | | |
| .data | | | |
| .bss | | | |

## RAM 影响

### 当前状态（修改后）
- PID: XXXX
- PSS: XXXX kB / RSS: XXXX kB / VmSize: XXXX kB
- libmmi .so PSS 合计: XXXX kB

### 估算变化
- .text 差值: +/-X bytes → shared clean PSS 变化 ≈ +/-Y kB
- .bss 差值: +/-X bytes → anonymous 变化 ≈ +/-Y kB

## 结论
ROM: +/-X bytes (+/-N%)
RAM: 估算 +/-X kB（.text 段变化导致的共享内存变化）
```

## Common Mistakes

| 错误 | 后果 | 修复 |
|------|------|------|
| 用 `ls -l` 文件大小评估 RAM | 文件大小包含 ELF 头、符号表等不映射到内存的部分 | 用 readelf 段级分析 |
| 忽略 .bss 段 | .bss 不占 ROM 但影响 anonymous RAM | 单独检查 .bss |
| 拿 RSS 做进程间对比 | RSS 包含共享页全量，被多次计算 | 用 PSS |
| 对比不同版本系统的 RAM 数据 | 系统库版本差异导致噪声 | 确保只替换目标 .so，系统基线一致 |
| 重启前不等服务稳定 | 懒加载导致初始 RAM 偏低 | 重启后等 30 秒或执行一次完整功能路径 |
