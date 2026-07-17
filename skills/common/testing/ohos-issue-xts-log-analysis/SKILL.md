---
name: ohos-issue-xts-log-analysis
description: "分析XTS测试日志并定界问题归属。当用户提供XTS测试日志目录（含summary_report.xml/module_run.log/hilog.*.gz）、提到测试失败/App died/Blocked/SIGSEGV/cppcrash/jscrash、或需要hilog时间窗切片与domain定界时使用。支持4种输入形态自动识别、Shell执行链判定、源码→领域证据链追溯、崩溃栈解析。"
metadata:
  author: openharmony
  scope: common
  stage: troubleshooting
  domain: xts
  capability: log-analysis
  version: 0.1.0
  status: stable
  tags:
    - xts
    - log-analysis
    - troubleshooting
    - domain-tracing
  related-skills:
    - ohos-issue-crash-log-analysis
    - ohos-test-xts-generation
---

# ohos-issue-xts-log-analysis

> **XTS测试问题日志定界分析**

## 技能概述

ohos-issue-xts-log-analysis 是一个基于执行日志的 XTS 测试问题分析技能，采用**分层过滤模型**，支持多种输入形态自动识别。

## ⭐ 流程状态管理（2026-07-09改进）

> **核心改进**：解决流程执行混乱、重复解密、dict位置错误等问题

### 2026-07-10新增改进：分层过滤验证与标记强制

> **改进原因**: 解决"XXX占位符猜测"问题，确保如实报告、分层可追溯

**改进要点**：
- ✅ Step 5新增强制验证步骤：验证grep结果，如实报告主分析集行数
- ✅ 强制分层来源标记：所有日志摘录必须带[主]/[P1]/[P2]/[P3]标记
- ✅ 强制分层统计报告：必须报告各分层行数（主: N行 | P1: X行 | P2: Y行 | P3: Z行）
- ✅ 新增AI行为约束：禁止猜测、禁止XXX占位符、禁止省略分层标记

**改进文件**：
- `modules/L0_Standard/README.md` - Step 5增强版
- `modules/L3_Report/templates/complete_testcase_template.md` - 强制分层标记
- `modules/L0_Standard/AI_CONSTRAINTS.md` - 分层过滤专用约束（新增）

**预期效果**：
- ✅ AI如实报告实际情况（不猜测）
- ✅ 用户可判断日志是否真的存在
- ✅ 用户可追溯证据链来源（分层标记）
- ✅ 避免"XXX占位符猜测"问题

### 状态管理机制

**状态文件**：`<日志目录>/.xts_analysis_state.json`

**功能**：
- ✅ 跟踪当前执行阶段（L0_PreAnalyze → L0_Standard → L1_Decrypt → L2_Filter → L3_Report）
- ✅ 记录已完成步骤，避免重复执行
- ✅ 缓存执行结果，提升效率

**使用方式**：
```bash
# 检查流程状态
python3 scripts/state_manager.py show <日志目录>

# 检查步骤是否已完成
python3 scripts/state_manager.py check <日志目录> L1_Decrypt

# 重置状态（重新分析）
python3 scripts/state_manager.py reset <日志目录>
```

### 解密缓存机制

**解密状态文件**：`<日志目录>_parsed/.decrypt_state.json`

**功能**：
- ✅ 缓存解密结果，避免重复解密（每个文件20-60秒）
- ✅ 并行解密多个文件，效率提升10倍
- ✅ 验证解密结果，确保成功

**使用方式**：
```bash
# 并行解密（自动检查缓存）
python3 scripts/parallel_decrypt.py <日志目录>

# 验证dict位置
bash scripts/verify_dict_location.sh <日志目录>
```

### 强制要求

⚠️ **AI必须执行以下步骤**：
1. **执行前检查状态**：检查步骤是否已完成，避免重复执行
2. **解密时检查缓存**：检查解密缓存，避免重复解密
3. **执行后更新状态**：更新流程状态，标记步骤完成
4. **验证dict位置**：验证dict文件是否在正确位置（<日志目录>_parsed/dict/）

