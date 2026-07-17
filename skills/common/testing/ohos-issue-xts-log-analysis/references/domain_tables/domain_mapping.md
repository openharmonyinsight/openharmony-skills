# Domain 映射关系总结

## 概述

本文档总结 XTS 测试问题分析中的 domain 映射关系，包括：
- 模块→精确 domain 映射（模块级精度）
- 子系统命名桥接（英文名 ↔ 中文名 ↔ 现有DB粗类）
- kit→模块聚合关系

## 三套命名体系对齐难点

存在**三套互不对齐的子系统命名**：

| 来源 | 命名风格 | 示例 | 粒度 |
|------|----------|------|------|
| `log_domains.cpp`（OS权威） | **英文+粗** | "TestSystem", "Ace", "AAFwk", "JSConsole" | 基础domain，一个名字覆盖子域 |
| `kit.json`（SDK权威） | **中文+细** | "测试框架", "ArkUI开发框架", "元能力" | 按模块精确 |
| 现有DB的 `rules.domain`/`contacts` | **中文+粗分类** | "元能力", "ArkUI", "测试框架", "包管理" | 7个粗类，仅80条规则 |

且 domain 存在**子域偏移**：`0xD003100`(UiTest核心)、`0xD003120`(PerfTest)、`0xD003130`(TestHelper) 都属于 "TestSystem"，但注册表只精确列出基础值。

**对齐策略**：
① 用 `domain & 0xFFFFFF00` 归约到基础域匹配注册表
② 中文↔英文建立人工 curated 桥接表（自动模糊匹配不可靠）

## 模块→精确 Domain 映射表

**数据来源**：
- `/base/hiviewdfx/hilog/services/hilogd/log_domains.cpp`（OS权威）
- 源码 `*_LOG_DOMAIN` 定义
- 人工校对

| 模块名 | domain_hex | short_hex | 子系统 | 标签示例 | 说明 |
|--------|------------|-----------|--------|----------|------|
| @ohos.UiTest | 0xD003100 | 00310 | 测试框架 | UiTestKit | UiTest核心框架 |
| @ohos.test.PerfTest | 0xD003120 | 00312 | 测试框架 | PerfTest | 性能测试框架 |
| @ohos.test.TestHelper | 0xD003130 | 00313 | 测试框架 | TestHelper | 测试辅助工具 |
| @ohos.display | 0xD003900 | 0039X | ArkUI | Display | 显示管理 |
| @ohos.app.ability.* | 0xD001300 | 0013X | 元能力 | AAFwk | Ability框架 |
| @ohos.hilog | 0xD002D00 | 002dX | DFX | Hilog | 日志系统 |
| @ohos.multimedia.* | 0xD002B00 | 002bX | 多媒体 | MultiMedia | 多媒体框架 |
| @ohos.notification.* | 0xD001200 | 0012X | 通知 | Notification | 通知框架 |
| @ohos.account.* | 0xD001B00 | 001bX | 账号 | Account | 账号管理 |
| @ohos.graphics.* | 0xD001400 | 0014X | 图形 | Graphics | 图形渲染 |

**数据库表**：`module_domain`（10条记录）

## 子系统命名桥接表

**英 domain 名 ↔ 中文子系统 ↔ 现有 DB 粗类**

| domain_en | subsystem_cn | rules_domain | 说明 |
|-----------|--------------|--------------|------|
| TestSystem | 测试框架 | 测试框架 | 测试系统domain |
| Ace | ArkUI | ArkUI | ArkUI开发框架 |
| AAFwk | 元能力 | 元能力 | Ability框架 |
| JSConsole | ArkUI | ArkUI | JS控制台 |
| Hilog | DFX | 测试框架 | 日志系统 |
| MultiMedia | 多媒体 | 多媒体 | 多媒体框架 |
| Notification | 通知 | 通知 | 通知框架 |
| Account | 账号 | 账号 | 账号管理 |
| Graphics | 图形 | 图形 | 图形渲染 |

