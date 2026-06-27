#!/usr/bin/env python3
"""
ArkTS 覆盖率扫描异步执行工具

状态判断（WSL 优化）：
  1. PID 存活 → running
  2. PID 已死 + WSL + 日志 90s 内活跃 → running
  3. PID 已死 + status_file 是终态 → 返回终态
  4. PID 已死 + status_file 非终态 → 从日志推断
  5. 无 status_file → 从日志推断
  6. 以上都不满足 → idle

进度（stage）始终从日志实时解析，不依赖额外文件。
"""

import os
import re
import sys
import io
import json
import signal
import time
import subprocess
import threading
import argparse
from datetime import datetime
from pathlib import Path

def _setup_stdio():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

_setup_stdio()


class AsyncCoverageScanner:
    """异步覆盖率扫描器"""

    STAGES = [
        '(1/10)', '(2/10)', '(3/10)', '(4/10)', '(5/10)',
        '(6/10)', '(7/10)', '(8/10)', '(9/10)', '(10/10)',
    ]
    COMPLETION_MARKERS = ('日志句柄删除 OK', 'complete the execution')
    ERROR_MARKERS = ('ERROR', 'Traceback')

    def __init__(self, work_dir=None):
        if work_dir is None:
            script_dir = Path(__file__).parent
            skill_root = script_dir.parent
            config_path = skill_root / ".oh-xts-config.json"
            scan_tool_root = None
            if config_path.exists():
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        cfg = json.load(f)
                    scan_tool_root = cfg.get('scan_tool_root', '')
                    if scan_tool_root and not Path(scan_tool_root).is_dir():
                        scan_tool_root = ''
                except Exception:
                    scan_tool_root = ''
            self.work_dir = Path(scan_tool_root) if scan_tool_root else (skill_root / "APICoverageDetector")
        else:
            self.work_dir = Path(work_dir)

        self.entrance_exe = self.work_dir / "arkts_entrance" / "arkts_entrance.exe"
        self.results_dir = self.work_dir / "results"
        self.log_dir = self.work_dir / "log"
        self.pid_file = self.work_dir / "coverage_scan.pid"
        self.status_file = self.work_dir / "coverage_scan.status"
        self._is_wsl = self._detect_wsl()

    # ── helpers ──────────────────────────────────────────────────────

    @staticmethod
    def _wsl_to_win_path(wsl_path):
        p = str(wsl_path)
        if p.startswith('/mnt/') and len(p) > 5:
            drive = p[5].upper()
            rest = p[6:]
            return drive + ':' + rest.replace('/', '\\')
        return p

    @staticmethod
    def _detect_wsl():
        try:
            if sys.platform == 'linux' and os.path.exists('/proc/version'):
                with open('/proc/version', 'r') as f:
                    return 'microsoft' in f.read().lower()
        except Exception:
            pass
        return False

    def _process_exists(self, pid):
        try:
            os.kill(pid, 0)
            return True
        except ProcessLookupError:
            return False
        except PermissionError:
            return True

    def _is_log_active(self, threshold_seconds=90):
        log_file = self.log_dir / "arkts_runner.log"
        if not log_file.exists():
            return False
        try:
            return (time.time() - log_file.stat().st_mtime) < threshold_seconds
        except Exception:
            return False

    def _read_pid(self):
        if self.pid_file.exists():
            with open(self.pid_file, 'r') as f:
                return int(f.read().strip())
        return None

    def _read_log_content(self, tail_bytes=8000):
        log_file = self.log_dir / "arkts_runner.log"
        if not log_file.exists():
            return ''
        try:
            with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
                f.seek(0, 2)
                size = f.tell()
                if size > tail_bytes:
                    f.seek(size - tail_bytes)
                return f.read()
        except Exception:
            return ''

    def _parse_stage_from_log(self):
        content = self._read_log_content()
        if not content:
            return None
        matched_idx = 0
        for i, stage in enumerate(self.STAGES):
            if stage in content:
                matched_idx = i
        return {
            'current_stage': matched_idx + 1,
            'total_stages': 10,
            'stage_name': self.STAGES[matched_idx],
            'progress_percent': (matched_idx + 1) * 10,
        }

    def _update_status(self, status, message, pid=None):
        status_data = {
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'pid': pid,
        }
        if pid is None and self.status_file.exists():
            try:
                with open(self.status_file, 'r', encoding='utf-8') as f:
                    old = json.load(f)
                if 'pid' in old:
                    status_data['pid'] = old['pid']
            except Exception:
                pass
        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump(status_data, f, indent=2, ensure_ascii=False)

    # ── public API ───────────────────────────────────────────────────

    def is_running(self):
        if not self.pid_file.exists():
            return False
        try:
            pid = int(self.pid_file.read_text().strip())
            if self._process_exists(pid):
                return True
            if self._is_wsl and self._is_log_active():
                return True
            self.pid_file.unlink(missing_ok=True)
            return False
        except Exception:
            return False

    def get_status(self):
        if self.is_running():
            return {
                'status': 'running',
                'message': '扫描正在运行',
                'pid': self._read_pid(),
                'stage': self._parse_stage_from_log(),
                'timestamp': datetime.now().isoformat(),
            }

        if self._is_wsl and self._is_log_active():
            return {
                'status': 'running',
                'message': '扫描正在运行（日志活跃，WSL 进程仍在执行）',
                'stage': self._parse_stage_from_log(),
                'timestamp': datetime.now().isoformat(),
            }

        if self.status_file.exists():
            try:
                with open(self.status_file, 'r', encoding='utf-8') as f:
                    status_data = json.load(f)
                if status_data.get('status') in ('completed', 'failed', 'stopped'):
                    return status_data
                if status_data.get('status') == 'running':
                    inferred = self._infer_from_log()
                    self._update_status(inferred['status'], inferred['message'],
                                        pid=status_data.get('pid'))
                    return inferred
            except Exception:
                pass

        inferred = self._infer_from_log()
        if inferred['status'] != 'idle':
            return inferred

        return {
            'status': 'idle',
            'message': '没有正在运行的扫描',
            'timestamp': datetime.now().isoformat(),
        }

    def get_results(self):
        results = {}
        if not self.results_dir.exists():
            return results
        for version_dir in self.results_dir.iterdir():
            if not version_dir.is_dir():
                continue
            for source_dir in [version_dir / "open_source", version_dir / "closed_source"]:
                if not source_dir.is_dir():
                    continue
                result_file = source_dir / "sdk_result.xlsx"
                key = f"{version_dir.name}/{source_dir.name}"
                if result_file.exists():
                    results[key] = {
                        'exists': True,
                        'path': str(result_file),
                        'size': result_file.stat().st_size,
                        'modified': datetime.fromtimestamp(result_file.stat().st_mtime).isoformat(),
                    }
        if not results:
            results['no_results'] = {'exists': False, 'message': '未找到扫描结果文件'}
        return results

    def get_log_tail(self, lines=30):
        log_file = self.log_dir / "arkts_runner.log"
        if not log_file.exists():
            return f"日志文件不存在: {log_file}"
        try:
            with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
                all_lines = f.readlines()
            return ''.join(all_lines[-lines:] if len(all_lines) > lines else all_lines)
        except Exception as e:
            return f"读取日志失败: {e}"

    # ── scan lifecycle ───────────────────────────────────────────────

    def start_scan(self, config_file=None):
        if self.is_running():
            return False, f"扫描已在运行中，PID: {self._read_pid()}", self._read_pid()

        if not self.entrance_exe.exists():
            return False, f"扫描入口文件不存在: {self.entrance_exe}", None

        env_label = 'WSL' if self._is_wsl else ('Windows' if sys.platform == 'win32' else 'Linux')
        if env_label == 'Linux' and not self._is_wsl:
            return False, "APICoverageDetector 为 Windows .exe 工具，Linux 计算云不可用。请提供覆盖率报告或使用 WSL 环境。", None

        config_file_path = config_file or (self.work_dir / "configs" / "arkts_config.json")
        if not Path(config_file_path).exists():
            return False, f"配置文件不存在: {config_file_path}", None

        try:
            with open(config_file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            case_paths = config.get('case_path', {}).get('open_source', [])
            if not case_paths:
                return False, "配置文件中缺少测试用例路径", None
            testcase_dir = self.work_dir / "testcase"
            for path in case_paths:
                if not (testcase_dir / path).exists():
                    return False, f"测试用例路径不存在: {testcase_dir / path}", None
        except Exception as e:
            return False, f"读取配置文件失败: {e}", None

        input_data = "1\n1\nN\nN\n"
        self._scan_error_log = self.work_dir / "scan_error.log"

        for stale in [self.pid_file, self.status_file, self._scan_error_log]:
            stale.unlink(missing_ok=True)

        try:
            exe_str = str(self.entrance_exe)

            if self._is_wsl:
                win_work_dir = self._wsl_to_win_path(str(self.work_dir))
                stdin_path = self.work_dir / 'stdin_input.txt'
                stdin_path.write_text(input_data, encoding='utf-8')
                win_stdin = self._wsl_to_win_path(str(stdin_path))
                bat_path = self.work_dir / 'wsl_scan_launcher.bat'
                bat_path.write_text(
                    '@echo off\n'
                    f'cd /d {win_work_dir}\n'
                    f'type {win_stdin} | arkts_entrance\\arkts_entrance.exe\n',
                    encoding='ascii',
                )
                win_bat = self._wsl_to_win_path(str(bat_path))
                stderr_file = open(self._scan_error_log, 'w', encoding='utf-8', errors='replace')
                process = subprocess.Popen(
                    ['/init', '/mnt/c/Windows/system32/cmd.exe', '/c', win_bat],
                    stdout=subprocess.DEVNULL,
                    stderr=stderr_file,
                    cwd='/tmp',
                )
            else:
                stderr_file = open(self._scan_error_log, 'w', encoding='utf-8', errors='replace')
                process = subprocess.Popen(
                    [exe_str],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.DEVNULL,
                    stderr=stderr_file,
                    text=True,
                    cwd=str(self.work_dir),
                )
                process.stdin.write(input_data)
                process.stdin.close()

            with open(self.pid_file, 'w') as f:
                f.write(str(process.pid))

            self._update_status("running", f"扫描已启动 [{env_label}]，路径: {case_paths[0]}", pid=process.pid)

            threading.Thread(target=self._monitor_log, args=(process, stderr_file), daemon=False).start()

            return True, f"扫描已启动 [{env_label}]，PID: {process.pid}, 路径: {case_paths[0]}", process.pid

        except Exception as e:
            return False, f"启动扫描失败: {e}", None

    def stop_scan(self):
        if not self.is_running():
            return False, "没有正在运行的扫描"
        try:
            pid = self._read_pid()
            if sys.platform == 'win32':
                subprocess.run(['taskkill', '/F', '/PID', str(pid)], capture_output=True)
            elif self._is_wsl:
                subprocess.run(['/init', '/mnt/c/Windows/system32/cmd.exe', '/c',
                                f'taskkill /F /PID {pid}'], capture_output=True)
            else:
                os.kill(pid, signal.SIGKILL)
            self.pid_file.unlink(missing_ok=True)
            self._update_status("stopped", "扫描已手动停止")
            return True, f"已停止扫描，PID: {pid}"
        except Exception as e:
            return False, f"停止扫描失败: {e}"

    # ── internal ─────────────────────────────────────────────────────

    def _infer_from_log(self):
        content = self._read_log_content()
        ts = datetime.now().isoformat()
        if not content:
            return {'status': 'idle', 'message': '没有正在运行的扫描', 'timestamp': ts}
        if any(m in content for m in self.COMPLETION_MARKERS):
            return {'status': 'completed', 'message': '扫描完成（日志推断）', 'timestamp': ts}
        if any(m in content for m in self.ERROR_MARKERS):
            err_lines = [l for l in content.split('\n') if any(m in l for m in self.ERROR_MARKERS)]
            return {'status': 'failed',
                    'message': f"扫描失败（日志推断）\n{chr(10).join(err_lines[:5])}",
                    'timestamp': ts}
        if self._is_log_active():
            return {'status': 'running',
                    'message': '扫描正在运行（日志活跃，无完成标记）',
                    'timestamp': ts}
        return {'status': 'idle', 'message': '没有正在运行的扫描', 'timestamp': ts}

    def _monitor_log(self, process, stderr_file=None):
        log_file = self.log_dir / "arkts_runner.log"

        for _ in range(60):
            if log_file.exists():
                break
            time.sleep(1)

        while True:
            if self._is_wsl:
                if not self._is_log_active(threshold_seconds=120) and not self._process_exists(process.pid):
                    break
            else:
                if process.poll() is not None:
                    break
            time.sleep(3)

        if process.poll() is None:
            try:
                process.wait(timeout=5)
            except Exception:
                pass

        if stderr_file and not stderr_file.closed:
            try:
                stderr_file.close()
            except Exception:
                pass

        error_hints = ''
        if self._scan_error_log.exists():
            try:
                with open(self._scan_error_log, 'r', encoding='utf-8', errors='replace') as f:
                    err_lines = [l.strip() for l in f
                                 if l.strip() and 'UNC' not in l and 'CMD.EXE' not in l]
                if err_lines:
                    error_hints = '\nstderr: ' + '\n'.join(err_lines[:10])
            except Exception:
                pass

        content = self._read_log_content()
        if self._is_wsl:
            if any(m in content for m in self.COMPLETION_MARKERS):
                self._update_status('completed', '扫描完成', pid=process.pid)
            elif any(m in content for m in self.ERROR_MARKERS):
                err_msg = '\n'.join(l for l in content.split('\n')
                                    if any(m in l for m in ('ERROR', 'Traceback', 'Error')))
                self._update_status('failed', f'扫描失败\n{err_msg[:500]}', pid=process.pid)
            else:
                self._update_status('completed', '扫描完成', pid=process.pid)
        elif process.returncode == 0:
            self._update_status('completed', '扫描完成', pid=process.pid)
        else:
            self._update_status('failed', f'扫描失败，返回码: {process.returncode}{error_hints}', pid=process.pid)

        self.pid_file.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(
        description='ArkTS 覆盖率扫描异步执行工具',
        usage='python async_coverage_scan.py <command> [options]',
    )
    sub = parser.add_subparsers(dest='command', help='可用命令')
    sub.add_parser('start', help='启动异步覆盖率扫描')
    sub.add_parser('stop', help='停止正在运行的扫描')
    sub.add_parser('status', help='查看当前扫描状态')
    sub.add_parser('results', help='获取扫描结果')
    lp = sub.add_parser('log', help='查看最近扫描日志')
    lp.add_argument('-n', '--lines', type=int, default=30, help='显示最后 N 行日志 (默认: 30)')

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    scanner = AsyncCoverageScanner()

    if args.command == "start":
        ok, msg, pid = scanner.start_scan()
        print(f"{'✅' if ok else '❌'} {msg}")
        if ok:
            print(f"使用 'python {sys.argv[0]} status' 查看状态")
            print(f"使用 'python {sys.argv[0]} results' 获取结果")
    elif args.command == "stop":
        ok, msg = scanner.stop_scan()
        print(f"{'✅' if ok else '❌'} {msg}")
    elif args.command == "status":
        print(json.dumps(scanner.get_status(), indent=2, ensure_ascii=False))
    elif args.command == "results":
        print(json.dumps(scanner.get_results(), indent=2, ensure_ascii=False))
    elif args.command == "log":
        print(scanner.get_log_tail(args.lines))


if __name__ == "__main__":
    main()
