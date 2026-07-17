# 子系统桥接表说明

## 概述

子系统桥接表（`subsystem_bridge`）用于解决三套互不对齐的子系统命名问题，建立英文名 ↔ 中文名 ↔ 现有DB粗类的映射关系。

## 三套命名体系异构问题

### 问题背景

在 XTS 测试问题分析中，存在三套互不对齐的子系统命名：

| 来源 | 命名风格 | 示例 | 粒度 |
|------|----------|------|------|
| `log_domains.cpp`（OS权威） | **英文+粗** | "TestSystem", "Ace", "AAFwk", "JSConsole" | 基础domain，一个名字覆盖子域 |
| `kit.json`（SDK权威） | **中文+细** | "测试框架", "ArkUI开发框架", "元能力" | 按模块精确 |
| 现有DB的 `rules.domain`/`contacts` | **中文+粗分类** | "元能力", "ArkUI", "测试框架", "包管理" | 7个粗类，仅80条规则 |

### 对齐难点

1. **命名风格不同**：英文 vs 中文
2. **粒度不同**：粗分类 vs 模块级精确
3. **子域偏移**：一个英文名覆盖多个子域（如 TestSystem 包含 UiTest/PerfTest/TestHelper）
4. **自动模糊匹配不可靠**："Ace" ≠ "ArkUI" 字面，无法自动匹配

### 对齐策略

**策略①**：用 `domain & 0xFFFFFF00` 归约到基础域匹配注册表
- 示例：`0xD003120` → `0xD003100` → 匹配 "TestSystem"

**策略②**：中文↔英文建立人工 curated 桥接表
- 原因：自动模糊匹配不可靠（如 "Ace" ≠ "ArkUI"）
- 方案：人工校对，建立权威桥接表

## 桥接表结构

**数据库表**：`subsystem_bridge`

