# User Guide Skill Evals

本目录提供 `skills/common/requirements` 下 requirements skills 的本地评测辅助工具。

## 评测模型

采用 Anthropic skill-creator 的 eval 结构：

1. 每个 skill 在 `evals/evals.json` 或 `evals/cases.yaml` 中维护真实任务 prompt。
2. 评测执行者分别运行 with-skill 和 baseline，把输出保存到 workspace。
3. `run_skill_evals.py grade` 对保存的文本输出执行可程序化断言。
4. `llm_judge` 类型断言标记为 manual，交由人工或外部 LLM judge 复核。
5. `run_skill_evals.py collect` 聚合全量用例覆盖，生成 benchmark 摘要。

## 生成覆盖率 benchmark

```bash
python3 skills/common/requirements/evals/run_skill_evals.py collect \
  --root skills/common/requirements \
  --benchmark-json /tmp/user-guide-skill-benchmark.json \
  --benchmark-md /tmp/user-guide-skill-benchmark.md
```

## 评分单个输出

```bash
python3 skills/common/requirements/evals/run_skill_evals.py grade \
  --evals skills/common/requirements/ohos-req-requirement-intake/evals/evals.json \
  --eval-id 1 \
  --output /tmp/with-skill-output.txt \
  --result /tmp/grading.json
```

`grading.json` 字段遵循 benchmark viewer 友好的结构：`text`、`passed`、`evidence`。
