#!/usr/bin/env python3
"""Phase4测试用例细化辅助脚本

功能:
1. merge_batch_mds - 合并批次MD（统一重编号）
2. validate_merged_md - 校验完整性
3. coverage_check - 覆盖率检查
4. demo_map - Demo控件映射

用法:
  python phase4_testcase_utils.py --action merge_batch_mds --batch-dir batches_phase4/ --testpoint test_point_design.md --output test_cases.md
"""

import argparse
import datetime
import json
import os
import re
import sys
from typing import Dict, List


class Phase4TestcaseUtils:

    def get_parallel_limit(self) -> int:
        """动态获取并行上限（混合方案：优先psutil，降级默认6）"""
        try:
            import psutil
            available_gb = psutil.virtual_memory().available / (1024 ** 3)
            if available_gb >= 16:
                return 10
            elif available_gb >= 8:
                return 8
            elif available_gb >= 4:
                return 6
            else:
                return 4
        except ImportError:
            return 6

    def get_memory_available_gb(self) -> float:
        """获取可用内存（GB）"""
        try:
            import psutil
            return round(psutil.virtual_memory().available / (1024 ** 3), 2)
        except ImportError:
            return 0.0

    def _extract_batch_sort_key(self, filename: str) -> tuple:
        """提取批次文件排序键（Phase4专用：支持多种命名格式）

        命名格式（推荐）：batch_US01_1.md, batch_US02_1.md（主单元编号_批次号）
        命名格式（对抗补充）：batch_ADD_1.md, batch_ADD_2.md（对抗评估补充测试点）
        命名格式（兼容）：batch_01.md, batch_02.md, batch_1.md（纯数字）

        注意：Phase4命名规范现已统一与Phase2一致
        - Phase2：batch_US_xx.md（主单元命名）
        - Phase4：batch_USxx_n.md（主单元编号_批次号）
        - Phase4对抗补充：batch_ADD_n.md（对抗评估补充）

        Returns:
            排序键tuple（如 (0,'US01',1), (0,'',1), (1,'ADD',1)）；首元素0=主测试点、1=对抗补充，确保 ADD 排在 US 之后
        """
        # 对抗补充格式：batch_ADD_1.md（首元素1，确保补充排在主测试点之后）
        match = re.search(r'batch_ADD_(\d+)', filename)
        if match:
            return (1, 'ADD', int(match.group(1)))
        # 推荐格式：batch_US01_1.md, batch_SPEC001_1.md
        match = re.search(r'batch_(US\d+|SPEC\d+|TR\d+|MU\d+)_(\d+)', filename)
        if match:
            return (0, match.group(1), int(match.group(2)))
        # 兼容旧格式：batch_US_1.md（Phase2格式）
        match = re.search(r'batch_(US_\d+|(?:SPEC|TR)_\d+|MU_\d+)', filename)
        if match:
            return (0, match.group(1).replace('_', ''), 0)
        # 兼容纯数字：batch_1.md, batch_01.md
        match = re.search(r'batch_([a-z]*)(\d+)', filename)
        if match:
            return (0, match.group(1) or '', int(match.group(2)))
        match = re.search(r'batch_(\d+)', filename)
        if match:
            return (0, '', int(match.group(1)))
        return (0, filename, 0)

    def update_batch_status(self, batch_plan_path: str, batch_id: str,
                            status: str, output_path: str) -> Dict:
        """更新批次状态"""
        if not os.path.isfile(batch_plan_path):
            return {"status": "error", "message": f"batch_plan.json不存在: {batch_plan_path}"}

        with open(batch_plan_path, 'r', encoding='utf-8') as f:
            plan = json.load(f)

        batch_found = False
        for batch in plan.get("batches", []):
            if batch["batch_id"] == batch_id:
                batch["status"] = status
                if status == "failed":
                    batch["retry_count"] += 1
                batch_found = True
                break

        if not batch_found:
            return {"status": "error", "message": f"未找到批次: {batch_id}"}

        # 更新统计
        plan["success_count"] = sum(1 for b in plan["batches"] if b["status"] == "success")
        plan["failed_count"] = sum(1 for b in plan["batches"] if b["status"] == "failed")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)

        return {"status": "success", "batch_id": batch_id, "new_status": status, "plan": plan}

    def merge_batch_mds(self, batch_dir: str, testpoint_path: str, output_path: str,
                       requirement_path: str = None) -> Dict:
        """合并批次MD（统一重编号）"""
        if not os.path.isdir(batch_dir):
            return {"status": "error", "message": f"批次目录不存在: {batch_dir}"}

        batch_files = sorted(
            [f for f in os.listdir(batch_dir) if f.startswith('batch_') and f.endswith('.md')],
            key=lambda x: self._extract_batch_sort_key(x)
        )

        if not batch_files:
            return {"status": "error", "message": "未找到批次MD文件"}

        # 解析并统一重编号
        all_cases = []
        case_counter = 1
        for bf in batch_files:
            bf_path = os.path.join(batch_dir, bf)
            cases = self._parse_batch_md(bf_path)
            for case in cases:
                case['id'] = f"TC-{case_counter:03d}"
                case_counter += 1
            all_cases.extend(cases)

        all_cases = self._deduplicate_names(all_cases)

        redundant_groups = self._detect_same_tp_multi_cases(all_cases)

        doc_cases = self._generate_doc_cases(testpoint_path, all_cases, requirement_path)
        all_cases.extend(doc_cases)

        total = len(all_cases)

        # 写入test_cases.md
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"""# 测试用例

> 生成时间：{datetime.datetime.now().strftime("%Y-%m-%d")}
> 输入文件：test_point_design.md
> 测试用例总数：{total}个

## 汇总表

| 用例ID | 用例名称 | 测试类型 | 测试技术 | 执行方式 | 用例级别 | 来源 | 关联测试点 |
|--------|---------|---------|---------|---------|---------|------|-----------|
""")
            for case in all_cases:
                f.write(
                    f"| {case['id']} | {case['name']} | {case['test_type']} | {case['test_technique']} | {case['exec_method']} | {case['level']} | {case['source']} | {case['related_tp']} |\n")

            f.write("\n## 统计\n\n")
            f.write(self._generate_stats_section(all_cases, testpoint_path))

            f.write("\n## 详细用例\n\n")
            for case in all_cases:
                f.write(self._format_case_detail(case))

        return {
            "status": "success",
            "batch_files": len(batch_files),
            "total_cases": total,
            "doc_cases": len(doc_cases),
            "same_tp_multi_case_groups": len(redundant_groups),
            "same_tp_multi_case_details": redundant_groups[:20],
            "id_range": f"TC-001~TC-{total:03d}",
            "output": output_path
        }

    def _read_file(self, path: str) -> str:
        if not os.path.isfile(path):
            return ""
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def _parse_batch_md(self, md_path: str) -> List[Dict]:
        """解析批次MD（支持多种临时编号格式）

        支持格式：
        - TC-batch_1-01（旧格式，纯batch序号）
        - TC-batch_US01_1-001（推荐格式，主单元+批次）
        - TC-US01-001（推荐格式，主单元编号）
        - TC-001（简单编号）
        """
        content = self._read_file(md_path)
        if not content:
            return []

        # 支持临时编号格式：支持连字符、下划线、字母数字组合
        case_pattern = r'### (TC-[a-zA-Z0-9_\-]+)-(.+?)\n'
        case_matches = list(re.finditer(case_pattern, content))

        cases = []
        for i, match in enumerate(case_matches):
            case_id = match.group(1)
            case_name = match.group(2)

            # 去掉用例名称开头的数字编号前缀（如 001-、002- 等）
            case_name = re.sub(r'^\d+-', '', case_name)

            start_pos = match.end()
            end_pos = case_matches[i + 1].start() if i < len(case_matches) - 1 else len(content)
            case_content = content[start_pos:end_pos]

            cases.append({
                "id": case_id,
                "name": case_name,
                "test_type": self._extract_field(case_content, '测试类型'),
                "test_technique": self._extract_field(case_content, '测试技术'),
                "exec_method": self._extract_field(case_content, '执行方式'),
                "level": self._extract_field(case_content, '用例级别'),
                "source": self._extract_field(case_content, '来源'),
                "related_tp": self._extract_field(case_content, '关联测试点'),
                "preconditions": self._extract_preconditions(case_content),
                "steps": self._extract_steps(case_content)
            })

        return cases

    def _extract_field(self, content: str, field_name: str) -> str:
        # 同时支持中文冒号和英文冒号
        pattern = rf'\*\*{field_name}[：:]\*\*\s*(.+?)\n'
        match = re.search(pattern, content)
        return match.group(1).strip() if match else ""

    def _extract_preconditions(self, content: str) -> List[str]:
        """提取预置条件（增强容错：兼容多种格式）

        支持格式：
        1. 数字序号格式：1. xxx, 2. xxx
        2. 减号列表格式：- xxx
        3. 单换行或双换行
        """
        preconditions = []

        pattern1 = r'\*\*预置条件[：:]\*\*\s*\n((?:\d+\.\s+.+\n|-\s+.+\n)+)'
        match = re.search(pattern1, content)
        if match:
            cond_text = match.group(1)
            for line in re.findall(r'(?:\d+\.\s+|-\s+)(.+)', cond_text):
                preconditions.append(line.strip())

        if not preconditions:
            pattern2 = r'\*\*预置条件[：:]\*\*\s*\n\n((?:\d+\.\s+.+\n|-\s+.+\n)+)'
            match = re.search(pattern2, content)
            if match:
                cond_text = match.group(1)
                for line in re.findall(r'(?:\d+\.\s+|-\s+)(.+)', cond_text):
                    preconditions.append(line.strip())

        if not preconditions:
            pattern3 = r'\*\*预置条件[：:]\*\*\s*\n(.+?)(?:\n\n|\n\*\*测试步骤)'
            match = re.search(pattern3, content, re.DOTALL)
            if match:
                cond_text = match.group(1)
                for line in cond_text.strip().split('\n'):
                    line = line.strip()
                    if line and (re.match(r'\d+\.\s+', line) or re.match(r'-\s+', line)):
                        cleaned = re.sub(r'^\d+\.\s+|^- ', '', line).strip()
                        if cleaned:
                            preconditions.append(cleaned)

        return preconditions

    def _extract_steps(self, content: str) -> List[Dict]:
        """提取测试步骤（增强容错：兼容多种格式）

        支持格式：
        1. 单换行或双换行
        2. 表格分隔符不同格式
        """
        steps = []

        pattern1 = r'\*\*测试步骤[：:]\*\*\s*\n+\| 步骤 \|.*?\| 预期结果 \|\n\|[^|]+\|[^|]+\|[^|]+\|\n((?:\| .+ \|\n)+)'
        match = re.search(pattern1, content)
        if match:
            steps_text = match.group(1)
            for step_num, action, expected in re.findall(r'\| (\d+) \| (.+?) \| (.+?) \|', steps_text):
                steps.append({
                    "step": int(step_num),
                    "action": action.strip(),
                    "expected": expected.strip()
                })

        if not steps:
            pattern2 = r'\*\*测试步骤[：:]\*\*\s*\n+\|.*?步骤.*?\|.*?操作.*?\|.*?预期.*?\|\n(?:\|[^|]+\|[^|]+\|[^|]+\|\n)+((?:\| .+ \|\n)+)'
            match = re.search(pattern2, content, re.IGNORECASE)
            if match:
                steps_text = match.group(1)
                for parts in re.findall(r'\| (.+?) \| (.+?) \| (.+?) \|', steps_text):
                    try:
                        step_num = int(parts[0].strip())
                        steps.append({
                            "step": step_num,
                            "action": parts[1].strip(),
                            "expected": parts[2].strip()
                        })
                    except ValueError:
                        continue

        if not steps:
            pattern3 = r'\*\*测试步骤[：:]\*\*\s*\n(.+?)(?:\n\n|\n\*\*|\n---)'
            match = re.search(pattern3, content, re.DOTALL)
            if match:
                steps_text = match.group(1)
                for parts in re.findall(r'\| (.+?) \| (.+?) \| (.+?) \|', steps_text):
                    try:
                        step_num = int(parts[0].strip())
                        steps.append({
                            "step": step_num,
                            "action": parts[1].strip(),
                            "expected": parts[2].strip()
                        })
                    except ValueError:
                        continue

        return steps

    def _deduplicate_names(self, cases: List) -> List:
        name_count = {case.get('name', ''): 0 for case in cases}
        for case in cases:
            name_count[case.get('name', '')] += 1

        name_index = {}
        for case in cases:
            name = case.get('name', '')
            if name_count[name] > 1:
                name_index[name] = name_index.get(name, 0) + 1
                suffix = f"_V{name_index[name]}"
                case['name'] = f"{name}{suffix}"
        return cases

    def _detect_same_tp_multi_cases(self, cases: List) -> List[Dict]:
        """检测同一测试点下多个用例（同执行方式）的潜在冗余"""
        tp_to_cases = {}
        for case in cases:
            related_tp = case.get('related_tp', '')
            if not related_tp:
                continue
            tps = re.findall(r'(?:TP-[A-Z0-9\-]+|US\d+-TP\d+)', related_tp)
            for tp in tps:
                if tp not in tp_to_cases:
                    tp_to_cases[tp] = []
                tp_to_cases[tp].append(case)

        redundant_groups = []
        for tp, tp_cases in tp_to_cases.items():
            if len(tp_cases) <= 1:
                continue
            exec_groups = {}
            for c in tp_cases:
                em = c.get('exec_method', '')
                if em not in exec_groups:
                    exec_groups[em] = []
                exec_groups[em].append(c)
            for exec_method, group_cases in exec_groups.items():
                if len(group_cases) > 1:
                    redundant_groups.append({
                        "tp_id": tp,
                        "exec_method": exec_method,
                        "case_count": len(group_cases),
                        "case_ids": [c.get('id', '') for c in group_cases],
                        "case_names": [c.get('name', '') for c in group_cases],
                        "recommend_keep": group_cases[0].get('id', ''),
                        "recommend_merge_source": [c.get('id', '') for c in group_cases[1:]],
                        "reason": f"同一测试点{tp}下有{len(group_cases)}个同执行方式({exec_method})用例，应合并为1个"
                    })

        return redundant_groups

    def _generate_doc_cases(self, testpoint_path: str, all_cases: List[Dict] = None,
                            requirement_path: str = None) -> List[Dict]:
        """生成资料测试用例（存在public接口时生成一条）

        通用规则：只要存在 public 接口（requirement_analysis.md §2.3有API条目），就生成一条资料用例。
        这是本质条件——资料用例检视的是public接口文档，与是否有文档验证类US无关。

        关联测试点优先级：
        1. TP-DOC-xxx 测试点（如有）
        2. 文档验证类US编号（从requirement_analysis.md提取，如有）
        3. 所有public SDK API的关联测试点（兜底）

        只生成一条，不重复。
        """
        tp_content = self._read_file(testpoint_path)
        req_content = self._read_file(requirement_path) if requirement_path and os.path.isfile(requirement_path) else ""

        has_public_api = bool(re.search(r'^\| API-\d+', req_content, re.MULTILINE))

        if not has_public_api:
            return []

        doc_tps = re.findall(r'^\| ((?:TP-DOC-[A-Z0-9\-]+|US\d+-TP-DOC\d+))', tp_content, re.MULTILINE)
        doc_us_list = self._extract_doc_verification_us(requirement_path)
        public_api_ids = re.findall(r'^\| (API-\d+)\s*\|', req_content, re.MULTILINE)

        xts_tps = []
        if tp_content:
            xts_tps = re.findall(r'^\| (TP-[A-Z0-9\-]+)\s*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\| XTS', tp_content, re.MULTILINE)

        if doc_tps:
            related_tp_str = ", ".join(doc_tps) if len(doc_tps) <= 5 else f"所有资料测试点（{len(doc_tps)}个）"
        elif doc_us_list:
            related_tp_str = ", ".join(doc_us_list)
        elif xts_tps:
            related_tp_str = ", ".join(xts_tps) if len(xts_tps) <= 5 else f"所有XTS测试点（{len(xts_tps)}个）"
        elif public_api_ids:
            related_tp_str = ", ".join(public_api_ids) if len(public_api_ids) <= 5 else f"所有public接口（{len(public_api_ids)}个）"
        else:
            related_tp_str = "所有public接口"

        api_names = re.findall(r'^\| API-\d+\s*\|\s*(\S+)', req_content, re.MULTILINE)
        api_names_str = ", ".join(api_names) if api_names else "所有public接口"

        preconditions = [f"打开 {api_names_str} 接口涉及的API参考文档"]
        steps = [
            {"step": 1, "action": "检视接口签名与参数说明", "expected": "接口签名、参数类型、必填标注与d.ts一致，描述准确无歧义"},
            {"step": 2, "action": "检视错误码表与返回值说明", "expected": "错误码定义完整，触发条件与规格一致，返回值类型描述准确"},
            {"step": 3, "action": "检视示例代码", "expected": "示例代码可编译运行，覆盖典型用法"}
        ]

        return [{
            "id": "TC-DOC-001",
            "name": "接口资料检视",
            "test_type": "资料测试",
            "test_technique": "资料检视",
            "exec_method": "手工",
            "level": "P1",
            "source": "当前需求规格",
            "related_tp": related_tp_str,
            "preconditions": preconditions,
            "steps": steps
        }]

    def _extract_doc_verification_us(self, requirement_path: str) -> List[str]:
        """从requirement_analysis.md中提取文档验证类US

        匹配格式：
        - "文档验证类US: US-04，Phase4统一生成资料用例"
        - "文档验证类US: US-04, US-05"
        - "文档验证类US：US-04"
        """
        if not requirement_path or not os.path.isfile(requirement_path):
            return []

        req_content = self._read_file(requirement_path)
        if not req_content:
            return []

        match = re.search(r'文档验证类US[：:]\s*([A-Z0-9\-,\s]+?)(?:，|,|\n)', req_content)
        if not match:
            return []

        us_str = match.group(1).strip()
        us_list = [us.strip() for us in re.split(r'[,\s]+', us_str) if re.match(r'US-\d+', us.strip())]
        return us_list

    def _generate_stats_section(self, cases: List, testpoint_path: str) -> str:
        total = len(cases)
        level_dist = {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
        tech_dist, exec_dist, type_dist = {}, {}, {}
        covered_tps = set()

        for case in cases:
            level_dist[case.get('level', 'P2')] = level_dist.get(case.get('level', 'P2'), 0) + 1
            tech_dist[case.get('test_technique', '')] = tech_dist.get(case.get('test_technique', ''), 0) + 1
            exec_dist[case.get('exec_method', '')] = exec_dist.get(case.get('exec_method', ''), 0) + 1
            type_dist[case.get('test_type', '')] = type_dist.get(case.get('test_type', ''), 0) + 1
            tp = case.get('related_tp', '')
            if tp and (tp.startswith('TP-') or tp.startswith('US') and '-TP' in tp):
                covered_tps.add(tp)

        tp_content = self._read_file(testpoint_path)
        tp_total = len(re.findall(r'^\| ((?:TP-[A-Z0-9\-]+|US\d+-TP\d+))', tp_content, re.MULTILINE))
        coverage_rate = round(len(covered_tps) / tp_total * 100, 2) if tp_total > 0 else 0

        stats = f"""### 用例级别分布
- 测试用例总数：{total}个
  - P0：{level_dist.get('P0', 0)}个（{round(level_dist.get('P0', 0) / total * 100, 2) if total > 0 else 0}%）
  - P1：{level_dist.get('P1', 0)}个（{round(level_dist.get('P1', 0) / total * 100, 2) if total > 0 else 0}%）
  - P2：{level_dist.get('P2', 0)}个（{round(level_dist.get('P2', 0) / total * 100, 2) if total > 0 else 0}%）
  - P3：{level_dist.get('P3', 0)}个（{round(level_dist.get('P3', 0) / total * 100, 2) if total > 0 else 0}%）

### 测试技术分布
"""
        for tech, count in sorted(tech_dist.items()):
            stats += f"- {tech}：{count}个（{round(count / total * 100, 2) if total > 0 else 0}%）\n"

        stats += "\n### 执行方式分布\n"
        for exec_method, count in sorted(exec_dist.items()):
            stats += f"- {exec_method}：{count}个（{round(count / total * 100, 2) if total > 0 else 0}%）\n"

        stats += "\n### 测试类型分布\n"
        for test_type, count in sorted(type_dist.items()):
            stats += f"- {test_type}：{count}个（{round(count / total * 100, 2) if total > 0 else 0}%）\n"

        stats += f"""
### 覆盖率统计
- 测试点总数：{tp_total}个
- 已覆盖测试点：{len(covered_tps)}个
- 测试点覆盖率：{coverage_rate}%（阈值≥95%）
"""
        return stats

    def _format_case_detail(self, case: Dict) -> str:
        """格式化用例详细内容（紧凑格式，无多余空行）"""
        md = f"### {case['id']}-{case['name']}\n\n"
        md += f"**测试类型：** {case['test_type']}\n"
        md += f"**测试技术：** {case['test_technique']}\n"
        md += f"**执行方式：** {case['exec_method']}\n"
        md += f"**用例级别：** {case['level']}\n"
        md += f"**来源：** {case['source']}\n"
        md += f"**关联测试点：** {case['related_tp']}\n\n"
        md += "**预置条件：**\n"

        for precond in case.get('preconditions', []):
            md += f"- {precond}\n"

        md += "\n**测试步骤：**\n\n| 步骤 | 操作（含数据） | 预期结果 |\n| --- | ------------ | -------- |\n"
        for step in case.get('steps', []):
            md += f"| {step['step']} | {step['action']} | {step['expected']} |\n"

        md += "\n---\n\n"
        return md

    def validate_merged_md(self, md_path: str, testpoint_path: str) -> Dict:
        """校验合并后的MD完整性"""
        md_content = self._read_file(md_path)
        tp_content = self._read_file(testpoint_path)

        if not md_content:
            return {"valid": False, "errors": ["MD文件不存在或为空"], "case_count": 0, "tp_total": 0, "coverage": 0}

        # 支持多种格式：TC-XXX-名称、TC-batchXX-YYY-名称、TC-US01-001-名称（支持连字符、下划线）
        case_matches = re.findall(r'### (TC-[a-zA-Z0-9_\-]+)-(.+?)\n', md_content)
        case_count = len(case_matches)

        all_tps = re.findall(r'^\| ((?:TP-[A-Z0-9\-]+|US\d+-TP\d+))', tp_content, re.MULTILINE)
        tp_total = len(all_tps)

        covered_tps, name_set, errors = set(), set(), []

        for case_id, case_name in case_matches:
            # 提取当前用例的完整内容块
            case_start = md_content.find(f"### {case_id}-{case_name}")
            case_end = md_content.find("\n### ", case_start + 1)
            if case_end == -1:
                case_end = len(md_content)
            case_block = md_content[case_start:case_end]

            # 从case_block中提取关联测试点（支持多个TP逗号分隔，兼容中英文冒号）
            tp_line = re.findall(r'\*\*关联测试点[：:]\*\* (.+)', case_block)
            for line in tp_line:
                for tp in re.findall(r'TP-[A-Z0-9\-]+', line):
                    covered_tps.add(tp)

            if case_name in name_set:
                errors.append(f"用例名称重复: {case_name}")
            name_set.add(case_name)

            if "'" in case_name:
                errors.append(f"用例名称含单引号: {case_name}")

        coverage_rate = round(len(covered_tps) / tp_total * 100, 2) if tp_total > 0 else 0
        if coverage_rate < 95:
            errors.append(f"测试点覆盖率{coverage_rate}%低于阈值95%")

        missing_tps = [tp for tp in all_tps if tp not in covered_tps and not (
                    tp.startswith('TP-DOC') or tp.startswith('US') and '-TP-DOC' in tp)]

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "case_count": case_count,
            "tp_total": tp_total,
            "covered_tps": len(covered_tps),
            "coverage": coverage_rate,
            "missing_tps": missing_tps[:20]
        }

    def demo_map(self, demo_path: str) -> Dict:
        """Demo控件映射"""
        demo_content = self._read_file(demo_path)
        if not demo_content:
            return {"controls": [], "total": 0}

        controls = []
        for m in re.finditer(r'^\| ([a-z_][a-z0-9_]+).*?\| (.+?) \|.*?\| (.+?) \|', demo_content, re.MULTILINE):
            controls.append({
                "id": m.group(1),
                "label": m.group(2),
                "type": self._map_control_type(m.group(3)),
                "area": self._infer_area(m.group(1))
            })

        return {"controls": controls, "total": len(controls)}

    def _map_control_type(self, type_raw: str) -> str:
        type_map = {"select": "下拉框", "input": "输入框", "textarea": "文本域", "toggle": "开关", "btn": "按钮",
                    "button": "按钮"}
        for key, value in type_map.items():
            if key in type_raw.lower():
                return value
        return type_raw

    def _infer_area(self, control_id: str) -> str:
        if any(p in control_id for p in ["select", "input", "textarea", "toggle"]):
            return "输入区"
        if "btn" in control_id:
            return "操作区"
        if any(p in control_id for p in ["result", "status"]):
            return "结果区"
        if "log" in control_id:
            return "日志区"
        return "未知区域"

    def coverage_check(self, testcases_path: str, testpoint_path: str, output_path: str = None) -> Dict:
        """覆盖率矩阵检查（测试点覆盖率+关键测试点覆盖率）"""

        tc_content = self._read_file(testcases_path)
        tp_content = self._read_file(testpoint_path)

        if not tc_content:
            return {"status": "error", "message": f"测试用例文件不存在: {testcases_path}"}
        if not tp_content:
            return {"status": "error", "message": f"测试点文件不存在: {testpoint_path}"}

        # 提取所有测试点ID（支持多种格式）
        tp_matches = re.findall(r'^\| ((?:TP-[A-Z0-9\-]+|US\d+-TP\d+))', tp_content, re.MULTILINE)
        all_tps = set(tp_matches)

        # 提取关键测试点（P0/P1级）
        critical_tps = set()
        tp_priority_pattern = r'^\| (TP-[A-Z0-9\-]+|US\d+-TP\d+)\s*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\| (P0|P1)'
        for match in re.findall(tp_priority_pattern, tp_content, re.MULTILINE):
            critical_tps.add(match[0])

        # 从测试用例文件提取关联测试点
        covered_tps = set()
        covered_critical_tps = set()

        # 格式：**关联测试点：** TP-xxx 或表格中提取（支持逗号分隔多TP）
        tc_tp_pattern = r'\*\*关联测试点[：:]\*\* (.+)'
        for match in re.findall(tc_tp_pattern, tc_content):
            for tp_id in re.findall(r'TP-[A-Z0-9\-]+', match):
                covered_tps.add(tp_id)
                if tp_id in critical_tps:
                    covered_critical_tps.add(tp_id)

        # 计算覆盖率
        tp_total = len(all_tps)
        critical_total = len(critical_tps)

        tp_coverage = round(len(covered_tps) / tp_total * 100, 2) if tp_total > 0 else 100.0
        critical_coverage = round(len(covered_critical_tps) / critical_total * 100, 2) if critical_total > 0 else 100.0

        # 判断是否通过
        tp_pass = tp_coverage >= 95
        critical_pass = critical_coverage >= 98
        overall_pass = tp_pass and critical_pass

        result = {
            "status": "success",
            "coverage_matrix": {
                "testpoint": {
                    "total": tp_total,
                    "covered": len(covered_tps),
                    "coverage": tp_coverage,
                    "pass": tp_pass,
                    "threshold": 95
                },
                "critical_testpoint": {
                    "total": critical_total,
                    "covered": len(covered_critical_tps),
                    "coverage": critical_coverage,
                    "pass": critical_pass,
                    "threshold": 98
                }
            },
            "uncovered_tps": list(all_tps - covered_tps)[:30],
            "uncovered_critical_tps": list(critical_tps - covered_critical_tps)[:20],
            "overall_pass": overall_pass,
            "validation_summary": {
                "testpoint_coverage_pass": tp_pass,
                "critical_testpoint_coverage_pass": critical_pass
            }
        }

        if output_path:
            try:
                output_dir = os.path.dirname(output_path)
                if output_dir and not os.path.isdir(output_dir):
                    os.makedirs(output_dir, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
            except Exception as e:
                return {"status": "error", "message": f"写入覆盖率检查结果失败: {str(e)}"}

        return result


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description='Phase4测试用例细化辅助工具')
    parser.add_argument('--action', required=True,
                        choices=['merge_batch_mds', 'validate_merged_md', 'coverage_check', 'demo_map'],
                        help='执行动作')
    parser.add_argument('--testpoint', help='test_point_design.md路径')
    parser.add_argument('--requirement', help='requirement_analysis.md路径(merge_batch_mds)')
    parser.add_argument('--batch-dir', help='批次MD文件目录(merge_batch_mds)')
    parser.add_argument('--md', help='test_cases.md路径(validate_merged_md/coverage_check)')
    parser.add_argument('--demo', help='demo_design.md路径(demo_map)')
    parser.add_argument('--output', required=True, help='输出路径')
    args = parser.parse_args()

    utils = Phase4TestcaseUtils()
    result = None

    if args.action == 'merge_batch_mds':
        if not args.batch_dir or not args.testpoint:
            print(json.dumps({"status": "error", "message": "缺少--batch-dir或--testpoint参数"}, ensure_ascii=False))
            sys.exit(1)
        result = utils.merge_batch_mds(args.batch_dir, args.testpoint, args.output,
                                        requirement_path=args.requirement)
        print(json.dumps(result, ensure_ascii=False))
        return

    elif args.action == 'validate_merged_md':
        if not args.md or not args.testpoint:
            print(json.dumps({"status": "error", "message": "缺少--md或--testpoint参数"}, ensure_ascii=False))
            sys.exit(1)
        result = utils.validate_merged_md(args.md, args.testpoint)

    elif args.action == 'coverage_check':
        if not args.md or not args.testpoint:
            print(json.dumps({"status": "error", "message": "缺少--md或--testpoint参数"}, ensure_ascii=False))
            sys.exit(1)
        result = utils.coverage_check(args.md, args.testpoint, args.output)

    elif args.action == 'demo_map':
        if not args.demo:
            print(json.dumps({"status": "error", "message": "缺少--demo参数"}, ensure_ascii=False))
            sys.exit(1)
        result = utils.demo_map(args.demo)

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(json.dumps({"status": "success", "output": args.output}, ensure_ascii=False))


if __name__ == '__main__':
    main()
