---
name: using-ohos-sdd
description: Use when starting any OpenHarmony SDD work, or when about to create or modify an OH deliverable (proposal/spec/design/plan/code) — establishes how to find and invoke ohos-sdd capability skills before any other action
license: MIT
---

<SUBAGENT-STOP>
如果你是被派发执行具体任务的子代理,跳过本技能,直接执行分配的任务。
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
只要你有 1% 的可能需要创建/修改 OpenHarmony 交付件(proposal/spec/design/execution-plan/code)或做审查,就必须先按本技能发现并 invoke 对应能力 skill。
</EXTREMELY-IMPORTANT>

# Using OHOS SDD

## 路径约定

本 skill 是 **runtime asset**（随 dist 分发，Agent 执行时读）。文中 `{{ASSET_ROOT}}/*` 是源码占位符，分发时由打包工具替换为实际路径。在**源仓** `openharmony/` 对应：

| `{{ASSET_ROOT}}` 路径 | 源仓对应 |
|---|---|
| `{{ASSET_ROOT}}/workflow/workflow.md` | `openharmony/workflow/workflow.md` |
| `{{ASSET_ROOT}}/profiles/<name>/profile.md` | `openharmony/profiles/<name>/profile.md`（主）/ `openharmony/profiles/<name>/subprofiles/<sub>.md`（子） |

从源仓阅读或改 skill 时以源仓路径为准；Agent 执行（runtime）时 `{{ASSET_ROOT}}` 已被替换为实际路径。

## 指令优先级

1. **用户/项目指令**(`AGENTS.md`/`CLAUDE.md`/直接请求)—— 最高
2. **ohos-sdd 能力 skill** —— 覆盖默认行为
3. **默认系统提示** —— 最低

## 发现规则

OHOS SDD 是**能力分解**(像 superpowers),不是阶段顺序器。每个能力 skill 自描述触发器(`description: Use when…`)。

```
收到 OH 任务 → 读相关能力 skill 的 description → 1% 可能匹配就 invoke → 按 skill 行动
```

能力 skill 清单(按交付件依赖图顺序,详见 `{{ASSET_ROOT}}/workflow/workflow.md`):

| 能力 skill | 触发(简) | owns 交付件 |
|---|---|---|
| ohos-clarify | 范围模糊 | —(横切) |
| ohos-propose | 起草/基线 proposal | proposal/manifest |
| ohos-spec | 写 spec | spec/epic |
| ohos-design | 写 design | design |
| ohos-spec-for-test | Profile 定义的测试输入旁路 | spec_for_test |
| ohos-plan | 写 execution-plan | execution_plan/task |
| ohos-review | 审查合规 | review |
| ohos-validate | 声称完成前 | gate_checklist |
| ohos-security-threat-model | 高风险安全/隐私/合规 | threat-model |

## 依赖骨干

交付件依赖(顺序涌现自此,非阶段 gate):`proposal → spec → design → execution-plan → code`;`evidence/{checks,reviews}` 旁证。完整依赖图 + Level A/B/C/D/E 一致性检查见 `{{ASSET_ROOT}}/workflow/workflow.md`。

## 守门

`ohos-validate` 是**声称完成前必跑**的守门:invoke 它 → `ohos-sdd validate . --level all` → 按 `broken_edges.rework_capability` 回对应能力修复。

## Red Flags(ohos 化 rationalization)

| 念头 | 现实 |
|---|---|
| "先实现再补 spec" | spec 是真相源,先 spec |
| "跳过 design,简单变更" | 标准及以上必须 design |
| "ReadyForReview 当 Approved" | 上游未 Approved 必须停 |
| "AI 自评通过" | 必跑 ohos-validate 取证据 |
| "下次再 validate" | 声称完成前必跑 |

## 平台工具

斜杠命令、hook 注入、skill 调用方式等平台专有配置由插件 manifest 声明（`.claude-plugin/plugin.json` / `.codex-plugin/plugin.json` / `opencode.json`），Agent 可从已安装的插件结构中自行发现。

## Profile 路由(命中声明写回 manifest)

收到 OH 任务且 `manifest.md` 存在时,执行 profile 命中(两维度),把结果写回 manifest:

1. **仓间 → 主 profile**:
   ```bash
   url="$(git remote get-url origin 2>/dev/null || true)"
   repo="$(basename "${url%.git}")"
   ```
   扫 `{{ASSET_ROOT}}/profiles/<name>/profile.md`(或 source `openharmony/profiles/<name>/profile.md`)的 `repos` 字段,仓名命中 → 主 profile。写回 `manifest.profile` + `profile_source: inferred`(owner 已定主类型则保留 `owner`)。
2. **仓内 → 子 profile**:扫本次变更文件路径 → 匹配 `profiles/<profile>/subprofiles/<sub>.md` 的 `applies_to` glob(`applies_to` 是路径 glob 模式,YAML 标量;按其字面值匹配路径,如 `**/components_ng/**`)→ 命中子 profile(可多个)→ 写回 `manifest.subprofiles`(block seq)。
3. **代码特征对账(轻量提示)**:若 manifest 声明的 profile 与 git remote 仓名归属不一致,或路径特征与声明子 profile 不符 → **提示 owner 确认**;**不自动改主类型**(主类型 owner 定)。
4. **兜底**:无 git / 无 remote / monorepo / 推断不出 → manifest.profile 留 owner 填或 `none`;subprofiles 留空。

frontmatter 一律 block seq(`- item`),不用内联数组。命中后,各能力 skill 按 `profile-application` 纪律(profiles/* 按需加载)应用 profile。

## 重内容按需加载

`workflow.md` 依赖图、`profiles/*`、`analysis/*` 是重内容,**按需加载**,不进 session 注入。本元路由只教发现 + 指针。
