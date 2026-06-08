---
name: ohos-dev-mmi-ram-rom-measurement
description: Use when measuring RAM/ROM impact of OpenHarmony multimodal input (MMI) subsystem changes on DAYU200 (RK3568). Covers ROM measurement via readelf section analysis and file size comparison, RAM measurement via /proc/PID/smaps, smaps_rollup, hidumper --mem, and baseline/current .so swap methodology. Includes code-level theoretical analysis for heap-allocated data structures.
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: mmi
  capability: ram-rom-measurement
  version: 0.2.0
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

## 度量三支柱

本 skill 要求从三个互相佐证的维度度量 RAM 影响：

| 维度 | 方法 | 反映什么 | 局限 |
|------|------|---------|------|
| **ROM 段级** | `readelf -S` | 静态映射内存（.text/.rodata/.bss） | 不反映堆分配 |
| **RAM 实测** | smaps + hidumper 真机采集 | 进程实际物理内存 | 受采集条件/编译差异影响 |
| **RAM 理论** | git diff 分析新增容器 + 结构体估算 | 堆分配和运行时数据结构 | 人工估算，依赖正确的结构体大小分析 |

三个维度**必须同时完成**，互相交叉验证。仅做段级估算会遗漏堆分配；仅做实测会受噪声影响；仅做理论分析无法确认实际表现。

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
BUILD_OUT="code/out/rk3568/multimodalinput/input"
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

**注意 PID 稳定性**：multimodalinput 是系统服务，可能被 watchdog 重启导致 PID 变化。在多条 hdc 命令之间 PID 可能不同。**解决方案**：使用命令替换在单次 hdc shell 调用中完成 PID 查找和数据采集：

```bash
$HDC shell "cat /proc/\$(pidof multimodalinput)/smaps_rollup"
```

### 2. smaps_rollup（进程级汇总）

```bash
$HDC shell "cat /proc/\$(pidof multimodalinput)/smaps_rollup"
```

关键字段：
- **Pss**: 按共享比例分摊后的实际物理内存（最能反映真实占用）
- **Rss**: 驻留物理内存（包含共享页全量）
- **Size**: 虚拟地址空间大小

### 3. smaps per-library PSS（重要）

```bash
$HDC shell "cat /proc/\$(pidof multimodalinput)/smaps" > smaps.txt
```

**解析脚本（修正版）**：

```python
import re
current_lib = None
pss_by_lib = {}
for line in open("smaps.txt"):
    # 每个 mapping header 行以 hex 地址范围开头
    # 必须在每个 header 行重置 current_lib，否则会将
    # anonymous 页（位于两个 libmmi mapping 之间）错误归入上一个 libmmi 库
    if re.match(r'[0-9a-f]+-[0-9a-f]+\s', line):
        m = re.search(r'(/system/lib\S*libmmi\S+\.so)', line)
        current_lib = m.group(1).split('/')[-1] if m else None
    m = re.match(r'Pss:\s+(\d+)\s+kB', line)
    if m and current_lib:
        pss_by_lib[current_lib] = pss_by_lib.get(current_lib, 0) + int(m.group(1))
for lib, pss in sorted(pss_by_lib.items()):
    print(f"  {lib}: {pss} kB")
```

> **关键修复**：早期版本的解析脚本在匹配到 libmmi mapping 后不重置 `current_lib`，导致后续的 anonymous mapping（无 .so 路径的 header 行）的 PSS 被错误累加到上一个 libmmi 库。实测中这会导致 3,220 kB 被错误报告为 7,701 kB（+140% 偏差）。

### 4. hidumper --mem（系统级）

```bash
$HDC shell "hidumper --mem \$(pidof multimodalinput)"
```

输出包含：native heap、.so mmap PSS、total PSS 等分类。

**注意**：hidumper 输出可能很长，通过 hdc shell 可能被截断。可重定向到文件后拉取：

```bash
$HDC shell "hidumper --mem \$(pidof multimodalinput) > /data/local/tmp/hidumper_mem.txt"
$HDC file recv /data/local/tmp/hidumper_mem.txt ./hidumper_mem.txt
```

