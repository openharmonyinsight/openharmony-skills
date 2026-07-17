# L3_Report - 报告生成模块

## 模块概述

报告生成模块负责生成符合规范的 XTS 测试问题分析报告，遵循4章节标准格式，包含完整的源码→领域证据链和时间窗追溯信息。

---

## 完整报告模板（固定格式，基于20260708改进）

> ⚠️ **强制要求**：报告必须严格遵循以下固定格式，不得随意调整章节标题和表格字段

### 报告标题和元信息

```markdown
# XTS测试问题分析报告

**测试套件**: ActsAceCArkUI16Test  
**设备SN**: FMR0123417000740  
**Bundle**: com.openharmony.arkui_capi_xts_api16  
**分析日期**: 2026-07-03  
**子系统**: arkui  
```

---

### 一、测试执行概况（固定格式）

```markdown
## 一、测试执行概况

### 测试套件信息

| 项目 | 值 |
|------|-----|
| 测试套件 | ActsAceCArkUI16Test |
| 设备SN | FMR0123417000740 |
| Bundle Name | com.openharmony.arkui_capi_xts_api16 |
| 总用例数 | 39 |
| 通过数 | 31 |
| 失败数 | 8 |
| 执行时间 | 1m36s |
| 测试开始时间 | 2026-06-26 16:25:10 |
| 测试结束时间 | 2026-06-26 16:26:36 |

### Shell命令执行链判定

| 阶段 | 命令/标记 | 结果 | 说明 |
|------|----------|------|------|
| 1. bm install | `bm install -p /data/local/tmp/...hap` | ✅ 通过 | hap安装成功 |
| 2. aa test | `aa test -m entry_test -b ...` | ✅ 通过 | aa test命令正常下发 |
| 3. Collected count | `Collected suite count is: X, test count is: Y` | ✅ 通过 | 用例被正常收集 |
| 4. [Listener] | `[Listener] ... PASSED/FAILED` | ✅ 通过 | 有逐用例结果输出 |

**结论**: 测试正常执行，继续进行hilog日志切片分析。
```

**固定字段说明**：
- 测试套件信息表格：必须包含9个固定字段（测试套件、设备SN、Bundle Name、总用例数、通过数、失败数、执行时间、测试开始时间、测试结束时间）
- Shell命令执行链判定表格：必须包含4个阶段（bm install、aa test、Collected count、[Listener]）
- 结论：固定格式"测试正常执行，继续进行hilog日志切片分析"

---

### 二、失败用例清单（固定格式）

```markdown
## 二、失败用例清单

### 失败用例列表

| 序号 | 测试套件 | 用例名 | 问题类型 | 根因分类 |
|------|---------|--------|---------|---------|
| 1 | TextAreaLetterSpacing | textAreaLetterSpacing001 | 断言失败 | API行为异常 |
| 2 | TextInputLetterSpacing | textInputLetterSpacing001 | TypeError | 组件查找失败 |
| 3 | textPickerTest | TestTextPickerColumnWidths001 | 断言失败 | API返回值异常 |
| 4 | textPickerTest | TestTextPickerColumnWidths002 | 断言失败 | [同根因用例] |

### 问题类型分组统计

| 问题类型 | 数量 | 占比 |
|---------|------|------|
| 断言失败(assertEqual失败) | 4 | 50% |
| TypeError(null对象访问) | 4 | 50% |
```

**固定字段说明**：
- 失败用例列表表格：必须包含5个固定字段（序号、测试套件、用例名、问题类型、根因分类）
- 同根因用例：必须在"根因分类"列标记 `[同根因用例]`
- 问题类型分组统计表格：必须包含3个固定字段（问题类型、数量、占比）

---

### 三、hilog日志用例详情（固定格式）

```markdown
## 三、hilog日志用例详情

### 用例1：TextAreaLetterSpacing#textAreaLetterSpacing001

#### 基本信息

| 项目 | 值 |
|------|-----|
| 测试套件 | TextAreaLetterSpacing |
| 用例名 | textAreaLetterSpacing001 |
| 源码路径 | `ace_c_arkui_test_api16_static/entry/src/main/src/test/textArea/TextAreaLetterSpacing.test.ets` |
| 所属子系统 | arkui |
| 所属domain | A03D00 (JSAPP) |

#### 时间窗提取

> **参考文档**: docs/workflows/time-window-alignment.md

| 项目 | 值 |
|------|-----|
| 所在日志(hilog) | hilog.107.20260626-162511.txt |
| 起始时间 | 06-26 16:25:42.611 (行6355) |
| 结束时间 | 06-26 16:25:51.417 (行18116) |
| 用例执行时长 | 8806ms |

#### 源码→领域证据链

| API | 子系统 | domain | 日志行 | 时间 |
|-----|--------|--------|--------|------|
| inspector.getInspectorByKey('text7') | 测试框架 | A03D00/JSAPP | 18098-18117 | 16:25:50.894-51.417 |

**证据链追溯**:
```
失败用例源码(.ets)
    │ import inspector from '@ohos.arkui.inspector'
    ▼
@ohos 模块 → 子系统
    │ '@ohos.arkui.inspector' → ArkUI子系统
    ▼
子系统 → hilog domain
    │ 测试应用日志 → A03D00 (JSAPP)
    ▼
精准日志过滤
    │ 过滤域：A03D00
    ▼
日志切片 → 行18098-18117
```

#### 关键日志

**所在日志**: hilog.107.20260626-162511.txt（行18098-18117）

```
[主] 行18098: I A03D00/JSAPP: [textAreaLetterSpacing001] component obj3 is: {"$type":"Text"...}
[主] 行18099: I A03D00/JSAPP: [textAreaLetterSpacing001] content is: "#00000000"
[主] 行18116: I A03D00/JSAPP: [Hypium][fail]textAreaLetterSpacing001 ; consuming 8806ms
[主] 行18117: I A03D00/JSAPP: [Hypium][failDetail]expect #00000000 equals #FFE31111
```

#### 源码分析

源码位置：`TextAreaLetterSpacing.test.ets:82`

```typescript
expect(obj3.getElement('$attrs').getString('backgroundColor')).assertEqual('#FFE31111');
```

测试逻辑：测试通过 `inspector.getInspectorByKey('text7')` 获取组件属性，验证 `backgroundColor` 是否为预期值 `#FFE31111`。

