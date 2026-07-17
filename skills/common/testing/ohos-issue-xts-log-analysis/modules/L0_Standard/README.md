# L0_Standard - 标准流程详细说明

> **适用形态**：形态①②③（全量报告/log根/单testsuite）

## 模块概述

标准流程适用于有完整日志文件的输入形态，AI可以从summary_report.xml或module_run.log中自动提取失败用例信息。

## 详细工作流程

### Step 1：形态识别

**AI操作**：
```bash
ls -la <日志目录>
```

**判定依据**：
- 含 `summary_report.xml` → 形态①（全量报告）
- 下全是 `Acts*/` 子目录 → 形态②（log根）
- 含 `module_run.log` → 形态③（单testsuite）

**输出格式（固定）**：
```
检测结果：形态①（判定依据：检测到 summary_report.xml 文件）
```

---

### Step 2：锁定失败用例

**AI操作**（优先级顺序）：

**方法1（优先）**：从 summary_report.xml 提取
```bash
grep "result=\"false\"" summary_report.xml
```

解析XML提取：
- testsuite name
- testcase name
- message（错误信息）

**方法2（回退）**：从 module_run.log 提取
```bash
grep "FAILED" module_run.log
```

解析日志提取：
- [Listener] 行中的 testsuite#caseID
- 时间戳

**输出格式（固定）**：
```
失败用例数：X个
信号源：summary_report.xml/module_run.log

失败用例列表（表格形式）：
| 序号 | 测试套件 | 用例名 | 问题类型 | 根因分类 |
|------|---------|--------|---------|---------|
| 1 | ActsAACommandImplicitStartTest | SUB_Ability_..._3100 | 断言失败 | API行为异常 |
| 2 | ActsAACommandImplicitStartTest | SUB_Ability_..._3200 | 断言失败 | [同根因用例] |
```

**同根因用例标记规范**：
- ✅ 必须在"根因分类"列标记 `[同根因用例]`
- ✅ AI必须识别同根因用例并统一标记

---

### Step 2.5：源码路径定位（新增）

> **改进时间**：2026-07-06  
> **改进原因**：解决 find 命令盲搜导致 static/non-static 版本混淆问题

**目标**：基于 BUILD.gn 中 hap_name 字段精准定位测试套件源码目录

**输入**：
- 日志目录名（hap_name）
- OH_ROOT（OpenHarmony 源码根路径，需在配置文件中设置）

**输出**：
- 测试套件目录路径
- 定位方法（hap_name / test_template / bundle_name）

#### 2.5.1 提取 hap_name（强制）

**方法1（优先）**：从日志目录名提取
```bash
# 日志目录结构示例
# /home/xianf/copy/20260706/log/ActsAceCArkUI16Test/
#                                            └───── hap_name

# 提取 hap_name
hap_name=$(basename <日志目录>)
# 输出: ActsAceCArkUI16Test
```

**方法2（备用）**：从 bundle name 推断（hap_name 缺失时）
```bash
# 从 module_run.log 提取 bundle name
grep "Obtain the app name" module_run.log | grep -oE "com\.openharmony\.[a-z_]+"

# 示例: com.openharmony.arkui_capi_xts_api16
# 推断 hap_name（去除 static 后缀）
hap_name=$(infer_hap_from_bundle $bundle_name)
```

#### 2.5.2 搜索 BUILD.gn 文件

```bash
# 在 OH_ROOT/test/xts/acts 下搜索所有 BUILD.gn
find $OH_ROOT/test/xts/acts -name "BUILD.gn" -type f

# 示例输出：
# /home/xianf/master/test/xts/acts/arkui/ace_c_arkui_test_api16/BUILD.gn
# /home/xianf/master/test/xts/acts/arkui/ace_c_arkui_test_api16_static/BUILD.gn
```

#### 2.5.3 匹配 hap_name 字段（优先级①）

**优先级①**：hap_name 字段匹配（精准定位）

