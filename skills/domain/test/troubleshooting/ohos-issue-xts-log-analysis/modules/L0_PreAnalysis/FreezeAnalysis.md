# 冻屏深度分析

> 由 [CrashFreezeDetect.md](./CrashFreezeDetect.md) Step 2.7 检测到 appfreeze 后引用（非独立入口）。流程总览见 [SKILL.md](../../SKILL.md)。
---

## 二、冻屏分析

### 目录

- 冻屏问题类型
  - 检测类型分类
  - 检测原理
- 分析流程（10分钟）
  - 第一步：确认冻屏类型（2分钟）
  - 第二步：抓取appfreeze日志（3分钟）
  - 第三步：提取主线程调用栈（强制，2026-07-15新增）
  - 第四步：解析appfreeze日志其他字段（5分钟）
- 详细分析示例
  - 示例：THREAD_BLOCK_6S分析
  - 示例：APP_INPUT_BLOCK分析
  - 示例：LIFECYCLE_TIMEOUT分析
- 内存告警判断
  - NOTE提示说明
- 使用分析脚本
  - 冻屏规则查询
  - 主线程调用栈提取（强制，见第三步）
  - 手动查询冻屏规则
- 数据库规则匹配
  - 冻屏相关规则

---

> **触发方式**：由 [CrashFreezeDetect.md](./CrashFreezeDetect.md) Step 2.7 检测到 appfreeze 后引用本模块深度分析（非独立入口）
> 
> **适用场景**：THREAD_BLOCK_6S、APP_INPUT_BLOCK、LIFECYCLE_TIMEOUT等冻屏类问题的深度分析
> 
> **问题类型**：主线程卡死、输入响应超时、生命周期切换超时

---

## 冻屏问题类型

### 检测类型分类

| 故障类型 | 含义 | 检测阈值 | 优先级 |
|---------|------|---------|--------|
| THREAD_BLOCK_6S | 主线程卡死 | 超过6s未响应判活检测 | 9 |
| APP_INPUT_BLOCK | 输入响应超时 | 点击事件超时5s（API 24后8s） | 9 |
| LIFECYCLE_TIMEOUT | 生命周期切换超时 | Load: 10s, Foreground: 5s | 9 |
| THREAD_BLOCK_3S | 主线程卡死告警 | 超过3s未响应（告警） | 7 |

### 检测原理

**THREAD_BLOCK_6S**：
- Watchdog线程定期向主线程插入判活检测任务
- 超过3s → THREAD_BLOCK_3S告警
- 超过6s → THREAD_BLOCK_6S主线程卡死

**APP_INPUT_BLOCK**：
- 用户点击 → 输入系统发送事件 → 应用响应反馈
- 响应超时 → APP_INPUT_BLOCK

**LIFECYCLE_TIMEOUT**：
- AMS发送生命周期指令 → 等待应用返回结果
- 半生命周期阈值未完成 → LIFECYCLE_HALF_TIMEOUT告警
- 完整生命周期阈值未完成 → LIFECYCLE_TIMEOUT

---

## 分析流程（10分钟）

### 第一步：确认冻屏类型（2分钟）

**检查日志关键字**：
```bash
# 检查appfreeze日志
grep -E "THREAD_BLOCK|APP_INPUT|LIFECYCLE_TIMEOUT" appfreeze.log

# 检查 module_run.log（已更正）
grep -E "freeze|block|timeout" module_run.log

# 检查hilog.log
grep -E "AppFreeze|freeze|block" hilog.log
```
> 注：此处为冻结**检测**（关键字存在性），非行号/domain分层取数——Windows 可用 Git Bash 或 PowerShell `Select-String`；行号/分层取数仍须 `filter_hilog.py`（见 [SKILL.md「全平台取数」](../../SKILL.md)）。

**关键日志示例**：
```
Reason: THREAD_BLOCK_6S
Process Memory(kB): 163819(Rss)
Device Memory(kB): Total 11679272, Free 3697424
Page switch history:
  14:08:30:327 /ets/pages/Index
  14:08:28:986 /ets/pages/Index
```

### 第二步：抓取appfreeze日志（3分钟）

**抓取方法**：
```bash
# 查看设备上的appfreeze日志
hdc shell ls /data/log/faultlog/faultlogger/

# 抓取appfreeze日志
hdc file recv /data/log/faultlog/faultlogger/appfreeze-*.log ./

# 抓取所有故障日志
hdc file recv /data/log/faultlog/faultlogger/ ./faultlog/
```

### 第三步：提取主线程调用栈（强制，2026-07-15新增）

> ⚠️ **这是appfreeze定界的核心证据**。appfreeze日志中的"Dump main thread stack"段显示主线程在阻塞时的完整调用栈，是判断问题归属（测试侧 vs 系统侧）的唯一依据。
>
> **为什么（理解而非死记）**：appfreeze = 主线程阻塞6秒。要回答"为什么阻塞"，必须看主线程在执行什么函数。调用栈中的顶层函数（#00）就是阻塞点。如果阻塞函数在测试NAPI库（如libavplayerndk.so的sleep()），是测试侧问题；如果在系统服务（如media_service），是系统侧问题。不提取栈=猜测=必错——实测把测试侧sleep()误判为系统侧media_service崩溃。

