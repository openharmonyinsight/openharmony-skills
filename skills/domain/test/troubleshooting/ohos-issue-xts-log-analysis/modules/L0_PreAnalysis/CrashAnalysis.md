# 崩溃深度分析

> 由 [CrashFreezeDetect.md](./CrashFreezeDetect.md) Step 2.7 检测到 cppcrash 后引用（非独立入口）。流程总览见 [SKILL.md](../../SKILL.md)。
---

## 一、崩溃分析

### 崩溃问题类型

崩溃类问题可通过日志关键字识别：`SIGSEGV`/`SIGILL`/`SIGABRT`/`SIGFPE`/`SIGBUS`、`App died`、`jscrash`/`cppcrash`/`appfreeze`。

> **注意**：本模块聚焦 OpenHarmony 专属的崩溃分析流程，基础信号含义（SIGSEGV=内存访问等）为 Claude 已知内容，不在此赘述。

---

## 分析流程（15分钟）

### 第一步：确认崩溃类型（2分钟）

**检查日志关键字**：
```bash
# 检查 module_run.log（已更正）
grep -E "App died|Process exit|crash" module_run.log

# 检查hilog.log
grep -E "SIGSEGV|SIGILL|SIGABRT|SIGFPE|jscrash|cppcrash" hilog.log
```
> 注：此处为崩溃**检测**（关键字存在性），非行号/domain分层取数——Windows 可用 Git Bash 或 PowerShell `Select-String`；行号/分层取数仍须 `filter_hilog.py`（见 [SKILL.md「全平台取数」](../../SKILL.md)）。

**关键日志示例**：
```
I 01:08:06.123 App died
I 01:08:06.124 Process com.example exit
I 01:08:06.125 crash log: /data/log/faultlog/faultlogger/cppcrash-xxx.log
```

### 第二步：抓取crash日志（3分钟）

**抓取方法**：
```bash
# 查看设备上的crash日志
hdc shell ls /data/log/faultlog/faultlogger/

# 抓取jscrash日志（JS崩溃）
hdc file recv /data/log/faultlog/faultlogger/jscrash-*.log ./

# 抓取cppcrash日志（C++崩溃）
hdc file recv /data/log/faultlog/faultlogger/cppcrash-*.log ./

# 抓取所有故障日志
hdc file recv /data/log/faultlog/faultlogger/ ./faultlog/
```

**日志文件命名规则**：
```
cppcrash-进程名-进程UID-毫秒级时间.log
jscrash-进程名-进程UID-毫秒级时间.log
```

### 第三步：解析crash日志（5分钟）

**cppcrash日志关键字段**：

```
Reason: SIGSEGV                     # 崩溃原因（信号类型）
Registers:                          # 寄存器信息
  pc: 0x12345678                    # 程序计数器（当前执行指令地址）
  lr: 0x12345679                    # 链接寄存器（返回地址）
  sp: 0x12345680                    # 堆栈指针
  fp: 0x12345681                    # 栈帧指针
Callstack:                          # 调用栈
  #0 0x12345678 in functionA        # 函数名和地址
  #1 0x12345679 in functionB
  #2 0x12345680 in main
```

**解析步骤**：

1. **查看Reason字段**：确定信号类型
2. **检查Registers**：查看PC/LR/SP/FP寄存器
3. **分析Callstack**：定位崩溃函数位置

### 第四步：定位代码位置（3分钟）

**根据PC/LR定位**：
```bash
# 使用addr2line工具（如果有）
addr2line -e <可执行文件> <PC地址>

# 或者手动查找
# 在源代码中搜索Callstack中的函数名
```

**常见崩溃场景**：
- PC在functionA → 检查functionA是否有空指针操作
- LR在functionB → 检查functionB调用functionA是否合法
- Callstack显示调用链 → 从最顶层函数开始排查

### 第五步：排查问题原因（2分钟）

**常见崩溃原因排查**：

| 崩溃类型 | 排查方向 | 检查项 |
|---------|---------|--------|
| SIGSEGV | 内存问题 | 空指针、数组越界、内存泄漏 |
| SIGILL | 指令问题 | 函数指针错误、代码注入 |
| SIGABRT | 逻辑问题 | assert失败、abort调用 |
| SIGFPE | 算术问题 | 除数为0、整数溢出 |

**排查清单**：
- ✅ 是否有空指针访问？
- ✅ 是否有数组越界？
- ✅ 是否有内存未初始化？
- ✅ 是否有除数为0情况？
- ✅ 是否有函数指针错误？

