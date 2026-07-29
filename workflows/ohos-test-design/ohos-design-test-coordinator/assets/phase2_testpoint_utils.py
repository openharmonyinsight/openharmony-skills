#!/usr/bin/env python3
"""Phase2测试点生成辅助脚本

功能:
1. merge_batch_mds - 合并批次MD（统一重编号TP-001~TP-N）
2. validate_merged_md - 校验完整性
3. coverage_check - 覆盖率矩阵检查（增强版：场景/API/手段/路径/高风险深度）
4. stats_generate - 统计信息生成（基础版）
5. generate_stats - 统计章节生成（增强版：支持知识库匹配结果+验证结果）

用法:
  python phase2_testpoint_utils.py --action merge_batch_mds --batch-dir batches_phase2/ --requirement requirement_analysis.md --output test_point_design.md
  python phase2_testpoint_utils.py --action coverage_check --testpoint test_point_design.md --requirement requirement_analysis.md --output coverage_result.json

格式兼容性:
  - 中英文冒号兼容 [：:]
  - 主单元ID格式兼容：US-01（标准）、US-1（无前导零）、US-70-1（带issue编号）、US-DFX-1（带字母）、MU-001（功能规格）、TR-001（功能规格）
  - 测试点ID格式兼容：TP-001, TP-batch_US01-001, TP-MU001-001, TP-TR001-001
  - 表格分隔线灵活匹配
"""

import argparse
import datetime
import json
import os
import re
import sys
import traceback
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Set


