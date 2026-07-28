# Skill 测试用例 (Evals)

## 概述

本目录包含 ohos-design-test-coordinator 和 ohos-design-test-demo-pipeline 两个 skill 的测试用例，用于评估 skill 的能力增量。

每个测试用例包含：
- **prompt**：输入提示词（with skill 和 without skill 两种模式使用相同 prompt）
- **files**：输入夹具文件（fixture），运行前 stage 到输出目录供 skill 读取
- **assertions**：断言点，检查输出产物是否满足 skill 定义的结构/规范

## 目录结构

```
evals/
├── evals.json              # 测试用例定义（coordinator 4个 + 共用 runner 配置）
├── eval_runner.py          # 通用对比运行器
├── README.md               # 本文件
└── fixtures/               # 输入夹具文件
    ├── requirement_appclone.md           # coordinator Phase1 输入
    ├── requirement_analysis_appclone.md  # coordinator Phase2 输入
    └── test_point_design_appclone.md     # coordinator Phase4 输入

# demo-pipeline 的测试用例在独立目录：
ohos-design-test-demo-pipeline/evals/
├── evals.json
└── fixtures/
    ├── demo_test_points_preference.md    # demo Phase1 输入
    └── demo_design_preference.md         # demo Phase2 输入
```

## 测试用例

### ohos-design-test-coordinator (4 个用例)

| ID | 名称 | 输入 | 输出 | 断言数 |
|----|------|------|------|--------|
| 1 | phase1-ibo-requirement-analysis | requirement_appclone.md | requirement_analysis.md + knowledge_match.md | 12 |
| 2 | phase2-testpoint-generation | requirement_analysis_appclone.md | test_point_design.md | 9 |
| 3 | phase4-testcase-refinement | test_point_design_appclone.md | test_cases.md | 9 |
| 4 | phase1-inner-api-filter | requirement_appclone.md | requirement_analysis.md | 7 |

### ohos-design-test-demo-pipeline (4 个用例)

| ID | 名称 | 输入 | 输出 | 断言数 |
|----|------|------|------|--------|
| 1 | phase1-ui-design | demo_test_points_preference.md | demo_design.md | 10 |
| 2 | phase2-code-generation | demo_design_preference.md | TestDemo/ + demo_code_manifest.md | 8 |
| 3 | phase2-arkts-never-rules | demo_design_preference.md | TestDemo/*.ets | 7 |
| 4 | phase2-template-integrity | demo_design_preference.md | TestDemo/ | 8 |

## 执行方法

### 核心理念

对每个用例执行两次，对比断言通过数差值：

1. **With skill（提示词 + skill）**：在 opencode 中加载对应 skill，输入 prompt，产物输出到 `output_with/`
2. **Without skill（纯提示词）**：在普通 LLM 对话中输入相同 prompt（不加载 skill），产物输出到 `output_without/`

运行器对比两个结果目录的断言通过数，差值即为 skill 的增量价值。

### 步骤 1：Stage 夹具文件

将测试用例的输入文件复制到输出目录：

```bash
# coordinator 用例
python eval_runner.py stage \
  --evals ohos-design-test-coordinator/evals/evals.json \
  --output-dir ./output_with \
  --eval-id 1

# demo-pipeline 用例
python eval_runner.py stage \
  --evals ohos-design-test-demo-pipeline/evals/evals.json \
  --output-dir ./output_with \
  --eval-id 1
```

### 步骤 2：执行 With skill 模式

在 opencode 中加载 skill，输入 evals.json 中的 prompt，将产物输出到 `output_with/` 目录。

### 步骤 3：执行 Without skill 模式

在普通 LLM 对话（不加载 skill）中输入相同 prompt，将产物输出到 `output_without/` 目录。

### 步骤 4：运行对比

```bash
python eval_runner.py compare \
  --evals ohos-design-test-coordinator/evals/evals.json \
  --with-skill-dir ./output_with \
  --without-skill-dir ./output_without \
  --output comparison_report.json
```

输出示例：
```
  Eval  Name                                      With    Without Delta
  --------------------------------------------------------------
  1     phase1-ibo-requirement-analysis          10/12   3/12    +7
  2     phase2-testpoint-generation              7/9     2/9     +5
  ...
  TOTAL                                        34/38   12/38   +22

  Skill incremental value: 22 additional assertions passed with skill.
```

### 单模式评估

仅评估一个输出目录（不对比）：

```bash
python eval_runner.py evaluate \
  --evals ohos-design-test-coordinator/evals/evals.json \
  --output-dir ./output_with \
  --eval-id 1
```

## 断言类型

| 类型 | 说明 |
|------|------|
| file_exists | 目标文件存在（支持通配符） |
| file_contains | 目标文件包含 pattern（match_mode: any/all） |
| file_not_contains | 目标文件不含 pattern（match_mode: all） |
| dir_contains | 目录下存在匹配文件（min_count） |
| script_exit_code | 执行命令退出码等于 expected |

## 占位符

| 占位符 | 说明 |
|--------|------|
| {skill_root} | skill 根目录绝对路径 |
| {output_dir} | 测试产物输出目录 |
| {fixtures_dir} | 夹具文件目录（evals/fixtures/） |