#### 问题定界

| 项目 | 值 |
|------|-----|
| 错误类型 | 断言失败 |
| 错误信息 | expect #00000000 equals #FFE31111 |
| 实际值 | backgroundColor = #00000000 (透明) |
| 预期值 | backgroundColor = #FFE31111 (红色) |
| 定界结论 | **测试用例问题/API实现问题** |
| 定界依据 | backgroundColor属性返回透明色而非预期的红色，可能原因：1) 组件未正确设置背景色；2) inspector获取属性时机不对；3) previewText回调接口未正确触发 |
| 建议流转 | **arkui子系统** - 需确认TextArea组件letterSpacing属性与previewText回调接口的联动行为 |

---

### 用例2：textPickerTest#TestTextPickerColumnWidths002 [同根因用例]

与TestTextPickerColumnWidths001同根因，columnWidths属性返回值异常。
```

**固定标签说明**（每个用例必须包含）：
- 基本信息：必须包含测试套件、用例名、源码路径、所属子系统、所属domain
- 时间窗提取：必须包含参考文档标签、所在日志、起始时间+行号、结束时间+行号、用例执行时长
- 源码→领域证据链：必须包含证据链表格和证据链追溯图
- 关键日志：必须标注所在日志文件和行号范围，使用 `[主]`/`[备]` 标记
- 源码分析：必须包含源码位置、源码片段、测试逻辑分析
- 问题定界：必须使用表格呈现定界依据

**同根因用例说明**：
- 标题必须追加 `[同根因用例]` 标签
- 正文简要说明同根因原因

---

### 四、总结（固定格式）

```markdown
## 四、总结

### 问题汇总

| 问题分类 | 数量 | 具体问题 |
|---------|------|---------|
| API行为异常 | 2 | TextArea的backgroundColor返回透明色；TextPicker的columnWidths返回0.00px |
| 组件查找失败 | 2 | textinput组件未找到；image组件未找到 |
| 测试代码缺陷 | 1 | dragCaseTest003缺少pushPage调用 |

### 定界结论表格

| 用例名 | 问题类型 | 定界结论 | 建议流转 |
|--------|---------|---------|---------|
| textAreaLetterSpacing001 | 断言失败 | API行为问题 | arkui子系统 |
| textInputLetterSpacing001 | TypeError | 测试用例/UI渲染问题 | arkui子系统 |
| TestTextPickerColumnWidths001/002/003 | 断言失败 | API实现问题 | arkui子系统 |
| dragCaseTest001/002/003 | TypeError | 测试用例问题 | XTS测试团队 |

### 建议流转

1. **arkui子系统**: TextAreaLetterSpacing、TextInputLetterSpacing、TextPickerColumnWidths相关用例，需确认组件属性实现是否符合预期
2. **XTS测试团队**: DragTest用例dragCaseTest003存在明显代码缺陷（缺少pushPage），需修复测试代码

### 用户确认提示

请确认以下问题：
1. TextArea组件的letterSpacing属性与previewText回调的联动行为是否需要backgroundColor变色？测试预期值为#FFE31111，但实际返回#00000000（透明）。
2. TextInputLetterSpacing页面是否正确配置了id='textinput'的组件？UiTest框架在行18454明确记录"self node not found"。
3. TextPicker组件的columnWidths属性在设置后是否应该立即生效？实际返回"0.00px"而非预期宽度值。
4. DragTest用例dragCaseTest003是否需要补充`Utils.pushPage`调用？源码分析显示该用例缺少页面加载逻辑。
```

**固定标签说明**：
- 问题汇总：必须使用表格，包含问题分类、数量、具体问题
- 定界结论表格：必须包含用例名、问题类型、定界结论、建议流转
- 建议流转：必须列出具体子系统和详细说明
- 用户确认提示：必须至少包含3条具体确认事项

---

## 展示规范详解（P1改进，基于20260708）

### 1. 源码→领域证据链展示规范

> ⚠️ **强制要求**：证据链的"@ohos/@kit → domain"映射必须使用 `scripts/map_domain.py` 查询，禁止AI自行推断！

**完整展示格式（固定）**：

```markdown
#### 源码→领域证据链

| API | 子系统 | domain | 日志行 | 时间 |
|-----|--------|--------|--------|------|
| inspector.getInspectorByKey('text7') | 测试框架 | A03D00/JSAPP | 18098-18117 | 16:25:50.894-51.417 |

**证据链追溯**:
```
失败用例源码(.ets)
    │ import inspector from '@ohos.arkui.inspector'
    ▼
@ohos 模块 → 子系统
    │ '@ohos.arkui.inspector' → ArkUI子系统
    ▼
子系统 → hilog domain
    │ 测试应用日志 → A03D00 (JSAPP)
    ▼
精准日志过滤
    │ 过滤域：A03D00
    ▼
日志切片 → 行18098-18117
```

**脚本查询示例**:
```bash
# 查询被测方API
python3 scripts/map_domain.py "@ohos.arkui.inspector"
# 返回：domain=0xD003900, subsystem=ArkUI（被测方）

# 查询测试运行时domain
python3 scripts/map_domain.py --list-runtime
# 返回：A03D00/JSAPP（测试运行时，非被测方）
```
```

**必填字段说明**：
- 证据链表格：必须包含API、子系统、domain、日志行、时间5个字段
- 证据链追溯图：必须展示从源码→@ohos模块→子系统→domain→日志过滤的完整流程
- 脚本查询示例：必须展示使用map_domain.py查询的具体命令

---

### 2. 关键日志片段展示规范

**完整展示格式（固定）**：

```markdown
#### 关键日志