---

## 详细分析示例

### 示例：SIGSEGV崩溃分析

**日志内容**：
```
Reason: SIGSEGV
Registers:
  pc: 0x00000012345678
  lr: 0x00000012345679
Callstack:
  #0 0x12345678 in processData
  #1 0x12345679 in handleRequest
  #2 0x12345680 in main
```

**分析步骤**：

1. **确定崩溃类型**：SIGSEGV（内存访问崩溃）
2. **定位崩溃函数**：processData函数
3. **查看调用链**：main → handleRequest → processData
4. **检查processData函数**：
   - 是否有指针操作？
   - 是否有内存访问？
   - 是否有空指针检查？

**解决方案**：
```typescript
// 检查空指针
function processData(data) {
    if (!data) {  // 添加空指针检查
        return;
    }
    // 原有代码...
}
```

### 示例：App died闪退分析

**日志内容**：
```
I 01:08:06.123 App died
I 01:08:06.124 Process com.example.app exit
I 01:08:06.125 crash: /data/log/faultlog/faultlogger/jscrash-com.example.app-20010177-123456.log
```

**分析步骤**：

1. **确认闪退**：App died关键字
2. **抓取jscrash日志**：
```bash
hdc file recv /data/log/faultlog/faultlogger/jscrash-com.example.app-20010177-123456.log ./
```

3. **解析jscrash日志**：
```
Exception: TypeError
Message: Cannot read property 'xxx' of undefined
Stack:
  at processData (file:///path/to/code.js:123:45)
  at handleRequest (file:///path/to/code.js:67:89)
```

4. **定位代码**：processData函数第123行
5. **修复问题**：添加undefined检查

---

## 使用分析脚本

### 自动化崩溃分析

```bash
# 分析 crash_log 目录下所有 cppcrash-*.log
python3 scripts/analyze_crash_stack.py /path/to/crash_log_*/

# 分析单个 cppcrash 文件
python3 scripts/analyze_crash_stack.py /path/to/cppcrash-media_service-*.log

# 从标准输入解析崩溃栈文本（适合 appfreeze 主线程栈）
grep -E "^#0[0-9] pc " appfreeze-*.log | python3 scripts/analyze_crash_stack.py -

# 运行内置示例
python3 scripts/analyze_crash_stack.py --example
```

**脚本功能**：
- 解析 cppcrash-*.log 文件（或目录批量解析），提取 Reason、Process Name、Timestamp、Thread Name
- 从 Callstack 提取 #NN pc 栈帧，解析 SO 库名与函数名
- 查询 so_mapping 表获取子系统归属与责任人
- 输出定界结论（主崩溃库、崩溃函数、问题归属、建议流转）

### 手动查询崩溃规则

```bash
# 查询崩溃相关规则
python3 scripts/query_db.py rules --keyword SIGSEGV
python3 scripts/query_db.py rules --keyword crash
python3 scripts/query_db.py rules --keyword "App died"
```

---

## 数据库规则匹配

### 崩溃相关规则

| 关键字 | 领域 | 问题类型 | 优先级 |
|--------|------|---------|--------|
| SIGSEGV | 应用问题 | 内存访问崩溃 | 8 |
| SIGILL | 应用问题 | 非法指令崩溃 | 8 |
| SIGABRT | 应用问题 | 进程终止崩溃 | 8 |
| SIGFPE | 应用问题 | 浮点异常崩溃 | 8 |
| SEGV_MAPERR | 应用问题 | 不存在内存地址 | 9 |
| SEGV_ACCERR | 应用问题 | 不可访问内存地址 | 9 |
| App died | 元能力 | 应用闪退 | 10 |
| jscrash | 应用问题 | JS Crash | 8 |
| cppcrash | 应用问题 | CPP Crash | 8 |

### 责任人查询

```python
import sqlite3

conn = sqlite3.connect('~/.opencode/skills/ohos-issue-xts-log-analysis/data/xts_rules.db')
cursor = conn.cursor()

# 查询应用问题责任人
cursor.execute('SELECT name, zhanma FROM contacts WHERE domain="应用问题"')
for row in cursor.fetchall():
    print(f'{row[0]}: {row[1]}')

# 查询元能力责任人
cursor.execute('SELECT name, zhanma FROM contacts WHERE domain="元能力"')
for row in cursor.fetchall():
    print(f'{row[0]}: {row[1]}')

conn.close()
```

