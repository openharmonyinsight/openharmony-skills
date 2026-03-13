# Plan 输出模板

Planner 在步骤 1 输出 Plan 时使用此模板：

```markdown
# [功能名] Implementation Plan

**Goal:** [一句话目标]
**Architecture:** [2-3 句方案描述]
**Reference:** [参考的源文件或文档列表，如有]
**Assumptions / Open questions:** [如果有推断项，写在这里；用“Assume:”或“Need user confirm:”标记]

---

### Task 1: [组件名]

**Files:**
- Create: `exact/path/to/file.h`
- Modify: `exact/path/to/existing.cpp:123-145`
- Test: `tests/exact/path/to/test.cpp`

**Tests:** TS / C++ / TS + C++

**Implementation outline:**
- 先补一个能证明缺陷/需求的失败测试
- 再补最小实现使测试通过
- 如需新增源文件，同步更新 `BUILD.gn`

**Acceptance:**
- 变更覆盖目标路径和关键边界
- 文档同步到 `.agents/ets-runtime-dev/<branch-name>/docs/`
- 提交保持原子化

**Commit:**
`feat(scope): description`
```