**所在日志**: hilog.107.20260626-162511.txt（行18098-18117）

```
[主] 行18098: I A03D00/JSAPP: [textAreaLetterSpacing001] component obj3 is: {"$type":"Text"...}
[主] 行18099: I A03D00/JSAPP: [textAreaLetterSpacing001] content is: "#00000000"
[主] 行18116: I A03D00/JSAPP: [Hypium][fail]textAreaLetterSpacing001 ; consuming 8806ms
[主] 行18117: I A03D00/JSAPP: [Hypium][failDetail]expect #00000000 equals #FFE31111
```
```

**展示要求**：
- ✅ 必须标注所在日志文件和行号范围：`hilog.107.20260626-162511.txt（行18098-18117）`
- ✅ 使用代码块格式展示日志内容
- ✅ 每行日志前必须标注 `[主]`（主分析集）或 `[备]`（备用集）
- ✅ 突出显示失败关键字（如 `[Hypium][fail]`、`[Hypium][error]`）

**分层来源标记说明**：
- `[主]`：主分析集（domain匹配失败用例引用API）
- `[P1]`：同(PID,TID)扩展（同线程因果链）
- `[P2]`：同PID不同TID扩展（同进程跨线程）
- `[P3]`：位置窗口前/后各20行（上下文兜底）
- `[备]`：备用集（domain不匹配的行，主→备用扩展触发时）

---

### 3. 同根因用例展示规范

**完整展示格式（固定）**：

```markdown
### 用例2：textPickerTest#TestTextPickerColumnWidths002 [同根因用例]

**根因关联**: 与TestTextPickerColumnWidths001同根因

**相同现象**: columnWidths属性返回"0.00px"而非预期宽度值

**源码位置**: `TextPickerColumnWidthsTest.test.ets:71`（仅参数不同）

---

### 用例8：DragTest#dragCaseTest003 [同根因用例]

**根因关联**: 与dragCaseTest001同根因，但存在额外缺陷

**相同现象**: 组件id='image'查找失败

**额外缺陷**: 源码中dragCaseTest003缺少`Utils.pushPage`调用，导致页面未加载

**源码位置**: `DragCaseTest.test.ets:103-105`

```typescript
it('dragCaseTest003', Level.LEVEL1, async (done: () => void): Promise<void> => {
    let PAGE_TAG = 'DragCaseTest3'
    await panAndPinchGesture('image')  // 缺少 await Utils.pushPage(...)
```
```

**展示要求**：
- ✅ 标题必须追加 `[同根因用例]` 标签
- ✅ 必须说明根因关联（与哪个用例同根因）
- ✅ 必须说明相同现象
- ✅ 如有差异点，必须说明额外缺陷
- ✅ 如有源码差异，必须提供源码位置和片段

---

### 4. 定界依据表格化呈现规范

**完整展示格式（固定）**：

```markdown
#### 问题定界

**定界依据**:

| 项目 | 内容 |
|------|------|
| 失败API | inspector.getInspectorByKey |
| API归属 | ArkUI子系统 / Ace部件 |
| 被测方domain | 0xD003900（C0039xx） |
| 定界规则 | assert.*fail - API返回值异常 |
| 定界结论 | **被测方问题** - ArkUI/Ace |

**定界说明**:
- 测试用例正确调用了API，参数合法
- API返回值不符合预期，导致断言失败
- 问题归属被测方（ArkUI/Ace子系统），而非测试用例本身
```

**必填字段说明**：
- 定界依据表格：必须包含失败API、API归属、被测方domain、定界规则、定界结论5个字段
- 定界说明：必须详细解释归属理由（至少3条）

---

### 5. 源码分析内容规范

**完整展示格式（固定）**：

```markdown
#### 源码分析

**源码位置**: `<源码路径>:<行号范围>`

**源码片段**:
```typescript
expect(obj3.getElement('$attrs').getString('backgroundColor')).assertEqual('#FFE31111');
```

**测试逻辑分析**:
1. **测试逻辑**: 测试通过 `inspector.getInspectorByKey('text7')` 获取组件属性，验证 `backgroundColor` 是否为预期值 `#FFE31111`
2. **预期行为**: API应返回组件的backgroundColor属性值
3. **实际行为**: API返回透明色 `#00000000`
4. **失败原因**: backgroundColor属性返回透明色而非预期的红色

**源码关键行**:
- 行82：关键API调用 inspector.getInspectorByKey('text7')
- 行82：断言失败点 expect().assertEqual('#FFE31111')
```

**必填字段说明**：
- 源码位置：必须包含源码路径和行号范围
- 源码片段：必须包含关键代码片段
- 测试逻辑分析：必须包含测试逻辑、预期行为、实际行为、失败原因4个部分
- 源码关键行：必须标注关键操作和断言失败点

---

## 报告核心要求

### 强制要求

⚠️ **强制要求**：**所有情况必须使用完整格式（4章节）**

**报告结构（基于20260703改进）**：
```markdown
# XTS测试问题分析报告

## 一、测试执行概况
## 二、失败用例清单
## 三、hilog日志用例详情
## 四、总结
```

### 改进要点（20260703）

1. **移除"零、数据库查询记录"章节** - 定界依据在"三、hilog日志用例详情"的"问题定界"部分说明
2. **"一、测试执行概况"不包含时间窗提取** - 时间窗提取下放到"三、hilog日志用例详情"每个用例下
3. **"三、hilog日志用例详情"展示所有失败用例** - 同根因用例标记标签并继承结果
4. **每个用例包含完整时间窗追溯信息** - 所在日志文件、起始/结束时间、起始/结束行号

### 禁止行为

- ❌ 不要生成多个报告文件
- ❌ 不要生成补充报告、最终报告等额外文件
- ❌ 不要在三章节添加"问题根因汇总"、"定界结论"等冗余内容
- ❌ 不要在"一、测试执行概况"中展示时间窗提取
- ❌ 不要遗漏失败用例（除非同根因已标记）

## 新增内容（IMPROVEMENT_PLAN）

### 1. 源码→领域证据链段落

在"三、hilog日志用例详情"每个用例节，**新增**标准段落：

**位置**：在现有 5 个标准段落之前

**内容格式**：
```markdown
**源码→领域证据链**：
- 失败 API 源自 @ohos.UiTest → subsystem=测试框架 → domain=0xD003100
- 用例 startAbility 触发 @ohos.app.ability → subsystem=元能力 → domain=0xD001300
- 故过滤域含 0xD003100 + 0xD001300
```

**证据链追溯**：
```
失败用例源码(.ets)
    │ import {Driver, ON} from '@kit.TestKit'
    ▼
