#!/usr/bin/env python3
"""Phase4测试用例对抗评估脚本

聚合功能:
1. 前置数据锁定
2. 测试点覆盖率检查
3. 关键测试点覆盖率计算
4. 重复用例精确检测
5. 重复用例潜在检测
6. 质量评分数据准备

用法: python phase4_adversary.py --testcases test_cases.md --testpoint test_point_design.md --output phase4.json
"""

import argparse
import json
import os
import re
import sys
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Tuple


class Phase4Adversary:
    def __init__(self, testcases_path: str, testpoint_path: str):
        self.tc_path = testcases_path
        self.tp_path = testpoint_path
        self.tc_content = self._read_file(testcases_path)
        self.tp_content = self._read_file(testpoint_path)

    def _read_file(self, path: str) -> str:
        if not os.path.isfile(path):
            print(json.dumps({"status": "error", "message": f"文件不存在: {path}"}, ensure_ascii=False))
            sys.exit(1)
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def _get_section(self, content: str, start: int) -> str:
        next_section = content.find('\n## ', start)
        if next_section == -1:
            next_section = len(content)
        return content[start:next_section]

    def data_lock(self) -> Dict:
        tc_total = len(re.findall(r'^\| (TC-[A-Z0-9]+)', self.tc_content, re.MULTILINE))
        tp_total = len(re.findall(r'^\| ((?:TP-[A-Z0-9\-]+|US\d+-TP\d+))', self.tp_content, re.MULTILINE))
        return {
            "tc_total": tc_total,
            "tp_total": tp_total,
            "tc_path": self.tc_path,
            "tp_path": self.tp_path
        }

    def coverage_calculate(self) -> Dict:
        tp_ids = re.findall(r'^\| ((?:TP-[A-Z0-9\-]+|US\d+-TP\d+))', self.tp_content, re.MULTILINE)
        tc_rows = re.findall(r'^\| (TC-[A-Z0-9]+).*?\| (.+?) \|$', self.tc_content, re.MULTILINE)
        covered_tps = set()
        for tc_id, related_tps in tc_rows:
            found_tps = re.findall(r'(?:TP-[A-Z0-9\-]+|US\d+-TP\d+)', related_tps)
            for tp in found_tps:
                covered_tps.add(tp)
        uncovered_tps = [tp for tp in tp_ids if tp not in covered_tps]
        coverage_rate = (len(covered_tps) / len(tp_ids) * 100) if tp_ids else 0
        
        need_ai_verify_coverage = coverage_rate < 95 and len(covered_tps) > 0
        
        ai_coverage_verify_hint = ""
        if need_ai_verify_coverage:
            ai_coverage_verify_hint = """
脚本测试点覆盖率计算未达标，但检测到已有用例关联测试点。
AI需进行覆盖率语义校验：
1. 检查test_cases.md中用例的"关联测试点"字段是否正确标注
2. 验证测试点ID格式与test_point_design.md是否一致
3. 若用例已关联测试点但脚本匹配失败，补充覆盖率并刷新评分
4. 识别合并删除的测试点（标注为"合并删除"）不计入未覆盖

覆盖率语义校验判断标准：
- 用例关联测试点字段含TP-ID引用（如"TP-US01-001"）→ 测试点已覆盖
- 合并删除的测试点（如TP-US01-007标注"合并删除"）→ 不计入未覆盖
"""
        
        return {
            "tp_total": len(tp_ids),
            "tp_covered": len(covered_tps),
            "tp_uncovered": uncovered_tps,
            "coverage_rate": round(coverage_rate, 2),
            "pass": coverage_rate >= 95,
            "need_ai_verify_coverage": need_ai_verify_coverage,
            "ai_coverage_verify_hint": ai_coverage_verify_hint if need_ai_verify_coverage else "",
            "covered_tps_raw": list(covered_tps)
        }

    def key_tp_coverage(self) -> Dict:
        keywords = {
            "特殊场景": ["安全", "权限", "system"],
            "竞态场景": ["竞态", "并发", "临界"],
            "边界值": ["边界", "越界", "极值"],
            "数据持久化": ["持久化", "存储", "写入"],
            "状态转换": ["ASSOC", "状态转换", "前置依赖"],
            "异常场景": ["异常恢复", "EX-"],
            "组合场景": ["组合", "耦合"]
        }
        priority_order = ["特殊场景", "竞态场景", "边界值", "数据持久化", "状态转换", "异常场景", "组合场景"]

        tp_rows = re.findall(
            r'^\| ((?:TP-[A-Z0-9\-]+|US\d+-TP\d+)) \| .+? \| .+? \| .+? \| (P0|P1) \| .+? \| (.+?) \|',
            self.tp_content, re.MULTILINE
        )

        key_tp_classified = {k: {"total": 0, "tps": []} for k in keywords}
        key_tps = set()
        other_p0_p1_tps = []

        for tp_id, priority, source in tp_rows:
            if priority not in ["P0", "P1"]:
                continue

            matched = False
            for scenario_type in priority_order:
                kw_list = keywords[scenario_type]
                for kw in kw_list:
                    if kw in source:
                        key_tp_classified[scenario_type]["total"] += 1
                        key_tp_classified[scenario_type]["tps"].append(tp_id)
                        key_tps.add(tp_id)
                        matched = True
                        break
                if matched:
                    break

            if not matched:
                other_p0_p1_tps.append(tp_id)
                key_tps.add(tp_id)

        key_tp_classified["其他P0/P1"] = {
            "total": len(other_p0_p1_tps),
            "tps": other_p0_p1_tps
        }

        tc_rows = re.findall(r'^\| (TC-[A-Z0-9]+).*?\| (.+?) \|$', self.tc_content, re.MULTILINE)
        covered_key_tps = set()
        for tc_id, related_tps in tc_rows:
            found_tps = re.findall(r'(?:TP-[A-Z0-9\-]+|US\d+-TP\d+)', related_tps)
            for tp in found_tps:
                if tp in key_tps:
                    covered_key_tps.add(tp)

        uncovered_key_tps = [tp for tp in key_tps if tp not in covered_key_tps]
        key_rate = (len(covered_key_tps) / len(key_tps) * 100) if key_tps else 0

        return {
            "key_tp_total": len(key_tps),
            "key_tp_covered": len(covered_key_tps),
            "key_tp_uncovered": list(uncovered_key_tps),
            "key_tp_rate": round(key_rate, 2),
            "pass": key_rate >= 98,
            "key_tp_classified": key_tp_classified,
            "note": "关键测试点识别基于phase2输出件的来源列关键词和优先级列，按互斥优先级分类统计"
        }

    def duplicate_detect(self) -> Dict:
        case_pattern = r'### (TC-[A-Z0-9]+(?:-[A-Z0-9]+)*)-(.+)\n'
        cases = []
        for m in re.finditer(case_pattern, self.tc_content):
            case_id = m.group(1)
            case_name = m.group(2)
            case_name = re.sub(r'^\d+-', '', case_name)
            sec_start = m.end()
            sec_end = self.tc_content.find('\n### TC-', sec_start)
            if sec_end == -1:
                sec_end = len(self.tc_content)
            section = self.tc_content[sec_start:sec_end]
            exec_method = self._extract_field(section, '执行方式')
            precondition = self._extract_field(section, '预置条件')
            steps = self._extract_steps(section)
            expected = self._extract_expected(section)
            cases.append({
                "id": case_id,
                "name": case_name,
                "exec_method": exec_method,
                "precondition": precondition,
                "steps": steps,
                "expected": expected,
                "text": f"{precondition} {steps} {expected}"
            })
        exact_duplicates = []
        potential_duplicates = []
        for i in range(len(cases)):
            for j in range(i + 1, len(cases)):
                case_a = cases[i]
                case_b = cases[j]
                similarity = self._similarity(case_a["text"], case_b["text"])
                exec_same = case_a["exec_method"] == case_b["exec_method"]
                if similarity >= 95 and exec_same:
                    exact_duplicates.append({
                        "tc_a": case_a["id"],
                        "tc_b": case_b["id"],
                        "similarity": round(similarity, 2),
                        "exec_same": exec_same
                    })
                elif similarity >= 80 and exec_same:
                    potential_duplicates.append({
                        "tc_a": case_a["id"],
                        "tc_b": case_b["id"],
                        "similarity": round(similarity, 2),
                        "exec_same": exec_same
                    })
        return {
            "exact_duplicates": exact_duplicates,
            "potential_duplicates": potential_duplicates,
            "auto_delete": [d["tc_b"] for d in exact_duplicates],
            "need_semantic_judgment": [d["tc_a"] for d in potential_duplicates] + [d["tc_b"] for d in
                                                                                   potential_duplicates]
        }

    def _extract_field(self, section: str, field: str) -> str:
        m = re.search(rf'\*\*{field}[：:]\*\*\s*\n(.+?)(?:\n\n|\n\*\*|\Z)', section, re.DOTALL)
        if not m:
            return ''
        return '\n'.join(l.strip() for l in m.group(1).split('\n') if l.strip())

    def _extract_steps(self, section: str) -> str:
        m = re.search(r'\*\*测试步骤[：:]\*\*\s*\n\|.*\n[\s\S]+?(?=\n---|\n\*\*|\n\n###|\Z)', section)
        if not m:
            return ''
        steps = []
        for ln in m.group(0).split('\n'):
            if ln.startswith('|') and '---' not in ln:
                parts = ln.split('|')
                if len(parts) >= 3:
                    steps.append(f"{parts[1].strip()}. {parts[2].strip()}")
        return '\n'.join(steps)

    def _extract_expected(self, section: str) -> str:
        m = re.search(r'\*\*测试步骤[：:]\*\*\s*\n\|.*\n[\s\S]+?(?=\n---|\n\*\*|\n\n###|\Z)', section)
        if not m:
            return ''
        expected = []
        for ln in m.group(0).split('\n'):
            if ln.startswith('|') and '---' not in ln:
                parts = ln.split('|')
                if len(parts) >= 4:
                    expected.append(f"{parts[1].strip()}. {parts[3].strip()}")
        return '\n'.join(expected)

    def _similarity(self, text_a: str, text_b: str) -> float:
        return SequenceMatcher(None, text_a, text_b).ratio() * 100

    def quality_sample_prepare(self) -> Dict:
        tp_ids = re.findall(r'^\| (TP-[A-Z0-9\-]+)', self.tp_content, re.MULTILINE)
        sample_count = min(len(tp_ids), 30)
        sample_tp_ids = tp_ids[:sample_count]
        case_pattern = r'### (TC-[A-Z0-9]+(?:-[A-Z0-9]+)*)'
        sample_cases = []
        for tp_id in sample_tp_ids:
            tc_match = re.search(rf'^\| (TC-[A-Z0-9]+).*?\| {tp_id}', self.tc_content, re.MULTILINE)
            if tc_match:
                tc_id = tc_match.group(1)
                case_start = re.search(rf'### {re.escape(tc_id)}', self.tc_content)
                if case_start:
                    sec_start = case_start.end()
                    sec_end = self.tc_content.find('\n### TC-', sec_start)
                    if sec_end == -1:
                        sec_end = len(self.tc_content)
                    section = self.tc_content[sec_start:sec_end]
                    steps = self._extract_steps(section)
                    expected = self._extract_expected(section)
                    sample_cases.append({
                        "tp_id": tp_id,
                        "tc_id": tc_id,
                        "steps": steps[:200],
                        "expected": expected[:200]
                    })
        return {
            "sample_count": len(sample_cases),
            "sample_cases": sample_cases
        }

    def same_tp_multi_case_detect(self) -> Dict:
        """检测同一测试点下多个用例（同执行方式）的情况
        
        检测逻辑：
        1. 从test_cases.md汇总表提取每个TC关联的测试点和执行方式
        2. 按测试点分组，找出同一TP下有多个同执行方式TC的组
        3. 对每组提取TC详细信息供AI语义判断
        """
        tc_rows = re.findall(
            r'^\| (TC-[A-Z0-9]+(?:-[A-Z0-9]+)*)\s+\|\s*(.+?)\s+\|\s*(.+?)\s+\|\s*(.+?)\s+\|\s*(.+?)\s+\|\s*(.+?)\s+\|\s*(.+?)\s+\|\s*(.+?)\s+\|',
            self.tc_content, re.MULTILINE
        )

        tp_to_cases = {}
        for row in tc_rows:
            tc_id = row[0]
            tc_name = row[1]
            tc_type = row[2]
            tc_tech = row[3]
            exec_method = row[4]
            tc_level = row[5]
            tc_source = row[6]
            related_tps_str = row[7]

            found_tps = re.findall(r'(?:TP-[A-Z0-9\-]+|US\d+-TP\d+)', related_tps_str)
            for tp in found_tps:
                if tp not in tp_to_cases:
                    tp_to_cases[tp] = []
                tp_to_cases[tp].append({
                    "tc_id": tc_id,
                    "tc_name": tc_name,
                    "exec_method": exec_method,
                    "tc_level": tc_level,
                    "related_tps": related_tps_str
                })

        same_tp_groups = []
        for tp, cases in tp_to_cases.items():
            if len(cases) <= 1:
                continue
            exec_groups = {}
            for c in cases:
                em = c["exec_method"]
                if em not in exec_groups:
                    exec_groups[em] = []
                exec_groups[em].append(c)
            for exec_method, group_cases in exec_groups.items():
                if len(group_cases) > 1:
                    same_tp_groups.append({
                        "tp_id": tp,
                        "exec_method": exec_method,
                        "case_count": len(group_cases),
                        "cases": group_cases
                    })

        return {
            "same_tp_multi_cases": same_tp_groups,
            "total_groups": len(same_tp_groups),
            "total_redundant_cases": sum(g["case_count"] - 1 for g in same_tp_groups),
            "need_ai_semantic_judgment": same_tp_groups
        }

    def run(self) -> Dict:
        result = {}
        result["data_lock"] = self.data_lock()
        result["coverage"] = self.coverage_calculate()
        result["key_tp_coverage"] = self.key_tp_coverage()
        result["duplicate"] = self.duplicate_detect()
        result["same_tp_multi_case"] = self.same_tp_multi_case_detect()
        result["quality_sample"] = self.quality_sample_prepare()
        failed = []
        if not result["coverage"]["pass"]:
            failed.append("测试点覆盖率")
        if not result["key_tp_coverage"]["pass"]:
            failed.append("关键测试点覆盖率")
        result["pass"] = len(failed) == 0
        result["failed_dimensions"] = failed
        result["status"] = "success"
        return result


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description='Phase4测试用例对抗评估')
    parser.add_argument('--testcases', required=True, help='test_cases.md路径')
    parser.add_argument('--testpoint', required=True, help='test_point_design.md路径')
    parser.add_argument('--output', required=True, help='输出JSON路径')
    args = parser.parse_args()

    adversary = Phase4Adversary(args.testcases, args.testpoint)
    result = adversary.run()

    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.isdir(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(json.dumps({"status": "success", "output": args.output}, ensure_ascii=False))


if __name__ == '__main__':
    main()
