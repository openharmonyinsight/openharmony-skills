# 开发环境预检参考文档

> 本文档供 Team Lead（SKILL.md Phase 0）调用，包含 Agent Teams 模式的环境检查清单、检查方法和自动修复流程。

## 检查清单总览

| # | 检查项 | 关键性 | 自动修复 |
|---|--------|--------|----------|
| 0.1 | Agent Teams 环境变量 | 阻断 | 是 |
| 0.2 | Agent 定义文件完整性 | 阻断 | 否 |
| 0.3 | Reference 文件完整性 | 阻断 | 否 |
| 0.4 | 编译分析脚本可用性 | 阻断 | 部分（权限） |
| 0.5 | Claude Code 版本 | 阻断 | 否 |

---

## 0.1 Agent Teams 环境变量

### 检查

```bash
echo $CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS
```

预期值：`1`

### 自动修复流程（未通过时执行）

1. Read `~/.claude/settings.json`
2. 解析 JSON，定位 `env` 对象
   - 如果 `env` 不存在，在顶层创建 `"env": {}`
3. 在 `env` 中添加或更新：`"CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"`
4. Write 回 `~/.claude/settings.json`（保持原有 JSON 缩进格式）
5. 向用户报告：
   ```
   已自动配置 CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1。
   需要重启 Claude Code 会话使配置生效（执行 /exit 后重新启动）。
   ```
6. **停止流程** — 因为当前会话中环境变量不会立即生效，必须等用户重启后重新触发。

### 修复示例

修复前的 `settings.json`：
```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "xxx"
  },
  "model": "opus"
}
```

修复后：
```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "xxx",
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  },
  "model": "opus"
}
```

---

## 0.2 Agent 定义文件完整性

### 检查

确认以下 4 个文件全部存在且 size > 0（相对于 SKILL.md 所在目录的 `agents/` 子目录）：

| 文件 | 角色 |
|------|------|
| `agents/requirements-analysis.md` | Teammate #1: 需求分析专家 |
| `agents/arkweb-coder.md` | Teammate #2: 代码实现工程师 |
| `agents/arkweb-reviewer.md` | Teammate #3: 代码检视工程师 |
| `agents/arkweb-builder.md` | Teammate #4: 编译验证工程师 |

### 检查方法

对每个文件执行 Glob + Read，确认存在且内容非空。

### 处理

- 缺失 → 停止流程，报告缺失文件列表
- 空文件 → 停止流程，报告空文件列表

---

## 0.3 Reference 文件完整性

### 检查

确认以下 3 个参考文件存在（相对于 SKILL.md 所在目录的 `reference/` 子目录）：

| 文件 | 用途 |
|------|------|
| `reference/design-conformance-check.md` | Phase 2 设计遵从性检查 |
| `reference/design-diff-alignment.md` | Phase 7 设计差异对齐 |
| `reference/build-verification.md` | Phase 8 编译验证 |

### 处理

- 缺失 → 停止流程，报告缺失文件列表

---

## 0.4 编译分析脚本可用性

### 检查

确认 `scripts/analyze_build_error.sh`（相对于 SKILL.md 所在目录）存在且具有执行权限。

### 检查方法

```bash
ls -la {skill_dir}/scripts/analyze_build_error.sh
```

### 处理

| 状态 | 处理 |
|------|------|
| 文件不存在 | 停止流程，报告缺失 |
| 文件存在但无执行权限 | 执行 `chmod +x` 修复，报告已修复 |
| 正常 | PASS |

---

## 0.5 Claude Code 版本

### 检查

```bash
claude --version 2>/dev/null
```

### 要求

版本 >= 2.1.x（Agent Teams 功能在此版本引入）。

### 处理

- 满足 → PASS
- 不满足 → 停止流程，建议用户升级 Claude Code

---

## 输出格式

全部检查完成后，输出格式：

```
═══════════════════════════════════════════
  Phase 0: 开发环境预检
═══════════════════════════════════════════
  0.1 Agent Teams 环境变量    ✅
  0.2 Agent 定义文件 (4/4)    ✅
  0.3 Reference 文件 (3/3)    ✅
  0.4 编译分析脚本            ✅
  0.5 Claude Code 版本        ✅ (vX.Y.Z)
═══════════════════════════════════════════
  结论: PASS → 进入 Phase 1
═══════════════════════════════════════════
```

FAIL 时：

```
═══════════════════════════════════════════
  Phase 0: 开发环境预检
═══════════════════════════════════════════
  0.1 Agent Teams 环境变量    ❌ (未设置，已自动修复 settings.json)
  0.2 Agent 定义文件 (3/4)    ❌ (缺失: agents/arkweb-builder.md)
  ...
═══════════════════════════════════════════
  结论: FAIL — 阻断原因:
    - 环境变量已修复，需重启会话后重新执行
    - 缺失 Agent 定义文件，请检查 skill 安装
═══════════════════════════════════════════
```