@kit → @ohos 模块
    │ '@kit.TestKit' 聚合 '@ohos.UiTest'
    ▼
模块 → 中文子系统
    │ '@ohos.UiTest' → "测试框架"
    ▼
子系统 → hilog domain
    │ "TestSystem" → 0xD003100
    ▼
精准日志过滤
```

### 2. 日志分层字段

在用例详情表格中**新增**两个字段：

| 项目 | 内容 |
|------|------|
| 日志过滤域 | C0031xx(UiTestKit) + C0013xx(AAFwk) |
| 日志分层来源 | 主分析集(domain匹配) + P1 PID/TID扩展 + P3 位置窗口 |
| 日志分层统计 | 主: 47行 \| P1: 23行 \| P2: 12行 \| P3: 40行 |

### 3. 分层来源标记说明

每行日志摘录前标注来源：

```markdown
**hilog日志摘录**（按domain+PID/TID分层过滤）：
```
[主] 行47: ... C00310/UiTestKit: findComponent failed ...
[P1] 行52: ... C00310/UiTestKit: component not found ...
[P2] 行61: ... C0013xx/Ams: ability launched ...
[P3] 行58: ... (上下文) ...
```
```

**标记含义**：
- `[主]`：主分析集（domain 匹配失败用例引用 API）
- `[P1]`：同 (PID, TID) 扩展（同线程因果链）
- `[P2]`：同 PID、不同 TID 扩展（同进程跨线程）
- `[P3]`：位置窗口前/后各 20 行（上下文兜底）

### 4. 扩展触发提示

当主分析集 0 命中触发扩展到备用集时，报告需显式标注：

```markdown
> ⚠️ 扩展提示：主分析集(domain匹配)0条规则命中，已扩展到备用集（时间窗内全量）重跑分析
```

## 报告章节详细模板（基于20260703改进）

### "一、测试执行概况"章节模板

**改进要点**：不包含时间窗提取，聚焦测试套件基本信息和Shell命令执行链判定。

#### 测试套件信息表格（必须包含）

```markdown
### 1.1 测试套件信息

| 项目 | 内容 |
|------|------|
| 测试套件 | ActsAACommandImplicitStartTest |
| 用例总数 | 32 |
| 通过数 | 31 |
| 失败数 | 1 |
| 执行时间 | 11s（PC时间） |
| 设备SN | FMR0123417000740 |
| Bundle Name | com.example.aacommandimplicitstarttest |
```

#### Shell命令执行链判定表格（必须包含）

```markdown
### 1.2 Shell命令执行链判定

| 执行阶段 | 命令 | 结果 | 状态 |
|---------|------|------|------|
| ① HAP安装 | `bm install -p /data/local/tmp/ActsAACommandImplicitStartTest.hap` | ✅ 成功 | 正常 |
| ② aa test下发 | `aa test -m entry_test -b com.example...` | ✅ 成功 | 正常 |
| ③ 用例收集 | `Collected suite count is: 1, test count is: 32` | ✅ 成功 | 正常 |
| ④ 用例执行 | `[Listener] PASSED/FAILED` 输出 | ✅ 成功 | 正常 |

**判定结论**: ✅ 测试正常执行，继续 hilog 切片分析
```

#### 失败情况表格模板

```markdown
### 1.2 Shell命令执行链判定

| 执行阶段 | 命令 | 结果 | 状态 |
|---------|------|------|------|
| ① HAP安装 | `bm install -p ...` | ❌ 失败 | 签名验证失败 |
| ② aa test | `aa test -m entry_test -b ...` | ⚠️ 未执行 | 因install失败中断 |
| ③ Collected count | - | ⚠️ 未执行 | 因install失败中断 |
| ④ 用例执行 | - | ⚠️ 未执行 | 因install失败中断 |

**判定结论**: ❌ hap安装失败（环境问题），不做 hilog 切片分析
```

---

### "二、失败用例清单"章节模板

**改进要点**：可选增加问题类型分组统计。

#### 失败用例列表（必须包含）

```markdown
### 2.1 失败用例列表

| 序号 | 用例名称 | 结果 | 执行时长 |
|------|---------|------|---------|
| 1 | SUB_Ability_AbilityRuntime_HyperSnapManager_SetHyperSnapEnabled_0100 | FAILED | 1ms |
| 2 | SUB_Ability_AbilityRuntime_HyperSnapManager_SetHyperSnapEnabled_0200 | FAILED | 0ms |
| 3 | SUB_Ability_AbilityRuntime_HyperSnapManager_RequestRebuildHyperSnap_0100 | FAILED | 0ms |
```

#### 失败详情（必须包含）

```markdown
### 2.2 失败详情

| 用例名 | 失败信息 | 问题类型 |
|--------|---------|---------|
| SUB_Ability_AbilityRuntime_HyperSnapManager_SetHyperSnapEnabled_0100 | `expect undefined equals 16000150` | API未返回预期错误码 |
| SUB_Ability_AbilityRuntime_HyperSnapManager_SetHyperSnapEnabled_0200 | `expect undefined equals 16000150` | API未返回预期错误码 |
| SUB_Ability_AbilityRuntime_HyperSnapManager_RequestRebuildHyperSnap_0100 | `expect undefined equals 16000150` | API未返回预期错误码 |
```

#### 问题类型分组统计（可选）

```markdown
### 2.3 问题类型分组统计

