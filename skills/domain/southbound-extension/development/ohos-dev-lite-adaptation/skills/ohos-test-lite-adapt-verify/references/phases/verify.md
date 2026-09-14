# 阶段 4 · verify — 验证

**前置**：optimization 模式已完成 implement（代码已改）；test-only 模式环境就绪即直接进入本阶段（跳过阶段 1-3）。基线 MAP 在 `xts_test/reports/baseline_map.md`（optimization 必需；test-only 仅有则参考、无则跳过 MAP 对比）。


> **模式区分**：本阶段有两种入口模式。
> - **test-only**（仅重跑测试，不改代码）：MAP 体积对比仅作信息参考，不强制改善；测试全过即进入 summary。
> - **optimization**（代码优化后验证）：需附 MAP 改善证据（基线/提案/收益），MAP 无改善（仅 optimization 模式；test-only 模式跳过此检查）先归因再路由——评估有误/实现问题回 implement，改动未生效/链接配置修构建环节。
> 模式由**用户意图**决定（不由代码是否变动决定）：用户要求跑测试/验证（含"功能改完了帮我跑 XTS"）= test-only；用户要求优化闭环、本工作流阶段 1-3（基线/提案/实施）已跑 = optimization（工作流 P5 优化路径）。
> test-only 的执行路径按**板上镜像是否就是待测产物**判定，判定**须核实**——启动日志的构建时间戳/版本号，或产物哈希比对；**无法核实 → 按不一致处理**：核实一致 → `ohos-ci-lite-deploy-burn` 的 `--run-only`（只复位 + 串口捕获，不烧录）；不一致或无法核实（如刚编译的新固件）→ 仍走完整烧录 + 测试（burn_one.py 不带 --run-only）。

## 核心原则：测试策略由用户决定

本阶段 **不硬编码任何特定测试套件**。实际执行的测试取决于 `init` 阶段
用户选择的 `test.strategy`（XTS / Unit Test / Integration / Manual / Custom）。

**约定路径**：

- ohos-ci-lite-deploy-burn：`skills/ohos-ci-lite-deploy-burn/`
- 基线 MAP：`xts_test/reports/baseline_map.md`
- 产物：`xts_test/reports/verify_result.md`

## 执行步骤

### 1. 编译（调用 ohos-ci-lite-deploy-burn Phase 1）

> test-only 且已核实板上镜像即待测产物时：编译/下载仅为获取**与板上镜像同源**的 .map（供 MAP 参考对比）。若本地无法产出同源 .map（源码已变动 / 原构建产物已删）：要么完整烧录待测产物，要么 MAP 参考值标注「来源为另一次构建，不可与本次测试结果关联」。

1. 读取 `config.json` 和设备 profile
2. 根据 `test.strategy` 选择编译模式：
   - **XTS**：build_mode = `xts_all`（含 XTS 编译）
   - **其他策略**：build_mode = `firmware`（标准固件编译，测试另计）
3. 调用 `ohos-ci-lite-deploy-burn` Phase 1 编译
4. 编译失败：先分类原因——**源码缺陷**（本轮改动引入的编译错误）：optimization → 回 `implement`（按已批准 tasks）修正；**环境 / 构建配置 / 工具链问题**（依赖缺失、工具链版本、GN 配置、服务器环境，与改动无关）→ 修环境或构建配置（必要时调 `ohos-dev-cross-toolchain` / `ohos-dev-build-config` skill）后重跑，**不改产品代码**；test-only → 报错并报告用户（含原因分类），不代改用户代码

### 2. 下载产物（Phase 2）

1. 调用 `ohos-ci-lite-deploy-burn` Phase 2 下载编译产物
2. 确认 .map 文件已下载到本地
3. 下载失败 → 归因为连接/网络问题（SSH/SCP 配置、服务器状态）：修 connection 配置（必要时回 `init` 校准）后重试，**不改产品代码**；optimization 模式 .map 缺失则 MAP 对比无法进行（阻塞验证），test-only 无 map 不阻塞（按模式规则跳过 MAP 对比）

### 3. 烧录 + 跑测试（Phase 3~4）

> 烧录失败 → 先分类（按 ohos-ci-lite-deploy-burn 的退出码表与排查清单）：**环境/端口问题**（端口占用、AT 静默、串口驱动）→ 修环境重试，不改产品代码；**介质/烧录包错配**（L1 典型：no find spi / Invalid spi flash block size）→ 按板上实际介质重做烧录包，不改产品代码；**产物问题**（bin 损坏/不完整）→ 重新构建下载产物再烧。烧录失败不回 implement。

**根据 test.strategy 分流**：

