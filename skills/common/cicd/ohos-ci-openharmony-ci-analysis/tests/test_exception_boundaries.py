"""Offline regression tests for external-data and partial-result boundaries."""
import io
import json
import subprocess
from argparse import Namespace
from contextlib import redirect_stdout
from unittest import TestCase, main
from unittest.mock import MagicMock, patch

from test_openharmony_ci import openharmony_ci as ci


def args(**overrides):
    values = dict(pr=None, pr_url=None, event_id='event', repo=None,
                  log_mode='auto', log_lines=80, download_dir=None,
                  codecheck_mode='auto', codecheck_page_size=300)
    values.update(overrides)
    return Namespace(**values)


def page(count, *ids):
    return {'data': {'count': count, 'defects': [
        {'defectId': identity, 'defectDetailList': [
            {'id': identity, 'filepath': identity + '.cpp'}]} for identity in ids]}}


class ExceptionBoundaryTests(TestCase):
    def test_auto_skipped_codecheck_does_not_claim_zero_defects(self):
        event = {'result': 'success', 'uuid': 'uuid', 'codeCheckSummary': [
            {'task_id': 'task', 'result': 'pass', 'issue_count': 3}]}
        with patch.object(ci, 'http_get_json', return_value={'data': event}), \
             patch.object(ci, 'http_post_json') as post:
            report = ci.build_output(args())
        post.assert_not_called()
        self.assertNotIn('codecheck', report)

    def test_paths_and_names_do_not_crash_either_output_mode(self):
        event = {'result': 'failed', 'uuid': 'uuid', 'builds': [
            {'buildTarget': {'name': 'broken'}, 'result': 'failed',
             'debug': {'Artifacts': {'path': 'x'}, 'buildLog': 42}},
            {'debug': {'component': ['bad']}, 'result': 'failed'},
            {'buildTarget': 'ok', 'result': 'failed', 'debug': {'buildLog': '/ok.log'}}],
            'codeCheckSummary': [{'task_id': 'valid'}]}
        with patch.object(ci, 'http_get_json', return_value={'data': event}), \
             patch.object(ci, 'http_get_bytes', return_value=b'error'), \
             patch.object(ci, 'http_post_json', return_value=page(0)):
            report = ci.build_output(args())
        self.assertFalse(report['complete'])
        self.assertEqual(report['jobs'][2]['log_detail']['tail'], 'error')
        self.assertEqual(report['codecheck']['tasks'][0]['defect_count'], 0)
        with redirect_stdout(io.StringIO()):
            ci.print_text_report(report)
        self.assertIn('broken', json.dumps(report))  # Original data retained.

    def test_subprocess_errors_are_domain_errors_and_timeout_is_set(self):
        for error in (PermissionError('not executable'),
                      UnicodeDecodeError('utf8', b'\xff', 0, 1, 'bad'),
                      subprocess.TimeoutExpired('oh-gc', 60)):
            with self.subTest(error=type(error)), patch.object(ci.subprocess, 'run', side_effect=error) as run:
                with self.assertRaises(ci.ToolError):
                    ci.run_oh_gc(['pr:comments'])
                self.assertEqual(run.call_args.kwargs['timeout'], ci.OH_GC_TIMEOUT)

    def test_invalid_summary_container_and_build_elements_mark_incomplete(self):
        for summaries in ({'result': 'noPass'}, None, 'invalid'):
            event = {'result': 'failed', 'builds': [None, 'bad', {'buildTarget': 'ok', 'result': 'success'}],
                     'codeCheckSummary': summaries}
            with self.subTest(summaries=summaries), patch.object(ci, 'http_get_json', return_value={'data': event}):
                report = ci.build_output(args())
            self.assertFalse(report['complete'])
            self.assertEqual(len(report['errors']), 3)
            self.assertEqual(report['jobs'][0]['job_name'], 'ok')
            self.assertFalse(report['codecheck']['complete'])

    def test_artifact_leaf_errors_preserve_valid_logs(self):
        listing = {'data': {'bad': {'url': None}, 'build.log': {'url': '/logs/build.log'}}}
        with patch.object(ci, 'http_get_json', return_value=listing), \
             patch.object(ci, 'http_get_bytes', return_value=b'compiler error'):
            result = ci.fetch_job_logs({'artifacts': 'dir'}, 80, None)
        self.assertIn('bad', result['error'])
        self.assertEqual(result['tail'], 'compiler error')

    def test_truncated_zip_and_tar_are_not_text(self):
        zipped = io.BytesIO()
        with ci.zipfile.ZipFile(zipped, 'w') as archive:
            archive.writestr('build.log', 'error')
        tarred = io.BytesIO()
        with ci.tarfile.open(fileobj=tarred, mode='w') as archive:
            member = ci.tarfile.TarInfo('build.log')
            member.size = 1000
            archive.addfile(member, io.BytesIO(b'x' * 1000))
        for payload in (zipped.getvalue()[:-22], tarred.getvalue()[:600]):
            with self.subTest(size=len(payload)), self.assertRaises(ci.ToolError):
                ci.inspect_archive_bytes(payload, 80)

    def test_valid_archives_and_plain_text_remain_supported(self):
        for mode in ('w', 'w:gz', 'w:bz2', 'w:xz'):
            buffer = io.BytesIO()
            with ci.tarfile.open(fileobj=buffer, mode=mode) as archive:
                member = ci.tarfile.TarInfo('build.log')
                member.size = 5
                archive.addfile(member, io.BytesIO(b'error'))
            self.assertEqual(ci.inspect_archive_bytes(buffer.getvalue(), 80), ('build.log', 'error'))
        self.assertEqual(ci.inspect_archive_bytes(b'ordinary error', 80), ('', 'ordinary error'))

    def test_bad_pagination_retains_first_page_without_duplicate_counts(self):
        for second in (page(2, 'a'), page(2, 'a', 'b'), page(3, 'b'), page(2), ci.ToolError('offline')):
            with self.subTest(second=second), patch.object(ci, 'http_post_json', side_effect=[page(2, 'a'), second]):
                result = ci.fetch_codecheck_defects('uuid', 'task', 1)
            self.assertFalse(result['complete'])
            self.assertIsNone(result['defect_count'])
            self.assertEqual(result['retrieved_count'], 1)
            self.assertEqual(result['defects'][0]['file'], 'a.cpp')
            self.assertEqual(len(result['defects']), 1)

    def test_resource_limits_fail_explicitly(self):
        with patch.object(ci, 'MAX_CODECHECK_PAGES', 1), patch.object(ci, 'http_post_json', return_value=page(2, 'a')):
            result = ci.fetch_codecheck_defects('uuid', 'task', 1)
        self.assertIn('page limit', result['error'])
        self.assertEqual(result['retrieved_count'], 1)
        with patch.object(ci, 'MAX_CODECHECK_DETAILS', 1), patch.object(ci, 'http_post_json', return_value=page(2, 'a', 'b')):
            self.assertIn('limit', ci.fetch_codecheck_defects('uuid', 'task')['error'])
        response = MagicMock()
        response.__enter__.return_value = io.BytesIO(b'12345')
        with patch.object(ci, 'MAX_DOWNLOAD_BYTES', 4), patch.object(ci.urllib.request, 'urlopen', return_value=response):
            with self.assertRaisesRegex(ci.ToolError, 'byte limit'):
                ci.http_get_bytes('https://example/log')
        buffer = io.BytesIO()
        with ci.zipfile.ZipFile(buffer, 'w') as archive:
            archive.writestr('build.log', '12345')
        with patch.object(ci, 'MAX_ARCHIVE_BYTES', 4):
            with self.assertRaisesRegex(ci.ToolError, 'byte limit'):
                ci.inspect_archive_bytes(buffer.getvalue(), 80)

    def test_invalid_arguments_fail_before_network(self):
        for options in ({'log_lines': 0}, {'log_lines': -1}, {'codecheck_page_size': 0},
                        {'pr': -1}, {'pr_url': 'https://[gitcode.com/a/b/pull/1'}):
            with self.subTest(options=options), patch.object(ci, 'http_get_json') as get:
                with self.assertRaises(ci.ToolError):
                    ci.build_output(args(**options))
                get.assert_not_called()

    def test_disk_failure_preserves_tail_and_partial_report(self):
        event = {'result': 'failed', 'builds': [{'buildTarget': 'job', 'result': 'failed',
                                               'debug': {'buildLog': '/build.log'}}]}
        with patch.object(ci, 'http_get_json', return_value={'data': event}), \
             patch.object(ci, 'http_get_bytes', return_value=b'compiler error'), \
             patch.object(ci, 'maybe_write_download', side_effect=OSError('disk full')):
            report = ci.build_output(args(download_dir='/tmp/unused'))
        self.assertFalse(report['complete'])
        self.assertEqual(report['jobs'][0]['log_detail']['tail'], 'compiler error')
        self.assertIn('disk full', report['errors'][0]['error'])

    def test_listing_failure_falls_back_to_absolute_url(self):
        source = 'https://cidownload.openharmony.cn/logs/build.log?token=example'
        with patch.object(ci, 'http_get_json', side_effect=ci.ToolError('listing unavailable')), \
             patch.object(ci, 'http_get_bytes', return_value=b'error') as download:
            result = ci.fetch_job_logs({'artifacts': 'dir', 'build_log': source}, 80, None)
        download.assert_called_once_with(source)
        self.assertEqual(result['tail'], 'error')
        self.assertIn('listing unavailable', result['error'])
        self.assertEqual(ci.normalize_log_url('/logs/build.log'), 'https://cidownload.openharmony.cn/logs/build.log')


if __name__ == '__main__':
    main()
