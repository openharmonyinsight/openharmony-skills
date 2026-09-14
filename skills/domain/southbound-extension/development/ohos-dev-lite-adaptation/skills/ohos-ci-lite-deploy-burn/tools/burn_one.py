#!/usr/bin/env python3
# coding=utf-8
"""
burn_one.py —— 烧录单个 Hi3861 XTS 测试 bin 并自动 reset 执行 + 抓 XTS 统计 PASS/FAIL。

复刻 xdevice _run_ctest 的流程（ohos/testkit/kit_lite.py DeployKit 等）+ 借鉴
burn_3861_auto.py / ohos_lite_pipeline.py 的健壮性（WAKE_MAGIC 唤醒 + AT 探测降级）：
  A) 让芯片进入下载模式并 HiBurn 烧录 bin
  B) 发魔法字节复位运行新固件，回读 XTS 输出，统计 PASSED/FAILED

进入下载模式有三种方式（--reset-mode）：
  at   : 发 AT+RST 软复位。仅当当前固件在 UART0 跑 hi3861 AT 框架时有效
         （acts 测试 bin 通常可以；OHOS_Image.bin 跑 OHOS shell 时无效）。
  dtr  : 拉扯 DTR/RTS 控制线做硬复位。仅当板子把 CH340 的 DTR/RTS 接到
         RESET/BOOT 时有效（HiSpark Pegasus 默认可能没接，需实测）。
  none : 不自动复位，HiBurn 提示时手动按一次 RESET（--skip-at-rst 等价）。

AT 健壮性（学 burn_3861_auto.py / ohos_lite_pipeline.py._capture_xts）：
  - AT 静默（发 AT 无 OK 应答）时自动发 WAKE_MAGIC（DEADBEEF 魔法字）唤醒 AT app，
    再探一次；唤醒成功才发 AT+RST，保证可反复烧录/重跑。
  - 唤醒仍失败则降级：仅监听串口 + 提示用户手按 RST 跑 XTS，避免 AT 不可用时
    AT+RST 发不出、静默超时白等。

XTS 统计（学 ohos_lite_pipeline.py._capture_xts）：
  - run_and_read / run_only / boot_and_confirm 在抓输出时累计 PASSED/FAILED 计数，
    退出时打印 "X Tests Y Failures Z Ignored" 风格的统计行（PASSED=n FAILED=m）。

依赖：pyserial  (pip install pyserial)
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time

try:
    import msvcrt  # Windows 文件字节锁（COM 端口互斥）；非 Windows 降级为无锁
except ImportError:
    msvcrt = None

try:
    import serial
except ImportError:
    sys.exit("缺少 pyserial，请先执行: pip install pyserial")

# 复位魔字节（DEADBEEF）：烧后启动新固件 / 唤醒 AT。两个用途同序列：
#   1. 烧后发它启动新固件（芯片还在 loader 态，魔字节触发复位进 app）。
#   2. AT 静默时发它唤醒 AT app（不进下载模式，仅唤醒），使 AT+RST 能发出。
# 与 burn_3861_auto.py 的 WAKE_MAGIC / ohos_lite_pipeline.py 的 RESET_CMD 同序列。
RESET_CMD = bytes([0xEF, 0xBE, 0xAD, 0xDE, 0x0C, 0x00,
                   0x87, 0x78, 0x00, 0x00, 0x61, 0x94])
WAKE_MAGIC = RESET_CMD  # AT 唤醒魔字节——与复位魔字节同序列
CTEST_END_SIGN = "All the test suites finished"
ANSI_PATTERN = re.compile(r'\x1B(\[([0-9]{1,2}(;[0-9]{1,2})*)?m)*')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_HIBURN = os.path.join(SCRIPT_DIR, "HiBurn.exe")

# Windows 上 serial.close() 返回后，COM 句柄并不一定立刻释放给下一个进程。
# HiBurn.exe 紧接着去开同一个 COM 口就会间歇性失败（"有时灵有时不灵"的主因）。
# 复位函数关端口后等这么久，再让 HiBurn 去开。
PORT_RELEASE_WAIT = 0.3


def com_number(com_port):
    m = re.search(r'\d+$', com_port)
    if not m:
        sys.exit("无法从串口名 %r 解析出数字，请用 COM3 这种形式" % com_port)
    return m.group(0)


def at_probe(ser, wait=0.8):
    """探 AT 框架是否在线（发 AT 期望 OK）。ser 须已打开。返回 bool。

    学 burn_3861_auto.py.at_probe / ohos_lite_pipeline.py._at_probe：
    发 AT 后监听 wait 秒看回显里有没有 OK。"""
    try:
        ser.flushInput()
        ser.write(b"AT\r\n"); ser.flush()
        t0 = time.time(); buf = bytearray()
        while time.time() - t0 < wait:
            n = ser.in_waiting
            if n:
                buf += ser.read(n)
            else:
                time.sleep(0.03)
        return b"OK" in buf
    except Exception:
        return False


def wake_at(com, baud):
    """发 WAKE_MAGIC 唤醒 AT app。两个场景（学 burn_3861_auto.py.wake_at）：
    - 烧前/运行前：AT 静默时唤醒，使 AT+RST 能发出。
    - 烧后：芯片重启 AT 可能静默，唤醒后保证下一轮可重复烧录/重跑。
    返回唤醒后 AT 是否在线。"""
    print("  [wake] AT 静默，发 WAKE_MAGIC 唤醒...")
    try:
        s = serial.Serial(com, baudrate=baud, timeout=0.3)
    except Exception:
        return False
    try:
        s.flushInput()
        s.write(WAKE_MAGIC); s.flush()
    finally:
        s.close()
        time.sleep(PORT_RELEASE_WAIT)
    time.sleep(2.0)  # 给 app/AT 恢复时间
    # 唤醒后再探一次确认
    try:
        s = serial.Serial(com, baudrate=baud, timeout=0.5)
    except Exception:
        return False
    try:
        return at_probe(s)
    finally:
        s.close()
        time.sleep(PORT_RELEASE_WAIT)


def ensure_at_online(com, baud):
    """确保 AT 框架在线：探一下，静默则 WAKE_MAGIC 唤醒，仍静默返回 False。

    学 ohos_lite_pipeline.py._capture_xts 的 at_rst 触发前探测逻辑：
    AT 在线才发 AT+RST，避免 AT 不可用时 AT+RST 发不出、静默超时白等。
    """
    try:
        s = serial.Serial(com, baudrate=baud, timeout=0.5)
    except Exception:
        return False
    try:
        if at_probe(s):
            return True
    finally:
        s.close()
        time.sleep(PORT_RELEASE_WAIT)
    # 静默 → 唤醒
    return wake_at(com, baud)


def send_at_rst(com, baud, rst_wait):
    """发 AT+RST 让芯片软复位（hi3861 at_general.c: at_setup_reset_cmd）。

    增强（学 burn_3861_auto.py）：发前先 ensure_at_online，AT 静默则 WAKE_MAGIC
    唤醒，唤醒失败返回 False（让上层降级为手动）。"""
    if not ensure_at_online(com, baud):
        print("      [warn] AT 唤醒失败，AT+RST 可能发不出（降级为手动/仅监听）")
        return False
    try:
        ser = serial.Serial(com, baudrate=baud, timeout=1)
    except Exception as e:
        print("      打开 %s 失败: %s" % (com, e)); return False
    try:
        ser.write("AT+RST={}\r\n".format(rst_wait).encode("utf-8"))
    finally:
        ser.close()
        time.sleep(PORT_RELEASE_WAIT)  # 等 Windows 释放 COM 句柄，再让 HiBurn 去开
    return True


def dtr_reset(com, baud):
    """用 DTR/RTS 控制线尝试硬复位进下载模式（板子需有自动复位电路才有效）。

    采用 ESP 风格时序：RTS 接 EN/RESET，DTR 接 BOOT/LINK。
    不同板子接线不同，无效就说明板子没接，需手按 RESET。
    """
    try:
        ser = serial.Serial(com, baudrate=baud, timeout=1)
    except Exception as e:
        print("      打开 %s 失败: %s" % (com, e)); return False
    try:
        ser.dtr = False
        ser.rts = False
        time.sleep(0.05)
        ser.dtr = True    # 拉低 BOOT/LINK -> 下载模式
        ser.rts = True    # 拉低 RESET
        time.sleep(0.1)   # 保持复位
        ser.rts = False   # 释放 RESET，芯片以 BOOT 低启动
        time.sleep(0.05)
    finally:
        ser.close()
        time.sleep(PORT_RELEASE_WAIT)  # 等 Windows 释放 COM 句柄，再让 HiBurn 去开
    return True


def trigger_reset(com, baud, rst_wait, reset_mode):
    if reset_mode == "at":
        return send_at_rst(com, baud, rst_wait)
    if reset_mode == "dtr":
        return dtr_reset(com, baud)
    return True  # none


def _port_number(com_port):
    """'COM9'/'com9'/'9' → 9；解析不出返回 None（进程归属判定用，不退出）。"""
    if not com_port:
        return None
    m = re.search(r'(\d+)\s*$', str(com_port).strip())
    return int(m.group(1)) if m else None


def _hiburn_cmd_port(cmd):
    """从 HiBurn 命令行精确解析 -com:<数字> 参数（HiBurn 接受的是数字端口）。

    只认独立参数形态（-com:9 / -com=9 / -com 9），不做全文子串匹配：
    `-bin:C:\\COM9\\fw.bin` 这类路径含 COM 字样不构成归属证据，
    `-com:99` 与本任务 COM9 端口号不同也不杀。
    """
    m = re.search(r'(?:^|\s)-com[:= ]\s*(\d+)', cmd, re.IGNORECASE)
    return int(m.group(1)) if m else None


def _list_procs(name):
    """列出指定名进程：[(pid, 父PID, 父进程是否存活, 命令行)]。

    父进程存活标记用于区分孤儿/活跃任务：上次运行被打断留下的孤儿，
    其父进程（发起它的 python/终端）已退出；父进程仍存活的进程属于
    某个进行中的任务，不允许杀。
    """
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-CimInstance Win32_Process -Filter \"name='%s'\" | "
             "ForEach-Object { $pp = Get-Process -Id $_.ParentProcessId -ErrorAction SilentlyContinue; "
             "('{0}|{1}|{2}|{3}' -f $_.ProcessId, $_.ParentProcessId, [int]($null -ne $pp), $_.CommandLine) }" % name],
            capture_output=True, text=True, timeout=10)
    except Exception:
        return []
    procs = []
    for line in out.stdout.splitlines():
        parts = line.strip().split("|", 3)
        if len(parts) != 4:
            continue
        try:
            procs.append((int(parts[0]), int(parts[1]), parts[2] == "1", parts[3]))
        except ValueError:
            continue
    return procs


def _pid_create_time(pid):
    """取指定 PID 的进程创建时间（Win32_Process CreationDate，ISO 字符串）。

    用于 PID 复用防护：登记时的 owner 创建时间与当前同号 PID 的创建时间比对，
    不一致 = PID 已被新进程复用。查询失败返回 None（调用方按保守方向处理）。
    """
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "(Get-CimInstance Win32_Process -Filter \"ProcessId=%d\").CreationDate.ToString('o')" % pid],
            capture_output=True, text=True, timeout=10)
        s = out.stdout.strip()
        return s or None
    except Exception:
        return None


RUN_STATE_DIR = os.path.join(tempfile.gettempdir(), "burn_one_runs")


def _run_state_path(port):
    return os.path.join(RUN_STATE_DIR, "com%d.json" % port)


def _record_child_pid(com, pid):
    """登记本任务刚 spawn 的 HiBurn 子进程 PID（按端口）。

    正常等子进程退出后由 _clear_child_pids 清除；登记文件残留 = 上次运行被打断，
    是下次清理"本任务孤儿"的最硬凭据。登记失败（权限/磁盘）不影响烧录主流程。
    """
    port = _port_number(com)
    if port is None:
        return
    try:
        os.makedirs(RUN_STATE_DIR, exist_ok=True)
        p = _run_state_path(port)
        data = {"pids": []}
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                data = json.load(f)
        data["owner_pid"] = os.getpid()  # 登记发起方（本 burn_one 进程）
        data["owner_start"] = _pid_create_time(os.getpid())  # owner 创建时间（PID 复用防护）
        data.setdefault("pids", []).append(pid)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except (OSError, ValueError):
        pass


def _clear_child_pids(com):
    """正常退出时清除本端口的子进程登记（文件残留由下次运行当作孤儿凭据）。"""
    port = _port_number(com)
    if port is None:
        return
    try:
        p = _run_state_path(port)
        if os.path.exists(p):
            os.remove(p)
    except OSError:
        pass


def _read_registry(com):
    """读回本端口登记簿（dict：pids / owner_pid；无登记/文件损坏返回空 dict）。"""
    port = _port_number(com)
    if port is None:
        return {}
    try:
        p = _run_state_path(port)
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                return json.load(f)
    except (OSError, ValueError):
        pass
    return {}


def _registered_pids(com):
    """读回本端口登记在册的子进程 PID（无登记/文件损坏返回空表）。"""
    return _read_registry(com).get("pids", [])


def _owner_genuinely_alive(reg, parent_pid):
    """存活的父进程是否为登记 owner 本尊（PID 复用防护）。

    父 PID 存活 ≠ owner 存活——PID 可能被新进程复用。用登记时的 owner 创建时间
    与当前 PID 创建时间比对：一致才是本尊。登记信息不全 / 父 PID 与登记不符 /
    查询失败时保守视为存活（宁可漏清不可误杀）。
    """
    owner_pid = reg.get("owner_pid")
    owner_start = reg.get("owner_start")
    if not owner_start or parent_pid != owner_pid:
        return True  # 无法严格校验：保守视为 owner 存活
    cur = _pid_create_time(parent_pid)
    if cur is None:
        return True  # 查询失败：保守视为存活
    return cur == owner_start


def kill_registered_hiburn(com=None):
    """清理本任务上次运行登记在册的 HiBurn 孤儿（登记 PID 是最硬归属凭据）。

    登记文件在 spawn HiBurn 时写入、正常退出时清除，残留即上次被打断。
    登记只证明"某个 burn_one 在本端口 spawn 过它"，不证明 owner 已退出——
    正常烧录期间登记文件同样存在。杀之前确认：① 进程名是 HiBurn.exe 且
    -com 端口匹配（PID 复用防护）；② 其父进程（登记 owner）已退出。
    owner 存活 = 同端口活跃烧录 → 返回 -1（端口占用），不杀不清，由调用方中止。
    """
    port = _port_number(com)
    if port is None:
        return 0
    reg = _read_registry(com)
    pids = reg.get("pids", [])
    if not pids:
        return 0
    live = {pid: (ppid, alive, cmd) for pid, ppid, alive, cmd in _list_procs("HiBurn.exe")}
    killed = 0
    for pid in pids:
        if pid not in live:
            continue  # 已退出，或 PID 被无关进程复用（进程名不再是 HiBurn.exe）
        parent_pid, parent_alive, cmd = live[pid]
        if parent_alive:
            if _owner_genuinely_alive(reg, parent_pid):
                # 登记在册且 owner 本尊仍在运行：同端口有活跃烧录 → 不杀、不清登记
                # （owner 正常退出时自行清除），返回 -1 交调用方处理（端口锁之下的第二道）
                print("[互斥] 登记PID=%d 的 owner（burn_one，PID=%s）仍在运行，"
                      "端口 %d 有活跃烧录，不清理" % (pid, reg.get("owner_pid", "?"), port))
                return -1
            print("[清理] 登记PID=%d 的父 PID=%d 存活但创建时间与登记不符（PID 复用），"
                  "owner 实已退出，按孤儿处理" % (pid, parent_pid))
        if _hiburn_cmd_port(cmd) != port:
            print("[清理] 登记PID=%d 现为其他端口的 HiBurn（PID 复用），跳过" % pid)
            continue
        subprocess.run(["taskkill", "/F", "/PID", str(pid)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[清理] 杀掉本任务登记在册的 HiBurn 孤儿 PID=%d（-com:%d，owner 已退出）" % (pid, port))
        killed += 1
    _clear_child_pids(com)  # 无活跃 owner，登记处理完毕
    if killed:
        time.sleep(0.5)  # 等 Windows 释放句柄
    return killed


def kill_existing_hiburn(com=None):
    """烧录前清掉残留的 HiBurn.exe（仅限端口归属明确**且为孤儿**的进程）。

    上一次烧录被 Ctrl+C 打断时，Popen 起并登记过 PID 的 HiBurn.exe 不一定跟着退出，
    会变成孤儿继续占着 COM 口。下一次新 HiBurn 打不开口、收不到 connect flag。

    安全策略（不做全局杀，也不做全文子串匹配）：
    - 端口归属：从命令行精确解析 -com:<数字>，与本任务端口号相等才算归属本任务；
      解析不出（GUI 启动无参数等）一律跳过并报告
    - 孤儿判定：父进程仍存活的 HiBurn 属于某个活跃烧录任务（哪怕同端口），
      不杀、报告端口被活跃任务占用；只有父进程已死且端口归属明确才杀
    """
    my_port = _port_number(com)
    if my_port is None:
        print("[清理] 未指定/无法解析 COM 口（%r），跳过 HiBurn 清理（避免误杀其他板子的）" % (com,))
        return False
    killed = 0
    for pid, parent_pid, parent_alive, cmd in _list_procs("HiBurn.exe"):
        port = _hiburn_cmd_port(cmd)
        if port is None:
            print("[清理] HiBurn PID=%d 命令行无 -com:<数字> 参数，跳过（无法确认端口归属）" % pid)
            continue
        if port != my_port:
            print("[清理] HiBurn PID=%d 端口 -com:%d ≠ 本任务 %d，跳过（可能是其他板子的）"
                  % (pid, port, my_port))
            continue
        if parent_alive:
            print("[清理] HiBurn PID=%d（-com:%d）父进程存活，是活跃任务占口，不杀——"
                  "请确认是否有另一烧录正在进行" % (pid, my_port))
            continue
        subprocess.run(["taskkill", "/F", "/PID", str(pid)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[清理] 杀掉孤儿 HiBurn.exe PID=%d（-com:%d）" % (pid, my_port))
        killed += 1
    if killed:
        time.sleep(0.5)  # 等 Windows 释放句柄
        return True
    return False


def kill_orphan_burn_one(com=None):
    """杀掉残留的 burn_one.py python 进程（不含自己；仅限同端口**且为孤儿**）。

    上一次烧录被 Ctrl+C 打断时，python 可能卡在 hiburn_proc.wait() 等 HiBurn 退出，
    或卡在串口回读阶段，变成孤儿继续占着 COM 口、阻塞新一次烧录。

    - 端口归属：解析命令行 -com 参数值，按端口号比较（COM9/com9/9 视为同一端口）；
      无 -com 参数（--probe 等模式）无法确认归属，保守跳过
    - 孤儿判定：父进程已死（上次运行被打断留下的）才杀；父进程存活的同端口
      进程是活跃任务，报告占用但不杀
    """
    self_pid = os.getpid()
    my_port = _port_number(com)
    if my_port is None:
        print("[清理] 未指定/无法解析 COM 口（%r），跳过 burn_one.py 清理" % (com,))
        return 0
    killed = 0
    for pid, parent_pid, parent_alive, cmd in _list_procs("python.exe"):
        if "burn_one.py" not in cmd or pid == self_pid:
            continue
        m = re.search(r'(?:^|\s)-com[=: ](\S+)', cmd)
        if not m:
            print("[清理] burn_one.py PID=%d 命令行无 -com 参数，跳过（无法确认端口归属）" % pid)
            continue
        if _port_number(m.group(1)) != my_port:
            continue  # 不同端口的烧录任务，跳过
        if parent_alive:
            print("[清理] burn_one.py PID=%d（端口 %d）父进程存活，是活跃任务，不杀——"
                  "请确认是否有另一烧录正在进行" % (pid, my_port))
            continue
        subprocess.run(["taskkill", "/F", "/PID", str(pid)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[清理] 杀掉孤儿 burn_one.py 进程 PID=%d（端口 %d）" % (pid, my_port))
        killed += 1
    if killed:
        time.sleep(0.5)  # 等句柄释放
    return killed


def com_free(com, baud):
    """探测 COM 口当前是否可打开（没被占用）。"""
    try:
        s = serial.Serial(com, baudrate=baud, timeout=1)
        s.close()
        return True
    except Exception:
        return False


def _acquire_burn_lock(com):
    """获取本 COM 端口的排他锁（文件字节锁，真互斥——非登记/事后检查）。

    返回：文件句柄 = 持锁成功（调用方持句柄直到烧录周期结束，close 即释放；
    进程正常退出或崩溃死亡时 OS 自动回收锁，无残留锁问题）；
    False = 端口锁被其他任务持有（并发烧录），已打印中止信息；
    None = 锁不可用（非 Windows / 端口无法解析），降级无锁运行，
    由登记 owner 检查 + 串口占用检查兜底。
    """
    port = _port_number(com)
    if port is None or msvcrt is None:
        return None
    fh = None
    try:
        os.makedirs(RUN_STATE_DIR, exist_ok=True)
        fh = open(os.path.join(RUN_STATE_DIR, "com%d.lock" % port), "a+")
        fh.seek(0)
        msvcrt.locking(fh.fileno(), msvcrt.LK_NBLCK, 1)
        fh.seek(0)
        fh.truncate()
        fh.write("%d\n" % os.getpid())
        fh.flush()
        return fh
    except OSError:
        if fh is not None:
            try:
                fh.close()
            except OSError:
                pass
        print("[中止] %s 的端口锁被另一任务持有（烧录/测试共用端口锁，并发操作互斥；端口冲突非固件/串口故障），本次退出" % com)
        return False


def release_com_lock(lock_fh):
    """释放端口锁（关闭句柄即解锁）。"""
    try:
        lock_fh.close()
    except OSError:
        pass


def reset_and_burn(com, baud, hiburn, bin_file, rst_wait, pre_wait, retries,
                   reset_mode, skip_reset):
    """烧录（清场 + 重试循环）。

    COM 端口锁由 main 的触板流程统一入口持有（覆盖烧录与测试全周期，含
    run-only 跨入口互斥）；独立调用本函数的并发场景需自行持锁。
    """
    return _reset_and_burn_locked(com, baud, hiburn, bin_file, rst_wait,
                                  pre_wait, retries, reset_mode, skip_reset)  # 正常/异常退出都释放


def _reset_and_burn_locked(com, baud, hiburn, bin_file, rst_wait, pre_wait, retries,
                           reset_mode, skip_reset):
    hiburn_cmd = [hiburn, "-com:{}".format(com_number(com)),
                  "-bin:{}".format(bin_file), "-signalbaud:{}".format(baud)]
    do_reset = not skip_reset and reset_mode != "none"

    # 进循环前清场（入口端口锁是第一道互斥；以下为第二道——锁降级兜底 + 跨重启孤儿判定）：
    # ① 本任务登记在册的 HiBurn 孤儿（登记凭据最硬，先清）；
    #    登记 owner 本尊仍存活 = 同端口有活跃烧录 → 中止本次烧录
    # ② 残留 burn_one.py python（限同端口且为孤儿）；③ COM 仍被占才按端口清 HiBurn
    if kill_registered_hiburn(com) < 0:
        print("[中止] %s 正被另一活跃烧录任务占用（登记 owner 仍在运行），本次烧录退出" % com)
        return False
    kill_orphan_burn_one(com)
    if not com_free(com, baud):
        kill_existing_hiburn(com)  # 仅 COM 被占时才杀 HiBurn（按 PID + COM 验证）
        if not com_free(com, baud):
            print("[警告] %s 仍被占用，HiBurn 可能连不上（继续尝试）" % com)

    attempts = retries  # skip_reset 也重试，给用户多个按 RESET 的窗口
    for attempt in range(1, attempts + 1):
        if not com_free(com, baud):
            kill_existing_hiburn(com)  # 仅 COM 被占时清残留 HiBurn（按 PID + COM 验证）
        if do_reset:
            print("[烧录] 第 %d/%d 次：%s 复位（mode=%s）" %
                  (attempt, attempts, com, reset_mode))
            if not trigger_reset(com, baud, rst_wait, reset_mode):
                if attempt < attempts:
                    time.sleep(1); continue
                return False
            if pre_wait > 0:
                time.sleep(pre_wait)
        else:
            print("[烧录] 第 %d/%d 次：HiBurn 已监听，请按 RESET（或按住 LINK 再按 RESET）..." %
                  (attempt, attempts))

        print("      $ " + " ".join(hiburn_cmd))
        # 记住本次 spawn 的 HiBurn PID：正常退出即清除登记；被打断则登记残留，
        # 下次运行凭登记 + 进程名/端口双重校验精确清理本任务孤儿
        hiburn_proc = subprocess.Popen(hiburn_cmd)
        _record_child_pid(com, hiburn_proc.pid)
        rc = hiburn_proc.wait()  # Ctrl+C 等打断时登记保留（不走到下一行的清除）
        _clear_child_pids(com)
        if rc == 0:
            print("[烧录] HiBurn 烧录成功")
            # 烧后发 WAKE_MAGIC 唤醒 AT（学 burn_3861_auto.py.one_attempt 的烧后唤醒）：
            # HiBurn 烧完芯片重启，AT 可能静默（bootrom/download 态退出），
            # WAKE_MAGIC 唤醒 AT app，保证下一轮 AT+RST 能发出、可反复烧录/重跑。
            # at 模式才发（dtr/none 模式用户按键控制，不强加唤醒）。
            if reset_mode == "at":
                wake_at(com, baud)
            return True
        if skip_reset:
            if attempt < attempts:
                print("[烧录] HiBurn 返回 %d（未检测到复位），重启 HiBurn 再等一次..." % rc)
                time.sleep(1)
                continue
            print("[烧录] 已尝试 %d 次均未检测到手动复位" % attempts)
            return False
        if attempt < attempts:
            print("[烧录] HiBurn 返回 %d，1 秒后重试..." % rc)
            time.sleep(1)
        else:
            print("[烧录] 已尝试 %d 次仍失败" % attempts)
    return False


def _parse_xts_stats(text):
    """从一段输出文本里统计 PASSED/FAILED（学 ohos_lite_pipeline.py._capture_xts）。

    XTS/ACTS 输出里 PASSED/FAILED 两个标记各出现次数即为通过/失败用例数。
    返回 (passed, failed)。"""
    return text.count("PASSED"), text.count("FAILED")


def _print_stats(passed, failed):
    """打印 PASS/FAIL 统计行（学 ohos_lite_pipeline.py 的统计输出）。"""
    total = passed + failed
    if total > 0:
        rate = passed / total * 100.0
        print("[统计] %d Tests, %d Failures, 通过率 %.1f%%" % (total, failed, rate))
    else:
        print("[统计] 未捕获到 PASSED/FAILED 标记（可能非 XTS 输出或测试未跑）")


def run_only(com, baud, rst_wait, timeout, log_file):
    """镜像已烧好时：发 AT+RST 软复位 -> 芯片重启自动重跑 XTS -> 回读输出 + 统计。

    增强（学 ohos_lite_pipeline.py._capture_xts）：
    - 发 AT+RST 前先 ensure_at_online（AT 静默则 WAKE_MAGIC 唤醒），
      唤醒失败降级为仅监听 + 提示手按 RST。
    - 回读时累计 PASSED/FAILED，退出打印统计。
    """
    print("[运行] %s 发送 AT+RST=%d 软复位，回读 XTS 输出（超时 %ds）" %
          (com, rst_wait, timeout))
    # AT 探测 + 唤醒降级（学 _capture_xts 的 at_rst 触发前探测）
    if not ensure_at_online(com, baud):
        print("[运行] [warn] AT 唤醒失败，降级为仅监听——若无输出请手按板子 RST 跑 XTS")
        return _monitor_only(com, baud, timeout, log_file)
    ser = open_serial_retry(com, baud)
    log = open(log_file, "w", encoding="utf-8") if log_file else None
    start = time.time()
    finished = False
    passed = failed = 0
    try:
        ser.write("AT+RST={}\r\n".format(rst_wait).encode("utf-8"))
        while time.time() - start < timeout:
            line = ser.readline()
            if not line:
                continue
            text = ANSI_PATTERN.sub('', line.decode("gbk", errors="ignore"))
            sys.stdout.write(text); sys.stdout.flush()
            if log:
                log.write(text); log.flush()
            p, f = _parse_xts_stats(text)
            passed += p; failed += f
            if CTEST_END_SIGN in text:
                finished = True; break
    finally:
        ser.close()
        if log:
            log.close()
    _print_stats(passed, failed)
    print("\n[完成] %s，耗时 %.1fs" % (
        "收到结束标志" if finished else "读超时退出（输出已全部捕获）",
        time.time() - start))
    return (finished, passed, failed)


def _monitor_only(com, baud, timeout, log_file):
    """AT 不可用时的降级监听：不触发复位，仅持续读 COM 抓 XTS 输出 + 统计。

    学 ohos_lite_pipeline.py._capture_xts 的 trigger='none' 分支：
    用户手按板子 RST 跑 XTS，监听已在抓不会遗漏。"""
    print("[监听] %s 持续抓 XTS 输出（超时 %ds），请手按板子 RST 跑 XTS" % (com, timeout))
    ser = open_serial_retry(com, baud)
    log = open(log_file, "w", encoding="utf-8") if log_file else None
    start = time.time()
    finished = False
    passed = failed = 0
    try:
        while time.time() - start < timeout:
            line = ser.readline()
            if not line:
                continue
            text = ANSI_PATTERN.sub('', line.decode("gbk", errors="ignore"))
            sys.stdout.write(text); sys.stdout.flush()
            if log:
                log.write(text); log.flush()
            p, f = _parse_xts_stats(text)
            passed += p; failed += f
            if CTEST_END_SIGN in text:
                finished = True; break
    finally:
        ser.close()
        if log:
            log.close()
    _print_stats(passed, failed)
    print("\n[完成] %s，耗时 %.1fs" % (
        "收到结束标志" if finished else "读超时退出（输出已全部捕获）",
        time.time() - start))
    return (finished, passed, failed)


def open_serial_retry(com, baud, timeout=2, attempts=4):
    """打开 COM 口，失败则短间隔重试——规避上一进程（HiBurn）刚退出、
    Windows 尚未释放句柄的窗口。"""
    last = None
    for i in range(attempts):
        try:
            return serial.Serial(com, baudrate=baud, timeout=timeout)
        except Exception as e:
            last = e
            time.sleep(0.3)
    sys.exit("打开 %s 失败（重试 %d 次）: %s" % (com, attempts, last))


def run_and_read(com, baud, timeout, log_file):
    """烧后发复位魔字节启动新固件 + 回读 XTS 输出 + 统计 PASSED/FAILED。

    增强（学 ohos_lite_pipeline.py._capture_xts 的 magic 触发 + 统计）：
    回读时累计 PASSED/FAILED，退出打印统计行。"""
    print("[运行] %s 发送复位魔法字节，回读输出（超时 %ds）" % (com, timeout))
    ser = open_serial_retry(com, baud)
    log = open(log_file, "w", encoding="utf-8") if log_file else None
    start = time.time()
    finished = False
    passed = failed = 0
    try:
        ser.write(RESET_CMD)
        while time.time() - start < timeout:
            line = ser.readline()
            if not line:
                continue
            text = ANSI_PATTERN.sub('', line.decode("gbk", errors="ignore"))
            sys.stdout.write(text); sys.stdout.flush()
            if log:
                log.write(text); log.flush()
            p, f = _parse_xts_stats(text)
            passed += p; failed += f
            if CTEST_END_SIGN in text:
                finished = True; break
    finally:
        ser.close()
        if log:
            log.close()
    _print_stats(passed, failed)
    print("\n[完成] %s，耗时 %.1fs" % (
        "收到结束标志" if finished else "读超时退出（输出已全部捕获）",
        time.time() - start))
    return (finished, passed, failed)


def boot_and_confirm(com, baud, peek_secs=5, log_file=None):
    """--burn-only 用：烧完后发 RESET_CMD 魔字节启动新固件，短读 peek_secs 秒确认能启动。

    reset_and_burn 成功后芯片仍停在 loader，不会自动跑新固件——启动靠这里发魔字节。
    只做"启动 + 短确认"（看到 boot banner 即说明没变砖、AT 框架即将就绪），
    不进入 XTS 回读循环，不阻塞。XTS 会在芯片上自行跑起来，但不捕获；
    后续用 --run-only（AT+RST 软复位）单独重跑并捕获。
    """
    print("[启动] %s 发送复位魔字节，短确认 %ds（不捕获 XTS）" % (com, peek_secs))
    ser = open_serial_retry(com, baud)
    log = open(log_file, "w", encoding="utf-8") if log_file else None
    start = time.time()
    booted = False
    passed = failed = 0
    try:
        ser.write(RESET_CMD)
        while time.time() - start < peek_secs:
            line = ser.readline()
            if not line:
                continue
            text = ANSI_PATTERN.sub('', line.decode("gbk", errors="ignore"))
            sys.stdout.write(text); sys.stdout.flush()
            if log:
                log.write(text); log.flush()
            # 短确认期间也累计 PASSED/FAILED（个别快速用例可能在 peek 窗口内出结果）
            p, f = _parse_xts_stats(text)
            passed += p; failed += f
            # 任一已知 boot banner 即视为启动成功
            if any(m in text for m in ("ready to OS start", "FileSystem mount ok",
                                       "wifi init success", "OHOS")):
                booted = True
    finally:
        ser.close()
        if log:
            log.close()
    if passed + failed > 0:
        _print_stats(passed, failed)
    print("\n[启动] %s，耗时 %.1fs" % (
        "已确认新固件启动" if booted else "未捕获到 boot banner（烧录本身已成功，可 --probe 复核）",
        time.time() - start))
    return booted


def probe(com, baud):
    """诊断：发 AT+RST，读回 3 秒，判断 UART0 上是否有 hi3861 AT 框架。"""
    print("[诊断] %s 发送 AT+RST，监听 3 秒..." % com)
    try:
        ser = serial.Serial(com, baudrate=baud, timeout=1)
    except Exception as e:
        sys.exit("打开 %s 失败: %s" % (com, e))
    buf = []
    try:
        # 先发一个 AT 探测，再发 AT+RST
        ser.write(b"AT\r\n")
        time.sleep(0.5)
        ser.write("AT+RST={}\r\n".format(20).encode("utf-8"))
        end = time.time() + 3
        while time.time() < end:
            line = ser.readline()
            if line:
                text = line.decode("gbk", errors="ignore")
                sys.stdout.write(text); sys.stdout.flush()
                buf.append(text)
    finally:
        ser.close()
    out = "".join(buf)
    print("\n[诊断] 结论：")
    if "+RST:" in out or (out.strip().endswith("OK")):
        print("  收到 '+RST:' / 'OK' -> AT 框架在运行，AT+RST 会软复位。")
        print("  若 HiBurn 仍连不上，说明软复位不进下载模式，需硬复位（--reset-mode dtr 或手按 RESET）。")
    elif "OHOS" in out or "#" in out:
        print("  收到 OHOS shell 提示 -> 当前固件跑的是 OHOS shell，不认 AT+RST。")
        print("  这就是 AT+RST 无效的根因。需硬复位进下载模式（--reset-mode dtr 或手按 RESET）。")
    elif out.strip():
        print("  收到非预期数据：%r" % out[:80])
        print("  可能是别的固件/波特率。建议手按 RESET 进下载模式。")
    else:
        print("  无任何回显 -> UART0 上没有交互终端（或波特率不对）。")
        print("  AT+RST 无效。需硬复位进下载模式（--reset-mode dtr 或手按 RESET）。")


def main():
    ap = argparse.ArgumentParser(
        description="烧录单个 Hi3861 XTS bin 并自动 reset 执行",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bin", nargs="?", help="要烧录的 .bin 文件路径（--probe 模式可省略）")
    ap.add_argument("-com", default=None, help="COM 端口（不指定则自动检测；多端口时列出请显式指定）")
    ap.add_argument("-baud", type=int, default=115200)
    ap.add_argument("--hiburn", default=DEFAULT_HIBURN)
    ap.add_argument("--rst-wait", type=int, default=20)
    ap.add_argument("--reset-mode", choices=["at", "dtr", "none"], default="at",
                    help="进下载模式的方式：at=AT+RST软复位 / dtr=DTR/RTS硬复位 / none=不自动复位")
    ap.add_argument("--pre-wait", type=float, default=0.2,
                    help="复位后到 HiBurn 的间隔秒数（含 HiBurn 冷启动余量，过小易错过下载握手窗口）")
    ap.add_argument("--retries", type=int, default=5)
    ap.add_argument("--timeout", type=int, default=90, help="回读输出超时秒数")
    ap.add_argument("--log", default=None)
    ap.add_argument("--skip-at-rst", action="store_true",
                    help="等价于 --reset-mode none：不自动复位，HiBurn 提示时手按 RESET")
    ap.add_argument("--probe", action="store_true",
                    help="诊断模式：发 AT+RST 看回显，判断 AT 框架是否在运行，不烧录")
    ap.add_argument("--run-only", action="store_true",
                    help="不烧录，仅发 AT+RST 软复位重跑 XTS 并回读（镜像已烧好时用，免按键）")
    ap.add_argument("--burn-only", action="store_true",
                    help="仅烧录：烧完发复位魔字节启动新固件并短确认（5s），不进入 XTS 回读循环。"
                         "后续用 --run-only 单独执行 XTS。")
    args = ap.parse_args()

    # COM 端口自动检测（不硬编码 COM4——不同机器端口不同）
    if args.com is None:
        try:
            from serial.tools import list_ports
            ports = [p.device for p in sorted(list_ports.comports())]
        except ImportError:
            ports = []
        if not ports:
            ap.error("未指定 -com，且无法自动检测串口（pyserial 未装？）。请用 -com <端口> 指定，如 -com COM5")
        if len(ports) == 1:
            args.com = ports[0]
            print(f"[burn] 自动检测到唯一串口: {args.com}")
        else:
            ap.error(f"未指定 -com，检测到多个串口: {ports}。请用 -com <端口> 显式指定。")

    # 触板操作（--probe 诊断 / 烧录 / --run-only / 烧+启动确认 / 烧+跑测试）统一持
    # COM 端口锁——跨入口互斥：防止并发操作同一 COM（复位/串口写入会打断进行中
    # 的 Flash 写入）。--probe 也持锁：它会发 AT+RST 复位板子，并非纯只读；
    # 持锁使"另一任务烧录/测试中"表现为明确的锁占用提示，而非含糊的串口打开失败。
    # 锁不可用（非 Windows）→ 降级无锁，由登记 owner 检查 + 串口占用检查兜底。
    lock_fh = _acquire_burn_lock(args.com)
    if lock_fh is False:
        sys.exit(1)  # 占用信息已由 _acquire_burn_lock 打印
    try:
        if args.probe:
            probe(args.com, args.baud)
            return
        _run_board_flow(args)
    finally:
        if lock_fh is not None:
            release_com_lock(lock_fh)


def _run_board_flow(args):
    """触板主流程（调用方 main 已持 COM 端口锁）：--run-only 或 烧录（+启动确认/+跑测试）。"""
    if args.run_only:
        finished, passed, failed = run_only(args.com, args.baud, args.rst_wait, args.timeout, args.log)
        if not finished:
            sys.exit(1)  # timeout / no end sign
        if failed > 0:
            sys.exit(2)  # test failures
        if passed + failed == 0:
            sys.exit(3)  # zero test cases
        return
    if not args.bin:
        sys.exit("请指定 bin 文件路径，或用 --probe / --run-only")

    bin_file = os.path.abspath(args.bin)
    if not os.path.isfile(bin_file):
        sys.exit("bin 文件不存在: %s" % bin_file)
    if not os.path.isfile(args.hiburn):
        sys.exit(
            "HiBurn 不存在: %s\n"
            "HiBurn.exe 为华为工具，不随 plugin 分发（用户自备）。\n"
            "修复：将自备的 HiBurn.exe 放到 burn_one.py 同目录（即 tools/，默认查找位置），"
            "或用 --hiburn 指定其绝对路径。" % args.hiburn)

    reset_mode = "none" if args.skip_at_rst else args.reset_mode

    print("bin    : %s" % bin_file)
    print("com    : %s @ %d" % (args.com, args.baud))
    print("hiburn : %s" % args.hiburn)
    print("reset  : %s" % ("none(手动按RESET)" if reset_mode == "none" else reset_mode))
    print()

    if not reset_and_burn(args.com, args.baud, args.hiburn, bin_file,
                          args.rst_wait, args.pre_wait, args.retries,
                          reset_mode, args.skip_at_rst):
        sys.exit("\n烧录失败。排查：\n"
                 "  1) python burn_one.py --probe  看 AT+RST 有无回显，确认 AT 框架是否在跑。\n"
                 "  2) 试 --reset-mode dtr（板子支持自动复位时可免按键）。\n"
                 "  3) 用 --skip-at-rst，HiBurn 提示时手按一次 RESET（仅这一下手动，运行复位仍自动）。\n"
                 "  4) 手按 RESET 也连不上时，按住 LINK 再按 RESET。")

    time.sleep(0.8)  # HiBurn.exe 退出后 COM 句柄释放也要时间，留足再开
    if args.burn_only:
        confirmed = boot_and_confirm(args.com, args.baud, peek_secs=5, log_file=args.log)
        if confirmed:
            print("\n[烧录完成] 固件已写入 Flash 且启动确认；未捕获 XTS 输出。"
                  "执行测试请用：--run-only（AT+RST 软复位重跑 XTS）")
        else:
            print("\n[烧录完成] 固件已写入 Flash；启动未确认（5s 内未见输出），"
                  "建议手动复位或用 --run-only 验证。")
            sys.exit(4)  # boot not confirmed
        return
    finished, passed, failed = run_and_read(args.com, args.baud, args.timeout, args.log)
    if not finished:
        sys.exit(1)  # timeout / no end sign
    if failed > 0:
        sys.exit(2)  # test failures
    if passed + failed == 0:
        sys.exit(3)  # zero test cases


if __name__ == "__main__":
    main()