### 5. 基线 RAM 获取

**精确方法**：临时恢复 .bak .so → 重启 → 采集 → 恢复修改版 .so

```bash
# 1. 备份当前修改版
$HDC shell "mount -o rw,remount /"    # RK3568 根文件系统在 /，不是 /system
$HDC shell "cp /system/lib/libmmi-server.z.so /data/local/tmp/libmmi-server.z.so.new"
# 对 libmmi-server-common.z.so, libmmi-util.z.so 同样操作

# 2. 恢复基线
$HDC shell "cp /data/local/tmp/libmmi-server.z.so.bak /system/lib/libmmi-server.z.so"
# 对每个库同样恢复 .bak
$HDC shell "reboot"
# 等待重启 (~60s)...

# 3. 采集基线 RAM
$HDC shell "cat /proc/\$(pidof multimodalinput)/smaps_rollup"
$HDC shell "cat /proc/\$(pidof multimodalinput)/smaps" > smaps_baseline.txt
$HDC shell "hidumper --mem \$(pidof multimodalinput) > /data/local/tmp/hidumper_baseline.txt"

# 4. 恢复修改版
$HDC shell "mount -o rw,remount /"
$HDC shell "cp /data/local/tmp/libmmi-server.z.so.new /system/lib/libmmi-server.z.so"
# 对每个库同样恢复 .new
$HDC shell "reboot"
```

> **RK3568 mount 注意**：根文件系统挂载在 `/`，不是 `/system`。`mount -o rw,remount /system` 会报 "not in /proc/mounts" 错误。正确命令是 `mount -o rw,remount /`。

**估算方法**（不需要重启）：

基于段级分析推算 RAM 变化：
- `.text` + `.rodata` 差值 → 影响 shared clean PSS
- `.bss` 差值 → 影响 anonymous 内存
- `.data` 差值 → 影响 private dirty

当段差值很小（< 1%）且 `.bss` 无变化时，可以直接用估算方法而无需重启。

### 6. 采集前必须执行功能路径

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

## 代码理论分析方法（第三支柱）

段级估算只能反映静态映射内存，无法反映堆分配（new/malloc）。对于引入新数据结构的特性变更，**必须**分析代码 diff 中的新增容器和对象。

### 1. 发现新增数据结构

```bash
# 查找新增的 map/vector/set 成员变量
git diff <baseline>..HEAD -- '*.h' | grep -E '^\+\s+(std::(map|unordered_map|vector|set))'

# 查找新增的 struct/class 定义
git diff <baseline>..HEAD -- '*.h' | grep -E '^\+.*struct |^\+.*class '
```

### 2. 估算单条目大小

| 维度 | 检查方法 |
|------|---------|
| 新增容器成员 | grep diff 中的 `std::map`, `std::vector` 等 |
| 每条目大小 | 分析 value type 的字段（见下方估算技巧） |
| 分配时机 | 是否懒分配（仅在使用时创建） |
| 条目数量上界 | 绑定的设备数、group 数 |
| 清理机制 | 是否有 erase/clear/remove 路径 |
| 泄漏风险 | 是否所有分配路径都有对应释放 |

#### 结构体大小估算技巧

**基类继承链开销**：

| 类型 | 额外开销 | 说明 |
|------|---------|------|
| `Parcelable` → `RefBase` | ~80 B | vtable(8B) + RefCounter 堆分配(~72B) |
| `InputEvent` (所有事件基类) | ~120 B | Parcelable + 时间戳、设备ID、source 等 |
| `shared_ptr` control block | ~16 B | 引用计数 + deleter |

**std::string SSO（Small String Optimization）**：
- 短字符串（通常 ≤15 字节）：inline 在 string 对象中，sizeof(std::string) ≈ 32B
- 长字符串：32B 对象 + 堆分配

**STL 容器 overhead**：

