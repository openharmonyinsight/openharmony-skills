# L0_PreAnalysis - 锁定失败用例与源码定位（Step 2-2.5.6）

> 流程总览见 [SKILL.md](../../SKILL.md)。约束见 [evidence-chain-constraints.md](../../references/evidence-chain-constraints.md)。源码手动回退见 [source-location.md](../../references/source-location.md)。
>
> **流程B（形态④）**：Step 2（锁定失败用例）跳过（改为用户提供用例名）；**Step 2.5（源码定位）和 Step 2.5.6（import提取）与流程A完全相同，必须执行**（用户提供路径/用例名作为输入，脚本仍定位文件、仍提取import→domain，否则Step 5无domain可过滤）。
---

## Step 2：锁定失败用例

### 失败信号源优先级

**AI操作**（优先级顺序）：

**方法1（优先）**：从 summary_report.xml 提取
```bash
grep "result=\"false\"" summary_report.xml
```

**解析XML提取**：
- testsuite name
- testcase name
- message（错误信息）

**方法2（回退）**：从 module_run.log 提取
```bash
grep "FAILED" module_run.log
```

**解析日志提取**：
- [Listener] 行中的 testsuite#caseID
- 时间戳

### 判定分支

| 失败信号源状态 | 判定 | 后续操作 |
|---------------|------|---------|
| ①或② 任一可达 | 得失败用例清单 | 继续 Step 2.5 |
| 两者均不可达 | 无失败信号源 | **必须用户提供用例名，否则中止** |
| 用户指定 testsuite 名称 | 仅分析该 testsuite 内的失败项 | 继续 Step 2.5 |

### 定位 module_run.log + 设备 SN

对每个失败 testsuite：
```bash
ls -la log/<modulename>/module_run.log
```

**提取信息**：
- 设备 SN（如 FMR0123417000740，来自 [Hdc] 行）
- bundle name（来自 aa test 命令 -b 参数）

**module_run.log 不可达** → 跳过，标注"无执行链信息"

### 输出

```
Step 2：锁定失败用例
失败用例数：X个
hap_name（源码定位用）: ActsAceCArkUI16Test  ← 用于 Step 2.5 源码路径定位
设备 SN: FMR0123417000740
bundle name: com.example.actsaac...
信号源：summary_report.xml（或 module_run.log）

失败用例列表（表格形式）：
| 序号 | 测试套件 | 用例名 | 问题类型 | 根因分类 |
|------|---------|--------|---------|---------|
| 1 | ActsAACommandImplicitStartTest | SUB_Ability_..._3100 | 断言失败 | API行为异常 |
| 2 | ActsAACommandImplicitStartTest | SUB_Ability_..._3200 | 断言失败 | [同根因用例] |
```

**hap_name 提取方法**：
- 形态①②③：从日志目录名提取 `basename <日志目录>`
- 形态④：需用户手动提供（否则无法定位源码）

**同根因用例标记规范**：
- ✅ 必须在"根因分类"列标记 `[同根因用例]`
- ✅ AI必须识别同根因用例并统一标记

---

## Step 2.5：源码路径定位

### 背景

**问题发现**：
- AI优先搜索testsuite名称或目录名，导致定位错误
- 目录命名规则与testsuite名不匹配（驼峰 vs 下划线）
- 未利用最精确的信息（testcase名称）
- OH_ROOT 静态绑定 skill 目录，不同用户路径不同（2026-07-13修复）

### ⚠️ 源码根路径解析优先级

**优先级链**（从高到低）：

| 优先级 | 来源 | 说明 |
|--------|------|------|
| ① 最高 | **用户本次输入提供的源码路径** | 用户在请求中直接给出源码路径，AI 据此推断 OH_ROOT |
| ② | **配置文件 OH_ROOT** | `.xts-analysis-config.json` 中的 `OH_ROOT` 字段 |
| ③ 最低 | **AI 主动提示用户提供** | 以上均无时，提示用户提供 |

