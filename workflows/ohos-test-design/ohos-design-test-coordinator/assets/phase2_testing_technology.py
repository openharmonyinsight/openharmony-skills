#!/usr/bin/env python3
"""Phase2 Testing Technology Engine - Unified Testing Design Techniques

Techniques:
1. boundary_value - Boundary Value Analysis
2. equivalence_class - Equivalence Class Partitioning
3. decision_table - Decision Table Testing
4. factor_combination - Factor Combination (Pairwise)

Main Usage (Phase2 Pre-processing):
  python phase2_testing_technology.py --technique generate_all --requirement requirement_analysis.md --output testing_technology.json

Dependencies: allpairspy (optional, only for factor_combination; 'pip install allpairspy' if pairwise coverage is needed; degrades to skipped if absent)
Stability: All outputs are DETERMINISTIC (no randomness)
"""

import argparse
import json
import os
import re
import sys
import traceback
from typing import Dict, List, Optional


_PAIRWISE_INSTALL_HINT = "pip install allpairspy"


def _load_pairwise():
    """Lazily resolve allpairspy.AllPairs. Never auto-installs and never touches
    the network or the user environment at import time. Returns (callable, True)
    on success or (None, False) when absent; callers must record a 'skipped'
    status so downstream gate checks can decide whether to continue.
    """
    try:
        from allpairspy import AllPairs
        return AllPairs, True
    except ImportError:
        return None, False


def _probe_optional_deps() -> bool:
    """Startup probe for optional dependencies. Prints a warning to stderr
    when allpairspy is absent — pairwise (factor_combination) coverage
    degrades to 'skipped'. Never auto-installs, never touches the network,
    and never fails; allpairspy is optional. Called after argparse so that
    --help exits cleanly without side effects.
    """
    try:
        _, available = _load_pairwise()
    except Exception:
        available = False
    if not available:
        sys.stderr.write(
            "[WARN] allpairspy not found — pairwise (factor_combination) "
            "coverage will degrade to 'skipped'. Install with: "
            f"{_PAIRWISE_INSTALL_HINT}\n"
        )
    return available


def _read_file(path: str) -> str:
    path = os.path.normpath(os.path.abspath(path))
    if not os.path.isfile(path):
        return ""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(path, 'r', encoding='utf-8-sig') as f:
                return f.read()
        except Exception:
            return ""
    except Exception:
        return ""


