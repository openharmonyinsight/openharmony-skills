# Skill 评估报告: ohos-test-arkts-xts-generation

## 总结

- **总分**: 113/120 (94.2%)
- **等级**: A
- **模式**: Process（12 阶段工作流 + 渐进式披露）
- **知识比例**: E:A:R = 75:20:5
- **结论**: 优秀的领域专家级 Skill —— 捕获了需要多年积累才能获得的 OpenHarmony XTS 测试深度知识。

## 维度评分

| 维度 | 得分 | 满分 | 说明 |
|------|------|------|------|
| D1: 知识增量 | 18 | 20 | 大量专家级内容：ArkTS-Dyn/Sta 差异、8 条类型约束及错误码、801 设备防护、prebuilts 切换、Flow A/B/C 决策树 |
| D2: 思维模式 + 流程 | 14 | 15 | 强思维框架（"设计文档是唯一蓝图"、"BOUNDARY 非必选——仅当 3 个条件同时满足"）+ 领域专属 12 阶段工作流 |
| D3: 反模式质量 | 15 | 15 | 20+ 条 NEVER 规则，每条含具体原因 + 正确做法 + 后果。如 "NEVER 并行编译 dyn/sta —— hvigor 版本不兼容" |
| D4: 规范合规性 | 15 | 15 | 完美的 description：WHAT（XTS 生成、覆盖率、Demo+UiTest）、WHEN（8 种触发场景）、KEYWORDS（XTS, ArkTS-Dyn/Sta, Hypium, @tc, build...） |
| D5: 渐进式披露 | 14 | 15 | SKILL.md=321 行（路由），prompts/=3,396 行（阶段工作流），modules+references/=18,538 行（深度知识）。条件加载触发器含"何时查阅"列 |
| D6: 自由度校准 | 14 | 15 | 对编译依赖型任务自由度适当偏低：精确脚本、类型约束表、错误码。安全范围内保留灵活性（测试设计、分批决策） |
| D7: 模式识别 | 9 | 10 | 清晰的 Process 模式：12 阶段、phase_tracker 检查点、Flow A/B/C 分支。因领域复杂性从 ~200 行扩展至 ~23K 行，合理 |
| D8: 实际可用性 | 14 | 15 | 决策树、可运行脚本、4 级错误分类、重试策略、边界场景（多版本、批量模式、801 防护、会话连续性） |

## 关键问题

无 —— 已达到生产就绪状态。

## 改进建议 Top 3

1. **D5**: 在 phase prompt 中增加更多明确的 "Do NOT Load" 指引以防止过度加载（如 "Do NOT load `arkts_static_constraints.md` for ArkTS-Dyn projects"）
2. **D1**: `docs/` 目录（4 个文件）标注为"仅供人类参考" —— 考虑是否可将部分内容整合到 phase prompt 中，减少孤立文件
3. **D8**: 跨阶段引用可更明确（如 Phase 5 引用 Phase 4 的控件 ID 清单时，可链接到具体章节）

## 详细分析

### D1: 知识增量 (18/20)

本 Skill 是知识外部化的典范。关键专家级内容：

- **ArkTS-Dyn vs ArkTS-Sta 差异表**（SKILL.md:110-117）：hypium 导入路径、401 错误码处理、`as any` 禁令、变量声明规则 —— 没有此 Skill，Claude 不可能知道这些
- **8 条类型约束**（phase-5-generation.md:65-74）：`Function` → `() => void`、`@ohos.router` 而非 `@ohos/router`、JSON.parse 用 `ESObject` —— 每条附带具体编译错误码（10605008、10505001）
- **801 设备能力防护**（test_generator.md:48-59）：当 `@throws` 声明 801 时，所有测试用例必须包裹 801 防护逻辑 —— 来自真机测试的非显而易见的规则
- **prebuilts 环境切换**（phase-8-build.md）：dyn 用 hvigor 5.x，sta 用不同版本 —— 并行编译会导致冲突
- **Flow A/B/C 决策树**：覆盖率报告驱动 vs 标准扫描 vs 新增接口 —— 每种对应不同的阶段执行路径

轻微扣分：部分通用测试概念（PARAM/ERROR/BOUNDARY 的含义）有简要解释，但可假设 Claude 已知。

### D2: 思维模式 + 流程 (14/15)

**思维框架**：
- "设计文档是**唯一蓝图**" —— 防止过度生成
- "BOUNDARY 非必选 —— 仅当三个条件同时满足" —— 防止在不可测边界上浪费精力
- "API 严格遵循：仅使用 .d.ts 中声明的接口" —— 防止编译失败