**提取方法**：
```bash
# 从appfreeze日志提取主线程调用栈
grep -A 50 "Dump main thread stack" appfreeze-*.log
# 或搜索栈帧模式
grep -E "^#0[0-9] pc " appfreeze-*.log
```

**appfreeze日志中的主线程栈位置**：
```
Dump main thread stack start time: 2026-06-30 00:40:38.925
Tid:5462, Name:player.napitest                    ← 主线程
#00 pc 00000000001f03cc ld-musl-aarch64.so.1(sleep+64)     ← 阻塞函数！
#01 pc 000000000001fdcc libavplayerndk.so                    ← 测试NAPI库
#02 pc 0000000000069830 libace_napi.z.so(ArkNativeFunctionCallBack)
#05 at anonymous (AVPlayerNdk.test.ts:701:39)                 ← JS测试代码
Dump main thread stack end time: 2026-06-30 00:40:38.997
```

**定界依据**：
| 栈帧位置 | 问题归属 | 示例 |
|---------|---------|------|
| #00 在测试NAPI库(.so) | **测试侧** | sleep() in libavplayerndk.so |
| #00 在系统服务库(.z.so) | **系统侧** | mutex_lock in libmedia_service.z.so |
| #00 在libc/系统运行时 | 需进一步分析 | sleep/pthread_cond_wait |

**报告要求**：
- ✅ appfreeze分析节必须包含主线程调用栈（至少#00-#03帧）
- ✅ 必须分析阻塞函数（#00帧的函数名）确定问题归属
- ❌ 禁止只用"可能原因"猜测，不提取栈
- ❌ 禁止把appfreeze直接归因为前序崩溃（除非栈中有崩溃函数）

---

### 第四步：解析appfreeze日志其他字段（5分钟）

**appfreeze日志关键字段**：

```
Reason: THREAD_BLOCK_6S              # 冻屏原因
Process Memory(kB): 163819(Rss)      # 进程内存占用
Device Memory(kB): ...               # 整机内存状态
Page switch history:                 # 页面切换轨迹
  14:08:30:327 /ets/pages/Index      # 页面路径和时间
  14:08:28:986 /ets/pages/Index
HitraceIdInfo: hitrace_id: xxx       # HiTrace链路跟踪信息
```

**解析步骤**：

1. **查看Reason字段**：确定冻屏类型
2. **检查Page switch history**：确定问题页面
3. **分析Process Memory**：检查进程内存状态
4. **查看Device Memory**：检查整机内存告警
5. **使用HitraceIdInfo**：跟踪调用链路

---

## 详细分析示例

### 示例：THREAD_BLOCK_6S分析

**日志内容**：
```
Reason: THREAD_BLOCK_6S
Process Memory(kB): 163819(Rss)
Device Memory(kB): Total 11679272, Free 3697424
Page switch history:
  14:08:30:327 /ets/pages/Index:Appfreeze
  14:08:28:986 /ets/pages/Index
  14:08:26:502 :enters foreground
HitraceIdInfo: hitrace_id: a92ab27238f409a
```

**分析步骤**：

1. **确定冻屏类型**：THREAD_BLOCK_6S（主线程卡死）
2. **分析页面切换轨迹**：
   - 问题发生在 `/ets/pages/Index` 页面
   - 14:08:30时卡死，距离上次页面切换约1.5秒
3. **检查内存状态**：
   - 进程内存163MB，整机内存充足（Free 3.7GB）
   - 无内存告警
4. **使用HiTraceId跟踪**：
```bash
# 查找对应时间段hilog日志
grep "a92ab27238f409a" hilog.log
```

**排查方向**：
- Index页面是否有耗时操作？
- 主线程是否有阻塞代码？
- 是否有无限循环或死锁？

### 示例：APP_INPUT_BLOCK分析

**日志内容**：
```
Reason: APP_INPUT_BLOCK
Process Memory(kB): 82000(Rss)
Page switch history:
  14:08:35:000 /ets/pages/MainPage
```

**分析步骤**：

1. **确定冻屏类型**：APP_INPUT_BLOCK（输入响应超时）
2. **分析页面**：问题发生在MainPage页面
3. **排查方向**：
   - MainPage页面点击事件处理是否耗时？
   - 是否有异步操作阻塞UI响应？
   - 是否有大量数据处理？

### 示例：LIFECYCLE_TIMEOUT分析

**日志内容**：
```
Reason: LIFECYCLE_TIMEOUT
Page switch history:
  14:08:25:000 :leaves foreground
  14:08:20:000 :enters foreground
```

**分析步骤**：

1. **确定冻屏类型**：LIFECYCLE_TIMEOUT（生命周期切换超时）
2. **分析生命周期轨迹**：
   - 14:08:20进入前台
   - 14:08:25离开前台
   - 可能是Foreground生命周期超时
3. **排查方向**：
   - onForeground生命周期是否有耗时操作？
   - 是否有异步任务未完成？
   - 是否有资源加载阻塞？

---

## 内存告警判断

