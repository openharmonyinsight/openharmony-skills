#!/usr/bin/env python3
# coding=utf-8 -*-
"""burn_one.py 进程清理回归测试（mock 进程表，不杀任何真实进程）。

覆盖：-com:<数字> 精确解析（不做全文子串匹配）、端口号归一比较（COM9/com9/9 同端口）、
父进程存活=活跃任务不杀、归属不明跳过、登记在册孤儿的清理（登记 PID + 进程名/端口
+ owner 创建时间三重校验，PID 复用防护）、COM 端口排他锁（含双进程同端口竞态）。

运行（两种入口等价，无需 pyserial / pytest）：
  python tools/test_burn_one_kill.py
  python -m unittest discover -s skills/ohos-ci-lite-deploy-burn/tools -p "test_*.py"
"""

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import types
import unittest

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))

# burn_one.py 顶部 import serial 缺失即 sys.exit——先探测/打桩，保证测试机无需 pyserial
if "serial" not in sys.modules:
    try:
        import serial  # noqa: F401
    except ImportError:
        _stub = types.ModuleType("serial")

        class _Serial:
            def __init__(self, *a, **k):
                raise RuntimeError("pyserial 未安装（测试桩，不触串口）")

        _stub.Serial = _Serial
        sys.modules["serial"] = _stub