| 问题类型 | 用例数 | 用例列表 |
|---------|--------|---------|
| API功能缺陷 | 3 | SetHyperSnapEnabled_0100, SetHyperSnapEnabled_0200, RequestRebuildHyperSnap_0100 |
```

---

### "三、hilog日志用例详情"章节模板

**改进要点（20260703）**：
1. 展示所有失败用例，同根因用例标记标签并继承结果
2. 每个用例包含：基本信息 + 时间窗提取 + 源码→领域证据链 + 关键日志 + 源码分析 + 问题定界
3. 时间窗提取包含：所在日志文件、起始/结束时间、起始/结束行号

#### 完整用例模板（独立用例）

```markdown
### 3.1 SUB_Ability_AbilityRuntime_HyperSnapManager_SetHyperSnapEnabled_0100

#### 3.1.1 基本信息

| 项目 | 内容 |
|------|------|
| 用例名称 | SUB_Ability_AbilityRuntime_HyperSnapManager_SetHyperSnapEnabled_0100 |
| 测试套件 | HyperSnapManagerTest |
| 执行序号 | 1/5 |
| 执行结果 | FAILED |
| 消耗时间 | 1ms |
| 所在日志（hilog） | hilog.050.20260626-160128.txt |

#### 3.1.2 时间窗提取

| 项目 | 内容 |
|------|------|
| 所在日志文件 | hilog.050.20260626-160128.txt |
| 起始时间 | 06-26 16:01:29.239 |
| 起始行号 | 4000 |
| 结束时间 | 06-26 16:01:29.310 |
| 结束行号 | 4662 |
| 时间来源 | hilog [Hypium] 标记（设备时间） |

#### 3.1.3 源码→领域证据链

⚠️ **强制要求**：此段落必须独立展示，包含表格和证据链追溯图，建立从源码API到日志domain的完整链路。

| API | 子系统 | domain | 日志行 | 时间 |
|-----|--------|--------|--------|------|
| hyperSnapManager.setHyperSnapEnabled(false) | Ability | A00000/testTag | 4299-4307 | 16:01:29.306-307 |

**证据链追溯**:
```
失败用例源码(.ets)
    │ import hyperSnapManager from '@ohos.hypersnap'
    ▼
@ohos 模块 → 子系统
    │ '@ohos.hypersnap' → Ability子系统
    ▼
子系统 → hilog domain
    │ "Ability" → A00000/testTag
    ▼
精准日志过滤
    │ 过滤域：A00000/testTag
    ▼
日志切片 → 行4299-4307
```

#### 3.1.4 关键日志片段

**所在日志**: hilog.050.20260626-160128.txt（行4266-4317）

**关键证据**:
```
行4299: [testTag] SUB_Ability_AbilityRuntime_HyperSnapManager_SetHyperSnapEnabled_0100 supprot false
行4304: [testTag] SUB_Ability_AbilityRuntime_HyperSnapManager_SetHyperSnapEnabled_0100 success
行4305: [testTag] SUB_Ability_AbilityRuntime_HyperSnapManager_SetHyperSnapEnabled_0100 catch
行4317: [Hypium][failDetail]expect undefined equals 16000150
```

#### 3.1.5 源码定位与分析

**源码位置**: `/home/xianf/master/test/xts/acts/ability/ability_runtime/.../HyperSnapManagerTest.test.ets:80-105`

**源码片段**:
```typescript
it('SUB_Ability_AbilityRuntime_HyperSnapManager_SetHyperSnapEnabled_0100', Level.LEVEL0, async (done: Function) => {
  hilog.info(0x0000, 'testTag', 'SUB_Ability_AbilityRuntime_HyperSnapManager_SetHyperSnapEnabled_0100 supprot ' + supportUse);
  if(!supportUse){
    try{
      hyperSnapManager.setHyperSnapEnabled(false);  // ← 应该抛出16000150错误码
      hilog.info(0x0000, 'testTag', 'SUB_Ability_AbilityRuntime_HyperSnapManager_SetHyperSnapEnabled_0100 success');
      expect().assertFail();  // ← API成功执行导致触发此断言失败
    }catch(e){
      hilog.info(0x0000, 'testTag', 'SUB_Ability_AbilityRuntime_HyperSnapManager_SetHyperSnapEnabled_0100 catch');
      expect((e as BusinessError).code).assertEqual(16000150);  // ← 预期错误码16000150
    }
    done();
  }
})
```

**源码分析**:
1. `supportUse=false`（设备不支持HyperSnap）
2. 调用 `hyperSnapManager.setHyperSnapEnabled(false)` 时：
   - **预期行为**: 抛出 BusinessError，错误码 16000150
   - **实际行为**: API成功执行，无异常抛出
3. 因API未抛异常，触发 `expect().assertFail()`
4. `(e as BusinessError).code` 为 undefined，导致最终断言失败

#### 3.1.6 问题定界

| 项目 | 内容 |
|------|------|
| 问题类型 | API功能缺陷 |
| 影响范围 | Ability子系统 - HyperSnapManager |
| 定界依据 | 关键字'undefined'匹配数据库规则 → 测试框架（优先级9） |
| 归属判定 | **Ability子系统问题** |
```

#### 同根因用例模板（继承结果）

```markdown
### 3.2 SUB_Ability_AbilityRuntime_HyperSnapManager_SetHyperSnapEnabled_0200 [同根因用例]

#### 3.2.1 基本信息

| 项目 | 内容 |
|------|------|
| 用例名称 | SUB_Ability_AbilityRuntime_HyperSnapManager_SetHyperSnapEnabled_0200 |
| 测试套件 | HyperSnapManagerTest |
| 执行序号 | 2/5 |
| 执行结果 | FAILED |
| 消耗时间 | 0ms |
| 所在日志（hilog） | hilog.050.20260626-160128.txt |