---

## 生成崩溃分析报告

### 报告模板

```
【崩溃问题定界报告】
问题类型: <SIGSEGV/SIGILL/SIGABRT/...>
崩溃进程: <进程名>
崩溃时间: <时间戳>

【关键信息】
Reason: <信号类型>
PC地址: <PC寄存器值>
LR地址: <LR寄存器值>
崩溃函数: <Callstack中最顶层函数>

【调用栈】
#0 <函数名> @ <地址>
#1 <函数名> @ <地址>
...

【问题原因】
<基于PC/LR和Callstack的分析结论>

【解决方案】
1. <修复建议1>
2. <修复建议2>

【建议流转】
责任人: <姓名> (<詹码>)
```

---

## 崩溃与级联阻塞（2026-07-14新增）

> 当系统进程崩溃导致测试用例级联阻塞时，崩溃分析是整个报告的根因。

### 崩溃 → FAILED + BLOCKED 模式

**典型场景**：系统服务进程（如media_service）崩溃，导致：
1. **直接FAILED**：崩溃后执行的用例返回非预期错误码
2. **级联BLOCKED**：崩溃后服务异常 → appfreeze → 套件中断 → 后续套件未执行

**识别方法**：
```bash
# 检查崩溃次数（多次崩溃=系统性问题）
ls crash_log_*/ | grep -c "cppcrash"

# 检查appfreeze（应用冻结导致套件中断）
ls crash_log_*/ | grep "appfreeze"

# 检查"missed"标记（套件中断标志）
grep -n "missed" module_run.log
```

### appfreeze → BLOCKED 模式

**appfreeze类型**：
| appfreeze原因 | 含义 | 对测试的影响 |
|--------------|------|-------------|
| THREAD_BLOCK_6S | 主线程阻塞6秒 | 测试套件中断，后续用例BLOCKED |
| APP_INPUT_BLOCK | 输入事件阻塞 | 交互类用例阻塞 |

**appfreeze分析要点**：
1. 查看 `Reason` 字段（如 THREAD_BLOCK_6S）
2. 查看阻塞线程调用栈（定位阻塞位置）
3. 关联崩溃日志（appfreeze通常由前序崩溃引发）

### 崩溃分析在报告中的位置

当崩溃是根因时，崩溃分析应作为报告的 **1.1节**（所有FAILED和BLOCKED的根因），包含：
- 崩溃基本信息（进程名、崩溃原因、崩溃SO库、崩溃函数）
- 崩溃时间线（多次崩溃逐条列出）
- 崩溃调用栈
- 崩溃根因分析

> 详细报告结构见 下方「崩溃作为根因时的报告结构」

---

## 崩溃问题快速参考

### 常见崩溃场景

| 场景 | 崩溃类型 | 典型原因 | 解决方法 |
|------|---------|---------|---------|
| 空指针访问 | SIGSEGV | 访问null/undefined | 添加空指针检查 |
| 数组越界 | SIGSEGV | 数组索引超范围 | 添加边界检查 |
| 除数为0 | SIGFPE | 整数/浮点除法 | 检查除数不为0 |
| 内存泄漏 | SIGSEGV | 访问已释放内存 | 使用智能指针 |
| 函数指针错误 | SIGILL | 调用无效函数指针 | 检查函数指针 |
| 析构竞态 | SIGSEGV | 析构时线程仍访问 | 确保线程先停止再析构 |

### 崩溃日志抓取命令速查

| 场景 | 命令 |
|------|------|
| 查看设备crash日志 | `hdc shell ls /data/log/faultlog/faultlogger/` |
| 抓取jscrash | `hdc file recv /data/log/faultlog/faultlogger/jscrash-* ./` |
| 抠取cppcrash | `hdc file recv /data/log/faultlog/faultlogger/cppcrash-* ./` |
| 抓取所有故障日志 | `hdc file recv /data/log/faultlog/faultlogger/ ./faultlog/` |

---

**更新时间**：2026-07-14  
**SO 库归属查询**：54 个系统 SO 库的子系统映射及查询命令详见 [so-crash-analysis.md](../../references/so-crash-analysis.md)  
**总结**：崩溃问题分析需要重点关注crash日志的Reason、Registers、Callstack字段，通过PC/LR地址定位代码位置，结合调用栈排查具体原因。当崩溃导致级联阻塞时，崩溃分析作为报告根因节（1.1），所有FAILED和BLOCKED均引用此节。
---

