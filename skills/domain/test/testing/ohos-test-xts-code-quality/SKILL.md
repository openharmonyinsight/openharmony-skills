---
name: ohos-test-xts-code-quality
description: "检查OpenHarmony XTS测试代码质量，审查PR测试代码，检测编码规范违规、异步安全问题与资源泄漏。当用户提到XTS测试代码质量检查、PR测试代码审查、编码规范检查、异步安全、资源泄漏、getSync接口检查、错误码断言、testcase命名、testsuite重复、p7b签名、HAP命名、用例重复时使用。支持本地代码扫描与GitCode PR审查两种模式，扫描29条内置规则（R001-R023, R201-R206），输出HTML/Excel报告并可自动提交PR评论。"
metadata:
  author: openharmony
  scope: domain
  stage: testing
  domain: xts
  capability: code-quality
  version: 2.0.13
  status: stable
  tags:
    - xts
    - code-quality
    - code-review
    - testing
  related-skills:
    - check-test-code-quality
    - ohos-test-ut-generation
    - ohos-test-arkts-xts-generation
---

# XTS测试代码质量检查

文件级并行引擎，扫描29条内置规则。

> **路径约定**: `{SKILL_DIR}` = Skill目录绝对路径，`{SCAN_PATH}` = 用户指定扫描路径

## 执行步骤

### 步骤1: 判断扫描模式

```bash
# 本地扫描（默认）
python {SKILL_DIR}/scripts/main.py {SCAN_PATH} --level all

# PR扫描
python {SKILL_DIR}/scripts/main.py --pr <PR_URL> --token <TOKEN> --level all
```

### 步骤2: 执行内置规则扫描

内置29条规则（R001-R023, R201-R206）由Python脚本自动执行。

**输出位置**: `{SCAN_PATH}/.xts_scan/`
- `XTS_代码质量检查报告.html` - HTML可视化报告（推荐）
- `XTS_代码质量检查报告.xlsx` - Excel报告
- `scan_meta.json` - 扫描元数据
- `all_issues.json` - 问题明细

### 步骤3: PR模式去重与提交

PR模式自动：
- 获取diff上下文，过滤非变更行问题
- 获取已有评论，去重已报告问题
- `--submit` 自动提交扫描结果为PR评论

**PR评论格式**：
```markdown
## XTS 代码质量扫描报告

### 扫描统计
| 严重级别 | 问题数量 |
| Critical | N |
| Warning | M |

### 问题规则统计
| 规则编号 | 问题数量 | 可自动修复 |

### 问题示例（每规则一个案例）
**R205** `file:line` 问题类型 `[可自动修复: Yes]`
```
代码片段
```
> 修复建议
> 可使用 `--fix` 自动修复或参考修复指南
```

## 风险边界

### PR模式局限

- **仅扫描变更文件**: 工程级规则（R011/R019/R020）可能漏检
- **建议**: 对工程级规则使用完整checkout扫描，或明确声明结论不完整

## 参数速览

| 参数 | 说明 |
|------|------|
| `--level` | critical/warning/all（默认all） |
| `--rules` | 指定内置规则ID（如 R001,R003,R201） |
| `--category` | compliance/async_safety/resource_management/test_design |
| `--parallel` | 并行线程数（默认自动） |
| `--sta-mode` | all/dyn/sta（默认all自动检测；dyn仅扫Dyn工程，sta仅扫Sta工程） |
| `--fix` | 自动修复（支持R008,R011,R012,R014,R016,R018） |
| `--pr` | GitCode PR URL |
| `--token` | GitCode PAT |
| `--submit` | 提交扫描结果为PR评论 |
| `--no-diff` | 跳过diff上下文获取 |
| `--no-comments` | 跳过已有评论获取 |

---

## R012修复特殊说明

> R012（签名证书APL等级错误）修复需使用签名工具重新生成p7b文件，详见修复指南

### 前置要求

- GitCode Personal Access Token（PAT）
- Java 8+ 环境
- git 命令行工具

### 工具路径

签名工具下载后存放于：`{SKILL_DIR}/guides/R012_p7b_signature/signature_tools/`

### 修复指南