#### 3.2.2 时间窗提取

| 项目 | 内容 |
|------|------|
| 所在日志文件 | hilog.050.20260626-160128.txt |
| 起始时间 | 06-26 16:01:29.308 |
| 起始行号 | 4375 |
| 结束时间 | 06-26 16:01:29.309 |
| 结束行号 | 4445 |
| 时间来源 | hilog [Hypium] 标记（设备时间） |

#### 3.2.3 根因继承

**同根因说明**: 与用例 3.1 相同，API `setHyperSnapEnabled(true)` 在不支持设备上也未抛出异常。

**差异点**: 参数值为 `true`，但失败根因与 3.1 一致。

#### 3.2.4 问题定界

| 项目 | 内容 |
|------|------|
| 问题类型 | API功能缺陷（同根因） |
| 影响范围 | Ability子系统 - HyperSnapManager |
| 归属判定 | **Ability子系统问题**（继承3.1结论）
```

---

### "四、总结"章节模板

**改进要点**：用户确认提示更具体，修复建议更可执行。

#### 问题汇总（必须包含）

```markdown
### 4.1 问题汇总

**共性问题**: 
- HyperSnapManager 的三个 API（`setHyperSnapEnabled(false)`, `setHyperSnapEnabled(true)`, `requestRebuildHyperSnap()`）
- 在不支持 HyperSnap 的设备上（`supportUse=false`）
- 未按规范抛出错误码 16000150
- 导致测试用例预期行为失效

**根本原因**:
- 设备不支持 HyperSnap 功能（beforeAll 中通过 `hidumper -s 1901 -a -a` 检查 `libforkall_plugin.z.so` 不存在）
- API 实现未正确校验设备支持状态，或未正确返回错误码 16000150
```

#### 定界结论表格（必须包含）

```markdown
### 4.2 定界结论

| 用例名 | 问题类型 | 归属子系统 | 归属领域 | 流转建议 |
|--------|---------|-----------|---------|---------|
| SUB_Ability_AbilityRuntime_HyperSnapManager_SetHyperSnapEnabled_0100 | API功能缺陷 | Ability | AbilityRuntime | 流转至 Ability 子系统 |
| SUB_Ability_AbilityRuntime_HyperSnapManager_SetHyperSnapEnabled_0200 | API功能缺陷 | Ability | AbilityRuntime | 流转至 Ability 子系统（同根因） |
| SUB_Ability_AbilityRuntime_HyperSnapManager_RequestRebuildHyperSnap_0100 | API功能缺陷 | Ability | AbilityRuntime | 流转至 Ability 子系统（同根因） |

**定界依据**:
1. 测试正常执行（Shell命令链完整）
2. API调用成功但未返回预期错误码
3. 属于 API 实现问题而非测试环境问题
4. 源码验证：测试用例逻辑正确，符合API规范
```

#### 建议流转（必须包含）

```markdown
### 4.3 建议流转

**主责任人**: Ability 子系统 - AbilityRuntime 模块  
**问题类型**: API 功能缺陷  
**修复建议**: 
- 检查 `hyperSnapManager` API 实现，确保在不支持 HyperSnap 的设备上正确返回错误码 16000150
- 验证 Forkall 插件检测逻辑与 API 错误处理的一致性

**修复示例（可选）**:
```typescript
// 建议在 hyperSnapManager.setHyperSnapEnabled 实现中增加检查
if (!isHyperSnapSupported()) {
  throw new BusinessError(16000150, "HyperSnap not supported on this device");
}
```
```

#### 用户确认提示（必须包含，至少3条，更具体）

```markdown
### 4.4 用户确认提示

请确认以下关键信息：

1. ✅ **测试环境判定**: 
   - 设备不支持 HyperSnap（beforeAll 中通过 `hidumper -s 1901 -a -a` 检查 `libforkall_plugin.z.so` 不存在）
   - 此结论是否正确？是否需要验证其他环境条件？

2. ✅ **API行为判定**: 
   - HyperSnapManager API 在不支持设备上应该返回错误码 16000150
   - 此预期是否符合 API 规范？是否有 API 文档链接？

3. ✅ **定界结论判定**: 
   - 问题归属 Ability 子系统
   - 是否需要进一步验证环境配置？
   - 是否需要流转至 Ability 子系统责任人？
