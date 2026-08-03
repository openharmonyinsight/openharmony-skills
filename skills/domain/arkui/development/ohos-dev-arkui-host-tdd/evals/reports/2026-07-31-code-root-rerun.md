# Host TDD eval rerun — 2026-07-31

## Result

Host workspace：`/srv/workspace/openharmony_master_default_20260713175555_huawei_b8da041e5/code`

| Suite | Arm | Expectations | Cases | Conclusion |
|---|---|---:|---:|---|
| Hermetic | with-skill | **48/54** | **5/8** | 比 baseline 多 15 条、5 个 case |
| Hermetic | isolated baseline | **33/54** | **0/8** | — |
| Integration | with-skill | **5/5** | **1/1** | PASS |
| Integration | isolated baseline | **5/5** | **1/1** | `no demonstrated gain` |

不能声称 `9/9`；hermetic 与 integration 必须分开报告。

## Case details

FAIL 列为未通过的 expectation 序号，其余均通过。Exact text 和 evidence 见 grading JSON。

| Suite | Case | With | FAIL | Baseline | FAIL | Grading |
|---|---:|---:|---|---:|---|---|
| Hermetic | 0 | 6/6 | — | 3/6 | 2,3,4 | [W](artifacts/2026-07-31-code-root-rerun/grading/with-0.json) / [B](artifacts/2026-07-31-code-root-rerun/grading/baseline-0.json) |
| Hermetic | 2 | 4/6 | 2,4 | 3/6 | 1,2,4 | [W](artifacts/2026-07-31-code-root-rerun/grading/with-2.json) / [B](artifacts/2026-07-31-code-root-rerun/grading/baseline-2.json) |
| Hermetic | 3 | 5/7 | 4,6 | 4/7 | 4,5,6 | [W](artifacts/2026-07-31-code-root-rerun/grading/with-3.json) / [B](artifacts/2026-07-31-code-root-rerun/grading/baseline-3.json) |
| Hermetic | 4 | 6/6 | — | 5/6 | 2 | [W](artifacts/2026-07-31-code-root-rerun/grading/with-4.json) / [B](artifacts/2026-07-31-code-root-rerun/grading/baseline-4.json) |
| Hermetic | 5 | 6/6 | — | 4/6 | 3,6 | [W](artifacts/2026-07-31-code-root-rerun/grading/with-5.json) / [B](artifacts/2026-07-31-code-root-rerun/grading/baseline-5.json) |
| Hermetic | 6 | 6/6 | — | 5/6 | 5 | [W](artifacts/2026-07-31-code-root-rerun/grading/with-6.json) / [B](artifacts/2026-07-31-code-root-rerun/grading/baseline-6.json) |
| Hermetic | 7 | 6/8 | 6,7 | 6/8 | 5,6 | [W](artifacts/2026-07-31-code-root-rerun/grading/with-7.json) / [B](artifacts/2026-07-31-code-root-rerun/grading/baseline-7.json) |
| Hermetic | 8 | 9/9 | — | 3/9 | 1,2,3,5,6,8 | [W](artifacts/2026-07-31-code-root-rerun/grading/with-8.json) / [B](artifacts/2026-07-31-code-root-rerun/grading/baseline-8.json) |
| Integration | 1 | 5/5 | — | 5/5 | — | [W](artifacts/2026-07-31-code-root-rerun/grading/with-1.json) / [B](artifacts/2026-07-31-code-root-rerun/grading/baseline-1.json) |

With-skill 的主要缺口：case 2 未完整区分 `--filter`/`--gtest_filter` 和核对双产物；case 3
未完整说明 GN generation 与 `OK` 的证据边界；case 7 未完整分离 stale 风险和 crash diagnosis。

## Integration evidence

- ace_engine revision：`3d648d632141678368bde7a0376cf80f67f6e3e4`，工作树干净。
- Build：`host_product/ace_engine_test`，exit `0`，matching Build ID
  `a7f8cc89dcded8ca02c7d51fb21f54d7`。
- 两臂都精确运行 `DrawableDescriptorTest.AnimatedDrawableDescTest044`，各执行 1、通过 1、
  失败 0，并生成独立 XML。

| Arm | Output | Manifest / XML |
|---|---|---|
| with-skill | [answer](artifacts/2026-07-31-code-root-rerun/audited/with-integration/with-1.txt) | [manifest](artifacts/2026-07-31-code-root-rerun/audited/with-integration/environment.json) / [XML](artifacts/2026-07-31-code-root-rerun/audited/with-integration/integration-case-1.xml) |
| baseline | [answer](artifacts/2026-07-31-code-root-rerun/audited/baseline-integration/baseline-1.txt) | [manifest](artifacts/2026-07-31-code-root-rerun/audited/baseline-integration/environment.json) / [XML](artifacts/2026-07-31-code-root-rerun/audited/baseline-integration/integration-case-1.xml) |

## Provenance and retained evidence

- [run provenance](artifacts/2026-07-31-code-root-rerun/run-provenance.json)
- [baseline isolation](artifacts/2026-07-31-code-root-rerun/baseline-isolation.json)
- `audited/`：18 份最终回答、2 份 manifest、2 份 XML。
- `grading/`：18 份逐 expectation grading JSON。

Prompt、逐运行 metadata、命令日志、完整 transcript 和 grader scratch 均为可再生成的中间产物，
不入库。必要的 prompt/output/command-audit hash 与动作摘要已合并到 run provenance。

## Limits

这是已知故障模式的 regression eval，不是 held-out benchmark。Eval 与 grader 使用同一模型，单次
分数存在波动；integration 只证明该 pinned revision、留存产物和一个精确 gtest case。
