#!/usr/bin/env python3
"""
query_db.py - XTS 规则数据库查询工具（替代文档里供抄写的 SQL）

设计原则：
1. 把 xts-database-queries.md / xts-keyword-search.md / L0_Crash / L0_Freeze 等
   文档里供 AI 抄写的 SQL，全部封装为函数 —— AI 调用函数即可，不再写 SQL
2. 字段名按真实 schema（probe 校正过），SELECT * + Row factory，杜绝字段脱节
3. 参数化查询（?），防注入、防特殊字符破坏 SQL
4. 返回 list[dict] 结构化数据，JSON 可直接喂给报告生成
5. db 缺失 → 明确报错，不静默返回空

覆盖的查询（对应文档章节）：
  rules              - 关键字/领域/优先级查询（xts-database-queries.md §3.1）
  contacts           - 责任人查询（§3.4）
  commands           - 常用命令（§3.2）
  common-issues      - 常见环境问题（§3.3）
  subsystem-mapping  - 目录→子系统（§3.5）
  technical-rules    - 技术规则（§3.6）
  hypium             - Hypium 版本问题（§3.7）
  so                 - SO 库归属（so-crash-analysis.md）
  issues             - 历史问题（workflow-details.md）
  stats              - 分组统计（§六）

用法：
    python query_db.py rules --keyword "App died"
    python query_db.py rules --domain 元能力
    python query_db.py rules --high
    python query_db.py contacts 元能力
    python query_db.py so libace.z.so
    python query_db.py so --subsystem ArkUI
    python query_db.py stats --by domain
    python query_db.py --list-tables
"""

import os
import sys
import json
import sqlite3
import argparse


def _default_db_path():
    here = os.path.dirname(os.path.abspath(__file__))
    rel = os.path.normpath(os.path.join(here, "..", "data", "xts_rules.db"))
    if os.path.exists(rel):
        return rel
    home = os.path.expanduser("~")
    return os.path.join(home, ".opencode", "skills", "ohos-issue-xts-log-analysis", "data", "xts_rules.db")


def _connect(db_path=None):
    if db_path is None:
        db_path = _default_db_path()
    if not os.path.exists(db_path):
        return None, "db 不存在: {}（xts_rules.db 随包预置，请重新获取 Skill 包或检查部署路径）".format(db_path)
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn, None
    except sqlite3.Error as e:
        return None, "连接 db 失败: {}".format(e)


def _query(table, where_sql="", params=(), db_path=None, order=""):
    conn, err = _connect(db_path)
    if err:
        return {"status": "db_error", "reason": err, "rows": []}
    try:
        cur = conn.cursor()
        sql = "SELECT * FROM {}".format(table)
        if where_sql:
            sql += " WHERE " + where_sql
        if order:
            sql += " ORDER BY " + order
        cur.execute(sql, params)
        rows = [dict(r) for r in cur.fetchall()]
        return {"status": "ok", "table": table, "count": len(rows), "rows": rows}
    except sqlite3.Error as e:
        return {"status": "sql_error", "reason": str(e), "rows": []}
    finally:
        conn.close()


# ============================================================
# rules 表
# ============================================================

def query_rules(keyword=None, domain=None, priority_min=None, priority_max=None, db_path=None):
    conds, params = [], []
    if keyword:
        conds.append("keyword LIKE ?")
        params.append("%{}%".format(keyword))
    if domain:
        conds.append("domain = ?")
        params.append(domain)
    if priority_min is not None:
        conds.append("priority >= ?")
        params.append(int(priority_min))
    if priority_max is not None:
        conds.append("priority < ?")
        params.append(int(priority_max))
    where = " AND ".join(conds) if conds else ""
    return _query("rules", where, tuple(params), db_path, order="priority DESC")


def query_high_priority_rules(db_path=None):
    return query_rules(priority_min=8, db_path=db_path)


