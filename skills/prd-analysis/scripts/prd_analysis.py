#!/usr/bin/env python3
"""
PRD Analysis Tool

Analyzes HM Desktop PRD documents to extract requirements,
validate completeness, and generate structured reports.

Usage:
    python prd_analysis.py <prd_file> [options]

Options:
    --output <file>     Output file path
    --format json       Output format (markdown|json)
    --check-completeness    Check completeness
    --extract-kep       Extract KEP list
    --detect-conflicts  Detect conflicts
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple


@dataclass
class KEP:
    """Key Experience Path"""
    id: str
    name: str
    priority: str
    user_story: str = ""
    acceptance_criteria: List[str] = field(default_factory=list)

    def is_valid(self) -> Tuple[bool, str]:
        """Validate KEP format"""
        # Check ID format: KEP{N}-{NN}
        if not re.match(r'^KEP\d+-\d{2}$', self.id):
            return False, f"KEP ID {self.id} doesn't match format KEP{{N}}-{{NN}}"

        # Check priority
        if self.priority not in ['P0', 'P1', 'P2']:
            return False, f"KEP {self.id} has invalid priority: {self.priority}"

        # Check name (verb-first, not empty)
        if not self.name or len(self.name) > 20:
            return False, f"KEP {self.id} name is invalid"

        return True, "OK"


@dataclass
class Requirement:
    """Functional requirement"""
    id: str
    description: str
    priority: str
    mapped_kep: Optional[str] = None


@dataclass
class PRDDocument:
    """PRD document metadata and content"""
    file_path: str
    version: str = ""
    date: str = ""
    author: str = ""
    product_name: str = ""
    content: str = ""

    keps: List[KEP] = field(default_factory=list)
    requirements: List[Requirement] = field(default_factory=list)


class PRDAnalyzer:
    """PRD Document Analyzer"""

    # Required sections for completeness check
    REQUIRED_SECTIONS = {
        "产品概述": ["产品定位", "目标用户", "核心价值"],
        "用户故事": ["角色定义", "使用场景", "操作流程"],
        "关键体验路径": [],  # KEPs have their own validation
        "功能规格": [],
        "验收标准": [],
        "非功能需求": ["性能指标", "安全性", "兼容性"],
    }

    def __init__(self, prd_file: str):
        self.prd_file = Path(prd_file)
        self.prd = PRDDocument(file_path=str(self.prd_file))
        self.issues: List[str] = []
        self.warnings: List[str] = []

    def load(self) -> bool:
        """Load and parse PRD file"""
        if not self.prd_file.exists():
            self.issues.append(f"PRD file not found: {self.prd_file}")
            return False

        try:
            self.prd.content = self.prd_file.read_text(encoding='utf-8')
        except Exception as e:
            self.issues.append(f"Failed to read PRD file: {e}")
            return False

        self._parse_metadata()
        self._extract_keps()
        self._extract_requirements()

        return True

    def _parse_metadata(self):
        """Extract PRD metadata from header"""
        content = self.prd.content

        # Extract version
        version_match = re.search(r'\|\s*文档版本\s*\|\s*([Vv]?\d+\.?\d*)', content)
        if version_match:
            self.prd.version = version_match.group(1)

        # Extract date
        date_match = re.search(r'\|\s*创建日期\s*\|\s*(\d{4}-\d{2}-\d{2})', content)
        if date_match:
            self.prd.date = date_match.group(1)

        # Extract author
        author_match = re.search(r'\|\s*文档作者\s*\|\s*([^\n|]+)', content)
        if author_match:
            self.prd.author = author_match.group(1).strip()

        # Extract product name from title
        title_match = re.search(r'#\s+(HM Desktop\s+[\d.]+[\s\w]+)\s+PRD', content)
        if title_match:
            self.prd.product_name = title_match.group(1)

    def _extract_keps(self):
        """Extract KEP definitions"""
        content = self.prd.content

        # Find KEP sections
        kep_pattern = r'###?\s*KEP(\d+)-(\d+)[：:]\s*([^\n]+)'
        matches = re.finditer(kep_pattern, content)

        for match in matches:
            category = match.group(1)
            number = match.group(2)
            name = match.group(3).strip()

            # Find the section content for this KEP
            kep_start = match.start()
            kep_section = content[kep_start:kep_start + 2000]  # Get next 2000 chars

            # Extract priority
            priority_match = re.search(r'[-*]\s*优先级[:：]\s*(P[012])', kep_section)
            priority = priority_match.group(1) if priority_match else "P1"

            # Extract user story
            story_match = re.search(r'[-*]\s*用户故事[:：]\s*([^\n]+)', kep_section)
            user_story = story_match.group(1).strip() if story_match else ""

            # Extract acceptance criteria
            criteria = []
            criteria_pattern = r'[-*]\s*验收标准[:：]\s*\n((?:[-*].*\n)*)'
            criteria_match = re.search(criteria_pattern, kep_section)
            if criteria_match:
                criteria_text = criteria_match.group(1)
                criteria = [line.strip('-* ') for line in criteria_text.split('\n') if line.strip() and any(c in line for c in ['-*', '•'])]

            kep = KEP(
                id=f"KEP{category}-{number}",
                name=name,
                priority=priority,
                user_story=user_story,
                acceptance_criteria=criteria
            )
            self.prd.keps.append(kep)

    def _extract_requirements(self):
        """Extract functional requirements"""
        content = self.prd.content

        # Look for numbered requirements in functional specs section
        req_pattern = r'###?\s*4\.?\d*\s*功能规格\s*\n((?:.*\n)*?)(?=##|\n\n|\Z)'
        req_section = re.search(req_pattern, content)

        if req_section:
            section_text = req_section.group(1)
            # Extract numbered items
            items = re.findall(r'[-*]\s+\**([^:*]+)[：:]', section_text)
            for i, item in enumerate(items[:50], 1):  # Max 50 requirements
                self.prd.requirements.append(Requirement(
                    id=f"REQ-{i:02d}",
                    description=item.strip(),
                    priority="P1"  # Default
                ))

    def check_completeness(self) -> Dict:
        """Check PRD completeness"""
        result = {
            "score": 0,
            "max_score": 12,
            "sections": {},
            "missing": []
        }

        content = self.prd.content

        for section, subsections in self.REQUIRED_SECTIONS.items():
            section_present = section in content
            subsections_present = []

            if section_present:
                for subsection in subsections:
                    present = subsection in content
                    subsections_present.append(present)
                    if not present:
                        result["missing"].append(f"{section} - {subsection}")

            # Score: 2 points per section
            if section_present:
                if all(subsections_present) if subsections else True:
                    result["score"] += 2
                    result["sections"][section] = "complete"
                elif any(subsections_present):
                    result["score"] += 1
                    result["sections"][section] = "partial"
                    result["missing"].append(f"{section} - 部分子章节缺失")
            else:
                result["sections"][section] = "missing"
                result["missing"].append(section)

        # Calculate level
        score = result["score"]
        if score >= 11:
            result["level"] = "Excellent"
        elif score >= 9:
            result["level"] = "Good"
        elif score >= 7:
            result["level"] = "Fair"
        else:
            result["level"] = "Poor"

        return result

    def validate_keps(self) -> Dict:
        """Validate all KEPs"""
        result = {
            "total": len(self.prd.keps),
            "valid": 0,
            "invalid": [],
            "by_priority": {"P0": 0, "P1": 0, "P2": 0}
        }

        for kep in self.prd.keps:
            is_valid, msg = kep.is_valid()
            if is_valid:
                result["valid"] += 1
                result["by_priority"][kek.priority] += 1
            else:
                result["invalid"].append({"id": kep.id, "error": msg})

        return result

    def detect_conflicts(self) -> List[Dict]:
        """Detect potential conflicts in PRD"""
        conflicts = []

        # Check for too many P0 requirements
        p0_count = sum(1 for k in self.prd.keps if k.priority == "P0")
        if p0_count > 5:
            conflicts.append({
                "type": "优先级冲突",
                "severity": "Medium",
                "description": f"P0功能过多({p0_count}个)，建议控制在5个以内",
                "suggestion": "考虑将部分P0降级为P1"
            })

        # Check for duplicate KEP IDs
        kep_ids = [k.id for k in self.prd.keps]
        duplicates = [id for id in set(kep_ids) if kep_ids.count(id) > 1]
        if duplicates:
            conflicts.append({
                "type": "KEP ID重复",
                "severity": "High",
                "description": f"KEP ID重复: {', '.join(duplicates)}",
                "suggestion": "确保每个KEP有唯一ID"
            })

        return conflicts

    def suggest_modules(self) -> List[Dict]:
        """Suggest module partitioning based on KEPs"""
        modules = []
        seen_names = set()

        # Group KEPs by type
        info_keps = []
        manager_keps = []
        listener_keps = []

        for kep in self.prd.keps:
            name_lower = kep.name.lower()

            if any(kw in name_lower for kw in ['查看', '获取', '显示', '列表', '详情', '信息']):
                info_keps.append(kep)
            elif any(kw in name_lower for kw in ['管理', '格式化', '修复', '执行']):
                manager_keps.append(kep)
            elif any(kw in name_lower for kw in ['监听', '通知', '变化']):
                listener_keps.append(kep)

        # Suggest modules based on groupings
        if info_keps:
            modules.append({
                "name": "DiskInfoService",
                "type": "Information Service",
                "keps": [k.id for k in info_keps],
                "sa_id": 5001
            })

        if manager_keps:
            for kep in manager_keps:
                if '格式化' in kep.name:
                    modules.append({
                        "name": "FormatManagerService",
                        "type": "Management Service",
                        "keps": [kep.id],
                        "sa_id": 5001
                    })
                elif '修复' in kep.name or '检测' in kep.name:
                    modules.append({
                        "name": "RepairManagerService",
                        "type": "Management Service",
                        "keps": [kep.id],
                        "sa_id": 5001
                    })

        if listener_keps:
            modules.append({
                "name": "DiskChangeListener",
                "type": "Listener",
                "keps": [k.id for k in listener_keps],
                "sa_id": 5001
            })

        return modules

    def generate_report(self, format: str = "markdown") -> str:
        """Generate analysis report"""
        completeness = self.check_completeness()
        kep_validation = self.validate_keps()
        conflicts = self.detect_conflicts()
        modules = self.suggest_modules()

        if format == "json":
            return json.dumps({
                "meta": {
                    "generated_at": datetime.now().isoformat(),
                    "tool_version": "1.0.0",
                    "prd_file": self.prd_file.name
                },
                "document_info": {
                    "file": self.prd_file.name,
                    "path": str(self.prd_file),
                    "version": self.prd.version,
                    "date": self.prd.date,
                    "author": self.prd.author,
                    "product": self.prd.product_name
                },
                "requirements": {
                    "total": len(self.prd.requirements),
                    "p0": kep_validation["by_priority"]["P0"],
                    "p1": kep_validation["by_priority"]["P1"],
                    "p2": kep_validation["by_priority"]["P2"]
                },
                "kep_list": [
                    {
                        "id": k.id,
                        "name": k.name,
                        "priority": k.priority,
                        "user_story": k.user_story,
                        "acceptance_criteria": k.acceptance_criteria
                    }
                    for k in self.prd.keps
                ],
                "completeness": completeness,
                "conflicts": conflicts,
                "module_suggestions": modules
            }, ensure_ascii=False, indent=2)

        # Markdown format
        lines = []
        lines.append("# PRD需求分析报告\n")
        lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("**分析工具**: PRD Analysis Skill v1.0\n")
        lines.append("---\n")
        lines.append("## 1. 文档信息\n")
        lines.append("| 项目 | 内容 |")
        lines.append("|------|------|")
        lines.append(f"| PRD文件 | {self.prd_file.name} |")
        lines.append(f"| 版本号 | {self.prd.version} |")
        lines.append(f"| 创建日期 | {self.prd.date} |")
        lines.append(f"| 文档作者 | {self.prd.author} |")
        lines.append(f"| 产品名称 | {self.prd.product_name} |\n")

        # KEP List
        lines.append("## 2. KEP清单\n")
        lines.append("| KEP ID | 名称 | 优先级 | 用户故事 |")
        lines.append("|--------|------|--------|----------|")
        for kep in self.prd.keps:
            story_short = (kep.user_story[:30] + '...') if len(kep.user_story) > 30 else kep.user_story
            lines.append(f"| {kep.id} | {kep.name} | {kep.priority} | {story_short} |\n")

        # Completeness
        lines.append("## 3. 完整性检查\n")
        lines.append(f"**评分**: {completeness['score']}/{completeness['max_score']} - {completeness['level']}\n")
        lines.append("| 检查项 | 状态 |")
        lines.append("|--------|------|")
        for section, status in completeness["sections"].items():
            status_icon = "✅" if status == "complete" else ("⚠️" if status == "partial" else "❌")
            lines.append(f"| {section} | {status_icon} {status} |\n")

        if completeness["missing"]:
            lines.append("### 缺失项")
            for item in completeness["missing"]:
                lines.append(f"- {item}")
            lines.append("")

        # Module suggestions
        lines.append("## 4. 模块划分建议\n")
        lines.append("| 模块名称 | 类型 | 对应KEP | SA分配 |")
        lines.append("|----------|------|---------|--------|")
        for module in modules:
            lines.append(f"| {module['name']} | {module['type']} | {', '.join(module['keps'])} | {module['sa_id']} |\n")

        # Conflicts
        lines.append("## 5. 冲突检测\n")
        if conflicts:
            lines.append("| 类型 | 严重程度 | 描述 | 建议 |")
            lines.append("|------|----------|------|------|")
            for conflict in conflicts:
                lines.append(f"| {conflict['type']} | {conflict['severity']} | {conflict['description']} | {conflict['suggestion']} |\n")
        else:
            lines.append("✅ 未发现明显需求冲突\n")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="PRD Analysis Tool")
    parser.add_argument("prd_file", help="Path to PRD file")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Output format")
    parser.add_argument("--check-completeness", action="store_true", help="Check completeness")
    parser.add_argument("--extract-kep", action="store_true", help="Extract KEP list")
    parser.add_argument("--detect-conflicts", action="store_true", help="Detect conflicts")

    args = parser.parse_args()

    analyzer = PRDAnalyzer(args.prd_file)
    if not analyzer.load():
        print(f"Error: {analyzer.issues[0]}", file=sys.stderr)
        return 1

    report = analyzer.generate_report(format=args.format)

    if args.output:
        Path(args.output).write_text(report, encoding='utf-8')
        print(f"Report saved to: {args.output}")
    else:
        print(report)

    return 0


if __name__ == "__main__":
    sys.exit(main())