```bash
# 搜索包含 hap_name 字段的 BUILD.gn
grep -r "hap_name = \"$hap_name\"" $OH_ROOT/test/xts/acts --include="BUILD.gn"

# 示例输出：
# /home/xianf/master/test/xts/acts/arkui/ace_c_arkui_test_api16/BUILD.gn:hap_name = "ActsAceCArkUI16Test"

# 提取目录路径
test_suite_dir=$(dirname <匹配的BUILD.gn路径>)
echo "✅ 定位成功（hap_name匹配）: $test_suite_dir"
```

**解析 BUILD.gn 示例**：
```gn
ohos_js_app_suite("ActsAceCArkUI16Test") {
  test_hap = true
  testonly = true
  certificate_profile = "./signature/openharmony_sx.p7b"
  hap_name = "ActsAceCArkUI16Test"      ← ✅ 匹配此字段
  part_name = "ace_engine"
  subsystem_name = "arkui"
  deps = [ ":ActsAceCArkUI16" ]
}
```

#### 2.5.4 匹配测试模板 target（优先级②）

**优先级②**：测试模板 target 匹配（hap_name 缺失时的备用方案）

**支持的测试模板类型**（基于 XTS 源码统计，按使用频率排序）：

| 模板类型 | 使用次数 | 是否含 hap_name | 说明 |
|---------|---------|---------------|------|
| `ohos_js_app_suite` | 1893 | ✅ 是 | JS 应用测试套件（主要） |
| `ohos_js_app_static_suite` | 1140 | ✅ 是 | JS 应用静态测试套件 |
| `ohos_app_assist_suite` | 1007 | ✅ 是 | 应用辅助测试套件 |
| `ohos_moduletest_suite` | 359 | ❌ 否 | 模块测试套件（无 hap_name） |
| `ohos_js_hap_suite` | 13 | ✅ 是 | JS HAP 测试套件 |
| `ohos_js_app_assist_static_suite` | 9 | ✅ 是 | JS 应用辅助静态套件 |
| `ohos_test_suite` | 4 | ❌ 否 | 通用测试套件（无 hap_name） |
| `ohos_hap_assist_suite` | 2 | ✅ 是 | HAP 辅助测试套件 |
| `ohos_sh_assist_suite` | 1 | ❌ 否 | Shell 辅助测试套件（无 hap_name） |

```bash
# hap_name 未找到时，搜索测试模板 target（支持 9 种模板类型）
grep -rE "(ohos_js_app_suite|ohos_js_app_static_suite|ohos_app_assist_suite|ohos_moduletest_suite|ohos_js_hap_suite|ohos_js_app_assist_static_suite|ohos_test_suite|ohos_hap_assist_suite|ohos_sh_assist_suite)\(\"$hap_name\"\)" $OH_ROOT/test/xts/acts --include="BUILD.gn"

# 示例输出（多种模板类型）：
# /home/xianf/master/test/xts/acts/arkui/ace_c_arkui_test_api16/BUILD.gn:ohos_js_app_suite("ActsAceCArkUI16Test")
# /home/xianf/master/test/xts/acts/arkui/ace_c_arkui_test_api16_static/BUILD.gn:ohos_js_app_static_suite("ActsAceCArkUI16StaticTest")

# 提取目录路径
test_suite_dir=$(dirname <匹配的BUILD.gn路径>)
echo "✅ 定位成功（测试模板匹配）: $test_suite_dir"
```

#### 2.5.5 验证源码路径结构

**路径结构对比**：

**非 static 版本**（正确结构）：
```
ace_c_arkui_test_api16/
├── entry/
│   └── src/
│       ├── main/
│       │   └── ets/
│       │       └── pages/                    ← 页面代码（应用层）
│       └── ohosTest/                         ← 测试代码目录
│           └── ets/
│               ├── test/                     ← 测试代码（测试层）
│               │   └── textArea/
│               │       └── TextAreaLetterSpacing.test.ets  ← ✅ 正确
│               └── MainAbility/
│                   └── pages/                ← 测试页面代码
```

