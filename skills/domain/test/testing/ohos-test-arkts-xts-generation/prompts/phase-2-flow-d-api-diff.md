## Phase 2 Flow D: API 变更驱动模式（基于 d.ts diff）

---

### 📚 参考文档（按需查阅）

本 Phase 执行过程中可参考以下文件，遇到具体问题时按需查阅：

| 文件 | 内容 | 何时查阅 |
|------|------|---------|
| `{skill_root}/references/api_change_design_rules.md` | 21 种 statusCode → 测试类型映射、增量消费细则 | Phase 4 设计时必读（本 Phase 仅产出数据） |
| `{OH_ROOT}/interface/sdk-js/build-tools/api_diff` | api_diff 工具源码（内置调用路径用到） | 内置调用报错时排查 |

---

### ⚙️ 按需加载

本 Flow 不需要额外加载模块。核心工具为 `scripts/parse_api_diff.py`。

---

**前置条件**：Phase 1 已判定 Flow = D（用户提供了 d.ts diff 报告，或要求基于 old/new 两版 .d.ts 做变更分析，关键词含「d.ts diff」「API 变更」「兼容性变更」等）。

**核心目标**：将 api_diff 产出的变更清单，转换为标准的 `uncovered_apis.json`（每个 API 附带 `change_info`），后续 Phase 3-11 完全复用，无需任何特殊处理。

**关键说明**：
- Flow D **跳过 APICoverageDetector 扫描**（变更来源是 diff，不是覆盖率扫描）
- Flow D **不需要 before baseline**：变更本身就是「需要测什么」的输入（类比 Flow C）
- Phase 10 仅执行 after 扫描；覆盖率报告中「生成前」列标注「N 条变更驱动」

---

### 步骤 1：确认 diff 输入来源

向用户确认（或从 Phase 1 参数中读取）以下四者之一：

| 输入路径 | 触发条件 | 需要的参数 | 是否需 OH_ROOT |
|---------|---------|-----------|--------------|
| **路径 A：用户已有 diff 报告** | 用户提供了 api_diff 产出的 JSON 文件 | `diff_report_path` | 否 |
| **路径 B：两个 SDK 目录** | 用户提供了 old/new 两版 .d.ts 目录 | `old_dts_dir`、`new_dts_dir` | 是（定位工具） |
| **路径 C：PR**（推荐，开发提测场景） | 用户提供了 PR 号或 merge commit | `pr`（如 `34064` / `af59f9f4c`） | 是（git worktree 导出） |
| **路径 D：两个 tag**（版本盘点场景） | 用户提供了两个版本 tag | `tag`（如 `TagA,TagB`） | 是（git worktree 导出） |

**路径 C/D 原理**：api_diff 工具基于完整 `.d.ts` 文件解析语法树对比（非 git 文本 diff），脚本自动用 `git worktree` 从 `{OH_ROOT}/interface/sdk-js` 导出对应 ref 的 `api/` 目录，再喂给工具。PR 模式取 `PR^1`（合并前）vs `PR`（合并后）。

**若四种都未提供**：向用户询问——「请提供 PR 号 / 两个 tag / api_diff 报告 / old+new 两版 SDK 目录」。无法获取则无法继续 Flow D，建议改用 Flow B。

---

### 步骤 2：执行 parse_api_diff.py

#### 路径 A：用户提供 diff 报告

```bash
python {skill_root}/scripts/parse_api_diff.py \
  --diff-report <用户提供的 JSON 路径> \
  --dts-file <可选：限定分析的 d.ts，如 @ohos.UiTest.d.ts> \
  --kit <可选> \
  --subsystem <可选> \
  --iter-phase 1 \
  --task-subsystem <子系统> --task-module <模块>
```

#### 路径 B：两个 SDK 目录

> 工具位于 `{OH_ROOT}/interface/sdk-js/build-tools/api_diff`，脚本会自动 `npm install`（首次）。目录需含 `api/` 子目录（工具会扫描 `{dir}/api/*.d.ts`）。

```bash
python {skill_root}/scripts/parse_api_diff.py \
  --old <old_sdk 目录，需含 api/ 子目录> \
  --new <new_sdk 目录，需含 api/ 子目录> \
  --dts-file <可选> \
  --iter-phase 1 \
  --task-subsystem <子系统> --task-module <模块>
```

#### 路径 C：PR（推荐——开发改 .d.ts 通过 PR 提交，测试 SE 拿此 PR 补测）

```bash
# 用 PR 号（脚本自动查 merge commit）
python {skill_root}/scripts/parse_api_diff.py --pr '!34064' --dts-file <可选> --iter-phase 1

# 或直接用 merge commit hash
python {skill_root}/scripts/parse_api_diff.py --pr af59f9f4c --dts-file <可选> --iter-phase 1
```

