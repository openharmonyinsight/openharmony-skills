# 数据库表结构说明

## 目录

- 数据库版本管理 ⭐ **新增**
  - db_version 表（版本历史）
- 核心表结构
  - rules 表（定界规则）
  - contacts 表（责任人信息）
  - so_mapping 表（SO库映射）
  - issues 表（历史问题记录）
  - subsystem_mapping 表（子系统目录映射）
  - 其他辅助表
- 新增表结构（改进计划新增）
  - kit_module 表（kit聚合关系）
  - module_domain 表（模块级精确domain映射）
  - subsystem_bridge 表（子系统命名桥接）
- 数据统计
- 查询示例

---

本文档详细说明XTS问题分析skill使用的数据库表结构。

**数据库路径**：`~/.opencode/skills/ohos-issue-xts-log-analysis/data/xts_rules.db`

**当前版本**：v3.0（2026-07-02）

---

## 数据库版本管理 ⭐ **新增**

### db_version 表（版本历史）

记录数据库版本演进历史，用于版本追踪和回溯。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INTEGER | 主键（自增） |
| version | TEXT | 版本号（如"v3.0"） |
| description | TEXT | 版本描述 |
| changes | TEXT | 变更内容 |
| created_at | TIMESTAMP | 创建时间 |
| updated_by | TEXT | 更新人 |

**当前版本历史**：

| 版本 | 描述 | 变更内容 | 时间 |
|------|------|---------|------|
| **v3.0** | 异常状态识别增强 | 新增10条异常状态规则，支持testsuite/testcase级别异常提取 | 2026-07-02 |
| **v2.0** | kit_module扩充 | 新增kit_module表（546条记录），支持@kit聚合关系 | 2026-06-20 |
| **v1.0** | 初始版本 | 基础规则表创建：rules, contacts, so_mapping, subsystem_mapping | 2025-01-01 |

**版本查询命令**：
```bash
# 查询当前版本
python3 -c "
import sqlite3, os
conn = sqlite3.connect(os.path.expanduser('~/.opencode/skills/ohos-issue-xts-log-analysis/data/xts_rules.db'))
cursor = conn.cursor()
cursor.execute('SELECT version, description, created_at FROM db_version ORDER BY id DESC LIMIT 1')
print(cursor.fetchone())
conn.close()
"
```

**版本升级脚本**：
```bash
# 升级到最新版本（如果版本落后）
python3 data/init_db.py --upgrade
```

---

## 核心表结构

### rules 表（定界规则）

用于存储问题关键字匹配规则。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INTEGER | 主键（自增） |
| keyword | TEXT | 匹配关键字（如 "App died"） |
| domain | TEXT | 问题领域（如 "元能力"） |
| problem_type | TEXT | 问题类型（如 "应用闪退"） |
| problem_category | TEXT | 问题分类 |
| solution | TEXT | 解决方案 |
| priority | INTEGER | 匹配优先级（越大越优先，默认0） |
| log_type | TEXT | 日志类型（默认task.log） |
| check_order | INTEGER | 检查顺序 |
| example | TEXT | 示例 |
| rule_id | TEXT | 规则ID |
| severity | TEXT | 严重程度（默认Critical） |
| enabled | INTEGER | 是否启用（默认1） |
| created_at | TIMESTAMP | 创建时间 |

**关键字段说明**：
- `keyword`：日志中匹配的关键字，如"App died"、"Blocked"、"SIGSEGV"
- `domain`：问题所属领域，如"元能力"、"测试框架"、"窗口"等
- `priority`：匹配优先级，数值越大优先级越高（10=最高）

---

### contacts 表（责任人信息）

存储各领域的问题责任人。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INTEGER | 主键（自增） |
| domain | TEXT | 问题领域 |
| name | TEXT | 负责人姓名 |
| zhanma | TEXT | 责任人詹码（如00839045） |
| weixin | TEXT | 微信号 |
| email | TEXT | 邮箱 |
| responsibility | TEXT | 责任描述 |
| is_primary | INTEGER | 是否主要负责人（1=主要，0=次要） |
| created_at | TIMESTAMP | 创建时间 |

**关键字段说明**：
- `is_primary`：主要责任人标记，用于推荐首要联系人

---

### so_mapping 表（SO库映射）

存储SO库名与子系统/责任人的映射关系。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INTEGER | 主键（自增） |
| so_name | TEXT | SO库名称（如 libace.z.so） |
| subsystem | TEXT | 所属子系统（如 ArkUI、元能力） |
| description | TEXT | SO库说明 |
| owner_name | TEXT | 责任人姓名 |
| owner_zhanma | TEXT | 责任人詹码 |
| created_at | TIMESTAMP | 创建时间 |

