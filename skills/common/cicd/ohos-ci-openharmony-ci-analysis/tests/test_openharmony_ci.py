#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib.util
import io
from contextlib import redirect_stdout
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "openharmony_ci.py"
SPEC = importlib.util.spec_from_file_location("openharmony_ci", SCRIPT_PATH)
openharmony_ci = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(openharmony_ci)


class CodeCheckTests(TestCase):
    def test_fetch_codecheck_defects_posts_pages_and_flattens_details(self):
        calls = []

        def fake_post(url, payload):
            calls.append((url, payload))
            if payload["pageNum"] == 1:
                return {
                    "data": {
                        "count": 2,
                        "defects": [
                            {
                                "defectId": "defect-a",
                                "defectDetailList": [
                                    {
                                        "filepath": "service/a.cpp",
                                        "lineNumber": "12",
                                        "ruleName": "Rule A",
                                        "defectContent": "first issue",
                                    }
                                ],
                            }
                        ],
                    }
                }
            return {
                "data": {
                    "count": 2,
                    "defects": [
                        {
                            "defectId": "defect-b",
                            "defectDetailList": [
                                {
                                    "filepath": "service/b.cpp",
                                    "lineNumber": "34",
                                    "ruleName": "Rule B",
                                    "defectContent": "second issue",
                                }
                            ],
                        }
                    ],
                }
            }

        with patch.object(openharmony_ci, "http_post_json", side_effect=fake_post):
            result = openharmony_ci.fetch_codecheck_defects("uuid-1", "MR_task", page_size=1)

        self.assertEqual(2, result["defect_count"])
        self.assertEqual(2, len(result["defects"]))
        self.assertEqual("service/a.cpp", result["defects"][0]["file"])
        self.assertEqual("defect-a", result["defects"][0]["defect_id"])
        self.assertEqual(
            "https://dcp.openharmony.cn/api/codecheckAccess/ci-portal/v1/event/uuid-1/codecheck/task/MR_task",
            calls[0][0],
        )
        self.assertEqual({"pageNum": 1, "pageSize": 1}, calls[0][1])
        self.assertEqual({"pageNum": 2, "pageSize": 1}, calls[1][1])

    def test_should_fetch_codecheck_in_auto_mode_when_summary_no_pass(self):
        event_data = {
            "result": "failed",
            "codeCheckSummary": [
                {
                    "result": "noPass",
                    "task_id": "MR_task",
                }
            ],
        }

        self.assertTrue(openharmony_ci.should_fetch_codecheck(event_data, "auto"))

    def test_print_text_report_includes_codecheck_summary_and_first_details(self):
        report = {
            "event_id": "event-1",
            "overall_result": "failed",
            "jobs": [],
            "failed_jobs": [],
            "codecheck": {
                "defect_count": 2,
                "tasks": [
                    {
                        "task_id": "MR_task",
                        "result": "noPass",
                        "defect_count": 2,
                        "defects": [
                            {
                                "file": "service/a.cpp",
                                "line": "12",
                                "rule": "Rule A",
                                "content": "first issue",
                                "tags": "clangtidy",
                                "level": "2",
                            },
                            {
                                "file": "service/b.cpp",
                                "line": "34",
                                "rule": "Rule B",
                                "content": "second issue",
                                "tags": "cmetrics",
                                "level": "1",
                            },
                        ],
                    }
                ],
            },
        }

        output = io.StringIO()
        with redirect_stdout(output):
            openharmony_ci.print_text_report(report)

        text = output.getvalue()
        self.assertIn("codecheck_defects=2", text)
        self.assertIn("codecheck_top_rules:", text)
        self.assertIn("- clangtidy / Rule A: 1", text)
        self.assertIn("codecheck_top_files:", text)
        self.assertIn("- service/a.cpp: 1", text)
        self.assertIn("[codecheck] task_id=MR_task result=noPass defects=2", text)
        self.assertIn("service/a.cpp:12 level=2 tags=clangtidy rule=Rule A", text)
        self.assertIn("first issue", text)


if __name__ == "__main__":
    main()
