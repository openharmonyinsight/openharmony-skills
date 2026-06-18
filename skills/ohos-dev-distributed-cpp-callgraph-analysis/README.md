# OpenHarmony C++ Callgraph Analysis Skill

This skill is registered as `ohos-dev-distributed-cpp-callgraph-analysis`:

```text
skills/ohos-dev-distributed-cpp-callgraph-analysis/
```

## Scope

Use this skill for cross-subsystem OpenHarmony C++ call-chain completeness analysis. It provides an evidence workflow for direct calls, virtual dispatch, callbacks, IPC, generated code, and dynamically loaded implementations.

## Architecture

```text
ohos-dev-distributed-cpp-callgraph-analysis Skill

Agent / Reviewer
  ↓
定义分析目标
(entry / groupId / displayId / IPC / callback / dlopen 等)
  ↓
优先使用 MCP / LSP 主路径
  ↓
Codex / Claude / 其它 MCP Client
  ↓
mcp-language-server
(MCP stdio bridge)
  ↓
clangd
  ↓
仓级 compile_commands.json
(从产品级 compile_commands.json 过滤)
  ↓
OpenHarmony C++ 源码
  ↓
definition / references / call hierarchy / hover / diagnostics
  ↓
证据表
  ↓
修改覆盖矩阵
  ↓
结论
Complete / Incomplete / Not provable
```

```text
可选 fallback 路径

LSP 不可用 / 证据有缺口 / 需要 artifact 佐证
  ↓
ohos_callgraph.py
  ↓
LLVM bitcode .o
  ↓
候选 direct / vtable / dlopen 边
  ↓
补充到证据表

注意：
helper 输出只是候选证据
不能单独证明调用链完整
不能单独证明 groupId / displayId 参数传递
```

```text
关键原则

LSP / source evidence 优先
  ↓
helper 只做候选发现
  ↓
IPC / callback / virtual dispatch / dlopen
  ↓
必须结合源码、符号、构建或运行时证据
  ↓
再给 Complete / Incomplete / Not provable 结论
```

## Runtime Files

- `SKILL.md` is the agent entry point.
- `ohos_callgraph.py` is an optional candidate-edge discovery helper. Its output is not completeness proof.
- `scripts/setup_lsp.py` prepares a repository-scoped clangd MCP service for supported agent clients.
- `evals/` contains seed prompts and expected behaviors for skill evaluation.
- `tests/` contains helper regression tests.

## Verification

Run:

```bash
python3 -m unittest discover \
  -s skills/ohos-dev-distributed-cpp-callgraph-analysis/tests \
  -p 'test_*.py'
```
