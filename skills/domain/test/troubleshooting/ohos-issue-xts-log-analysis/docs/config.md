# 配置说明

> **ohos-issue-xts-log-analysis** - 配置系统说明

## 配置概述

ohos-issue-xts-log-analysis 支持可选配置，用于启用P0核心功能（源码验证、API→domain链路解析）。

---

## OH_ROOT 路径配置

### ⚠️ 源码根路径解析优先级（2026-07-13新增）

> **设计改进**：解决 OH_ROOT 静态绑定 skill 目录、不同用户路径不同的问题

**优先级链**（从高到低）：

| 优先级 | 来源 | 说明 | 适用场景 |
|--------|------|------|---------|
| ① 最高 | **用户本次输入提供的源码路径** | 用户在分析请求中直接给出源码路径，AI 据此推断 OH_ROOT | 形态④；用户主动提供源码路径 |
| ② | **脚本命令行参数** | `locate_xts_source.py --root` / `map_domain.py --oh-root` | 脚本显式指定 |
| ③ | **脚本 --source-path 推断** | `locate_xts_source.py --source-path` 自动推断根路径 | 用户提供源码路径给脚本 |
| ④ | **配置文件 OH_ROOT** | `.xts-analysis-config.json` 中的 `OH_ROOT` 字段 | 通用默认配置 |
| ⑤ 最低 | **AI 主动提示用户提供** | 以上均无时，AI 提示用户提供源码路径 | 无配置且用户未提供 |

**解析流程**：
```
AI检查用户输入是否含源码路径
    ↓ 含 → 优先使用用户提供的路径（优先级①）
    ↓ 不含
脚本 --root / --oh-root 参数是否指定
    ↓ 指定 → 使用命令行参数（优先级②）
    ↓ 未指定
脚本 --source-path 是否指定
    ↓ 指定 → 自动推断（优先级③）
    ↓ 未指定
读取配置文件 OH_ROOT
    ↓ 存在 → 使用配置（优先级④）
    ↓ 不存在
AI 提示用户提供源码路径（优先级⑤）
```

### 配置文件位置

`ohos-issue-xts-log-analysis/.xts-analysis-config.json`（skill 根目录下）

### 配置格式

```json
{
  "OH_ROOT": "/path/to/openharmony/root"
}
```

### 配置说明

**OH_ROOT**：OpenHarmony 工程根目录的绝对路径

**用途**：
- 源码定位（`locate_xts_source.py`、FailureAndSource.md Step 2.5）
- 关联源码进行深度分析
- 验证 API 调用是否匹配子系统归属
- 解析 API→domain 链路（`map_domain.py`、`extract_imports.py` + `explore_import_chain.py`）

**脚本参数覆盖**：
- `locate_xts_source.py --root <路径>`：覆盖配置文件 OH_ROOT
- `locate_xts_source.py --source-path <源码路径>`：自动推断 OH_ROOT
- `map_domain.py --oh-root <路径>`：覆盖配置文件 OH_ROOT

**效果对比**：

| 源码状态 | 分析质量 | domain来源 | 证据链完整性 | 报告标注 |
|---------|---------|-----------|------------|---------|
| **有源码** | **L0**（完整域驱动切片） | API→domain精确映射 | ✅ 完整证据链 | ✅ "源码→领域证据链完整" |
| **无源码** | **L1**（域切片无源码） | testsuite名推断子系统 | ⚠️ 证据链缺失 | ⚠️ "未提供源码，推断自testsuite" |

---

## 数据库配置

### 数据库位置

`data/xts_rules.db`

### 数据库内容

| 表名 | 记录数 | 用途 |
|------|--------|------|
| rules | 80条 | 定界规则（关键字→领域→解决方案） |
| contacts | 79条 | 责任人信息（内部查询使用） |
| so_mapping | 711条 | SO库映射（库名→子系统） |
| kit_module | 0条 | kit聚合关系（@kit→@ohos模块） |
| module_domain | 10条 | 模块级精确 domain 映射 |
| subsystem_bridge | 9条 | 子系统命名桥接 |

### 数据库验证（强制）

**验证命令**：
```bash
ls ~/.opencode/skills/ohos-issue-xts-log-analysis/data/xts_rules.db
```

**如果数据库不存在**：
```bash
python3 -c "import sqlite3; print("请从备份恢复xts_rules.db")"
```

---

## 配置建议

### 强烈推荐配置

✅ 如有 OpenHarmony 源码权限，**强烈推荐配置 OH_ROOT**

**优势**：
- 启用 P0 核心功能（源码验证、API→domain 链路解析）
- 建立完整证据链，提高定界准确性和可信度
- 提高报告质量

### 无源码时

⚠️ skill 仍可运行（不强制），但质量降级（L0→L1）

**降级处理**：
- 用 testsuite 名推断子系统
- 报告标注降级状态："未提供源码，无法定位具体 API/断言"
- 建议用户提供源码路径或配置 OH_ROOT 以提高准确性

### 多用户环境建议

> 不同用户的 OH_ROOT 不同，建议以下做法之一：

1. **用户输入优先（推荐）**：在分析请求中直接提供源码路径，无需改配置文件
   ```
   # Linux 示例
   请分析 /tmp/xts_logs/xxx，源码路径是 /home/myuser/code/oh/test/xts/acts/ability

   # Windows 示例
   请分析 C:\xts_logs\xxx，源码路径是 C:\Users\myuser\code\oh\test\xts\acts\ability
   ```
2. **各自配置**：编辑 `.xts-analysis-config.json`，填入自己的路径
   ```json
   // Linux
   { "OH_ROOT": "/home/myuser/code/openharmony" }
   // Windows（正斜杠或双反斜杠均可）
   { "OH_ROOT": "C:/Users/myuser/code/openharmony" }
   ```
3. **脚本参数**：通过 `--root` / `--oh-root` / `--source-path` 显式指定
   ```bash
   # Linux
   python3 scripts/locate_xts_source.py --testcase "xxx" --root "/home/myuser/code/oh"
   # Windows (cmd/PowerShell)
   python scripts\locate_xts_source.py --testcase "xxx" --root "C:\Users\myuser\code\oh"
   ```

---

---

**更新时间**：2026-07-29  
**设计理念**：可选配置，不强制源码，降级处理明确；用户输入优先于静态配置
