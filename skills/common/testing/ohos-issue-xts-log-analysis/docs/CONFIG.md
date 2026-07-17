# 配置说明

> **xts-issue-analysis** - 配置系统说明

## 配置概述

xts-issue-analysis 支持可选配置，用于启用P0核心功能（源码验证、API→domain链路解析）。

---

## OH_ROOT 路径配置（可选）

### 配置文件位置

`.opencode/skills/xts-issue-analysis/.xts-analysis-config.json`

### 配置格式

```json
{
  "OH_ROOT": "/path/to/openharmony/root"
}
```

### 配置说明

**OH_ROOT**：OpenHarmony 工程根目录的绝对路径

**用途**：
- 关联源码进行深度分析
- 验证 API 调用是否匹配子系统归属
- 解析 API→domain 链路

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
ls ~/.opencode/skills/xts-issue-analysis/data/xts_rules.db
```

**如果数据库不存在**：
```bash
python3 data/init_db.py
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

---

## 配置优先级（未来扩展）

> 📖 **配置驱动设计**：支持子系统定制化配置

**配置层级**（计划实现）：

| 层级 | 文件 | 说明 |
|------|------|------|
| **核心配置** | `references/configs/_common.md` | 核心规范（数据库规则、报告格式） |
| **子系统配置** | `references/configs/{Subsystem}/_common.md` | 子系统特有规则（domain映射、关键字规则） |
| **模块配置** | `references/configs/{Subsystem}/{Module}.md` | 模块特有规则（API→domain映射） |

**配置优先级**：
```
用户自定义配置 > 模块配置 > 子系统配置 > 核心配置
```

---

**更新时间**：2026-07-03  
**设计理念**：可选配置，不强制源码，降级处理明确