### 核心功能
- **多形态自动识别**：自动识别4种输入形态（全量报告/log根/单testsuite/hilog目录）
- **分层过滤分析**：时间窗过滤 → domain分组 → 渐进式扩展
- **源码→领域证据链**：建立API→子系统→domain→日志行的完整证据链
- **标准报告生成**：4章节标准格式，符合XTS规范

### 适用场景
- XTS 测试失败问题定界
- 应用崩溃（App died）分析
- 测试阻塞（Blocked）排查
- SO 库崩溃栈解析

## 前置配置

### OH_ROOT 路径配置（可选）

> 📖 **详细配置说明**: [docs/CONFIG.md](./docs/CONFIG.md)

**配置文件**：`./.xts-analysis-config.json`（技能根目录，有源码时可启用P0核心功能）

### 数据库验证（强制）

**验证数据库存在**：`ls ~/.opencode/skills/xts-issue-analysis/data/xts_rules.db`

**数据库表说明**：
- `module_domain`：334 条 API 模块 → domain 映射（来源：Excel + API接口文件）
- `subsystem_domain_mapping`：555 条子系统/部件 → domain 映射
- 表结构详见：[references/database_schema.md](./references/database_schema.md)

### 工具验证（强制）

> 📖 **详细工具说明**: [docs/tools/hilogtool-guide.md](./docs/tools/hilogtool-guide.md)

**hilogtool 用途**：解密加密的 hilog 日志文件（hilog.*.gz）

**⚠️ 重要提示**：
- 检测到 `hilog.*.gz` → **必须使用 hilogtool 解密**（不要用 gunzip/strings）
- **字典文件必需**：hilog解密必须配套dict文件，否则会超时失败
- **dict文件名格式**：`hilog_dict.*.zip` 或 `dict.zip`（通常与hilog同目录）
- **推荐使用并行解密**：`python3 scripts/parallel_decrypt.py <日志目录>`（效率提升10倍）

**dict文件检查**：
```bash
# 方法1：使用检测脚本（推荐）
bash scripts/check_dict.sh <hilog日志目录>

# 方法2：手动检查
ls -la <日志目录> | grep -E "hilog_dict|dict.zip"

# 方法3：验证dict位置（解密后）
bash scripts/verify_dict_location.sh <hilog日志目录>
```

**并行解密命令（推荐）**：
```bash
# 自动检查缓存，避免重复解密
python3 scripts/parallel_decrypt.py <日志目录>

# 输出目录：<日志目录>_parsed/
# 解密状态：<日志目录>_parsed/.decrypt_state.json
```

**Linux环境手动命令**（不推荐，建议使用parallel_decrypt.py）：
```bash
# 1. 先确认dict文件存在
dict_file=$(find <日志目录> -name "hilog_dict.*.zip" -o -name "dict.zip" | head -1)
[ -z "$dict_file" ] && echo "错误：未找到dict文件" && exit 1

# 2. 使用绝对路径执行hilogtool（不要cd）
DISPLAY= wine64 /绝对路径/hilogtool.exe parse -i <日志目录> -o <日志目录>_parsed -d "$dict_file"
```

## 快速开始

> 📖 **详细使用方式**: [docs/USAGE.md](./docs/USAGE.md)

### ⚠️ 强制阅读（报告生成前）

**生成报告前必须阅读以下文档，确保报告格式符合规范**：
1. ✅ [报告格式指南](./references/report-format-guide.md) - 了解4章节结构
2. ✅ **[失败用例模板](./modules/L3_Report/templates/complete_testcase_template.md)** - ⚠️ **严格按照表格格式生成每个用例**
3. ✅ [Shell命令执行链分析](./docs/workflows/shell-chain-analysis.md) - 必须用表格格式（执行阶段 | 命令 | 结果 | 状态）

### 输入形态自动识别

本技能支持4种输入形态，AI自动识别并选择对应工作流程：

| 形态 | 识别特征 | 工作流程 |
|------|----------|----------|
| ① 全量报告 | 含 `summary_report.xml` | 流程A |
| ② log 根 | 下全是 `Acts*/` 子目录 | 流程A |
| ③ 单 testsuite | 含 `module_run.log` | 流程A |
| ④ hilog 目录 | 含 `hilog.*.gz`，无 `module_run.log` | 流程B |

**示例**：`请分析 /tmp/xts_logs/20260620 目录下的测试日志`