#### 策略 A：XTS
详见 `references/test-strategies/xts.md`。

简要流程：
1. 调用 `ohos-ci-lite-deploy-burn` Phase 3 烧录（带 XTS 固件）
2. 调用 Phase 4 复位设备 + 串口捕获输出
3. 解析 XTS 输出：统计 Total / Pass / Fail / Not Run
4. 生成 XTS 结果报告

#### 策略 B：Unit Test
1. 若测试代码在固件内：烧录后触发测试运行（串口捕获结果）
2. 若测试在主机端（host-test）：在编译服务器上运行测试二进制
3. 解析测试框架输出（Unity / GoogleTest / 自定义框架）
4. 统计通过率

#### 策略 C：Integration Test
1. 烧录固件
2. 按集成测试用例逐步操作（可能需要外部激励：按键/网络/传感器）
3. 串口捕获 + 人工/自动判定结果
4. 记录每条用例 Pass/Fail

#### 策略 D：Manual Test
1. 烧录固件
2. 提供 manual test checklist 给用户
3. 用户逐项操作并报告结果
4. 记录用户反馈

#### 策略 E：Custom Test
1. 按 init 阶段用户描述的自定义方案执行
2. 按用户定义的格式采集结果

### 4. MAP 对比确认收益（仅 optimization 模式设门槛）

- **optimization 模式**：执行 MAP 对比并按提案预期判定（见下）。
- **test-only 模式**：有基线 MAP 则跑对比作参考信息（只记录、不设门槛）；无基线则跳过本节。参考值须注明来源构建：.map 与板上待测镜像同源时可直接关联；来自另一次构建时标注「不可与本次测试结果关联」。

```bash
python skills/ohos-ci-lite-deploy-burn/tools/map_analyzer.py compare \
  <基线map文件> <新map文件>
```

将 delta 写入 `verify_result.md`：
- RAM 变化（+/- KB，百分比）
- Flash/ROM 变化（+/- KB，百分比）
- Top 变化最大的段/符号

确认（仅 optimization 模式）：
- RAM/ROM 改善达到提案预期？
- 反而增大？→ 先归因再路由（同回炉表：评估有误/实现问题 → implement；改动未生效/链接配置 → 修构建环节，不改产品代码）

### 5. 不通过则回炉

| 情况 | 处理 |
|------|------|
| 测试有 Fail（optimization） | 先分类（实现缺陷 / 环境问题 / 用例缺陷），**按类别路由**：**实现缺陷** → 回 `implement` 按已批准 tasks 修正 → 重跑本阶段；**环境问题**（串口/供电/烧录配置/测试板）→ 修环境或配置（必要时回 `init` 校准）后重跑，**不改产品代码**；**用例缺陷**（测试方案/用例本身错）→ 修测试方案或报告用户（改动需授权），不进 implement |
| 测试有 Fail（test-only） | 记录失败用例与证据、保留失败状态并报告结果，**不自动进 implement**（implement 前置要求已批准提案/tasks，且 test-only 约定不改代码）；确需修源码先征得用户授权，再切换修改流程 |
| MAP 无改善 / 恶化（仅 optimization 模式） | 先归因再路由：**优化点评估有误 / 实现问题** → 回 `implement` 修正；**改动未生效**（烧错 bin / 构建缓存 / 编译未含改动）→ 修构建或烧录环节后重跑，不改产品代码；**gc-sections 丢段 / 链接配置** → 修构建配置（必要时调 `ohos-dev-build-config`），不改产品代码 |
| 测试全部通过（test-only 即满足） | 进入 `summary` |
| 测试全部通过 + MAP 达标（optimization） | 进入 `summary` |

**回炉次数上限建议**：同一问题回炉超过 3 次 → 咨询 Oracle 或请求用户介入决策。回炉循环仅 optimization 模式；test-only 失败即报告终止，不进入回炉循环。

### 6. 阶段收尾

确认清单：
- [ ] 编译成功（无 error）
- [ ] 烧录成功（设备正常启动）
- [ ] 测试结果已采集（按所选策略的格式）
- [ ] `verify_result.md` 含测试统计（MAP 对比 delta：optimization 必含；test-only 有基线则记参考值，无基线标 N/A）
- [ ] 测试结果收口：test-only 必须全部通过——有 Fail 即终止并报告，不进 summary；optimization 通过，或按已批准规则回炉；用户明确接受的未达标项单独标记为未达标，不写成「验证通过」
- [ ] RAM/ROM 改善达提案预期（仅 optimization 模式；或用户接受当前结果）

回显验证结果摘要（缺失项标 N/A，不硬凑），提示用户下一阶段（summary，见 `references/phases/summary.md`）。
