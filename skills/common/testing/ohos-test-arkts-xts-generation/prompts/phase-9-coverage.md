## Phase 9: Coverage Verification

---

### 📦 MANDATORY - 必须先加载以下模块

**在执行本 Phase 前，你必须完整阅读以下文件**（不得设置行数限制）：

**Flow B（执行 APICoverageDetector 扫描时）**：
```
{skill_root}/modules/L1_Analysis/tools/api_coverage_detector.md
{skill_root}/modules/L1_Analysis/verifier/coverage_verifier.md
{skill_root}/scripts/async_coverage_scan.py
```

**注意**：Flow A（已提供覆盖率报告）时，无需加载这些模块。

---

### ⚙️ 按需加载（根据执行模式）

以下模块仅在你执行对应任务时才需要加载：

| 执行模式 | 加载文件 | 说明 |
|---------|---------|------|
| 需要对比覆盖率时 | `{skill_root}/scripts/compare_coverage.py` | 对比 before/after 覆盖率 |
| 需要提取未覆盖项时 | `{skill_root}/scripts/extract_uncovered.py` | 提取未覆盖 API 列表 |

---

### 🚫 Do NOT Load - 禁止加载

本 Phase 期间禁止加载以下模块：

```
所有 L2_Generation 模块（modules/L2_Generation/）
references/conventions/ 目录
```

---

在生成测试用例后，验证覆盖率的补充情况。

| 条件 | 执行方式 | 说明 |
|------|---------|------|
| Flow B（Phase 2 使用了 APICoverageDetector） | 再次运行 APICoverageDetector，与 Phase 2 对比 | 必须：量化生成效果 |
| Flow A（用户提供了覆盖率报告） | 可选：基于用户报告对比新生成用例的覆盖情况 | 用户报告即为基线，无需再次扫描 |

---

### Flow B: APICoverageDetector 覆盖率验证

#### 9.1 执行 APICoverageDetector 扫描

1. **读取 .oh-xts-config.json 中的 ets_version 配置**

   ```powershell
   # 读取配置
   $config = Get-Content .oh-xts-config.json | ConvertFrom-Json
   $ets_version = $config.ets_version
   Write-Host "将扫描 ETS 版本: $($ets_version -join ', ')"
   ```

2. **准备扫描环境（与 Phase 2 步骤 1 相同）**

   使用与 Phase 2 Flow B 步骤 1 相同的文件复制和 `arkts_config.json` 修改流程，确保扫描环境一致。

   ```powershell
   python {skill_root}/scripts/manage_scan_env.py setup --subsystem {Subsystem}
   ```

   覆盖率扫描环境通过 `manage_scan_env.py` 自动准备。

3. **重新执行扫描**（确保新生成的测试用例已在正确的测试目录中）

   统一使用 `async_coverage_scan.py` 操作，与 Phase 2 保持一致。**不要直接调用 `arkts_entrance.exe` 或使用管道输入。**

   ```powershell
   # 3.1 启动异步扫描
   python {skill_root}/scripts/async_coverage_scan.py start

   # 3.2 轮询检查状态（每 30 秒一次，直到完成）
   python {skill_root}/scripts/async_coverage_scan.py status

   # 3.3 扫描完成后获取结果
   python {skill_root}/scripts/async_coverage_scan.py get_results
   ```

   如果配置了多个 ETS 版本，异步扫描会自动为每个版本分别执行扫描。

4. **恢复扫描环境**（与 Phase 2 步骤 4 相同）

   删除过滤目录并恢复 `arkts_config.json`，遵循 Phase 2 Flow B 步骤 4 的操作流程。

#### 9.2 覆盖率分析目标

1. **验证新测试用例的覆盖率贡献**
   - 对比 Phase 2 保存的基线数据（`.coverage_data/iter-1/before_generation_*.csv`）与本次扫描结果
   - 识别新增覆盖的 API
   - 计算覆盖率提升百分点

2. **识别剩余覆盖缺口**
   - 仍然未覆盖的 API 方法
   - 部分覆盖但仍有缺口的场景

3. **生成覆盖率验证报告**

#### 9.3 覆盖率对比报告格式

