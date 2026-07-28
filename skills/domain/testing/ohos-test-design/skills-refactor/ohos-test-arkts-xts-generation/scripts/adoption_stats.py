#!/usr/bin/env python3
"""
代码采纳率自动统计脚本
在 Phase 5/8/9/10 各阶段采集数据，Phase 11 输出综合报告
零 Token 消耗：所有统计通过本地脚本执行
"""

import json
import os
import re
import sys
import difflib
from datetime import datetime
from pathlib import Path

class AdoptionStats:
    def __init__(self, output_dir=".coverage_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.stats_file = self.output_dir / "adoption_stats.json"
        self.stats = self._load_stats()
    
    def _load_stats(self):
        if self.stats_file.exists():
            with open(self.stats_file, 'r') as f:
                return json.load(f)
        return {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "phases": {},
            "summary": {}
        }
    
    def record_phase5(self, design_doc_path, generated_files):
        """Phase 5: 记录生成情况"""
        design_cases = self._count_test_cases_in_design(design_doc_path)
        generated_cases = self._count_test_cases_in_files(generated_files)
        
        self.stats["phases"]["phase5"] = {
            "timestamp": datetime.now().isoformat(),
            "design_cases": design_cases,
            "generated_cases": generated_cases,
            "generation_rate": generated_cases / design_cases if design_cases > 0 else 0
        }
        self._save_stats()
    
    def record_phase8(self, build_log_path):
        """Phase 8: 记录编译通过情况"""
        compile_passed, compile_failed = self._parse_build_log(build_log_path)
        generated = self.stats["phases"].get("phase5", {}).get("generated_cases", 0)
        
        self.stats["phases"]["phase8"] = {
            "timestamp": datetime.now().isoformat(),
            "compile_passed": compile_passed,
            "compile_failed": len(compile_failed),
            "compile_pass_rate": compile_passed / generated if generated > 0 else 0,
            "failed_files": compile_failed
        }
        self._save_stats()
    
    def record_phase9(self, test_report_path):
        """Phase 9: 记录设备测试通过情况"""
        passed, failed = self._parse_test_report(test_report_path)

        self.stats["phases"]["phase9"] = {
            "timestamp": datetime.now().isoformat(),
            "device_passed": passed,
            "device_failed": failed,
            "device_pass_rate": passed / (passed + failed) if (passed + failed) > 0 else 0
        }
        self._save_stats()
    
    def record_phase10(self, coverage_before, coverage_after):
        """Phase 10: 记录覆盖率提升"""
        self.stats["phases"]["phase10"] = {
            "timestamp": datetime.now().isoformat(),
            "coverage_before": coverage_before,
            "coverage_after": coverage_after,
            "coverage_improvement": coverage_after - coverage_before
        }
        self._save_stats()
    
    def record_line_adoption(self, phase5_snapshot_dir, final_dir):
        """Phase 11: 计算按行采纳率"""
        total_lines = 0
        diff_modified_lines = 0
        file_details = []
        
        if not os.path.exists(phase5_snapshot_dir):
            return
        
        for filename in os.listdir(phase5_snapshot_dir):
            orig_path = os.path.join(phase5_snapshot_dir, filename)
            final_path = os.path.join(final_dir, filename)
            
            if not os.path.exists(final_path):
                continue
            
            with open(orig_path, 'r') as f:
                orig_lines = f.readlines()
            with open(final_path, 'r') as f:
                final_lines = f.readlines()
            
            # 使用 difflib 对比
            matcher = difflib.SequenceMatcher(None, orig_lines, final_lines)
            opcodes = matcher.get_opcodes()
            
            file_total = len(orig_lines)
            file_modified = sum(
                b_end - b_start for tag, _, _, b_start, b_end in opcodes
                if tag != 'equal'
            )
            
            total_lines += file_total
            diff_modified_lines += file_modified
            
            file_details.append({
                "file": filename,
                "total_lines": file_total,
                "modified_lines": file_modified,
                "adoption_rate": (file_total - file_modified) / file_total if file_total > 0 else 0
            })
        
        self.stats["phases"]["line_adoption"] = {
            "timestamp": datetime.now().isoformat(),
            "total_lines": total_lines,
            "diff_modified_lines": diff_modified_lines,
            "line_adoption_rate": (total_lines - diff_modified_lines) / total_lines if total_lines > 0 else 0,
            "file_details": file_details
        }
        self._save_stats()
    
    def generate_report(self, output_path=None):
        """Phase 11: 生成综合采纳率报告"""
        p5 = self.stats["phases"].get("phase5", {})
        p8 = self.stats["phases"].get("phase8", {})
        p9 = self.stats["phases"].get("phase9", {})
        p10 = self.stats["phases"].get("phase10", {})
        la = self.stats["phases"].get("line_adoption", {})
        
        report_lines = [
            "# 代码采纳率统计报告",
            f"\n生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"\n## 分层指标",
            f"- 生成率：{p5.get('generation_rate', 0)*100:.1f}%",
            f"- 编译通过率：{p8.get('compile_pass_rate', 0)*100:.1f}%",
            f"- 设备通过率：{p9.get('device_pass_rate', 0)*100:.1f}%",
            f"- 按行采纳率：{la.get('line_adoption_rate', 0)*100:.1f}%",
            f"- 覆盖率提升：+{p10.get('coverage_improvement', 0):.1f}%",
        ]
        
        # 编译失败文件列表
        if p8.get("failed_files"):
            report_lines.append("\n## 编译失败文件列表")
            for f in p8["failed_files"]:
                report_lines.append(f"- {f}")
        
        # 按文件明细
        if la.get("file_details"):
            report_lines.append("\n## 按文件修改明细")
            report_lines.append("\n| 文件 | 生成行数 | 修改行数 | 采纳率 |")
            report_lines.append("|------|---------|---------|--------|")
            for fd in la["file_details"]:
                report_lines.append(f"| {fd['file']} | {fd['total_lines']} | {fd['modified_lines']} | {fd['adoption_rate']*100:.1f}% |")
        
        report = "\n".join(report_lines)
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(report)
        
        return report
    
    def _count_test_cases_in_design(self, design_doc_path):
        """解析设计文档中的用例数"""
        if not design_doc_path or not Path(design_doc_path).exists():
            return 0
        with open(design_doc_path, 'r') as f:
            content = f.read()
        return len(re.findall(r'@tc\.number\s+\S+', content))
    
    def _count_test_cases_in_files(self, file_paths):
        """统计生成文件中的用例数"""
        total = 0
        for f in file_paths:
            if Path(f).exists():
                with open(f, 'r') as fp:
                    content = fp.read()
                total += len(re.findall(r"it\(['\"]", content))
        return total
    
    def _parse_build_log(self, build_log_path):
        """解析编译日志，统计通过/失败文件"""
        if not build_log_path or not Path(build_log_path).exists():
            return 0, []
        with open(build_log_path, 'r') as f:
            content = f.read()
        
        success_pattern = r'Finished\s+:(\S+):default@CompileArkTSEvolution'
        success_files = re.findall(success_pattern, content)
        
        error_pattern = r'Error Message:.*At File:\s+(\S+):(\d+)'
        error_matches = re.findall(error_pattern, content)
        failed_files = list(set([m[0] for m in error_matches]))
        
        return len(success_files), failed_files
    
    def _parse_test_report(self, test_report_path):
        """解析设备测试报告"""
        if not test_report_path or not Path(test_report_path).exists():
            return 0, 0
        with open(test_report_path, 'r') as f:
            content = f.read()
        
        passed = len(re.findall(r'PASS|✅', content))
        failed = len(re.findall(r'FAIL|❌', content))
        return passed, failed
    
    def _save_stats(self):
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="代码采纳率统计")
    parser.add_argument("--action", required=True, 
                       choices=["record_phase5", "record_phase8", "record_phase9", 
                                "record_phase10", "record_line_adoption", "generate_report"])
    parser.add_argument("--output-dir", default=".coverage_data")
    parser.add_argument("--design-doc")
    parser.add_argument("--generated-files", nargs="*")
    parser.add_argument("--build-log")
    parser.add_argument("--test-report")
    parser.add_argument("--coverage-before", type=float)
    parser.add_argument("--coverage-after", type=float)
    parser.add_argument("--phase5-snapshot")
    parser.add_argument("--final-dir")
    parser.add_argument("--report-output")
    
    args = parser.parse_args()
    stats = AdoptionStats(args.output_dir)
    
    if args.action == "record_phase5":
        stats.record_phase5(args.design_doc, args.generated_files)
    elif args.action == "record_phase8":
        stats.record_phase8(args.build_log)
    elif args.action == "record_phase9":
        stats.record_phase9(args.test_report)
    elif args.action == "record_phase10":
        stats.record_phase10(args.coverage_before, args.coverage_after)
    elif args.action == "record_line_adoption":
        stats.record_line_adoption(args.phase5_snapshot, args.final_dir)
    elif args.action == "generate_report":
        report = stats.generate_report(args.report_output)
        print(report)
