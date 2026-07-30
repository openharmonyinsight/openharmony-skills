#!/usr/bin/env python3
"""
query_api_path.py - 从API路径查询子系统信息

设计原则：
1. 支持从 api_path_mapping 表查询路径对应的子系统
2. 支持模糊匹配（路径部分匹配）
3. 支持模块名查询（@ohos.xxx 或 xxx.h）

用法：
    python3 query_api_path.py "@ohos.arkui.inspector"
    python3 query_api_path.py "native_api.h"
    python3 query_api_path.py "/interface/sdk_c/arkui/napi/native_api.h"
    python3 query_api_path.py --list-sdk-c
    python3 query_api_path.py --list-sdk-js
"""

import os
import re
import sys
import json
import sqlite3
import argparse

def get_db_path():
    """获取数据库路径"""
    here = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.normpath(os.path.join(here, "..", "data", "xts_rules.db"))
    if os.path.exists(db_path):
        return db_path
    
    home = os.path.expanduser("~")
    return os.path.join(home, ".opencode", "skills", "ohos-issue-xts-log-analysis", "data", "xts_rules.db")

def query_by_exact_path(path: str, db_path: str = None) -> dict:
    """精确路径查询"""
    if db_path is None:
        db_path = get_db_path()
    
    if not os.path.exists(db_path):
        return {"status": "error", "reason": "数据库不存在", "db_path": db_path}
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 标准化路径（去掉前缀 /interface）
    normalized_path = path
    if path.startswith('/interface'):
        normalized_path = path.replace('/interface', '/interface')
    
    cursor.execute('''
        SELECT api_path, subsystem_cn, kit_cn, kit_en, sdk_type, module_name
        FROM api_path_mapping
        WHERE api_path = ?
    ''', (normalized_path,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "status": "found",
            "query_type": "exact_path",
            "input": path,
            "api_path": row[0],
            "subsystem_cn": row[1],
            "kit_cn": row[2],
            "kit_en": row[3],
            "sdk_type": row[4],
            "module_name": row[5]
        }
    
    return {"status": "not_found", "query_type": "exact_path", "input": path}

def query_by_module(module: str, db_path: str = None) -> dict:
    """模块名查询（支持 @ohos.xxx 或 xxx.h）"""
    if db_path is None:
        db_path = get_db_path()
    
    if not os.path.exists(db_path):
        return {"status": "error", "reason": "数据库不存在", "db_path": db_path}
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 查询 module_name 字段
    cursor.execute('''
        SELECT api_path, subsystem_cn, kit_cn, kit_en, sdk_type, module_name
        FROM api_path_mapping
        WHERE module_name = ?
        LIMIT 5
    ''', (module,))
    
    rows = cursor.fetchall()
    
    if rows:
        results = []
        for row in rows:
            results.append({
                "api_path": row[0],
                "subsystem_cn": row[1],
                "kit_cn": row[2],
                "kit_en": row[3],
                "sdk_type": row[4],
                "module_name": row[5]
            })
        
        return {
            "status": "found",
            "query_type": "module_name",
            "input": module,
            "count": len(results),
            "results": results
        }
    
    conn.close()
    
    return {"status": "not_found", "query_type": "module_name", "input": module}

def query_by_fuzzy_path(keyword: str, db_path: str = None) -> dict:
    """模糊路径查询"""
    if db_path is None:
        db_path = get_db_path()
    
    if not os.path.exists(db_path):
        return {"status": "error", "reason": "数据库不存在", "db_path": db_path}
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # LIKE 查询
    cursor.execute('''
        SELECT api_path, subsystem_cn, kit_cn, kit_en, sdk_type, module_name
        FROM api_path_mapping
        WHERE api_path LIKE ?
        LIMIT 20
    ''', (f'%{keyword}%',))
    
    rows = cursor.fetchall()
    
    if rows:
        results = []
        for row in rows:
            results.append({
                "api_path": row[0],
                "subsystem_cn": row[1],
                "kit_cn": row[2],
                "kit_en": row[3],
                "sdk_type": row[4],
                "module_name": row[5]
            })
        
        return {
            "status": "found",
            "query_type": "fuzzy_path",
            "input": keyword,
            "count": len(results),
            "results": results
        }
    
    conn.close()
    
    return {"status": "not_found", "query_type": "fuzzy_path", "input": keyword}

def list_by_sdk_type(sdk_type: str, limit: int = 50, db_path: str = None) -> dict:
    """列出指定类型的API"""
    if db_path is None:
        db_path = get_db_path()
    
    if not os.path.exists(db_path):
        return {"status": "error", "reason": "数据库不存在", "db_path": db_path}
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT api_path, subsystem_cn, kit_cn, kit_en, module_name
        FROM api_path_mapping
        WHERE sdk_type = ?
        ORDER BY subsystem_cn, kit_cn
        LIMIT ?
    ''', (sdk_type, limit))
    
    rows = cursor.fetchall()
    
    # 统计子系统分布
    cursor.execute('''
        SELECT subsystem_cn, COUNT(*) as count
        FROM api_path_mapping
        WHERE sdk_type = ?
        GROUP BY subsystem_cn
        ORDER BY count DESC
    ''', (sdk_type,))
    
    subsystem_stats = cursor.fetchall()
    
    conn.close()
    
    results = []
    for row in rows:
        results.append({
            "api_path": row[0],
            "subsystem_cn": row[1],
            "kit_cn": row[2],
            "kit_en": row[3],
            "module_name": row[4]
        })
    
    return {
        "status": "ok",
        "sdk_type": sdk_type,
        "total_count": len(results),
        "subsystem_distribution": [{"subsystem": s[0], "count": s[1]} for s in subsystem_stats],
        "results": results
    }

def main():
    parser = argparse.ArgumentParser(
        description='从API路径查询子系统信息',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python3 query_api_path.py "@ohos.arkui.inspector"
  python3 query_api_path.py "native_api.h"
  python3 query_api_path.py "/interface/sdk_c/arkui/napi/native_api.h"
  python3 query_api_path.py --list-sdk-c
  python3 query_api_path.py --list-sdk-js
  python3 query_api_path.py --stats
        """
    )
    parser.add_argument('query', nargs='?', help='查询内容（路径/模块名/关键字）')
    parser.add_argument('--db', help='指定数据库路径')
    parser.add_argument('--list-sdk-c', action='store_true', help='列出所有sdk_c接口')
    parser.add_argument('--list-sdk-js', action='store_true', help='列出所有sdk-js接口')
    parser.add_argument('--stats', action='store_true', help='显示统计信息')
    parser.add_argument('--limit', type=int, default=20, help='限制返回数量')
    parser.add_argument('--format', choices=['json', 'text'], default='json', help='输出格式')
    
    args = parser.parse_args()
    
    if args.stats:
        db_path = args.db or get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT sdk_type, COUNT(*) FROM api_path_mapping GROUP BY sdk_type')
        stats = cursor.fetchall()
        
        result = {
            "status": "ok",
            "total": sum(s[1] for s in stats),
            "distribution": [{"sdk_type": s[0], "count": s[1]} for s in stats]
        }
        
        conn.close()
        
    elif args.list_sdk_c:
        result = list_by_sdk_type('sdk_c', args.limit, args.db)
    
    elif args.list_sdk_js:
        result = list_by_sdk_type('sdk-js', args.limit, args.db)
    
    elif args.query:
        # 判断查询类型
        query = args.query
        
        if query.startswith('/interface'):
            # 精确路径查询
            result = query_by_exact_path(query, args.db)
        elif query.startswith('@ohos') or query.endswith('.h'):
            # 模块名查询
            result = query_by_module(query, args.db)
        else:
            # 模糊查询
            result = query_by_fuzzy_path(query, args.db)
    
    else:
        parser.print_help()
        sys.exit(1)
    
    if args.format == 'json':
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if result['status'] == 'found':
            print(f"查询类型: {result['query_type']}")
            print(f"匹配数: {result.get('count', 1)}")
            print("\n结果:")
            for r in result.get('results', [result]):
                print(f"  路径: {r['api_path']}")
                print(f"  子系统: {r['subsystem_cn']}")
                print(f"  Kit: {r['kit_cn']} / {r['kit_en']}")
                print(f"  类型: {r['sdk_type']}")
                if r.get('module_name'):
                    print(f"  模块名: {r['module_name']}")
                print()
        elif result['status'] == 'ok':
            print(f"类型: {result.get('sdk_type', 'stats')}")
            if 'subsystem_distribution' in result:
                print("\n子系统分布:")
                for s in result['subsystem_distribution']:
                    print(f"  {s['subsystem']}: {s['count']} 条")
            print(f"\n总计: {result.get('total', result.get('total_count', 0))} 条")
        else:
            print(f"状态: {result['status']}")
            print(f"输入: {result['input']}")

if __name__ == '__main__':
    main()