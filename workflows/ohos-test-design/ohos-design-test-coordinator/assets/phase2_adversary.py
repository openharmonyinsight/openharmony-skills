#!/usr/bin/env python3
"""Phase2测试点对抗评估脚本

聚合功能:
1. 前置数据锁定
2. 前置约束检查
3. 需求覆盖率计算（脚本+AI语义校验）- 测试对象40分，风险加权
4. 关键场景分类（脚本初步识别+AI语义校验）- 测试对象45分，风险等级差异化基础分
5. 变异体生成（含固定值过滤+对象类型风险等级差异化）
6. 变异杀死判断（脚本精确+范围+AI语义）- 测试对象15分，风险加权
7. 深度覆盖脚本化识别
8. 综合评分计算（三维度，总分≥80分达标）
9. 重复测试点检测
10. 测试经验覆盖验证（§2验证点按采纳规则纳入覆盖率维度评分）

优化说明:
- 风险等级加权：覆盖率/杀死率 P0×4,P1×3,P2×1,P3×0.5
- 关键场景基础分差异化：测试对象P0(8+8)/P1(6+6)/P2(4)/P3(2)
- 变异生成差异化：测试对象P0(4-5类)/P1(2-3)/P2(1-2)/P3(1)
- 回归对象不纳入对抗评分维度
- 固定值变异过滤：权限2750、属组3823等固定值不生成±1变异
"""

import argparse
import json
import os
import re
import sys
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Set, Tuple

FIXED_VALUE_PARAMS = {
    "权限": ["2750"],
    "属组": ["3823", "gid"],
    "mode": ["2750"],
}

FREQ_TO_RISK = {"高": "P0", "中": "P1", "低": "P2"}

RISK_WEIGHTS = {"P0": 4, "P1": 3, "P2": 1, "P3": 0.5}

DEPTH_COVER_KEYWORDS = {
    "边界场景": ["边界附近", "边界±1", "临界值", "边界极值", "边界值", "±1", "±5%", "极限", "极端"],
    "异常场景": ["异常恢复", "重试", "修复", "清理", "失败后", "恢复验证", "异常后", "恢复正常"],
    "竞态场景": ["并发边界", "竞态条件", "时间窗口", "同时", "临界", "并发上限", "竞态"],
    "特殊场景": ["权限隔离", "跨用户", "跨应用", "安全深度", "权限校验失败", "隔离验证"],
    "数据持久化": ["写入后读取", "持久化验证", "数据恢复", "写入验证", "持久化"],
}

SCORE_CONFIG_TEST_OBJ = {
    "边界场景":   {"P0": {"base": 8, "depth": 8}, "P1": {"base": 6, "depth": 6}, "P2": {"base": 4, "depth": 0}, "P3": {"base": 2, "depth": 0}},
    "异常场景":   {"P0": {"base": 8, "depth": 8}, "P1": {"base": 6, "depth": 6}, "P2": {"base": 4, "depth": 0}, "P3": {"base": 2, "depth": 0}},
    "竞态场景":   {"P0": {"base": 8, "depth": 8}, "P1": {"base": 6, "depth": 6}, "P2": {"base": 4, "depth": 0}, "P3": {"base": 2, "depth": 0}},
    "特殊场景":   {"P0": {"base": 8, "depth": 8}, "P1": {"base": 6, "depth": 6}, "P2": {"base": 4, "depth": 0}, "P3": {"base": 2, "depth": 0}},
    "数据持久化": {"P0": {"base": 8, "depth": 8}, "P1": {"base": 6, "depth": 6}, "P2": {"base": 4, "depth": 0}, "P3": {"base": 2, "depth": 0}},
    "状态转换":   {"P0": {"base": 8, "depth": 0}, "P1": {"base": 6, "depth": 0}, "P2": {"base": 4, "depth": 0}, "P3": {"base": 2, "depth": 0}},
    "组合场景":   {"P0": {"base": 8, "depth": 0}, "P1": {"base": 6, "depth": 0}, "P2": {"base": 4, "depth": 0}, "P3": {"base": 2, "depth": 0}},
}

TOTAL_SCORE_THRESHOLD = 80

AI_COVERAGE_VERIFY_HINT_TEMPLATE = """
脚本已基于关键词初步计算覆盖率，但可能存在遗漏或误判。
AI需进行覆盖率语义校验：
1. 检查测试点来源列是否包含场景ID引用
2. 验证场景ID格式与requirement_analysis.md被测场景表是否一致
3. 若测试点已覆盖场景但脚本匹配失败，补充覆盖率得分
4. 若脚本误判为覆盖但测试意图未真正覆盖，移除覆盖率得分

对象类型区分（基于knowledge_match.md§1.1）：
- 仅测试对象参与对抗评估，回归对象不纳入对抗评分维度

覆盖率语义校验判断标准：
- 被测场景覆盖：测试点测试意图与AC描述语义一致
- API覆盖：测试点触发了API调用路径
- 规则覆盖：测试点验证了业务规则约束
"""

AI_VERIFY_HINT_TEMPLATE = """
脚本已基于关键词初步识别深度覆盖，但可能存在遗漏或误判。
AI需进行语义校验：
1. 遍历tp_details中的每个测试点
2. 判断测试点的测试意图是否满足深度覆盖条件
3. 对于脚本未识别但实际有深度覆盖的测试点，增加深度分
4. 对于脚本误判的测试点，移除深度分

对象类型区分（基于knowledge_match.md§1.1）：
- 仅测试对象测试点参与深度覆盖校验，回归对象不纳入对抗评分

深度覆盖语义判断标准：
- 边界场景深度：测试意图是验证边界值附近的系统行为
- 异常场景深度：测试意图是验证异常发生后系统的恢复能力
- 竞态场景深度：测试意图是验证并发场景的边界条件
- 特殊场景深度：测试意图是验证安全/权限的深度隔离
- 数据持久化深度：测试意图是验证数据写入后的读取一致性

风险等级差异化基础分/深度分：
- 测试对象：P0(8+8), P1(6+6), P2(4), P3(2)
"""