**AI操作**：
1. 先检查用户输入是否含源码路径（如"源码路径是 /home/.../acts/ability"）
2. 含 → 优先使用用户提供的路径
3. 不含 → 回退到配置文件 OH_ROOT
4. 均无 → 提示用户提供源码路径

> 📖 详细配置说明见 [config.md](../../docs/config.md)

### 第一步：提取 testcase 名称（强制，在任何搜索之前）

**必须先从 module_run.log 提取 testcase 名称，再开始任何源码搜索。**

```bash
grep "FAILED" module_run.log
# → [Listener] [TestSuite#testcaseName FAILED]
# 提取 # 后的 testcaseName（如 request_video_delivery_fast_source_original_compatible）
```

> ⚠️ **禁止在提取 testcase 名称前做任何源码搜索操作**：
> - ❌ 禁止先做 `find -type d -name "xxx"`（目录浏览）
> - ❌ 禁止先做 `grep hap_name BUILD.gn`（hap_name 是兜底方案）
> - ❌ 禁止先浏览目录结构再猜测试文件位置
> - ✅ 必须先提取 testcase 名→用 testcase 名搜索源码→唯一匹配则直接定位

### 第二步：脚本自动定位（MUST，首个搜索动作）

**必须先运行 locate_xts_source.py 脚本。脚本失败才回退到第三步手动流程。**

```bash
# Linux/macOS
python3 scripts/locate_xts_source.py --testcase <testcase名> --root <OH_ROOT>
# 或用户提供源码路径时：--source-path <用户源码路径>（自动推断根）
# 或从配置文件回退：--testcase <testcase名>（无 --root/--source-path）

# Windows（python3 零输出/桩程序时改用启动器，详见 SKILL.md「全平台取数」）
cmd /c scripts\run.cmd locate_xts_source --testcase <testcase名> --root <OH_ROOT>
```

### 第三步：手动回退流程（仅在脚本失败时执行）

> ⚠️ 以下流程是 locate_xts_source.py 的内部逻辑展开，**仅在脚本失败时手动执行**。不要跳过脚本直接做手动搜索。
>
> 下方 `grep -r` / `find` 命令为 Linux/macOS/Git Bash 语法。Windows 原生 cmd/PowerShell 不兼容，须用 Git Bash 执行，或改用上方 `run.cmd locate_xts_source` 脚本定位（推荐）。

**优先级**：testcase 名称（最高）→ testsuite 名称 → 路径交集 → hap_name（兜底）

```
步骤一：搜索 testcase 名称（最高优先级，通常一步定位）
  ↓ 唯一匹配 → ✅ 确定

步骤二：搜索 testsuite 名称
  ↓ 唯一匹配 → ✅ 确定

步骤三：路径交集检查
  ↓ 步骤一 + 步骤二的路径交集 → 唯一则确定

步骤四：搜索 BUILD.gn 中的 hap_name（兜底方案）
  ↓ 最终兜底
```

**步骤一：搜索 testcase 名称（最高优先级）**

```bash
# 已从第一步提取 testcase 名（如 request_video_delivery_fast_source_original_compatible）
# 用 it('testcase名' 精确搜索（匹配 it() 调用，非任意出现）
grep -r "it('request_video_delivery_fast_source_original_compatible'" OH_ROOT/acts --include="*.test.ets" --include="*.test.ts"

# 结果判定
匹配数 = 1 → ✅ 成功，返回源码路径
匹配数 > 1 → 进入步骤二
匹配数 = 0 → 进入步骤二
```

**步骤二：搜索 testsuite 名称**

```bash
# 从 module_run.log 的 [Listener] 行提取 testsuite 名（# 前的部分）
# 如 [Listener] [MediaAssetManager#request_video_delivery... FAILED] → testsuite = MediaAssetManager

grep -ri "describe.*MediaAssetManager" OH_ROOT/acts --include="*.test.ets"

# 结果判定
匹配数 = 1 → ✅ 成功
匹配数 > 1 → 进入步骤三
匹配数 = 0 → 进入步骤四
```