**Claude 不会知道的领域流程**：
- APICoverageDetector 通过 `async_coverage_scan.py` 异步扫描（不直接调用可执行文件）
- `cleanup_group.sh` → `async_build.sh start` → `async_build.sh wait` → 验证产物的流水线
- BUILD.gn target 提取：`grep -oP 'ohos_js_app_suite\("\K[^"]+' BUILD.gn`
- Phase tracker：每个 phase 前 `check`，完成后 `complete`

### D3: 反模式质量 (15/15)

NEVER 列表（SKILL.md:209-301）极为出色。每条规则都包含：
1. **具体禁止项**："NEVER 在 ArkTS-Sta 项目中使用 `as any`"
2. **非显而易见的理由**："静态编译器会拒绝并报错 ESE0143/ESE0046"
3. **正确做法**："使用具体类型声明或类型守卫"
4. **后果**："编译失败"

只有经验才能教会的突出规则：
- "NEVER 并行编译 dyn/sta —— hvigor 版本不兼容"
- "NEVER 在 Phase 9 后自动修复断言失败 —— 可能掩盖接口 bug"
- "NEVER 延迟创建 session_issues 日志 —— 上下文丢失"
- "NEVER 跳过 prebuilts 切换直接编译静态版本"

### D4: 规范合规性 (15/15)

description 是典范级示例：
```yaml
description: >
  OpenHarmony ArkTS XTS测试用例生成器。解析.d.ts API定义，生成符合Hypium框架的测试用例，
  支持覆盖率分析、编译验证和Demo+UiTest生成。
  支持ArkTS-Dyn（动态）和ArkTS-Sta（静态）两种语法模式，覆盖12-Phase完整工作流。
  Use when: (1) 用户提到XTS测试、ArkTS测试用例生成、API覆盖率扫描,
  (2) 用户需要为@kit.* SDK生成测试,
  ...
  (7) 用户要求编译指定的测试套（如"编译xxx"、"build xxx"、"重新编译"）,
  (8) 用户提到编译失败、编译错误、SDK补齐后重新编译。
  Trigger keywords: XTS, ArkTS-Dyn, ArkTS-Sta, test generation, API coverage,
  APICoverageDetector, Hypium, batch generation, .ets files, @tc annotation...
```
- WHAT：XTS 测试生成、覆盖率分析、Demo+UiTest
- WHEN：8 种明确的触发场景
- KEYWORDS：20+ 个可搜索关键词，含中文

### D5: 渐进式披露 (14/15)

三层架构执行良好：
- **Layer 1**（SKILL.md，321 行）：路由表、配置、反模式、架构概览
- **Layer 2**（prompts/，16 个文件）：阶段专属工作流，含条件加载表
- **Layer 3**（modules/ + references/，~18,500 行）：深度领域知识

加载触发器嵌入在每个 phase prompt 中：
```markdown
### ⚙️ 按需加载（根据任务需要）
| 任务 | 加载文件 | 说明 |
|------|---------|------|
| 生成错误码测试 | error_test.md | 错误码提取和测试规则 |
| ArkTS-Sta 静态项目 | arkts_static_constraints.md | 静态语法约束 |
```

轻微扣分：部分 phase 可增加明确的 "Do NOT Load" 指引以防止过度加载。

### D6: 自由度校准 (14/15)

对编译依赖型任务，自由度适当偏低：
- **低自由度**：精确脚本（`async_build.sh`）、类型约束表（T1-T8）、错误码映射
- **中自由度**：测试设计决策（BOUNDARY 可选）、Flow 选择、分批大小
- **高自由度**：不适用 —— 此领域需要精度

约束级别与脆弱性匹配：错误类型 → 编译失败，错误路径 → 环境损坏。

### D7: 模式识别 (9/10)

清晰的 Process 模式执行：
- 12 个阶段，含明确的入口/出口条件
- `phase_tracker.py` 检查点强制执行
- Flow A/B/C 基于用户上下文分支
- 强制阶段（4、7）不可跳过

该 Skill 将 Process 模式从 ~200 行扩展到 ~23K 行总行数，因 OpenHarmony 的领域复杂性而合理。SKILL.md 通过有效的渐进式披露保持在 321 行。

### D8: 实际可用性 (14/15)

全面的决策支持：
- **决策树**：Flow A/B/C 优先级规则、入口点选择、错误级别分类
- **可运行代码**：Python 脚本、bash 命令、TypeScript 模板均可直接使用
- **错误处理**：4 级分类（自动修复 → 重试 → 用户确认 → 终止），最多 3 次重试且每次采用不同策略
- **边界场景**：多版本串行编译、批量模式（>20 API）、801 设备防护、会话连续性、格式不兼容降级方案
