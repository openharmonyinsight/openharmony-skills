# ohos-test-lite-adapt-verify evals

7 个评估用例，判据来自 SR-10 交付件自验证的 iter12 端到端真实数据（6 阶段 PROVENANCE、27/27 PASS 回炉链）+ skill 原文的路由/纪律规则（编译失败分类路由、镜像一致性核实为规则补充用例），非编造。

## 用例覆盖

| id | 场景 | 验证的核心能力 | 真实来源 |
|----|------|--------------|---------|
| `six_phase_orchestration_correctness` | 6 阶段编排正确性 | 阶段顺序 + implement↔verify 循环 + 每阶段产物路径 | SR-10 iter12 端到端 6 阶段 PROVENANCE（终点 27/27 PASS） |
| `test_strategy_user_decision_discipline` | 测试策略由用户决定的纪律 | Custom 策略被尊重、不硬编码 XTS、按用户格式采集结果 | init Step 4 / verify 核心原则（五策略可插拔） |
| `fail_classification_and_rollback` | fail 分类路由 | 分类接路由：实现缺陷→implement、环境问题→修环境重跑（不改产品代码）、MAP 恶化→先归因路由（评估有误→implement；改动未生效/链接配置→修构建环节）+ 回炉超 3 次升级 | iter12 实战回炉链（实现缺陷路径）+ R15 环境问题案例 |
| `dual_intent_test_vs_miniaturization` | 双意图判别（测试验证 vs 体积优化） | 路径选择 + 产物区分 + 结果不可互换充当 | 主 SKILL 职责边界表 |
| `test_only_fail_no_implement_route` | test-only 模式测试 Fail 的处理 | 记录失败并报告、不自动进 implement、修源码需用户授权；optimization 才按已批准 tasks 回炉 | 主 SKILL 职责边界 + verify.md 回炉表分流（R4 检视修复） |
| `compile_failure_classification_routing` | 编译失败分类路由 | 源码缺陷→implement；环境/工具链/构建配置→修环境重跑不改产品代码；test-only 报告用户 | 主 SKILL 异常表 + verify.md Step1 分类路由（R16 检视修复） |
| `run_only_image_consistency_gate` | --run-only 镜像一致性核实 | 核实板上镜像即待测产物（时间戳/版本/哈希）；无法核实完整烧录；MAP 参考须同源或标注不可关联 | verify.md 模式块 + Step1 同源说明（R18 检视修复） |

## 评估方法

**with skill**：把 `prompt` 发给装了本 skill 的 agent（自然语言触发，不给 skill 名），对照 `expectations[]` 逐条判定。全部用例的 expectations 全过 = with skill 评估通过。

**without skill（基线）**：同样的 `prompt` 发给不带本 skill 的 agent，对照同一 `expectations[]` 判定。预期基线在以下断言上显著弱于 with skill：
- 6 阶段编排（基线常直接烧板跑测试，跳过量基线/提案/归档）
- 测试策略纪律（基线倾向默认跑 XTS 或替用户选策略）
- 回炉规则（基线常带 Fail 出报告或在原地反复盲改）
- 双意图判别（基线常把"测试通过"直接当"优化完成"）

**通过判据**：每条 expectation 是布尔断言，人工或 LLM-judge 判定；用例通过 = 全部 expectations 命中。

## 期望的基线差异（with vs without 关键差异预测）

1. **编排完整率**：with skill 6 阶段 + 产物路径齐全（xts_test/reports|proposals|lessons）；基线流程自由发挥无固定产物契约
2. **策略纪律**：with skill 问用户并写入 config，按策略分流；基线默认选最常见策略
3. **回溯纪律**：with skill Fail/恶化按模式分类处理（optimization 回 implement、test-only 记录报告不代改用户代码）、超 3 次升级；基线倾向忽略或死磕
4. **产物诚实度**：with skill 测试/优化两类报告分开、MAP 对比按模式（optimization 必做，test-only 仅参考/跳过）；基线常拿单方面结果宣称完成
