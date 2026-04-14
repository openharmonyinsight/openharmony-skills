#!/usr/bin/env python3
"""XTS Test Code Quality Scanner - R004 Rule Scanner

R004 is the most complex rule (L5 complexity), requiring:
- Recursive function call chain tracking
- Class method extraction
- Cross-file import resolution
- Helper function try-catch defect detection

This module MUST be used for R004 scanning. Manual implementation by the model
is extremely error-prone (historical lesson: v1 had 23,152 false positives).

Source: rules/R004/SKILL.md
Sync rule: Update when rules/R004/SKILL.md technical details change.
"""
import os, re, sys
from common import (
    find_matching_brace, parse_it_blocks, has_assertion,
    _find_try_catch, get_subsystem,
)

IMPORT_CACHE = {}

def collect_function_definitions(content):
    funcs = {}; lines = content.split('\n')
    for i, line in enumerate(lines):
        m = re.search(r'(?:function\s+|static\s+(?:async\s+)?|async\s+function\s+)(\w+)\s*\(', line)
        if m:
            fname = m.group(1)
            ft = '\n'.join(lines[i:])
            bi = ft.find('{', m.end() - m.start())
            if bi == -1: continue
            be = find_matching_brace(ft, bi)
            if be == -1: continue
            funcs[fname] = ft[bi+1:be]; continue
        m = re.search(r'(?:let|const|var)\s+(\w+)\s*(?::\s*[^=]+)?\s*=\s*(?:async\s*)?\([^)]*(?:\([^)]*\)[^)]*)*\)\s*(?:async\s*)?=>', line)
        if m:
            fname = m.group(1)
            ft = '\n'.join(lines[i:])
            bi = ft.find('{', m.end() - 2)
            if bi == -1: continue
            be = find_matching_brace(ft, bi)
            if be == -1: continue
            funcs[fname] = ft[bi+1:be]; continue
        m = re.search(r'(?:let|const|var)\s+(\w+)\s*:', line)
        if m and line.rstrip().endswith('='):
            fname = m.group(1); combined = line
            for j in range(i + 1, min(i + 5, len(lines))):
                combined += ' ' + lines[j].strip()
                m2 = re.search(r'=>', combined)
                if m2:
                    arrow_offset_in_combined = m2.start() + 2
                    ft = '\n'.join(lines[i:])
                    bi = ft.find('{', arrow_offset_in_combined)
                    if bi == -1: break
                    be = find_matching_brace(ft, bi)
                    if be == -1: break
                    funcs[fname] = ft[bi+1:be]; break
                if '{' in lines[j]: break
    return funcs

def get_imported_functions(filepath):
    if filepath in IMPORT_CACHE: return IMPORT_CACHE[filepath]
    if not os.path.exists(filepath): return {}
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f: content = f.read()
    except Exception as e:
        print(f"  [R004] 读取文件失败 {filepath}: {e}", file=sys.stderr)
        return {}
    funcs = collect_function_definitions(content)
    IMPORT_CACHE[filepath] = funcs
    return funcs

def resolve_import_file(import_path, current_filepath):
    if import_path.startswith('./') or import_path.startswith('../'):
        base_dir = os.path.dirname(current_filepath)
        resolved = os.path.normpath(os.path.join(base_dir, import_path))
        for ext in ['.test.ets', '.test.ts', '.ets', '.ts', '.js']:
            if os.path.exists(resolved + ext): return resolved + ext
        if os.path.exists(resolved): return resolved
    return None