### ⚠️ 前置检查（强制）

**解密hilog前必须执行**：

```bash
# 检查dict文件（形态③④必须）
bash scripts/check_dict.sh <hilog日志目录>
```

**检查结果处理**：
- ✅ dict文件存在 → 继续解密（时间戳不匹配也可正常解密）
- ❌ dict文件不存在 → 不执行hilogtool，使用module_run.log分析
- ⚠️ 解密耗时较长 → 每个文件约20-60秒，需等待足够时间

---

## 核心工作流程

> **设计理念**：根据输入形态自动选择工作流程，文档驱动AI操作

### ⚠️ 强制流程（证据链追溯）

**生成证据链前必须执行以下步骤（禁止跳过）**：

#### ⚠️ AI行为约束（强制）

**详细约束规则**: [.opencode/AI_BEHAVIOR_CONSTRAINTS.md](./.opencode/AI_BEHAVIOR_CONSTRAINTS.md)

**分层过滤专用约束**: [modules/L0_Standard/AI_CONSTRAINTS.md](./modules/L0_Standard/AI_CONSTRAINTS.md)

**核心禁止事项**:
1. ❌ **禁止猜测import语句**：必须使用脚本提取
2. ❌ **禁止猜测模块名**：必须从查询结果提取
3. ❌ **禁止瞎编domain值**：必须从查询结果提取
4. ❌ **禁止混淆测试框架和被测API**：必须过滤测试框架
5. ❌ **禁止跳过内部模块探索**：必须探索引用链（最多3层）
6. ❌ **禁止猜测日志内容**：必须验证grep结果，如实报告（新增）
7. ❌ **禁止使用XXX占位符**：必须明确说明日志缺失（新增）
8. ❌ **禁止省略分层标记**：所有日志必须带来源标记（新增）

**违规后果**: 报告无效，需重新生成

#### 步骤1：提取源码import（必须执行）

```bash
$ python3 scripts/extract_imports.py <测试源码文件>
```

**禁止事项**：
- ❌ 禁止猜测import语句（如：猜测`import stream from '@ohos.stream'`）
- ✅ 必须使用脚本提取实际import语句

#### 步骤2：探索引用链（可选，针对内部模块）

```bash
$ python3 scripts/explore_import_chain.py <测试源码文件> --max-depth 3
```

**适用场景**：
- 测试文件引用了内部模块（如：`import Utils from '../common/Utils'`）
- 内部模块可能封装了OpenHarmony API

#### 步骤3：查询domain（必须执行）

```bash
# API模块
$ python3 scripts/map_domain.py "@ohos.app.ability.Want"

# Kit引用
$ python3 scripts/map_domain.py "@kit.ArkTS"
```

**禁止事项**：
- ❌ 禁止猜测模块名（如：猜测`@ohos.stream`而实际是`@ohos.util.stream`）
- ❌ 禁止瞎编domain值
- ✅ 必须使用脚本查询结果

#### 步骤4：生成证据链（必须使用查询结果）

**证据链追溯模板**：
```markdown
失败用例源码(XXX.test.ets)
    │ import { stream } from '@kit.ArkTS';  ← 从脚本提取（禁止猜测）
    ▼
@kit.ArkTS 展开
    │ 查询 kit_module 表 → 找到 @ohos.util.stream
    ▼
@ohos.util.stream → domain
    │ 查询 module_domain 表 → domain: 0xD003F00（禁止瞎编）
    ▼
子系统归属
    │ subsystem: 公共基础类库（从查询结果提取）
    ▼
精准日志过滤
    │ 过滤域：C003F[0-9a-fA-F]/
    ▼
日志切片 → 行xxx-xxx
```

**强制要求**：
1. ✅ import语句必须从源码文件实际读取（禁止猜测）
2. ✅ 模块名必须从查询结果中提取（禁止猜测）
3. ✅ domain必须从查询结果中提取（禁止瞎编）
4. ✅ 必须区分测试运行时domain和被测方domain

### 流程分支

