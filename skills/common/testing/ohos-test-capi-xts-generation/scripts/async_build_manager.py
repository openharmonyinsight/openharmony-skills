#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenHarmony CAPI XTS 异步编译管理器
方案 A：轻量级后台编译 + 日志轮询

使用方法:
    from async_build_manager import AsyncBuildManager
    
    manager = AsyncBuildManager(OH_ROOT)
    
    # 启动编译
    manager.start_build("ActsCameraManagerCapiTest")
    
    # 检查状态
    status = manager.get_status("ActsCameraManagerCapiTest")
    
    # 等待完成
    result = manager.wait_for_completion("ActsCameraManagerCapiTest")
"""

import os
import sys
import subprocess
import time
import json
import re
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from dataclasses import dataclass
from enum import Enum


class BuildStatus(Enum):
    """编译状态枚举"""
    NOT_STARTED = "NOT_STARTED"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    STOPPED = "STOPPED"
    UNKNOWN = "UNKNOWN"


@dataclass
class BuildResult:
    """编译结果数据类"""
    suite_name: str
    status: BuildStatus
    exit_code: int = -1
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    log_file: Optional[str] = None
    error_file: Optional[str] = None
    errors: list = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "suite_name": self.suite_name,
            "status": self.status.value,
            "exit_code": self.exit_code,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "log_file": self.log_file,
            "error_file": self.error_file,
            "errors": self.errors
        }


class AsyncBuildManager:
    """异步编译管理器"""
    
    LOG_DIR = "/tmp/oh_capi_build"
    SCRIPT_PATH = Path(__file__).parent / "async_build.sh"
    
    def __init__(self, oh_root: str, product_name: str = "rk3568"):
        """
        初始化异步编译管理器
        
        Args:
            oh_root: OpenHarmony 工程根目录
            product_name: 产品名称，默认 rk3568
        """
        self.oh_root = Path(oh_root).resolve()
        self.product_name = product_name
        
        # 验证路径
        if not self.oh_root.exists():
            raise ValueError(f"OH_ROOT 目录不存在: {self.oh_root}")
        
        build_script = self.oh_root / "test" / "xts" / "acts" / "build.sh"
        if not build_script.exists():
            raise ValueError(f"编译脚本不存在: {build_script}")
        
        # 创建日志目录
        os.makedirs(self.LOG_DIR, exist_ok=True)
    
    def _get_file_paths(self, suite_name: str) -> Dict[str, Path]:
        """获取编译相关文件路径"""
        return {
            "log": Path(self.LOG_DIR) / f"{suite_name}.log",
            "pid": Path(self.LOG_DIR) / f"{suite_name}.pid",
            "status": Path(self.LOG_DIR) / f"{suite_name}.status",
            "error": Path(self.LOG_DIR) / f"{suite_name}.error"
        }
    
    def start_build(self, suite_name: str, blocking: bool = False, timeout: int = 3600) -> BuildResult:
        """
        启动编译
        
        Args:
            suite_name: 测试套名称
            blocking: 是否阻塞等待完成
            timeout: 阻塞模式下的超时时间（秒）
        
        Returns:
            BuildResult: 编译结果
        """
        cmd = [
            str(self.SCRIPT_PATH),
            str(self.oh_root),
            suite_name,
            self.product_name,
            "start"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            return BuildResult(
                suite_name=suite_name,
                status=BuildStatus.FAILED,
                errors=[result.stderr]
            )
        
        if blocking:
            return self.wait_for_completion(suite_name, timeout)
        
        return BuildResult(
            suite_name=suite_name,
            status=BuildStatus.RUNNING
        )
    
    def get_status(self, suite_name: str) -> BuildResult:
        """
        获取编译状态
        
        Args:
            suite_name: 测试套名称
        
        Returns:
            BuildResult: 编译状态
        """
        paths = self._get_file_paths(suite_name)
        
        # 读取状态文件
        if paths["status"].exists():
            status_data = self._parse_status_file(paths["status"])
        else:
            status_data = {}
        
        # 检查进程状态
        pid = self._read_pid(paths["pid"])
        if pid:
            if self._is_process_running(pid):
                status = BuildStatus.RUNNING
            else:
                # 进程已结束，从状态文件获取最终状态
                status_str = status_data.get("status", "UNKNOWN")
                status = BuildStatus(status_str) if status_str in [s.value for s in BuildStatus] else BuildStatus.UNKNOWN
        else:
            if status_data:
                status_str = status_data.get("status", "UNKNOWN")
                status = BuildStatus(status_str) if status_str in [s.value for s in BuildStatus] else BuildStatus.UNKNOWN
            else:
                status = BuildStatus.NOT_STARTED
        
        # 读取错误信息
        errors = []
        if paths["error"].exists():
            with open(paths["error"], "r", encoding="utf-8", errors="ignore") as f:
                errors = [line.strip() for line in f if line.strip()]
        
        return BuildResult(
            suite_name=suite_name,
            status=status,
            exit_code=status_data.get("exit_code", -1),
            start_time=status_data.get("start_time"),
            end_time=status_data.get("end_time"),
            log_file=str(paths["log"]) if paths["log"].exists() else None,
            error_file=str(paths["error"]) if paths["error"].exists() else None,
            errors=errors
        )
    
    def wait_for_completion(self, suite_name: str, timeout: int = 3600, poll_interval: float = 2.0) -> BuildResult:
        """
        等待编译完成
        
        Args:
            suite_name: 测试套名称
            timeout: 超时时间（秒）
            poll_interval: 轮询间隔（秒）
        
        Returns:
            BuildResult: 编译结果
        """
        start_time = time.time()
        
        while True:
            result = self.get_status(suite_name)
            
            # 检查是否完成
            if result.status not in [BuildStatus.RUNNING, BuildStatus.NOT_STARTED]:
                return result
            
            # 检查超时
            if time.time() - start_time > timeout:
                return BuildResult(
                    suite_name=suite_name,
                    status=BuildStatus.FAILED,
                    errors=["编译超时"]
                )
            
            time.sleep(poll_interval)
    
    def stop_build(self, suite_name: str) -> BuildResult:
        """
        停止编译
        
        Args:
            suite_name: 测试套名称
        
        Returns:
            BuildResult: 操作结果
        """
        cmd = [
            str(self.SCRIPT_PATH),
            str(self.oh_root),
            suite_name,
            self.product_name,
            "stop"
        ]
        
        subprocess.run(cmd, capture_output=True, text=True)
        
        return BuildResult(
            suite_name=suite_name,
            status=BuildStatus.STOPPED
        )
    
    def tail_logs(self, suite_name: str, lines: int = 50) -> str:
        """
        获取最近的日志
        
        Args:
            suite_name: 测试套名称
            lines: 行数
        
        Returns:
            str: 日志内容
        """
        paths = self._get_file_paths(suite_name)
        
        if not paths["log"].exists():
            return "日志文件不存在"
        
        cmd = ["tail", "-n", str(lines), str(paths["log"])]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        return result.stdout
    
    def get_progress(self, suite_name: str) -> Dict[str, Any]:
        """
        获取编译进度信息
        
        Args:
            suite_name: 测试套名称
        
        Returns:
            Dict: 进度信息
        """
        paths = self._get_file_paths(suite_name)
        result = self.get_status(suite_name)
        
        progress = {
            "status": result.status.value,
            "log_size": 0,
            "log_lines": 0,
            "recent_logs": []
        }
        
        if paths["log"].exists():
            stat = paths["log"].stat()
            progress["log_size"] = stat.st_size
            
            with open(paths["log"], "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                progress["log_lines"] = len(lines)
                progress["recent_logs"] = [line.strip() for line in lines[-10:]]
        
        return progress
    
    def cleanup(self, suite_name: str = None):
        """
        清理编译临时文件
        
        Args:
            suite_name: 测试套名称，为 None 时清理所有
        """
        if suite_name:
            paths = self._get_file_paths(suite_name)
            for path in paths.values():
                if path.exists():
                    path.unlink()
        else:
            log_dir = Path(self.LOG_DIR)
            for file in log_dir.glob("*"):
                file.unlink()
    
    def _parse_status_file(self, status_file: Path) -> Dict[str, Any]:
        """解析状态文件"""
        data = {}
        
        if not status_file.exists():
            return data
        
        with open(status_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                match = re.match(r'\[BUILD\]\s+([\w]+):\s*(.+)', line)
                if match:
                    key = match.group(1).lower()
                    value = match.group(2).strip()
                    
                    if key == "exit_code":
                        try:
                            value = int(value)
                        except ValueError:
                            pass
                    
                    data[key] = value
        
        return data
    
    def _read_pid(self, pid_file: Path) -> Optional[int]:
        """读取 PID"""
        if not pid_file.exists():
            return None
        
        try:
            with open(pid_file, "r") as f:
                return int(f.read().strip())
        except (ValueError, IOError):
            return None
    
    def _is_process_running(self, pid: int) -> bool:
        """检查进程是否在运行"""
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False


# 命令行接口
def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenHarmony CAPI XTS 异步编译管理器")
    parser.add_argument("oh_root", help="OpenHarmony 工程根目录")
    parser.add_argument("suite_name", help="测试套名称")
    parser.add_argument("--action", "-a", 
                        choices=["start", "status", "wait", "stop", "logs", "progress"],
                        default="start",
                        help="执行的操作")
    parser.add_argument("--product", "-p", default="rk3568", help="产品名称")
    parser.add_argument("--timeout", "-t", type=int, default=3600, help="超时时间（秒）")
    parser.add_argument("--blocking", "-b", action="store_true", help="阻塞等待完成")
    
    args = parser.parse_args()
    
    manager = AsyncBuildManager(args.oh_root, args.product)
    
    if args.action == "start":
        result = manager.start_build(args.suite_name, blocking=args.blocking, timeout=args.timeout)
    elif args.action == "status":
        result = manager.get_status(args.suite_name)
    elif args.action == "wait":
        result = manager.wait_for_completion(args.suite_name, timeout=args.timeout)
    elif args.action == "stop":
        result = manager.stop_build(args.suite_name)
    elif args.action == "logs":
        logs = manager.tail_logs(args.suite_name)
        print(logs)
        return
    elif args.action == "progress":
        progress = manager.get_progress(args.suite_name)
        print(json.dumps(progress, indent=2, ensure_ascii=False))
        return
    
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