```

---

## 标准段落结构（每个失败用例）

**改进要点（20260703）**：每个失败用例详情节**必须包含以下6个标准段落**（按顺序排列）：

1. **基本信息** - 用例名、testsuite、执行序号、执行结果、消耗时间、所在日志（hilog）
2. **时间窗提取** - 所在日志文件、起始时间、起始行号、结束时间、结束行号、时间来源
3. ⚠️ **源码→领域证据链** - **独立段落**，必须包含：
   - 证据链表格（API | 子系统 | domain | 日志行 | 时间）
   - 证据链追溯图（源码→@ohos模块→子系统→domain→日志过滤）
4. **关键日志片段** - 带行号
5. **源码定位与分析** - 源码位置、源码片段、源码分析
6. **问题定界** - 问题类型、影响范围、定界依据、归属判定

**同根因用例特殊处理**：
- 标题追加 `[同根因用例]` 标签
- 包含：基本信息 + 时间窗提取 + 根因继承 + 问题定界
- 根因继承章节说明差异点（如有）

## 报告生成流程

### AI 主动生成

AI 应按照以下步骤主动生成报告：

1. ✅ 阅读改进计划（IMPROVEMENT_PLAN.md）
2. ✅ 根据 L0/L1/L2 的输出产物组装报告内容
3. ✅ 移除"零、数据库查询记录"章节
4. ✅ 在"一、测试执行概况"中不包含时间窗提取
5. ✅ 在"三、hilog日志用例详情"中展示所有失败用例（同根因标记）
6. ✅ 每个用例包含完整时间窗提取信息（日志文件、行号）
7. ✅ 在"四、总结"中提供更具体的用户确认提示
8. ✅ 保存到日志目录（`XTS_Analysis_Report_YYYYMMDD.md`）

### 输入产物

从其他模块接收：

- **L0_PreAnalyze**：failed_cases, exec_status, time_windows, device_sn
- **L1_Decrypt**：解密后的日志文件
- **L2_Filter**：分层过滤后的日志切片 + 分层统计

### 输出产物

- 完整的 XTS 分析报告（4章节）
- 报告文件路径

## 质量检查清单（基于20260703改进）

### 一章节检查

| 检查项 | 要求 |
|--------|------|
| 测试套件信息表格 | 包含：套件名、用例数、通过/失败数、设备SN、Bundle Name |
| Shell命令执行链判定表格 | 4阶段判定：bm install → aa test → Collected count → [Listener] |
| 执行状态判定结论 | ✅ 测试正常执行 或 ❌ 测试未执行 |
| ❌ 时间窗提取 | 不应在"一"中展示，已下放至"三" |

### 二章节检查

| 检查项 | 要求 |
|--------|------|
| 失败用例列表 | 表格形式：序号、用例名称、结果、执行时长 |
| 失败详情 | 表格形式：用例名、失败信息、问题类型 |
| 问题类型分组统计 | 可选，按问题类型统计失败用例数 |

### 三章节检查

| 检查项 | 要求 |
|--------|------|
| 展示所有失败用例 | ❌ 不要遗漏失败用例（除非同根因已标记） |
| 基本信息 | 包含：所在日志（hilog） |
| 时间窗提取 | 包含：所在日志文件、起始/结束时间、起始/结束行号 |
| ⚠️ **源码→领域证据链** | **独立段落**，包含：证据链表格 + 证据链追溯图 |
| 关键日志片段 | 带行号 |
| 源码定位与分析 | 源码位置、源码片段、源码分析 |
| 问题定界 | 包含：定界依据来源（简要引用数据库查询结果） |
| 同根因用例标记 | 标题追加 `[同根因用例]`，包含根因继承章节 |

### 四章节检查

| 检查项 | 要求 |
|--------|------|
| 问题汇总 | 简洁列表格式 |
| 定界结论表格 | 5个字段：用例名、问题类型、归属子系统、归属领域、流转建议 |
| 建议流转 | 包含：主责任人、问题类型、修复建议、修复示例（可选） |
| 用户确认提示 | 至少3条，更具体，包含详细说明 |

## 报告示例

详见 `/home/xianf/copy/20260703/IMPROVEMENT_PLAN.md`

---

## 常见格式错误示例（基于20260708改进）

> ⚠️ **重要提示**：以下是历史报告中的常见格式错误，AI必须避免重复犯错

### 错误1：一、测试执行概况格式混乱

**错误示例**：
```markdown
## 一、测试执行概况

测试套件ActsAceCArkUI16Test，设备SN FMR0123417000740，Bundle Name com.openharmony.arkui_capi_xts_api16

Shell命令执行链：
- bm install: 成功
- aa test: 成功
- Collected count: 1个套件，39个用例
- [Listener]: 有结果输出
```

**正确做法**：
- ✅ 使用表格呈现测试套件信息（固定9个字段）
- ✅ 使用表格呈现Shell命令执行链判定（固定4阶段）
- ✅ 必须包含结论："测试正常执行，继续进行hilog日志切片分析"

---

### 错误2：二、失败用例清单表格列数不固定

**错误示例**：
```markdown
## 二、失败用例清单

| 用例名 | 问题类型 | 说明 |
|--------|---------|------|
| textAreaLetterSpacing001 | 断言失败 | backgroundColor返回透明色 |
```

**正确做法**：
- ✅ 表格列固定：序号、测试套件、用例名、问题类型、根因分类
- ✅ 同根因用例必须在"根因分类"列标记 `[同根因用例]`
- ✅ 必须包含问题类型分组统计表格

---

### 错误3：三、hilog日志用例详情时间窗提取不规范

**错误示例**：
```markdown
### 用例1：textAreaLetterSpacing001

时间窗：16:25:42 - 16:25:51
```

**正确做法**：
- ✅ 时间窗提取必须有参考文档标签：`> **参考文档**: docs/workflows/time-window-alignment.md`
- ✅ 起始和结束时间必须包含时间戳和行号：`06-26 16:25:42.611 (行6355)`
- ✅ 必须包含用例执行时长

---

### 错误4：三、hilog日志用例详情缺少源码→领域证据链

**错误示例**：
```markdown
### 用例1：textAreaLetterSpacing001

#### 基本信息
...

#### 时间窗提取
...

#### 关键日志
...
```

**正确做法**：
- ✅ 必须包含"源码→领域证据链"独立段落
- ✅ 必须包含证据链表格（API | 子系统 | domain | 日志行 | 时间）
- ✅ 必须包含证据链追溯图

---

### 错误5：关键日志片段缺少来源标记

**错误示例**：
```markdown
#### 关键日志

```
行18098: I A03D00/JSAPP: [textAreaLetterSpacing001] component obj3 is: ...
行18099: I A03D00/JSAPP: [textAreaLetterSpacing001] content is: "#00000000"
```
```

**正确做法**：
- ✅ 必须标注所在日志文件和行号范围：`**所在日志**: hilog.107.20260626-162511.txt（行18098-18117）`
- ✅ 每行日志前必须标注 `[主]`（主分析集）或 `[备]`（备用集）
- ✅ 突出显示失败关键字（如 `[Hypium][fail]`）

---

### 错误6：同根因用例展示过于简单

**错误示例**：
```markdown
### 用例2：TestTextPickerColumnWidths002 [同根因用例]
```

**正确做法**：
- ✅ 标题必须追加 `[同根因用例]` 标签
- ✅ 正文必须简要说明与哪个用例同根因，以及具体原因
- ✅ 如有差异点，必须说明差异

---

### 错误7：四、总结用户确认提示不够具体

**错误示例**：
```markdown
### 用户确认提示

