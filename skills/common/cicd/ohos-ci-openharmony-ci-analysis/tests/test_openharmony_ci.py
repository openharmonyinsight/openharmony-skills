#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib.util
import io
from argparse import Namespace
from tempfile import TemporaryDirectory
from contextlib import redirect_stdout
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import MagicMock, patch


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


class ReportTests(TestCase):
    def args(self, **overrides):
        values = dict(pr=None, pr_url=None, event_id="event", repo=None,
                      log_mode="auto", log_lines=80, download_dir=None,
                      codecheck_mode="auto", codecheck_page_size=300)
        values.update(overrides)
        return Namespace(**values)

    def test_url_infers_repository_and_rejects_conflict(self):
        args = self.args(event_id=None, pr_url="https://gitcode.com/openharmony/multimodalinput_input/pull/9506")
        with patch.object(openharmony_ci, "latest_event_id_from_pr", return_value=("event", {})) as lookup, \
             patch.object(openharmony_ci, "http_get_json", return_value={"data": {"result": "success"}}):
            report = openharmony_ci.build_output(args)
        lookup.assert_called_once_with(9506, "openharmony/multimodalinput_input")
        self.assertEqual(report["repo"], "openharmony/multimodalinput_input")
        args.repo = "openharmony/arkui_ace_engine"
        with self.assertRaisesRegex(openharmony_ci.ToolError, "conflicts"):
            openharmony_ci.build_output(args)

    def test_pr_number_requires_repository(self):
        with self.assertRaisesRegex(openharmony_ci.ToolError, "--repo"):
            openharmony_ci.build_output(self.args(event_id=None, pr=1))

    def test_skips_are_not_failures_or_auto_downloads(self):
        for state in ("skip", "skipped", "ignore"):
            job = {"result": state}
            self.assertFalse(openharmony_ci.is_failure_result(state))
            self.assertFalse(openharmony_ci.should_fetch_logs(job, "auto"))
            self.assertEqual(openharmony_ci.infer_overall_result("", [job]), "skipped")
            self.assertEqual(openharmony_ci.infer_overall_result("", [job, {"result": "success"}]), "success")
        self.assertEqual(openharmony_ci.infer_overall_result("success", [{"result": "failed"}]), "success")

    def test_null_event_is_user_facing_error(self):
        for payload in ({"data": None}, {}, {"data": []}):
            with patch.object(openharmony_ci, "http_get_json", return_value=payload):
                with self.assertRaisesRegex(openharmony_ci.ToolError, "event data"):
                    openharmony_ci.build_output(self.args())

    def test_partial_failures_preserve_other_logs_and_tasks(self):
        event = {"result": "failed", "uuid": "uuid", "builds": [
            {"buildTarget": "a", "result": "failed"},
            {"buildTarget": "b", "result": "failed"},
            {"buildTarget": "c", "result": "skip"}],
            "codeCheckSummary": [{"task_id": "bad"}, {"task_id": "good"}]}
        with patch.object(openharmony_ci, "http_get_json", return_value={"data": event}), \
             patch.object(openharmony_ci, "fetch_job_logs", side_effect=[openharmony_ci.ToolError("download failed"), {"tail": "compiler error"}]) as logs, \
             patch.object(openharmony_ci, "fetch_codecheck_defects", side_effect=[openharmony_ci.ToolError("task failed"), {"task_id": "good", "defect_count": 1, "defects": []}]):
            report = openharmony_ci.build_output(self.args())
        self.assertEqual(logs.call_count, 2)
        self.assertFalse(report["complete"])
        self.assertEqual(len(report["errors"]), 2)
        self.assertEqual(report["failed_jobs"], ["a", "b"])
        self.assertEqual(report["jobs"][1]["log_detail"]["tail"], "compiler error")
        self.assertEqual(report["codecheck"]["tasks"][1]["defect_count"], 1)
        output = io.StringIO()
        with redirect_stdout(output):
            openharmony_ci.print_text_report(report)
        self.assertIn("report_complete=false", output.getvalue())
        self.assertIn("task failed", output.getvalue())

    def test_missing_codecheck_uuid_preserves_status(self):
        event = {"result": "failed", "codeCheckSummary": [{"task_id": "a"}]}
        with patch.object(openharmony_ci, "http_get_json", return_value={"data": event}):
            report = openharmony_ci.build_output(self.args())
        self.assertEqual(report["overall_result"], "failed")
        self.assertFalse(report["complete"])
        self.assertIn("UUID", report["errors"][0]["error"])

    def test_http_helpers_convert_truncated_responses_to_tool_errors(self):
        for helper, args in ((openharmony_ci.http_get_bytes, ("https://example/log",)),
                             (openharmony_ci.http_get_json, ("https://example/event",)),
                             (openharmony_ci.http_post_json, ("https://example/task", {}))):
            with self.subTest(helper=helper.__name__):
                response = MagicMock()
                response.__enter__.return_value.read.side_effect = openharmony_ci.http.client.IncompleteRead(b"partial", 100)
                with patch.object(openharmony_ci.urllib.request, "urlopen", return_value=response):
                    with self.assertRaises(openharmony_ci.ToolError):
                        helper(*args)

    def test_truncated_download_preserves_later_jobs(self):
        event = {"result": "failed", "builds": [
            {"buildTarget": name, "result": "failed", "debug": {"buildLog": f"https://example/{name}.log"}}
            for name in ("a", "b")]}
        bad, good = MagicMock(), MagicMock()
        bad.__enter__.return_value.read.side_effect = openharmony_ci.http.client.IncompleteRead(b"partial", 100)
        good.__enter__.return_value.read.return_value = b"compiler error"
        with patch.object(openharmony_ci, "http_get_json", return_value={"data": event}), \
             patch.object(openharmony_ci.urllib.request, "urlopen", side_effect=[bad, good]):
            report = openharmony_ci.build_output(self.args())
        self.assertFalse(report["complete"])
        self.assertEqual(len(report["errors"]), 1)
        self.assertEqual(report["jobs"][1]["log_detail"]["tail"], "compiler error")

    def test_invalid_codecheck_responses_are_isolated_and_not_zero_defects(self):
        invalid_pages = [None, [], {"message": "upstream unavailable"}, {"data": None},
                         {"data": {}}, {"data": {"count": 1, "defects": None}},
                         {"data": {"count": 1, "defects": [{"defectDetailList": None}]}},
                         {"data": {"count": 1, "defects": [{"defectDetailList": [None]}]}},
                         {"data": {"count": "invalid", "defects": []}},
                         {"data": {"count": 1, "defects": []}}]
        event = {"result": "failed", "uuid": "uuid", "codeCheckSummary": [
            {"task_id": "bad", "result": "noPass", "issue_count": 5},
            {"task_id": "good", "result": "pass"}]}
        for page in invalid_pages:
            with self.subTest(page=page), \
                 patch.object(openharmony_ci, "http_get_json", return_value={"data": event}), \
                 patch.object(openharmony_ci, "http_post_json", side_effect=[page, {"data": {"count": 0, "defects": []}}]):
                report = openharmony_ci.build_output(self.args())
                self.assertFalse(report["complete"])
                self.assertFalse(report["codecheck"]["complete"])
                self.assertEqual(len(report["errors"]), 1)
                bad, good = report["codecheck"]["tasks"]
                self.assertIsNone(bad["defect_count"])
                self.assertIn("error", bad)
                self.assertEqual(good["defect_count"], 0)
                self.assertNotIn("error", good)

    def test_invalid_artifact_listings_preserve_later_jobs(self):
        event = {"result": "failed", "builds": [
            {"buildTarget": "a", "result": "failed", "debug": {"Artifacts": "directory"}},
            {"buildTarget": "b", "result": "failed", "debug": {"buildLog": "https://example/b.log"}}]}
        for listing in (None, [], {}, {"data": None}, {"data": []}):
            with self.subTest(listing=listing), \
                 patch.object(openharmony_ci, "http_get_json", side_effect=[{"data": event}, listing]), \
                 patch.object(openharmony_ci, "http_get_bytes", return_value=b"later job log"):
                report = openharmony_ci.build_output(self.args())
            self.assertFalse(report["complete"])
            self.assertIn("artifact listing", report["errors"][0]["error"])
            self.assertEqual(report["jobs"][1]["log_detail"]["tail"], "later job log")

    def test_corrupt_deflate_archive_preserves_later_jobs(self):
        buffer = io.BytesIO()
        with openharmony_ci.zipfile.ZipFile(buffer, "w", compression=openharmony_ci.zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("build.log", "compiler error\n" * 20)
        payload = bytearray(buffer.getvalue())
        offset = 30 + int.from_bytes(payload[26:28], "little") + int.from_bytes(payload[28:30], "little")
        payload[offset] = (payload[offset] & 0xf8) | 0x07  # Reserved DEFLATE block type.
        event = {"result": "failed", "builds": [
            {"buildTarget": name, "result": "failed", "debug": {"buildLog": f"https://example/{name}.log"}}
            for name in ("a", "b")]}
        with patch.object(openharmony_ci, "http_get_json", return_value={"data": event}), \
             patch.object(openharmony_ci, "http_get_bytes", side_effect=[bytes(payload), b"later job log"]):
            report = openharmony_ci.build_output(self.args())
        self.assertFalse(report["complete"])
        self.assertIn("unable to read log archive", report["errors"][0]["error"])
        self.assertEqual(report["jobs"][1]["log_detail"]["tail"], "later job log")

    def test_zip_selection_ignores_directories(self):
        buffer = io.BytesIO()
        with openharmony_ci.zipfile.ZipFile(buffer, "w") as archive:
            archive.writestr("logs/", b"")
            archive.writestr("logs/compile.txt", b"compiler error")
        member, tail = openharmony_ci.inspect_archive_bytes(buffer.getvalue(), 80)
        self.assertEqual(member, "logs/compile.txt")
        self.assertEqual(tail, "compiler error")

    def test_invalid_task_identifiers_preserve_summary_and_later_tasks(self):
        for summary in ({"result": "noPass", "issue_count": 5},
                        {"task_id": " "}, {"task_id": 42}, None):
            event = {"result": "failed", "uuid": "uuid", "codeCheckSummary": [summary, {"task_id": "good"}]}
            with self.subTest(summary=summary), \
                 patch.object(openharmony_ci, "http_get_json", return_value={"data": event}), \
                 patch.object(openharmony_ci, "http_post_json", return_value={"data": {"count": 0, "defects": []}}) as post:
                report = openharmony_ci.build_output(self.args())
            self.assertFalse(report["complete"])
            self.assertFalse(report["codecheck"]["complete"])
            bad, good = report["codecheck"]["tasks"]
            self.assertEqual(bad["summary"], summary)
            self.assertIsNone(bad["defect_count"])
            self.assertIn("summary[0]", bad["error"])
            self.assertEqual(good["defect_count"], 0)
            self.assertEqual(post.call_count, 1)
            with redirect_stdout(io.StringIO()):
                openharmony_ci.print_text_report(report)

    def test_downloads_with_same_basename_do_not_overwrite(self):
        with TemporaryDirectory() as directory:
            first = openharmony_ci.maybe_write_download(directory, "https://example/a/build.log.zip", b"first")
            second = openharmony_ci.maybe_write_download(directory, "https://example/b/build.log.zip", b"second")
            self.assertNotEqual(first, second)
            self.assertEqual(Path(first).read_bytes(), b"first")
            self.assertEqual(Path(second).read_bytes(), b"second")


if __name__ == "__main__":
    main()
