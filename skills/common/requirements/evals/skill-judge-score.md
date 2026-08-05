# Skill Judge Score - OHOS Requirements Skills

评审版本：`feat/restructure-ohos-req-skills`，R4 修复后。

## 总分

| 指标 | 结果 |
|------|------|
| 总分 | 110 / 120 |
| 等级 | A |
| Eval cases | 48 |
| Assertions | 155 |
| Programmatic assertions | 111 |
| Manual assertions | 44 |
| Unsupported assertions | 0 |

## D1-D8 明细

| 维度 | 得分 | 扣分依据 |
|------|------|----------|
| D1 触发与适用边界 | 14 / 15 | 7 个 skill frontmatter 均有明确 trigger/Do NOT use；PPT 可选依赖触发边界仍依赖用户显式请求。 |
| D2 指令清晰度 | 14 / 15 | 主流程已改为对外 5 个产物阶段、内部 checkpoint；仍保留少量 Step 编号用于机器路由。 |
| D3 产物契约 | 14 / 15 | 01/02/03/04/proposal/value-decision 均有模板和输出字段；ODK handoff 已定义，但实际转换器由下游实现。 |
| D4 Gate 与错误处理 | 14 / 15 | Review Ready Gate、GA 证据、Not Ready 硬阻断、rollback 路由已补齐；跨系统 GA 证据可达性需在集成环境验证。 |
| D5 Eval 覆盖 | 14 / 15 | 48 cases、155 assertions，覆盖 Gate/ODK/runner/安装一致性；with-skill/baseline 自动执行仍需外部 judge。 |
| D6 工具与安装一致性 | 13 / 15 | install/probe/source-target/semver/全树引用检查已覆盖；仍为 shell 实现，复杂 schema 校验能力有限。 |
| D7 用户体验 | 14 / 15 | 用户提示改为阶段名，减少 Step 噪音；少数恢复/调试信息仍保留 target_step。 |
| D8 可维护性 | 13 / 15 | README、eval runner、consistency tests、score report 已对齐；评分仍需人工复核维护。 |

## 证据

- `README.md`：对外 5 个产物阶段、评分摘要、验证命令。
- `ohos-req-intake-orchestration/SKILL.md`：内部 checkpoint、用户提示阶段名、预检变量。
- `ohos-req-feature-proposal-baseline/SKILL.md`：Gate 输出契约、GA 证据、ODK handoff、IR/SR/handoff 兼容边界。
- `ohos-req-value-decision/SKILL.md`：Gate=Not Ready 硬阻断 Accepted。
- `evals/run_skill_evals.py`：严格 assertion schema。
- `evals/tests/test_run_skill_evals.py`：真实 eval schema、regex pattern、not_contains tokens 回归测试。