**数据库表**：`subsystem_bridge`（9条记录）

## Kit→模块聚合关系

**数据来源**：`/interface/sdk-js/kits/@kit.*.d.ts`（49个kit文件）

**聚合示例**：
- `@kit.TestKit` 聚合 `@ohos.UiTest`、`@ohos.test.PerfTest`、`@ohos.test.TestHelper`
- `@kit.ArkUI` 聚合 `@ohos.display`、`@ohos.animator`、`@ohos.picture`

**数据库表**：`kit_module`（待填充）

## Domain 过滤命令速查

| 子系统 | domain (full) | 日志打印 | 过滤命令 |
|--------|---------------|----------|----------|
| UiTest / UiTestKit / TestKit | 0xD003100 | C00310/UiTestKit | `hilog -D 0xD003100` 或 grep `C0031[0-9a-f]{2}/` |
| PerfTest | 0xD003120 | C00312/… | `hilog -D 0xD003120` |
| TestHelper | 0xD003130 | C00313/… | `hilog -D 0xD003130` |
| ArkUI (ACE) | 0xD003900 | C0039xx/… | `hilog -D 0xD003900` |
| Ability / AAFwk | 0xD001300 | C0013xx/… | `hilog -D 0xD001300` |
| AbilityBase | 0xD001305 | C001305/… | `hilog -D 0xD001305` |
| hilog / DFX | 0xD002D00 | C002dxx/… | `hilog -D 0xD002D00` |
| XTS acts runner | 0xD005D00 | C005dxx/… | `hilog -D 0xD005D00` |
| JSConsole | 0xD003B00 | C003bxx/… | `hilog -D 0xD003B00` |
| MultiMedia | 0xD002B00 | C002bxx/… | `hilog -D 0xD002B00` |
| Notification | 0xD001200 | C0012xx/… | `hilog -D 0xD001200` |
| Account | 0xD001B00 | C001bxx/… | `hilog -D 0xD001B00` |
| Graphics | 0xD001400 | C0014xx/… | `hilog -D 0xD001400` |

**过滤规则**：
- 日志打印的是低 20 位（5 hex），格式：`Cddddd/TAG: msg`
- 过滤时需补回 `0xD0` 前缀
- 使用正则：`grep -E 'Cddddd/'`（5位短domain）

## 数据链路示例

**完整证据链**：

```
失败用例源码(.ets)
    │ import {Driver, ON} from '@kit.TestKit'
    ▼
@kit → @ohos 模块      ← kit_module 表
    │ '@kit.TestKit' 聚合 '@ohos.UiTest'
    ▼
模块 → 中文子系统      ← module_domain 表
    │ '@ohos.UiTest' → "测试框架"(0xD003100)
    ▼
子系统 → hilog domain   ← subsystem_bridge 表
    │ "TestSystem" → 0xD003100(标签UiTestKit)
    ▼
精准日志过滤  grep -E 'C0031[0-9a-f]{2}/'
    ▼
结合失败断言源码做根因分析
```

## 数据库查询示例

```bash
# 查询模块的 domain
python3 -c "
import sqlite3
conn = sqlite3.connect('data/xts_rules.db')
cursor = conn.cursor()
cursor.execute(\"SELECT module_name, domain_hex, subsystem_cn FROM module_domain WHERE module_name LIKE '%UiTest%'\")
print(cursor.fetchall())
conn.close()
"

# 查询子系统桥接
python3 -c "
import sqlite3
conn = sqlite3.connect('data/xts_rules.db')
cursor = conn.cursor()
cursor.execute(\"SELECT domain_en, subsystem_cn FROM subsystem_bridge WHERE subsystem_cn='测试框架'\")
print(cursor.fetchall())
conn.close()
"
```

---

**更新时间**：2026-07-02
**数据来源**：IMPROVEMENT_PLAN.md 附录 + log_domains.cpp + kit.json
**数据库位置**：data/xts_rules.db（kit_module/module_domain/subsystem_bridge 三表）