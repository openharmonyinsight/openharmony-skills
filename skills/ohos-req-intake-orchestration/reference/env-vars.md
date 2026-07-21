# 环境变量解析

主 Session 在 Phase 0 启动时确定以下变量值，后续所有步骤引用这些变量：

| 变量 | 含义 | 取值规则 |
|------|------|----------|
| `SKILL_HOME` | 只读资源路径（skill 定义、模板、参考资料、已有分析） | **默认 = 主 Session 当前工作目录（cwd）**，即 skill 定义的根路径 |
| `WORK_HOME` | 产出物路径（设计文档、分析报告、生成代码） | **默认 = SKILL_HOME**。用户可指定为目标代码仓库（跨仓库场景） |
| `DOCS_REPO` | 设计文档仓库路径（产出物存放位置） | **启动时自动发现，找不到则询问用户**：按优先级查找 → 找到即使用 → 均未找到则询问用户输入路径 |
| `docs_dir` | 特性归档产物目录 | `{DOCS_REPO}/docs/features/{change-id}/`（默认）或 `{DOCS_REPO}/.codespec/changes/{change-id}/`（可选，与 ODK 对齐） |
| `analysis_dir` | 代码分析缓存目录 | `{DOCS_REPO}/analysis/` |
| `references_dir` | 参考资料 | `{DOCS_REPO}/references/` |

**取值逻辑：**

1. 主 Session 启动时，`SKILL_HOME` = 当前工作目录（cwd）
2. 如果用户指定了其他工作目录，则 `WORK_HOME` = 用户指定路径；否则 `WORK_HOME` = `SKILL_HOME`
3. `DOCS_REPO` 启动时检查（按优先级依次尝试，找到第一个满足条件的即停止）：
   - `{SKILL_HOME}` 本身（检查是否包含 `docs/features/` 和 `analysis/` 子目录）
   - 从 `SKILL_HOME` 逐级向上查找包含 `docs/features/` 和 `analysis/` 子目录的目录
   - 以上均未找到 → 询问用户："未找到设计文档仓库（需包含 docs/features/ 和 analysis/ 目录），请输入完整路径"
4. `docs_dir` = `{DOCS_REPO}/docs/features/{change-id}/` — 默认归档路径（与 ODK 对齐场景可使用 `.codespec/changes/{change-id}/`）
5. 主 Session 在 spawn subagent 时，将上述变量替换为实际绝对路径后注入 task 描述；subagent 收到的是实际路径值，不含变量名

> **重要：** SKILL.md 中所有路径引用均使用上述变量。实际执行时由主 Session 完成变量替换。