def stats_rules_by(field="domain", db_path=None):
    field = field.lower()
    if field not in ("domain", "priority", "severity", "log_type"):
        return {"status": "error", "reason": "不支持的分组字段: {}（可选 domain/priority/severity/log_type）".format(field)}
    conn, err = _connect(db_path)
    if err:
        return {"status": "db_error", "reason": err}
    try:
        cur = conn.cursor()
        cur.execute("SELECT {} AS k, COUNT(*) AS cnt FROM rules GROUP BY {} ORDER BY cnt DESC".format(field, field))
        return {"status": "ok", "by": field, "groups": [{"key": r["k"], "count": r["cnt"]} for r in cur.fetchall()]}
    except sqlite3.Error as e:
        return {"status": "sql_error", "reason": str(e)}
    finally:
        conn.close()


# ============================================================
# contacts 表
# ============================================================

def query_contacts(domain=None, primary_only=False, db_path=None):
    conds, params = [], []
    if domain:
        conds.append("domain = ?")
        params.append(domain)
    if primary_only:
        conds.append("is_primary = 1")
    where = " AND ".join(conds) if conds else ""
    return _query("contacts", where, tuple(params), db_path, order="is_primary DESC")


# ============================================================
# so_mapping 表
# ============================================================

def query_so(so_name=None, subsystem=None, db_path=None):
    conds, params = [], []
    if so_name:
        conds.append("so_name LIKE ?")
        params.append("%{}%".format(so_name))
    if subsystem:
        conds.append("subsystem = ?")
        params.append(subsystem)
    where = " AND ".join(conds) if conds else ""
    return _query("so_mapping", where, tuple(params), db_path)


# ============================================================
# commands / common_issues / subsystem_mapping / technical_rules / hypium_versions
# ============================================================

def query_commands(category=None, match=None, db_path=None):
    conds, params = [], []
    if category:
        conds.append("category = ?")
        params.append(category)
    if match:
        conds.append("(command LIKE ? OR description LIKE ?)")
        params.extend(["%{}%".format(match), "%{}%".format(match)])
    where = " AND ".join(conds) if conds else ""
    return _query("commands", where, tuple(params), db_path, order="category")


def query_common_issues(symptom=None, db_path=None):
    if symptom:
        return _query("common_issues", "symptom LIKE ?", ("%{}%".format(symptom),), db_path)
    return _query("common_issues", db_path=db_path)


def query_subsystem_mapping(directory=None, subsystem=None, db_path=None):
    conds, params = [], []
    if directory:
        conds.append("directory LIKE ?")
        params.append("%{}%".format(directory))
    if subsystem:
        conds.append("subsystem = ?")
        params.append(subsystem)
    where = " AND ".join(conds) if conds else ""
    return _query("subsystem_mapping", where, tuple(params), db_path)


def query_technical_rules(db_path=None):
    return _query("technical_rules", db_path=db_path)


def query_hypium_versions(db_path=None):
    return _query("hypium_versions", db_path=db_path)


# ============================================================
# issues 表（历史问题）
# ============================================================

def query_issues_recent(limit=10, db_path=None):
    conn, err = _connect(db_path)
    if err:
        return {"status": "db_error", "reason": err}
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM issues ORDER BY created_at DESC LIMIT ?", (int(limit),))
        rows = [dict(r) for r in cur.fetchall()]
        return {"status": "ok", "count": len(rows), "rows": rows}
    except sqlite3.Error as e:
        return {"status": "sql_error", "reason": str(e)}
    finally:
        conn.close()


def list_tables(db_path=None):
    conn, err = _connect(db_path)
    if err:
        return {"status": "db_error", "reason": err}
    try:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        names = [r["name"] for r in cur.fetchall()]
        sizes = {}
        for n in names:
            cur.execute("SELECT COUNT(*) AS c FROM {}".format(n))
            sizes[n] = cur.fetchone()["c"]
        return {"status": "ok", "tables": names, "rows_per_table": sizes}
    except sqlite3.Error as e:
        return {"status": "sql_error", "reason": str(e)}
    finally:
        conn.close()


# ============================================================
# CLI
# ============================================================

def _emit(result, fmt):
    if fmt == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    if result.get("status") != "ok":
        print(json.dumps(result, ensure_ascii=False))
        return
    if "tables" in result:
        sizes = result.get("rows_per_table", {})
        for t in result["tables"]:
            print("{:<22} {:>5} 行".format(t, sizes.get(t, 0)))
        return
    rows = result.get("rows") or result.get("groups") or []
    if not rows:
        print("(无记录) " + str(result.get("reason", "")))
        return
    if "groups" in result:
        for g in rows:
            print("{:<6} {}".format(g["count"], g["key"]))
        return
    for i, r in enumerate(rows, 1):
        head = r.get("keyword") or r.get("so_name") or r.get("name") or r.get("command") or r.get("directory") or r.get("title") or list(r.values())[0]
        print("[{}] {}".format(i, head))


