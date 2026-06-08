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

### 6. 代码理论分析（推荐作为佐证）

段级估算只能反映静态映射内存，无法反映堆分配（new/malloc）。对于引入新数据结构的特性变更，应分析代码 diff 中的新增容器和对象：

```bash
# 查找新增的 map/vector/set 成员变量
git diff <baseline>..HEAD -- '*.h' | grep -E '^\+\s+(std::(map|unordered_map|vector|set))'

# 查找新增的 struct/class 定义
git diff <baseline>..HEAD -- '*.h' | grep -E '^\+.*struct |^\+.*class '
```

分析维度：

| 维度 | 检查方法 |
|------|---------|
| 新增容器成员 | grep diff 中的 `std::map`, `std::vector` 等 |
| 每条目大小 | 分析 value type 的字段（标量、vector、shared_ptr 等） |
| 分配时机 | 是否懒分配（仅在使用时创建） |
| 条目数量上界 | 绑定的设备数、group 数 |
| 清理机制 | 是否有 erase/clear/remove 路径 |
| 泄漏风险 | 是否所有分配路径都有对应释放 |

将理论分析结果按场景估算：
- 不使用特性时（0 条目）：仅容器头部 + 固定对象开销
- 典型场景（如 2 设备 × 2 group）：按条目数 × 条目大小估算
- 极端场景（上界）：最大设备数 × 最大 group 数

### 7. 采集前必须执行功能路径

**关键约束**：仅部署 .so 并重启是不够的。如果变更引入了懒分配（lazy allocation）的数据结构，必须在采集前执行完整的功能路径，确保所有运行时状态被实际分配：

```
部署 .so → 重启 → 等待系统稳定 (30s) → 执行功能路径 → 等待稳定 (5s) → 采集
```

功能路径示例（以 display group 绑定为例）：
1. 创建显示组（UpdateDisplayInfo）
2. 注入窗口（UpdateWindowInfo）
3. 创建设备 + 绑定（BindDeviceToDisplayGroupByDisplay）
4. 注入事件（鼠标移动、按键、滚轮）触发所有状态路径
5. 解绑 + 清理

不执行功能路径的 RAM 采集会**低估**实际内存占用，因为懒分配的容器仍为空。

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
| 重启后不执行功能路径就采集 | 懒分配的数据结构未实际分配，RAM 被低估 | 采集前必须执行完整功能路径触发所有状态分配 |
| 只做段级估算不做理论分析 | 段级估算不反映堆分配（new/malloc），遗漏运行时数据结构 | 结合 diff 中的新增容器做理论内存估算 |
| 重启前不等服务稳定 | 懒加载导致初始 RAM 偏低 | 重启后等 30 秒或执行一次完整功能路径 |
