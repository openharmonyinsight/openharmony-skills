# L0_PreAnalysis - 崩溃/冻结检测（Step 2.7，强制）

> 检测到 cppcrash → 加载 [CrashAnalysis.md](./CrashAnalysis.md)；检测到 appfreeze → 加载 [FreezeAnalysis.md](./FreezeAnalysis.md)。
---

## Step 2.7：崩溃/冻结检测（强制）

> **断链修复**：此步骤补上"失败用例→appfreeze分析"的断链。检测到崩溃/冻结但报告中无对应分析节 → 报告无效。

**AI操作**：
```bash
# 1. 检测崩溃日志（cppcrash = 进程崩溃，appfreeze = 应用冻结）
ls <日志目录>/crash_log_*/ 2>/dev/null | grep -cE "cppcrash"
ls <日志目录>/crash_log_*/ 2>/dev/null | grep "appfreeze"

# 2. 检测套件中断（missed = 级联阻塞标志）
grep -n "missed" <日志目录>/module_run.log

# 3. 统计崩溃文件数（时间线完整性校验用）
ls <日志目录>/crash_log_*/cppcrash-*.log 2>/dev/null | wc -l
```

**判定分支**：

| 检测结果 | 报告影响 | 深度分析 |
|---------|---------|---------|
| 有 cppcrash（系统服务崩溃） | 1.1节放崩溃分析（根因） | 读 [CrashAnalysis.md](./CrashAnalysis.md)（崩溃分析）深度分析：崩溃时间线（逐条）+ 真实调用栈 + 根因 |
| 有 appfreeze（应用冻结） | 新增 BLOCKED 类型A 分析节（完整6段） | 读 [CrashAnalysis.md](./CrashAnalysis.md)（冻屏分析）深度分析：THREAD_BLOCK原因 + 主线程调用栈 + 源码定位 |
| 有 missed（套件中断） | 新增 BLOCKED 类型B 汇总节 | 汇总：阻塞用例分布表 + 阻塞链分析 |
| 无崩溃/冻结 | 正常分析（无崩溃分析节） | — |

**强制要求**：
- ✅ cppcrash 文件数 = 崩溃时间线条目数（逐条列出，禁"等"省略）
- ✅ appfreeze 必须提取主线程调用栈（from appfreeze-*.log），定位阻塞函数
- ✅ missed 统计必须含"套件内未执行"（如 `52 tests in X had missed`）+ "整套件未执行"（如 `2 suites have missed`）
- ✅ BLOCKED 总数 = 套件内 missed + 整套件 BLOCKED，禁止漏算
- ❌ 禁止检测到 cppcrash/appfreeze 但跳过对应分析节
- ❌ 禁止只统计整套件 BLOCKED 而漏算套件内 missed

**输出**：
```
Step 2.7：崩溃/冻结检测
检测结果：[cppcrash X个 / appfreeze Y个 / missed Z条]
崩溃分析：1.1节（崩溃时间线 X 条 + 调用栈）
appfreeze分析：1.X节（BLOCKED类型A，完整6段）
级联阻塞汇总：1.Y节（BLOCKED类型B，Z条）
```

---

