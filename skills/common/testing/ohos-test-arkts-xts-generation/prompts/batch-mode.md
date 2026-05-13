## 分批执行模式（Batch Mode）

当未覆盖 API 数量较多时（>20），支持分批生成测试用例。每批最多 10 个 API，按模块分组，同模块尽量同批。使用 `scripts/batch_manager.py` 管理。

在 Phase 1 结束后向用户确认执行模式：

1. **完整流程**（Phase 2-10 一次性执行）— 适合 API 数量 ≤ 20
2. **分批执行**（每批 ≤10 API，逐批执行）— 适合大型子系统
3. **精准增量**（用户手动指定 API 范围）— 适合补充特定 API 测试

### 核心命令

```bash
python {skill_root}/scripts/batch_manager.py plan [--max-apis 10]   # 生成分批计划
python {skill_root}/scripts/batch_manager.py status                  # 查看执行状态
python {skill_root}/scripts/batch_manager.py start <batch_id>        # 开始指定批次
python {skill_root}/scripts/batch_manager.py complete <batch_id>     # 完成批次
python {skill_root}/scripts/batch_manager.py skip <batch_id>         # 跳过批次（保留已生成内容）
python {skill_root}/scripts/batch_manager.py resume                  # 查看下一个待执行批次
```

### 与 Phase 流程的集成

批量模式不改变 Phase 1-10 的定义，仅在 Phase 3-5 的**执行范围**上做分批：

| Phase | 批量模式行为 |
|-------|-------------|
| 1-2 | 不变（配置加载 + 覆盖率扫描） |
| 3 | 仅解析 `batch_manager.py start <id>` 指定的 10 个 API |
| 4 | 仅生成这 10 个 API 的测试设计 |
| 5 | 仅生成这 10 个 API 的测试用例 |
| 6-10 | 每批次执行，或全部批次完成后统一执行 |

数据持久化目录 `batch_workspace/`（含 `batch_plan.json` 分批计划、`completed.json` API 级完成状态、`batch_N_generated_apis.json` 各批次生成详情），并发安全通过 `scripts/batch_lock.py` 文件锁保护。