**步骤三：路径交集检查**

```bash
# 步骤一的匹配路径 ∩ 步骤二的匹配路径 → 如果有交集 → 确定
```

**步骤四：搜索 BUILD.gn 中的 hap_name（兜底方案）**

```bash
# 从日志目录名提取 hap_name（如 ActsPhotoAccessNDKTest）
find OH_ROOT/acts -name "BUILD.gn" -exec grep -l "ActsPhotoAccessNDKTest" {} \;

# 结果判定
匹配数 = 1 → ✅ 成功，返回项目目录
匹配数 > 1 → 返回候选列表，需人工确认
匹配数 = 0 → ❌ 失败，未找到源码
```

### 实际案例

**案例**：testcase = `testWebView_getPercentComplete1006`

```bash
# 第一步：提取 testcase 名
grep "FAILED" module_run.log
# → [Listener] [getPercentComplete#testWebView_getPercentComplete1006 FAILED]

# 第二步：脚本定位
python3 scripts/locate_xts_source.py --testcase testWebView_getPercentComplete1006 --root /home/xianf/master/test/xts
# → 成功: True, 定位步骤: step1, 源码文件: .../GetPercentComplete.test.ets
```

**脚本失败时的手动回退（步骤一）**：
```bash
grep -r "it('testWebView_getPercentComplete1006'" /home/xianf/master/test/xts/acts --include="*.test.ets"
# → 唯一匹配: .../GetPercentComplete.test.ets ✅
```

### 注意事项

1. **testcase 是最精确的标识符**：唯一性最高，通常一步定位，无需后续步骤
2. **搜索模式**：用 `it('testcase名'` 精确匹配（Hypium 的 `it()` 调用），不要用裸 testcase 名搜索（会匹配到注释、变量名等）
3. **hap_name 不要转换为目录名**：直接搜索 BUILD.gn 中的 hap_name 字段（驼峰 vs 下划线转换易错）
4. **编码处理**：读取测试文件时添加 `encoding='utf-8', errors='ignore'`
5. **兜底方案**：步骤四找到项目目录后，自动搜索测试文件匹配 testcase/testsuite

### 手动回退补充（脚本失败时）

hap_name 匹配 BUILD.gn `hap_name` 字段 / 9种测试模板target / ohosTest vs static 路径结构验证，详见 [source-location.md](../../references/source-location.md)。

### 输出

测试套件目录路径 + 定位方法（hap_name / test_template / bundle_name）+ 源码结构（ohosTest / static）。

---

### Step 2.5.6：提取 import 语句（强制）

> ⚠️ **源码定位后，必须立即执行此步骤**，不可跳过

**目标**：从定位到的测试源码文件中提取 import 语句，作为后续 domain 查询的输入

```bash
# 步骤A：提取 import 语句
python3 scripts/extract_imports.py <定位到的源码文件绝对路径>

# 步骤B：查询 domain（对每个 api_module / kit_module）
python3 scripts/map_domain.py "<模块名>"

# 步骤C：（可选）探索内部模块引用链
python3 scripts/explore_import_chain.py <源码文件> --max-depth 3
```

**输出**：JSON 格式的 import 列表，含分类（api_module / kit_module / c_api / test_framework）

**后续衔接**：
- 步骤A的输出是后续 domain 查询和证据链生成的基础
- 步骤B的 domain 查询结果作为 Step 5 分层过滤的 `<domain正则>` 输入
- 禁止跳过步骤A直接进入分层过滤（详见 [AI行为约束](../../references/evidence-chain-constraints.md)）

**禁止事项**：
- ❌ 禁止跳过此步骤直接进入 Step 5 分层过滤
- ❌ 禁止猜测 import 语句（必须用脚本提取）
- ❌ 禁止在 Step 5 中使用未经验证的 domain 正则

---

