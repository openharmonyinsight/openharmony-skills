## Phase 10: Coverage Verification

---

> **`knowledge_root` 降级**：下文中所有 `{knowledge_root}/...` 路径，若 `knowledge_root` 未配置或路径不存在，则降级从 `{skill_root}/modules/` 和 `{skill_root}/references/` 加载对应内置知识。完整映射表见 `system.md`「知识库路径与降级规则」。

### 📚 参考文档（按需查阅）

本 Phase 执行过程中可参考以下文件，遇到具体问题时按需查阅：

| 文件 | 内容 | 何时查阅 |
|------|------|---------|
| `{knowledge_root}/common/xts_experience/09_methodology/06_api_coverage_detector.md` | APICoverageDetector 工具完整手册 | 扫描命令参数不确定时（Flow B） |
| `{knowledge_root}/common/xts_experience/09_methodology/07_coverage_verifier.md` | 覆盖率验证方法论（before/after 对比、增量计算） | 对比逻辑不确定时（Flow B） |

---

### ⚙️ 按需加载（根据执行模式）

以下模块仅在你执行对应任务时才需要加载：

| 执行模式 | 加载文件 | 说明 |
|---------|---------|------|
| 需要提取未覆盖项时 | `{skill_root}/scripts/extract_uncovered.py` | 提取未覆盖 API 列表（直读 Excel） |
| 需要对比覆盖率时 | `{skill_root}/scripts/compare_uncovered.py` | 对比 before/after uncovered JSON，生成变化报告 |

---

### 🚫 Do NOT Load - 禁止加载

本 Phase 期间禁止加载以下模块：

```
所有 L2_Generation 模块（{knowledge_root}/common/xts_experience/）
{knowledge_root}/common/xts_experience/ 下的 01_framework、02_arkts、03_standards、04_project、05_patterns 规范文件
```

---

### Phase 执行策略

Phase 10 耗时较长（APICoverageDetector 扫描约需 5-15 分钟），支持以下执行策略：

| 策略 | 触发条件 | 说明 |
|------|---------|------|
| **执行** | Flow B 必须（量化生成效果），Flow A/C 可选 | 完整执行覆盖率扫描和对比 |
| **跳过** | 用户明确要求跳过，或无 APICoverageDetector 环境 | 记录跳过原因，直接输出最终结果 |

> **与 Phase 9 并行**：Phase 10 与 Phase 9 互相独立，可以并行执行以节省总耗时。详见 Phase 9 的 9.8 节。

---

在生成测试用例后，验证覆盖率的补充情况。

| 条件 | 执行方式 | 说明 |
|------|---------|------|
| Flow B（Phase 2 使用了 APICoverageDetector） | 再次运行 APICoverageDetector，与 Phase 2 对比 | 必须：量化生成效果 |
| Flow A（用户提供了覆盖率报告） | 可选：基于用户报告对比新生成用例的覆盖情况 | 用户报告即为基线，无需再次扫描 |
| Flow C（新增接口模式） | **仅执行 after 扫描**，无 before baseline | 新增接口生成前覆盖率为 0，仅需验证 after 覆盖情况 |

---

### Flow B: APICoverageDetector 覆盖率验证

#### 10.1 执行 APICoverageDetector 扫描

1. **读取 .oh-xts-config.json 中的 ets_version 配置**

    ```bash
    cat .oh-xts-config.json | python -c "import sys,json; cfg=json.load(sys.stdin); print('ETS versions:', cfg.get('ets_version', []))"
    ```

2. **增量同步新生成的测试文件到扫描目录**

   Phase 10 复用 Phase 2 已准备好的扫描环境，使用 `manage_scan_env.py sync`（用法见 Phase 2 步骤 2 的增量同步说明）仅同步新增/修改的文件。manifest 文件由 Phase 5 生成代码时自动记录：

   ```json
   {"files": ["ace_ets_module_ui/.../NewTest.test.ets", ...]}
   ```

   > **仅在 Phase 2 未执行过 setup 时**才需要完整 setup：
   > ```bash
   > python {skill_root}/scripts/manage_scan_env.py setup --subsystem {Subsystem} --module {ModuleRelPath}
   > ```

3. **重新执行扫描**（确保新生成的测试用例已在正确的测试目录中）

   操作与 Phase 2 步骤 3 完全一致（`async_coverage_scan.py` 的 start → status → get_results 流程）。
   **不要直接调用 `arkts_entrance.exe`。**

   如果配置了多个 ETS 版本，异步扫描会自动为每个版本分别执行扫描。

4. **恢复扫描环境（仅在用户要求时执行）**

   与 Phase 2 步骤 5 保持一致：**默认不执行 teardown**，仅在用户明确要求时才恢复环境。