**static 版本**（备用结构）：
```
ace_c_arkui_test_api16_static/
├── entry/
│   └── src/
│       └── main/                             ← 注意：无 ohosTest 目录
│           ├── ets/
│           │   └── pages/                    ← 页面代码
│           └── src/                          ← 额外的 src 层
│               └── test/                     ← 测试代码
│                   └── textArea/
│                       └── TextAreaLetterSpacing.test.ets
```

**验证命令**：
```bash
# 优先查找 ohosTest 路径
ohosTest_path="$test_suite_dir/entry/src/ohosTest/ets/test"

if [ -d "$ohosTest_path" ]; then
    echo "✅ 非 static 版本，测试代码路径: $ohosTest_path"
    source_structure="ohosTest"
else
    # 回退查找 static 路径
    static_path="$test_suite_dir/entry/src/main/src/test"
    if [ -d "$static_path" ]; then
        echo "⚠️ static 版本，测试代码路径: $static_path"
        source_structure="static"
    else
        echo "❌ 源码路径结构异常"
        source_structure="invalid"
    fi
fi
```

#### 输出示例

```
Step 2.5：源码路径定位
hap_name: ActsAceCArkUI16Test
定位方法: hap_name 字段匹配
测试套件目录: /home/xianf/master/test/xts/acts/arkui/ace_c_arkui_test_api16
源码结构: ohosTest（非 static 版本）
```

**OH_ROOT 未配置时的降级处理**：
```
Step 2.5：源码路径定位
⚠️ OH_ROOT 未配置，跳过源码路径定位
备注: 将在报告中标注"未提供源码路径"
```

---

### Step 3：分析执行状态

**AI操作**：检查 shell 命令执行链

读取 module_run.log，检查执行阶段：

**阶段1**：bm install
```bash
grep "bm install" module_run.log
```

**阶段2**：aa test
```bash
grep "aa test" module_run.log
```

**阶段3**：Collected count
```bash
grep "Collected suite count" module_run.log
```

**阶段4**：[Listener] 输出
```bash
grep "[Listener]" module_run.log
```

**判定分支**：
- ①②③④ 全通过 → 测试正常执行 → 继续 hilog 切片
- ① 失败 → 定界：hap 安装失败 → 不做 hilog 切片
- ②③ 失败 → 定界：aa test 执行失败 → 不做 hilog 切片
- ④ 无 [Listener] → 定界：测试框架/启动问题 → 不做 hilog 切片

**输出**：
```
Step 3：分析执行状态
判定结果：测试正常执行
证据：
  - bm install：成功
  - aa test：成功
  - Collected count：100个用例
  - [Listener]：有逐用例输出
```

---

### Step 4：提取时间窗（用于"三、hilog日志用例详情"）

**改进要点（20260703）**：时间窗提取信息不再在"一、测试执行概况"中展示，而是下放到"三、hilog日志用例详情"每个用例下。

**改进要点（20260710）**：新增精确结束标记逻辑，解决结束行号错误问题。

**AI操作**（优先级顺序）：

**方法1（优先）**：从 hilog [Hypium] 标记提取（精确时间窗）

**⚠️ 时间窗提取必须包含完整生命周期**（2026-07-10强制改进）：

```bash
# 步骤1：提取起始标记
grep -n "Hypium.*start running case 'testcase_X'" hilog.txt

# 步骤2：提取结束标记（优先级顺序）
# 优先级①：specDone标记（最精确）
grep -n "Hypium.*testcase_X specDone end print success" hilog.txt

# 优先级②：下一个用例的start标记（边界）
grep -n "Hypium.*start running case 'testcase_Y'" hilog.txt

# 优先级③：fail标记（失败标记，包含部分后续日志）
grep -n "Hypium.*\[fail\]testcase_X" hilog.txt
```

**结束标记优先级**（强制要求）：
1. **优先级①（最精确）**：`[Hypium]XXX specDone end print success` - 用例真正结束，包含完整生命周期
2. **优先级②（边界）**：下一个 `[Hypium]start running case 'YYY'` 的前一行 - 用例边界，避免包含下一个用例日志
3. **优先级③（失败标记）**：`[Hypium][fail]XXX` - 失败标记，包含部分后续日志（不完全精确）
4. **优先级④（suite end）**：`OHOS_REPORT_RESULT` - 测试套件结束标记（最后一条用例的精确结束）
5. **优先级⑤（文件末尾）**：文件总行数 - 最后的回退方案（suite end未找到时使用）