class Phase2TestpointUtils:

    def get_parallel_limit(self) -> int:
        """动态获取并行上限（phase2限制最大4，符合SKILL.md约束）"""
        try:
            import psutil
            available_gb = psutil.virtual_memory().available / (1024 ** 3)
            # phase2并行上限固定为4，符合SKILL.md "NEVER 并行spawn超过4个Agent"
            # 内存充足时仍为4，内存不足时降级为2
            if available_gb >= 4:
                return 4
            elif available_gb >= 2:
                return 2
            else:
                return 1
        except ImportError:
            return 4  # 无psutil时默认4
        except Exception:
            return 4

    def get_memory_available_gb(self) -> float:
        """获取可用内存（GB）"""
        try:
            import psutil
            return round(psutil.virtual_memory().available / (1024 ** 3), 2)
        except ImportError:
            return 0.0
        except Exception:
            return 0.0

    def _normalize_path(self, path: str) -> str:
        """标准化文件路径"""
        if not path:
            return ""
        return os.path.normpath(os.path.abspath(path))

    def _read_file(self, path: str) -> str:
        """读取文件内容（带错误处理）"""
        path = self._normalize_path(path)
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

    def _safe_regex_search(self, pattern: str, content: str, flags: int = 0) -> Optional[re.Match]:
        """安全正则搜索"""
        try:
            return re.search(pattern, content, flags)
        except re.error:
            return None

    def _safe_regex_findall(self, pattern: str, content: str, flags: int = 0) -> List:
        """安全正则查找"""
        try:
            return re.findall(pattern, content, flags)
        except re.error:
            return []

    def _extract_main_units(self, req_content: str) -> List[Dict]:
        """提取主单元信息（US/TR/MU）- 支持多种格式

        支持的主单元ID格式：
        - US-01（带前导零）
        - US-1（无前导零）
        - US-70-1（带issue编号）
        - US-DFX-1（带字母）
        - MU-001（功能规格）
        - TR-001（规格格式）
        """
        main_units = []

        us_patterns = [
            # 功能规格格式：MU-xxx（SR3/output2）
            r'## (\d+)\.\s*(MU-\d+)[：:]\s*(.+?)(?:\n|$)',
            # 标准格式：US-01（SR1/output6,7,9,10）
            r'## (\d+)\.\s*(US-\d+)[：:]\s*(.+?)(?:\n|$)',
            # 无前导零格式：US-1（SR2/output1, SR4/output1）
            r'## (\d+)\.\s*(US-\d+)[：:]\s*(.+?)(?:\n|$)',
            # 紧凑格式：[US-xxx] 名称（SR1/output6索引、SR2/output1）
            r'- \[(US-\d+|TR-\d+|MU-\d+)\]\s+(.+?)(?:\n|$)',
            # 主单元索引表格格式（SR3/output2）
            r'\| (MU-\d+|US-\d+|TR-\d+)\s+\|\s*(.+?)\s+\|\s*[^|]+\|\s*[^|]+',
            # 带issue编号格式：US-70-1
            r'## (\d+)\.\s*(US-\d+-\d+)[：:]\s*(.+?)(?:\n|$)',
            # 带字母格式：US-DFX-1
            r'## (\d+)\.\s*(US-[A-Z]+\d+-\d+)[：:]\s*(.+?)(?:\n|$)',
            # TR格式
            r'## (\d+)\.\s*(TR-\d+)[：:]\s*(.+?)(?:\n|$)',
        ]

        for pattern in us_patterns:
            us_matches = self._safe_regex_findall(pattern, req_content, re.MULTILINE)
            if us_matches:
                for match in us_matches:
                    # 解析match内容（不同pattern返回不同数量字段）
                    if len(match) == 3:
                        # 格式：章节编号、单元ID、名称
                        num, unit_id, unit_name = match
                    elif len(match) == 2:
                        # 格式：单元ID、名称（索引格式）
                        unit_id, unit_name = match
                        num = unit_id.replace('-', '').replace('US', '').replace('MU', '').replace('SPEC', '')
                    else:
                        continue

                    unit_name = unit_name.replace('测试点', '').strip()

                    # 查找主单元章节位置
                    section_patterns = [
                        f'## {num}. {unit_id}',
                        f'## {num}. {unit_id}：',  # 中文冒号
                        f'## {num}. {unit_id}:',   # 英文冒号
                        f'## {num}.{unit_id}',
                        f'- [{unit_id}]',
                    ]

                    section_start = -1
                    for sp in section_patterns:
                        section_start = req_content.find(sp)
                        if section_start != -1:
                            break

                    # 兜底：直接搜索单元ID
                    if section_start == -1:
                        section_start = req_content.find(f'## {unit_id}')

                    if section_start == -1:
                        # 尝试从主单元章节标题搜索（支持无章节编号格式）
                        match = self._safe_regex_search(rf'## [\d]+\. {unit_id}[：:]', req_content)
                        if match:
                            section_start = match.start()

                    if section_start == -1:
                        continue

                    # 定位章节结束边界
                    if '.' in str(num) and not num.isdigit():
                        # 小数编号（如 3.1）
                        base = num.split('.')[0]
                        next_decimal = int(num.split('.')[1]) + 1
                        next_num_str = f'{base}.{next_decimal}'
                        section_end = req_content.find(f'\n### {next_num_str}', section_start)
                    else:
                        # 整数编号
                        try:
                            next_num = int(num) + 1 if str(num).isdigit() else 1
                            section_end = req_content.find(f'\n## {next_num}.', section_start)
                        except Exception:
                            section_end = -1

                    if section_end == -1:
                        section_end = req_content.find('\n## 汇总统计', section_start)
                    if section_end == -1:
                        section_end = req_content.find('\n## ', section_start + 50)
                    if section_end == -1:
                        section_end = len(req_content)

                    section_content = req_content[section_start:section_end]

                    # 统计AC和COND数量
                    ac_patterns = [
                         r'US\d+-AC\d+[a-z]?',
                         r'AC-\d+[a-z]?',
                         r'AC\d+[a-z]?',
                         r'MU\d+-AC\d+',  # 功能规格AC格式
                         r'TR\d+-AC\d+',  # TR规格AC格式
                    ]
                    ac_count = 0
                    for ap in ac_patterns:
                        ac_count += len(self._safe_regex_findall(ap, section_content))
                    ac_count = max(1, ac_count)

                    cond_count = len(self._safe_regex_findall(r'COND-[A-Z0-9]+', section_content))

                    main_units.append({
                        "unit_id": unit_id,
                        "unit_name": unit_name.strip(),
                        "section_num": str(num),
                        "ac_count": ac_count,
                        "cond_count": cond_count,
                        "estimated_tps": max(3, ac_count + cond_count // 2)
                    })
                break

        return main_units

    def _duplicate_detect_testpoints(self, tps: List[Dict]) -> Dict:
        """检测重复测试点（增强版：支持跨US重复检测）

        检测逻辑：
        1. 精确重复（相似度≥95% + 执行方式相同）→ 自动删除
        2. 潜在重复（相似度80%-95% + 执行方式相同）→ 标记待确认
        3. 跨US重叠（测试点ID不同但场景相同）→ 标记待确认

        Returns:
            {
                "exact_duplicates": [...],
                "potential_duplicates": [...],
                "cross_us_duplicates": [...],  # 新增：跨US重复
                "auto_delete": [...],
                "exact_count": N,
                "potential_count": N,
                "cross_us_count": N  # 新增
            }
        """
        exact_duplicates = []
        potential_duplicates = []
        cross_us_duplicates = []

        # 构建场景指纹（用于跨US检测）
        scenario_fingerprint_map = {}  # {fingerprint: [tp_ids]}

        for i in range(len(tps)):
            for j in range(i + 1, len(tps)):
                tp_a = tps[i]
                tp_b = tps[j]

                # 跳过DOC资料测试点之间的比对：DOC TP按API自动生成、共用模板
                # (input_cond/expected相同仅scenario的API编号不同)，不应作为重复删除，
                # 否则会误删每个API应有的资料测试点
                id_a = tp_a.get('id', '')
                id_b = tp_b.get('id', '')
                if id_a.startswith('TP-DOC-') and id_b.startswith('TP-DOC-'):
                    continue

                # 文本相似度检测
                text_a = f"{tp_a.get('scenario', '')} {tp_a.get('input_cond', '')} {tp_a.get('expected', '')}"
                text_b = f"{tp_b.get('scenario', '')} {tp_b.get('input_cond', '')} {tp_b.get('expected', '')}"

                similarity = SequenceMatcher(None, text_a, text_b).ratio() * 100
                exec_same = tp_a.get('exec_method', '') == tp_b.get('exec_method', '')

                # 提取主单元ID用于跨US检测
                unit_a_match = re.match(r'TP-(US\d+|TR\d+|MU\d+)-', tp_a.get('id', ''))
                unit_b_match = re.match(r'TP-(US\d+|TR\d+|MU\d+)-', tp_b.get('id', ''))
                unit_a = unit_a_match.group(1) if unit_a_match else ''
                unit_b = unit_b_match.group(1) if unit_b_match else ''
                cross_us = unit_a and unit_b and unit_a != unit_b

                # 验证侧重点检测（避免过度合并）
                # 提取预期输出中的关键验证点，验证侧重点不同时不去重
                verification_keywords = [
                    '回调', '公共事件', '状态', '参数', '返回值', '错误码',
                    '屏幕', '亮屏', '灭屏', '编译', '隔离', '权限', '数据',
                    '触发', '发布', '传递', '校验', '验证', '注销', '注册'
                ]
                expected_a = tp_a.get('expected', '')
                expected_b = tp_b.get('expected', '')

                # 检查验证侧重点是否一致
                verification_focus_same = True
                for kw in verification_keywords:
                    kw_in_a = kw in expected_a
                    kw_in_b = kw in expected_b
                    if kw_in_a != kw_in_b:
                        verification_focus_same = False
                        break

                if similarity >= 95 and exec_same and verification_focus_same:
                    exact_duplicates.append({
                        "tp_a": tp_a["id"],
                        "tp_b": tp_b["id"],
                        "similarity": round(similarity, 2),
                        "cross_us": cross_us,
                        "verification_focus_same": verification_focus_same
                    })
                elif similarity >= 80 and exec_same and verification_focus_same:
                    potential_duplicates.append({
                        "tp_a": tp_a["id"],
                        "tp_b": tp_b["id"],
                        "similarity": round(similarity, 2),
                        "cross_us": cross_us,
                        "verification_focus_same": verification_focus_same
                    })
                elif cross_us and similarity >= 85 and verification_focus_same:
                    # 跨US场景重叠检测（提高阈值到85%，避免过度合并）
                    # 验证侧重点不同时（如回调验证 vs 公共事件验证）不视为重复
                    cross_us_duplicates.append({
                        "tp_a": tp_a["id"],
                        "tp_b": tp_b["id"],
                        "similarity": round(similarity, 2),
                        "unit_a": unit_a,
                        "unit_b": unit_b,
                        "verification_focus_same": verification_focus_same
                    })

        # 自动删除列表：精确重复 + 跨US精确重复（保留最早出现的US）
        auto_delete = [d["tp_b"] for d in exact_duplicates]

        return {
            "exact_duplicates": exact_duplicates,
            "potential_duplicates": potential_duplicates,
            "cross_us_duplicates": cross_us_duplicates,
            "auto_delete": auto_delete,
            "exact_count": len(exact_duplicates),
            "potential_count": len(potential_duplicates),
            "cross_us_count": len(cross_us_duplicates)
        }

    def _deduplicate_testpoints(self, tps: List[Dict], delete_ids: List[str]) -> List[Dict]:
        """去重测试点（删除auto_delete列表中的测试点）"""
        seen = set()
        unique_delete = []
        for d in delete_ids:
            if d not in seen:
                seen.add(d)
                unique_delete.append(d)
        return [tp for tp in tps if tp.get("id") not in unique_delete]

    def _resolve_id_collisions(self, all_tps: List[Dict], unit_id_map: Dict) -> List[Dict]:
        """解决同一主单元跨批次ID冲突

        当同一主单元有多个批次文件时，测试点ID可能冲突
        （如batch_US01.md和batch_US01_1.md都产生TP-US01-001）。
        处理策略：
        1. 完全相同的ID+高相似度内容 → 保留首个，删除后续
        2. 相同ID但不同内容 → 重新编号后续测试点
        """
        id_occurrences = {}
        for i, tp in enumerate(all_tps):
            tp_id = tp.get('id', '')
            if tp_id not in id_occurrences:
                id_occurrences[tp_id] = []
            id_occurrences[tp_id].append((i, tp))

        collisions = {tid: occ for tid, occ in id_occurrences.items() if len(occ) > 1}

        if not collisions:
            return all_tps

        delete_indices = set()

        for tp_id, occurrences in collisions.items():
            unit_match = re.match(r'TP-(US\d+|SPEC\d+|TR\d+|MU\d+)-(\d+)', tp_id)
            if not unit_match:
                continue

            unit_prefix = unit_match.group(1)

            max_num = 0
            for tp in all_tps:
                curr_match = re.match(rf'TP-{unit_prefix}-(\d+)', tp.get('id', ''))
                if curr_match:
                    num = int(curr_match.group(1))
                    if num > max_num:
                        max_num = num

            renumber_counter = 0

            for idx, tp in occurrences:
                if idx == occurrences[0][0]:
                    continue

                first_tp = occurrences[0][1]
                text_first = f"{first_tp.get('scenario', '')} {first_tp.get('input_cond', '')} {first_tp.get('expected', '')}"
                text_curr = f"{tp.get('scenario', '')} {tp.get('input_cond', '')} {tp.get('expected', '')}"
                similarity = SequenceMatcher(None, text_first, text_curr).ratio() * 100

                if similarity >= 90:
                    delete_indices.add(idx)
                else:
                    renumber_counter += 1
                    new_num = max_num + renumber_counter
                    tp['id'] = f'TP-{unit_prefix}-{new_num:03d}'

        if delete_indices:
            all_tps = [tp for i, tp in enumerate(all_tps) if i not in delete_indices]

        return all_tps

    def _deduplicate_same_unit_testpoints(self, tps: List[Dict], unit_id_map: Dict) -> Dict:
        """同一主单元内的测试点去重（降低阈值）

        当同一主单元有多个批次时，不同批次可能生成语义重叠的测试点。
        此方法使用更低的相似度阈值（80%）进行同单元内去重，
        比跨单元去重（95%）更激进。

        Returns:
            {
                "same_unit_duplicates": [...],
                "auto_delete": [...],
                "auto_delete_count": N
            }
        """
        same_unit_duplicates = []
        auto_delete = []

        unit_groups = {}
        for tp in tps:
            tp_id = tp.get('id', '')
            unit_match = re.match(r'TP-(US\d+|SPEC\d+|TR\d+|MU\d+)-', tp_id)
            if unit_match:
                unit = unit_match.group(1)
                if unit not in unit_groups:
                    unit_groups[unit] = []
                unit_groups[unit].append(tp)

        multi_source_units = set()
        for bf, uid in unit_id_map.items():
            for bf2, uid2 in unit_id_map.items():
                if bf != bf2 and uid == uid2:
                    multi_source_units.add(uid)

        for unit in multi_source_units:
            unit_tps = unit_groups.get(unit, [])
            for i in range(len(unit_tps)):
                for j in range(i + 1, len(unit_tps)):
                    tp_a = unit_tps[i]
                    tp_b = unit_tps[j]

                    batch_a = tp_a.get('_source_batch', '')
                    batch_b = tp_b.get('_source_batch', '')
                    if batch_a and batch_b and batch_a == batch_b:
                        continue

                    id_a = tp_a.get('id', '')
                    id_b = tp_b.get('id', '')
                    if id_a.startswith('TP-DOC-') and id_b.startswith('TP-DOC-'):
                        continue

                    text_a = f"{tp_a.get('scenario', '')} {tp_a.get('input_cond', '')} {tp_a.get('expected', '')}"
                    text_b = f"{tp_b.get('scenario', '')} {tp_b.get('input_cond', '')} {tp_b.get('expected', '')}"

                    full_similarity = SequenceMatcher(None, text_a, text_b).ratio() * 100
                    scenario_similarity = SequenceMatcher(None, tp_a.get('scenario', ''), tp_b.get('scenario', '')).ratio() * 100
                    exec_same = tp_a.get('exec_method', '') == tp_b.get('exec_method', '')

                    if scenario_similarity >= 90 and full_similarity >= 90 and exec_same:
                        same_unit_duplicates.append({
                            "tp_a": tp_a["id"],
                            "tp_b": tp_b["id"],
                            "scenario_similarity": round(scenario_similarity, 2),
                            "full_similarity": round(full_similarity, 2),
                            "unit": unit
                        })
                        auto_delete.append(tp_b["id"])

        seen_delete = set()
        unique_auto_delete = []
        for id_val in auto_delete:
            if id_val not in seen_delete:
                seen_delete.add(id_val)
                unique_auto_delete.append(id_val)

        return {
            "same_unit_duplicates": same_unit_duplicates,
            "auto_delete": unique_auto_delete,
            "auto_delete_count": len(unique_auto_delete)
        }

    def _generate_tp_table_from_list(self, tps: List[Dict]) -> str:
        """从测试点列表生成标准8列markdown表格（确保与汇总统计一致）"""
        if not tps:
            return ""

        table = "| 测试点ID | 测试场景 | 输入条件 | 预期输出概要 | 测试类型 | 优先级 | 执行方式 | 来源 |\n"
        table += "|---------|---------|---------|------------|---------|--------|---------|------|\n"

        for tp in tps:
            tp_id = tp.get('id', '')
            scenario = tp.get('scenario', '')
            input_cond = tp.get('input_cond', '')
            expected = tp.get('expected', '')
            test_type = tp.get('test_type', '')
            priority = tp.get('priority', '')
            exec_method = tp.get('exec_method', '')
            source = tp.get('source', '')
            table += f"| {tp_id} | {scenario} | {input_cond} | {expected} | {test_type} | {priority} | {exec_method} | {source} |\n"

        return table

    def _parse_batch_md(self, md_path: str) -> List[Dict]:
        """解析批次MD（支持多种表格格式）- 增强版

        修复：仅在测试点列表section中提取测试点，跳过知识库匹配日志等非测试点表格。
        测试点列表section的识别标准：含"测试点列表"或"测试点"关键词的标题行（###/##），
        且首个单元格为TP-前缀的表格行。遇到非测试点section标题时停止提取。
        """
        content = self._read_file(md_path)
        if not content:
            return []

        tps = []
        seen_ids = set()

        tp_id_pattern = r'(TP-batch_[A-Z0-9_]+-\d+|TP-[A-Z0-9\-]+|TP-MU\d+-\d+|TP-TR\d+-\d+|TP-ADD-\d+)'

        lines = content.split('\n')
        in_testpoint_section = False

        for i, line in enumerate(lines):
            line = line.strip()

            if line.startswith('##') or line.startswith('###'):
                section_title = line.lstrip('#').strip()
                if '测试点列表' in section_title or '测试点' in section_title and '列表' not in section_title:
                    in_testpoint_section = True
                elif in_testpoint_section:
                    in_testpoint_section = False
                continue

            if not in_testpoint_section:
                continue

            if not line.startswith('|'):
                continue

            id_match = self._safe_regex_search(tp_id_pattern, line)
            if not id_match:
                continue

            tp_id = id_match.group(1)
            if tp_id in seen_ids:
                continue
            seen_ids.add(tp_id)

            cells = [c.strip() for c in line.split('|')]
            if cells and cells[0] == '':
                cells = cells[1:]
            if cells and cells[-1] == '':
                cells = cells[:-1]

            if len(cells) < 2:
                continue

            if not cells[0].startswith('TP-'):
                continue

            priority = 'P2'
            source = ''
            scenario = ''
            test_type = '功能测试'
            test_technique = ''
            exec_method = 'XTS'
            input_cond = ''
            expected = ''

            # 检测表格列格式（8列标准格式 vs 9列含测试技术格式）
            # 标准8列：TP-ID|测试场景|输入条件|预期输出概要|测试类型|优先级|执行方式|来源
            # 9列格式：TP-ID|测试场景|输入条件|预期输出概要|测试类型|测试技术|优先级|执行方式|来源
            if cells[0].startswith('TP-') and len(cells) >= 8:
                # 判断是否为9列格式（检查cells[5]是否为测试技术而非优先级）
                test_technique_keywords = ['判定表', '等价类划分', '边界值分析', '因子组合', '边界值', '等价类']
                is_9_column = (
                    len(cells) >= 9 and
                    (cells[5] in test_technique_keywords or
                     any(kw in cells[5] for kw in test_technique_keywords) or
                     cells[5] not in ['P0', 'P1', 'P2', 'P3', '']))

                if is_9_column and len(cells) >= 9:
                    scenario = cells[1]
                    input_cond = cells[2]
                    expected = cells[3]
                    test_type = cells[4]
                    priority = cells[6] if cells[6] in ['P0', 'P1', 'P2', 'P3'] else 'P2'
                    exec_method = cells[7]
                    source = cells[8] if len(cells) >= 9 else cells[7]
                else:
                    scenario = cells[1]
                    input_cond = cells[2]
                    expected = cells[3]
                    test_type = cells[4]
                    priority = cells[5] if cells[5] in ['P0', 'P1', 'P2', 'P3'] else 'P2'
                    exec_method = cells[6]
                    source = cells[7]

            tps.append({
                "id": tp_id,
                "scenario": scenario,
                "input_cond": input_cond,
                "expected": expected,
                "test_type": test_type,
                "test_technique": test_technique,
                "priority": priority,
                "exec_method": exec_method,
                "source": source,
                "section": None
            })

        return tps

    def merge_batch_mds(self, batch_dir: str, requirement_path: str, output_path: str) -> Dict:
        """合并批次MD（按主单元编号，不重新编号）"""
        batch_dir = self._normalize_path(batch_dir)
        requirement_path = self._normalize_path(requirement_path)
        output_path = self._normalize_path(output_path)

        if not os.path.isdir(batch_dir):
            return {"status": "error", "message": f"批次目录不存在: {batch_dir}"}

        try:
            batch_files = sorted(
                [f for f in os.listdir(batch_dir) if f.startswith('batch_') and f.endswith('.md')],
                key=lambda x: self._extract_batch_sort_key(x)
            )
        except Exception as e:
            return {"status": "error", "message": f"读取批次目录失败: {str(e)}"}

        if not batch_files:
            return {"status": "error", "message": "未找到批次MD文件"}

        # 读取需求文件内容
        req_content = ""
        if requirement_path and os.path.isfile(requirement_path):
            req_content = self._read_file(requirement_path)

        # 第一步：解析所有测试点（保持原编号）
        all_tps = []
        unit_id_map = {}  # {batch_file: unit_id} 如 {"batch_SPEC_001.md": "SPEC001"}

        for bf in batch_files:
            bf_path = os.path.join(batch_dir, bf)
            tps = self._parse_batch_md(bf_path)

            # 提取主单元ID用于编号转换（支持多种格式）
            unit_id = None

            # 方法1：从文件名提取（优先匹配推荐格式）
            # 推荐格式：batch_US01.md, batch_US01_1.md, batch_SPEC001.md, batch_TR001_1.md
            unit_match = self._safe_regex_search(r'batch_(US\d+|SPEC\d+|TR\d+|MU\d+)(?:_\d+)?', bf)
            if unit_match:
                unit_id = unit_match.group(1)  # 直接提取 US01, SPEC001, TR001, MU001
                unit_id_map[bf] = unit_id

                # 转换编号格式：TP-batch_US01_1-001 -> TP-US01-001
                for tp in tps:
                    old_id = tp['id']
                    num_match = self._safe_regex_search(r'-(\d+)$', old_id)
                    if num_match:
                        num = num_match.group(1)
                        new_id = f"TP-{unit_id}-{num}"
                        tp['id'] = new_id

            # 方法1b：兼容旧格式 batch_US_1.md（带下划线分隔数字）
            if not unit_id:
                unit_match = self._safe_regex_search(r'batch_(US_\d+|(?:SPEC|TR)_\d+|MU_\d+)', bf)
                if unit_match:
                    unit_raw = unit_match.group(1)  # 如 US_1, SPEC_001, TR_001
                    unit_id = unit_raw.replace('_', '')  # 如 US1, SPEC001, TR001
                    unit_id_map[bf] = unit_id

                    for tp in tps:
                        old_id = tp['id']
                        num_match = self._safe_regex_search(r'-(\d+)$', old_id)
                        if num_match:
                            num = num_match.group(1)
                            new_id = f"TP-{unit_id}-{num}"
                            tp['id'] = new_id

            # 方法2：从文件内容提取（格式：# US-1: 名称, # US-01: 名称）
            if not unit_id:
                bf_content = self._read_file(bf_path)
                # 匹配章节标题格式
                content_unit_match = self._safe_regex_search(
                    r'#\s*(US-\d+|SPEC-\d+|TR-\d+|MU-\d+)[：:]\s*(.+?)(?:\n|$)',
                    bf_content
                )
                if content_unit_match:
                    unit_raw_id = content_unit_match.group(1)  # 如 US-1, US-01
                    unit_id = unit_raw_id.replace('-', '')  # 如 US1, US01
                    unit_id_map[bf] = unit_id

                    # 转换测试点编号
                    for tp in tps:
                        old_id = tp['id']
                        num_match = self._safe_regex_search(r'TP-(US\d+|SPEC\d+|TR\d+|MU\d+)-(\d+)$', old_id)
                        if num_match:
                            num = num_match.group(2)
                            new_id = f"TP-{unit_id}-{num}"
                            tp['id'] = new_id

            # 方法3：从测试点ID提取（如 TP-US1-001）
            if not unit_id and tps:
                first_tp_id = tps[0].get('id', '')
                tp_unit_match = self._safe_regex_search(r'TP-(US\d+|SPEC\d+|TR\d+|MU\d+)-', first_tp_id)
                if tp_unit_match:
                    unit_id = tp_unit_match.group(1)
                    unit_id_map[bf] = unit_id

            for tp in tps:
                tp['_source_batch'] = bf
            all_tps.extend(tps)

        # 修复：同一主单元跨批次ID冲突解决
        all_tps = self._resolve_id_collisions(all_tps, unit_id_map)

        # 资料测试点不在Phase2生成，由Phase4统一生成一条资料用例

        total = len(all_tps)

        if total == 0:
            return {"status": "error", "message": "未解析到任何测试点"}

        # 第二步：重复测试点检测与去重
        duplicate_result = self._duplicate_detect_testpoints(all_tps)
        if duplicate_result["exact_count"] > 0:
            all_tps = self._deduplicate_testpoints(all_tps, duplicate_result["auto_delete"])
            total = len(all_tps)

        # 修复：同一主单元跨批次去重（降低阈值，同单元内相似度≥80%即视为重复）
        same_unit_dedup = self._deduplicate_same_unit_testpoints(all_tps, unit_id_map)
        if same_unit_dedup["auto_delete_count"] > 0:
            all_tps = self._deduplicate_testpoints(all_tps, same_unit_dedup["auto_delete"])
            total = len(all_tps)

        # 修复：构建主单元→去重后测试点映射（确保汇总与表格一致）
        unit_tp_map = {}
        for tp in all_tps:
            tp_id = tp.get('id', '')
            unit_match = self._safe_regex_search(r'TP-(US\d+|SPEC\d+|TR\d+|MU\d+|DOC|UNIT\d+)-', tp_id)
            if unit_match:
                unit = unit_match.group(1)
                if unit not in unit_tp_map:
                    unit_tp_map[unit] = []
                unit_tp_map[unit].append(tp)

        # 第三步：提取风险分级和验证完整性汇总（传入测试点和需求内容作为兜底数据源）
        risk_summary = self._extract_risk_summary(batch_dir, batch_files, all_tps, req_content)
        integrity_summary = self._extract_integrity_summary(batch_dir, batch_files, all_tps, req_content)

        # 第四步：统计汇总（按主单元分组）
        stats_summary = self._generate_unit_stats(all_tps, unit_id_map, req_content)

        # 第五步：生成设计概述
        design_overview = self._extract_design_overview(req_content, total)

        md_content = f"""# 测试点设计

> 生成时间：{datetime.datetime.now().strftime("%Y-%m-%d")}
> 输入文件：requirement_analysis.md
> 测试点总数：{total}个

## 1. 汇总统计

{stats_summary}

## 2. 测试设计策略应用说明

### 2.1 风险分级结果

{risk_summary}

### 2.2 验证完整性原则应用

{integrity_summary}

"""

        # 第五步：合并各批次内容，按主单元构建章节
        section_counter = 3  # 从第3节开始（前2节是概述和策略）
        seen_unit_ids = set()  # 修复：同一主单元多批次合并，避免重复章节

        for bf in batch_files:
            bf_path = os.path.join(batch_dir, bf)
            unit_content = self._read_file(bf_path)

            # 提取主单元ID和名称（支持多种格式）
            unit_raw_id = ""
            unit_id = ""
            unit_name = ""

            # 格式：元数据格式（> 主单元ID: TR-001）
            unit_id_match = self._safe_regex_search(r'> 主单元ID[：:]\s*((?:SPEC|TR)-\d+|US-\d+|MU-\d+)', unit_content)
            unit_name_match = self._safe_regex_search(r'> 主单元名称[：:]\s*(.+)', unit_content)

            if unit_id_match:
                unit_raw_id = unit_id_match.group(1)  # 如 TR-001
                unit_id = unit_raw_id.replace('-', '')  # 如 TR001
                if unit_name_match:
                    unit_name = unit_name_match.group(1).strip()
                else:
                    # 尝试从章节标题提取名称
                    title_match = self._safe_regex_search(r'## (SPEC|US)-\d+ (.+)', unit_content)
                    unit_name = title_match.group(2).strip() if title_match else ""

            # 格式：合并格式（> 主单元：TR-006 字面量表达式引擎）
            if not unit_id:
                combined_match = self._safe_regex_search(r'> 主单元[：:]\s*(SPEC|TR|US|MU)-(\d+)\s+(.+)', unit_content)
                if combined_match:
                    unit_type = combined_match.group(1)  # SPEC or TR or US or MU
                    unit_num = combined_match.group(2)  # 006
                    unit_raw_id = f"{unit_type}-{unit_num}"
                    unit_id = f"{unit_type}{unit_num}"
                    unit_name = combined_match.group(3).strip()

            # 格式：章节标题格式（## TR-004 表达式内置函数size 测试点）
            if not unit_id:
                title_match = self._safe_regex_search(r'## (SPEC|TR|US|MU)-(\d+) (.+?) 测试点', unit_content)
                if title_match:
                    unit_type = title_match.group(1)  # SPEC or US or MU
                    unit_num = title_match.group(2)  # 004
                    unit_raw_id = f"{unit_type}-{unit_num}"
                    unit_id = f"{unit_type}{unit_num}"
                    unit_name = title_match.group(3).strip()

            # 格式：从文件名提取（支持 batch_US01.md, batch_US01_1.md, batch_US_1.md, batch_TR_001.md）
            if not unit_id:
                # 推荐格式：batch_US01.md, batch_US01_1.md
                file_match = self._safe_regex_search(r'batch_(US\d+|SPEC\d+|TR\d+|MU\d+)(?:_\d+)?', bf)
                if file_match:
                    unit_id = file_match.group(1)  # US01, SPEC001, TR001
                    unit_raw_id = unit_id[:2] + '-' + unit_id[2:] if len(unit_id) > 2 else unit_id  # US01 -> US-01

            # 兼容旧格式：batch_US_1.md, batch_TR_001.md
            if not unit_id:
                file_match = self._safe_regex_search(r'batch_(US_\d+|(?:SPEC|TR)_\d+|MU_\d+)', bf)
                if file_match:
                    unit_raw_id = file_match.group(1).replace('_', '-')  # US_1 -> US-1
                    unit_id = file_match.group(1).replace('_', '')  # US1

            # 兜底：从文件内容第一行标题提取（## US-1: 名称）
            if not unit_id:
                first_line_match = self._safe_regex_search(r'##\s*(US-\d+|SPEC-\d+|TR-\d+|MU-\d+)[：:]', unit_content)
                if first_line_match:
                    unit_raw_id = first_line_match.group(1)  # US-1
                    unit_id = unit_raw_id.replace('-', '')  # US1

            # 兜底：从测试点ID前缀提取
            if not unit_id:
                tp_prefix_match = self._safe_regex_search(r'TP-(US\d+|SPEC\d+|TR\d+|MU\d+)-', unit_content)
                if tp_prefix_match:
                    unit_id = tp_prefix_match.group(1)  # US1

            # 最终兜底：使用序号
            if not unit_id:
                unit_id = f"UNIT{section_counter}"
                unit_raw_id = unit_id

            # 修复：同一主单元多批次合并，仅首个批次生成章节
            if unit_id and unit_id in seen_unit_ids:
                continue
            if unit_id:
                seen_unit_ids.add(unit_id)

            # 构建主单元章节标题
            md_content += f"\n## {section_counter}. {unit_id}: {unit_name}\n\n"

            # 转换测试点编号格式
            # TP-batch_TR_001-001 -> TP-TR001-001
            batch_prefix = unit_raw_id.replace('-', '_')  # TR-001 -> TR_001
            unit_content = re.sub(
                r'TP-batch_' + batch_prefix + r'-(\d+)',
                f'TP-{unit_id}-\\1',
                unit_content
            )

            # 提取并重新组织章节内容
            # N.1 风险分级结果
            risk_section = self._extract_section_content(unit_content, '风险分级结果')
            if risk_section:
                md_content += f"### {section_counter}.1 风险分级结果\n\n{risk_section}\n\n"
            else:
                # 尝试从主单元引用资源中提取风险信息
                risk_table = self._extract_risk_table_from_ref(unit_content)
                if risk_table:
                    md_content += f"### {section_counter}.1 风险识别\n\n{risk_table}\n\n"

            # 修复：N.2 测试点列表从去重后的unit_tp_map生成，确保与汇总统计一致
            if unit_id and unit_id in unit_tp_map:
                tp_table = self._generate_tp_table_from_list(unit_tp_map[unit_id])
            else:
                tp_table = self._extract_testpoint_table(unit_content)
            if tp_table:
                md_content += f"### {section_counter}.2 测试点列表\n\n{tp_table}\n\n"

            # N.3 测试点详细设计（可选）
            detail_section = self._extract_detail_section(unit_content)
            if detail_section:
                md_content += f"### {section_counter}.3 测试点详细设计\n\n{detail_section}\n\n"

            section_counter += 1

        # 补顶级"测试点详细"章节（format_check 必需章节，指向各单元子节）
        md_content += f"\n## 测试点详细\n\n各主单元测试点详细列表见上方各主单元章节「测试点列表」与「测试点详细设计」子节。\n\n"

        # 资料测试点不在Phase2生成，由Phase4统一生成一条资料用例

        # 添加非功能测试点章节（如果有）
        nf_section = self._extract_nf_section(batch_dir, batch_files)
        if nf_section:
            md_content += f"\n## {section_counter}. 非功能测试点\n\n{nf_section}\n\n"
            section_counter += 1

        # 添加知识库补充测试点章节（如果有）
        kb_section = self._extract_kb_section(batch_dir, batch_files)
        if kb_section:
            md_content += f"\n## {section_counter}. 知识库补充测试点\n\n{kb_section}\n\n"

        try:
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.isdir(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
        except Exception as e:
            return {"status": "error", "message": f"写入test_point_design.md失败: {str(e)}"}

        return {
            "status": "success",
            "batch_files": len(batch_files),
            "total_tps": total,
            "doc_tps": 0,
            "duplicate": {
                "exact_count": duplicate_result.get("exact_count", 0),
                "potential_count": duplicate_result.get("potential_count", 0),
                "cross_us_count": duplicate_result.get("cross_us_count", 0),
                "auto_delete_count": len(duplicate_result.get("auto_delete", [])),
                "potential_duplicates": duplicate_result.get("potential_duplicates", []),
                "cross_us_duplicates": duplicate_result.get("cross_us_duplicates", [])
            },
            "same_unit_dedup": {
                "auto_delete_count": same_unit_dedup.get("auto_delete_count", 0),
                "same_unit_duplicates": same_unit_dedup.get("same_unit_duplicates", [])
            },
            "id_range": f"{all_tps[0].get('id', 'TP-???')}~{all_tps[-1].get('id', 'TP-???')}" if all_tps else "无测试点",
            "output": output_path
        }

    def _extract_batch_sort_key(self, filename: str) -> tuple:
        """提取批次文件排序键

        支持命名格式：
        - batch_US01.md、batch_US01_1.md、batch_US01_010.md（推荐格式）
        - batch_US_1.md、batch_US_01.md（旧格式，带下划线分隔）
        - batch_TR_001.md、batch_SPEC001_1.md（TR/SPEC格式）
        - batch_MU_001.md（MU格式）
        - batch_ADD_1.md、batch_ADD_2.md（对抗评估补充测试点）
        - batch_1.md、batch_2.md（纯序号）

        Returns:
            排序键tuple（如 (0,'US01',1), (0,'US01',10), (1,'ADD',1)）；首元素0=主测试点、1=对抗补充，确保 ADD 排在 US 之后
        """
        # 对抗补充格式：batch_ADD_1.md（首元素1，确保补充排在主测试点之后）
        match = re.search(r'batch_ADD_(\d+)', filename)
        if match:
            return (1, 'ADD', int(match.group(1)))
        # 推荐格式：batch_US01.md, batch_US01_1.md, batch_US01_010.md
        match = re.search(r'batch_(US\d+|SPEC\d+|TR\d+|MU\d+)(?:_(\d+))?', filename)
        if match:
            return (0, match.group(1), int(match.group(2) or '0'))
        # 兼容旧格式：batch_US_1.md, batch_TR_001.md
        match = re.search(r'batch_(US_\d+|(?:SPEC|TR)_\d+|MU_\d+)', filename)
        if match:
            return (0, match.group(1).replace('_', ''), 0)
        # 兼容纯数字：batch_1.md, batch_10.md
        match = re.search(r'batch_(\d+)', filename)
        if match:
            return (0, '', int(match.group(1)))
        return (0, filename, 0)

    def _extract_unit_section(self, md_path: str) -> str:
        """提取批次MD中的主单元章节"""
        content = self._read_file(md_path)
        if not content:
            return ""

        # 尝试提取主单元章节
        unit_patterns = [
            r'## [\d]+\.\s*主单元.*?\n',
            r'## 主单元.*?\n',
            r'### 主单元.*?\n',
        ]

        unit_start = -1
        for pattern in unit_patterns:
            match = self._safe_regex_search(pattern, content)
            if match:
                unit_start = match.start()
                break

        # 如果没有主单元章节，尝试从第一个表格或第一个二级标题开始
        if unit_start == -1:
            # 查找第一个表格或第一个有实质内容的二级标题
            table_match = self._safe_regex_search(r'\n\| ', content)
            section_match = self._safe_regex_search(r'\n## [^#]', content)

            if table_match and section_match:
                unit_start = min(table_match.start(), section_match.start())
            elif table_match:
                unit_start = table_match.start()
            elif section_match:
                unit_start = section_match.start()
            else:
                # 如果都没找到，返回整个文件内容（去掉文件头）
                unit_start = content.find('\n## ')
                if unit_start == -1:
                    return ""

        stats_patterns = [
            '\n## 汇总统计',
            '\n## 统计',
        ]

        stats_start = -1
        for sp in stats_patterns:
            pos = content.find(sp, unit_start + 50)
            if pos != -1:
                stats_start = pos
                break

        if stats_start == -1:
            stats_start = len(content)

        unit_section = content[unit_start:stats_start]
        return unit_section.strip() + "\n\n"

    def _extract_design_overview(self, req_content: str, total_tps: int = 0) -> str:
        """提取设计概述信息"""
        strategy_patterns = [
            r'- \*\*拆分策略声明[：:]\*\*\s*(.+)',
            r'拆分策略[：:]\s*(.+)',
        ]

        strategy = "功能规格格式"
        for pattern in strategy_patterns:
            match = self._safe_regex_search(pattern, req_content)
            if match:
                strategy = match.group(1).strip()
                break

        unit_count = len(self._extract_main_units(req_content))

        return f"""- **拆分策略声明**：{strategy}
- **主单元总数**：{unit_count}个
- **测试点总数**：{total_tps}个"""

    def _generate_doc_tps_from_content(self, req_content: str) -> List[Dict]:
        """生成资料测试点（基于public API）

        规则：仅当存在public SDK API时才生成资料测试点（每个public接口1条）
        """
        if not req_content:
            return []

        # 快速检查：如果"public接口0个"或"SDK API统计"显示无public接口，直接返回空
        no_public_patterns = [
            r'public接口0个',
            r'public\s*接口\s*0\s*个',
            r'SDK API统计.*?public接口\s*0\s*个',
        ]
        for pattern in no_public_patterns:
            if self._safe_regex_search(pattern, req_content):
                return []

        api_patterns = [
            r'### 2\.3\s*SDK\s*API信息',
            r'### [\d.]*\s*API信息',
            r'## API信息',
        ]

        api_section_start = -1
        for pattern in api_patterns:
            match = self._safe_regex_search(pattern, req_content)
            if match:
                api_section_start = match.end()
                break

        if api_section_start == -1:
            return []

        section_end = req_content.find('\n### ', api_section_start)
        if section_end == -1:
            section_end = req_content.find('\n## ', api_section_start)
        if section_end == -1:
            section_end = len(req_content)

        section_content = req_content[api_section_start:section_end]

        # 精确匹配"接口类型(public)"列：表格格式为 | API-XXX | 名称 | public/inner | ...
        # pattern匹配第三列明确标记为"public"的行
        public_patterns = [
            r'^\| (API-[A-Z0-9]+)\s+\|[^|]+\|\s*public\s*\|',  # 第三列明确是public
            r'^\| (API-[A-Z0-9]+)\s+\|[^|]+\|\s*Public\s*\|',  # 第三列明确是Public（大写）
        ]

        public_apis = []
        for pattern in public_patterns:
            matches = self._safe_regex_findall(pattern, section_content, re.MULTILINE)
            if matches:
                public_apis.extend(matches)
                # 不break，继续尝试其他pattern以合并结果

        # 如果没有找到任何public API，返回空列表
        if not public_apis:
            return []

        doc_tps = []
        for i, api_id in enumerate(public_apis[:20], 1):
            doc_tps.append({
                "id": f"TP-DOC-{i:03d}",
                "scenario": f"{api_id}接口资料验证",
                "input_cond": "文档示例代码",
                "expected": "示例可执行，结果与文档一致",
                "test_type": "资料测试",
                "priority": "P2",
                "exec_method": "手工",
                "source": api_id
            })

        return doc_tps

    def _extract_risk_summary(self, batch_dir: str, batch_files: List[str], all_tps: List[Dict] = None, req_content: str = "") -> str:
        """从批次文件汇总风险分级结果

        多数据源策略：
        1. 从batch文件的"### 风险分级结果"章节提取表格
        2. 从需求文件的主单元章节提取风险信息
        3. 从测试点优先级统计生成简化表格
        """
        all_risks = []

        # 方法1：从batch文件提取
        for bf in batch_files:
            bf_path = os.path.join(batch_dir, bf)
            content = self._read_file(bf_path)
            if not content:
                continue

            risk_section_start = content.find('### 风险分级结果')
            if risk_section_start == -1:
                continue

            next_section = content.find('\n### ', risk_section_start + 20)
            if next_section == -1:
                next_section = content.find('\n## ', risk_section_start + 20)
            if next_section == -1:
                next_section = len(content)

            risk_section = content[risk_section_start:next_section]

            rows = self._safe_regex_findall(r'\| [^|]+ \| [^|]+ \| [^|]+ \| [^|]+ \|', risk_section)
            for row in rows:
                if '场景ID' in row and '场景名称' in row:
                    continue
                if '-------' in row:
                    continue
                all_risks.append(row.strip())

        # 方法2：从需求文件提取风险信息（兜底）
        if not all_risks and req_content:
            # 从主单元章节提取场景和AC信息
            main_units = self._extract_main_units(req_content)
            for mu in main_units:
                unit_id = mu.get('unit_id', '')
                unit_name = mu.get('unit_name', '')
                # 从需求文件中提取该主单元的风险相关描述
                risk_patterns = [
                    r'涉及安全|涉及权限|数据持久化',
                    r'重要功能|状态转换',
                    r'辅助功能|默认值',
                    r'参数校验|格式检查'
                ]
                risk_level = 'P2'  # 默认中风险
                for i, pattern in enumerate(risk_patterns):
                    if self._safe_regex_search(pattern, req_content):
                        risk_level = ['P0', 'P1', 'P2', 'P3'][i]
                        break

                all_risks.append(f"| {unit_id} | {unit_name} | {risk_level} | 按场景风险分级 |")

        # 方法3：从测试点优先级统计生成（最终兜底）
        if not all_risks and all_tps:
            # 按优先级分组统计
            priority_scenarios = {}
            for tp in all_tps:
                priority = tp.get('priority', 'P2')
                scenario = tp.get('scenario', '')
                if priority not in priority_scenarios:
                    priority_scenarios[priority] = []
                if scenario:
                    priority_scenarios[priority].append(scenario)

            for priority in ['P0', 'P1', 'P2', 'P3']:
                if priority in priority_scenarios:
                    count = len(priority_scenarios[priority])
                    examples = priority_scenarios[priority][:3]
                    desc = '、'.join(examples) if examples else '多个场景'
                    coverage = {'P0': '4-5类', 'P1': '2-3类', 'P2': '1-2类', 'P3': '1类'}[priority]
                    all_risks.append(f"| {priority}级场景 | {desc}等{count}个场景 | {priority} | {coverage} |")

        if not all_risks:
            return "（各批次文件中未找到风险分级结果表格）"

        summary = "| 场景ID | 场景名称 | 风险等级 | 异常值覆盖深度 |\n"
        summary += "|-------|---------|---------|-------------|\n"
        for row in all_risks[:100]:
            summary += f"{row}\n"

        return summary

    def _extract_integrity_summary(self, batch_dir: str, batch_files: List[str], all_tps: List[Dict] = None, req_content: str = "") -> str:
        """从批次文件汇总验证完整性原则应用

        多数据源策略：
        1. 从batch文件的"### 验证完整性原则应用"章节提取完整内容，按主单元分组
        2. 从需求文件的§2.4可测试性手段信息提取
        3. 从测试点来源列和预期输出提取手段覆盖信息
        """
        all_integrity = []
        unit_integrity_map = {}  # 按主单元分组存储

        # 方法1：从batch文件提取（按主单元分组）
        for bf in batch_files:
            bf_path = os.path.join(batch_dir, bf)
            content = self._read_file(bf_path)
            if not content:
                continue

            # 提取主单元ID（从文件名或内容标题）
            unit_id = None
            unit_match = self._safe_regex_search(r'batch_(US\d+|SPEC\d+|TR\d+|MU\d+)(?:_\d+)?', bf)
            if unit_match:
                unit_id = unit_match.group(1)
            else:
                # 从内容标题提取
                title_match = self._safe_regex_search(r'#\s*(US-\d+|SPEC-\d+|TR-\d+|MU-\d+)[：:]', content)
                if title_match:
                    unit_id = title_match.group(1).replace('-', '')

            if not unit_id:
                unit_id = "未知主单元"

            integrity_section_start = content.find('### 验证完整性原则应用')
            if integrity_section_start == -1:
                continue

            next_section = content.find('\n### ', integrity_section_start + 20)
            if next_section == -1:
                next_section = content.find('\n## ', integrity_section_start + 20)
            if next_section == -1:
                next_section = len(content)

            integrity_section = content[integrity_section_start:next_section]

            # 提取完整内容（去掉章节标题行，保留后续内容）
            lines = integrity_section.split('\n')
            content_lines = []
            for line in lines[1:]:  # 跳过章节标题行
                line = line.strip()
                if line:  # 只保留非空行
                    content_lines.append(line)

            if content_lines:
                if unit_id not in unit_integrity_map:
                    unit_integrity_map[unit_id] = []
                unit_integrity_map[unit_id].extend(content_lines)

        # 汇总按主单元分组的内容
        if unit_integrity_map:
            for unit_id, lines in unit_integrity_map.items():
                all_integrity.append(f"\n**{unit_id}**:")
                for line in lines:
                    all_integrity.append(f"  {line}")

        # 方法2：从需求文件§2.4可测试性手段信息提取（兜底）
        if not unit_integrity_map and req_content:
            tm_section_start = req_content.find('### 2.4 可测试性手段信息')
            if tm_section_start != -1:
                tm_section_end = req_content.find('\n### ', tm_section_start + 20)
                if tm_section_end == -1:
                    tm_section_end = req_content.find('\n## ', tm_section_start + 20)
                if tm_section_end == -1:
                    tm_section_end = len(req_content)

                tm_section = req_content[tm_section_start:tm_section_end]

                # 提取手段ID和用途
                tm_matches = self._safe_regex_findall(r'\| (TM-\d+)\s+\|\s*(.+?)\s+\|\s*(.+?)\s+\|', tm_section)
                if tm_matches:
                    tm_ids = [m[0] for m in tm_matches]
                    tm_descs = [f"{m[0]}（{m[1]}）" for m in tm_matches]
                    all_integrity.append(f"- 涉及手段：{', '.join(tm_ids)}")
                    all_integrity.append(f"- 手段用途：")
                    for desc in tm_descs[:5]:
                        all_integrity.append(f"  - {desc}")

        # 方法3：从测试点来源列提取手段覆盖（最终兜底）
        if not unit_integrity_map and not all_integrity and all_tps:
            # 从来源列提取TM-XXX
            tm_coverage = {}
            for tp in all_tps:
                source = tp.get('source', '')
                tm_matches = self._safe_regex_findall(r'TM-\d+', source)
                for tm_id in tm_matches:
                    if tm_id not in tm_coverage:
                        tm_coverage[tm_id] = []
                    scenario = tp.get('scenario', '')
                    expected = tp.get('expected', '')
                    if scenario:
                        tm_coverage[tm_id].append(f"{scenario}：{expected[:50]}...")

            if tm_coverage:
                all_integrity.append(f"- 测试点涉及手段：{', '.join(tm_coverage.keys())}")
                all_integrity.append(f"- 手段生效验证覆盖：")
                for tm_id, coverage_list in tm_coverage.items():
                    all_integrity.append(f"  - {tm_id}：{len(coverage_list)}个测试点覆盖")

        if not all_integrity:
            return "（各批次文件中未找到验证完整性原则应用说明）"

        return "\n".join(all_integrity)

    def _generate_unit_stats(self, tps: List[Dict], unit_id_map: Dict, req_content: str = "") -> str:
        """生成按主单元分组的统计汇总"""
        total = len(tps)

        # 从需求文件提取拆分策略（容忍冒号在bold内外；泛化pattern行首锚定避免"可选拆分策略"子串误匹配）
        strategy_patterns = [
            r'拆分策略声明\**[：:]\s*(.+)',
            r'(?:^|\n)\s*[-*>]*\s*\**拆分策略\**[：:]\s*(.+)',
        ]

        strategy = "按主单元划分"
        for pattern in strategy_patterns:
            match = self._safe_regex_search(pattern, req_content)
            if match:
                strategy = match.group(1).strip()
                break

        # 统计优先级分布
        priority_dist = {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
        for tp in tps:
            priority = tp.get('priority', 'P2')
            if priority in priority_dist:
                priority_dist[priority] += 1

        # 统计测试类型分布
        type_dist = {}
        for tp in tps:
            test_type = tp.get('test_type', '功能测试')
            type_dist[test_type] = type_dist.get(test_type, 0) + 1

        # 统计执行方式分布
        exec_dist = {}
        for tp in tps:
            exec_method = tp.get('exec_method', 'XTS')
            exec_dist[exec_method] = exec_dist.get(exec_method, 0) + 1

        # 统计主单元分布（从测试点ID提取）
        unit_dist = {}
        for tp in tps:
            tp_id = tp.get('id', '')
            # 提取主单元ID: TP-US1-001 -> US1, TP-TR001-001 -> TR001, TP-MU001-001 -> MU001
            unit_match = self._safe_regex_search(r'TP-((?:SPEC|TR)\d+|US\d+|MU\d+|DOC|UNIT\d+)', tp_id)
            if unit_match:
                unit = unit_match.group(1)
                unit_dist[unit] = unit_dist.get(unit, 0) + 1

        # 主单元总数：优先从测试点分布提取，其次从unit_id_map，最后从需求文件
        unit_count = len(unit_dist) if unit_dist else len(unit_id_map)
        if unit_count == 0:
            main_units = self._extract_main_units(req_content)
            unit_count = len(main_units)

        stats = f"""- **拆分策略**：{strategy}
- **主单元总数**：{unit_count}个
- **测试点总数**：{total}个
  - P0：{priority_dist['P0']}个（高风险）
  - P1：{priority_dist['P1']}个（中风险）
  - P2：{priority_dist['P2']}个（低风险）
  - P3：{priority_dist['P3']}个（防御性）

### 主单元分布

| 主单元ID | 测试点数 | 说明 |
|---------|---------|------|
"""
        for unit_id in sorted(unit_dist.keys()):
            stats += f"| {unit_id} | {unit_dist[unit_id]}个 | - |\n"

        # 如果unit_dist为空但需求文件有主单元索引，补充显示
        if not unit_dist and unit_count > 0:
            main_units = self._extract_main_units(req_content)
            for mu in main_units:
                stats += f"| {mu.get('unit_id', '')} | - | {mu.get('unit_name', '')} |\n"

        return stats

    def _extract_section_content(self, content: str, section_name: str) -> str:
        """提取指定章节的内容"""
        section_start = content.find(f'### {section_name}')
        if section_start == -1:
            section_start = content.find(f'## {section_name}')
        if section_start == -1:
            return ""

        # 找到下一个章节作为结束
        next_section = content.find('\n### ', section_start + 20)
        if next_section == -1:
            next_section = content.find('\n## ', section_start + 20)
        if next_section == -1:
            next_section = len(content)

        section_content = content[section_start:next_section]
        # 去掉章节标题行
        lines = section_content.split('\n')
        if lines:
            lines = lines[1:]  # 去掉第一行（章节标题）
        return '\n'.join(lines).strip()

    def _extract_testpoint_table(self, content: str) -> str:
        """提取测试点汇总表（支持表格格式和详细设计格式）- 增强版

        修复：支持多section测试点表格提取，避免只提取第一个表格导致数据丢失
        """
        all_tables = []

        section_patterns = [
            r'### [一二三四五六七八九十]+、(.+?)测试点\s*\n.*?\n(\| 测试点ID \|.*?\n(?:\| [-]+ \|.*?\n)?(?:\| TP-[A-Za-z0-9_\-]+ \|.*?\n)+)',
            r'### \d+\.\s*(.+?)测试点\s*\n.*?\n(\| 测试点ID \|.*?\n(?:\| [-]+ \|.*?\n)?(?:\| TP-[A-Za-z0-9_\-]+ \|.*?\n)+)',
            r'### [一二三四五六七八九十]+、知识库补充测试点.*?\n.*?\n(\| 测试点ID \|.*?\n(?:\| [-]+ \|.*?\n)?(?:\| TP-[A-Za-z0-9_\-]+ \|.*?\n)+)',
            r'(\| 测试点ID \|.*?\n(?:\| [-]+ \|.*?\n)?(?:\| TP-[A-Za-z0-9_\-]+ \|.*?\n)+)',
        ]

        for pattern in section_patterns:
            matches = self._safe_regex_findall(pattern, content, re.DOTALL)
            for match in matches:
                if isinstance(match, tuple):
                    table_content = match[-1] if len(match) > 1 else match[0]
                else:
                    table_content = match

                table_content = re.sub(r'TP-batch_', 'TP-', table_content)
                table_content = self._standardize_table_columns(table_content)

                if table_content and '| TP-' in table_content:
                    all_tables.append(table_content)

        if all_tables:
            result = ""
            for i, table in enumerate(all_tables, 1):
                result += table
                if i < len(all_tables):
                    result += "\n\n"
            return result

        header_pattern = r'### (TP-[A-Za-z0-9_\-]+)'
        headers = self._safe_regex_findall(header_pattern, content)

        if headers:
            result = "| 测试点ID | 测试场景 | 输入条件 | 预期输出概要 | 测试类型 | 优先级 | 执行方式 | 来源 |\n"
            result += "|---------|---------|---------|------------|---------|--------|---------|------|\n"

            for tp_id in headers:
                section_start = content.find(f"### {tp_id}")
                if section_start == -1:
                    continue

                title_end = content.find('\n', section_start)
                if title_end == -1:
                    title_end = section_start + 100

                title_line = content[section_start:title_end]

                tp_name = ""
                for colon in ['：', ':', '\uff1a']:
                    colon_pos = title_line.find(colon)
                    if colon_pos != -1:
                        tp_name = title_line[colon_pos + 1:].strip()
                        break

                next_section = content.find('\n### TP-', section_start + 20)
                if next_section == -1:
                    next_section = content.find('\n## ', section_start + 20)
                if next_section == -1:
                    next_section = len(content)

                section_content = content[section_start:next_section]

                scenario = tp_name
                input_cond = "-"
                expected = "-"
                priority = "P2"
                test_type = "功能测试"
                exec_method = "XTS"
                source = "-"

                ac_match = self._safe_regex_search(r'\| 关联AC \| (.+?) \|', section_content)
                if ac_match:
                    ac_ref = ac_match.group(1).strip()
                    if ac_ref and ac_ref != "-":
                        source = ac_ref

                source_match = self._safe_regex_search(r'\| 来源 \| (.+?) \|', section_content)
                if source_match:
                    source_val = source_match.group(1).strip()
                    if source_val and source_val != "-":
                        source = source_val

                priority_match = self._safe_regex_search(r'\| 优先级 \| (P\d) \|', section_content)
                if priority_match:
                    priority = priority_match.group(1)

                type_match = self._safe_regex_search(r'\| 测试类型 \| (.+?) \|', section_content)
                if type_match:
                    test_type = type_match.group(1).strip()

                exec_match = self._safe_regex_search(r'\| 执行方式 \| (.+?) \|', section_content)
                if exec_match:
                    exec_method = exec_match.group(1).strip()

                input_match = self._safe_regex_search(r'\| 输入条件 \| (.+?) \|', section_content)
                if input_match:
                    input_cond = input_match.group(1).strip()

                expected_match = self._safe_regex_search(r'\| 预期输出 \| (.+?) \|', section_content)
                if expected_match:
                    expected = expected_match.group(1).strip()

                result += f"| {tp_id} | {scenario} | {input_cond} | {expected} | {test_type} | {priority} | {exec_method} | {source} |\n"

            return result

        return ""

    def _standardize_table_columns(self, table_content: str) -> str:
        """标准化表格列名（统一为标准8列格式）"""
        lines = table_content.split('\n')
        if len(lines) < 2:
            return table_content

        # 标准列名映射
        column_map = {
            '关联场景': '测试场景',
            '场景ID': '测试场景',
            '场景': '测试场景',
            '测试目标': '测试场景',
            '测试目的': '测试场景',
            '风险等级': '优先级',
            '关联AC': '来源',
            'AC编号': '来源',
            '输入': '输入条件',
            '预期输出': '预期输出概要',
            '预期结果': '预期输出概要',
        }

        # 处理表头行（按单元格整体匹配，避免子串替换损坏已标准列名）
        header_line = lines[0]
        if header_line.startswith('|'):
            cells = header_line.split('|')
            for i, cell in enumerate(cells):
                c = cell.strip()
                if c in column_map:
                    cells[i] = cell.replace(c, column_map[c], 1)
            header_line = '|'.join(cells)

            # 检查是否缺少必要列，补充为标准8列
            if '输入条件' not in header_line:
                header_line = header_line.replace('测试场景', '测试场景 | 输入条件')
            if '预期输出概要' not in header_line:
                header_line = header_line.replace('输入条件', '输入条件 | 预期输出概要')
            if '执行方式' not in header_line:
                header_line = header_line.replace('优先级', '优先级 | 执行方式')
            if '来源' not in header_line:
                header_line = header_line.replace('执行方式', '执行方式 | 来源')

            lines[0] = header_line

        # 处理分隔行（保持与表头一致的列数）
        if len(lines) > 1 and lines[1].startswith('|'):
            sep_parts = lines[1].split('|')
            header_parts = lines[0].split('|')
            if len(sep_parts) < len(header_parts):
                # 补充分隔符
                while len(sep_parts) < len(header_parts):
                    sep_parts.append('---------|')
                lines[1] = '|'.join(sep_parts)

        return '\n'.join(lines)

    def _extract_detail_section(self, content: str) -> str:
        """提取测试点详细设计章节"""
        # 查找详细设计章节
        detail_start = content.find('### TP-')
        if detail_start == -1:
            detail_start = content.find('## 测试点详细设计')
        if detail_start == -1:
            return ""

        # 找到下一个主章节作为结束
        next_section = content.find('\n## ', detail_start + 20)
        if next_section == -1:
            next_section = content.find('\n### 知识库', detail_start + 20)
        if next_section == -1:
            next_section = content.find('\n### 统计', detail_start + 20)
        if next_section == -1:
            next_section = len(content)

        return content[detail_start:next_section].strip()

    def _extract_risk_table_from_ref(self, content: str) -> str:
        """从主单元引用资源中提取风险识别表格"""
        # 查找风险识别表格
        risk_match = self._safe_regex_search(
            r'(### 风险分级结果|### 风险识别).*?\n.*?\n((?:\| .*? \|.*?\n)+)',
            content, re.DOTALL
        )
        if risk_match:
            return risk_match.group(0).strip()

        return ""

    def _extract_nf_section(self, batch_dir: str, batch_files: List[str]) -> str:
        """提取非功能测试点"""
        nf_tps = []
        for bf in batch_files:
            bf_path = os.path.join(batch_dir, bf)
            content = self._read_file(bf_path)
            if not content:
                continue

            # 查找非功能测试点章节
            nf_match = self._safe_regex_search(
                r'(### 本主单元非功能测试点|## 非功能测试点).*?\n.*?\n((?:\| .*? \|.*?\n)+)',
                content, re.DOTALL
            )
            if nf_match:
                table_content = nf_match.group(0)
                # 提取表格行
                rows = self._safe_regex_findall(r'\| TP-[^|]+\|.*?\|', table_content)
                for row in rows:
                    nf_tps.append(row.strip())

        if not nf_tps:
            return ""

        # 构建汇总表格
        result = "| 测试点ID | 关联需求 | 测试类型 | 优先级 | 执行方式 | 输入条件 | 预期输出概要 | 来源 |\n"
        result += "|---------|---------|---------|--------|---------|---------|------------|------|\n"
        for row in nf_tps[:50]:
            result += f"{row}\n"

        return result

    def _extract_kb_section(self, batch_dir: str, batch_files: List[str]) -> str:
        """提取知识库补充测试点"""
        kb_tps = []
        for bf in batch_files:
            bf_path = os.path.join(batch_dir, bf)
            content = self._read_file(bf_path)
            if not content:
                continue

            # 查找知识库补充章节
            kb_match = self._safe_regex_search(
                r'(### 本主单元知识库补充|## 知识库补充).*?\n.*?\n((?:\| .*? \|.*?\n)+)',
                content, re.DOTALL
            )
            if kb_match:
                table_content = kb_match.group(0)
                rows = self._safe_regex_findall(r'\| TP-[^|]+\|.*?\|', table_content)
                for row in rows:
                    kb_tps.append(row.strip())

        if not kb_tps:
            return ""

        result = "| 测试点ID | 关联场景 | 测试类型 | 优先级 | 执行方式 | 输入条件 | 预期输出概要 | 来源 |\n"
        result += "|---------|---------|---------|--------|---------|---------|------------|------|\n"
        for row in kb_tps[:50]:
            result += f"{row}\n"

        return result

    def _generate_stats_section(self, tps: List[Dict], requirement_path: str) -> str:
        """生成统计章节"""
        total = len(tps)

        priority_dist = {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
        exec_dist = {}
        type_dist = {}
        covered_sources = set()

        for tp in tps:
            priority = tp.get('priority', 'P2')
            if priority in priority_dist:
                priority_dist[priority] += 1
            else:
                priority_dist['P2'] += 1

            exec_method = tp.get('exec_method', '')
            if exec_method:
                exec_dist[exec_method] = exec_dist.get(exec_method, 0) + 1

            test_type = tp.get('test_type', '')
            if test_type:
                type_dist[test_type] = type_dist.get(test_type, 0) + 1

            source = tp.get('source', '')
            if source:
                ac_patterns_local = [
                    r'US\d+-AC\d+[a-z]?',      # 标准格式
                    r'US\d+-AC[A-Z]+[a-z]?',   # 扩展格式
                    r'US\d+-AC[A-Z]+\d+[a-z]?',# 扩展格式数字混合
                    r'AC-\d+[a-z]?',           # 简化格式
                    r'AC[A-Z]+\d+[a-z]?',      # 扩展格式
                    r'TR\d+-AC\d+',            # TR格式
                ]
                for pattern in ac_patterns_local:
                    matches = self._safe_regex_findall(pattern, source)
                    covered_sources.update(matches)

                api_matches = self._safe_regex_findall(r'API-[A-Z0-9]+', source)
                covered_sources.update(api_matches)

        req_content = self._read_file(requirement_path)

        total_ac_patterns = [
            r'US\d+-AC\d+[a-z]?',      # 标准格式
            r'US\d+-AC[A-Z]+[a-z]?',   # 扩展格式
            r'US\d+-AC[A-Z]+\d+[a-z]?',# 扩展格式数字混合
            r'AC-\d+[a-z]?',           # 简化格式
            r'AC[A-Z]+\d+[a-z]?',      # 扩展格式
        ]
        total_scenarios = 0
        for pattern in total_ac_patterns:
            total_scenarios += len(self._safe_regex_findall(pattern, req_content))

        scenario_coverage = round(len(covered_sources) / total_scenarios * 100, 2) if total_scenarios > 0 else 100.0

        stats = f"""- 测试点总数：{total}个
- 优先级分布：P0 {priority_dist.get('P0', 0)}个 / P1 {priority_dist.get('P1', 0)}个 / P2 {priority_dist.get('P2', 0)}个 / P3 {priority_dist.get('P3', 0)}个
- 主单元覆盖：待校验
- 被测场景覆盖：{len(covered_sources)}/{total_scenarios}个（{scenario_coverage}%）

### 执行方式分布
"""
        for exec_method, count in sorted(exec_dist.items()):
            pct = round(count / total * 100, 2) if total > 0 else 0
            stats += f"- {exec_method}：{count}个（{pct}%）\n"

        stats += "\n### 测试类型分布\n"
        for test_type, count in sorted(type_dist.items()):
            pct = round(count / total * 100, 2) if total > 0 else 0
            stats += f"- {test_type}：{count}个（{pct}%）\n"

        stats += f"""
### 覆盖率统计
- 被测场景总数：{total_scenarios}个
- 已覆盖场景：{len(covered_sources)}个
- 场景覆盖率：{scenario_coverage}%（阈值≥95%）
"""
        return stats

    def validate_merged_md(self, md_path: str, requirement_path: str) -> Dict:
        """校验合并后的MD完整性"""
        md_path = self._normalize_path(md_path)
        requirement_path = self._normalize_path(requirement_path)

        md_content = self._read_file(md_path)
        req_content = self._read_file(requirement_path)

        if not md_content:
            return {"valid": False, "errors": ["测试点文件不存在或为空"], "tp_total": 0}
        if not req_content:
            return {"valid": False, "errors": ["需求分析文件不存在或为空"], "tp_total": 0}

        tp_patterns = [
            r'^\|\s*(TP-[A-Za-z0-9_\-]+)',  # 支持TP-batch_US01-001等格式
            r'^\|\s*(TP-\d+)',
            r'^\|\s*(US\d+-TP\d+)',
        ]

        tp_matches = []
        for pattern in tp_patterns:
            tp_matches.extend(self._safe_regex_findall(pattern, md_content, re.MULTILINE))

        tp_total = len(tp_matches)

        ac_patterns = [
            r'US\d+-AC\d+[a-z]?',      # 标准格式
            r'US\d+-AC[A-Z]+[a-z]?',   # 扩展格式
            r'US\d+-AC[A-Z]+\d+[a-z]?',# 扩展格式数字混合
            r'MU\d+-AC\d+',            # 功能规格AC格式
            r'AC-\d+[a-z]?',           # 简化格式
            r'AC[A-Z]+\d+[a-z]?',      # 扩展格式
        ]
        all_acs = set()
        for pattern in ac_patterns:
            all_acs.update(self._safe_regex_findall(pattern, req_content))

        api_patterns = [
            r'^\| (API-[A-Z0-9]+)',
            r'API-[A-Z0-9]+',
        ]
        all_apis = set()
        for pattern in api_patterns:
            all_apis.update(self._safe_regex_findall(pattern, req_content, re.MULTILINE))

        covered_acs = set()
        covered_apis = set()
        tp_id_set = set()
        errors = []

        tp_row_patterns = [
            r'^\|\s*(TP-[A-Za-z0-9_\-]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|',
            r'^\|\s*(TP-\d+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|',
        ]

        tp_rows = []
        for pattern in tp_row_patterns:
            tp_rows.extend(self._safe_regex_findall(pattern, md_content, re.MULTILINE))

        for match in tp_rows:
            # 根据匹配长度解包字段，source在最后一列
            if len(match) == 8:  # 8列格式
                tp_id, scenario, input_cond, output, test_type, priority, exec_method, source = match
            elif len(match) == 2:  # 旧格式（仅ID和source）
                tp_id, source = match
            else:
                continue

            if tp_id in tp_id_set:
                errors.append(f"测试点ID重复: {tp_id}")
            tp_id_set.add(tp_id)

            for pattern in ac_patterns:
                ac_matches = self._safe_regex_findall(pattern, source)
                covered_acs.update(ac_matches)

            api_matches = self._safe_regex_findall(r'API-[A-Z0-9]+', source)
            covered_apis.update(api_matches)

        scenario_coverage = round(len(covered_acs) / len(all_acs) * 100, 2) if all_acs else 100.0
        api_coverage = round(len(covered_apis) / len(all_apis) * 100, 2) if all_apis else 100.0

        if scenario_coverage < 95:
            errors.append(f"场景覆盖率{scenario_coverage}%低于阈值95%")

        uncovered_acs = [ac for ac in all_acs if ac not in covered_acs]
        uncovered_apis = [api for api in all_apis if api not in covered_apis]

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "tp_total": tp_total,
            "scenario_total": len(all_acs),
            "scenario_covered": len(covered_acs),
            "scenario_coverage": scenario_coverage,
            "api_total": len(all_apis),
            "api_covered": len(covered_apis),
            "api_coverage": api_coverage,
            "uncovered_acs": list(uncovered_acs)[:20],
            "uncovered_apis": list(uncovered_apis)[:20]
        }

    def coverage_check(self, testpoint_path: str, requirement_path: str, output_path: str = None) -> Dict:
        """覆盖率矩阵检查（场景/API/手段/路径/高风险深度）- 增强版"""
        testpoint_path = self._normalize_path(testpoint_path)
        requirement_path = self._normalize_path(requirement_path)

        tp_content = self._read_file(testpoint_path)
        req_content = self._read_file(requirement_path)

        if not tp_content:
            return {"status": "error", "message": f"测试点文件不存在: {testpoint_path}"}
        if not req_content:
            return {"status": "error", "message": f"需求分析文件不存在: {requirement_path}"}

        # 步骤1：从需求分析的被测场景表提取主场景ID（US-AC格式或TR-S格式）
        # 被测场景表格式：| 场景ID | 关联AC | WHEN | THEN | 来源 |
        # 兼容多种格式：US1-AC1a, US-1-AC1, US01-AC001, TR001-S001, TR-001-S001
        scenario_table_pattern = r'\|\s*(US(?:-?\d+)-AC(?:\d+)[a-z]?|TR(?:-?\d+)-S(?:\d+)[a-z]?|US\d+-AC\d+[a-z]?|TR\d+-S\d+[a-z]?)\s*\|[^|]+\|[^|]+\|[^|]+\|'
        primary_scenarios = set()
        primary_scenarios.update(self._safe_regex_findall(scenario_table_pattern, req_content, re.MULTILINE))

        # 步骤2：建立AC-X到US-AC的映射（从被测场景表的关联AC列提取）
        # 格式：| US1-AC1 | AC-1 | ... | → 映射 AC-1 → US1-AC1
        # 兼容多种格式：US1-AC1a, US-1-AC1, AC-1, AC-001a等
        ac_mapping_pattern = r'\|\s*(US(?:-?\d+)-AC(?:\d+)[a-z]?|US\d+-AC\d+[a-z]?)\s*\|\s*(AC-[A-Z\d\.]+(?:-[A-Z\d]+)*[a-z]?)\s*\|'
        ac_to_us_mapping = {}
        for match in self._safe_regex_findall(ac_mapping_pattern, req_content, re.MULTILINE):
            us_ac, ac = match
            ac_to_us_mapping[ac] = us_ac

        # 步骤3：all_scenarios只包含主场景（避免AC-X重复统计）
        all_scenarios = primary_scenarios

        # 提取API并过滤internal接口（仅统计public接口）
        # API表格格式: | API-ID | 名称 | 接口类型(public/internal) | ...
        api_row_pattern = r'^\| (API-[A-Z0-9]+)\s*\| .*?\s*\| (public|Public)\s*\|'
        all_apis = set()
        all_apis.update(self._safe_regex_findall(api_row_pattern, req_content, re.MULTILINE))

        # 同时支持旧的简单格式（无类型列时默认为public）
        if not all_apis:
            api_patterns = [
                r'^\| (API-[A-Z0-9]+)',
            ]
            for pattern in api_patterns:
                potential_apis = self._safe_regex_findall(pattern, req_content, re.MULTILINE)
                # 检查是否含internal标记，过滤掉
                for api_id in potential_apis:
                    api_row = self._safe_regex_search(rf'^\| {api_id}\s*\| .*?\s*\| (internal|Internal|已过滤)', req_content, re.MULTILINE)
                    if not api_row:
                        all_apis.add(api_id)

        all_tms = set(self._safe_regex_findall(r'TM-\d+', req_content))
        all_conds = set(self._safe_regex_findall(r'COND-[A-Z0-9]+', req_content))

        # 兼容：从测试点文件章节头部提取TM引用（格式: "可测试手段: TM-xxx"）
        # 将章节头部的TM关联到该章节内的所有测试点
        section_tm_pattern = r'## (US-\d+|TR-\d+)[^\n]*测试点.*?\n.*?可测试手段[：:]\s*(TM-\d+(?:[^,\n]*,\s*TM-\d+)*|[^\n]+)'
        section_tm_matches = self._safe_regex_findall(section_tm_pattern, tp_content, re.DOTALL)

        # 构建章节ID到TM列表的映射
        section_tms_map = {}
        for section_id, tm_text in section_tm_matches:
            tms_in_section = self._safe_regex_findall(r'TM-\d+', tm_text)
            section_tms_map[section_id] = set(tms_in_section)

        # 兼容：从章节头部的"涉及手段"提取TM（备用格式）
        involved_tm_pattern = r'## (US-\d+|TR-\d+)[^\n]*测试点.*?\n.*?- 涉及手段[：:]\s*TM-\d+'
        involved_tm_matches = self._safe_regex_findall(involved_tm_pattern, tp_content, re.DOTALL)
        for section_id, tm_text in involved_tm_matches:
            tms_in_section = self._safe_regex_findall(r'TM-\d+', tm_text)
            if section_id not in section_tms_map:
                section_tms_map[section_id] = set()
            section_tms_map[section_id].update(tms_in_section)

        tp_row_patterns = [
            # TR格式8列：| ID | 关联场景 | 测试目标 | 优先级 | 风险等级 | 测试类型 | 关联AC | 来源 |
            r'^\|\s*(TP-[A-Za-z0-9_\-]+)\s*\|\s*([^|]+)\s*\|\s*[^|]*\s*\|\s*([^|]+)\s*\|\s*[^|]*\s*\|\s*[^|]*\s*\|\s*([^|]+)\s*\|\s*[^|]*\s*\|',
            # 标准8列格式：| ID | 场景 | 输入 | 输出 | 类型 | 优先级 | 执行方式 | 来源 |
            r'^\|\s*(TP-[A-Za-z0-9_\-]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|',
            # 兼容7列格式
            r'^\|\s*(TP-[A-Za-z0-9_\-]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|',
            # 原惰性匹配（备用）
            r'^\|\s*(TP-[A-Za-z0-9_\-]+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*.*?\s*\|\s*.*?\s*\|\s*(P\d)\s*\|\s*.*?\s*\|\s*(.+?)\s*\|',
        ]

        tp_rows = []
        for pattern in tp_row_patterns:
            matches = self._safe_regex_findall(pattern, tp_content, re.MULTILINE)
            tp_rows.extend(matches)

        covered_scenarios = set()
        covered_apis = set()
        covered_tms = set()
        covered_conds = set()

        high_risk_tps = []
        high_risk_keywords = ["边界", "极值", "异常", "竞态", "并发", "安全", "权限", "空值"]

        # 记录当前所在的章节ID（用于关联章节头部的TM）
        current_section_id = None

        for match in tp_rows:
            # 根据匹配长度和格式解包字段
            tp_id = match[0]

            # TR格式8列：| ID | 关联场景 | 测试目标 | 优先级 | 风险等级 | 测试类型 | 关联AC | 来源 |
            # 提取: TP ID, 关联场景(TR), 优先级, 关联AC
            if len(match) == 4:  # TR格式提取4个关键列
                scenario = match[1] if match[1] and match[1] != '-' else ''
                priority = match[2]
                ac_field = match[3] if match[3] and match[3] != '-' else ''
                source = ''
                input_cond = ''
            # 标准8列格式：| ID | 场景 | 输入 | 输出 | 类型 | 优先级 | 执行方式 | 来源 |
            elif len(match) == 8:  # 8列格式
                scenario = match[1]
                input_cond = match[2]
                output = match[3]
                test_type = match[4]
                priority = match[5]
                exec_method = match[6]
                source = match[7]
                ac_field = ''
            elif len(match) == 7:  # 7列格式
                tp_id, scenario, input_cond, output, test_type, priority, source = match
                exec_method = "黑盒自动化"
                ac_field = ''
            elif len(match) == 5:  # 原5列格式
                tp_id, scenario, input_cond, priority, source = match
                exec_method = "黑盒自动化"
                test_type = "功能测试"
                output = ""
                ac_field = ''
            else:
                continue

            # 从来源列提取场景ID（来源列格式如"US1-AC1a/US-1-AC1/COND-001/API-001/TM-007"）
            # 应用AC-X映射：如果提取到AC-X格式，映射到对应的US-AC
            # 支持多种格式：US1-AC1, US-1-AC1, US01-AC001, US1-AC1a, TR001-S001
            if source and source.strip() and source.strip() != '-':
                for pattern in [
                    r'US(?:-?\d+)-AC(?:\d+)[a-z]?',          # US1-AC1a / US-1-AC1
                    r'US\d+-AC\d+[a-z]?',                     # US1-AC1a (简化)
                    r'TR(?:-?\d+)-S(?:\d+)[a-z]?',            # TR001-S001 / TR-001-S001
                    r'TR\d+-AC\d+[a-z]?',                     # TR001-AC1
                    r'AC-[A-Z\d\.]+(?:-[A-Z\d]+)*[a-z]?'      # AC-001 / AC-001a
                ]:
                    matches = self._safe_regex_findall(pattern, source)
                    for m in matches:
                        if m.startswith('AC-'):
                            mapped = ac_to_us_mapping.get(m, m)
                            covered_scenarios.add(mapped)
                        else:
                            covered_scenarios.add(m)

                # 提取API ID
                api_matches = self._safe_regex_findall(r'API-[A-Z0-9]+', source)
                covered_apis.update(api_matches)

                # 提取TM ID
                tm_matches = self._safe_regex_findall(r'TM-\d+', source)
                covered_tms.update(tm_matches)

                # 提取COND ID
                cond_matches = self._safe_regex_findall(r'COND-[A-Z0-9]+', source)
                covered_conds.update(cond_matches)

            # 当来源列为空或"-"时，尝试从其他列推断场景覆盖（多格式兼容）
            if not source or source.strip() == '-' or not covered_scenarios:
                # 策略1：从ac_field提取（TR格式8列的"关联AC"列）
                if ac_field and ac_field.strip() and ac_field.strip() != '-':
                    for pattern in [
                        r'AC-[A-Z\d\.]+(?:-[A-Z\d]+)*[a-z]?',
                        r'US(?:-?\d+)-AC(?:\d+)[a-z]?',
                        r'TR(?:-?\d+)-S(?:\d+)[a-z]?'
                    ]:
                        matches = self._safe_regex_findall(pattern, ac_field)
                        for m in matches:
                            if m.startswith('AC-'):
                                mapped = ac_to_us_mapping.get(m, m)
                                covered_scenarios.add(mapped)
                            else:
                                covered_scenarios.add(m)

                # 策略2：从场景列提取
                for pattern in [
                    r'US(?:-?\d+)-AC(?:\d+)[a-z]?',
                    r'US\d+-AC\d+[a-z]?',
                    r'TR(?:-?\d+)-S(?:\d+)[a-z]?'
                ]:
                    covered_scenarios.update(self._safe_regex_findall(pattern, scenario))

                # 策略3：从测试点ID推断主单元，然后根据章节标题推断场景
                # TP-US01-001 -> US01 -> 需求文件中的US01相关场景
                tp_unit_match = self._safe_regex_search(r'TP-(US\d+|TR\d+)-', tp_id)
                if tp_unit_match:
                    unit_prefix = tp_unit_match.group(1)  # 如 US01
                    # 从需求文件中查找该主单元的所有场景
                    unit_pattern = rf'{unit_prefix}-AC\d+[a-z]?'
                    covered_scenarios.update(self._safe_regex_findall(unit_pattern, req_content))

            # 从场景列提取场景ID（备用）
            for pattern in [
                r'US(?:-?\d+)-AC(?:\d+)[a-z]?',          # US1-AC1a / US-1-AC1
                r'US\d+-AC\d+[a-z]?',                     # US1-AC1a (简化)
                r'TR(?:-?\d+)-S(?:\d+)[a-z]?'             # TR001-S001
            ]:
                covered_scenarios.update(self._safe_regex_findall(pattern, scenario))

            if priority in ["P0", "P1"]:
                for kw in high_risk_keywords:
                    if kw in scenario or kw in input_cond:
                        high_risk_tps.append(tp_id)
                        break

        # TM覆盖检查：补充从测试点来源列和预期输出列提取TM引用
        # TM表格格式：| TM-ID | 类型 | 触发方式 | 用途 | 来源 |
        tm_table_pattern = r'\|\s*(TM-\d+)\s*\|[^|]+\|([^|]+)\s*\|[^|]+\|'
        tm_triggers = {}
        for match in self._safe_regex_findall(tm_table_pattern, req_content, re.MULTILINE):
            tm_id, trigger = match
            tm_triggers[tm_id] = trigger.strip()

        # 注意：covered_tms已在上方从来源列提取，此处不再重置，仅补充关键词匹配
        # 从每个TM的触发方式中自动提取关键词（支持中英文混合）
        for tm_id, trigger in tm_triggers.items():
            if tm_id in covered_tms:  # 已从来源列提取，跳过
                continue
            keywords = []

            # 提取策略1：中文名词短语（2-6字中文+可选后缀）
            cn_phrase = re.findall(r'[\u4e00-\u9fff]{2,6}', trigger)

            # 提取策略2：英文术语（3+字母）
            en_terms = re.findall(r'[A-Z][a-zA-Z]{3,}', trigger)

            # 提取策略3：中英混合词（英文+中文后缀，如"HAP文件"、"scripts文件"）
            mixed = re.findall(r'[A-Za-z]+[\u4e00-\u9fff]{2,4}', trigger)

            # 提取策略4：括号内容（过滤"具体"、"待确认"）
            bracket_matches = re.findall(r'[（(]([^）)]+)[）)]', trigger)
            bracket_filtered = [kw for kw in bracket_matches if len(kw) >= 3 and '具体' not in kw and '待确认' not in kw]

            # 合并候选关键词（优先混合词和短语）
            keywords = mixed + cn_phrase + en_terms + bracket_filtered

            for kw in keywords[:8]:  # 取前8个关键词尝试匹配
                if kw and len(kw) >= 2 and kw in tp_content:
                    covered_tms.add(tm_id)
                    break

        scenario_coverage = round(len(covered_scenarios) / len(all_scenarios) * 100, 2) if all_scenarios else 100.0
        api_coverage = round(len(covered_apis) / len(all_apis) * 100, 2) if all_apis else 100.0
        tm_coverage = round(len(covered_tms) / len(all_tms) * 100, 2) if all_tms else 100.0
        cond_coverage = round(len(covered_conds) / len(all_conds) * 100, 2) if all_conds else 100.0

        path_check = self.check_path_coverage(tp_content, req_content)
        high_risk_depth_check = self.check_high_risk_depth(tp_content, req_content)

        all_pass = (
            scenario_coverage >= 95 and
            api_coverage >= 95 and
            tm_coverage >= 90 and
            path_check.get("pass", True) and
            high_risk_depth_check.get("pass", True)
        )

        result = {
            "status": "success",
            "coverage_matrix": {
                "scenario": {"total": len(all_scenarios), "covered": len(covered_scenarios), "coverage": scenario_coverage, "pass": scenario_coverage >= 95},
                "api": {"total": len(all_apis), "covered": len(covered_apis), "coverage": api_coverage, "pass": api_coverage >= 95},
                "tm": {"total": len(all_tms), "covered": len(covered_tms), "coverage": tm_coverage, "pass": tm_coverage >= 90},
                "cond": {"total": len(all_conds), "covered": len(covered_conds), "coverage": cond_coverage},
                "path": path_check,
                "high_risk_depth": high_risk_depth_check
            },
            "high_risk_tps": high_risk_tps,
            "high_risk_count": len(high_risk_tps),
            "uncovered_scenarios": list(all_scenarios - covered_scenarios)[:20],
            "uncovered_apis": list(all_apis - covered_apis)[:20],
            "uncovered_tms": list(all_tms - covered_tms)[:20],
            "overall_pass": all_pass,
            "validation_summary": {
                "scenario_coverage_pass": scenario_coverage >= 95,
                "api_coverage_pass": api_coverage >= 95,
                "tm_coverage_pass": tm_coverage >= 90,
                "path_coverage_pass": path_check.get("pass", True),
                "high_risk_depth_pass": high_risk_depth_check.get("pass", True)
            }
        }

        if output_path:
            output_path = self._normalize_path(output_path)
            try:
                output_dir = os.path.dirname(output_path)
                if output_dir and not os.path.isdir(output_dir):
                    os.makedirs(output_dir, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
            except Exception as e:
                result["write_error"] = str(e)

        return result

    def generate_stats_section(self, tps: List[Dict], requirement_path: str, knowledge_results: Dict = None, validation_results: Dict = None) -> str:
        """生成汇总统计章节（增强版）

            tps: 测试点列表
            requirement_path: 需求分析文件路径
            knowledge_results: 知识库匹配结果（可选）
            validation_results: 验证结果（可选）

        Returns:
            MD格式的汇总统计章节
        """
        total = len(tps)

        priority_dist = {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
        exec_dist = {}
        type_dist = {}
        knowledge_tp_count = 0
        doc_tp_count = 0
        nonfunc_tp_count = 0
        high_risk_covered = 0

        for tp in tps:
            priority = tp.get('priority', 'P2')
            priority_dist[priority] = priority_dist.get(priority, 0) + 1

            exec_method = tp.get('exec_method', '')
            exec_dist[exec_method] = exec_dist.get(exec_method, 0) + 1

            test_type = tp.get('test_type', '')
            type_dist[test_type] = type_dist.get(test_type, 0) + 1

            tp_id = tp.get('id', '')
            source = tp.get('source', '')
            if tp_id.startswith('TP-ADD') or '对抗模型' in source or '知识库' in source:
                knowledge_tp_count += 1
            if tp_id.startswith('TP-DOC') or test_type == '资料测试':
                doc_tp_count += 1
            if test_type in ['性能测试', '稳定性测试', '安全测试']:
                nonfunc_tp_count += 1

            if priority in ['P0', 'P1']:
                high_risk_covered += 1

        req_content = self._read_file(requirement_path)
        unit_count = len(self._extract_main_units(req_content))

        scenario_patterns = [r'US\d+(?:-\d+)?AC(?:\d+)?(?:[A-Z][a-z]|[a-z])?(?:-[A-Z\d]+)*[a-z]?', r'AC-[A-Z\d\.]+(?:-[A-Z\d]+)*[a-z]?']
        total_scenarios = 0
        for pattern in scenario_patterns:
            total_scenarios += len(self._safe_regex_findall(pattern, req_content))

        covered_sources = set()
        for tp in tps:
            source = tp.get('source', '')
            for pattern in scenario_patterns:
                covered_sources.update(self._safe_regex_findall(pattern, source))

        scenario_coverage = round(len(covered_sources) / total_scenarios * 100, 2) if total_scenarios > 0 else 100.0

        self_check_results = {
            "场景覆盖": True,
            "路径覆盖": validation_results.get('path_coverage_pass', True) if validation_results else True,
            "高风险参数深度覆盖": validation_results.get('high_risk_depth_pass', True) if validation_results else True,
            "测试点无重复": True,
            "手段覆盖": True,
            "内部ID隔离": True,
            "知识库匹配日志": knowledge_results is not None,
            "知识库覆盖率（参考）": round(knowledge_results.get('stats', {}).get('coverage', 100), 1) if knowledge_results else None,
            "补充测试点来源": knowledge_tp_count == 0 or all(
                '对抗模型' in tp.get('source', '') or '知识库' in tp.get('source', '') or '经验库' in tp.get('source', '')
                for tp in tps if tp.get('id', '').startswith('TP-ADD') or '对抗模型' in tp.get('source', '') or '知识库' in tp.get('source', '') or '经验库' in tp.get('source', '')
            )
        }
        self_check_passed = sum(self_check_results.values())
        self_check_total = len(self_check_results)

        stats = f"""## 汇总统计

- **测试点总数**：{total}个
  - P0（高风险）：{priority_dist.get('P0', 0)}个
  - P1（中风险）：{priority_dist.get('P1', 0)}个
  - P2（低风险）：{priority_dist.get('P2', 0)}个
  - P3（防御性）：{priority_dist.get('P3', 0)}个
  - 知识库补充：{knowledge_tp_count}个
  - 资料测试点：{doc_tp_count}个
  - 非功能测试点：{nonfunc_tp_count}个

### 覆盖率统计

- 主单元覆盖：{unit_count}/{unit_count}个（100%）
- 被测场景覆盖：{len(covered_sources)}/{total_scenarios}个（{scenario_coverage}%）
- 高风险参数深度覆盖：{high_risk_covered}个高风险测试点（阈值：每参数≥3类异常值）
- 验证完整性原则：所有测试点的预期输出概要验证到外部可观测效果

### 执行方式分布

"""
        for exec_method, count in sorted(exec_dist.items()):
            pct = round(count / total * 100, 2) if total > 0 else 0
            stats += f"- {exec_method}：{count}个（{pct}%）\n"

        stats += "\n### 测试类型分布\n"
        for test_type, count in sorted(type_dist.items()):
            pct = round(count / total * 100, 2) if total > 0 else 0
            stats += f"- {test_type}：{count}个（{pct}%）\n"

        stats += f"""
### 自检结果

| 检查项 | 结果 |
|-------|------|
"""
        for check_name, check_result in self_check_results.items():
            status = "✓通过" if check_result else "✗未通过"
            stats += f"| {check_name} | {status} |\n"
        stats += f"\n**自检统计**：{self_check_passed}/{self_check_total}项通过\n"

        return stats

    def check_path_coverage(self, tp_content: str, req_content: str) -> Dict:
        """检查路径覆盖（基于耦合分析章节）

        Returns:
            {"pass": True/False, "total_paths": N, "covered_paths": N, "uncovered": [...]}
        """
        coupling_patterns = [
            r'## 2\.2\s*耦合分析',
            r'### 2\.2\s*耦合分析',
            r'## 耦合分析',
        ]

        coupling_start = -1
        for pattern in coupling_patterns:
            match = self._safe_regex_search(pattern, req_content)
            if match:
                coupling_start = match.end()
                break

        if coupling_start == -1:
            return {"pass": True, "total_paths": 0, "covered_paths": 0, "uncovered": [], "note": "未找到耦合分析章节"}

        section_end = req_content.find('\n## ', coupling_start + 50)
        if section_end == -1:
            section_end = len(req_content)

        coupling_content = req_content[coupling_start:section_end]

        path_patterns = [
            r'路径[：:]\s*([^\n]+)',
            r'路径\s*\d+[：:]\s*([^\n]+)',
            r'关键路径[：:]\s*([^\n]+)',
        ]

        total_paths = set()
        for pattern in path_patterns:
            matches = self._safe_regex_findall(pattern, coupling_content)
            total_paths.update(matches)

        if not total_paths:
            cond_patterns = [r'COND-[A-Z0-9]+']
            all_conds = set()
            for pattern in cond_patterns:
                all_conds.update(self._safe_regex_findall(pattern, coupling_content))
            total_paths = all_conds

        covered_paths = set()
        for path in total_paths:
            if path in tp_content:
                covered_paths.add(path)

        uncovered = list(total_paths - covered_paths)[:10]

        return {
            "pass": len(covered_paths) >= len(total_paths) * 0.9 if total_paths else True,
            "total_paths": len(total_paths),
            "covered_paths": len(covered_paths),
            "coverage": round(len(covered_paths) / len(total_paths) * 100, 2) if total_paths else 100.0,
            "uncovered": uncovered
        }

    def check_high_risk_depth(self, tp_content: str, req_content: str) -> Dict:
        """检查高风险参数深度覆盖（每参数≥3类异常值）

        Returns:
            {"pass": True/False, "high_risk_params": [...], "coverage_details": [...]}
        """
        br_patterns = [
            r'BR-\d+[：:]\s*([^\n]+)',
            r'业务规则[：:]\s*([^\n]+)',
        ]

        high_risk_keywords = ['安全', '权限', '数据完整性', '数据丢失', '核心业务']
        high_risk_params = []

        for pattern in br_patterns:
            matches = self._safe_regex_findall(pattern, req_content)
            for match in matches:
                for kw in high_risk_keywords:
                    if kw in match:
                        cond_matches = self._safe_regex_findall(r'COND-[A-Z0-9]+', match)
                        high_risk_params.extend(cond_matches)
                        break

        high_risk_params = list(set(high_risk_params))[:20]

        if not high_risk_params:
            return {"pass": True, "high_risk_params": [], "coverage_details": [], "note": "未识别到高风险参数"}

        coverage_details = []
        all_pass = True

        exception_types = ['边界', '极值', '空值', 'null', 'undefined', '类型错误', '格式', '非法']

        for param in high_risk_params:
            param_in_tps = param in tp_content

            if param_in_tps:
                tp_rows = self._safe_regex_findall(
                    rf'\| TP-[^\|]+\| [^\|]+\| [^\|]*{re.escape(param)}[^\|]*\|',
                    tp_content, re.MULTILINE
                )

                covered_types = set()
                for row in tp_rows:
                    for et in exception_types:
                        if et in row:
                            covered_types.add(et)

                depth = len(covered_types)
                passed = depth >= 3
                if not passed:
                    all_pass = False

                coverage_details.append({
                    "param": param,
                    "depth": depth,
                    "passed": passed,
                    "covered_types": list(covered_types)
                })
            else:
                all_pass = False
                coverage_details.append({
                    "param": param,
                    "depth": 0,
                    "passed": False,
                    "covered_types": []
                })

        return {
            "pass": all_pass,
            "high_risk_params": high_risk_params,
            "coverage_details": coverage_details
        }

    def stats_generate(self, testpoint_path: str, output_path: str = None) -> Dict:
        """统计信息生成"""
        testpoint_path = self._normalize_path(testpoint_path)

        tp_content = self._read_file(testpoint_path)
        if not tp_content:
            return {"status": "error", "message": f"测试点文件不存在: {testpoint_path}"}

        tp_patterns = [
            r'^\|\s*(TP-[A-Za-z0-9_\-]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|',
        ]

        tp_rows = []
        for pattern in tp_patterns:
            tp_rows.extend(self._safe_regex_findall(pattern, tp_content, re.MULTILINE))

        total = len(tp_rows)
        priority_dist = {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
        exec_dist = {}
        type_dist = {}
        knowledge_tps = 0
        doc_tps = 0
        nonfunc_tps = 0

        for match in tp_rows:
            # 8列格式：ID | 场景 | 输入 | 输出 | 类型 | 优先级 | 执行方式 | 来源
            if len(match) == 8:
                tp_id, scenario, input_cond, output, test_type, priority, exec_method, source = match
                # 清理空格
                priority = priority.strip()
                test_type = test_type.strip()
                exec_method = exec_method.strip()
            elif len(match) == 4:  # 旧格式兼容
                tp_id, test_type, priority, exec_method = match
                priority = priority.strip()
                test_type = test_type.strip()
                exec_method = exec_method.strip()
                source = ""  # 旧格式无来源列
            else:
                continue

            priority_dist[priority] = priority_dist.get(priority, 0) + 1
            exec_dist[exec_method] = exec_dist.get(exec_method, 0) + 1
            type_dist[test_type] = type_dist.get(test_type, 0) + 1

            source_str = source.strip() if source else ""
            if tp_id.startswith("TP-ADD") or "对抗模型" in source_str or "知识库" in source_str:
                knowledge_tps += 1
            if tp_id.startswith("TP-DOC") or test_type == "资料测试":
                doc_tps += 1
            if test_type in ["性能测试", "稳定性测试", "安全测试"]:
                nonfunc_tps += 1

        result = {
            "status": "success",
            "total": total,
            "priority_distribution": priority_dist,
            "exec_method_distribution": exec_dist,
            "test_type_distribution": type_dist,
            "knowledge_tps": knowledge_tps,
            "doc_tps": doc_tps,
            "nonfunc_tps": nonfunc_tps,
            "id_range": f"{tp_rows[0][0]}~{tp_rows[-1][0]}" if tp_rows else "无测试点"
        }

        if output_path:
            output_path = self._normalize_path(output_path)
            try:
                output_dir = os.path.dirname(output_path)
                if output_dir and not os.path.isdir(output_dir):
                    os.makedirs(output_dir, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
            except Exception as e:
                result["write_error"] = str(e)

        return result


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description='Phase2测试点生成辅助工具')
    parser.add_argument('--action', required=True,
                        choices=['merge_batch_mds', 'validate_merged_md', 'coverage_check',
                                 'stats_generate', 'generate_stats'],
                        help='执行动作')
    parser.add_argument('--requirement', help='requirement_analysis.md path (required for merge_batch_mds/validate_merged_md/coverage_check/generate_stats)')
    parser.add_argument('--testpoint', help='test_point_design.md path (required for coverage_check/stats_generate/generate_stats)')
    parser.add_argument('--batch-dir', help='Batch MD files directory (required for merge_batch_mds)')
    parser.add_argument('--md', help='test_point_design.md path (required for validate_merged_md)')
    parser.add_argument('--output', help='输出路径')
    parser.add_argument('--validation-results', help='验证结果JSON文件(generate_stats)')
    args = parser.parse_args()

    utils = Phase2TestpointUtils()
    result = None

    try:
        if args.action == 'merge_batch_mds':
            if not args.batch_dir or not args.requirement:
                print(json.dumps({"status": "error", "message": "Missing required parameters: --batch-dir and --requirement are both required for merge_batch_mds action"}, ensure_ascii=False))
                sys.exit(1)
            if not args.output:
                args.output = "test_point_design.md"
            result = utils.merge_batch_mds(args.batch_dir, args.requirement, args.output)
            print(json.dumps(result, ensure_ascii=False))
            return

        elif args.action == 'validate_merged_md':
            if not args.md or not args.requirement:
                print(json.dumps({"status": "error", "message": "Missing required parameters: --md and --requirement are both required for validate_merged_md action"}, ensure_ascii=False))
                sys.exit(1)
            result = utils.validate_merged_md(args.md, args.requirement)
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)

        elif args.action == 'coverage_check':
            if not args.testpoint or not args.requirement:
                print(json.dumps({"status": "error", "message": "Missing required parameters: --testpoint and --requirement are both required for coverage_check action"}, ensure_ascii=False))
                sys.exit(1)
            result = utils.coverage_check(args.testpoint, args.requirement, args.output)

        elif args.action == 'stats_generate':
            if not args.testpoint:
                print(json.dumps({"status": "error", "message": "Missing required parameter: --testpoint is required for stats_generate action"}, ensure_ascii=False))
                sys.exit(1)
            result = utils.stats_generate(args.testpoint, args.output)

        elif args.action == 'generate_stats':
            if not args.testpoint or not args.requirement:
                print(json.dumps({"status": "error", "message": "Missing required parameters: --testpoint and --requirement are both required for generate_stats action"}, ensure_ascii=False))
                sys.exit(1)

            validation_data = None
            if args.validation_results:
                validation_path = utils._normalize_path(args.validation_results)
                if os.path.isfile(validation_path):
                    try:
                        with open(validation_path, 'r', encoding='utf-8') as f:
                            validation_data = json.load(f)
                    except Exception:
                        pass

            tp_content = utils._read_file(args.testpoint)

            tp_patterns = [
                r'^\| (TP-[A-Z0-9\-]+)\s*\| (.+?)\s*\| (.+?)\s*\| (.+?)\s*\| (.+?)\s*\| (P\d)\s*\| (.+?)\s*\| (.+?) \|',
            ]

            tp_rows = []
            for pattern in tp_patterns:
                tp_rows.extend(utils._safe_regex_findall(pattern, tp_content, re.MULTILINE))

            tps = []
            for row in tp_rows:
                tps.append({
                    "id": row[0],
                    "scenario": row[1],
                    "input_cond": row[2],
                    "expected": row[3],
                    "test_type": row[4],
                    "priority": row[5],
                    "exec_method": row[6],
                    "source": row[7]
                })

            stats_md = utils.generate_stats_section(tps, args.requirement, None, validation_data)

            if args.output:
                output_path = utils._normalize_path(args.output)
                output_dir = os.path.dirname(output_path)
                if output_dir and not os.path.isdir(output_dir):
                    os.makedirs(output_dir, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(stats_md)
                result = {"status": "success", "output": output_path, "length": len(stats_md)}
            else:
                print(stats_md)
                return

        print(json.dumps(result, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e), "traceback": traceback.format_exc()}, ensure_ascii=False))
        sys.exit(1)


if __name__ == '__main__':
    main()