```markdown
# 覆盖率验证报告

## 覆盖率提升统计

### 更新前覆盖率 (Phase 2)
- 总 API 数: 45
- 已覆盖 API: 12  
- 未覆盖 API: 33
- 覆盖率: 26.7%

### 更新后覆盖率 (Phase 9)
- 总 API 数: 45
- 已覆盖 API: 28
- 未覆盖 API: 17
- 覆盖率: 62.2%

### 覆盖率提升
- 新增覆盖 API: 16
- 覆盖率提升: +35.5%
- 提升百分比: 133.1%

## 新增覆盖的 API

**新增完整覆盖**
- `ArraySortUtil.sort()`: 从 0% → 100%
- `DateUtils.formatDate()`: 从 0% → 100%

**新增部分覆盖**
- `NetworkManager.request()`: 从 30% → 80%

## 仍然未覆盖的 API

**高优先级未覆盖**
- `DatabaseManager.query()`: 核心方法未测试

**中优先级未覆盖**  
- `Logger.debug()`: 辅助功能未测试

## 覆盖率缺口分析

### 方法级缺口
- 完全未测试方法: 17 个
- 部分测试方法: 8 个

### 参数场景缺口
- 缺少 null/undefined 测试: 12 个方法
- 缺少边界值测试: 8 个方法
- 缺少错误码测试: 15 个方法

## 进一步测试建议

1. 优先测试 `DatabaseManager.query()` 的基本功能
2. 为 `NetworkManager.request()` 添加错误码测试
3. 完善 `Logger.debug()` 的参数验证
```

#### 9.4 保存覆盖率验证数据

使用 `convert_results.py` 自动保存 after_generation CSV：

```bash
python {skill_root}/scripts/convert_results.py --iter {N} --phase after
```

然后使用 `compare_coverage.py` 自动生成覆盖率对比报告：

```bash
python {skill_root}/scripts/compare_coverage.py --iter {N}
```

`compare_coverage.py` 自动完成：
- 读取 `iter-{N}/` 下的 `before_generation_*.csv` 和 `after_generation_*.csv`
- 对比覆盖率差异（新增覆盖、仍未覆盖）
- 生成 Markdown 报告：`iter-{N}/coverage_comparison_{ver}.md`

**迭代数据保存规则**：
- 每轮迭代完成后，将生成后的覆盖率数据保存到对应的 `iter-{N}/` 目录
- 第N轮的 `after_generation_ets{X}_timestamp.csv` 将作为第N+1轮的 `before_generation_ets{X}_timestamp.csv`
- 这样可以完整追踪每一轮的覆盖率变化：before → after

**多版本处理**：
- 如果用户选择了多个 ETS 版本，会为每个版本保存对应的 after_generation 文件
- 每个版本独立追踪覆盖率变化，便于比较不同语法版本的测试效果

**迭代数据流示例**：
```
iter-1/
├── before_generation_ets1.1_20260417103000.csv  # 初始覆盖率
├── uncovered_apis_20260417103500.json           # 提取的未覆盖API
├── xxxxx.design.md                              # 测试设计
└── after_generation_ets1.1_20260417120000.csv   # 第一轮后覆盖率

iter-2/  
├── before_generation_ets1.1_20260417120500.csv  # 复用 iter-1/after_generation
├── uncovered_apis_20260417121000.json           # 提取的新未覆盖API
├── yyyy.design.md                              # 测试设计  
└── after_generation_ets1.1_20260417150000.csv   # 第二轮后覆盖率
```

#### 9.5 注意事项

1. **扫描环境**: 确保在正确的 SDK 环境下运行 APICoverageDetector
2. **配置文件**: 根据子系统类型选择正确的配置文件（arkts_config.json 或 c_config.json）
3. **路径设置**: 确保测试路径和 SDK 路径配置正确
4. **结果记录**: 保存覆盖率对比数据，用于后续分析和改进
5. **连续验证**: 对于大型子系统，可以分批次进行覆盖率验证

---

### Flow A: 可选验证

用户已提供覆盖率报告，Phase 9 验证为可选项：
- 如果用户要求验证，对比用户报告中的缺失项与新生成的用例覆盖情况
- 如果用户未要求，直接进入 Phase 10（Output）