def extract_class_methods(content):
    methods = {}; lines = content.split('\n')
    in_class = False; class_indent = 0
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if re.match(r'(?:export\s+)?(?:default\s+)?class\s+\w+', stripped):
            in_class = True; class_indent = len(line) - len(stripped); continue
        if in_class:
            ci = len(line) - len(stripped)
            if stripped.startswith('}') and ci <= class_indent:
                in_class = False; continue
            if ci > class_indent:
                ft = '\n'.join(lines[i:])
                m = re.search(r'static\s+(?:async\s+)?(\w+)\s*\([^)]*(?:\([^)]*\)[^)]*)*\)', stripped)
                if not m:
                    m = re.search(r'(?:async\s+)(\w+)\s*\(', stripped)
                if m:
                    fname = m.group(1)
                    abs_start = m.start() + stripped.find(m.group(0))
                    bi = ft.find('{', abs_start)
                    if bi != -1:
                        be = find_matching_brace(ft, bi)
                        if be != -1:
                            body = ft[bi+1:be]
                            methods[fname] = body
                            inner = collect_function_definitions(body)
                            for k, v in inner.items():
                                if k not in methods: methods[k] = v
    return methods

def check_function_has_assertion(body, local_funcs, all_known_funcs, visited=None, depth=0):
    if visited is None: visited = set()
    if depth > 5: return False
    if has_assertion(body): return True
    for fname, fbody in local_funcs.items():
        key = f"local:{fname}"
        if key in visited: continue
        if not (fname in body and fbody): continue
        visited.add(key)
        if check_function_has_assertion(fbody, local_funcs, all_known_funcs, visited, depth + 1):
            return True
    for fname, fbody in all_known_funcs.items():
        key = f"known:{fname}"
        if key in visited: continue
        if fname in local_funcs: continue
        if not (fname in body and fbody): continue
        visited.add(key)
        if check_function_has_assertion(fbody, {}, all_known_funcs, visited, depth + 1):
            return True
    return False

def _find_try_catch_gaps_in_func(body, local_funcs, all_known_funcs, visited=None, depth=0):
    if visited is None: visited = set()
    if depth > 5: return []
    gaps = []
    tcs = _find_try_catch(body)
    for tb in tcs:
        eff_try = '\n'.join(l for l in tb['try_content'].split('\n') if not l.strip().startswith('//'))
        eff_catch = '\n'.join(l for l in tb['catch_content'].split('\n') if not l.strip().startswith('//')) if tb['catch_content'] else ''
        if not has_assertion(eff_try): gaps.append(('try_missing', tb['try_content']))
        if tb['catch_content'] and not has_assertion(eff_catch): gaps.append(('catch_missing', tb['catch_content']))
        for tl in tb['try_content'].split('\n'):
            if re.match(r'^\s*//\s*(expect\s*\(|assertEqual\s*\(|assertTrue\s*\(|assertFalse\s*\(|assertFail\s*\()', tl):
                gaps.append(('commented_assertion', tl))
    for fname, fbody in local_funcs.items():
        key = f"tc:{fname}"
        if key in visited: continue
        if not (fname in body and fbody): continue
        visited.add(key)
        gaps.extend(_find_try_catch_gaps_in_func(fbody, local_funcs, all_known_funcs, visited, depth + 1))
    for fname, fbody in all_known_funcs.items():
        key = f"tc_k:{fname}"
        if key in visited: continue
        if fname in local_funcs: continue
        if not (fname in body and fbody): continue
        visited.add(key)
        gaps.extend(_find_try_catch_gaps_in_func(fbody, {}, all_known_funcs, visited, depth + 1))
    return gaps

