# tasks.md 模板

Planner 在用户确认 Plan 后，按此模板生成 `.agents/ets-runtime-dev/<branch-name>/tasks.md`：

只使用 `Status` / `Reason` / `Progress` 表达任务生命周期；不要追加 `Compile Validation Status`、`Build Result` 等自定义字段。
编译验证也复用已有 Task；不要新建 `Task 2: Compile Validation` 一类结构。

```markdown
# Tasks

## Task 1: [组件名]
- [ ] Write failing test (TS / C++ / TS + C++)
- [ ] Write implementation
- [ ] Format & commit
- Status: pending
- Reason:

## Task 2: ...

---
Progress: 0/N completed
```

括号内测试类型为 `TS` / `C++` / `TS + C++` 之一，与 Plan 中对应 Task 的 `Tests` 字段一致。