**⚠️ 边界情况处理（2026-07-10补充）**：

**最后一条用例的特殊处理**：
- 如果是测试套件的最后一个用例（无下一个start标记）→ 使用优先级①、④或⑤
- 优先级①（specDone）：仍然可用，优先使用
- 优先级②（边界）：不可用（无下一个start）
- 优先级④（suite end）：`OHOS_REPORT_RESULT` 标记（测试套件结束）
- 优先级⑤（文件末尾）：suite end未找到时的最后回退

```bash
# 判断是否为最后一条用例
if [ -z "$(grep 'Hypium.*start running case' hilog.txt | tail -1 | grep 'testcase_X')" ]; then
    echo "✅ 这是最后一条用例"
    
    # 优先级①：specDone标记（仍然可用）
    grep -n "Hypium.*testcase_X specDone end print success" hilog.txt
    
    # 优先级④：suite end标记（测试套件结束）
    grep -n "OHOS_REPORT_RESULT" hilog.txt
    
    # 优先级⑤：文件末尾（最后回退）
    wc -l hilog.txt
fi
```

**⚠️ 禁止事项**：
- ❌ 禁止仅用 `[fail]` 标记作为结束（会遗漏后续的 specDone 日志）
- ❌ 禁止超过下一个用例的 start 标记（会包含下一个用例的日志）
- ✅ 必须按优先级①②③④⑤顺序查找结束标记
- ✅ 必须判断是否为最后一条用例（特殊处理）

**示例对比（testXmlCase001）**：

**❌ 错误示例（仅用fail标记）**：
```
起始：3082 [Hypium]start running case 'testXmlCase001'
结束：3102 [Hypium][fail]testXmlCase001 ← 错误！遗漏了specDone日志
结果：时间窗3082-3102，缺少后续关键日志（specDone标记）
```

**✅ 正确示例（使用specDone标记）**：
```
起始：3082 [Hypium]start running case 'testXmlCase001'
结束：3124 [Hypium]testXmlCase001 specDone end print success ← 正确！
结果：时间窗3082-3124，包含完整生命周期

下一个用例：3125 [Hypium]start running case 'testXmlCase002' ← 边界验证
```

**✅ 最后一条用例示例（testLastCase）**：
```
起始：60753 [Hypium]start running case 'testLastCase'
结束标记查找：
  - 优先级①：未找到specDone标记
  - 优先级②：无下一个start标记（这是最后一条用例）
  - 优先级④：找到suite end标记 OHOS_REPORT_RESULT（行43181）← 精确！
  
时间窗：60753-43181（suite end标记）
边界情况：最后一条用例，无下一个start，使用suite end标记
```

**✅ 文件末尾回退示例（suite end未找到）**：
```
起始：60753 [Hypium]start running case 'testLastCase'
结束标记查找：
  - 优先级①：未找到specDone标记
  - 优先级②：无下一个start标记（这是最后一条用例）
  - 优先级④：未找到suite end标记（OHOS_REPORT_RESULT）
  - 优先级⑤：文件末尾（行51877）← 最后回退

时间窗：60753-51877（文件末尾）
边界情况：最后一条用例，suite end未找到，使用文件末尾
```

**提取内容**：
- [Hypium]start running case → 起始时间 + 行号
- [Hypium]XXX specDone end → 结束时间 + 行号（精确）
- 设备时间（无需对齐）
- **所在日志文件** - hilog文件名（如 hilog.050.20260626-160128.txt）
- **边界验证** - 下一个用例start标记（确保不越界）

**方法2（回退）**：从 module_run.log 提取
```bash
grep "FAILED.*testcase_X" module_run.log
```

**提取内容**：
- PC时间（需对齐设备时间）