def _write_json(data: Dict, output_path: str) -> bool:
    try:
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.isdir(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Failed to write: {str(e)}")
        return False


def _safe_regex_search(pattern: str, content: str, flags: int = 0) -> Optional[re.Match]:
    try:
        return re.search(pattern, content, flags)
    except re.error:
        return None


def _safe_regex_findall(pattern: str, content: str, flags: int = 0) -> List:
    try:
        return re.findall(pattern, content, flags)
    except re.error:
        return []


def _extract_unit_section(req_content: str, unit_id: str) -> str:
    patterns = [
        rf'## [\d]+\.\s+{re.escape(unit_id)}[：:]',
        rf'## [\d]+\.\s+{re.escape(unit_id)}\s',
        rf'## [\d]+\.\s*主单元\s*\[{re.escape(unit_id)}\]',
        rf'### [\d.]+\s+{re.escape(unit_id)}[：:]',
        rf'### [\d.]+\s+{re.escape(unit_id)}：',
        rf'### {re.escape(unit_id)}[：:]',
        rf'#### {re.escape(unit_id)}[：:]',
        rf'#### {re.escape(unit_id)}：',
        rf'## {re.escape(unit_id)}[：:]',
        rf'#### {re.escape(unit_id)}[（(]',
    ]

    unit_start = -1
    matched_level = 0
    for pattern in patterns:
        match = _safe_regex_search(pattern, req_content)
        if match:
            unit_start = match.start()
            if pattern.startswith(rf'## [\d]+'):
                matched_level = 2
            elif pattern.startswith(rf'###'):
                matched_level = 3
            elif pattern.startswith(rf'####'):
                matched_level = 4
            break

    if unit_start == -1:
        return ""

    unit_end = len(req_content)
    if matched_level == 2:
        pos = req_content.find('\n## ', unit_start + 50)
        if pos != -1:
            unit_end = pos
    elif matched_level == 3:
        pos = req_content.find('\n## ', unit_start + 50)
        if pos != -1 and pos < unit_end:
            unit_end = pos
        pos = req_content.find('\n### ', unit_start + 50)
        if pos != -1 and pos < unit_end:
            unit_end = pos
    elif matched_level == 4:
        pos = req_content.find('\n## ', unit_start + 50)
        if pos != -1 and pos < unit_end:
            unit_end = pos
        pos = req_content.find('\n### ', unit_start + 50)
        if pos != -1 and pos < unit_end:
            unit_end = pos
        pos = req_content.find('\n#### ', unit_start + 50)
        if pos != -1 and pos < unit_end:
            unit_end = pos

    return req_content[unit_start:unit_end]


def _keyword_present(text: str, keyword: str) -> bool:
    """关键词是否在非否定语境中出现。

    遍历关键词所有出现位置，若存在某次出现其前3字符内不含否定词(无/不/非/未/没)，
    则视为真实提及；全部出现均被否定修饰则返回False。
    避免"不涉及权限""无安全关键词"等否定语境误触发风险分级。
    """
    for m in re.finditer(re.escape(keyword), text):
        prefix = text[max(0, m.start() - 3):m.start()]
        if not any(neg in prefix for neg in '无不非未没'):
            return True
    return False


def _get_unit_risk_level(unit_content: str) -> str:
    # 1) 表格中以 P0/P1/P2 作为单元格值（风险分级表、AC优先级表等，格式无关）
    if _safe_regex_search(r'\|\s*P0\s*\|', unit_content):
        return 'P0'
    if _safe_regex_search(r'\|\s*P1\s*\|', unit_content):
        return 'P1'
    if _safe_regex_search(r'\|\s*P2\s*\|', unit_content):
        return 'P2'
    # 2) 显式优先级标签（散文中的"优先级：P0"/"级别：P0"等，避免裸P0字样误判）
    if _safe_regex_search(r'(?:优先级|级别|风险)[：:]\s*P0', unit_content):
        return 'P0'
    if _safe_regex_search(r'(?:优先级|级别|风险)[：:]\s*P1', unit_content):
        return 'P1'
    # 3) 关键词推断：涉及安全/权限/崩溃/数据完整性/沙箱 → P0；重要功能/状态转换/生命周期 → P1
    #    否定守卫：关键词前3字符内含 无/不/非/未/没 视为否定语境(如"不涉及权限""无安全")，不触发
    p0_keywords = ['安全', '权限', '崩溃', '数据完整性', '沙箱', '越权', '攻击', '隔离', '路径遍历', 'AbortError', 'NotSupportedError']
    p1_keywords = ['状态转换', '生命周期', '重要功能', 'destroy', '流式', '并发', '清理']
    for kw in p0_keywords:
        if _keyword_present(unit_content, kw):
            return 'P0'
    for kw in p1_keywords:
        if _keyword_present(unit_content, kw):
            return 'P1'
    return 'P2'


def generate_all(requirement_path: str, output_path: str) -> Dict:
    """Generate all testing technology data for Phase2"""
    req_content = _read_file(requirement_path)
    if not req_content:
        result = {"status": "error", "message": f"File not found: {requirement_path}", "techniques": {}}
        _write_json(result, output_path)
        return result

    units = _extract_all_units(req_content)
    if not units:
        result = {"status": "error", "message": "No main units found", "techniques": {}}
        _write_json(result, output_path)
        return result

    techniques_data = {
        "boundary_value": {},
        "equivalence_class": {},
        "decision_table": {},
        "factor_combination": {}
    }

    for unit in units:
        unit_id = unit["unit_id"]
        risk_level = unit["risk_level"]
        orth_type = unit["orthogonal_type"]
        has_cond = unit["has_cond"]
        has_br = unit["has_br"]

        unit_content = _extract_unit_section(req_content, unit_id)

        if has_cond:
            conditions = _extract_boundary_conditions(unit_content, req_content)
            boundary_testpoints = []
            for cond in conditions:
                # 参数来源判断：InnerApi参数不生成边界值测试点
                if cond.get("source") == "§API变更分析":
                    # 注：若该参数所属API为InnerApi，应在Phase1过滤
                    # 此处仅跳过来源标注为API但条件类型为"直接参数"的InnerApi残留
                    if cond.get("cond_type") == "直接参数":
                        continue  # 跳过InnerApi参数的边界值测试

                # 条件类型判断：仅用户可控参数生成边界值
                # "直接参数"需进一步判断来源（InnerApi已在上面跳过）
                # "上下文条件"需判断是否外部可触发
                # 此处保守处理：上下文条件生成边界值（由Agent判断可触发性）

                boundary_values = _calculate_boundary_values(cond)
                selected_values = _apply_boundary_risk_depth(boundary_values, risk_level)
                for val in selected_values:
                    boundary_testpoints.append({
                        "id": f"BV-{unit_id}-{len(boundary_testpoints)+1:03d}",
                        "cond_id": cond.get("cond_id", ""),
                        "parameter": cond.get("parameter", ""),
                        "value": val["value"],
                        "value_type": val["type"],
                        "expected": _infer_boundary_expected(val["type"]),
                        "risk_level": _map_boundary_risk(val["type"])
                    })
            techniques_data["boundary_value"][unit_id] = {
                "testpoints": boundary_testpoints, "risk_level": risk_level, "total": len(boundary_testpoints)
            }

        if has_cond:
            conditions = _extract_equivalence_conditions(unit_content, req_content)
            equivalence_testpoints = []
            for cond in conditions:
                # 参数来源判断：InnerApi参数不生成等价类测试点（同边界值逻辑）
                if cond.get("source") == "§API变更分析":
                    if cond.get("cond_type") == "直接参数":
                        continue  # 跳过InnerApi参数

                equivalence_classes = _classify_equivalence_classes(cond)
                selected_values = _select_equivalence_values(equivalence_classes, risk_level)
                for val in selected_values:
                    equivalence_testpoints.append({
                        "id": f"EQ-{unit_id}-{len(equivalence_testpoints)+1:03d}",
                        "cond_id": cond.get("cond_id", ""),
                        "parameter": cond.get("parameter", ""),
                        "value": val["value"],
                        "class_type": val["class_type"],
                        "description": val["description"],
                        "expected": _infer_equivalence_expected(val["class_type"]),
                        "risk_level": _map_equivalence_risk(val["class_type"])
                    })
            techniques_data["equivalence_class"][unit_id] = {
                "testpoints": equivalence_testpoints, "risk_level": risk_level, "total": len(equivalence_testpoints)
            }

        if has_br:
            business_rules = _extract_business_rules(unit_content, req_content)
            if business_rules:
                conditions_set = _build_decision_conditions(business_rules)
                truth_table = _generate_truth_table(conditions_set)
                decision_testpoints = []
                for i, truth_row in enumerate(truth_table):
                    action = _map_rule_to_action(truth_row, business_rules, conditions_set)
                    decision_testpoints.append({
                        "id": f"DT-{unit_id}-{i+1:03d}",
                        "conditions": dict(zip(conditions_set, truth_row)),
                        "expected_action": action,
                        "risk_level": _map_decision_risk(truth_row, business_rules)
                    })
                selected_testpoints = _apply_decision_risk_depth(decision_testpoints, risk_level)
                techniques_data["decision_table"][unit_id] = {
                    "testpoints": selected_testpoints, "conditions_count": len(conditions_set),
                    "rules_count": len(business_rules), "risk_level": risk_level, "total": len(selected_testpoints)
                }

        if orth_type == "非正交":
            factors = _extract_factors_internal(unit_content, req_content, unit_id)
            if factors:
                strength_map = {'P0': 3, 'P1': 2, 'P2': 2, 'P3': 1}
                strength = strength_map.get(risk_level, 2)
                if len(factors) < 2:
                    strength = 1
                elif len(factors) < 3 and strength == 3:
                    strength = 2

                factor_values = [[v for v in f['values']] for f in factors]
                factor_names = [f['name'] for f in factors]

                AllPairs, pairwise_ok = _load_pairwise()
                if pairwise_ok and AllPairs is not None:
                    try:
                        pairs = AllPairs(factor_values, n=strength)
                        combinations = []
                        for i, row in enumerate(pairs, 1):
                            comb_values = {}
                            for j, name in enumerate(factor_names):
                                comb_values[name] = row[j]
                            combinations.append({"id": f"COMB-{unit_id}-{i:03d}", "values": comb_values})
                        techniques_data["factor_combination"][unit_id] = {
                            "combinations": combinations, "strength": strength,
                            "risk_level": risk_level, "total": len(combinations)
                        }
                    except Exception as e:
                        techniques_data["factor_combination"][unit_id] = {
                            "status": "skipped", "coverage": "pairwise=skipped",
                            "reason": f"AllPairs failed: {e}; install with: {_PAIRWISE_INSTALL_HINT}",
                            "risk_level": risk_level
                        }
                else:
                    techniques_data["factor_combination"][unit_id] = {
                        "status": "skipped", "coverage": "pairwise=skipped",
                        "reason": f"allpairspy not installed; install with: {_PAIRWISE_INSTALL_HINT}",
                        "risk_level": risk_level
                    }

    result = {
        "status": "success",
        "technique": "generate_all",
        "units": units,
        "techniques": techniques_data,
        "trigger_rules": {
            "boundary_value": "has_cond",
            "equivalence_class": "has_cond",
            "decision_table": "has_br",
            "factor_combination": "orthogonal_type=非正交"
        },
        "algorithm": "确定性算法（无随机性）",
        "stability": "相同输入产生相同输出",
        "dependencies": ["allpairspy (optional, factor_combination only; skipped if absent)"],
        "total_units": len(units)
    }

    _write_json(result, output_path)
    return result


def _extract_all_units(req_content: str) -> List[Dict]:
    units = []
    unit_patterns = [
        r'#### (US-\d+|US-[A-Z]+\d+-\d+|TR-\d+|MU-\d+)[：:]',
        r'### [\d.]+\s+(US-\d+|US-[A-Z]+\d+-\d+|TR-\d+|MU-\d+)[：:]',
        r'### [\d]+\.\s+(US-\d+|TR-\d+|MU-\d+)[：:]',
        r'### (US-\d+|TR-\d+|MU-\d+)[：:]',
        r'## [\d]+\.\s*主单元\s*\[(US-\d+|TR-\d+|MU-\d+)\]',
        r'## [\d]+\.\s+(US-\d+|TR-\d+|MU-\d+)[：:]',
        r'## [\d]+\.\s+(US-\d+|TR-\d+|MU-\d+)\s',
    ]

    for pattern in unit_patterns:
        matches = _safe_regex_findall(pattern, req_content, re.MULTILINE)
        if matches:
            for match in matches:
                if isinstance(match, tuple):
                    unit_id = match[0] if match[0] and match[0].startswith(('US-', 'TR-', 'MU-')) else (match[1] if len(match) > 1 else "")
                else:
                    unit_id = match
                if not unit_id:
                    continue
                unit_content = _extract_unit_section(req_content, unit_id)
                risk_level = _get_unit_risk_level(unit_content)

                orth_type = "未判定"
                orth_patterns = [
                    r'\*\*正交判定\*\*[：:]\s*(正交|非正交|混合型)',
                    r'正交判定[：:]\s*(正交|非正交|混合型)',
                    r'\*正交判定\*[：:]\s*(正交|非正交|混合型)',
                ]
                for op in orth_patterns:
                    orth_match = _safe_regex_search(op, unit_content)
                    if orth_match:
                        orth_type = orth_match.group(1)
                        break

                # 检查主单元章节是否引用COND（从§2.1全局规格表引用）
                has_cond_patterns = [
                    r'涉及条件[：:]\s*COND-\d+',
                    r'涉及参数[：:]\s*COND-\d+',
                    r'输入条件[：:]\s*COND-\d+',
                    r'\*?\*?涉及条件\*?\*?[：:]',
                    r'COND-\d+\([^)]+\)',
                    r'COND-\d+[，,\s]',
                ]
                has_cond = False
                for cp in has_cond_patterns:
                    if _safe_regex_search(cp, unit_content):
                        has_cond = True
                        break

                # 检查主单元章节是否引用BR（业务规则）
                has_br_patterns = [
                    r'关联规则[：:]\s*BR-\d+',
                    r'业务规则[：:]\s*BR-\d+',
                    r'\*?\*?关联规则\*?\*?[：:]',
                    r'BR-\d+\([^)]+\)',
                    r'BR-\d+[，,\s]',
                ]
                has_br = False
                for bp in has_br_patterns:
                    if _safe_regex_search(bp, unit_content):
                        has_br = True
                        break

                units.append({"unit_id": unit_id, "risk_level": risk_level,
                             "orthogonal_type": orth_type, "has_cond": has_cond, "has_br": has_br})
            break

    return units


def _parse_cond_row(req_content: str) -> List[Dict]:
    """解析§2.1输入条件规格表（9列：条件ID|条件名称|数据类型|取值范围|必填可选|枚举值|默认值|条件类型|来源）

    返回富条件字典，含 value_range(取值范围) 与 enum_values(枚举值) 与 source(来源)，供边界/等价类计算使用。
    兼容3列简表（兜底取第3列为constraint）。
    """
    conditions = []
    seen = set()
    # 9列标准格式
    for m in re.finditer(r'^\| (COND-[A-Z0-9]+) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|', req_content, re.MULTILINE):
        cond_id = m.group(1)
        if cond_id in seen:
            continue
        seen.add(cond_id)
        parameter = m.group(2).strip()
        data_type = m.group(3).strip()
        value_range = m.group(4).strip()
        required = m.group(5).strip()
        enum_values = m.group(6).strip()
        default_val = m.group(7).strip()
        cond_type = m.group(8).strip()
        source = m.group(9).strip()
        # constraint 优先取值范围，为空时退回枚举值，再为空时退回数据类型
        constraint = value_range if value_range and value_range not in ['—', '-', ''] else (enum_values if enum_values and enum_values not in ['—', '-', ''] else data_type)
        conditions.append({
            "cond_id": cond_id, "parameter": parameter, "data_type": data_type,
            "value_range": value_range, "enum_values": enum_values, "default": default_val,
            "required": required, "constraint": constraint, "type": _infer_param_type(constraint, data_type),
            "cond_type": cond_type, "source": source
        })
    # 兜底：3列简表
    if not conditions:
        for m in re.finditer(r'^\| (COND-[A-Z0-9]+) \| (.+?) \| (.+?) \|', req_content, re.MULTILINE):
            cond_id = m.group(1)
            if cond_id in seen:
                continue
            seen.add(cond_id)
            parameter = m.group(2).strip()
            constraint = m.group(3).strip()
            conditions.append({"cond_id": cond_id, "parameter": parameter, "data_type": constraint,
                               "value_range": constraint, "enum_values": "", "default": "",
                               "required": "", "constraint": constraint, "type": _infer_param_type(constraint, constraint)})
    return conditions[:20]


def _extract_boundary_conditions(unit_content: str, req_content: str) -> List[Dict]:
    return _parse_cond_row(req_content)


def _infer_param_type(constraint: str, data_type: str = "") -> str:
    # 优先用数据类型列判断
    dt = (data_type or "").lower()
    if 'bool' in dt or re.search(r'true|false|布尔', constraint, re.IGNORECASE):
        return "boolean"
    if 'int' in dt or 'number' in dt or re.search(r'\d+[-~]\d+', constraint):
        return "integer"
    if 'string' in dt or '路径' in dt or 'path' in dt or '字符' in constraint or '长度' in constraint:
        return "string"
    # 约束含数字范围
    if re.search(r'\d+[-~]\d+', constraint):
        return "integer"
    if '长度' in constraint or '字符' in constraint:
        return "string"
    return "string"


def _calculate_boundary_values(cond: Dict) -> List[Dict]:
    constraint = cond.get("constraint", "")
    enum_values_col = cond.get("enum_values", "")
    param_type = cond.get("type", "string")
    values = []

    # 1) 优先用枚举值列（如 SUCCESS=0, FAILURE=1, RUNNING=2 或 TRANSLATOR=1,...）
    if enum_values_col and enum_values_col not in ['—', '-', '']:
        enum_items = [v.strip() for v in re.split(r'[,，、;；]', enum_values_col) if v.strip() and v.strip() not in ['—', '-']]
        if enum_items:
            values = [
                {"type": "min_valid", "value": enum_items[0]},
                {"type": "max_valid", "value": enum_items[-1]},
                {"type": "invalid_enum", "value": f"INVALID_{enum_items[0].split('=')[0]}"},
                {"type": "empty", "value": ""},
            ]
            return values

    # 2) 数字范围：兼容 - 和 ~ 分隔符（如 1~7、0-255、1-7）
    range_match = re.search(r'(\d+)\s*[-~]\s*(\d+)', constraint)
    if range_match:
        min_val = int(range_match.group(1))
        max_val = int(range_match.group(2))
        if param_type == "string":
            values = [
                {"type": "min_valid", "value": "a" * min_val if min_val > 0 else "a"},
                {"type": "max_valid", "value": "a" * max_val},
                {"type": "min_boundary-1", "value": "a" * (min_val - 1) if min_val > 1 else ""},
                {"type": "max_boundary+1", "value": "a" * (max_val + 1)},
                {"type": "empty", "value": ""},
            ]
        else:
            values = [
                {"type": "min_valid", "value": min_val},
                {"type": "max_valid", "value": max_val},
                {"type": "min_boundary-1", "value": min_val - 1},
                {"type": "max_boundary+1", "value": max_val + 1},
                {"type": "empty", "value": None},
            ]
        return values

    # 3) 枚举（约束用 / 分隔，如 true/false、registered/not_registered、0/1/2）
    if '/' in constraint:
        enum_values = [v.strip() for v in constraint.split('/') if v.strip()]
        if enum_values:
            values = [
                {"type": "min_valid", "value": enum_values[0]},
                {"type": "max_valid", "value": enum_values[-1]},
                {"type": "invalid_enum", "value": f"INVALID_{enum_values[0]}"},
                {"type": "empty", "value": ""},
            ]
            return values

    # 4) 布尔
    if param_type == "boolean":
        values = [
            {"type": "min_valid", "value": "true"},
            {"type": "max_valid", "value": "false"},
            {"type": "invalid_enum", "value": "INVALID_bool"},
            {"type": "empty", "value": ""},
        ]
        return values

    # 5) 兜底：用参数名生成有意义的典型值，不再用无意义占位符 test_value
    param_name = cond.get("parameter", "参数")
    values = [
        {"type": "typical", "value": f"有效{param_name}值"},
        {"type": "empty", "value": ""},
    ]
    return values


def _apply_boundary_risk_depth(boundary_values: List[Dict], risk_level: str) -> List[Dict]:
    depth_map = {"P0": 6, "P1": 5, "P2": 4, "P3": 2}
    depth = depth_map.get(risk_level, 4)
    return boundary_values[:depth]


def _infer_boundary_expected(value_type: str) -> str:
    if value_type in ["min_boundary-1", "max_boundary+1", "invalid_enum", "empty"]:
        return "参数校验失败"
    return "处理成功"


def _map_boundary_risk(value_type: str) -> str:
    if value_type in ["min_boundary-1", "max_boundary+1"]:
        return "P1"
    elif value_type in ["empty", "invalid_enum"]:
        return "P2"
    return "P3"


def _extract_equivalence_conditions(unit_content: str, req_content: str) -> List[Dict]:
    return _parse_cond_row(req_content)


def _classify_equivalence_classes(cond: Dict) -> Dict:
    constraint = cond.get("constraint", "无约束")
    enum_values_col = cond.get("enum_values", "")
    valid_classes = []
    invalid_classes = []

    # 1) 优先用枚举值列
    if enum_values_col and enum_values_col not in ['—', '-', '']:
        enum_items = [v.strip() for v in re.split(r'[,，、;；]', enum_values_col) if v.strip() and v.strip() not in ['—', '-']]
        if enum_items:
            valid_classes = [{"value": v, "description": f"有效枚举值{v}"} for v in enum_items]
            invalid_classes = [{"value": f"INVALID_{enum_items[0].split('=')[0]}", "description": "无效枚举值"},
                               {"value": "", "description": "空值"}]
            return {"valid_classes": valid_classes, "invalid_classes": invalid_classes}

    # 2) 数字范围（兼容 - 和 ~）
    range_match = re.search(r'(\d+)\s*[-~]\s*(\d+)', constraint)
    if range_match:
        min_val = int(range_match.group(1))
        max_val = int(range_match.group(2))
        typical_val = (min_val + max_val) // 2
        valid_classes = [{"value": min_val, "description": "最小有效值"},
                         {"value": typical_val, "description": "典型有效值"},
                         {"value": max_val, "description": "最大有效值"}]
        invalid_classes = [{"value": min_val - 1, "description": "小于最小值"},
                           {"value": max_val + 1, "description": "大于最大值"},
                           {"value": "", "description": "空值"}]
        return {"valid_classes": valid_classes, "invalid_classes": invalid_classes}

    # 3) / 分隔枚举
    if '/' in constraint:
        enum_values = [v.strip() for v in constraint.split('/') if v.strip()]
        if enum_values:
            valid_classes = [{"value": v, "description": f"有效枚举值{v}"} for v in enum_values]
            invalid_classes = [{"value": f"INVALID_{enum_values[0]}", "description": "无效枚举值"},
                               {"value": "", "description": "空值"}]
            return {"valid_classes": valid_classes, "invalid_classes": invalid_classes}

    # 4) 兜底：用参数名生成有意义典型值，不再用无意义占位符 test_value
    param_name = cond.get("parameter", "参数")
    valid_classes = [{"value": f"有效{param_name}值", "description": "典型有效值"}]
    invalid_classes = [{"value": "", "description": "空值"}]
    return {"valid_classes": valid_classes, "invalid_classes": invalid_classes}


def _select_equivalence_values(equivalence_classes: Dict, risk_level: str) -> List[Dict]:
    valid_classes = equivalence_classes.get("valid_classes", [])
    invalid_classes = equivalence_classes.get("invalid_classes", [])

    selected_valid = []
    selected_invalid = []
    if risk_level == "P0":
        selected_valid = valid_classes
        selected_invalid = invalid_classes
    elif risk_level == "P1":
        selected_valid = valid_classes[:3]
        selected_invalid = invalid_classes[:2]
    elif risk_level == "P2":
        selected_valid = valid_classes[:2]
        selected_invalid = invalid_classes[:1]
    else:
        selected_valid = valid_classes[:1]
        selected_invalid = invalid_classes[:1]

    for val in selected_valid:
        val["class_type"] = "valid"
    for val in selected_invalid:
        val["class_type"] = "invalid"

    return selected_valid + selected_invalid


def _infer_equivalence_expected(class_type: str) -> str:
    if class_type == "invalid":
        return "参数校验失败"
    return "处理成功"


def _map_equivalence_risk(class_type: str) -> str:
    if class_type == "invalid":
        return "P2"
    return "P3"


def _extract_business_rules(unit_content: str, req_content: str) -> List[Dict]:
    rules = []
    br_patterns = [r'\| (BR-\d+[A-Z0-9]*) \| (.+?) \| (.+?) \|', r'BR-\d+[：:]\s*([^\n]+)']

    for pattern in br_patterns:
        matches = _safe_regex_findall(pattern, req_content, re.MULTILINE)
        for match in matches:
            if isinstance(match, tuple):
                br_id = match[0]
                condition = match[1].strip() if len(match) > 1 else ""
                action = match[2].strip() if len(match) > 2 else ""
            else:
                br_id = "BR-UNKNOWN"
                condition = match
                action = ""

            rules.append({"br_id": br_id, "condition": condition, "action": action,
                          "cond_ids": _safe_regex_findall(r'COND-\d+[A-Z0-9]*', condition)})

    return rules[:15]


def _build_decision_conditions(rules: List[Dict]) -> List[str]:
    conditions = set()
    for rule in rules:
        conditions.update(rule.get("cond_ids", []))
    return sorted(list(conditions))[:8]


def _generate_truth_table(conditions: List[str]) -> List[List[bool]]:
    n = len(conditions)
    if n == 0:
        return []

    truth_table = []
    for i in range(2 ** n):
        row = []
        for j in range(n):
            row.append(bool((i >> j) & 1))
        truth_table.append(row)

    return truth_table


def _map_rule_to_action(truth_row: List[bool], rules: List[Dict], conditions: List[str]) -> str:
    truth_dict = dict(zip(conditions, truth_row))

    for rule in rules:
        rule_cond_ids = rule.get("cond_ids", [])
        if len(rule_cond_ids) == 0:
            continue

        match_count = 0
        for cond_id in rule_cond_ids:
            if cond_id in truth_dict:
                expected_value = True
                if "NOT" in rule.get("condition", "") or "不" in rule.get("condition", ""):
                    expected_value = False
                if truth_dict[cond_id] == expected_value:
                    match_count += 1

        if match_count == len(rule_cond_ids):
            return rule.get("action", "规则触发")

    return "未匹配规则"


def _map_decision_risk(truth_row: List[bool], rules: List[Dict]) -> str:
    match_count = sum(truth_row)
    if match_count >= len(truth_row) * 0.8:
        return "P0"
    elif match_count >= len(truth_row) * 0.5:
        return "P1"
    return "P2"


def _apply_decision_risk_depth(testpoints: List[Dict], risk_level: str) -> List[Dict]:
    depth_map = {"P0": len(testpoints), "P1": min(len(testpoints), int(len(testpoints) * 0.7)),
                 "P2": min(len(testpoints), int(len(testpoints) * 0.5)), "P3": min(len(testpoints), int(len(testpoints) * 0.3))}
    depth = depth_map.get(risk_level, int(len(testpoints) * 0.5))
    return testpoints[:depth]


def _extract_factors_internal(unit_content: str, req_content: str, unit_id: str) -> List[Dict]:
    truth_table_match = _safe_regex_search(r'#{4,5} 组合真值表', unit_content)

    cond_ids = []
    table_lines = []

    if truth_table_match:
        truth_table_start = truth_table_match.end()
        truth_table_end = unit_content.find('\n#####', truth_table_start)
        if truth_table_end == -1:
            truth_table_end = unit_content.find('\n####', truth_table_start)
        if truth_table_end == -1:
            truth_table_end = len(unit_content)

        truth_table_content = unit_content[truth_table_start:truth_table_end]
        header_pattern = r'\| (COND-\d+[A-Z0-9]*) \|'
        cond_ids = _safe_regex_findall(header_pattern, truth_table_content)

        for line in truth_table_content.split('\n'):
            if line.startswith('|') and '---' not in line:
                cells = [c.strip() for c in line.split('|') if c.strip()]
                if len(cells) >= 2 and not cells[0].startswith('COND-'):
                    table_lines.append(cells)

    if not cond_ids:
        return []

    factors = []
    for i, cond_id in enumerate(cond_ids[:10]):
        values = set()
        for line in table_lines:
            if i < len(line):
                val = line[i].strip()
                if val and val != '*' and val != '-':
                    values.add(val)

        if values:
            factor_name = cond_id
            name_pattern = rf'\| {re.escape(cond_id)} \| (.+?) \|'
            name_match = _safe_regex_search(name_pattern, req_content)
            if name_match:
                factor_name = name_match.group(1).strip()

            factors.append({"name": factor_name, "values": sorted(list(values)), "cond_id": cond_id})

    return factors


def check_non_orthogonal(requirement_path: str, output_path: str) -> Dict:
    req_content = _read_file(requirement_path)
    if not req_content:
        result = {"status": "error", "message": f"File not found: {requirement_path}",
                  "non_orthogonal_units": [], "orthogonal_units": []}
        _write_json(result, output_path)
        return result

    unit_patterns = [r'## [\d]+\.\s*主单元\s*\[(US-\d+|TR-\d+|MU-\d+)\]', r'## [\d]+\.\s+(US-\d+|TR-\d+|MU-\d+)[：:]']
    units = []
    for pattern in unit_patterns:
        found = _safe_regex_findall(pattern, req_content)
        if found:
            units = found
            break

    non_orthogonal = []
    orthogonal = []
    mixed = []

    for unit_id in units:
        unit_content = _extract_unit_section(req_content, unit_id)
        orth_type = "未判定"
        orth_patterns = [
            r'\*\*正交判定\*\*[：:]\s*(正交|非正交|混合型)',
            r'正交判定[：:]\s*(正交|非正交|混合型)',
            r'\*正交判定\*[：:]\s*(正交|非正交|混合型)',
        ]
        for op in orth_patterns:
            orth_match = _safe_regex_search(op, unit_content)
            if orth_match:
                orth_type = orth_match.group(1)
                break

        if orth_type == "非正交":
            non_orthogonal.append(unit_id)
        elif orth_type == "正交":
            orthogonal.append(unit_id)
        elif orth_type == "混合型":
            mixed.append(unit_id)

    result = {"status": "success", "technique": "factor_combination", "action": "check_non_orthogonal",
              "non_orthogonal_units": non_orthogonal, "orthogonal_units": orthogonal, "mixed_units": mixed,
              "total_units": len(non_orthogonal) + len(orthogonal) + len(mixed),
              "message": f"发现{len(non_orthogonal)}个非正交主单元", "dependencies": ["allpairspy"]}

    _write_json(result, output_path)
    return result


def validate_coverage(testpoint_path: str, combinations_path: str, output_path: str) -> Dict:
    tp_content = _read_file(testpoint_path)
    if not tp_content:
        result = {"status": "error", "message": f"测试点文件不存在: {testpoint_path}", "coverage_rate": 0, "passed": False}
        _write_json(result, output_path)
        return result

    try:
        with open(combinations_path, 'r', encoding='utf-8') as f:
            combinations_data = json.load(f)
    except Exception as e:
        result = {"status": "error", "message": f"读取组合矩阵失败: {str(e)}", "coverage_rate": 0, "passed": False}
        _write_json(result, output_path)
        return result

    combinations = combinations_data.get('combinations', [])
    if not combinations:
        result = {"status": "success", "message": "组合矩阵为空，无需验证", "coverage_rate": 100, "passed": True}
        _write_json(result, output_path)
        return result

    covered = set()
    for comb in combinations:
        comb_id = comb.get('id', '')
        if comb_id and re.search(rf'{comb_id}', tp_content):
            covered.add(comb_id)
        values_str = ','.join([f'{k}={v}' for k, v in comb['values'].items()])
        if values_str in tp_content:
            covered.add(comb_id)

    missing = [c['id'] for c in combinations if c['id'] not in covered]
    coverage_rate = round(len(covered) / len(combinations) * 100, 2) if combinations else 0

    result = {"status": "success", "technique": "factor_combination", "action": "validate_coverage",
              "coverage_rate": coverage_rate, "covered_combinations": sorted(list(covered)),
              "missing_combinations": missing, "total_combinations": len(combinations),
              "threshold": 95, "passed": coverage_rate >= 95, "dependencies": ["allpairspy"]}

    _write_json(result, output_path)
    return result


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description='Testing Technology Engine')
    parser.add_argument('--technique', required=True,
                        choices=['generate_all', 'boundary_value', 'equivalence_class',
                                 'decision_table', 'factor_combination'],
                        help='Testing technique')
    parser.add_argument('--action', choices=['check_non_orthogonal', 'validate_coverage'], help='Action for factor_combination')
    parser.add_argument('--requirement', help='requirement_analysis.md path')
    parser.add_argument('--testpoint', help='test_point_design.md path')
    parser.add_argument('--combinations', help='Combinations JSON file path')
    parser.add_argument('--risk-level', choices=['P0', 'P1', 'P2', 'P3'], default='P2', help='Risk level')
    parser.add_argument('--output', required=True, help='Output file path')

    args = parser.parse_args()
    _probe_optional_deps()
    result = None

    try:
        if args.technique == 'generate_all':
            if not args.requirement:
                result = {"status": "error", "message": "Missing --requirement"}
            else:
                result = generate_all(args.requirement, args.output)

        elif args.technique == 'boundary_value':
            if not args.requirement:
                result = {"status": "error", "message": "Missing --requirement"}
            else:
                result = generate_all(args.requirement, args.output)

        elif args.technique == 'factor_combination':
            if args.action == 'check_non_orthogonal':
                if not args.requirement:
                    result = {"status": "error", "message": "Missing --requirement"}
                else:
                    result = check_non_orthogonal(args.requirement, args.output)

            elif args.action == 'validate_coverage':
                if not args.testpoint or not args.combinations:
                    result = {"status": "error", "message": "Missing --testpoint or --combinations"}
                else:
                    result = validate_coverage(args.testpoint, args.combinations, args.output)

            else:
                result = {"status": "error", "message": "Missing --action for factor_combination"}

    except Exception as e:
        result = {"status": "error", "message": f"Exception: {str(e)}", "traceback": traceback.format_exc()}

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()