def scan_r004(files, base_dir):
    issues = []
    for fp in files:
        try:
            with open(fp, 'r', encoding='utf-8', errors='ignore') as f: c = f.read()
        except Exception as e:
            print(f"  [R004] 读取文件跳过 {fp}: {e}", file=sys.stderr)
            continue
        if not re.search(r'\bit\s*\(', c): continue
        rel = os.path.relpath(fp, base_dir); ls = c.split('\n')
        local_funcs = collect_function_definitions(c)
        class_methods = extract_class_methods(c)
        local_funcs.update(class_methods)
        imported_funcs = {}
        for m in re.finditer(r'import\s+\{([^}]+)\}\s+from\s+["\'](.+?)["\']', c):
            names = [n.strip() for n in m.group(1).split(',')]
            resolved = resolve_import_file(m.group(2), fp)
            if resolved:
                imported_funcs.update(get_imported_functions(resolved))
        for dm in re.finditer(r'import\s+(\w+)\s+from\s+["\'](.+?)["\']', c):
            resolved = resolve_import_file(dm.group(2), fp)
            if resolved:
                imported_funcs.update(get_imported_functions(resolved))
        reported_gap_keys = set()
        for i, l in enumerate(ls):
            m = re.search(r'\bit(?:\.only|\.skip|\.each)?\s*\(\s*[\'"](.+?)[\'"]\s*,', l)
            if not m: continue
            name = m.group(1); start = i + 1
            rest = '\n'.join(ls[i:])
            ai = rest.find('=>')
            if ai == -1: continue
            bi = rest.find('{', ai)
            if bi == -1: continue
            eb = find_matching_brace(rest, bi)
            if eb == -1: continue
            body = rest[bi+1:eb]
            if has_assertion(body): continue
            tcs = _find_try_catch(body)
            if tcs:
                missing = []
                for tb in tcs:
                    th = has_assertion(tb['try_content']) or check_function_has_assertion(tb['try_content'], local_funcs, imported_funcs)
                    ch = has_assertion(tb['catch_content']) or check_function_has_assertion(tb['catch_content'], local_funcs, imported_funcs) if tb['catch_content'] else True
                    if not th and not ch: missing.append('try和catch块都缺少断言')
                    elif not th: missing.append('try块缺少断言')
                    elif not ch and tb['catch_content']: missing.append('catch块缺少断言')
                if missing:
                    body_via_func = check_function_has_assertion(body, local_funcs, imported_funcs)
                    if not body_via_func:
                        issues.append({'rule':'R004','type':'测试用例缺少断言','severity':'Critical',
                            'file':rel,'line':start,'testcase':name,'snippet':f"it('{name}', ...) 缺少断言",
                            'suggestion':f'路径: {rel}, 行号: {start}, 问题描述: 测试用例缺少断言。检测到try-catch结构，{"；".join(missing)}。',
                            'subsystem':get_subsystem(rel)}); continue
            if check_function_has_assertion(body, local_funcs, imported_funcs):
                tc_gaps = _find_try_catch_gaps_in_func(body, local_funcs, imported_funcs)
                if tc_gaps:
                    gap_parts = []
                    for gt, gc in tc_gaps:
                        gk = (gt, gc[:80])
                        if gk in reported_gap_keys: continue
                        reported_gap_keys.add(gk)
                        if gt == 'try_missing': gap_parts.append('辅助函数的try块缺少有效断言')
                        elif gt == 'catch_missing': gap_parts.append('辅助函数的catch块缺少断言')
                        elif gt == 'commented_assertion': gap_parts.append('辅助函数中存在注释掉的断言')
                    if gap_parts:
                        issues.append({'rule':'R004','type':'辅助函数try-catch断言缺陷','severity':'Warning',
                            'file':rel,'line':start,'testcase':name,'snippet':f"it('{name}', ...) 辅助函数缺陷",
                            'suggestion':f'路径: {rel}, 行号: {start}, 问题描述: 调用的辅助函数存在try-catch断言缺陷。{"；".join(gap_parts)}。',
                            'subsystem':get_subsystem(rel)})
                continue
            issues.append({'rule':'R004','type':'测试用例缺少断言','severity':'Critical',
                'file':rel,'line':start,'testcase':name,'snippet':f"it('{name}', ...) 缺少断言",
                'suggestion':f'路径: {rel}, 行号: {start}, 问题描述: 测试用例缺少断言。请在it()块中添加expect或assert*断言方法。',
                'subsystem':get_subsystem(rel)})
    return issues