**输出**（存储到内部变量，用于"三"章节）：
```
Step 4：提取时间窗（用于"三、hilog日志用例详情"）
时间窗来源：hilog [Hypium] 标记（精确时间窗）
所在日志文件：hilog.427.20260630-020003.txt
起始时间：06-30 02:00:04.019，行号：3082
结束时间：06-30 02:00:04.020，行号：3124（specDone标记）
结束标记类型：优先级①（specDone标记）
边界验证：下一个用例start在行3125，未越界

⚠️ 注意：时间窗提取信息不在"一、测试执行概况"中展示，而是在"三、hilog日志用例详情"每个用例下展示。
```

---

### Step 5：分层过滤（增强版）

> 📖 **详细分层过滤说明**: [modules/L2_Filter/README.md](../L2_Filter/README.md)
> 
> ⚠️ **强制改进**：新增验证步骤和分层来源标记，解决"XXX占位符猜测"问题

**AI操作**：执行分层过滤（强制验证步骤）

#### 5.1 Layer 1：时间窗过滤（硬过滤）

```bash
# 提取时间窗内的日志
sed -n '<起始行号>,<结束行号>p' <hilog文件>

# 示例
sed -n '241,352p' hilog.418.20260630-015557.txt > time_window_slice.txt
```

**输出**：
- 时间窗范围：01:55:56.725 - 01:55:56.764
- 过滤结果：保留时间窗内日志，丢弃窗外噪音

#### 5.2 Layer 2：domain分组 + **验证（强制）**

**⚠️ 新增强制验证步骤** - 解决"XXX占位符猜测"问题

```bash
# 步骤1：执行domain过滤
grep -n -E '<domain正则>' time_window_slice.txt

# 示例（针对ActsBase3LibTest，domain为C003F00）
grep -n -E 'C003F[0-9a-fA-F]/' time_window_slice.txt

# 步骤2：强制验证grep结果（新增）
primary_lines=$(grep -c -E '<domain正则>' time_window_slice.txt)

if [ "$primary_lines" -eq 0 ]; then
    # ⚠️ 明确报告：时间窗内未找到domain日志
    echo "⚠️ 主分析集为空：时间窗内未找到domain日志"
    echo "统计：主: 0行"
    # 触发Layer 3扩展
    # ❌ 禁止事项：不得猜测、不得使用XXX占位符
else
    # 提取日志行，标记所有为[主]
    echo "统计：主: $primary_lines行"
    grep -n -E '<domain正则>' time_window_slice.txt | \
    awk -F: '{print "[主] 行" $1 ": " $2}'
fi
```

**AI强制行为**：
- ✅ 必须验证grep结果行数
- ✅ 如果主分析集为0行，必须明确报告"时间窗内未找到domain日志"
- ✅ 必须统计：主: N行（如实报告，不猜测）
- ❌ **禁止猜测**：不得使用XXX占位符暗示应该有日志
- ❌ **禁止省略**：不得跳过验证步骤

#### 5.3 Layer 3：渐进式扩展（强制执行）

> 📖 **详细说明**: [modules/L2_Filter/README.md](../L2_Filter/README.md)

**触发条件**：
- 主分析集为0行 → **强制触发**扩展
- 主分析集非0但规则匹配失败 → 可选触发扩展

**P1扩展（最高）**：同(PID,TID) → 同线程因果链
```bash
# 提取PID/TID对（从Hypium标记行或主分析集行）
grep -n "Hypium" time_window_slice.txt | awk '{print $3, $4}'

# P1扩展：同(PID,TID)的日志
grep -n "<PID> <TID>" time_window_slice.txt | \
awk -F: '{print "[P1] 行" $1 ": " $2}'
```

**P2扩展（中等）**：同PID不同TID → 同进程跨线程
```bash
# P2扩展：同PID不同TID的日志
grep -n "<PID>" time_window_slice.txt | grep -v "<TID>" | \
awk -F: '{print "[P2] 行" $1 ": " $2}'
```