**关键字段说明**：
- `so_name`：崩溃栈中的SO库名，用于定界crash问题
- 当前包含**711个SO库映射**，覆盖**23个子系统**

---

### issues 表（历史问题记录）

记录历史分析的问题，用于追溯和学习。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INTEGER | 主键（自增） |
| title | TEXT | 问题标题 |
| log_dir | TEXT | 日志目录路径 |
| log_content | TEXT | 日志内容 |
| matched_keywords | TEXT | 匹配到的关键字（JSON格式） |
| domain | TEXT | 定界领域 |
| problem_type | TEXT | 问题类型 |
| problem_category | TEXT | 问题分类 |
| conclusion | TEXT | 定界结论 |
| solution | TEXT | 解决方案 |
| confidence | INTEGER | 定界置信度 |
| status | TEXT | 状态（open/resolved） |
| contact_name | TEXT | 转交负责人姓名 |
| contact_zhanma | TEXT | 转交负责人詹码 |
| created_at | TIMESTAMP | 创建时间 |
| resolved_at | TIMESTAMP | 解决时间 |

---

### subsystem_mapping 表（子系统目录映射）

存储测试目录与子系统的映射关系。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INTEGER | 主键（自增） |
| directory | TEXT | 测试目录名 |
| subsystem | TEXT | 所属子系统 |
| is_inferred | INTEGER | 是否推断 |
| notes | TEXT | 备注 |
| created_at | TIMESTAMP | 创建时间 |

---

### 其他辅助表

#### common_issues 表（常见问题）
存储常见问题分类和解决方案。

**清理说明**：2026-07-02 已清理，只保留能基于日志定位的 symptom（环境/配置问题）。当前7条记录。

#### commands 表（常用命令）
存储XTS测试相关的常用命令。

#### technical_rules 表（技术规则）
存储代码编写技术规范。

---

## 新增表结构（改进计划新增）

### kit_module 表（kit聚合关系）

存储 kit 与 @ohos 模块的聚合关系。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INTEGER | 主键（自增） |
| kit_name | TEXT | kit名称（如 'TestKit', 'ArkUI', 'AbilityKit'） |
| module_name | TEXT | @ohos模块名（如 '@ohos.UiTest', '@ohos.display'） |
| subsystem_cn | TEXT | 中文子系统名（如 '测试框架', 'ArkUI开发框架', '元能力'） |
| created_at | TIMESTAMP | 创建时间 |

**数据来源**：从 `/interface/sdk-js/kits/@kit.*.d.ts` 解析import语句自动填充。

**关键字段说明**：
- `kit_name`：kit名称，对应 @kit.X 语法中的 X
- `module_name`：被聚合的 @ohos 模块名，用于源码→领域链路解析
- 当前包含**546条记录**，覆盖**48个kit**和**300+个@ohos模块**

**示例数据**：
```sql
-- TestKit 聚合关系
INSERT INTO kit_module (kit_name, module_name, subsystem_cn) VALUES 
('TestKit', '@ohos.UiTest', '测试框架'),
('TestKit', '@ohos.test.PerfTest', '测试框架'),
('TestKit', '@ohos.app.ability.abilityDelegatorRegistry', '测试框架');

-- ArkUI 聚合关系
INSERT INTO kit_module (kit_name, module_name, subsystem_cn) VALUES 
('ArkUI', '@ohos.display', 'ArkUI开发框架'),
('ArkUI', '@ohos.arkui.componentSnapshot', 'ArkUI开发框架'),
('ArkUI', '@ohos.window', 'ArkUI开发框架');
```

---

### module_domain 表（模块级精确domain映射）

存储 @ohos 模块到 hilog domain 的精确映射关系（模块级精度）。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INTEGER | 主键（自增） |
| module_name | TEXT | @ohos模块名（如 '@ohos.UiTest'） |
| domain_hex | TEXT | domain完整十六进制（如 '0xD003100'） |
| short_hex | TEXT | domain短格式（如 '00310'，日志实际打印5位） |
| subsystem_cn | TEXT | 中文子系统名（如 '测试框架'） |
| tag_example | TEXT | 标签示例（如 'UiTestKit'） |
| description | TEXT | 模块说明 |
| created_at | TIMESTAMP | 创建时间 |