- **流程A（标准）**：形态①②③ → [modules/L0_Standard/README.md](./modules/L0_Standard/README.md)
- **流程B（受限）**：形态④ → [modules/L1_Limited/README.md](./modules/L1_Limited/README.md)
- **崩溃专项**：[modules/L0_Crash/README.md](./modules/L0_Crash/README.md)
- **冻屏专项**：[modules/L0_Freeze/README.md](./modules/L0_Freeze/README.md)

### 核心流程步骤

**前置分析**：形态识别 → 锁定失败用例 → 定位执行日志 → 分析执行状态
**日志分析**：提取时间窗 → 分层过滤
**报告生成**：生成标准报告

> 详细流程见 [modules/L0_Standard/README.md](./modules/L0_Standard/README.md)

## 辅助工具

### 脚本定位说明

> 📖 **详细脚本定位**: [scripts/README.md](./scripts/README.md)

**脚本分类**：
- **核心脚本（运行时辅助）**：AI在运行时可以使用的辅助查询脚本（4个）
- **可选脚本（高级分析）**：AI在特定场景下可以使用的专项分析脚本（2个）
- **构建脚本（只运行一次）**：在skill构建时运行，运行时不需要（1个）

**核心原则**：
- ✅ AI主导判断，脚本辅助查询
- ✅ AI可以选择使用脚本辅助，也可以自己实现
- ❌ 不要用脚本替代AI判断

### 🔒 强制脚本

**⚠️ 证据链映射必须使用以下脚本，禁止AI自行推断**

#### 1. import语句提取（新增）

```bash
# 提取源码文件的import语句并分类
python3 scripts/extract_imports.py <测试源码文件>
```

**用途**：
- 自动提取import语句
- 自动分类import类型（api_module / kit_module / internal_module / test_framework）
- 识别被测API（过滤测试框架）

#### 2. 引用链探索（新增）

```bash
# 探索内部模块的引用链（最多3层）
python3 scripts/explore_import_chain.py <测试源码文件> --max-depth 3
```

**用途**：
- 探索内部模块（如Utils.ets）中引用的OpenHarmony API
- 避免遗漏间接引用的API
- 生成完整的API调用链

#### 3. domain映射查询（已有）

```bash
python3 scripts/map_domain.py "@ohos.arkui.inspector"  # → 0xD003900 / ArkUI
python3 scripts/map_domain.py "@kit.ArkTS"             # → 展开kit并查询domain
python3 scripts/map_domain.py --list-runtime           # → 测试运行时domain（非被测方）
```

### 🔄 状态管理脚本（2026-07-09新增）

```bash
# 流程状态管理
python3 scripts/state_manager.py show <日志目录>           # 显示状态信息
python3 scripts/state_manager.py check <日志目录> <步骤>  # 检查步骤是否完成
python3 scripts/state_manager.py reset <日志目录>         # 重置状态

# 并行解密（缓存机制）
python3 scripts/parallel_decrypt.py <日志目录>            # 并行解密，自动检查缓存

# dict位置验证
bash scripts/verify_dict_location.sh <日志目录>          # 验证dict位置是否正确
```

### ✅ 核心脚本

```bash
python3 scripts/query_db.py rules --keyword "App died"  # 查询定界规则
python3 scripts/query_db.py contacts 元能力            # 查询责任人
python3 scripts/query_db.py so libace.z.so             # 查询SO库归属
python3 scripts/detect_logs.py <日志目录>              # 检测加密文件
```

### 🚀 自动化脚本（P1新增）

#### 1. 自动生成证据链

```bash
# 自动生成证据链追溯（Markdown格式，可直接粘贴到报告）
python3 scripts/generate_evidence_chain.py <测试文件> --test-case <用例名>
```

**功能**：
- 自动提取import语句
- 自动探索引用链
- 自动查询domain和subsystem
- 生成标准Markdown格式的证据链追溯

#### 2. 模板推荐

```bash
# 根据测试文件自动推荐报告模板
python3 scripts/recommend_template.py <测试文件> --subsystem <子系统名>
```

**功能**：
- 根据文件路径和API类型推荐模板
- 提供必填段落建议
- 支持多种测试场景（Stream API、ArkUI组件、元能力等）

### 可选脚本

```bash
python3 scripts/analyze_source.py test.ets            # 源码解析
python3 scripts/analyze_crash_stack.py cppcrash.log  # 崩溃栈分析
python3 scripts/filter_hilog.py -i hilog.txt -d 00310 # 分层过滤
```

