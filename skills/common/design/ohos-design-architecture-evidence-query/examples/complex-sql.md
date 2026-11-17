# 复杂 SQL 示例：按子系统聚合部件

这是 **CLI 查询示例**；运行时下载与安装见 `references/usage.md`。

多行 SQL 写入文件，避免 shell 对引号、百分号和换行的二次解释：

```sql
-- 排除 thirdparty，找出部件数大于 8 的子系统
SELECT subsystem, COUNT(*) AS parts
  FROM components
 WHERE subsystem != 'thirdparty'
 GROUP BY subsystem
HAVING parts > 8
 ORDER BY parts DESC, subsystem
 LIMIT 20;
```

```bash
CLI="$HOME/.oskm/oskm-cli.pyz"
DB="$HOME/.oskm/knowledge.db"
python3.12 "$CLI" --db "$DB" sql --file examples/query-parts-by-subsystem.sql
```

返回的 `rows` 随当前快照变化；判断查询是否完整看 `row_count` 与 `truncated`，
不要把某一次结果当成产品常量。`sql` 只接受只读 `SELECT`/`WITH`，表名走白名单，
并自动注入当前 `scan_id` 与 `LIMIT`。

## 对比时的前置条件

跨库对比需要两个真实 DB：

```bash
python3.12 "$CLI" --db older.db --db newer.db diff --entity components
```

同库跨快照需要库里至少有两个扫描。先用 `ask list_scans` 确认有效 scan ID，再执行：

```bash
python3.12 "$CLI" --db "$DB" diff --entity gn_args --scan-a <id-a> --scan-b <id-b>
```

没有第二个快照时，不要把“全部删除”当成架构变化；那是输入不满足对比前置条件。