**表结构**：
```sql
CREATE TABLE subsystem_bridge (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  domain_en     TEXT NOT NULL,   -- 英文domain名（如 'Ace'）
  subsystem_cn  TEXT NOT NULL,   -- 中文子系统名（如 'ArkUI开发框架'）
  rules_domain  TEXT,            -- 现有DB粗类（如 'ArkUI'）
  description   TEXT,            -- 说明
  created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**记录数**：9条（初始数据）

## 桥接表数据

| domain_en | subsystem_cn | rules_domain | 说明 |
|-----------|--------------|--------------|------|
| TestSystem | 测试框架 | 测试框架 | 测试系统domain，覆盖UiTest/PerfTest/TestHelper |
| Ace | ArkUI | ArkUI | ArkUI开发框架，英文"Ace"≠中文"ArkUI"字面 |
| AAFwk | 元能力 | 元能力 | Ability框架 |
| JSConsole | ArkUI | ArkUI | JS控制台，归属于ArkUI子系统 |
| Hilog | DFX | 测试框架 | 日志系统，现有DB归类为"测试框架" |
| MultiMedia | 多媒体 | 多媒体 | 多媒体框架 |
| Notification | 通知 | 通知 | 通知框架 |
| Account | 账号 | 账号 | 账号管理 |
| Graphics | 图形 | 图形 | 图形渲染 |

## 使用方式

### 1. 从 domain_en 查 subsystem_cn

**场景**：从 log_domains.cpp 的英文名定位中文子系统

```bash
# 查询示例
python3 -c "
import sqlite3
conn = sqlite3.connect('data/xts_rules.db')
cursor = conn.cursor()
cursor.execute(\"SELECT subsystem_cn FROM subsystem_bridge WHERE domain_en='Ace'\")
print(cursor.fetchone()[0])  # 输出：ArkUI
conn.close()
"
```

### 2. 从 subsystem_cn 查 rules_domain

**场景**：从 kit.json 的中文子系统名映射到现有DB的粗类

```bash
# 查询示例
python3 -c "
import sqlite3
conn = sqlite3.connect('data/xts_rules.db')
cursor = conn.cursor()
cursor.execute(\"SELECT rules_domain FROM subsystem_bridge WHERE subsystem_cn='测试框架'\")
print(cursor.fetchone()[0])  # 输出：测试框架
conn.close()
"
```

### 3. 从 rules_domain 查所有相关 subsystem_cn

**场景**：查询现有DB粗类对应的所有中文子系统

```bash
# 查询示例
python3 -c "
import sqlite3
conn = sqlite3.connect('data/xts_rules.db')
cursor = conn.cursor()
cursor.execute(\"SELECT domain_en, subsystem_cn FROM subsystem_bridge WHERE rules_domain='ArkUI'\")
for row in cursor.fetchall():
    print(row)  # 输出：('Ace', 'ArkUI'), ('JSConsole', 'ArkUI')
conn.close()
"
```

## 数据维护

### 新增子系统映射

当发现新的子系统命名差异时，需人工校对并新增映射：

```bash
# 新增示例
python3 -c "
import sqlite3
conn = sqlite3.connect('data/xts_rules.db')
cursor = conn.cursor()
cursor.execute(\"INSERT INTO subsystem_bridge (domain_en, subsystem_cn, rules_domain, description) VALUES ('NewDomain', '新子系统', '粗分类', '说明')\")
conn.commit()
conn.close()
"
```

### 更新现有映射

当子系统命名发生变化时，需更新桥接表：

```bash
# 更新示例
python3 -c "
import sqlite3
conn = sqlite3.connect('data/xts_rules.db')
cursor = conn.cursor()
cursor.execute(\"UPDATE subsystem_bridge SET subsystem_cn='更新后的中文' WHERE domain_en='Ace'\")
conn.commit()
conn.close()
"
```

## 证据链中的作用

在"源码→领域证据链"中，桥接表用于：

```
模块 → 中文子系统      ← module_domain 表（精确）
    │ '@ohos.UiTest' → "测试框架"
    ▼
子系统 → hilog domain   ← subsystem_bridge 表（桥接）
    │ "TestSystem" → "测试框架" → 映射到现有DB粗类
    ▼
精准日志过滤 + 定界分析
```

**示例证据链**：
```markdown
**源码→领域证据链**：
- 失败 API 源自 @ohos.UiTest → subsystem=测试框架 → domain=0xD003100
- 通过 subsystem_bridge 映射：TestSystem(英文) → 测试框架(中文) → 测试框架(DB粗类)
- 故过滤域含 0xD003100，定界为"测试框架"
```

## 人工校对要点

### 为什么需要人工校对

- **Ace ≠ ArkUI**：字面不匹配，自动模糊匹配不可靠
- **JSConsole → ArkUI**：归属关系需人工确认
- **Hilog → DFX vs 测试框架**：不同来源的分类不一致，需统一

### 校对原则

1. **OS权威优先**：log_domains.cpp 的英文名为OS权威注册
2. **SDK权威次之**：kit.json 的中文子系统名为SDK权威定义
3. **现有DB兼容**：rules_domain 必须与现有DB的粗类对齐
4. **人工最终判定**：不一致时由人工最终判定归属

## 数据来源

**domain_en**：`/base/hiviewdfx/hilog/services/hilogd/log_domains.cpp`
- `g_DomainList` 静态表中的英文名

**subsystem_cn**：`/interface/sdk-js/build-tools/dts_parser/kit.json`
- `kitName` + `subSystem` 中文字段

**rules_domain**：`data/xts_rules.db` 的 `rules` 表
- 现有DB的7个粗类（测试框架/元能力/包管理/窗口/锁屏/应用问题/待分析）

---

**更新时间**：2026-07-02
**数据来源**：IMPROVEMENT_PLAN.md + log_domains.cpp + kit.json
**数据库位置**：data/xts_rules.db（subsystem_bridge 表）
**记录数**：9条（初始数据，需持续补充）