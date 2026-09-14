# ohos-issue-lite-diagnose evals

5 个评估用例，判据来自真实交付件数据（SR-09 自验证说明 + iter09 diagnosis.md 227 行报告 + iter07 HUKS/良性报错实战），非编造。

> **2026-08-27 C-6 修订**：全部用例 prompt 已去内嵌脚手架——原 0x81 用例内嵌"软件 CRC 通过/NDA 查不到/位域分解"等答案线索、良性报错用例预消化判据标注（"每次 retry 成功"）、版本标记用例含 `/etc/rootfs_version` 专有名词，均已移除/改为原始日志与中性事实；expectations 同步改为验证真实能力（术语/缺口/实践泛化，不点名 skill 专有实现）。判据来源（source_example）不变。重跑记录见 `evals-reports/{with,without}/ohos-issue-lite-diagnose.md` 的重跑小节。

## 用例覆盖

| id | 场景 | 验证的核心能力 | 真实来源 |
|----|------|--------------|---------|
| `boot_0x81_structured_diagnosis_discipline` | 0x81 启动失败单点诊断（嵌入真实寄存器值） | 结构化报告 / 多假设每条标状态 / 根因不轻断 / NDA 查不死磕转标准产物对比 | iter09 `diagnosis.md`：7 假设 H1-H7 + 3 修复方案 + P1-P7 |
| `unconfirmed_root_cause_labeling_discipline` | 根因未确证时的标注纪律 | 证据不足不下"确认根因"，只标"假设/待验证" | iter07 教训（dont-claim-rootcause-before-verification） |
| `compile_error_c11_atomic_musl_gcc_incompatibility` | 编译错误诊断（musl `__c11_atomic` vs GCC 不兼容） | 编译错误分类 + 兼容性根因方向 + 映射/版本对齐修复 | skill 故障知识库 arm-gcc 兼容性类 |
| `benign_error_triage_not_all_logs_are_faults` | 良性报错判别 | 4 条良性判据逐条核对 + 判良性后交用户决定 | 实测：EACCES/-32 spam，XTS 426/426 → 判良性（OH005） |
| `stale_log_version_mismatch_guard` | 日志与烧录件版本对不上 | 拿日志先核对版本标记，不分析旧版日志 | iter07 教训（huksfix14 版本标记实证） |

## 评估方法

**with skill**：把 `prompt` 发给装了本 skill 的 agent（自然语言触发，不给 skill 名），对照 `expectations[]` 逐条判定。全部用例的 expectations 全过 = with skill 评估通过。

**without skill（基线）**：同样的 `prompt` 发给不带本 skill 的 agent。预期基线在以下断言上显著弱于 with skill：

- `boot_0x81`：基线倾向单假设直奔（"就是 CRC 错了"）或直接下"确认根因"；假设无状态标注、无验证手段
- `unconfirmed_root_cause`：基线常顺着用户说法补强结论（"对，就是没注册"）
- `benign_error`：基线两个极端——要么每条报错都当 bug 死磕，要么"有报错但能跑就不管"，无 4 条判据逐条核对
- `stale_log`：基线常直接开始分析日志内容

**通过判据**：每条 expectation 是布尔断言，人工或 LLM-judge 判定；用例通过 = 全部 expectations 命中。

## 期望的基线差异（with vs without 关键差异预测）

1. **假设纪律**：with skill 每条假设标状态 + 验证手段；基线假设裸奔
2. **根因表述**：with skill 未实测前一律"未确证"；基线常提前"确认"
3. **良性判别**：with skill 4 条判据逐条 + 用户决定；基线拍脑袋
4. **版本核对**：with skill 先核对标记再分析；基线直接钻日志