**数据来源**：`/base/hiviewdfx/hilog/services/hilogd/log_domains.cpp` + 源码 `*_LOG_DOMAIN` 定义 + 人工校对。

**关键字段说明**：
- `domain_hex`：完整的domain值（含0xD0前缀），用于精准过滤
- `short_hex`：短格式（低20位），对应日志中的打印格式
- `module_name`：精确到模块级，如 UiTest=0xD003100、PerfTest=0xD003120
- 当前包含**10条记录**，覆盖核心子系统

**示例数据**：
```sql
INSERT INTO module_domain (module_name, domain_hex, short_hex, subsystem_cn, tag_example) VALUES 
('@ohos.UiTest', '0xD003100', '00310', '测试框架', 'UiTestKit'),
('@ohos.test.PerfTest', '0xD003120', '00312', '测试框架', 'PerfTest'),
('@ohos.display', '0xD003900', '0039X', 'ArkUI', 'Display'),
('@ohos.app.ability.*', '0xD001300', '0013X', '元能力', 'AAFwk');
```

---

### subsystem_bridge 表（子系统命名桥接）

存储三套子系统命名体系的桥接关系。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INTEGER | 主键（自增） |
| domain_en | TEXT | 英文domain名（来自log_domains.cpp，如 'Ace', 'AAFwk'） |
| subsystem_cn | TEXT | 中文子系统名（来自kit.json，如 'ArkUI开发框架', '元能力'） |
| rules_domain | TEXT | 现有DB粗类（来自rules表，如 'ArkUI', '元能力'） |
| description | TEXT | 桥接说明 |
| created_at | TIMESTAMP | 创建时间 |

**数据来源**：log_domains.cpp英文名 + kit.json中文名 + 人工curated桥接。

**关键字段说明**：
- `domain_en`：log_domains.cpp中的英文domain名（粗粒度）
- `subsystem_cn`：kit.json中的中文子系统名（细粒度）
- `rules_domain`：现有rules表的domain字段（粗分类）
- 当前包含**9条记录**，解决三套命名异构对齐难点

**示例数据**：
```sql
INSERT INTO subsystem_bridge (domain_en, subsystem_cn, rules_domain) VALUES 
('Ace', 'ArkUI开发框架', 'ArkUI'),
('AAFwk', '元能力', '元能力'),
('TestSystem', '测试框架', '测试框架');
```

---

## 数据统计

**当前数据库统计**：
- rules: 80条定界规则
- contacts: 79个责任人（包含PM和接口人）
- so_mapping: 711个SO库映射（23个子系统）
- subsystem_mapping: 76个目录映射
- common_issues: 7个常见问题（环境/配置问题，已清理）
- commands: 21条常用命令
- technical_rules: 6条技术规范
- **kit_module: 546条kit聚合关系**（新增）
- **module_domain: 10条模块级精确domain映射**（新增）
- **subsystem_bridge: 9条子系统命名桥接**（新增）

---

## 查询示例

```bash
# 查看表结构
sqlite3 ~/.opencode/skills/ohos-issue-xts-log-analysis/data/xts_rules.db ".schema rules"

# 查看所有领域
sqlite3 ~/.opencode/skills/ohos-issue-xts-log-analysis/data/xts_rules.db "SELECT DISTINCT domain FROM rules ORDER BY domain;"

# 查看高优先级规则
sqlite3 ~/.opencode/skills/ohos-issue-xts-log-analysis/data/xts_rules.db "SELECT keyword, domain, problem_type FROM rules WHERE priority >= 8 ORDER BY priority DESC;"

# 查看SO库子系统分布
sqlite3 ~/.opencode/skills/ohos-issue-xts-log-analysis/data/xts_rules.db "SELECT subsystem, COUNT(*) FROM so_mapping GROUP BY subsystem ORDER BY COUNT(*) DESC LIMIT 10;"

# 查看kit聚合关系（新增）
sqlite3 ~/.opencode/skills/ohos-issue-xts-log-analysis/data/xts_rules.db "SELECT kit_name, COUNT(*) as module_count FROM kit_module GROUP BY kit_name ORDER BY COUNT(*) DESC LIMIT 10;"

# 查看模块级domain映射（新增）
sqlite3 ~/.opencode/skills/ohos-issue-xts-log-analysis/data/xts_rules.db "SELECT module_name, domain_hex, subsystem_cn FROM module_domain LIMIT 10;"
```

---

**更新时间**：2026-07-02  
**数据库版本**：v3.0（新增三表）