完整修复流程（工具下载、签名配置、批量修复）见：
- **主指南**: [guides/R012_p7b_signature/R012_FIX_GUIDE.md](guides/R012_p7b_signature/R012_FIX_GUIDE.md)
- **脚本设计**: [guides/R012_p7b_signature/R012_FIX_SCRIPT_DESIGN.md](guides/R012_p7b_signature/R012_FIX_SCRIPT_DESIGN.md)
- **特殊场景**: [guides/R012_p7b_signature/R012_UNKNOWN_PERMISSION_GUIDE.md](guides/R012_p7b_signature/R012_UNKNOWN_PERMISSION_GUIDE.md)

## 规则速览

| 规则 | 类型 | Sta适用 | 一句话描述 |
|------|------|---------|-----------|
| R001 | Critical | ✅ | 禁止getSync系统接口 |
| R002 | Critical | ❌ Sta不适用 | 错误码断言必须是number类型 |
| R003 | Critical | ✅ | 禁止恒真断言 |
| R004 | Critical | ✅ | 测试用例缺少断言 |
| R201 | Critical | ✅ Sta特化 | 异步用例缺少done |
| R202 | Critical | ✅ Sta特化 | Promise缺少catch |
| R204 | Critical | ✅ | 资源创建后未释放 |
| R206 | Warning | ✅ Sta特化 | 用例间隐式依赖 |
| R022 | Critical | ❌ Sta不适用 | errcode宽松比较 |

> **编码规范合规（R001-R023）**: [references/RULES_COMPLIANCE.md](references/RULES_COMPLIANCE.md)
> **测试技术问题（R201-R206）**: [references/RULES_TECHNICAL.md](references/RULES_TECHNICAL.md)

---

## NEVER 清单

> **严格执行以下禁止模式，避免误判和风险遗漏**

### 扫描结论表述

- **NEVER** 把"脚本返回0问题"表述为"代码无风险"
- **NEVER** 在未读取 `references/TRAPS.md` 的情况下裁定复杂规则误报/漏报

### PR模式边界

- **NEVER** 在只拉取PR变更文件时宣称工程级重复检测（R011/R019/R020）完整
- **NEVER** 对PR模式漏检的工程级问题给出"已全部检出"结论
- **注意**: R018（testcase重复）仅检测同一describe块内，不受PR模式影响

### 文档引用

- **NEVER** 一次性加载全部references文档（按需加载：解释编码规范读RULES_COMPLIANCE.md，解释测试技术读RULES_TECHNICAL.md，判断误报读TRAPS.md，PR排障读pr_scanner_usage.md）

---

## 评估用例（evals）

随包提供覆盖全部 30 条规则的评估用例集，用于验证 Skill 的检出能力与误报抑制：

| 文档 | 加载时机 |
|------|---------|
| [evals/evals.json](evals/evals.json) | 复跑评估或新增 eval 用例时 |
| [evals/test_cases/subsystem_demo/](evals/test_cases/subsystem_demo/) | 评估输入夹具（11 个文件，覆盖 .ts/.ets/.json/.gn/.json5/.p7b 多类型） |

复跑方式：

```bash
# with_skill（扫描器）
python {SKILL_DIR}/scripts/main.py {SKILL_DIR}/evals/test_cases/subsystem_demo --level all

# without_skill：在未加载本 Skill 的环境中，对 evals.json 中各 prompt 用 LLM 执行同一任务
```

## 参考文档

| 文档 | 加载时机 |
|------|---------|
| [references/RULES_COMPLIANCE.md](references/RULES_COMPLIANCE.md) | 解释编码规范规则（R001-R023）时 |
| [references/RULES_TECHNICAL.md](references/RULES_TECHNICAL.md) | 解释测试技术规则（R201-R206）时 |
| [references/TRAPS.md](references/TRAPS.md) | 判断误报/漏报时 |
| [references/subsystem_mapping.md](references/subsystem_mapping.md) | 子系统映射数据源 |
| [references/pr_scanner_usage.md](references/pr_scanner_usage.md) | PR模式排障时 |
| [guides/FIX_GUIDE.md](guides/FIX_GUIDE.md) | 执行自动修复时 |

---

## 维护说明

### 子系统映射同步

修改 `references/subsystem_mapping.md` 后，需执行同步脚本：

```bash
# 检查差异
python {SKILL_DIR}/scripts/sync_subsystem_mapping.py --check

# 执行同步
python {SKILL_DIR}/scripts/sync_subsystem_mapping.py --update
```

> **版本**: 2.0.13 | 更新日期: 2026-07-29 | 配置文件: skill_config.json