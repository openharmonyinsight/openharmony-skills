## 分批执行模式（Batch Mode）

当未覆盖 API 数量较多时，支持分批生成测试用例。每批最多 10 个 API，按模块分组，同模块尽量同批。使用 `scripts/batch_manager.py` 管理。

### 分批决策依据

**并非简单的"API数量>20就分批"**，还需综合判断：

| 因素 | 倾向完整流程 | 倾向分批执行 |
|------|------------|------------|
| API数量 | ≤20 | >20 |
| API复杂度 | 简单（单参数） | 复杂（回调/异步/多态） |
| 模块分散度 | 同一模块 | 跨多个模块 |
| Context窗口余量 | 充裕 | 紧张 |
| 用户时间要求 | 不急 | 需要快速看到部分结果 |

**分批经验**：
- 同模块API尽量同批（共享import和helper函数）
- 异步API单独分批（需要特殊的测试框架处理）
- UI类API和非UI类API分开（不同的生成流程，UI类走Phase 5A/5B，非UI类走Phase 5）

在 Phase 1 结束后向用户确认执行模式：

1. **完整流程**（Phase 2-10 一次性执行）— 适合 API 数量 ≤ 20 且复杂度低
2. **分批执行**（每批 ≤10 API，逐批执行）— 适合大型子系统或API复杂度高
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
| 4 | 仅生成这 10 个 API 的测试设计（含控件ID清单） |
| 5A | 仅对这 10 个 API 中的 UI 类用例生成 Demo（增量追加到已有 Demo 工程） |
| 5 | 仅生成这 10 个 API 中的非 UI 类测试用例 |
| 5B | 仅生成这 10 个 API 中的 UI 类 UiTest 测试用例 |
| 6-10 | 每批次执行，或全部批次完成后统一执行 |

数据持久化目录 `batch_workspace/`（含 `batch_plan.json` 分批计划、`completed.json` API 级完成状态、`batch_N_generated_apis.json` 各批次生成详情），并发安全通过 `scripts/batch_lock.py` 文件锁保护。