> 详细说明见 [scripts/README.md](./scripts/README.md)

## 输出规范

### ⚠️ 标准报告格式（强制）

**必须包含4章节（表格格式）**：
1. **一、测试执行概况** - 测试套件信息表格 + Shell命令执行链判定**表格**
2. **二、失败用例清单** - 失败用例列表表格 + 失败详情**表格** + 问题类型分组统计**表格**
3. **三、hilog日志用例详情** - ⚠️ **每个失败用例必须包含6个标准段落（表格格式）**
4. **四、总结** - 问题汇总 + 定界结论**表格** + 建议流转 + 用户确认提示

**命名格式**: `XTS_Analysis_Report_YYYYMMDD.md`
**存储位置**: 日志目录（与module_run.log同级）

**⚠️ 三章节核心要求**：
- **每个失败用例必须包含6个标准段落**（表格格式）：基本信息、时间窗提取、源码→领域证据链、关键日志片段、源码定位与分析、问题定界
- **所有失败用例必须相同格式**，禁止简化第2-14个用例（即使同根因也需完整表格）
- **必须包含关键信息**："所在日志（hilog）"、"起始行号"、"结束行号"
- **源码→领域证据链段落必须包含表格+追溯图**
- **关键日志片段必须包含分层来源标记和分层统计**（新增）：
  - 强制报告分层过滤结果：主: N行 | P1: X行 | P2: Y行 | P3: Z行
  - 强制标记分层来源：[主]/[P1]/[P2]/[P3]
  - 如果主分析集为0行，必须明确说明"时间窗内未找到domain日志"

**表格格式示例**：
```markdown
| 项目 | 内容 |
|------|------|
| 用例名称 | textAreaLetterSpacing001 |
| 测试套件 | TextAreaLetterSpacing |
| 执行序号 | 21/39 |
| 执行结果 | FAILED |
| 消耗时间 | 8806ms |
| 所在日志（hilog） | hilog.107.20260626-162511.txt |
```

**标准模板**: ⚠️ **必须严格按照模板生成** [modules/L3_Report/templates/complete_testcase_template.md](./modules/L3_Report/templates/complete_testcase_template.md)

> 详细格式见 [references/report-format-guide.md](./references/report-format-guide.md)

## 重要注意事项

### 1. ⚠️ AI主导判断

- ✅ AI检测目录特征，判定输入形态①②③④
- ✅ AI解析失败信号源，锁定失败用例
- ✅ AI检查shell命令执行链，判定执行状态
- ✅ AI提取时间窗，执行分层过滤，生成标准报告
- ❌ 不要用脚本替代AI判断

### 2. ⚠️ 输入形态识别（强制）

**识别方法**：`ls -la <日志目录>`
- 含 summary_report.xml → 形态① → 流程A
- 下全是 Acts*/ 子目录 → 形态② → 流程A
- 含 module_run.log → 形态③ → 流程A
- 含 hilog.*.gz，无 module_run.log → 形态④ → 流程B

### 3. ⚠️ Shell命令执行链分析（强制）

检查4阶段：bm install → aa test → Collected count → [Listener]，判定测试是否正常执行。
> 详细见 [docs/workflows/shell-chain-analysis.md](./docs/workflows/shell-chain-analysis.md)

### 4. ⚠️ 时间窗提取优先级（强制）

**优先级**：hilog [Hypium] 标记（设备时间） → module_run.log（PC时间，需对齐）
> 详细见 [docs/workflows/time-window-alignment.md](./docs/workflows/time-window-alignment.md)

### 5. ⚠️ 报告格式规范（强制）

**必须包含4章节（全部表格格式）**：
1. **一、测试执行概况** - 测试套件信息表格 + Shell命令执行链判定**表格**（执行阶段 | 命令 | 结果 | 状态）
2. **二、失败用例清单** - 失败用例列表表格 + 失败详情**表格**（用例名 | 失败信息 | 问题类型）+ 问题类型分组统计**表格**
3. **三、hilog日志用例详情** - ⚠️ **每个失败用例必须包含6个标准段落（表格格式）**
4. **四、总结** - 问题汇总 + 定界结论**表格**（用例名 | 问题类型 | 归属子系统 | 归属领域 | 流转建议）+ 建议流转 + 用户确认提示