### NOTE提示说明

从API version 20开始，当整机资源告警时，日志中会输出NOTE行：

```
NOTE: Current fault may be caused by the system's low memory or thermal throttling, you may ignore it and analysis other faults.
```

**判断方法**：
- 如果有NOTE提示 → 可忽略该冻屏故障（系统资源问题）
- 如果没有NOTE提示 → 需深入分析应用侧问题

**内存告警检查**：
```bash
# 检查Device Memory字段
grep "Device Memory" appfreeze.log

# 检查Free内存是否充足（通常 >1GB为充足）
# Total - Free = Used
```

---

## 使用分析脚本

### 冻屏规则查询

无专用冻屏分析脚本。使用以下脚本辅助分析：

```bash
# 查询冻屏相关定界规则
python3 scripts/query_db.py rules --keyword "THREAD_BLOCK"
python3 scripts/query_db.py rules --keyword "appfreeze"

# 查询冻屏问题责任人
python3 scripts/query_db.py contacts 应用问题
```

### 主线程调用栈提取（强制，见第三步）

appfreeze 定界的核心证据是主线程调用栈，必须从 appfreeze-*.log 手动提取（grep）：

```bash
# 从appfreeze日志提取主线程调用栈
grep -A 50 "Dump main thread stack" appfreeze-*.log
# 或搜索栈帧模式
grep -E "^#0[0-9] pc " appfreeze-*.log
```

### 手动查询冻屏规则

```bash
# 查询冻屏相关规则
python3 scripts/query_db.py rules --keyword THREAD_BLOCK
python3 scripts/query_db.py rules --keyword freeze
python3 scripts/query_db.py rules --keyword block
```

---

## 数据库规则匹配

### 冻屏相关规则

| 关键字 | 领域 | 问题类型 | 优先级 |
|--------|------|---------|--------|
| THREAD_BLOCK_6S | 应用问题 | 主线程卡死 | 9 |
| APP_INPUT_BLOCK | 应用问题 | 输入响应超时 | 9 |
| LIFECYCLE_TIMEOUT | 应用问题 | 生命周期超时 | 9 |
| THREAD_BLOCK_3S | 应用问题 | 主线程卡死告警 | 7 |
| appfreeze | 应用问题 | 应用冻结 | 9 |

### 责任人查询

```python
import sqlite3

conn = sqlite3.connect(os.path.expanduser('~/.opencode/skills/ohos-issue-xts-log-analysis/data/xts_rules.db')
cursor = conn.cursor()

# 查询应用问题责任人
cursor.execute('SELECT name, zhanma FROM contacts WHERE domain="应用问题"')
for row in cursor.fetchall():
    print(f'{row[0]}: {row[1]}')

conn.close()
```

**责任人信息**：
- 张义恒(00448841) - 应用问题主要负责人

---

## 生成冻屏分析报告

### 报告模板

```
【冻屏问题定界报告】
问题类型: <THREAD_BLOCK_6S/APP_INPUT_BLOCK/LIFECYCLE_TIMEOUT>
冻屏进程: <进程名>
冻屏时间: <时间戳>

【关键信息】
Reason: <冻屏原因>
问题页面: <Page switch history中的最后页面>
进程内存: <Process Memory值>
整机内存: <Device Memory值>
内存告警: <是否有NOTE提示>

【页面切换轨迹】
<时间>: <页面路径>
<时间>: <页面路径>
...

【问题原因】
<基于页面轨迹和内存状态的分析结论>

【解决方案】
1. <修复建议1>
2. <修复建议2>

【建议流转】
责任人: 张义恒 (00448841)
```

---

## 冻屏问题快速参考

### 常见冻屏场景

| 场景 | 冻屏类型 | 典型原因 | 解决方法 |
|------|---------|---------|---------|
| 主线程卡死 | THREAD_BLOCK_6S | 死循环、死锁、耗时操作 | 异步处理、避免阻塞 |
| 点击无响应 | APP_INPUT_BLOCK | 点击处理耗时、异步阻塞 | 优化响应速度 |
| 生命周期超时 | LIFECYCLE_TIMEOUT | 初始化耗时、资源加载慢 | 分步加载、异步初始化 |

### 冻屏日志抓取命令速查

| 场景 | 命令 |
|------|------|
| 查看设备appfreeze日志 | `hdc shell ls /data/log/faultlog/faultlogger/` |
| 抓取appfreeze | `hdc file recv /data/log/faultlog/faultlogger/appfreeze-* ./` |
| 抓取所有故障日志 | `hdc file recv /data/log/faultlog/faultlogger/ ./faultlog/` |

### 内存状态判断标准

| 指标 | 充足 | 告警 | 严重 |
|------|------|------|------|
| Device Memory Free | >1GB | 500MB-1GB | <500MB |
| Process Memory | <100MB | 100-200MB | >200MB |
| NOTE提示 | 无 | 无 | 有 |

---

**总结**：冻屏问题分析需要重点关注appfreeze日志的Reason、Page switch history、Memory字段，通过页面轨迹确定问题位置，检查内存状态判断是否系统资源问题，结合HiTraceId跟踪调用链路。