**P3扩展（兜底）**：位置窗口前/后各20行 → 上下文兜底
```bash
# P3扩展：位置窗口（基于主分析集行号或Hypium标记行号）
sed -n '<行号-20>,<行号+20>p' time_window_slice.txt | \
awk '{print "[P3] 行" NR+<起始行号-1> ": " $0}'
```

**强制要求**：
- ✅ 必须执行P1/P2/P3扩展（当主分析集为0行时）
- ✅ 必须标记扩展日志来源：[P1]/[P2]/[P3]
- ✅ 必须统计各分层行数

#### 5.4 分层统计报告（强制）

**⚠️ 新增强制输出** - 供"三、hilog日志用例详情"使用

```markdown
**分层过滤统计**:

| 分层来源 | 行数 | 说明 |
|---------|------|------|
| 主分析集（domain匹配） | [N]行 | 时间窗内domain日志 |
| P1扩展（同PID/TID） | [X]行 | 同线程因果链 |
| P2扩展（同PID不同TID） | [Y]行 | 同进程跨线程 |
| P3扩展（位置窗口±20行） | [Z]行 | 上下文兜底 |

> 如果主分析集为0行，明确标注：⚠️ 时间窗内未找到domain日志
```

**输出示例**：
```
Step 5：分层过滤
时间窗过滤：保留111行（241-352），丢弃窗外噪音
主分析集：0行（⚠️ 时间窗内未找到domain C003F00日志）
P1扩展：23行（同PID/TID）
P2扩展：12行（同PID不同TID）
P3扩展：40行（位置窗口±20行）
分层统计：主: 0行 | P1: 23行 | P2: 12行 | P3: 40行
```

---

### Step 6：生成报告

> 📖 **详细报告生成说明**: [modules/L3_Report/README.md](../L3_Report/README.md)

**改进要点（20260703）**：
1. 移除"零、数据库查询记录"章节
2. "一、测试执行概况"不包含时间窗提取
3. "三、hilog日志用例详情"展示所有失败用例（同根因标记）
4. 每个用例包含完整时间窗提取信息（所在日志文件、起始/结束行号）

**AI操作**：生成4章节标准报告

**章节结构（改进后）**：
- 一、测试执行概况（测试套件信息 + Shell命令执行链判定）
- 二、失败用例清单（失败列表 + 失败详情 + 问题类型分组统计）
- 三、hilog日志用例详情（每个失败用例：基本信息 + 时间窗提取 + 源码→领域证据链 + 关键日志 + 源码分析 + 问题定界）
- 四、总结（问题汇总 + 定界结论 + 建议流转 + 用户确认提示）

**报告命名**：`XTS_Analysis_Report_YYYYMMDD.md`

**保存路径**：日志目录

---

## 输入产物

- 日志目录（含 summary_report.xml 或 module_run.log）
- hilog 日志文件（可选）
- 源码路径（可选，配置 OH_ROOT）

## 输出产物

- 形态判定结果
- 失败用例清单
- 执行状态判定结果
- 时间窗（起始/结束时间 + 行号）
- 分层过滤结果 + 分层来源标记
- 标准分析报告（4章节）

---

## 关键改进说明

**与原设计对比**：

| 对比项 | 原设计 | 新设计 | 改进效果 |
|--------|--------|--------|---------|
| 流程分支 | 单一流程 | 根据形态自动选择流程A/B | 提高适配性 |
| AI职责 | 不明确，脚本自动化 | AI主导判断，明确职责 | 符合设计理念 |
| 脚本定位 | pre_analyze.py全流程自动化 | 移除，AI自己实现 | 回归辅助定位 |
| 时间窗提取 | module_run.log优先 | hilog [Hypium] 标记优先 | 更准确 |

---

**更新时间**：2026-07-06  
**设计理念**：文档驱动AI操作，AI主导判断，脚本辅助查询  
**改进要点**：
- 2026-07-06：新增 Step 2.5（源码路径定位），基于 BUILD.gn hap_name 字段精准定位，支持 9 种测试模板类型
- 2026-07-03：时间窗提取不再在"一、测试执行概况"展示，下放至"三、hilog日志用例详情"每个用例下