请确认以下问题：
1. 是否需要验证环境配置？
2. 是否需要流转至责任人？
3. 是否需要进一步分析？
```

**正确做法**：
- ✅ 用户确认提示必须具体，列出需要确认的事项清单
- ✅ 每个确认事项必须包含详细说明（如具体问题、预期值、实际值等）
- ✅ 至少包含3条确认事项

---

### 错误8：domain映射AI自行推断

**错误示例**：
```markdown
#### 源码→领域证据链

根据源码推断：inspector.getInspectorByKey 属于 ArkUI子系统，domain 为 A03D00。
```

**正确做法**：
- ✅ domain映射必须使用 `scripts/map_domain.py` 查询
- ✅ 必须明确区分被测方domain vs 测试运行时domain
- ✅ 必须展示脚本查询结果

---

## 格式检查清单（基于20260708改进）

### AI生成报告后自检

| 检查项 | 要求 | 是否符合 |
|--------|------|---------|
| 报告标题 | 固定格式："# XTS测试问题分析报告" | ✅/❌ |
| 一、测试套件信息表格 | 固定9个字段，表格形式 | ✅/❌ |
| 一、Shell命令执行链表格 | 固定4阶段，表格形式 | ✅/❌ |
| 一、结论 | 固定格式："测试正常执行，继续进行hilog日志切片分析" | ✅/❌ |
| 二、失败用例列表表格 | 固定5个字段，表格形式 | ✅/❌ |
| 二、同根因用例标记 | 必须在"根因分类"列标记 `[同根因用例]` | ✅/❌ |
| 二、问题类型分组统计 | 固定3个字段，表格形式 | ✅/❌ |
| 三、基本信息 | 固定5个字段，表格形式 | ✅/❌ |
| 三、时间窗提取 | 必须包含参考文档标签、时间戳+行号 | ✅/❌ |
| 三、源码→领域证据链 | 必须包含证据链表格和追溯图 | ✅/❌ |
| 三、关键日志 | 必须标注所在日志文件和行号范围 | ✅/❌ |
| 三、源码分析 | 必须包含源码位置、片段、测试逻辑 | ✅/❌ |
| 三、问题定界 | 必须使用表格呈现定界依据 | ✅/❌ |
| 三、同根因用例展示 | 必须简要说明同根因原因 | ✅/❌ |
| 四、问题汇总表格 | 固定3个字段，表格形式 | ✅/❌ |
| 四、定界结论表格 | 固定4个字段，表格形式 | ✅/❌ |
| 四、建议流转 | 必须列出具体子系统 | ✅/❌ |
| 四、用户确认提示 | 至少3条具体确认事项 | ✅/❌ |

---

**更新时间**：2026-07-08  
**文档来源**：基于 SKILL_IMPROVEMENT_PLAN.md 改进  
**适用场景**：生成符合新规范的 XTS 分析报告  
**改进要点**：报告格式固定模板、格式检查清单、常见格式错误示例
---

## 常见错误清单（禁止）

### ⚠️ 格式错误（高频问题）

| 错误类型 | 错误示例 | 正确做法 |
|----------|----------|----------|
| 用例格式不一致 | 第1个用例完整，第2-8个用例简化 | **所有用例必须相同格式**，每个用例包含6个标准段落 |
| 源码→领域证据链未独立 | 混在源码分析段落里，缺少表格或追溯图 | **独立成节**（3.X.3），必须包含：表格（API \| 子系统 \| domain \| 日志行 \| 时间）+ 证据链追溯图 |
| 缺少行号时间窗 | 时间窗提取只写时间，不写行号 | 必须包含：所在日志文件、起始行号、结束行号（从grep -n提取） |
| 缺少关键日志片段 | 没有摘录日志，或摘录不带行号 | 必须摘录关键日志片段，格式：`行[行号]: [日志内容]` |
| 问题定界未独立 | 问题定界混在其他段落里，或没有表格 | 问题定界必须是独立表格（3.X.6），包含：问题类型、影响范围、定界依据、归属判定 |
| 基本信息缺少字段 | 基本信息表缺少"所在日志（hilog）" | 基本信息表必须包含：用例名称、测试套件、执行序号、执行结果、消耗时间、**所在日志（hilog）** |

### ⚠️ 内容错误（定界错误）

| 错误类型 | 错误示例 | 正确做法 |
|----------|----------|----------|
| A03D00误判为被测方 | 把测试运行时当成子系统问题 | A03D00/JSAPP是测试运行时（非被测方），不要在证据链中作为子系统 |
| domain归属猜测 | 未用map_domain.py验证，AI自行推断domain归属 | 必须经`map_domain.py`脚本验证，禁止AI猜测 |
| 证据链缺失 | 没有"源码→领域证据链"段落 | **强制要求**：每个用例必须有证据链段落，建立API→子系统→domain→日志行的完整链路 |
| 同根因未标记 | 第3-8个用例与第1个根因相同，但没有标记 | 标题追加 `[同根因用例]`，包含"根因继承"章节 |

### ⚠️ 检查方法

生成报告后，按以下清单逐项检查：

**三章节检查（每个用例）**：
- [ ] 基本信息：包含"所在日志（hilog）"
- [ ] 时间窗提取：包含"起始行号"、"结束行号"
- [ ] 源码→领域证据链：独立成节（3.X.3），包含表格+追溯图
- [ ] 关键日志片段：带行号摘录
- [ ] 源码定位与分析：包含源码位置、片段、分析
- [ ] 问题定界：独立表格

**格式一致性检查**：
- [ ] 所有失败用例格式一致（同根因用例除外）
- [ ] 同根因用例已标记 `[同根因用例]`

**domain归属检查**：
- [ ] 证据链中的domain已经过`map_domain.py`验证
- [ ] A03D00/JSAPP未作为被测方domain

---

**新增时间**：2026-07-09  
**新增内容**：常见错误清单（禁止）  
**新增原因**：避免AI简化第2-8个用例格式，强化格式规范理解  
