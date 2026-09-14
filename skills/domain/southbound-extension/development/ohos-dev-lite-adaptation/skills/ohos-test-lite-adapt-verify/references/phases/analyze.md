# 阶段 2 · analyze — 需求分析（提案）

**前置**：已完成 explore（有基线 MAP、架构图、优化/验证初稿）。

**约定路径**：

- ohos-ci-lite-deploy-burn tools：`.../ohos-ci-lite-deploy-burn/tools/map_analyzer.py`
- 产物：`xts_test/proposals/<proposal-id>/` 下的 proposal / design / specs / tasks

## 执行步骤

### 1. 深入分析优化/验证点

对探索阶段的每个初稿条目逐一论证：

**每项分析必须包含**：
- **可行性**：技术上能否实现？有什么依赖或约束？
- **预期收益**：RAM / ROM 预估节省量（KB 级精度）
- **风险评估**：可能影响哪些功能？回归风险多大？
- **实现复杂度**：改动范围（文件数 / 代码行数）

量化手段：
- `map_analyzer.py analyze` 对基线 MAP 做更细粒度的段/符号级量化
- 若有多个历史 build 产物，可用 `map_analyzer.py compare` 做对比
- 读取源码确认优化点的实际影响面

### 2. 生成提案文档

在 `xts_test/proposals/<proposal-id>/` 下生成完整提案：

```
proposals/<proposal-id>/
├── proposal.md    # 提案总览（目标、基线、验收标准）
├── design.md      # 技术方案（每项优化的具体做法）
├── specs.md       # 能力规格 delta（变更前后对比）
└── tasks.md       # 可执行任务清单
```

**proposal.md 必须包含**：
- 优化/验证目标（一句话）
- 基线数字（来自 baseline_map.md）
- 各优化点汇总表（预期收益 / 风险 / 复杂度）
- **验收标准**（必须包含）：
  - 测试策略不回归（见 init 阶段选择的测试策略）
  - RAM / ROM 改善量达到预期
  - 无新增编译错误 / 警告

**tasks.md 每条 task 必须**：
- 明确目标文件（相对 code_dir 的路径）
- 改动意图（做什么、为什么）
- 预期收益（RAM / ROM 影响）
- 验证方法（如何确认改动正确）

### 3. 与用户迭代到批准

1. 向用户展示提案摘要（各优化点 + 预期收益汇总）
2. 询问是否有补充 / 修改 / 排除意见
3. 用户有补充 → 回步骤 1 分析补充点 → 更新提案；循环直到用户明确批准
4. **用户批准前不进入实现阶段**

批准标志：用户明确说"通过"/"批准"/"可以开始改了"。

### 4. 阶段收尾

确认清单：
- [ ] `xts_test/proposals/<proposal-id>/` 下 4 个文件齐全
- [ ] tasks 清晰可执行（每条含目标文件、改动意图、预期收益、验证方法）
- [ ] 验收标准明确（含测试不回归 + RAM/ROM 改善量）
- [ ] 用户已明确批准

回显任务清单摘要，提示用户下一阶段（implement，见 `references/phases/implement.md`）。