**⚠️ 三章节核心要求（最易违反）**：
- **每个失败用例必须包含6个标准段落**（表格格式）：基本信息、时间窗提取、源码→领域证据链、关键日志片段、源码定位与分析、问题定界
- **所有失败用例必须相同格式**，禁止简化第2-14个用例（即使判定为"同根因"，也必须生成完整的"基本信息"和"时间窗提取"表格）
- **必须包含关键信息**："所在日志（hilog）"、"起始行号"、"结束行号"
- **源码→领域证据链段落必须包含表格+追溯图**（证据链表格 + 源码→@ohos模块→子系统→domain→日志过滤）

**常见错误示例对比**：
- ✅ **标准报告**：709行（8个用例）→ 每个用例完整6段落，全部表格格式，包含"所在日志"、"行号"
- ❌ **错误报告**：425行（14个用例）→ 前4个完整，后10个简化，缺少表格格式和关键信息

**标准模板**: ⚠️ **生成报告前必须阅读模板** [modules/L3_Report/templates/complete_testcase_template.md](./modules/L3_Report/templates/complete_testcase_template.md)

> 详细格式见 [references/report-format-guide.md](./references/report-format-guide.md)

### 6. 加密日志解密（如有）

**⚠️ 强制要求**：
- 检测到 `hilog.*.gz` → 必须使用 hilogtool 解密（不要用 gunzip/strings）
- **dict文件必需**：未提供dict会超时失败，检查方法：`ls <日志目录> | grep hilog_dict`
- **dict文件名**：`hilog_dict.*.zip` 或 `dict.zip`（通常与hilog同目录）
- **dict时间戳**：与hilog时间戳**不需要匹配**（dict是密钥字典，与日志时间无关）
- **⚠️ 禁止cd到工具目录**：必须用绝对路径执行，否则dict会被错误地放在skill目录下（污染）
- **解密耗时**：wine处理较慢，每个文件约20-60秒，批量解密需等待足够时间（几分钟）
- dict将自动解压到**输出路径/dict/**（约50-100M），与解密日志同级

**⚠️ dict位置错误预防（强制）**：
```bash
# ❌ 错误做法：cd到工具目录（会导致dict在skill目录下）
cd ~/.opencode/skills/ohos-issue-xts-log-analysis/docs/tools/hilogtool
wine64 hilogtool.exe parse ...  # dict会被放在skill目录（污染）

# ✅ 正确做法：不cd，直接用绝对路径
DISPLAY= wine64 ~/.opencode/skills/ohos-issue-xts-log-analysis/docs/tools/hilogtool/hilogtool.exe parse \
    -i /home/user/hilog_xxx \
    -o /home/user/hilog_xxx_parsed \
    -d /home/user/hilog_xxx/hilog_dict.zip
```

**正确命令（Linux）**：
```bash
# 1. 检查并获取dict文件路径
dict_file=$(find <日志目录> -name "hilog_dict.*.zip" -o -name "dict.zip" | head -1)
echo "使用dict文件: $dict_file"

# 2. 执行解密（不要cd，用绝对路径）
DISPLAY= wine64 ~/.opencode/skills/ohos-issue-xts-log-analysis/docs/tools/hilogtool/hilogtool.exe parse \
    -i <输入目录> \
    -o <输入目录>_parsed \
    -d "$dict_file"

# 3. 验证dict位置（解密后强制执行）
bash scripts/verify_dict_location.sh <日志目录>
```

**错误示例**：
```bash
# ❌ 错误1：未检查dict文件是否存在
wine64 hilogtool.exe parse ...  # 会超时

# ❌ 错误2：cd到工具目录（dict会被放在skill目录，污染）
cd ~/.opencode/skills/ohos-issue-xts-log-analysis/docs/tools/hilogtool
wine64 hilogtool.exe parse ...

# ❌ 错误3：dict文件名错误
-d dict.zip  # 实际文件名可能是 hilog_dict.20260626-144351.zip
```

**验证与清理**：
```bash
# 验证dict位置（解密后必须执行）
bash scripts/verify_dict_location.sh <日志目录>

# 自动清理错误位置的dict
bash scripts/verify_dict_location.sh <日志目录> --clean
```

> 详细见 [docs/tools/hilogtool-guide.md](./docs/tools/hilogtool-guide.md)

### 7. ⚠️ 证据链映射（强制）

证据链的"@ohos/@kit → domain"映射必须使用 `scripts/map_domain.py`，禁止AI自行推断！

## 故障排除

### 常见问题与解决方案

**Q1: 数据库文件不存在**
- 验证：`ls ~/.opencode/skills/xts-issue-analysis/data/xts_rules.db`
- 解决：确认技能安装完整，数据库文件未丢失

**Q2: 加密日志未解密**
- ⚠️ 强制要求：发现 `hilog.*.gz` 必须使用 hilogtool 解密，不要用 gunzip/strings
- 解决：参考 [docs/tools/hilogtool-guide.md](./docs/tools/hilogtool-guide.md) 使用 hilogtool 解密

**Q3: 关键字未匹配到规则**
- 验证：使用 `scripts/query_db.py rules --keyword "<关键字>"` 查询数据库
- 解决：确认关键字拼写正确，或补充数据库规则

**Q4: SO库未在映射表中**
- 验证：使用 `scripts/query_db.py so "<SO库名>"` 查询数据库
- 解决：补充 SO 库映射或人工定界

**Q5: 报告格式不符合要求**
- ⚠️ 强制要求：报告必须包含4章节（一、测试执行概况；二、失败用例清单；三、hilog日志用例详情；四、总结）
- 解决：参考 [references/report-format-guide.md](./references/report-format-guide.md) 确保格式规范

**Q6: hilogtool 解密参数错误**
- 正确命令：`wine64 hilogtool.exe parse -i <日志目录> -o <输出目录> -d <dict目录>`
- 解决：确认 dict 目录存在（应有 256 个子目录 00-FF），验证解密结果（行数 > 0）

**Q7: 测试用例执行状态识别错误**
- 检查：Shell命令执行链（bm install → aa test → Collected count → [Listener]）
- 解决：参考 [docs/workflows/shell-chain-analysis.md](./docs/workflows/shell-chain-analysis.md) 正确判定

**Q8: 源码验证失败**
- 检查：OH_ROOT 配置正确，源码路径存在
- 解决：参考 [docs/CONFIG.md](./docs/CONFIG.md) 配置 OH_ROOT

### 强制检查清单

**分析前必须验证**：
1. ✅ 数据库文件存在
2. ✅ 加密文件已解密（如有）
3. ✅ 时间窗提取正确
4. ✅ 报告格式规范（4章节）

### 标准报告示例对比

**✅ 标准报告示例（ActsAceCArkUI16Test）**：
- 行数：709行（8个失败用例，平均88行/用例）
- 格式：每个用例完整6段落，全部表格格式
- 关键信息：包含"所在日志（hilog）"、"起始行号"、"结束行号"
- Shell命令执行链：表格格式（执行阶段 | 命令 | 结果 | 状态）
- 失败详情：表格格式（用例名 | 失败信息 | 问题类型）
- 定界结论：表格格式（用例名 | 问题类型 | 归属子系统 | 归属领域 | 流转建议）

**❌ 错误报告示例（需避免）**：
- 行数：425行（14个失败用例，过度简化）
- 格式：前4个用例完整，后10个简化（违反"禁止简化"规则）
- 缺失项：缺少"所在日志"、"起始行号"、"结束行号"
- Shell命令执行链：仅有文字描述，无表格
- 失败详情：仅有列表，无表格
- 定界结论：仅有总结，无表格

**教训总结**：
- ❌ 不要因为"同根因"就简化用例格式（必须有完整的6个标准段落表格）
- ❌ 不要省略关键信息（日志文件名、起始行号、结束行号）
- ❌ 不要用文字替代表格（Shell命令链、失败详情、定界结论必须用表格）

---

**更新时间**：2026-07-09  
**设计理念**：文档驱动AI操作，AI主导判断，脚本辅助查询  
**改进要点**：强化表格格式要求，增加示例对比，醒目提示易违反规则