def main():
    ap = argparse.ArgumentParser(
        description="XTS 规则数据库查询（替代文档 SQL 抄写）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python query_db.py rules --keyword "App died"
  python query_db.py rules --domain 元能力
  python query_db.py rules --high
  python query_db.py contacts 元能力
  python query_db.py contacts --primary
  python query_db.py so libace.z.so
  python query_db.py so --subsystem ArkUI
  python query_db.py commands 日志管理
  python query_db.py stats --by domain
  python query_db.py --list-tables
        """,
    )
    sub = ap.add_subparsers(dest="cmd")

    p_rules = sub.add_parser("rules", help="查 rules 表")
    p_rules.add_argument("--keyword", "-k")
    p_rules.add_argument("--domain", "-d")
    p_rules.add_argument("--high", action="store_true", help="高优先级 (priority>=8)")
    p_rules.add_argument("--all", action="store_true")
    p_rules.add_argument("--priority-min", type=int)
    p_rules.add_argument("--priority-max", type=int)

    p_ct = sub.add_parser("contacts", help="查 contacts 表")
    p_ct.add_argument("domain", nargs="?")
    p_ct.add_argument("--primary", action="store_true")

    p_so = sub.add_parser("so", help="查 so_mapping 表")
    p_so.add_argument("so_name", nargs="?")
    p_so.add_argument("--subsystem")

    p_cmd = sub.add_parser("commands", help="查 commands 表")
    p_cmd.add_argument("category", nargs="?")
    p_cmd.add_argument("--match", "-m")

    sub.add_parser("common-issues", help="查 common_issues 表").add_argument("symptom", nargs="?")
    sub.add_parser("subsystem", help="查 subsystem_mapping 表").add_argument("directory", nargs="?")
    sub.add_parser("technical", help="查 technical_rules 表")
    sub.add_parser("hypium", help="查 hypium_versions 表")
    p_iss = sub.add_parser("issues", help="查 issues 表")
    p_iss.add_argument("--limit", type=int, default=10)

    p_st = sub.add_parser("stats", help="分组统计")
    p_st.add_argument("--by", choices=["domain", "priority", "severity", "log_type"], default="domain")

    sub.add_parser("list-tables", help="列出所有表及行数")

    ap.add_argument("--format", "-f", choices=["json", "text"], default="text")
    ap.add_argument("--db", help="指定 db 路径")
    args = ap.parse_args()

    db = args.db

    if args.cmd == "rules":
        if args.high:
            r = query_high_priority_rules(db_path=db)
        elif args.all or not (args.keyword or args.domain or args.priority_min):
            r = query_rules(db_path=db)
        else:
            r = query_rules(keyword=args.keyword, domain=args.domain,
                            priority_min=args.priority_min, priority_max=args.priority_max, db_path=db)
    elif args.cmd == "contacts":
        r = query_contacts(domain=args.domain, primary_only=args.primary, db_path=db)
    elif args.cmd == "so":
        r = query_so(so_name=args.so_name, subsystem=args.subsystem, db_path=db)
    elif args.cmd == "commands":
        r = query_commands(category=args.category, match=args.match, db_path=db)
    elif args.cmd == "common-issues":
        r = query_common_issues(symptom=args.symptom, db_path=db)
    elif args.cmd == "subsystem":
        r = query_subsystem_mapping(directory=args.directory, db_path=db)
    elif args.cmd == "technical":
        r = query_technical_rules(db_path=db)
    elif args.cmd == "hypium":
        r = query_hypium_versions(db_path=db)
    elif args.cmd == "issues":
        r = query_issues_recent(limit=args.limit, db_path=db)
    elif args.cmd == "stats":
        r = stats_rules_by(field=args.by, db_path=db)
    elif args.cmd == "list-tables":
        r = list_tables(db_path=db)
    else:
        ap.print_help()
        sys.exit(1)

    _emit(r, args.format)


if __name__ == "__main__":
    main()