| 容器 | 空容器大小 | 每条目额外开销 |
|------|----------|--------------|
| `std::map<K,V>` | ~48 B | 节点 ~48B + sizeof(K) + sizeof(V) |
| `std::unordered_map<K,V>` | ~56 B | 节点 ~56B + sizeof(K) + sizeof(V) |
| `std::vector<T>` | ~24 B | sizeof(T) per element (amortized) |
| `std::set<T>` | ~48 B | 节点 ~48B + sizeof(T) |
| `std::list<T>` | ~24 B | 节点 ~24B + sizeof(T) |

**Render Service (RS) 资源**：

如果变更涉及 RS SurfaceNode / CanvasNode / RSUIDirector 等图形资源，需要特别分析：

| RS 资源 | 内存开销 | 说明 |
|---------|---------|------|
| RSSurfaceNode + BufferQueue (64×64 RGBA, triple-buffer) | ~48 KB | 16 KB/buffer × 3 |
| RSSurfaceNode + BufferQueue (128×128 RGBA, triple-buffer) | ~192 KB | 64 KB/buffer × 3 |
| RSCanvasNode + RSUIDirector + RSUIContext | ~1.6 KB | 控制结构 |

RS 资源通常是**最大的单项内存开销**。如果代码中 RS shared_ptr 为 nullptr（未实际创建），需要在报告中明确标注"当前实现"与"完整实现"两个场景的区别。

### 3. 按场景汇总

| 场景 | 估算方法 |
|------|---------|
| 不使用特性（0 条目） | 仅容器头部 + 固定对象开销 |
| 典型场景（如 2 设备 × 2 group） | 按条目数 × 条目大小估算 |
| 极端场景（上界） | 最大设备数 × 最大 group 数 |

### 4. 与实测数据交叉验证

理论估算结果应与实测 libmmi PSS 差值对比：
- 理论值远小于实测差值 → 遗漏了某类数据结构（如 RS 资源、第三方库对象）
- 理论值远大于实测差值 → 估算偏高，检查懒分配是否实际触发
- 两者数量级一致 → 分析可信

## 输出报告模板

```markdown
## ROM 影响

### 文件级对比

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

### 实测对比（libmmi 库 PSS）

| 库 | 基线 PSS (kB) | 修改版 PSS (kB) | 差值 |
|----|-------------|---------------|------|
| libmmi-server.z.so | X | Y | +/-Z |
| ... | | | |

### 理论分析

| 场景 | 当前实现 | 完整实现(含RS) |
|------|---------|--------------|
| 不使用特性 | ~X B | ~X B |
| 典型 N设备×N group | ~X KB | ~X KB |

### 实测 vs 理论对照

[说明两者是否一致，差异原因]

## 结论

ROM: +/-X bytes (+/-N%)
RAM: 实测 libmmi PSS +/-X kB；理论典型场景 ~X KB
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
| 只做理论分析不做实测 | 理论估算可能遗漏/高估，无法确认实际表现 | 三支柱（段级 + 实测 + 理论）交叉验证 |
| smaps 解析器不重置 current_lib | anonymous mapping 的 PSS 被错误归入上一个 libmmi 库，严重高估 | 每个 mapping header 行必须重置 current_lib |
| PID 在多条 hdc 命令间变化 | 读取了不同进程的 smaps | 使用 `$(pidof multimodalinput)` 在单次 shell 调用内完成 |
| `mount -o rw,remount /system` | RK3568 根文件系统在 /，报 "not in /proc/mounts" | 使用 `mount -o rw,remount /` |
| 忽略 Parcelable/RefBase 继承 | 低估含 RefCounter 堆分配的对象大小 | 分析完整继承链，包含 vtable 和 RefCounter |
| 忽略 RS SurfaceNode/BufferQueue | 遗漏最大的单项内存开销（每 group 50-200 KB） | 分析 RS 资源创建路径，区分 nullptr vs 实际创建 |
| 理论分析只看 sizeof 不看堆分配 | 遗漏 std::string 长字符串、vector 元素、map 节点的堆分配 | 分析每个字段的实际内存布局 |