class Phase2Adversary:
    def __init__(self, testpoint_path: str, requirement_path: str, km_path: str = ""):
        self.tp_path = testpoint_path
        self.req_path = requirement_path
        self.km_path = km_path
        self.tp_content = self._read_file(testpoint_path)
        self.req_content = self._read_file(requirement_path)
        self.km_data = self._parse_knowledge_match(km_path) if km_path else {
            "test_object_units": [], "regression_object_domains": [],
            "unit_risk_levels": {}, "has_regression": False
        }

    def _read_file(self, path: str) -> str:
        if not os.path.isfile(path):
            print(json.dumps({"status": "error", "message": f"文件不存在: {path}"}, ensure_ascii=False))
            sys.exit(1)
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def _parse_knowledge_match(self, km_path: str) -> Dict:
        if not km_path or not os.path.isfile(km_path):
            return {"test_object_units": [], "regression_object_domains": [],
                    "unit_risk_levels": {}, "has_regression": False}
        km_content = self._read_file(km_path)
        test_object_units = []
        regression_object_domains = []
        unit_risk_levels = {}
        section_match = re.search(r'### 1\.1 交付推断结果', km_content)
        if section_match:
            section_start = section_match.end()
            next_h = km_content.find('\n### ', section_start)
            if next_h == -1:
                next_h = km_content.find('\n## ', section_start)
            if next_h == -1:
                next_h = len(km_content)
            section = km_content[section_start:next_h]
            for row_match in re.finditer(
                r'^\| (测试对象|回归对象) \| (.+?) \| (.+?) \| (.+?) \|', section, re.MULTILINE
            ):
                obj_type = row_match.group(1).strip()
                unit_or_domain = row_match.group(2).strip()
                if obj_type == "测试对象":
                    test_object_units.append(unit_or_domain)
                elif obj_type == "回归对象":
                    regression_object_domains.append(unit_or_domain)
        tt_path = os.path.join(os.path.dirname(self.req_path), 'testing_technology.json')
        if os.path.isfile(tt_path):
            try:
                with open(tt_path, 'r', encoding='utf-8') as f:
                    tt_data = json.load(f)
                for unit in tt_data.get("units", []):
                    unit_risk_levels[unit["unit_id"]] = unit["risk_level"]
            except Exception:
                pass
        has_regression = len(regression_object_domains) > 0
        return {
            "test_object_units": test_object_units,
            "regression_object_domains": regression_object_domains,
            "unit_risk_levels": unit_risk_levels,
            "has_regression": has_regression,
        }

    def _classify_tp_object_type(self, source_col: str) -> str:
        for unit_id in self.km_data.get("test_object_units", []):
            norm_unit = unit_id.replace("-", "").replace(" ", "")
            if norm_unit in source_col.replace("-", "").replace(" ", ""):
                return "test_object"
        for domain in self.km_data.get("regression_object_domains", []):
            if f"回归验证-{domain}" in source_col or domain in source_col:
                return "regression_object"
        return "test_object"

    def _get_unit_risk_level(self, source_col: str) -> str:
        for unit_id, risk in self.km_data.get("unit_risk_levels", {}).items():
            norm_unit = unit_id.replace("-", "").replace(" ", "")
            if norm_unit in source_col.replace("-", "").replace(" ", ""):
                return risk
        priority_match = re.search(r'(P\d)', source_col)
        if priority_match:
            return priority_match.group(1)
        return "P2"

    def _get_section(self, content: str, start: int) -> str:
        next_section = content.find('\n## ', start)
        if next_section == -1:
            next_section = content.find('\n### ', start)
        if next_section == -1:
            next_section = len(content)
        return content[start:next_section]

    def _parse_experience_section(self) -> List[Dict]:
        if not self.km_path or not os.path.isfile(self.km_path):
            return []
        km_content = self._read_file(self.km_path)
        section_match = re.search(r'## 2\. 测试经验匹配结果', km_content)
        if not section_match:
            return []
        section_start = section_match.end()
        next_h = km_content.find('\n## ', section_start)
        if next_h == -1:
            next_h = len(km_content)
        section = km_content[section_start:next_h]
        if "无匹配条目" in section or "经验库为空" in section:
            return []
        entries = []
        for row_match in re.finditer(
            r'^\| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|',
            section, re.MULTILINE
        ):
            entry_id = row_match.group(1).strip()
            if entry_id.startswith('-') or entry_id.startswith('条目'):
                continue
            title = row_match.group(2).strip()
            source = row_match.group(3).strip()
            match_status = row_match.group(4).strip()
            match_degree = row_match.group(5).strip()
            features = row_match.group(6).strip()
            tech = row_match.group(7).strip()
            related_us = row_match.group(8).strip()
            adoption = row_match.group(9).strip() if len(row_match.groups()) >= 9 else ""
            content_col_idx = section.find(entry_id)
            full_content = ""
            if content_col_idx >= 0:
                row_end = section.find('\n|', content_col_idx)
                if row_end == -1:
                    row_end = section.find('\n', content_col_idx)
                row_text = section[content_col_idx:row_end]
                cells = [c.strip() for c in row_text.split('|')]
                if len(cells) >= 10:
                    full_content = cells[9]
            verif_points = []
            is_deep_level = "直接采纳" in adoption or adoption == ""
            is_parent_level = "语义匹配" in adoption or "相关性匹配" in adoption
            if full_content:
                for vp_match in re.finditer(
                    r'- \[?(必测|选测)\]? (.+?)(?:（可观测[：:] (.+?)）)?(?:\n|$)', full_content
                ):
                    tag = vp_match.group(1) if vp_match.group(1) else ""
                    desc = vp_match.group(2).strip()
                    observable = vp_match.group(3).strip() if vp_match.group(3) else ""
                    verif_points.append({"tag": tag, "description": desc, "observable": observable})
                bare_matches = re.finditer(r'- ([^[\(].+?)(?:（可观测[：:] (.+?)）)?(?:\n|$)', full_content)
                for bm in bare_matches:
                    desc = bm.group(1).strip()
                    if desc and not any(vp["description"] == desc for vp in verif_points):
                        observable = bm.group(2).strip() if bm.group(2) else ""
                        verif_points.append({"tag": "", "description": desc, "observable": observable})
            freq_match = re.search(r'\*?\*?历史频率\*?\*?[：:]\s*(高|中|低)', full_content)
            frequency = freq_match.group(1) if freq_match else "中"
            risk_level = FREQ_TO_RISK.get(frequency, "P1")
            obj_type = "regression_object" if "回归验证" in related_us else "test_object"
            entries.append({
                "entry_id": entry_id, "title": title, "source": source,
                "match_status": match_status, "match_degree": match_degree,
                "features": features, "tech": tech, "related_us": related_us,
                "adoption": adoption, "full_content": full_content,
                "verification_points": verif_points, "frequency": frequency,
                "risk_level": risk_level, "object_type": obj_type,
                "is_deep_level": is_deep_level, "is_parent_level": is_parent_level,
            })
        return entries

    def experience_coverage_calculate(self) -> Dict:
        te_entries = self._parse_experience_section()
        if not te_entries:
            return {
                "total_entries": 0, "total_vp": 0, "required_vp": 0,
                "covered_vp": 0, "experience_coverage_rate": 100.0,
                "test_object_required": 0, "test_object_covered": 0,
                "test_obj_exp_rate": 100.0,
                "uncovered_details": [], "note": "经验库为空或无匹配条目"
            }
        tp_source_text = ""
        tp_rows = self._extract_tp_rows()
        for row in tp_rows:
            source = row[8] if len(row) > 8 else ""
            tp_source_text += source + "\n"
        tp_content_lower = self.tp_content.lower()

        test_obj_required_vps = []
        test_obj_covered_vps = []
        uncovered_details = []

        for entry in te_entries:
            entry_id = entry["entry_id"]
            obj_type = entry["object_type"]
            is_deep = entry["is_deep_level"]
            is_parent = entry["is_parent_level"]
            risk = entry["risk_level"]

            if obj_type == "regression_object":
                continue

            for vp in entry["verification_points"]:
                tag = vp["tag"]
                desc = vp["description"]
                is_required = False

                if tag == "必测":
                    is_required = True
                elif tag == "选测":
                    is_required = True
                elif tag == "" and is_deep:
                    is_required = True
                elif tag == "" and is_parent:
                    is_required = True
                elif tag == "" and not is_deep and not is_parent:
                    is_required = True

                if not is_required:
                    continue

                vp_id = f"{entry_id}/{desc[:30]}"
                adoption = entry.get("adoption", "")
                adoption_adopted = bool(adoption) and "采纳" in adoption
                covered = (entry_id in tp_source_text
                           or desc.lower() in tp_content_lower
                           or adoption_adopted)

                test_obj_required_vps.append(vp_id)
                if covered:
                    test_obj_covered_vps.append(vp_id)
                else:
                    uncovered_details.append({
                        "entry_id": entry_id, "vp_desc": desc, "tag": tag or "无标注(直接采纳)",
                        "object_type": obj_type, "risk_level": risk, "adoption": entry["adoption"]
                    })

        test_obj_vp_risk = {vp: te_entries[0]["risk_level"] for vp in test_obj_required_vps}
        for i, vp in enumerate(test_obj_required_vps):
            for entry in te_entries:
                if vp.startswith(entry["entry_id"]):
                    test_obj_vp_risk[vp] = entry["risk_level"]
                    break

        test_obj_exp_rate = self._risk_weighted_rate(test_obj_covered_vps, test_obj_required_vps, test_obj_vp_risk) if test_obj_required_vps else 100.0

        total_required = len(test_obj_required_vps)
        total_covered = len(test_obj_covered_vps)
        overall_rate = (total_covered / total_required * 100) if total_required > 0 else 100.0

        return {
            "total_entries": len(te_entries), "total_vp": sum(len(e["verification_points"]) for e in te_entries),
            "required_vp": total_required, "covered_vp": total_covered,
            "experience_coverage_rate": round(overall_rate, 2),
            "test_object_required": len(test_obj_required_vps), "test_object_covered": len(test_obj_covered_vps),
            "test_obj_exp_rate": round(test_obj_exp_rate, 2), "test_obj_vp_risk": test_obj_vp_risk,
            "uncovered_details": uncovered_details,
            "adoption_rules": {
                "最深层级-无标注": "全部直接采纳(视为必测)",
                "最深层级-必测": "直接采纳",
                "最深层级-选测": "语义匹配采纳",
                "父层级-无标注": "按选测逻辑(语义匹配)",
                "父层级-必测": "直接采纳",
                "父层级-选测": "语义匹配采纳",
            },
            "freq_to_risk": FREQ_TO_RISK,
            "note": "经验验证点按采纳规则纳入覆盖率维度；仅测试对象参与；历史频率映射风险等级(高→P0,中→P1,低→P2)"
        }

    def _risk_weighted_rate(self, covered_items: List[str], all_items: List[str],
                            item_risk_map: Dict[str, str]) -> float:
        if not all_items:
            return 100.0
        total_weight = sum(RISK_WEIGHTS.get(item_risk_map.get(item, "P2"), 1) for item in all_items)
        covered_weight = sum(RISK_WEIGHTS.get(item_risk_map.get(item, "P2"), 1) for item in covered_items)
        return (covered_weight / total_weight * 100) if total_weight > 0 else 0

    def data_lock(self) -> Dict:
        tp_rows = re.findall(r'^\| ((?:TP-[A-Z0-9\-]+|US\d+-TP\d+)) \|', self.tp_content, re.MULTILINE)
        tp_total = len(tp_rows)

        scenario_patterns = [
            r'US\d+-AC\d+\.\d+[a-z]?', r'US\d+-AC\d+[a-z]?',
            r'US-\d+-AC-\d+\.\d+[a-z]?', r'US-\d+-AC-\d+[a-z]?',
            r'AC-[A-Z\d\.]+(?:-[A-Z\d]+)*[a-z]?',
            r'(?:SPEC|TR)\d+-AC\d+[A-Z]?[a-z]?'
        ]
        scenarios: Set[str] = set()
        for pattern in scenario_patterns:
            matches = re.findall(pattern, self.req_content)
            scenarios.update(matches)
        scenario_total = len(scenarios)

        api_section = re.search(r'### 2\.3 SDK API信息', self.req_content)
        apis: Set[str] = set()
        if api_section:
            section = self._get_section(self.req_content, api_section.end())
            api_matches = re.findall(r'^\| (API-[A-Z0-9]+)', section, re.MULTILINE)
            apis.update(api_matches)
        api_total = len(apis)

        vm_matches = re.findall(r'VM-\d+', self.req_content)
        vm_total = len(set(vm_matches))

        test_obj_tp_count = 0
        reg_tp_count = 0
        tp_rows9 = re.findall(
            r'^\| (TP-[A-Z0-9\-]+) \| [^|]+ \| [^|]+ \| [^|]+ \| [^|]+ \| [^|]+ \| (P\d) \| [^|]+ \| ([^|]+) \|',
            self.tp_content, re.MULTILINE
        )
        tp_rows8 = re.findall(
            r'^\| (TP-[A-Z0-9\-]+) \| [^|]+ \| [^|]+ \| [^|]+ \| [^|]+ \| (P\d) \| [^|]+ \| ([^|]+) \|',
            self.tp_content, re.MULTILINE
        )
        for rows in [tp_rows9, tp_rows8]:
            for row in rows:
                obj_type = self._classify_tp_object_type(row[2] if len(row) > 2 else "")
                if obj_type == "test_object":
                    test_obj_tp_count += 1
                else:
                    reg_tp_count += 1

        return {
            "tp_total": tp_total,
            "test_object_tp_total": test_obj_tp_count,
            "regression_tp_total": reg_tp_count,
            "scenario_total": scenario_total,
            "api_total": api_total,
            "vm_total": vm_total,
            "has_regression": self.km_data.get("has_regression", False),
            "test_object_units": self.km_data.get("test_object_units", []),
            "regression_object_domains": self.km_data.get("regression_object_domains", []),
            "tp_path": self.tp_path, "req_path": self.req_path, "km_path": self.km_path
        }

    def constraint_check(self) -> Dict:
        inner_section = re.search(r'Inner接口过滤说明', self.req_content)
        deleted_apis: List[str] = []
        if inner_section:
            section = self._get_section(self.req_content, inner_section.end())
            deleted_apis = re.findall(r'([a-z_][a-zA-Z0-9_]+).*?删除', section)

        violated_tps: List[Dict] = []
        for api in deleted_apis:
            pattern = rf'^\| ((?:TP-[A-Z0-9\-]+|US\d+-TP\d+)) \| .*? \| .*? \| .*? \| .*? \| .*? \| XTS \| .*?{api}'
            matches = re.findall(pattern, self.tp_content, re.MULTILINE)
            for tp_id in matches:
                violated_tps.append({"tp_id": tp_id, "api": api, "exec_method": "XTS"})

        return {"deleted_apis": deleted_apis, "violated_tps": violated_tps, "violated_count": len(violated_tps)}

    def coverage_calculate(self) -> Dict:
        scenarios: Set[str] = set()
        scenario_row_patterns = [
            r'^\| (US-?\d+-?AC-?\d+(?:\.\d+)?[a-z]?) \|',
            r'^\| (US\d+-AC\d+(?:\.\d+)?[a-z]?) \|',
            r'^\| (US-\d+-AC-\d+(?:\.\d+)?[a-z]?) \|',
        ]
        for pattern in scenario_row_patterns:
            scenario_rows = re.findall(pattern, self.req_content, re.MULTILINE)
            scenarios.update(scenario_rows)

        api_section = re.search(r'### 2\.3 SDK API信息', self.req_content)
        apis: Set[str] = set()
        api_is_method: Dict[str, bool] = {}
        if api_section:
            section = self._get_section(self.req_content, api_section.end())
            for m in re.finditer(r'^\| (API-[A-Z0-9]+) \| [^|]+ \| ([^|]+) \|', section, re.MULTILINE):
                api_id = m.group(1)
                iface_type = m.group(2).strip().lower()
                apis.add(api_id)
                api_is_method[api_id] = 'method' in iface_type

        covered_scenarios: Set[str] = set()
        covered_apis: Set[str] = set()

        tp_rows9 = re.findall(
            r'^\| (TP-[A-Z0-9\-]+) \| [^|]+ \| [^|]+ \| [^|]+ \| [^|]+ \| [^|]+ \| [^|]+ \| [^|]+ \| ([^|]+) \|',
            self.tp_content, re.MULTILINE
        )
        tp_rows8 = re.findall(
            r'^\| (TP-[A-Z0-9\-]+) \| [^|]+ \| [^|]+ \| [^|]+ \| [^|]+ \| [^|]+ \| [^|]+ \| ([^|]+) \|',
            self.tp_content, re.MULTILINE
        )
        tp_rows = tp_rows9 + tp_rows8

        source_scenario_patterns = [
            r'US\d+-AC\d+\.\d+[a-z]?', r'US\d+-AC\d+[a-z]?',
            r'US-\d+-AC-\d+[a-z]?', r'US\d+-AC\d+\.\d+',
        ]
        for tp_id, source_col in tp_rows:
            for pattern in source_scenario_patterns:
                scenario_matches = re.findall(pattern, source_col)
                covered_scenarios.update(scenario_matches)
            api_found = re.findall(r'API-[A-Z0-9]+', source_col)
            covered_apis.update(api_found)

        for api_in_content in re.findall(r'API-[A-Z0-9]+', self.tp_content):
            covered_apis.add(api_in_content)

        if api_is_method:
            any_method_covered = any(covered_apis & {a for a, is_m in api_is_method.items() if is_m})
            if any_method_covered:
                for api_id, is_method in api_is_method.items():
                    if not is_method:
                        covered_apis.add(api_id)

        def normalize_scenario_id(scenario_id: str) -> str:
            match = re.match(r'US-?(\d+)-?AC-?(\d+)(\.\d+)?([a-z])?', scenario_id)
            if match:
                us_num = int(match.group(1))
                ac_num = int(match.group(2))
                dot_suffix = match.group(3) or ""
                letter_suffix = match.group(4) or ""
                return f'US{us_num}-AC{ac_num}{dot_suffix}{letter_suffix}'
            return scenario_id

        normalized_scenarios = {normalize_scenario_id(s) for s in scenarios}
        normalized_covered_raw = {normalize_scenario_id(s) for s in covered_scenarios}
        normalized_covered = {s for s in normalized_covered_raw if s in normalized_scenarios}

        test_obj_scenarios = normalized_scenarios
        test_obj_covered = normalized_covered
        uncovered_scenarios = [s for s in normalized_scenarios if s not in normalized_covered]

        def _scenario_risk(s: str) -> str:
            us_num_match = re.match(r'US(\d+)', s)
            if us_num_match:
                for unit_id, risk in self.km_data.get("unit_risk_levels", {}).items():
                    uid_match = re.match(r'US-?(\d+)', unit_id)
                    if uid_match and uid_match.group(1) == us_num_match.group(1):
                        return risk
            return "P2"

        test_obj_scenario_risk = {s: _scenario_risk(s) for s in test_obj_scenarios}
        test_obj_scenario_rate = self._risk_weighted_rate(test_obj_covered, list(test_obj_scenarios), test_obj_scenario_risk)

        def _api_risk(api_id: str) -> str:
            section_text = self._get_section(self.req_content, api_section.end()) if api_section else ""
            api_row = re.search(rf'^\| {re.escape(api_id)} \| [^|]+ \| [^|]+ \|', section_text, re.MULTILINE)
            source = api_row.group(0) if api_row else ""
            for unit_id, risk in self.km_data.get("unit_risk_levels", {}).items():
                norm = unit_id.replace("-", "").replace(" ", "")
                if norm in source.replace("-", "").replace(" ", ""):
                    return risk
            return "P2"

        test_obj_apis = apis
        test_obj_covered_apis = covered_apis & test_obj_apis
        test_obj_api_risk = {a: _api_risk(a) for a in test_obj_apis}
        test_obj_api_rate = self._risk_weighted_rate(list(test_obj_covered_apis), list(test_obj_apis), test_obj_api_risk) if test_obj_apis else 100.0

        has_test_obj_api = len(test_obj_apis) > 0

        if has_test_obj_api:
            test_obj_coverage = test_obj_scenario_rate * 0.7 + test_obj_api_rate * 0.3
        else:
            test_obj_coverage = test_obj_scenario_rate

        test_obj_cov_score = test_obj_coverage / 100 * 40

        return {
            "test_object": {
                "scenario_total": len(test_obj_scenarios),
                "scenario_covered": len(test_obj_covered),
                "scenario_coverage_rate": round(test_obj_scenario_rate, 2),
                "api_total": len(test_obj_apis),
                "has_api": has_test_obj_api,
                "api_covered": len(test_obj_covered_apis),
                "api_coverage_rate": round(test_obj_api_rate, 2) if has_test_obj_api else None,
                "coverage_rate": round(test_obj_coverage, 2),
                "weight": 40,
                "score": round(test_obj_cov_score, 2),
                "risk_weighted": True,
                "risk_weights": RISK_WEIGHTS,
            },
            "combined_coverage_rate": round(test_obj_coverage, 2),
            "total_cov_score": round(test_obj_cov_score, 2),
            "uncovered_test_obj_scenarios": uncovered_scenarios,
            "need_ai_verify": True,
            "ai_verify_hint": AI_COVERAGE_VERIFY_HINT_TEMPLATE,
            "experience_coverage": self.experience_coverage_calculate(),
            "note": "三维度评分：测试对象覆盖率×40+关键场景×45+变异杀死率×15+经验覆盖率修正；风险加权(P0×4,P1×3,P2×1,P3×0.5)；回归对象不纳入对抗评分；经验§2验证点按采纳规则纳入覆盖率修正"
        }

    def _has_depth_cover(self, tp_detail: Dict, scenario_type: str) -> bool:
        keywords = DEPTH_COVER_KEYWORDS.get(scenario_type, [])
        text = f"{tp_detail.get('scenario', '')} {tp_detail.get('input_cond', '')} {tp_detail.get('expected', '')}"
        for kw in keywords:
            if kw in text:
                return True
        return False

    def _extract_tp_rows(self) -> List[Tuple]:
        tp_rows9 = re.findall(
            r'^\| (TP-[A-Z0-9\-]+) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (P\d) \| (.+?) \| (.+?) \|',
            self.tp_content, re.MULTILINE
        )
        tp_rows8 = re.findall(
            r'^\| (TP-[A-Z0-9\-]+) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (P\d) \| (.+?) \| (.+?) \|',
            self.tp_content, re.MULTILINE
        )
        result = []
        for row in tp_rows9:
            result.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8] if len(row) > 8 else ""))
        for row in tp_rows8:
            if not any(r[0] == row[0] for r in result):
                result.append((row[0], row[1], row[2], row[3], row[4], "", row[5], row[6], row[7] if len(row) > 7 else ""))
        return result

    def key_scenario_classify(self) -> Dict:
        keywords = {
            "特殊场景": ["安全", "权限", "system", "沙箱", "攻击", "防护"],
            "竞态场景": ["竞态", "并发", "临界", "同时", "多线程"],
            "边界场景": ["边界", "极值", "空值", "越界", "最大", "最小", "空数组", "无效枚举", "边界附近"],
            "数据持久化": ["持久化", "存储", "写入", "保存", "文件", "沙箱"],
            "状态转换": ["ASSOC", "状态", "转换", "destroy", "销毁"],
            "组合场景": ["组合", "混合", "耦合"],
            "异常场景": ["异常", "无效", "非法", "错误", "失败", "崩溃", "缺失", "恢复"]
        }

        classified_test_obj = {}
        for k in keywords:
            classified_test_obj[k] = {"total": 0, "tps": [], "tp_details": [],
                                      "script_depth_cover_count": 0, "script_depth_cover_tps": []}

        priority_order = ["竞态场景", "边界场景", "特殊场景", "数据持久化", "状态转换", "组合场景", "异常场景"]

        tp_rows = self._extract_tp_rows()

        for row in tp_rows:
            tp_id = row[0]
            scenario = row[1]
            input_cond = row[2]
            expected = row[3]
            test_type = row[4]
            test_technique = row[5]
            priority = row[6]
            exec_method = row[7]
            source = row[8]

            obj_type = self._classify_tp_object_type(source)
            if obj_type == "regression_object":
                continue

            risk_level = self._get_unit_risk_level(source)

            matched = False
            for scenario_type in priority_order:
                kw_list = keywords[scenario_type]
                for kw in kw_list:
                    if kw in scenario or kw in input_cond or kw in source or kw in expected:
                        tp_detail = {
                            "tp_id": tp_id, "scenario": scenario, "input_cond": input_cond,
                            "expected": expected, "test_type": test_type,
                            "test_technique": test_technique, "priority": priority,
                            "exec_method": exec_method, "source": source,
                            "object_type": obj_type, "risk_level": risk_level,
                            "script_depth_cover": False, "need_ai_verify_depth": True
                        }
                        has_depth = self._has_depth_cover(tp_detail, scenario_type)
                        tp_detail["script_depth_cover"] = has_depth

                        classified_test_obj[scenario_type]["total"] += 1
                        classified_test_obj[scenario_type]["tps"].append(tp_id)
                        classified_test_obj[scenario_type]["tp_details"].append(tp_detail)
                        if has_depth:
                            classified_test_obj[scenario_type]["script_depth_cover_count"] += 1
                            classified_test_obj[scenario_type]["script_depth_cover_tps"].append(tp_id)
                        matched = True
                        break
                if matched:
                    break

        return {
            "test_object": classified_test_obj,
            "weight": 45,
            "score_config_test_obj": SCORE_CONFIG_TEST_OBJ,
            "risk_weights": RISK_WEIGHTS,
            "need_ai_verify": True,
            "ai_verify_hint": AI_VERIFY_HINT_TEMPLATE,
        }

    def mutation_generate(self) -> Dict:
        spec_section = re.search(r'### 2\.1 输入条件规格表', self.req_content)
        mutations_test_obj: List[Dict] = []
        skipped_fixed_values: List[Dict] = []

        if spec_section:
            section = self._get_section(self.req_content, spec_section.end())
            rows = re.findall(
                r'^\| (COND-[A-Z0-9]+) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \|',
                section, re.MULTILINE
            )

            for row in rows:
                cond_id = row[0]
                param_name = row[1]
                data_type = row[2]
                value_range = row[3]
                required = row[4]
                source = row[8] if len(row) > 8 else ""

                obj_type = self._classify_tp_object_type(source)
                risk_level = self._get_unit_risk_level(source)

                def _add_mutation(mtype: str, value, target_list: List[Dict], idx_counter: List[int]):
                    idx_counter[0] += 1
                    target_list.append({
                        "id": f"M-{idx_counter[0]:03d}", "type": mtype, "value": value,
                        "param": param_name, "source": cond_id, "is_fixed": False,
                        "object_type": obj_type, "risk_level": risk_level,
                    })

                idx_test = [len(mutations_test_obj)]

                if obj_type == "regression_object":
                    continue

                if "int" in data_type.lower() or "number" in data_type.lower():
                    range_match = re.search(r'\[(\d+),\s*(\d+)\]', value_range)
                    if range_match:
                        lower = int(range_match.group(1))
                        upper = int(range_match.group(2))
                        is_fixed_value = False
                        for fixed_param, fixed_vals in FIXED_VALUE_PARAMS.items():
                            if fixed_param.lower() in param_name.lower():
                                if str(lower) in fixed_vals or str(upper) in fixed_vals:
                                    is_fixed_value = True
                                    skipped_fixed_values.append({
                                        "param": param_name, "value_range": value_range,
                                        "reason": f"固定值参数，跳过±1变异（{fixed_param}={lower}/{upper})"
                                    })
                                    break
                        if not is_fixed_value:
                            if risk_level in ("P0", "P1"):
                                _add_mutation("边界-1", lower - 1, mutations_test_obj, idx_test)
                                _add_mutation("边界+1", upper + 1, mutations_test_obj, idx_test)
                            elif risk_level == "P2":
                                _add_mutation("边界-1", lower - 1, mutations_test_obj, idx_test)
                            else:
                                pass
                if "可选" in required:
                    if risk_level in ("P0", "P1", "P2"):
                        _add_mutation("空值", "null", mutations_test_obj, idx_test)
                    elif risk_level == "P3":
                        _add_mutation("空值", "null", mutations_test_obj, idx_test)
                if "string" in data_type.lower() or "path" in data_type.lower():
                    if risk_level == "P0":
                        _add_mutation("格式", "invalid_format", mutations_test_obj, idx_test)
                    elif risk_level == "P1":
                        _add_mutation("格式", "invalid_format", mutations_test_obj, idx_test)

        return {
            "test_object_mutations": mutations_test_obj,
            "test_object_total": len(mutations_test_obj),
            "skipped_fixed_values": skipped_fixed_values,
            "skipped_count": len(skipped_fixed_values),
            "mutation_depth_matrix": {
                "test_object": {"P0": "4-5类", "P1": "2-3类", "P2": "1-2类", "P3": "1类"},
            },
            "note": "变异体按风险等级差异化生成；回归对象不纳入对抗评估"
        }

    def mutation_kill(self, mutation_data: Dict) -> Dict:
        mutations = mutation_data.get("test_object_mutations", [])

        tp_rows1 = re.findall(
            r'^\| (TP-[A-Z0-9\-]+) \| .*? \| (.+?) \|', self.tp_content, re.MULTILINE
        )
        tp_rows2 = re.findall(
            r'^\| (TP-[A-Z0-9\-]+) \| (.+?) \| .*? \| .*? \| .*? \| .*? \| .*? \| (.+?) \|',
            self.tp_content, re.MULTILINE
        )
        tp_rows = [(r[0], r[1]) for r in tp_rows1] + [(r[0], f"{r[1]} {r[2]}") for r in tp_rows2]

        tp_values_map: Dict[str, List[int]] = {}
        for tp_id, input_cond in tp_rows:
            numbers = re.findall(r'=(-?\d+)', input_cond)
            tp_values_map[tp_id] = [int(n) for n in numbers]

        exact_killed: List[Dict] = []
        range_killed: List[Dict] = []
        format_killed: List[Dict] = []
        null_killed: List[Dict] = []

        boundary_mutations = [m for m in mutations if m["type"] in ["边界-1", "边界+1"]]

        for mutation in boundary_mutations:
            target_value = mutation["value"]
            mutation_id = mutation["id"]
            for tp_id, values in tp_values_map.items():
                for v in values:
                    if v == target_value:
                        exact_killed.append({
                            "mutation_id": mutation_id, "mutation_value": target_value,
                            "mutation_type": mutation["type"], "killed_tp": tp_id,
                            "killed_value": v, "kill_method": "精确覆盖(60%)",
                            "object_type": mutation.get("object_type", "test_object"),
                            "risk_level": mutation.get("risk_level", "P2"),
                        })
                    else:
                        range_min = target_value * 0.9
                        range_max = target_value * 1.1
                        if range_min <= v <= range_max:
                            range_killed.append({
                                "mutation_id": mutation_id, "mutation_value": target_value,
                                "mutation_type": mutation["type"], "killed_tp": tp_id,
                                "killed_value": v, "kill_method": "范围覆盖(30%)",
                                "object_type": mutation.get("object_type", "test_object"),
                                "risk_level": mutation.get("risk_level", "P2"),
                            })

        format_keywords = ["特殊字符", "非法字符", "特殊符号", "格式错误", "无效格式", "非法格式",
                           "@", "#", "$", "%", "^", "&", "*", "空格", "制表符"]
        for mutation in mutations:
            if mutation["type"] == "格式":
                killed = False
                for tp_id, input_cond in tp_rows:
                    for kw in format_keywords:
                        if kw in input_cond:
                            format_killed.append({
                                "mutation_id": mutation["id"], "mutation_value": mutation["value"],
                                "mutation_type": "格式", "killed_tp": tp_id,
                                "killed_value": kw, "kill_method": "语义覆盖(格式变异)",
                                "object_type": mutation.get("object_type", "test_object"),
                                "risk_level": mutation.get("risk_level", "P2"),
                            })
                            killed = True
                            break
                    if killed:
                        break

        null_keywords = ["空", "null", "None", "\"\"", "[]", "{}"]
        for mutation in mutations:
            if mutation["type"] == "空值":
                killed = False
                for tp_id, input_cond in tp_rows:
                    for kw in null_keywords:
                        if kw in input_cond:
                            null_killed.append({
                                "mutation_id": mutation["id"], "mutation_value": mutation["value"],
                                "mutation_type": "空值", "killed_tp": tp_id,
                                "killed_value": kw, "kill_method": "语义覆盖(空值变异)",
                                "object_type": mutation.get("object_type", "test_object"),
                                "risk_level": mutation.get("risk_level", "P2"),
                            })
                            killed = True
                            break
                    if killed:
                        break

        exact_ids = [k["mutation_id"] for k in exact_killed]
        range_ids = [k["mutation_id"] for k in range_killed]
        format_ids = [k["mutation_id"] for k in format_killed]
        null_ids = [k["mutation_id"] for k in null_killed]
        script_killed_ids = list(set(exact_ids + range_ids + format_ids + null_ids))

        alive_mutations = [
            {
                "mutation_id": m["id"], "mutation_value": m["value"],
                "mutation_type": m["type"], "mutation_param": m["param"],
                "mutation_source": m["source"], "object_type": m.get("object_type", "test_object"),
                "risk_level": m.get("risk_level", "P2"),
                "need_semantic_judgment": True,
                "weighted_score_hint": "AI语义判定为独立第三杀死维度"
            }
            for m in mutations if m["id"] not in script_killed_ids
        ]

        def _risk_weighted_kill_rate(killed_ids: List[str], all_mutations: List[Dict]) -> float:
            if not all_mutations:
                return 100.0
            killed_mutations = [m for m in all_mutations if m["id"] in killed_ids]
            total_weight = sum(RISK_WEIGHTS.get(m.get("risk_level", "P2"), 1) for m in all_mutations)
            killed_weight = sum(RISK_WEIGHTS.get(m.get("risk_level", "P2"), 1) for m in killed_mutations)
            return (killed_weight / total_weight * 100) if total_weight > 0 else 0

        test_obj_mutations = mutation_data.get("test_object_mutations", [])
        test_obj_killed_ids = script_killed_ids
        test_obj_kill_rate = _risk_weighted_kill_rate(test_obj_killed_ids, test_obj_mutations)

        return {
            "test_object": {
                "mutation_total": len(test_obj_mutations),
                "script_killed_count": len(test_obj_killed_ids),
                "script_kill_rate": round(test_obj_kill_rate, 2),
                "risk_weighted": True,
                "weight": 15,
                "score": round(test_obj_kill_rate / 100 * 15, 2),
                "alive_mutations": alive_mutations,
                "alive_count": len(alive_mutations),
            },
            "exact_killed": exact_killed,
            "range_killed": range_killed,
            "format_killed": format_killed,
            "null_killed": null_killed,
            "alive_mutations": alive_mutations,
            "alive_count": len(alive_mutations),
            "note": "风险加权杀死率(P0×4,P1×3,P2×1,P3×0.5)；仅测试对象变异体参与"
        }

    def total_score(self, coverage: Dict, key_scenarios: Dict, mutation: Dict) -> Dict:
        cov_test_obj_score = coverage.get("test_object", {}).get("score", 0)

        exp_cov = coverage.get("experience_coverage", {})
        exp_test_obj_rate = exp_cov.get("test_obj_exp_rate", 100.0)
        has_exp = exp_cov.get("required_vp", 0) > 0

        exp_test_obj_modifier = 1.0
        if has_exp:
            exp_test_obj_modifier = max(0.7, 1 - 0.3 * (1 - exp_test_obj_rate / 100))
            cov_test_obj_score = cov_test_obj_score * exp_test_obj_modifier

        key_test_obj_data = key_scenarios.get("test_object", {})
        score_config_t = key_scenarios.get("score_config_test_obj", SCORE_CONFIG_TEST_OBJ)

        def _calc_key_score(classified: Dict, score_config: Dict, valid_priorities: List[str]) -> Tuple[float, float, Dict]:
            total_actual = 0
            total_max = 0
            details = {}
            for scenario_type, data in classified.items():
                config = score_config.get(scenario_type, SCORE_CONFIG_TEST_OBJ.get(scenario_type, {"P0": {"base": 8, "depth": 8}}))
                for tp_detail in data.get("tp_details", []):
                    priority = tp_detail.get("priority", "P2")
                    if priority not in valid_priorities:
                        continue
                    p_config = config.get(priority, config.get("P2", {"base": 4, "depth": 0}))
                    base = p_config["base"]
                    depth = p_config["depth"] if tp_detail.get("script_depth_cover", False) else 0
                    max_score = p_config["base"] + p_config["depth"]
                    actual = base + depth
                    total_actual += actual
                    total_max += max_score
                details[scenario_type] = {
                    "total_count": data.get("total", 0),
                    "tp_details": data.get("tp_details", []),
                    "base_score_total": sum(score_config.get(scenario_type, {}).get(tp.get("priority", "P2"), {"base": 4}).get("base", 4)
                                          for tp in data.get("tp_details", []) if tp.get("priority") in valid_priorities),
                    "depth_score_total": sum(score_config.get(scenario_type, {}).get(tp.get("priority", "P2"), {"depth": 0}).get("depth", 0)
                                          for tp in data.get("tp_details", []) if tp.get("priority") in valid_priorities and tp.get("script_depth_cover", False)),
                    "max_score_total": sum(score_config.get(scenario_type, {}).get(tp.get("priority", "P2"), {"base": 4, "depth": 0}).get("base", 4) +
                                          score_config.get(scenario_type, {}).get(tp.get("priority", "P2"), {"depth": 0}).get("depth", 0)
                                          for tp in data.get("tp_details", []) if tp.get("priority") in valid_priorities),
                }
            rate = (total_actual / total_max * 100) if total_max > 0 else 0
            return total_actual, total_max, details

        test_obj_actual, test_obj_max, key_test_obj_details = _calc_key_score(
            key_test_obj_data, score_config_t, ["P0", "P1", "P2", "P3"])
        test_obj_key_rate = (test_obj_actual / test_obj_max * 100) if test_obj_max > 0 else 0
        key_test_obj_score = test_obj_key_rate / 100 * 45

        mut_kill = mutation.get("kill", mutation)
        mut_test_obj_data = mut_kill.get("test_object", mutation.get("test_object", {}))
        mut_test_obj_score = mut_test_obj_data.get("score", 0)

        script_total = cov_test_obj_score + key_test_obj_score + mut_test_obj_score
        script_pass = script_total >= TOTAL_SCORE_THRESHOLD

        return {
            "coverage": {
                "test_object_score": round(cov_test_obj_score, 2),
                "test_object_weight": 40,
                "test_object_rate": coverage.get("test_object", {}).get("coverage_rate", 0),
                "test_object_exp_modifier": round(exp_test_obj_modifier, 4) if has_exp else 1.0,
                "experience_coverage": exp_cov,
                "need_ai_verify": True,
                "ai_verify_hint": coverage.get("ai_verify_hint", AI_COVERAGE_VERIFY_HINT_TEMPLATE),
            },
            "key_scenario": {
                "test_object_score": round(key_test_obj_score, 2),
                "test_object_weight": 45,
                "test_object_rate": round(test_obj_key_rate, 2),
                "test_object_details": key_test_obj_details,
                "need_ai_verify": True,
                "ai_verify_hint": AI_VERIFY_HINT_TEMPLATE,
                "score_config_test_obj": score_config_t,
            },
            "mutation": {
                "test_object_score": round(mut_test_obj_score, 2),
                "test_object_weight": 15,
                "test_object_kill_rate": mut_test_obj_data.get("script_kill_rate", 0),
                "alive_test_obj": mut_test_obj_data.get("alive_mutations", []),
            },
            "weights": {
                "coverage": 40, "key_scenario": 45, "mutation": 15,
                "note": "三维度评分权重：覆盖率40分+关键场景45分+变异杀死率15分=100"
            },
            "risk_weights": RISK_WEIGHTS,
            "script_total_score": round(script_total, 2),
            "script_pass": script_pass,
            "threshold": TOTAL_SCORE_THRESHOLD,
            "need_ai_verify": True,
            "ai_verify_summary": "三维度均需AI语义校验：覆盖率(风险加权)+关键场景深度(仅测试对象)+变异语义相似(风险加权)",
            "note": "三维度加权求和：覆盖率40 + 关键场景45 + 变异15 = 100；风险加权P0×4,P1×3,P2×1,P3×0.5；回归对象不纳入对抗评分"
        }

    def duplicate_detect(self) -> Dict:
        tps = []
        tp_pattern9 = r'^\| ((?:TP-[A-Z0-9\-]+|US\d+-TP\d+)) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (P\d) \| (.+?) \| (.+?) \|'
        tp_pattern8 = r'^\| ((?:TP-[A-Z0N9\-]+|US\d+-TP\d+)) \| (.+?) \| (.+?) \| (.+?) \| (.+?) \| (P\d) \| (.+?) \| (.+?) \|'

        for m in re.finditer(tp_pattern9, self.tp_content, re.MULTILINE):
            tp_id = m.group(1); scenario = m.group(2).strip(); input_cond = m.group(3).strip()
            expected = m.group(4).strip(); test_type = m.group(5).strip()
            test_technique = m.group(6).strip(); priority = m.group(7).strip()
            exec_method = m.group(8).strip(); source = m.group(9).strip()
            tps.append({"id": tp_id, "scenario": scenario, "input_cond": input_cond, "expected": expected,
                        "test_type": test_type, "test_technique": test_technique, "priority": priority,
                        "exec_method": exec_method, "source": source, "text": f"{scenario} {input_cond} {expected}"})

        for m in re.finditer(tp_pattern8, self.tp_content, re.MULTILINE):
            tp_id = m.group(1); scenario = m.group(2).strip(); input_cond = m.group(3).strip()
            expected = m.group(4).strip(); test_type = m.group(5).strip()
            priority = m.group(6).strip(); exec_method = m.group(7).strip(); source = m.group(8).strip()
            if not any(tp["id"] == tp_id for tp in tps):
                tps.append({"id": tp_id, "scenario": scenario, "input_cond": input_cond, "expected": expected,
                            "test_type": test_type, "test_technique": "", "priority": priority,
                            "exec_method": exec_method, "source": source, "text": f"{scenario} {input_cond} {expected}"})

        exact_duplicates = []
        potential_duplicates = []
        cross_type_candidates = []
        logic_equivalent_candidates = []
        nf_types = ['安全测试', '性能测试', '稳定性测试', '兼容性测试']

        for i in range(len(tps)):
            for j in range(i + 1, len(tps)):
                tp_a = tps[i]; tp_b = tps[j]
                similarity = self._similarity(tp_a["text"], tp_b["text"])
                exec_same = tp_a["exec_method"] == tp_b["exec_method"]
                if similarity >= 95 and exec_same:
                    exact_duplicates.append({"tp_a": tp_a["id"], "tp_b": tp_b["id"],
                                             "scenario_a": tp_a["scenario"], "scenario_b": tp_b["scenario"],
                                             "similarity": round(similarity, 2), "exec_same": exec_same})
                elif similarity >= 80 and exec_same:
                    potential_duplicates.append({"tp_a": tp_a["id"], "tp_b": tp_b["id"],
                                                 "scenario_a": tp_a["scenario"], "scenario_b": tp_b["scenario"],
                                                 "similarity": round(similarity, 2), "exec_same": exec_same})
                else:
                    type_a = tp_a.get('test_type', '')
                    type_b = tp_b.get('test_type', '')
                    is_nf_ac = (
                        (type_a in nf_types and type_b and type_b not in nf_types) or
                        (type_b in nf_types and type_a and type_a not in nf_types)
                    )
                    source_a = tp_a.get('source', '')
                    source_b = tp_b.get('source', '')
                    is_exp_ac = (
                        ('经验库' in source_a and 'AC' in source_b) or
                        ('经验库' in source_b and 'AC' in source_a)
                    )
                    if is_nf_ac:
                        cross_type_candidates.append({"tp_a": tp_a["id"], "tp_b": tp_b["id"],
                            "type_a": type_a, "type_b": type_b,
                            "similarity": round(similarity, 2), "reason": "nf_ac"})
                    elif is_exp_ac:
                        cross_type_candidates.append({"tp_a": tp_a["id"], "tp_b": tp_b["id"],
                            "source_a": source_a, "source_b": source_b,
                            "similarity": round(similarity, 2), "reason": "exp_ac"})
                    elif similarity >= 60:
                        logic_equivalent_candidates.append({"tp_a": tp_a["id"], "tp_b": tp_b["id"],
                            "similarity": round(similarity, 2)})

        return {
            "exact_duplicates": exact_duplicates, "potential_duplicates": potential_duplicates,
            "cross_type_candidates": cross_type_candidates,
            "logic_equivalent_candidates": logic_equivalent_candidates,
            "auto_delete": [d["tp_b"] for d in exact_duplicates],
            "need_semantic_judgment": ([d["tp_a"] for d in potential_duplicates] +
                                       [d["tp_b"] for d in potential_duplicates] +
                                       [d["tp_a"] for d in cross_type_candidates] +
                                       [d["tp_b"] for d in cross_type_candidates] +
                                       [d["tp_a"] for d in logic_equivalent_candidates] +
                                       [d["tp_b"] for d in logic_equivalent_candidates]),
            "exact_count": len(exact_duplicates), "potential_count": len(potential_duplicates),
            "cross_type_count": len(cross_type_candidates),
            "logic_equivalent_count": len(logic_equivalent_candidates)
        }

    def _similarity(self, text_a: str, text_b: str) -> float:
        return SequenceMatcher(None, text_a, text_b).ratio() * 100

    def run(self) -> Dict:
        result = {}
        result["data_lock"] = self.data_lock()
        result["constraint_check"] = self.constraint_check()
        result["coverage"] = self.coverage_calculate()
        result["key_scenarios"] = self.key_scenario_classify()
        mutation_data = self.mutation_generate()
        mutation_kill_data = self.mutation_kill(mutation_data)
        result["mutation"] = {"generate": mutation_data, "kill": mutation_kill_data}
        result["duplicate"] = self.duplicate_detect()
        result["total_score"] = self.total_score(result["coverage"], result["key_scenarios"], result["mutation"])
        result["status"] = "success"
        return result


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description='Phase2测试点对抗评估')
    parser.add_argument('--testpoint', required=True, help='test_point_design.md路径')
    parser.add_argument('--requirement', required=True, help='requirement_analysis.md路径')
    parser.add_argument('--knowledge-match', default='', help='knowledge_match.md路径')
    parser.add_argument('--output', required=True, help='输出JSON路径')
    args = parser.parse_args()

    adversary = Phase2Adversary(args.testpoint, args.requirement, args.knowledge_match)
    result = adversary.run()

    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps({"status": "success", "output": args.output}, ensure_ascii=False))


if __name__ == '__main__':
    main()