spec = importlib.util.spec_from_file_location("burn_one", os.path.join(HERE, "burn_one.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# 注意：mod.subprocess 即全局 subprocess 模块——每个用例 setUp 打桩、tearDown 恢复
REAL_RUN = subprocess.run

H = "HiBurn.exe"
P = "python.exe"
# 进程表元组：(pid, parent_pid, parent_alive, cmdline, proc_name)——parent_pid 仅登记路径使用
PPID = 999999


class KillTestBase(unittest.TestCase):
    """公共：mock 进程表 + taskkill 记录器（不杀真实进程）。"""

    procs = []

    def setUp(self):
        self.killed = []
        mod._list_procs = lambda name: [p[:4] for p in self.procs if p[4] == name]
        mod._pid_create_time = lambda pid: None  # 默认查询失败 → 保守路径
        mod.time.sleep = lambda s: None

        def fake_run(cmd, **kw):
            if cmd and cmd[:2] == ["taskkill", "/F"]:
                self.killed.append(int(cmd[cmd.index("/PID") + 1]))
                return types.SimpleNamespace(returncode=0, stdout="", stderr="")
            return types.SimpleNamespace(returncode=0, stdout="", stderr="")

        mod.subprocess.run = fake_run

    def tearDown(self):
        mod.subprocess.run = REAL_RUN

    def assertKilled(self, expect):
        self.assertEqual(sorted(self.killed), sorted(expect),
                         "killed=%s expect=%s" % (self.killed, expect))


class TestKillExistingHiburn(KillTestBase):
    """kill_existing_hiburn：-com 精确解析 + 孤儿（父进程已死）判定。"""

    def test_com99_and_path_substring_no_kill(self):
        """复现A: -com:99 + 路径含 COM99（子串误杀源）→ 不杀。"""
        self.procs = [(424242, PPID, False, "%s -com:99 -bin:C:\\fw\\COM99.bin" % H, H)]
        mod.kill_existing_hiburn("COM9")
        self.assertKilled([])

    def test_com9_real_orphan_killed(self):
        """复现B: -com:9 真孤儿（本任务残留）→ 杀。"""
        self.procs = [(111, PPID, False, "%s -com:9 -bin:C:\\fw.bin" % H, H)]
        mod.kill_existing_hiburn("COM9")
        self.assertKilled([111])

    def test_same_port_active_task_no_kill(self):
        """同端口但父进程存活（活跃任务）→ 不杀。"""
        self.procs = [(222, PPID, True, "%s -com:9 -bin:C:\\fw.bin" % H, H)]
        mod.kill_existing_hiburn("COM9")
        self.assertKilled([])

    def test_gui_launch_no_com_skip(self):
        """GUI 启动无 -com 参数 → 不杀（归属不明）。"""
        self.procs = [(333, PPID, False, H, H)]
        mod.kill_existing_hiburn("COM9")
        self.assertKilled([])

    def test_none_com_skip_all(self):
        """com=None → 全跳过。"""
        self.procs = [(444, PPID, False, "%s -com:9" % H, H)]
        mod.kill_existing_hiburn(None)
        self.assertKilled([])

    def test_bin_path_com9_substring_no_attribution(self):
        """-bin 路径含 COM9 字样但端口不同（-com:12）→ 不杀。"""
        self.procs = [(555, PPID, False, "%s -com:12 -bin:C:\\COM9\\fw.bin" % H, H)]
        mod.kill_existing_hiburn("COM9")
        self.assertKilled([])


class TestKillOrphanBurnOne(KillTestBase):
    """kill_orphan_burn_one：端口号归一比较 + 孤儿判定。"""

    def test_com9_orphan_killed(self):
        self.procs = [(555, PPID, False, "%s C:\\x\\burn_one.py -com COM9 -baud 115200" % P, P)]
        mod.kill_orphan_burn_one("COM9")
        self.assertKilled([555])

    def test_equals_form_orphan_killed(self):
        """-com=COM9（= 形态）孤儿 → 杀。"""
        self.procs = [(666, PPID, False, "%s C:\\x\\burn_one.py -com=COM9" % P, P)]
        mod.kill_orphan_burn_one("COM9")
        self.assertKilled([666])

    def test_com99_different_port_no_kill(self):
        self.procs = [(777, PPID, False, "%s C:\\x\\burn_one.py -com COM99" % P, P)]
        mod.kill_orphan_burn_one("COM9")
        self.assertKilled([])

    def test_probe_no_com_skip(self):
        """--probe 无 -com → 不杀（归属不明）。"""
        self.procs = [(888, PPID, False, "%s C:\\x\\burn_one.py --probe" % P, P)]
        mod.kill_orphan_burn_one("COM9")
        self.assertKilled([])

    def test_lowercase_com9_active_no_kill(self):
        """-com com9 小写 + 父进程存活 → 不杀（活跃）。"""
        self.procs = [(999, PPID, True, "%s C:\\x\\burn_one.py -com com9" % P, P)]
        mod.kill_orphan_burn_one("COM9")
        self.assertKilled([])

    def test_lowercase_com9_orphan_killed(self):
        """-com com9 小写 + 孤儿 → 杀（端口号比较，与写法无关）。"""
        self.procs = [(1010, PPID, False, "%s C:\\x\\burn_one.py -com com9" % P, P)]
        mod.kill_orphan_burn_one("COM9")
        self.assertKilled([1010])

    def test_self_pid_excluded(self):
        self.procs = [(mod.os.getpid(), PPID, False, "%s C:\\x\\burn_one.py -com COM9" % P, P)]
        mod.kill_orphan_burn_one("COM9")
        self.assertKilled([])

    def test_non_burn_one_python_no_kill(self):
        self.procs = [(2020, PPID, False, "%s jupyter-notebook" % P, P)]
        mod.kill_orphan_burn_one("COM9")
        self.assertKilled([])


class TestPortParsing(unittest.TestCase):
    """-com 解析与端口归一单元。"""

    def test_hiburn_cmd_port(self):
        self.assertEqual(mod._hiburn_cmd_port("%s -com:9 -bin:C:\\fw.bin" % H), 9)
        self.assertEqual(mod._hiburn_cmd_port("%s -com:99 -bin:C:\\fw\\COM99.bin" % H), 99)
        self.assertEqual(mod._hiburn_cmd_port("%s -COM:17" % H), 17, "大写形态")
        self.assertIsNone(mod._hiburn_cmd_port(H), "GUI 无参数")
        self.assertIsNone(mod._hiburn_cmd_port("%s -bin:C:\\COM9\\fw.bin" % H),
                          "路径字样不算归属证据")

    def test_port_number(self):
        self.assertEqual(mod._port_number("COM9"), 9)
        self.assertEqual(mod._port_number("com9"), 9)
        self.assertEqual(mod._port_number("9"), 9)
        self.assertIsNone(mod._port_number(None))


class TestKillRegisteredHiburn(KillTestBase):
    """kill_registered_hiburn：登记孤儿清理（登记 PID + 进程名/端口 + owner 身份三重校验）。"""

    @classmethod
    def setUpClass(cls):
        cls.tmpdir = tempfile.mkdtemp(prefix="burn_one_kill_test_")
        cls._orig_dir = mod.RUN_STATE_DIR
        mod.RUN_STATE_DIR = cls.tmpdir

    @classmethod
    def tearDownClass(cls):
        mod.RUN_STATE_DIR = cls._orig_dir
        shutil.rmtree(cls.tmpdir, ignore_errors=True)

    def _write_registry(self, pids, owner_pid=12345, owner_start="2026-01-01T00:00:00.0000000+08:00"):
        with open(mod._run_state_path(9), "w", encoding="utf-8") as f:
            json.dump({"pids": pids, "owner_pid": owner_pid, "owner_start": owner_start}, f)

    def _registry_cleared(self):
        return not os.path.exists(mod._run_state_path(9))

    def test_owner_alive_identity_verified_occupies(self):
        """父进程存活 + 创建时间与登记一致（owner 本尊）→ 不杀、不清登记、返回 -1。"""
        self.procs = [(111, 12345, True, "%s -com:9 -bin:C:\\fw.bin" % H, H)]
        mod._pid_create_time = lambda pid: "2026-01-01T00:00:00.0000000+08:00"
        self._write_registry([111], owner_pid=12345)
        ret = mod.kill_registered_hiburn("COM9")
        self.assertKilled([])
        self.assertEqual(ret, -1)
        self.assertFalse(self._registry_cleared(), "活跃 owner 的登记不得清除")

    def test_owner_pid_reused_treated_as_orphan(self):
        """父 PID 存活但创建时间与登记不符（PID 被新进程复用）→ owner 实已死，按孤儿杀。"""
        self.procs = [(222, 12345, True, "%s -com:9 -bin:C:\\fw.bin" % H, H)]
        mod._pid_create_time = lambda pid: "2027-06-06T00:00:00.0000000+08:00"  # 复用后的新进程
        self._write_registry([222], owner_pid=12345)
        ret = mod.kill_registered_hiburn("COM9")
        self.assertKilled([222])
        self.assertEqual(ret, 1)
        self.assertTrue(self._registry_cleared())

    def test_owner_start_missing_conservative_occupies(self):
        """旧格式登记无 owner_start → 无法严格校验，保守视为存活 → -1。"""
        self.procs = [(333, 12345, True, "%s -com:9 -bin:C:\\fw.bin" % H, H)]
        self._write_registry([333], owner_pid=12345, owner_start=None)
        ret = mod.kill_registered_hiburn("COM9")
        self.assertKilled([])
        self.assertEqual(ret, -1)

    def test_create_time_query_fail_conservative(self):
        """父进程存活 + 创建时间查询失败 → 保守视为 owner 存活 → -1。"""
        self.procs = [(444, 12345, True, "%s -com:9 -bin:C:\\fw.bin" % H, H)]
        mod._pid_create_time = lambda pid: None
        self._write_registry([444], owner_pid=12345)
        ret = mod.kill_registered_hiburn("COM9")
        self.assertKilled([])
        self.assertEqual(ret, -1)

    def test_registered_via_record_child_pid_owner_alive_no_kill(self):
        """检视者原样复现：_record_child_pid 真实写入登记 + owner 存活 → 不杀。"""
        mod._pid_create_time = lambda pid: "T0"
        mod._record_child_pid("COM9", 900111)  # owner_pid=本测试进程，owner_start=T0
        self.procs = [(900111, mod.os.getpid(), True, "%s -com:9 -bin:C:\\fw.bin" % H, H)]
        ret = mod.kill_registered_hiburn("COM9")
        self.assertKilled([])
        self.assertEqual(ret, -1)
        self.assertFalse(self._registry_cleared())
        mod._clear_child_pids("COM9")

    def test_registered_orphan_killed(self):
        """登记 PID + owner 已退出（父进程死）+ 进程名/端口匹配 → 杀（真孤儿）。"""
        self.procs = [(555, 12345, False, "%s -com:9 -bin:C:\\fw.bin" % H, H)]
        self._write_registry([555], owner_pid=12345)
        ret = mod.kill_registered_hiburn("COM9")
        self.assertKilled([555])
        self.assertEqual(ret, 1)
        self.assertTrue(self._registry_cleared(), "孤儿处理后登记应清除")

    def test_registered_pid_reused_other_port_skip(self):
        """登记 PID 被复用为其他端口的 HiBurn（-com:12）→ 不杀。"""
        self.procs = [(666, PPID, False, "%s -com:12 -bin:C:\\fw.bin" % H, H)]
        self._write_registry([666])
        ret = mod.kill_registered_hiburn("COM9")
        self.assertKilled([])
        self.assertEqual(ret, 0)

    def test_registered_pid_reused_non_hiburn_skip(self):
        """登记 PID 被复用为非 HiBurn 进程（HiBurn 进程表中不存在）→ 不杀。"""
        self.procs = [(777, PPID, False, "%s C:\\x\\burn_one.py -com COM9" % P, P)]
        self._write_registry([777])
        mod.kill_registered_hiburn("COM9")
        self.assertKilled([])

    def test_registered_pid_exited_skip_and_clear(self):
        """登记 PID 已退出（进程表为空）→ 不杀、登记照常清除。"""
        self.procs = [(888, PPID, False, "%s -com:9" % H, H)]
        self._write_registry([999])
        mod.kill_registered_hiburn("COM9")
        self.assertKilled([])
        self.assertTrue(self._registry_cleared())


class TestRegistryIO(unittest.TestCase):
    """登记簿读写往返（record → registered → clear）。"""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="burn_one_regio_test_")
        self._orig_dir = mod.RUN_STATE_DIR
        mod.RUN_STATE_DIR = self.tmpdir
        self._orig_ct = mod._pid_create_time
        mod._pid_create_time = lambda pid: None

    def tearDown(self):
        mod.RUN_STATE_DIR = self._orig_dir
        mod._pid_create_time = self._orig_ct
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_record_read_clear_roundtrip(self):
        mod._record_child_pid("COM9", 5555)
        mod._record_child_pid("com9", 6666)
        reg = mod._read_registry("COM9")
        self.assertEqual(reg.get("pids"), [5555, 6666])
        self.assertEqual(reg.get("owner_pid"), mod.os.getpid())
        mod._clear_child_pids("COM9")
        self.assertEqual(mod._registered_pids("COM9"), [], "清除后读回为空")

    def test_no_registry_returns_empty(self):
        self.assertEqual(mod._registered_pids("COM10"), [], "无登记端口返回空")


class TestComLock(unittest.TestCase):
    """COM 端口排他锁（文件字节锁）：真互斥，含双进程同端口竞态。"""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="burn_one_lock_test_")
        self._orig_dir = mod.RUN_STATE_DIR
        mod.RUN_STATE_DIR = self.tmpdir

    def tearDown(self):
        mod.RUN_STATE_DIR = self._orig_dir
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_lock_acquire_release_roundtrip(self):
        """取锁 → 句柄有效；释放 → 可再取。"""
        fh = mod._acquire_burn_lock("COM9")
        self.assertIsNotNone(fh)
        self.assertIsNot(fh, False)
        mod.release_com_lock(fh)
        fh2 = mod._acquire_burn_lock("COM9")
        self.assertIsNotNone(fh2)
        self.assertIsNot(fh2, False)
        mod.release_com_lock(fh2)

    def test_lock_busy_returns_false(self):
        """本进程持锁期间，再次取锁（新句柄）→ False（占用）。"""
        fh = mod._acquire_burn_lock("COM9")
        self.assertIsNot(fh, False)
        try:
            second = mod._acquire_burn_lock("COM9")
            self.assertIs(second, False, "持锁期间二次获取应返回 False")
        finally:
            mod.release_com_lock(fh)

    def test_reset_and_burn_delegates_lock_to_caller(self):
        """锁已上移到 main 触板流程统一入口：reset_and_burn 自身不再取锁（直接委托），
        同进程持锁调用也正常委托（锁由入口层统一管理，避免自我死锁）。"""
        fh = mod._acquire_burn_lock("COM9")
        self.assertIsNot(fh, False)
        try:
            called = []
            orig_locked = mod._reset_and_burn_locked
            mod._reset_and_burn_locked = lambda *a, **k: called.append(True) or True
            try:
                ret = mod.reset_and_burn("COM9", 115200, "hiburn.exe", "fw.bin",
                                         1, 0, 3, "at", False)
                self.assertTrue(ret)
                self.assertEqual(called, [True], "持锁方调用应正常委托（锁由入口层管理）")
            finally:
                mod._reset_and_burn_locked = orig_locked
        finally:
            mod.release_com_lock(fh)

    def test_run_only_cli_aborts_when_lock_held_cross_entry(self):
        """跨入口竞争（R9 修复目标）：另一进程持锁（模拟烧录进行中）时，
        --run-only 的 CLI 入口（main 触板流程统一入口）应快速中止——
        非零退出 + [中止] 提示，且不进 run_only（不触串口、秒回）。"""
        mod.RUN_STATE_DIR = self._orig_dir  # 子进程无法继承 monkeypatch，用真实目录
        holder_code = (
            "import sys, time, types\n"
            "sys.path.insert(0, %r)\n"
            "try:\n"
            "    import serial\n"
            "except ImportError:\n"
            "    sys.modules['serial'] = types.ModuleType('serial')\n"
            "import burn_one\n"
            "fh = burn_one._acquire_burn_lock('COM7')\n"
            "print('LOCKED' if fh else 'FAILED', flush=True)\n"
            "time.sleep(60)\n" % HERE
        )
        cli_code = (
            "import sys, types\n"
            "sys.path.insert(0, %r)\n"
            "try:\n"
            "    import serial\n"
            "except ImportError:\n"
            "    sys.modules['serial'] = types.ModuleType('serial')\n"
            "import burn_one\n"
            "sys.argv = ['burn_one.py', '--run-only', '-com', 'COM7', '-baud', '115200']\n"
            "burn_one.main()\n" % HERE
        )
        holder = subprocess.Popen([sys.executable, "-c", holder_code],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            self.assertEqual(holder.stdout.readline().strip(), "LOCKED", "持锁子进程应就绪")
            cli = subprocess.Popen([sys.executable, "-c", cli_code],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            out, err = cli.communicate(timeout=15)
            self.assertNotEqual(cli.returncode, 0, "锁被持有时 CLI 必须非零退出")
            self.assertIn("[中止]", out + err, "应打印端口锁占用中止信息")
        finally:
            holder.kill()
            holder.wait()
            for pipe in (holder.stdout, holder.stderr):
                if pipe is not None:
                    pipe.close()  # 显式关闭管道，避免 ResourceWarning

    def test_probe_cli_aborts_when_lock_held_cross_entry(self):
        """跨入口竞争（R10 补测）：--probe 发 AT+RST 复位板子（非只读），
        与烧录同受端口锁保护——另一进程持锁时 --probe 的 CLI 入口必须拒绝。"""
        mod.RUN_STATE_DIR = self._orig_dir
        holder_code = (
            "import sys, time, types\n"
            "sys.path.insert(0, %r)\n"
            "try:\n"
            "    import serial\n"
            "except ImportError:\n"
            "    sys.modules['serial'] = types.ModuleType('serial')\n"
            "import burn_one\n"
            "fh = burn_one._acquire_burn_lock('COM7')\n"
            "print('LOCKED' if fh else 'FAILED', flush=True)\n"
            "time.sleep(60)\n" % HERE
        )
        cli_code = (
            "import sys, types\n"
            "sys.path.insert(0, %r)\n"
            "try:\n"
            "    import serial\n"
            "except ImportError:\n"
            "    sys.modules['serial'] = types.ModuleType('serial')\n"
            "import burn_one\n"
            "sys.argv = ['burn_one.py', '--probe', '-com', 'COM7', '-baud', '115200']\n"
            "burn_one.main()\n" % HERE
        )
        holder = subprocess.Popen([sys.executable, "-c", holder_code],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            self.assertEqual(holder.stdout.readline().strip(), "LOCKED", "持锁子进程应就绪")
            cli = subprocess.Popen([sys.executable, "-c", cli_code],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            out, err = cli.communicate(timeout=15)
            self.assertNotEqual(cli.returncode, 0, "锁被持有时 --probe 必须非零退出")
            self.assertIn("[中止]", out + err, "应打印端口锁占用中止信息")
        finally:
            holder.kill()
            holder.wait()
            for pipe in (holder.stdout, holder.stderr):
                if pipe is not None:
                    pipe.close()  # 显式关闭管道，避免 ResourceWarning

    def test_dual_process_same_port_exclusion(self):
        """双进程竞态（codex 提出的真并发场景）：子进程持锁 → 父进程取锁失败；
        子进程退出（锁由 OS 回收）→ 父进程可取。用真实 %TEMP% 锁目录保证两进程同路径。"""
        mod.RUN_STATE_DIR = self._orig_dir  # 子进程无法继承 monkeypatch，用真实目录
        child_code = (
            "import sys, time, types\n"
            "sys.path.insert(0, %r)\n"
            "try:\n"
            "    import serial\n"
            "except ImportError:\n"
            "    sys.modules['serial'] = types.ModuleType('serial')\n"
            "import burn_one\n"
            "fh = burn_one._acquire_burn_lock('COM7')\n"
            "print('LOCKED' if fh else 'FAILED', flush=True)\n"
            "time.sleep(60)\n" % HERE
        )
        child = subprocess.Popen([sys.executable, "-c", child_code],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            line = child.stdout.readline().strip()
            self.assertEqual(line, "LOCKED", "子进程应成功持锁")
            # 子进程持锁期间，本进程取同端口锁 → False
            second = mod._acquire_burn_lock("COM7")
            self.assertIs(second, False, "并发进程持锁期间取锁应失败")
        finally:
            child.kill()
            child.wait()
            for pipe in (child.stdout, child.stderr):
                if pipe is not None:
                    pipe.close()  # 显式关闭管道，避免 ResourceWarning
        # 子进程死亡 → OS 回收锁 → 本进程可取
        third = mod._acquire_burn_lock("COM7")
        self.assertIsNot(third, False)
        self.assertIsNotNone(third)
        mod.release_com_lock(third)


if __name__ == "__main__":
    unittest.main(verbosity=2)
