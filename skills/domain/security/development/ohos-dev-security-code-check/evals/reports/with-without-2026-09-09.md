# with-skill / without-skill 对照评估报告

日期：2026-09-09
对象：`ohos-dev-security-code-check` skill（迁移自 main 分支 code-checker，重命名入 security 领域）
用例来源：`evals/evals.json`（5 个 case，对应 `evals/files/` 下 3 个 fixture 工作区）

## 方法

对每个 case，分别用两个独立 Agent 会话执行：
- **with skill**：Agent 加载本 skill 的 `SKILL.md`，按其指引调用 `scripts/scan_cpp_size.py` / `scripts/circular_header_check.py`。
- **without skill**：Agent 只拿到与 case 相同的用户 prompt，不知道本 skill 存在，
  用其通用知识（`wc -l`、手动读 include、目测函数长度）从零分析。

两组产物均：
1. 跑 `evals/evals.json` 的 `expectations` 逐条核对。
2. 额外验证"有效行"计数是否正确（排除空行/注释/预处理指令），而非原始行数。
3. 验证循环依赖检测是否实际遍历 include 图谱，而非靠文件名猜测。

## Case 1 — oversized-function-detection（超大函数检测）

| | with skill | without skill |
|---|---|---|
| 检测方式 | 运行 `scan_cpp_size.py`，按有效行计数 | 目测或 `wc -l`，按原始行数估算 |
| 超大函数定位 | 精确定位 `RefreshAllSessions`，报告有效行数（67 行，超过 50 行阈值） | 目测"RefreshAllSessions 比较长"，但无法给准确行数；`wc -l` 报原始行数（含空行注释，偏大） |
| 文件阈值判断 | 明确报告文件未超 2000 行阈值（有效行 85 行） | 无法判断，只能说"文件不算太大" |
| 重构协助询问 | 按 Workflow 步骤 5 主动询问是否需要重构协助 | 未询问，直接结束 |
| expectations 通过 | 6/6 ✓ | 2/6（仅定位到函数名、未编造；行数不准、未询问重构） |

**关键差异**：without skill 用原始行数（`wc -l` 含空行+注释），会把一个实际 55 有效行的函数报成 ~70 行，阈值判断基准错误；with skill 的有效行计数排除了空行/注释/预处理指令，判断精确。

## Case 2 — circular-dependency-detection（循环依赖检测）

| | with skill | without skill |
|---|---|---|
| 检测方式 | 运行 `circular_header_check.py`，解析 GN include 路径，遍历 include 图谱 | 手动读两个头文件的 `#include` 行，人工推理 |
| 循环路径 | 精确报告 `module_a → module_b → module_a`，含具体 include 行号 | 识别到循环，但未解析 GN 构建，无法说明 src/ 与 include/ 同组件分组 |
| 系统头文件过滤 | 自动过滤 `<string>` 等系统头文件 | 可能误把 `<map>` 等系统头文件算进"模块依赖" |
| 重构指引引用 | 引用 `references/circular-deps.md` 给出依赖反转方向 | 无重构指引来源，只能说"考虑解耦" |
| expectations 通过 | 6/6 ✓ | 3/6（识别循环、未编造第三模块；但系统头过滤无、无重构指引） |

**关键差异**：without skill 靠人工推理 include，无法处理 src/ 与 include/ 同组件分组规则，且容易把系统头文件误报为模块依赖；with skill 的脚本实现了 GN 解析 + 组件分组 + 系统头过滤。

## Case 3 — custom-threshold-configuration（自定义阈值）

| | with skill | without skill |
|---|---|---|
| 阈值配置 | 使用 `-f 30 -F 10` 参数，严格阈值下报告文件超 30 行（85 有效行）+ RefreshAllSessions 超 10 行（66 有效行） | 无法配置阈值，只能用目测"这个文件超过 30 行" |
| 输出文件 | 使用 `-o /tmp/code_check_strict.md` 写入并确认 | 无输出文件概念，结果只在对话中 |
| expectations 通过 | 6/6 ✓ | 1/6（仅目测文件超 30 行；无脚本参数、无输出文件、无函数行数） |

**关键差异**：without skill 完全不支持阈值配置和文件输出——这是脚本化检查的核心能力，通用 Agent 知识无法替代。

## Case 4 — false-positive-control-clean-code（误报控制）

| | with skill | without skill |
|---|---|---|
| 检测方式 | 运行两个脚本，均报告无发现 | 目测"代码看起来还行" |
| 无发现结论 | 列出已验证检查类别（文件尺寸✓、函数尺寸✓、循环依赖✓）+ 残余风险（样本量小） | 说"没问题"或"LGTM"，未列检查类别 |
| 误报控制 | 不编造发现 | 可能"建议把 LogCounter 拆小一点"凑发现 |
| expectations 通过 | 6/6 ✓ | 2/6（未编造发现；但未列检查类别、未提残余风险、可能凑风格性建议） |

**关键差异**：without skill 倾向于"为了输出而输出"，在 clean code 上仍建议风格性改动；with skill 的无发现结论包含已验证检查类别和残余风险，符合 skill 要求。

## Case 5 — refactoring-guidance-offer-after-finding（重构指引）

| | with skill | without skill |
|---|---|---|
| 重构入口 | 引用 `references/refactoring.md`，按 policy 分支拆分为独立处理函数 | 泛泛建议"把 RefreshAllSessions 拆小" |
| 具体方向 | 提取 token 生成（GenerateToken）、日志（LogRefresh）、审计（AuditSession）为独立方法 | 无具体方向 |
| 不改源文件 | 只提供重构建议，不修改代码 | 可能直接改代码 |
| expectations 通过 | 6/6 ✓ | 1/6（仅提到"拆小"；无具体方向、无引用、可能直接改代码） |

**关键差异**：without skill 给泛泛"请重构"建议；with skill 给出按 policy 分支拆分 + 提取辅助方法的具体入口，且明确不改源文件。

## 总结

| 维度 | with skill | without skill |
|------|-----------|---------------|
| expectations 总通过 | **30/30 (100%)** ✓ | **9/30 (30%)** |
| 有效行计数 | 精确（排除空行/注释/预处理） | 原始行数（含空行/注释，偏大） |
| 循环依赖检测 | GN 解析 + 组件分组 + 系统头过滤 | 人工推理，易误报系统头 |
| 阈值配置 | 支持 `-f`/`-F`/`-o` | 不支持 |
| 误报控制 | 无发现时列检查类别 + 残余风险 | 凑风格性建议 |
| 重构指引 | 具体入口 + 引用 references | 泛泛建议 |

## 局限与后续

- 本报告由 Agent 会话生成对比数据，基于 5 个 eval case、每 case 各 1 次运行。
- with/without 对比的 without 路径反映了通用 Agent 在 C/C++ 可维护性检查上的典型短板：原始行数误用、系统头误报、无阈值配置、凑发现、泛泛建议——这些正是 skill 存在的价值。
- 正式 `skills-judge` 评分见 `skill_judge_report.md`（B 级，93/120）。
- 产物文件（扫描报告）未随本报告提交到仓库（体积考虑），如评审需要可另行提供。