#### 10.2 覆盖率分析目标

1. **验证新测试用例的覆盖率贡献**
    - 使用 `extract_uncovered.py` 从本次扫描结果（after Excel）提取未覆盖 API
    - 使用 `compare_uncovered.py` 对比 Phase 2 的 before uncovered JSON 与本次 after uncovered JSON
    - 识别新增覆盖的 API 和覆盖率提升

2. **识别剩余覆盖缺口**
    - 仍然未覆盖的 API 方法
    - 部分覆盖但仍有缺口的场景

3. **生成覆盖率验证报告**（报告格式见 Phase 11 §3 覆盖率总结）

#### 10.4 提取未覆盖项并生成对比报告

**步骤 1**：使用 `extract_uncovered.py` 从 after 扫描结果提取未覆盖 API（用法同 Phase 2「解析覆盖率结果」章节），需额外指定 `--iter-phase {N+1}`。

```bash
python {skill_root}/scripts/extract_uncovered.py --subsystem "{子系统名}" --iter-phase {N+1}
```

输出到 `.coverage_data/iter-{N+1}/`：`uncovered_apis_{timestamp}.json` 和 `manual_confirm_{timestamp}.json`。

**步骤 2**：使用 `compare_uncovered.py` 对比 before/after：

```bash
python {skill_root}/scripts/compare_uncovered.py \
    --before .coverage_data/iter-1/uncovered_apis_{before_ts}.json \
    --after  .coverage_data/iter-2/uncovered_apis_{after_ts}.json \
    --before-mc .coverage_data/iter-1/manual_confirm_{before_ts}.json \
    --after-mc  .coverage_data/iter-2/manual_confirm_{after_ts}.json \
    --iter 2
```

脚本输出 `coverage_comparison_{timestamp}.md` 到 `.coverage_data/iter-{N+1}/`（报告格式见 Phase 11 §3 覆盖率总结）。

**迭代数据流**：
```
iter-1/
├── uncovered_apis_{ts1}.json           # Phase 2 before
├── manual_confirm_{ts1}.json           # Phase 2 before
└── (Phase 5 生成的测试文件)

iter-2/
├── uncovered_apis_{ts2}.json           # Phase 10 after
├── manual_confirm_{ts2}.json           # Phase 10 after
└── coverage_comparison_{ts3}.md        # before → after 对比
```

> **注意**：下一轮迭代的 before 数据直接从 APICoverageDetector 的新 Excel 扫描结果读取（`extract_uncovered.py` 直读 Excel），无需手动传递 CSV 文件。

#### 10.5 注意事项

1. **扫描环境**: 确保在正确的 SDK 环境下运行 APICoverageDetector
2. **配置文件**: 根据子系统类型选择正确的配置文件（arkts_config.json 或 c_config.json）
3. **路径设置**: 确保测试路径和 SDK 路径配置正确
4. **结果记录**: 保存覆盖率对比数据，用于后续分析和改进
5. **连续验证**: 对于大型子系统，可以分批次进行覆盖率验证

---

### Flow C: 新增接口覆盖率验证

新增接口模式下，Phase 2 已跳过 before 扫描（覆盖率为 0），Phase 10 仅需执行 after 扫描。

#### 10C.1 执行 after 扫描

环境准备和扫描操作与 Flow B 步骤 10.1 相同（sync → scan → extract），唯一差异：
- `extract_uncovered.py` 使用 `--iter-phase 1`（Flow C 没有 Phase 2 的 before 数据，这是首次迭代）

```bash
python {skill_root}/scripts/extract_uncovered.py --subsystem "{子系统名}" --iter-phase 1
```

#### 10C.2 生成覆盖率报告（生成后，Flow C 专用）

由于没有 before baseline，仅运行 `extract_uncovered.py` 提取 after 数据（无 `compare_uncovered.py` 对比）。

#### 10C.3 注意事项

- **不使用 `compare_uncovered.py`**：Flow C 没有 before uncovered JSON，无法对比
- **不回填 before 数据**：禁止伪造 before 数据（覆盖率为 0 是事实，不应伪造数据文件）
- **覆盖率表中标注"新增接口"**：Phase 10 输出时，"生成前"列标注为"0（新增接口）"

---

### Flow A: 基于用户提供的覆盖率报告验证

用户已提供覆盖率报告，Phase 10 验证为可选项：
- 如果用户要求验证，对比用户报告中的缺失项与新生成的用例覆盖情况
- 如果用户未要求，直接进入 Phase 10（Output）

### 常见覆盖率异常排查

#### 覆盖率无变化
- **症状**：Phase 10 对比显示 0% 改进
- **根因**：生成的测试未实际调用未覆盖的 API
- **修复**：检查测试代码是否正确导入和调用了目标 API