脚本自动完成：查 merge commit → worktree 导出 `PR^1`（base）和 `PR`（head）的 `api/` → 跑 api_diff → 解析。耗时与 PR 改动文件数相关（全量 `api/` 扫描约 15-20 秒）。

#### 路径 D：两个 tag（版本盘点——SDK 版本升级时对比两个 Release）

```bash
python {skill_root}/scripts/parse_api_diff.py \
  --tag OpenHarmony-v5.1.0-Release,OpenHarmony-v6.0-Release \
  --dts-file <可选，强烈推荐加以限定范围，如 @ohos.hilog> \
  --iter-phase 1
```

> **性能提示**：两 tag 全量对比会产出数千条变更（如 5.1→6.0 有 6670 条）。务必用 `--dts-file` 或 `--kit` 限定到本次需求涉及的文件/Kit，避免下游 Phase 处理过量数据。

**内置调用（路径 B/C/D）失败时的处理**：
- `OH_ROOT not configured`：提示用户在 `.oh-xts-config.json` 配置 `OH_ROOT`，或改用路径 A（提供 diff 报告）
- `api_diff entry not found`：`OH_ROOT` 下不存在 api_diff 工具，请改用路径 A
- `SDK repo not found` / `not a git worktree`：`{OH_ROOT}/interface/sdk-js` 不可用，请改用路径 A 或 B
- `PR !N not found`：PR 号在 merge commit message 中未匹配到，请确认 PR 号或改用 commit hash
- `npm install` 失败：网络问题，建议手动在 api_diff 目录执行或改用路径 A
- 工具执行超时：api_diff 全量约 15-20 秒；超过 2 分钟建议加 `--dts-file` 限定范围

---

### 步骤 3：解析脚本输出

脚本会在最后两行输出：
1. 摘要（保留的变更数、按 change_type 分类统计）
2. 输出文件路径（`uncovered_apis_<timestamp>.json`）

**捕获输出文件路径**，作为 Phase 3 的输入。

#### 输出结构（标准格式 + change_info 扩展）

```json
{
  "ets1.1": {
    "methods": [
      {
        "module": "@ohos.UiTest", "class": "By", "method": "text",
        "type": "Method", "func": "text(txt: string | number, ...): By;",
        "kit": "Test", "file_path": "api/@ohos.UiTest.d.ts", ...
        "coverage": { "call": {"status":"未覆盖"}, "param": {"status":"未覆盖"}, ... },
        "change_info": {
          "statusCode": 16, "change_type": "FUNCTION_CHANGES",
          "risk_level": "HIGH",
          "old_message": "...", "new_message": "...",
          "incremental": { "new_param_types": ["number"] }
        }
      }
    ],
    "interfaces": [...], "properties": [...]
  },
  "metadata": { "source": "api_diff (Flow D)", "summary": {...} }
}
```

#### 风险分级汇总（向用户报告）

脚本已按 statusCode 输出分类统计。向用户汇报时使用风险分级口径：

| 风险等级 | 对应 statusCode | 含义 |
|---------|----------------|------|
| 🔴 高 | 0,1,2,14,15,16 | 删除类 / 类型变更 / 函数签名变更 |
| 🟡 中 | 6,7,10,11,12 | 错误码 / 权限变更 |
| 🟢 低 | 3,4,5,8,9,13,18-22 | 新增 / 兼容性变更 |

**删除类（0/1/2）**：在报告中单独提示——「N 个 API 已删除，不会生成测试，请人工确认现有用例是否引用了已删除 API（这部分不在本 skill 职责内，可由 code-quality 类 skill 检查）」。

---

### 步骤 4：代码风格扫描（与 Flow A/C 一致）

1. 快速扫描 3-5 个目标测试目录下的现有测试文件
2. 提取代码风格：导入顺序、describe/it 结构、断言方法、错误处理模式

---

### 输出总览

| 维度 | Flow D 输出 |
|------|------------|
| 未覆盖 API 列表 | `.coverage_data/iter-1/uncovered_apis_<timestamp>.json`（含 `change_info`） |
| 覆盖率缺口列表 | 由 statusCode 驱动（HIGH=删除/签名变更，MEDIUM=错误码/权限，LOW=新增/兼容） |
| before baseline | **无**（变更驱动，类比 Flow C） |
| 代码风格总结 | 有 |

**关键说明**：Flow D 的下游（Phase 3-11）**完全复用**，Phase 3 解析时读取 `change_info` 作为补充信息，Phase 4 设计时按 `references/api_change_design_rules.md` 消费 `change_info.incremental`，其余 Phase 无感知。
