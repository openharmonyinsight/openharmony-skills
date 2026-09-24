# ohos-dev-driver-review evals

5 个评估用例，判据全部来自真实交付数据（SR-08 代码审查与优化器 自验证说明 + iter09 深审 34 条发现（8C/10H/9M/7L）+ hal_token.c / hal_sys_param.c 真实源码）与 SKILL.md 真实规则（SEC-001/002/003/004、FUNC-002/005、L0/L1 规则适用性筛选），非编造。

## 用例覆盖

| id | 场景 | 验证的核心能力 | 真实来源 |
|----|------|--------------|---------|
| `sec004_mutex_unlock_without_lock` | 互斥锁加锁失败仍 unlock + 返回 OK | SEC-004 检出 + CRITICAL 定级 + Before/After 修复 | SR-08 iter09 深审判例 C-1（hal_token.c:181-205，代码与源码逐字一致） |
| `severity_calibration_three_tiers` | 三段代码三个档位定级 | 严重度校准（不偏严不偏松） | iter09 深审校准判例：C-5 泄漏应 HIGH / H-4 close 应 MEDIUM / C-6 硬编码密钥保持 CRITICAL |
| `fix_suggestion_before_after` | 无符号下溢越界写 | 每条问题带可用修复代码（不只说"需修复"） | iter09 判例 C-3（TOKEN_WITH_FLAG_SIZE - len 下溢，hal_token.c:315/337/359/385/401） |
| `l1_rule_filtering_no_false_positive` | L1 代码的规则适用性筛选 | L0/L1 自动判定 + Cortex-M 规则零误报 | SR-08 TC-08-02 实测：pthread/POSIX 特征自动判 L1，排除 FUNC-002/SEC-003/SEC-002 严格 |
| `isr_safety_violation_l0` | L0 ISR 安全违规（阻塞 API/printf/大局部/动态内存） | MCU 专项检查 | SKILL.md Step 4 真实规则（SEC-003 ISR 无阻塞 / SEC-002 局部 < 256B / 禁 malloc） |

## 评估方法

**with skill**：把 `prompt` 发给装了本 skill 的 agent（自然语言触发，不给 skill 名），对照 `expectations[]` 逐条布尔判定。全部用例 expectations 全过 = 通过。

**without skill（基线）**：同一 `prompt` 发给不带本 skill 的 agent，对照同一 `expectations[]`。预期基线弱项：
- 加锁失败静默返回 OK 的"静默成功"模式（基线常只报 unlock UB 不报返回值语义，或整体漏报）
- 严重度校准（基线常把失败路径泄漏定 CRITICAL、把 close 忽略定 HIGH——偏严）
- L1 上误报 Cortex-M 规则（基线常不分 L0/L1 一把梭）
- ISR 专项的 256B 局部变量/禁 malloc 检查（基线常只报阻塞调用）
- 规则 ID 引用与 Before/After 修复格式（基线常给散文式意见）

**通过判据**：每条 expectation 是布尔断言，人工或 LLM-judge 判定；用例通过 = 全部 expectations 命中。
