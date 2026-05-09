#!/usr/bin/env python3
"""
ArkTS 覆盖率扫描异步执行工具
"""

import os
import sys
import io
import json
import signal
import time
import subprocess
import threading
from datetime import datetime
from pathlib import Path

def _setup_stdio():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

_setup_stdio()


class AsyncCoverageScanner:
    """异步覆盖率扫描器"""
    
    def __init__(self, work_dir=None):
        """初始化扫描器
        
        Args:
            work_dir: 工作目录，默认从 .oh-xts-config.json 的 scan_tool_root 读取，
                      回退到 {skill_root}/APICoverageDetector
        """
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
        self.progress_file = self.work_dir / "coverage_scan.progress"
        
    def _process_exists(self, pid):
        if sys.platform == 'win32':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                handle = kernel32.OpenProcess(0x100000, False, pid)
                if handle:
                    kernel32.CloseHandle(handle)
                    return True
                return False
            except Exception:
                return False
        else:
            try:
                os.kill(pid, 0)
                return True
            except ProcessLookupError:
                return False
            except PermissionError:
                return True

    def is_running(self):
        if not self.pid_file.exists():
            return False

        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())

            if not self._process_exists(pid):
                self.pid_file.unlink(missing_ok=True)
                return False
            return True
        except Exception:
            return False
    
    def start_scan(self, config_file=None):
        """启动异步扫描
        
        Args:
            config_file: 配置文件路径，默认为 configs/arkts_config.json
            
        Returns:
            tuple: (success: bool, message: str, pid: int)
        """
        # 检查是否已经在运行
        if self.is_running():
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            return False, f"扫描已在运行中，PID: {pid}", pid
        
        # 检查可执行文件
        if not self.entrance_exe.exists():
            return False, f"扫描入口文件不存在: {self.entrance_exe}", None
        
        # 验证配置文件中的路径
        config_file_path = config_file or (self.work_dir / "configs" / "arkts_config.json")
        if not Path(config_file_path).exists():
            return False, f"配置文件不存在: {config_file_path}", None
        
        # 检查配置中的路径
        try:
            with open(config_file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            case_paths = config.get('case_path', {}).get('open_source', [])
            if not case_paths:
                return False, "配置文件中缺少测试用例路径", None
            
            # 验证每个路径是否存在（相对于 testcase/ 目录）
            testcase_dir = self.work_dir / "testcase"
            for path in case_paths:
                full_path = testcase_dir / path
                if not full_path.exists():
                    return False, f"测试用例路径不存在: {full_path}", None
                    
        except Exception as e:
            return False, f"读取配置文件失败: {e}", None
        
        # 准备输入参数（4 个交互输入：开源=1, public=1, 无特性=N, 全部版本=N）
        # text=True 模式下 Python 会自动处理换行符：Windows 转为 \r\n，Linux 保持 \n
        input_data = "1\n1\nN\nN\n"
        
        # 启动扫描进程
        try:
            process = subprocess.Popen(
                [str(self.entrance_exe)],
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                text=True,
                cwd=str(self.work_dir)
            )
            
            # 发送输入参数
            process.stdin.write(input_data)
            process.stdin.close()
            
            # 保存 PID
            with open(self.pid_file, 'w') as f:
                f.write(str(process.pid))
            
            # 保存启动状态
            self._update_status("running", f"扫描已启动，路径: {case_paths[0]}")
            
            # 启动日志监听线程
            log_thread = threading.Thread(target=self._monitor_log, args=(process,))
            log_thread.daemon = True
            log_thread.start()
            
            return True, f"扫描已启动，PID: {process.pid}, 路径: {case_paths[0]}", process.pid
            
        except Exception as e:
            return False, f"启动扫描失败: {e}", None
    
    def stop_scan(self):
        """停止扫描
        
        Returns:
            tuple: (success: bool, message: str)
        """
        if not self.is_running():
            return False, "没有正在运行的扫描"
        
        try:
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # 终止进程
            if sys.platform == 'win32':
                subprocess.run(['taskkill', '/F', '/PID', str(pid)], capture_output=True)
            else:
                os.kill(pid, signal.SIGKILL)
            
            # 清理文件
            self.pid_file.unlink(missing_ok=True)
            self._update_status("stopped", "扫描已手动停止")
            
            return True, f"已停止扫描，PID: {pid}"
            
        except Exception as e:
            return False, f"停止扫描失败: {e}"
    
    def get_status(self):
        """获取扫描状态
        
        Returns:
            dict: 状态信息
        """
        if not self.is_running():
            # 检查是否完成
            if self.status_file.exists():
                with open(self.status_file, 'r', encoding='utf-8') as f:
                    status_data = json.load(f)
                    if status_data.get('status') == 'completed':
                        return status_data
                    elif status_data.get('status') == 'failed':
                        return status_data
            
            return {
                'status': 'idle',
                'message': '没有正在运行的扫描',
                'timestamp': datetime.now().isoformat()
            }
        
        # 读取进度
        progress = self._read_progress()
        
        return {
            'status': 'running',
            'message': '扫描正在运行',
            'pid': self._read_pid(),
            'progress': progress,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_results(self):
        results = {}

        if not self.results_dir.exists():
            print(f"结果目录不存在: {self.results_dir}")
            return results

        # 实际结果目录结构: results/ets1.1/open_source/sdk_result.xlsx
        version_dirs = [d for d in self.results_dir.iterdir() if d.is_dir()]
        for version_dir in version_dirs:
            for source_dir in [version_dir / "open_source", version_dir / "closed_source"]:
                if not source_dir.is_dir():
                    continue
                source_name = source_dir.name
                version_name = version_dir.name
                result_file = source_dir / "sdk_result.xlsx"
                key = f"{version_name}/{source_name}"
                if result_file.exists():
                    results[key] = {
                        'exists': True,
                        'path': str(result_file),
                        'size': result_file.stat().st_size,
                        'modified': datetime.fromtimestamp(result_file.stat().st_mtime).isoformat()
                    }

        if not results:
            results['no_results'] = {'exists': False, 'message': '未找到扫描结果文件'}

        return results
    
    def _read_pid(self):
        """读取 PID"""
        if self.pid_file.exists():
            with open(self.pid_file, 'r') as f:
                return int(f.read().strip())
        return None
    
    def _update_status(self, status, message):
        """更新状态文件"""
        status_data = {
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(self.status_file, 'w', encoding='utf-8') as f:
            json.dump(status_data, f, indent=2, ensure_ascii=False)
    
    def _read_progress(self):
        """读取进度"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except (json.JSONDecodeError, ValueError):
                    return None
        return None

    def get_log_tail(self, lines=30):
        """读取扫描日志最后 N 行
        
        Args:
            lines: 读取的行数，默认 30
            
        Returns:
            str: 日志最后 N 行内容
        """
        log_file = self.log_dir / "arkts_runner.log"
        if not log_file.exists():
            return f"日志文件不存在: {log_file}"
        
        try:
            with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
                all_lines = f.readlines()
            tail_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
            return ''.join(tail_lines)
        except Exception as e:
            return f"读取日志失败: {e}"
    
    def _monitor_log(self, process):
        """监控日志文件并更新进度"""
        log_file = self.log_dir / "arkts_runner.log"
        
        # 等待日志文件创建
        for _ in range(60):
            if log_file.exists():
                break
            time.sleep(1)
        
        # 监控日志并更新进度
        last_size = 0
        while process.poll() is None:
            try:
                if log_file.exists():
                    current_size = log_file.stat().st_size
                    if current_size > last_size:
                        with open(log_file, 'r', encoding='utf-8', errors='replace') as f:
                            f.seek(last_size)
                            new_content = f.read()
                            last_size = current_size
                            
                            progress = self._parse_progress(new_content)
                            if progress:
                                self._write_progress(progress)
                
                time.sleep(2)
                
            except Exception as e:
                time.sleep(2)
        
        # 等待进程完全结束
        process.wait()
        
        # 更新最终状态
        if process.returncode == 0:
            self._update_status('completed', '扫描完成')
        else:
            self._update_status('failed', f'扫描失败，返回码: {process.returncode}')
        
        # 清理 PID 文件
        self.pid_file.unlink(missing_ok=True)
    
    def _parse_progress(self, log_content):
        """解析日志内容中的进度信息"""
        progress = {}
        
        # 检查各个阶段
        stages = [
            '(1/10) count工具',
            '(2/10) metrics工具',
            '(3/10) 检查metrics工具结果',
            '(4/10) 扫描覆盖率',
            '(5/10) 汇总覆盖率信息',
            '(6/10) 统计覆盖度',
            '(7/10) 检查参数规格',
            '(8/10) 检查错误码',
            '(9/10) 检查返回值',
            '(10/10) 格式化输出'
        ]
        
        for i, stage in enumerate(stages):
            if stage in log_content:
                progress['current_stage'] = i + 1
                progress['total_stages'] = 10
                progress['stage_name'] = stage
                progress['progress_percent'] = (i + 1) * 10
                break
        
        return progress
    
    def _write_progress(self, progress):
        """写入进度文件"""
        if progress:
            progress['timestamp'] = datetime.now().isoformat()
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(progress, f, indent=2, ensure_ascii=False)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python async_coverage_scan.py start   - 启动扫描")
        print("  python async_coverage_scan.py stop    - 停止扫描")
        print("  python async_coverage_scan.py status  - 查看状态")
        print("  python async_coverage_scan.py results - 获取结果")
        print("  python async_coverage_scan.py log     - 查看最近日志 (默认30行)")
        print("  python async_coverage_scan.py log 50  - 查看最近50行日志")
        sys.exit(1)
    
    command = sys.argv[1]
    scanner = AsyncCoverageScanner()
    
    if command == "start":
        success, message, pid = scanner.start_scan()
        print(f"{'✅' if success else '❌'} {message}")
        if success:
            print(f"使用 'python {sys.argv[0]} status' 查看状态")
            print(f"使用 'python {sys.argv[0]} results' 获取结果")
    
    elif command == "stop":
        success, message = scanner.stop_scan()
        print(f"{'✅' if success else '❌'} {message}")
    
    elif command == "status":
        status = scanner.get_status()
        print(json.dumps(status, indent=2, ensure_ascii=False))
    
    elif command == "results":
        results = scanner.get_results()
        print(json.dumps(results, indent=2, ensure_ascii=False))

    elif command == "log":
        lines = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        print(scanner.get_log_tail(lines))
    
    else:
        print(f"未知命令: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()