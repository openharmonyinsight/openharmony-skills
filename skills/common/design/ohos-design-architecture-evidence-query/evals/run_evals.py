#!/usr/bin/env python3
"""把发布 eval 真跑一遍，并把转录写进 `evals/runs/<arm>/`。

三种执行臂（arm），共用同一套夹具，唯一区别是"执行者手上有什么"：

    scripted       本脚本按 SKILL.md 写死的命令逐条执行（确定性复现）
    with-skill     真起一个 codex agent，临时 CODEX_HOME 里装好本 skill
    without-skill  真起一个 codex agent，只给工具代码，不给任何 skill 文档

    python3.12 evals/run_evals.py --arm scripted
    python3.12 evals/run_evals.py --arm with-skill    --jobs 3
    python3.12 evals/run_evals.py --arm without-skill --jobs 3
    python3.12 evals/run_evals.py --arm with-skill --only 4     # 单场景
    python3.12 evals/run_evals.py --live-smoke                  # 真连 CI 端点

产物：`evals/runs/<arm>/NN-<name>.md` 转录 + `summary.json`。夹具、临时工作区、
agent 事件流默认落在系统临时目录（`--workdir` 可改），不进仓库。

夹具需要 oskm 源码树（构建真 `oskm-cli.pyz`、生成合成 `knowledge.db`）：
用 `OSKM_SOURCE_ROOT` 指定，否则从本文件向上探测 `packages/oskm`。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import shutil
import signal
import sqlite3
import subprocess
import sys
import tarfile
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

EVALS_DIR = Path(__file__).resolve().parent
SKILL_ROOT = EVALS_DIR.parent
BOOTSTRAP = SKILL_ROOT / 'bootstrap.py'
RUNTIME_PKG = SKILL_ROOT / 'oskm_runtime'
RUNS_DIR = EVALS_DIR / 'runs'

DB_NAME = 'knowledge.db'
CLI_NAME = 'oskm-cli.pyz'
STATE_NAME = '.oskm-runtime.json'
SDK_JS = 'interface/sdk-js'
SDK_C = 'interface/sdk_c'
EVAL_DATE = '20261102'
TOMORROW = (datetime.now() + timedelta(days=1)).strftime('%Y%m%d')
YESTERDAY = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
TODAY = datetime.now().strftime('%Y%m%d')


# ---------------------------------------------------------------- 源码树探测

def find_source_root() -> Path:
    """Locate `packages/oskm` so fixtures can build a real CLI and DB."""
    explicit = os.environ.get('OSKM_SOURCE_ROOT', '').strip()
    candidates = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    here = EVALS_DIR
    candidates.extend([here, *here.parents])
    for candidate in candidates:
        root = Path(candidate)
        if root.name == 'oskm' and (root.parent.name == 'packages'):
            pass
        probe = root if (root / 'oskm_testing' / 'fixture.py').is_file() else None
        if probe is None and (root / 'packages' / 'oskm' / 'oskm_testing'
                              / 'fixture.py').is_file():
            probe = root / 'packages' / 'oskm'
        if probe is not None and (probe / 'cli' / 'scripts' / 'build_cli.py').is_file():
            return probe.resolve()
    raise SystemExit(
        '找不到 oskm 源码树（需要 oskm_testing/fixture.py 与 '
        'cli/scripts/build_cli.py）。请用 OSKM_SOURCE_ROOT=<packages/oskm> 指定。')


def import_fixture_builders(source_root: Path):
    for path in (source_root, source_root / 'cli', source_root / 'cli' / 'scripts'):
        entry = str(path)
        if entry not in sys.path:
            sys.path.insert(0, entry)
    from oskm_testing import fixture as oskm_fixture  # noqa: E402
    import build_cli  # noqa: E402
    return oskm_fixture, build_cli


# ---------------------------------------------------------------- 夹具

@dataclass
class Fixtures:
    """Built once per process; every scenario copies what it needs."""
    root: Path
    db: Path
    cli: Path
    good_archive: Path
    corrupt_archive: Path
    source_root: Path
    cli_tree: Path
    facts: dict = field(default_factory=dict)

    @property
    def db_sha(self) -> str:
        return sha256(self.db)

    @property
    def cli_sha(self) -> str:
        return sha256(self.cli)


def sha256(path) -> str:
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def build_fixtures(workdir: Path, source_root: Path) -> Fixtures:
    oskm_fixture, build_cli = import_fixture_builders(source_root)
    root = workdir / 'fixtures'
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)

    db = oskm_fixture.create_fixture_db(root / DB_NAME)
    cli_meta = build_cli.build_pyz(root / CLI_NAME)
    cli = Path(cli_meta['archive'])

    sdk_js_file = 'api/@internal/ohos.evalmarker.d.ts'
    sdk_js_body = 'export interface EvalMarker {\n  readonly id: number;\n}\n'
    sdk_c_file = 'evalmarker.h'
    sdk_c_body = '#ifndef EVALMARKER_H\n#define EVALMARKER_H 1\n#endif\n'

    def write_archive(destination: Path, *, db_bytes: bytes) -> Path:
        stage = destination.parent / f'.stage-{destination.stem}'
        if stage.exists():
            shutil.rmtree(stage)
        (stage / SDK_JS / 'api' / '@internal').mkdir(parents=True)
        (stage / SDK_C).mkdir(parents=True)
        (stage / DB_NAME).write_bytes(db_bytes)
        shutil.copy2(cli, stage / CLI_NAME)
        (stage / SDK_JS / sdk_js_file).write_text(sdk_js_body, encoding='utf-8')
        (stage / SDK_C / sdk_c_file).write_text(sdk_c_body, encoding='utf-8')
        with tarfile.open(destination, 'w:gz') as bundle:
            for name in ('.', 'interface', SDK_JS, SDK_JS + '/api',
                         SDK_JS + '/api/@internal', SDK_C):
                info = tarfile.TarInfo(name)
                info.type = tarfile.DIRTYPE
                info.mode = 0o755
                bundle.addfile(info)
            for relative in (DB_NAME, CLI_NAME, f'{SDK_JS}/{sdk_js_file}',
                             f'{SDK_C}/{sdk_c_file}'):
                bundle.add(stage / relative, arcname=relative)
        shutil.rmtree(stage)
        return destination

    good = write_archive(root / 'knowledge.tar.gz', db_bytes=db.read_bytes())
    corrupt = write_archive(
        root / 'knowledge-corrupt.tar.gz',
        db_bytes=b'THIS-IS-NOT-SQLITE' + os.urandom(4096))

    # 一个"完整的 OpenHarmony 源码根"：.gn + 两套非空 SDK + out/**/oskm/knowledge.db
    # + cli/dist/oskm-cli.pyz。install 应该优先用它，并且一次网络都不发。
    source = root / 'source'
    (source / SDK_JS / 'api' / '@internal').mkdir(parents=True)
    (source / SDK_C).mkdir(parents=True)
    (source / 'out' / 'sample-product' / 'oskm').mkdir(parents=True)
    (source / 'cli' / 'dist').mkdir(parents=True)
    (source / '.gn').write_text(
        'buildconfig = "//build/config/BUILDCONFIG.gn"\n', encoding='utf-8')
    (source / SDK_JS / sdk_js_file).write_text(sdk_js_body, encoding='utf-8')
    (source / SDK_C / sdk_c_file).write_text(sdk_c_body, encoding='utf-8')
    shutil.copy2(db, source / 'out' / 'sample-product' / 'oskm' / DB_NAME)
    shutil.copy2(cli, source / 'cli' / 'dist' / CLI_NAME)

    # 只有源码树 CLI 布局（cli/oskm_cli/__init__.py）的最小目录，用来验证
    # cli-path 的第二级候选。
    cli_tree = root / 'cli-tree'
    (cli_tree / 'cli' / 'oskm_cli').mkdir(parents=True)
    (cli_tree / 'cli' / 'oskm_cli' / '__init__.py').write_text(
        "__version__ = '9.9.9'\n", encoding='utf-8')

    return Fixtures(
        root=root, db=db, cli=cli, good_archive=good, corrupt_archive=corrupt,
        source_root=source, cli_tree=cli_tree,
        facts={
            'source_root': str(source_root),
            'cli_sha256': sha256(cli),
            'cli_bytes': cli.stat().st_size,
            'db_sha256': sha256(db),
            'good_archive_sha256': sha256(good),
            'corrupt_archive_sha256': sha256(corrupt),
        })


# ---------------------------------------------------------------- 夹具服务端

class FixtureHandler(BaseHTTPRequestHandler):
    """A local stand-in for the CI endpoints; logs every request."""

    protocol_version = 'HTTP/1.1'
    server_version = 'oskm-eval-fixture/1.0'
    #: keep-alive 空闲连接必须自己断开：agent 派生的 curl/子进程可能在 turn 结束后
    #: 仍然握着连接，`server_close()` 就会一直等它——实测把一个场景卡了 70 分钟。
    timeout = 5

    def _record(self, body: bytes | None):
        entry = {
            'seq': self.server.next_seq(),
            'ts': datetime.now().astimezone().isoformat(timespec='milliseconds'),
            'method': self.command,
            'path': self.path,
            'user_agent': self.headers.get('User-Agent', ''),
            'accept': self.headers.get('Accept', ''),
            'body': None,
        }
        if body:
            try:
                entry['body'] = json.loads(body.decode('utf-8'))
            except (UnicodeDecodeError, json.JSONDecodeError):
                entry['body'] = body[:200].hex()
        self.server.record(entry)

    def _send(self, payload: bytes, content_type: str, status: int = 200):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):  # noqa: N802
        length = int(self.headers.get('Content-Length') or 0)
        body = self.rfile.read(length) if length else b''
        self._record(body)
        if not self.path.startswith('/openharmony/'):
            self._send(b'{"error":"not found"}', 'application/json', 404)
            return
        document = json.loads(body.decode('utf-8')) if body else {}
        start = str(document.get('startTime', ''))
        date = start[:8] or 'unknown-date'
        payload = json.dumps({'data': {'list': {'dataList': [
            {'obsPath': f'/openharmony/obs/{date}/knowledge.tar.gz'}]}}}).encode()
        self._send(payload, 'application/json')

    def do_GET(self):  # noqa: N802
        self._record(None)
        fixtures: Fixtures = self.server.fixtures
        if self.path.startswith('/openharmony/obs/') or \
                self.path.startswith('/internal/'):
            archive = fixtures.good_archive
        elif self.path.startswith('/corrupt/'):
            archive = fixtures.corrupt_archive
        else:
            self._send(b'{"error":"not found"}', 'application/json', 404)
            return
        self._send(archive.read_bytes(), 'application/gzip')

    def log_message(self, *args):  # silence stderr noise
        return


class FixtureServer:
    def __init__(self, fixtures: Fixtures, log_path: Path):
        self.fixtures = fixtures
        self.log_path = log_path
        self._lock = threading.Lock()
        self._seq = 0
        self._entries: list[dict] = []
        outer = self

        class _Server(ThreadingHTTPServer):
            daemon_threads = True
            #: 关服务端时不等 handler 线程收场，理由同 `timeout`。
            block_on_close = False
            allow_reuse_address = True

            def handle_error(self, request, client_address):
                # 评估夹具：agent 派生的 curl 提前断开是常态，不往 stderr 刷栈。
                return

            def next_seq(self):
                with outer._lock:
                    outer._seq += 1
                    return outer._seq

            def record(self, entry):
                with outer._lock:
                    outer._entries.append(entry)

        self._server = _Server(('127.0.0.1', 0), FixtureHandler)
        self._server.fixtures = fixtures
        self._thread = threading.Thread(target=self._server.serve_forever,
                                        daemon=True)

    def start(self) -> 'FixtureServer':
        self._thread.start()
        return self

    def stop(self) -> None:
        self._server.shutdown()
        self._server.server_close()
        self.flush()

    @property
    def base(self) -> str:
        host, port = self._server.server_address[:2]
        return f'http://{host}:{port}'

    def requests(self) -> list[dict]:
        with self._lock:
            return list(self._entries)

    def flush(self) -> None:
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self._lock, self.log_path.open('w', encoding='utf-8') as stream:
            for entry in self._entries:
                stream.write(json.dumps(entry, ensure_ascii=False) + '\n')

    def mark(self) -> int:
        with self._lock:
            return len(self._entries)

    def since(self, mark: int) -> list[dict]:
        with self._lock:
            return list(self._entries[mark:])


# ---------------------------------------------------------------- 执行与转录

MAX_OUTPUT_CHARS = 6000


def clip(text: str, limit: int = MAX_OUTPUT_CHARS) -> str:
    if len(text) <= limit:
        return text
    head = text[:limit // 2]
    tail = text[-limit // 4:]
    return (f'{head}\n… [输出截断，完整内容见工作区] …\n{tail}')


def quote_command(parts) -> str:
    return ' '.join(shlex.quote(str(part)) for part in parts)


def q(value) -> str:
    return shlex.quote(str(value))


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec='seconds')


@dataclass
class StepResult:
    label: str
    command: str
    cwd: str
    rc: int
    stdout: str
    stderr: str
    seconds: float


@dataclass
class CheckResult:
    name: str
    kind: str          # auto | manual
    ok: bool | None    # None = manual
    evidence: str


class ScenarioRun:
    """One scenario, one arm: fixtures, commands, transcript, checks."""

    def __init__(self, *, scenario, arm, workdir, fixtures, server, python,
                 codex, home, timeout, source_root, arm_root=None):
        self.scenario = scenario
        self.arm = arm
        self.workdir = Path(workdir)
        self.fixtures = fixtures
        self.server = server
        self.python = python
        self.codex = codex
        self.home = Path(home)
        self.timeout = timeout
        self.source_root = source_root
        self.arm_root = Path(arm_root) if arm_root else Path(workdir).parent.parent
        self.steps: list[StepResult] = []
        self.checks: list[CheckResult] = []
        self.notes: list[tuple[str, str]] = []
        self.agent: dict | None = None
        self.started = now()
        self._request_mark = server.mark() if server else 0

    # -- 环境 ------------------------------------------------------------
    def env(self, **overrides) -> dict:
        env = {
            'PATH': os.environ.get('PATH', '/usr/bin:/bin'),
            'HOME': str(self.home),
            'CODEX_HOME': str(self.home / '.codex'),
            'LANG': os.environ.get('LANG', 'en_US.UTF-8'),
            'LC_ALL': os.environ.get('LC_ALL', os.environ.get('LANG', 'en_US.UTF-8')),
            'TMPDIR': os.environ.get('TMPDIR', '/tmp'),
            'PYTHONDONTWRITEBYTECODE': '1',
        }
        # 场景自己声明的 OSKM_* 才算数，开发者 shell 里的残留一律丢掉。
        env.update({key: str(value) for key, value in overrides.items()
                    if value is not None})
        return env

    def oskm_env(self, runtime, *, source=None, endpoint=None, cli=None,
                 **extra) -> dict:
        return self.env(
            OSKM_RUNTIME_ROOT=str(runtime),
            OSKM_DOWNLOAD_SOURCE=source,
            OSKM_DOWNLOAD_ENDPOINT=endpoint,
            OSKM_CLI=cli,
            **extra)

    # -- 执行 ------------------------------------------------------------
    def sh(self, label, command, *, cwd=None, env=None, expect=None,
           timeout=600) -> StepResult:
        cwd = Path(cwd) if cwd else self.workdir
        cwd.mkdir(parents=True, exist_ok=True)
        started = time.monotonic()
        try:
            proc = subprocess.run(
                ['/bin/bash', '-c', command], cwd=str(cwd),
                capture_output=True, text=True, timeout=timeout,
                env=env if env is not None else self.env())
            rc, out, err = proc.returncode, proc.stdout, proc.stderr
        except subprocess.TimeoutExpired as exc:
            rc, out, err = 124, exc.stdout or '', (exc.stderr or '') + '\n[timeout]'
        seconds = time.monotonic() - started
        result = StepResult(label=label, command=command, cwd=str(cwd), rc=rc,
                            stdout=out, stderr=err, seconds=round(seconds, 2))
        self.steps.append(result)
        if expect is not None and rc != expect:
            self.check(f'退出码应为 {expect}（{label}）', False,
                       f'实际 {rc}；stderr: {err.strip()[:400]}')
        return result

    def check(self, name, ok, evidence=''):
        self.checks.append(CheckResult(name=name, kind='auto', ok=bool(ok),
                                       evidence=str(evidence)))

    def manual(self, name, evidence=''):
        self.checks.append(CheckResult(name=name, kind='manual', ok=None,
                                       evidence=str(evidence)))

    def note(self, title, body):
        self.notes.append((title, body))

    # -- 夹具视图 --------------------------------------------------------
    def requests(self) -> list[dict]:
        return self.server.since(self._request_mark) if self.server else []

    #: `oskm_runtime` 只用 urllib（UA=`Python-urllib/x.y`）。agent 自己为了验证
    #: 语义常常另外用 curl 打端点做对照实验——那是**评估者的动作**，不是被测
    #: 工具的动作，契约判定只算工具发出的那部分，探测请求单独列出来。
    TOOL_USER_AGENT = 'Python-urllib'

    def tool_requests(self) -> list[dict]:
        return [item for item in self.requests()
                if str(item.get('user_agent', '')).startswith(self.TOOL_USER_AGENT)]

    def probe_requests(self) -> list[dict]:
        return [item for item in self.requests()
                if not str(item.get('user_agent', '')).startswith(
                    self.TOOL_USER_AGENT)]

    def reset_request_mark(self) -> int:
        """夹具准备阶段的请求不算进被测阶段。"""
        self._request_mark = self.server.mark() if self.server else 0
        return self._request_mark

    def prepare(self, label, command, *, cwd=None, env=None, expect=0):
        """Run a fixture-preparation command (all arms get the same pre-state)."""
        result = self.sh(f'[夹具准备] {label}', command, cwd=cwd, env=env)
        if expect is not None and result.rc != expect:
            raise SystemExit(f'夹具准备失败（{label}）：rc={result.rc}\n'
                             f'{result.stdout}\n{result.stderr}')
        return result

    def observed(self) -> str:
        chunks = [step.stdout + '\n' + step.stderr for step in self.steps]
        if self.agent:
            chunks.append(self.agent.get('last_message', ''))
            chunks.append(self.agent.get('answer_file', ''))
            chunks.extend(self.agent.get('commands', []))
        return '\n'.join(chunks)

    # -- agent 臂 --------------------------------------------------------
    def run_agent(self, prompt: str, *, cwd: Path, with_skill: bool,
                  env: dict | None = None) -> dict:
        cwd = Path(cwd)
        cwd.mkdir(parents=True, exist_ok=True)
        (cwd / 'PROMPT.md').write_text(prompt, encoding='utf-8')
        events_path = cwd / 'codex-events.jsonl'
        last_path = cwd / 'agent-last-message.md'
        command = [
            self.codex, 'exec', '--skip-git-repo-check',
            '--sandbox', 'danger-full-access', '-C', str(cwd), '--json',
            '-o', str(last_path), '-',
        ]
        # 事件流直接落文件，不走管道：`subprocess.run(capture_output=True)` 超时
        # 之后会为了等管道 EOF 一直挂着（codex 派生的子进程还握着写端），实测把
        # 整个评估臂卡死过。落文件既不会卡，超时被杀后转录里还留着已产生的事件。
        err_path = cwd / 'codex-stderr.log'
        started = time.monotonic()
        timed_out = False
        with events_path.open('wb') as events_file, \
                err_path.open('wb') as err_file:
            proc = subprocess.Popen(
                command, stdin=subprocess.PIPE, stdout=events_file,
                stderr=err_file, cwd=str(cwd), start_new_session=True,
                env=env if env is not None else self.env())
            try:
                proc.communicate(input=prompt.encode('utf-8'),
                                 timeout=self.timeout)
            except subprocess.TimeoutExpired:
                timed_out = True
                kill_group(proc)
                try:
                    proc.wait(timeout=30)
                except subprocess.TimeoutExpired:
                    pass
            rc = 124 if timed_out else proc.returncode
        seconds = round(time.monotonic() - started, 1)
        if timed_out:
            with err_path.open('ab') as err_file:
                err_file.write(
                    f'\n[harness] timeout after {self.timeout}s; '
                    'process group killed\n'.encode('utf-8'))
        roots = [self.workdir, self.home, self.arm_root,
                 Path(self.workdir).parent, Path(self.arm_root).parent]
        if self.fixtures is not None:
            roots.append(self.fixtures.root)
        summary = summarize_events(events_path, allowed_roots=roots)
        answer = ''
        if last_path.is_file():
            answer = last_path.read_text(encoding='utf-8', errors='replace')
        info = {
            'rc': rc,
            'seconds': seconds,
            'last_message': answer,
            'answer_file': read_if_any(cwd / 'answer.md'),
            'commands': summary['commands'],
            'skill_files_touched': summary['skill_hits'],
            'outside_hits': summary['outside_hits'],
            'stderr_tail': read_if_any(err_path)[-800:],
            'timed_out': timed_out,
            'events': summary['counts'],
            'usage': summary['usage'],
            'cwd': str(cwd),
            'with_skill': with_skill,
        }
        self.agent = info
        self.steps.append(StepResult(
            label='codex exec（agent 臂）',
            command=quote_command(command[:6]) + ' … < PROMPT.md',
            cwd=str(cwd), rc=rc, stdout=clip(answer, 4000),
            stderr=info['stderr_tail'], seconds=seconds))
        return info


def kill_group(proc) -> None:
    """Kill the whole process group.

    codex 会派生子进程；只杀父进程会留下握着管道的孤儿，`communicate()` 就永远
    等不到 EOF。所以自建进程组，超时后整组 SIGKILL。
    """
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    except (OSError, ProcessLookupError):
        try:
            proc.kill()
        except OSError:
            pass


def read_if_any(path: Path) -> str:
    try:
        return path.read_text(encoding='utf-8', errors='replace')
    except OSError:
        return ''


def summarize_events(path: Path, *, allowed_roots=()) -> dict:
    """Pull the auditable bits out of a `codex exec --json` event stream.

    只认两类事实：**执行过哪些命令**（`item.type == command_execution`）与
    **有没有读 skill 文档**（路径里出现 SKILL.md / skills 目录）。token 用量
    取自 `turn.completed`，用来在报告里对比两个臂的成本。
    """
    commands: list[str] = []
    skill_hits: set[str] = set()
    counts: dict[str, int] = {}
    usage = {'input_tokens': 0, 'cached_input_tokens': 0, 'output_tokens': 0,
             'reasoning_output_tokens': 0}
    text = read_if_any(path)
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith('{'):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        kind = str(event.get('type') or '?')
        counts[kind] = counts.get(kind, 0) + 1
        for value in walk_strings(event):
            if 'SKILL.md' in value or f'skills/{SKILL_NAME}' in value:
                skill_hits.add(value[:200])
        item = event.get('item') if isinstance(event.get('item'), dict) else {}
        item_type = item.get('type')
        if item_type:
            key = f'item:{item_type}'
            counts[key] = counts.get(key, 0) + 1
        if kind == 'item.started' and item_type == 'command_execution':
            command = item.get('command')
            if isinstance(command, list):
                commands.append(' '.join(str(part) for part in command))
            elif isinstance(command, str):
                commands.append(command)
        payload = event.get('msg') if isinstance(event.get('msg'), dict) else None
        if payload and isinstance(payload.get('command'), (str, list)):
            command = payload['command']
            commands.append(command if isinstance(command, str)
                            else ' '.join(str(part) for part in command))
        turn_usage = event.get('usage') if isinstance(event.get('usage'), dict) \
            else None
        if turn_usage:
            for key in usage:
                usage[key] += int(turn_usage.get(key) or 0)
    outside = find_outside_commands(commands, allowed_roots)
    return {'commands': commands, 'skill_hits': sorted(skill_hits),
            'counts': counts, 'usage': usage, 'outside_hits': outside}


#: 越界审计：真实源码仓与用户主目录都在 `/Users/` 下，评估工作区在临时目录里。
#: 基线臂一旦读到源码仓、skill 文档或本评估器的实现，这一跑就作废——它衡量的
#: 不再是"没有这份知识增量能走多远"。只挑三类**确定**的越界信号：
#:   1. 命令里出现 `/Users/...` 绝对路径（宿主源码仓、别的 skill 安装目录）
#:   2. 命令里出现别的评估工作区（`oskm-eval*` 但不在自己的根下）
#:   3. 用 `ps` / `pgrep` / `lsof` 反查宿主进程（上一轮基线就是这样找到源码仓的）
#: 不做"任何工作区外路径都算越界"的宽判定：agent 在 answer.md 里写 `/var/...`
#: 这类省略路径是正常表达，宽判定会把它误判成越界，反而毁掉真实结果。
#: agent 写 `answer.md` 时用 heredoc，正文里会出现 `pgrep`、`/var/...` 这类字样。
#: 那是**结论文本**不是命令，审计前先把 heredoc 正文剥掉，否则会把自己写的
#: 说明当成越界命令（实测误判过 3 个场景）。
HEREDOC_RE = re.compile(
    r"<<-?\s*[^A-Za-z0-9_\n]{0,8}([A-Za-z_][A-Za-z0-9_]*)"
    r"[^A-Za-z0-9_\n]{0,8}\n.*?\n[ \t]*\1", re.S)


def strip_heredocs(command: str) -> str:
    return HEREDOC_RE.sub('<<heredoc>>', command)


PATH_TOKEN = re.compile(
    r'/(?:Users|var|private|tmp|opt)[/A-Za-z0-9_.+\-]*')
#: 只在"命令位"（行首或 `;`/`&&`/`|`/`$(` 之后）才算宿主进程探测：
#: agent 在 answer.md 里写「没有用 ps/pgrep/lsof」是结论，不是动作。
HOST_PROBE = re.compile(
    r'(?:^|[;&|\n]|\$\(|`|\bthen\s|\bdo\s)\s*'
    r'(?:ps\s+(?:aux|-ef|-A|-eo)|pgrep|lsof)\b')


def find_outside_commands(commands, allowed_roots=()) -> list:
    """Return the commands that reached outside the evaluation sandbox."""
    # macOS 上 `/var` 是 `/private/var` 的符号链接，agent 拿到的常是解析后的
    # 绝对路径；两种写法都要算"自己的工作区"。
    own: list[str] = []
    for root in allowed_roots:
        if not root:
            continue
        text = str(root)
        own.append(text)
        try:
            resolved = str(Path(text).resolve())
        except OSError:
            continue
        if resolved not in own:
            own.append(resolved)
    hits = []
    for command in commands:
        scanned = strip_heredocs(command)
        reasons = []
        for token in set(PATH_TOKEN.findall(scanned)):
            if token.startswith('/Users/'):
                reasons.append(f'宿主路径: {token}')
            elif 'oskm-eval' in token and not any(
                    token.startswith(root) for root in own):
                reasons.append(f'其它评估工作区: {token}')
        probe = HOST_PROBE.search(scanned)
        if probe:
            reasons.append(f'宿主进程探测: {probe.group(0).strip()}')
        if reasons:
            hits.append({'reasons': sorted(set(reasons))[:4],
                         'command': command[:240]})
    return hits


def walk_strings(node, depth: int = 0):
    if depth > 8:
        return
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for value in node.values():
            yield from walk_strings(value, depth + 1)
    elif isinstance(node, list):
        for value in node:
            yield from walk_strings(value, depth + 1)


# ---------------------------------------------------------------- 检查助手

def is_sqlite(path) -> bool:
    try:
        with Path(path).open('rb') as stream:
            return stream.read(16).startswith(b'SQLite format 3\x00')
    except OSError:
        return False


def scans_readable(path) -> bool:
    try:
        connection = sqlite3.connect(Path(path).as_uri() + '?mode=ro', uri=True)
    except sqlite3.Error:
        return False
    try:
        connection.execute('SELECT 1 FROM scans LIMIT 1').fetchone()
        return True
    except sqlite3.Error:
        return False
    finally:
        connection.close()


def state_document(runtime) -> dict | None:
    path = Path(runtime) / STATE_NAME
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return None


def count_files(directory) -> int:
    directory = Path(directory)
    if not directory.is_dir():
        return 0
    return sum(1 for path in directory.rglob('*') if path.is_file())


def file_map(root) -> dict:
    root = Path(root)
    if not root.exists():
        return {}
    return {str(path.relative_to(root)): sha256(path)
            for path in sorted(root.rglob('*')) if path.is_file()}


def leftovers(runtime) -> list:
    return sorted(path.name for path in Path(runtime).glob('.oskm-runtime-*')
                  if path.is_dir())


def same_path(left, right) -> bool:
    try:
        return Path(str(left).strip()).resolve() == Path(right).resolve()
    except OSError:
        return False


def bootstrap_cmd(run, *args) -> str:
    return quote_command([run.python, BOOTSTRAP, *args])


def copy_tree(source, destination) -> Path:
    destination = Path(destination)
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination, symlinks=True)
    return destination


def agent_prompt(run, task: str, facts: list, ws: Path) -> str:
    lines = [
        '# 任务',
        '',
        task.strip(),
        '',
        '# 环境事实（夹具已就位，请勿修改 fixtures 目录）',
        '',
        *facts,
        '',
        '# 交付要求',
        '',
        '- 真的把命令跑出来，不要只描述步骤或凭记忆作答。',
        '- 结束后把结论写进当前工作目录的 `answer.md`：包含你执行过的关键命令、'
        '关键输出片段，以及对任务的直接回答。',
        '- 不要访问或修改 `~/.oskm`；本次评估的运行时根目录以任务里给出的路径为准。',
        f'- 边界：只在本工作区（`{ws}`）、夹具目录与你的 `CODEX_HOME` 内工作。'
        '不要去工作区之外找这个工具的文档、实现或评估材料，也不要通过 `ps` / '
        '`pgrep` / `lsof` 之类去反查宿主进程——那样这一次评估就作废了。',
    ]
    if run.arm == 'without-skill':
        lines += [
            '',
            '# 说明',
            '',
            f'- 本任务没有配套说明文档。可用的工具代码在 {q(ws / "tool")}'
            '（`bootstrap.py` 与 `oskm_runtime/`），请自行判断怎么用。',
        ]
    return '\n'.join(lines) + '\n'


def give_tool_code(run, ws: Path) -> Path:
    """without-skill 臂：只给代码，不给任何 skill 文档。"""
    tool = ws / 'tool'
    tool.mkdir(parents=True, exist_ok=True)
    shutil.copy2(BOOTSTRAP, tool / BOOTSTRAP.name)
    destination = tool / RUNTIME_PKG.name
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(RUNTIME_PKG, destination,
                    ignore=shutil.ignore_patterns('.env', '__pycache__'))
    return tool


# ---------------------------------------------------------------- 场景 1

def scenario_01(run):
    ws = run.workdir
    agent_start = ws / 'agent-start'
    agent_start.mkdir(parents=True, exist_ok=True)
    runtime = ws / 'runtime'
    runtime.mkdir(parents=True, exist_ok=True)
    endpoint = f'{run.server.base}/internal'
    env = run.oskm_env(runtime, source='INTERNAL_CI', endpoint=endpoint)
    facts = [
        f'- Agent 启动目录（当前目录）：{agent_start}',
        f'- 托管运行时根目录（`OSKM_RUNTIME_ROOT` 已指向它，当前为空）：{runtime}',
        f'- 下载方式已配置：`OSKM_DOWNLOAD_SOURCE=INTERNAL_CI`，'
        f'`OSKM_DOWNLOAD_ENDPOINT={endpoint}`（本地夹具服务已启动）',
        '- 该端点按日期返回完整 `knowledge.tar.gz`，内含 `knowledge.db`、'
        '`oskm-cli.pyz`、`interface/sdk-js/`、`interface/sdk_c/`',
        f'- Python 解释器：{run.python}',
    ]
    if run.arm == 'scripted':
        run.sh('记录 Agent 启动目录', 'pwd', cwd=agent_start, env=env)
        run.sh('用绝对路径安装托管运行时（不 cd 到 skill 目录）',
               bootstrap_cmd(run, '--runtime-root', runtime, 'install',
                             '--source', 'INTERNAL_CI', '--date', TODAY),
               cwd=agent_start, env=env, expect=0)
        run.sh('确认当前目录未变', 'pwd', cwd=agent_start, env=env)
        run.sh('运行时布局', f'find {q(runtime)} -maxdepth 3 | sort', env=env)
        run.sh('状态文件', f'cat {q(runtime / STATE_NAME)}', env=env)
    else:
        if run.arm == 'without-skill':
            give_tool_code(run, ws)
        run.run_agent(agent_prompt(run, run.scenario['prompt'], facts, ws),
                      cwd=agent_start, with_skill=(run.arm == 'with-skill'),
                      env=env)

    document = state_document(runtime) or {}
    run.check('knowledge.db 装到了运行时根目录',
              is_sqlite(runtime / DB_NAME), f'{runtime / DB_NAME}')
    run.check('oskm-cli.pyz 与 DB 并排（同一次安装装齐）',
              (runtime / CLI_NAME).is_file(), f'{runtime / CLI_NAME}')
    run.check('interface/sdk-js 非空', count_files(runtime / SDK_JS) > 0,
              f'{count_files(runtime / SDK_JS)} 个文件')
    run.check('interface/sdk_c 非空', count_files(runtime / SDK_C) > 0,
              f'{count_files(runtime / SDK_C)} 个文件')
    run.check('状态文件同时记录 db / sdk / cli 三段',
              all(key in document for key in ('db', 'sdk', 'cli')),
              json.dumps(sorted(document), ensure_ascii=False))
    requests = run.tool_requests()
    dated = [item for item in requests
             if re.fullmatch(r'/internal/\d{8}', item['path'])]
    run.check('工具每次安装只发一条"按日期取归档"的请求'
              '（没有盲探端点，也没有单独的 CLI 下载端点）',
              bool(requests) and len(dated) == len(requests)
              and (runtime / CLI_NAME).is_file(),
              f'请求数={len(requests)}，其中按日期归档请求={len(dated)}；'
              f'{CLI_NAME} 已随归档装好={(runtime / CLI_NAME).is_file()}；'
              + json.dumps([{key: item[key] for key in ('method', 'path')}
                            for item in requests], ensure_ascii=False))
    run.check('Agent 启动目录没有被安装产物污染',
              not (agent_start / DB_NAME).exists() and
              not (agent_start / CLI_NAME).exists() and
              not (agent_start / 'interface').exists(),
              f'启动目录内容: {sorted(p.name for p in agent_start.iterdir())}')
    run.check('运行时根目录没有残留安装临时目录', not leftovers(runtime),
              f'leftovers={leftovers(runtime)}')
    if run.arm == 'scripted':
        pwds = [step.stdout.strip() for step in run.steps
                if step.command == 'pwd']
        run.check('安装前后当前目录一致（未用 cd 污染 Agent 启动目录）',
                  len(pwds) == 2 and pwds[0] == pwds[1], f'pwd={pwds}')


# ---------------------------------------------------------------- 场景 2

def scenario_02(run):
    ws = run.workdir
    runtime = ws / 'runtime'
    runtime.mkdir(parents=True, exist_ok=True)
    endpoint = f'{run.server.base}/openharmony/api/daily_build/build/list/component'
    env = run.oskm_env(runtime, source='OPENHARMONY_CI', endpoint=endpoint)
    facts = [
        f'- 托管运行时根目录（`OSKM_RUNTIME_ROOT`，当前为空）：{runtime}',
        f'- `OSKM_DOWNLOAD_SOURCE=OPENHARMONY_CI`，'
        f'`OSKM_DOWNLOAD_ENDPOINT={endpoint}`（本地夹具服务已启动）',
        f'- 要安装的日期：{EVAL_DATE}',
        f'- Python 解释器：{run.python}',
        f'- 当前目录：{ws}',
    ]
    if run.arm == 'scripted':
        run.sh('按显式日期安装',
               bootstrap_cmd(run, '--runtime-root', runtime, 'install',
                             '--source', 'OPENHARMONY_CI', '--date', EVAL_DATE),
               cwd=ws, env=env, expect=0)
        run.sh('install 的参数面（确认没有 --component）',
               bootstrap_cmd(run, 'install', '--help'), cwd=ws, env=env)
        run.sh('状态文件', f'cat {q(runtime / STATE_NAME)}', env=env)
    else:
        if run.arm == 'without-skill':
            give_tool_code(run, ws)
        run.run_agent(agent_prompt(run, run.scenario['prompt'], facts, ws),
                      cwd=ws, with_skill=(run.arm == 'with-skill'), env=env)

    requests = run.tool_requests()
    posts = [item for item in requests if item['method'] == 'POST']
    gets = [item for item in requests if item['method'] == 'GET']
    body = (posts[0]['body'] if posts and isinstance(posts[0]['body'], dict)
            else {})
    run.check('工具的请求只落在"构建列表 POST + obs 归档 GET"两条路径上',
              len(posts) >= 1 and len(gets) >= 1 and
              all((item['method'] == 'POST' and
                   item['path'].endswith('/build/list/component')) or
                  (item['method'] == 'GET' and
                   item['path'].startswith(f'/openharmony/obs/{EVAL_DATE}/'))
                  for item in requests),
              f'POST={len(posts)} GET={len(gets)}；'
              + json.dumps([{key: item[key] for key in ('method', 'path')}
                            for item in requests], ensure_ascii=False))
    run.check('component 固定为 dayu600_7885_ai（不需要用户传）',
              body.get('component') == 'dayu600_7885_ai',
              f"component={body.get('component')}")
    run.check('起止时间都来自同一个显式日期',
              body.get('startTime') == f'{EVAL_DATE}00000000' and
              body.get('endTime') == f'{EVAL_DATE}235959',
              f"startTime={body.get('startTime')} endTime={body.get('endTime')}")
    run.check('只取构建成功的记录', body.get('buildStatus') == 'success',
              f"buildStatus={body.get('buildStatus')}")
    run.check('下载物是 knowledge.tar.gz',
              bool(gets) and gets[0]['path'].endswith('knowledge.tar.gz'),
              gets[0]['path'] if gets else '没有 GET')
    run.check('请求里没有 latest 语义',
              'latest' not in json.dumps(requests, ensure_ascii=False).lower(),
              'request log 无 latest')
    document = state_document(runtime) or {}
    run.check('状态文件记录 source=OPENHARMONY_CI 与 date=' + EVAL_DATE,
              document.get('source') == 'OPENHARMONY_CI' and
              document.get('date') == EVAL_DATE,
              json.dumps({key: document.get(key)
                          for key in ('source', 'date')}, ensure_ascii=False))
    run.check('四件产物装齐',
              is_sqlite(runtime / DB_NAME) and (runtime / CLI_NAME).is_file()
              and count_files(runtime / SDK_JS) > 0
              and count_files(runtime / SDK_C) > 0,
              f'db={is_sqlite(runtime / DB_NAME)} cli={(runtime / CLI_NAME).is_file()}')
    if run.arm == 'scripted':
        help_text = next((step.stdout for step in run.steps
                          if step.command.endswith('install --help')), '')
        run.check('install 没有 --component 参数（component 是固定值）',
                  '--component' not in help_text, 'install --help 输出无 --component')


# ---------------------------------------------------------------- 场景 3

def scenario_03(run):
    ws = run.workdir
    runtime = ws / 'runtime'
    runtime.mkdir(parents=True, exist_ok=True)
    endpoint = f'{run.server.base}/internal'
    env = run.oskm_env(runtime, source='INTERNAL_CI', endpoint=endpoint)
    facts = [
        f'- 托管运行时根目录（`OSKM_RUNTIME_ROOT`，当前为空）：{runtime}',
        f'- `OSKM_DOWNLOAD_SOURCE=INTERNAL_CI`，'
        f'`OSKM_DOWNLOAD_ENDPOINT={endpoint}`（本地夹具服务已启动）',
        f'- 要下载的日期：{EVAL_DATE}',
        f'- Python 解释器：{run.python}',
        f'- 当前目录：{ws}',
    ]
    if run.arm == 'scripted':
        run.sh('按显式日期安装',
               bootstrap_cmd(run, '--runtime-root', runtime, 'install',
                             '--source', 'INTERNAL_CI', '--date', EVAL_DATE),
               cwd=ws, env=env, expect=0)
        run.sh('状态文件', f'cat {q(runtime / STATE_NAME)}', env=env)
    else:
        if run.arm == 'without-skill':
            give_tool_code(run, ws)
        run.run_agent(agent_prompt(run, run.scenario['prompt'], facts, ws),
                      cwd=ws, with_skill=(run.arm == 'with-skill'), env=env)

    requests = run.tool_requests()
    run.check('工具的所有请求都是 GET $OSKM_DOWNLOAD_ENDPOINT/$date',
              bool(requests) and
              all(item['method'] == 'GET' and
                  item['path'] == f'/internal/{EVAL_DATE}'
                  for item in requests),
              f'请求数={len(requests)}；'
              + json.dumps([{key: item[key] for key in ('method', 'path')}
                            for item in requests], ensure_ascii=False))
    run.check('URL 是 $OSKM_DOWNLOAD_ENDPOINT/$date',
              bool(requests) and requests[0]['path'] == f'/internal/{EVAL_DATE}',
              requests[0]['path'] if requests else '没有请求')
    run.check('没有退化成 latest 或系统当天',
              bool(requests) and
              all('latest' not in item['path'] and
                  item['path'] != f'/internal/{TODAY}' for item in requests),
              f'当天是 {TODAY}，工具实际请求 '
              f'{[item["path"] for item in requests] or "-"}')
    document = state_document(runtime) or {}
    run.check('状态文件记录 date=' + EVAL_DATE,
              document.get('date') == EVAL_DATE,
              f"date={document.get('date')}")
    run.check('归档按 knowledge.tar.gz 落地并装齐四件产物',
              is_sqlite(runtime / DB_NAME) and (runtime / CLI_NAME).is_file()
              and count_files(runtime / SDK_JS) > 0
              and count_files(runtime / SDK_C) > 0,
              f'runtime={sorted(p.name for p in runtime.iterdir())}')


# ---------------------------------------------------------------- 场景 4

def scenario_04(run):
    ws = run.workdir
    runtime = ws / 'runtime'
    runtime.mkdir(parents=True, exist_ok=True)
    good_endpoint = f'{run.server.base}/internal'
    corrupt_endpoint = f'{run.server.base}/corrupt'
    prep_env = run.oskm_env(runtime, source='INTERNAL_CI',
                            endpoint=good_endpoint)
    run.prepare('先装一个可用运行时',
                bootstrap_cmd(run, '--runtime-root', runtime, 'install',
                              '--source', 'INTERNAL_CI', '--date', TODAY),
                cwd=ws, env=prep_env, expect=0)
    before = file_map(runtime)
    run.note('被测前状态', '```json\n' + json.dumps(before, indent=2,
                                                    ensure_ascii=False) + '\n```')
    run.reset_request_mark()

    env = run.oskm_env(runtime, source='INTERNAL_CI', endpoint=corrupt_endpoint)
    facts = [
        f'- 已有一个可用运行时：{runtime}（knowledge.db / oskm-cli.pyz / '
        'interface/sdk-js / interface/sdk_c / .oskm-runtime.json 都在）',
        f'- `OSKM_DOWNLOAD_SOURCE=INTERNAL_CI`，'
        f'`OSKM_DOWNLOAD_ENDPOINT={corrupt_endpoint}`'
        '（该端点会正常返回一个 SQLite 已损坏的 knowledge.tar.gz）',
        f'- 刷新目标日期：{TOMORROW}（比已装运行时新，所以 refresh 会真的动手）',
        f'- Python 解释器：{run.python}',
        f'- 当前目录：{ws}',
    ]
    if run.arm == 'scripted':
        result = run.sh('对损坏归档执行 refresh',
                        bootstrap_cmd(run, '--runtime-root', runtime, 'refresh',
                                      '--source', 'INTERNAL_CI',
                                      '--date', TOMORROW),
                        cwd=ws, env=env)
        run.check('refresh 以非零状态失败', result.rc != 0, f'rc={result.rc}')
        run.check('失败信息指向归档/校验',
                  any(token in result.stderr for token in
                      ('归档', '校验', 'SQLite', '失败')),
                  result.stderr.strip()[:300])
    else:
        if run.arm == 'without-skill':
            give_tool_code(run, ws)
        run.run_agent(agent_prompt(run, run.scenario['prompt'], facts, ws),
                      cwd=ws, with_skill=(run.arm == 'with-skill'), env=env)
        run.manual('是否如实报告 refresh 失败（而不是宣称成功）',
                   (run.agent or {}).get('last_message', '')[:600])

    after = file_map(runtime)
    run.check('已有运行时逐文件保持不变（DB / CLI / 两套 SDK / 状态文件）',
              before == after,
              f'变化: {sorted(set(before) ^ set(after)) or "无"}；'
              f'sha 变化: {[k for k in before if before.get(k) != after.get(k)] or "无"}')
    run.check('旧库仍然可打开且 scans 可读', scans_readable(runtime / DB_NAME),
              f'{runtime / DB_NAME}')
    run.check('没有留下半装运行时（无安装/备份临时目录）',
              not leftovers(runtime), f'leftovers={leftovers(runtime)}')
    requests = run.tool_requests()
    run.check('被测阶段工具的请求都指向损坏归档端点（没有转去别处凑数据）',
              bool(requests) and
              all(item['path'].startswith('/corrupt/') for item in requests),
              f'请求数={len(requests)}；'
              + json.dumps([{key: item[key] for key in ('method', 'path')}
                            for item in requests], ensure_ascii=False))


# ---------------------------------------------------------------- 场景 5

def scenario_05(run):
    ws = run.workdir
    source = copy_tree(run.fixtures.source_root, ws / 'source')
    runtime = ws / 'runtime'
    runtime.mkdir(parents=True, exist_ok=True)
    endpoint = f'{run.server.base}/internal'
    env = run.oskm_env(runtime, source='INTERNAL_CI', endpoint=endpoint)
    source_db = source / 'out' / 'sample-product' / 'oskm' / DB_NAME
    source_cli = source / 'cli' / 'dist' / CLI_NAME
    facts = [
        f'- 当前目录是完整的 OpenHarmony 源码根：{source}',
        f'  （`.gn` 是文件，`{SDK_JS}/`、`{SDK_C}/` 非空，'
        f'`out/sample-product/oskm/{DB_NAME}` 与 `cli/dist/{CLI_NAME}` 都在）',
        f'- 托管运行时根目录（`OSKM_RUNTIME_ROOT`，当前为空）：{runtime}',
        f'- 下载端点已配置且可用：`OSKM_DOWNLOAD_SOURCE=INTERNAL_CI`，'
        f'`OSKM_DOWNLOAD_ENDPOINT={endpoint}`（本地夹具服务已启动，会记录每一次请求）',
        f'- Python 解释器：{run.python}',
    ]
    run.reset_request_mark()
    if run.arm == 'scripted':
        result = run.sh('在源码根里安装（不显式给 --source-root）',
                        bootstrap_cmd(run, '--runtime-root', runtime, 'install',
                                      '--date', TODAY),
                        cwd=source, env=env, expect=0)
        run.sh('状态文件', f'cat {q(runtime / STATE_NAME)}', env=env)
        run.sh('源码 DB 与已装 DB 的 sha256',
               f'shasum -a 256 {q(source_db)} {q(runtime / DB_NAME)}', env=env)
    else:
        if run.arm == 'without-skill':
            give_tool_code(run, ws)
        run.run_agent(agent_prompt(run, run.scenario['prompt'], facts, ws),
                      cwd=source, with_skill=(run.arm == 'with-skill'), env=env)

    document = state_document(runtime) or {}
    run.check('本地候选完整时工具一次网络请求都不发',
              not run.tool_requests(),
              json.dumps(run.tool_requests(), ensure_ascii=False) or '工具请求数 0')
    run.check('状态文件记录 source=local', document.get('source') == 'local',
              f"source={document.get('source')}")
    run.check('状态文件记录源码根路径',
              same_path(document.get('source_root', ''), source),
              f"source_root={document.get('source_root')}")
    run.check('装进来的 DB 就是源码树那一份（sha256 相同）',
              (runtime / DB_NAME).is_file() and
              sha256(runtime / DB_NAME) == sha256(source_db),
              f'installed={sha256(runtime / DB_NAME) if (runtime / DB_NAME).is_file() else "-"} '
              f'source={sha256(source_db)}')
    run.check('装进来的 CLI 就是源码树 cli/dist 那一份',
              (runtime / CLI_NAME).is_file() and
              sha256(runtime / CLI_NAME) == sha256(source_cli),
              f'installed={sha256(runtime / CLI_NAME) if (runtime / CLI_NAME).is_file() else "-"} '
              f'source={sha256(source_cli)}')
    run.check('两套 SDK 都从源码树复制过来且非空',
              count_files(runtime / SDK_JS) > 0 and count_files(runtime / SDK_C) > 0,
              f'sdk-js={count_files(runtime / SDK_JS)} sdk_c={count_files(runtime / SDK_C)}')
    run.check('源码树本身没有被改动（DB 仍在原位）',
              source_db.is_file() and source_cli.is_file(),
              f'{source_db} / {source_cli}')
    if run.arm == 'scripted':
        run.check('安装日志说明用了源码本地运行时',
                  '使用源码本地运行时' in run.steps[0].stderr,
                  run.steps[0].stderr.strip()[:300])


# ---------------------------------------------------------------- 场景 6

def _copy_tool(destination: Path) -> Path:
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copy2(BOOTSTRAP, destination / BOOTSTRAP.name)
    package = destination / RUNTIME_PKG.name
    if package.exists():
        shutil.rmtree(package)
    shutil.copytree(RUNTIME_PKG, package,
                    ignore=shutil.ignore_patterns('.env', '__pycache__'))
    return destination / BOOTSTRAP.name


def scenario_06(run):
    ws = run.workdir
    fixtures = run.fixtures
    installed_runtime = ws / 'installed-runtime'
    installed_runtime.mkdir(parents=True, exist_ok=True)
    shutil.copy2(fixtures.cli, installed_runtime / CLI_NAME)
    empty_runtime = ws / 'empty-runtime'
    empty_runtime.mkdir(parents=True, exist_ok=True)
    agent_start = ws / 'agent-start'
    agent_start.mkdir(parents=True, exist_ok=True)

    # 源码树候选：cli/oskm_cli/__init__.py 决定"这是不是源码树"，
    # 而 cli_install 是从**自己所在的包**向上探测的，所以工具代码要放进树里。
    source_tree = ws / 'source-tree'
    (source_tree / 'cli' / 'oskm_cli').mkdir(parents=True, exist_ok=True)
    (source_tree / 'cli' / 'oskm_cli' / '__init__.py').write_text(
        "__version__ = '9.9.9'\n", encoding='utf-8')
    tool_in_tree = _copy_tool(source_tree / 'skills' / SKILL_NAME)
    plain_tool = _copy_tool(ws / 'plain-tool')

    env_all = run.oskm_env(installed_runtime, cli=fixtures.cli)
    env_tree = run.oskm_env(installed_runtime)
    env_none = run.oskm_env(empty_runtime)
    facts = [
        f'- 已安装 CLI 的运行时根目录：{installed_runtime}（内含 {CLI_NAME}）',
        f'- 空的运行时根目录：{empty_runtime}',
        f'- 环境变量 `OSKM_CLI` 可指向：{fixtures.cli}',
        f'- 一个源码树（含 `cli/oskm_cli/__init__.py`）：{source_tree}',
        f'- 工具入口：{plain_tool}（不在任何源码树内）与 {tool_in_tree}（在源码树内）',
        f'- Python 解释器：{run.python}',
        f'- 当前目录：{agent_start}',
        '- 本次任务不需要联网，下载端点未配置。',
    ]
    run.reset_request_mark()
    if run.arm == 'scripted':
        a = run.sh('a) 三个候选都在，且设置了 OSKM_CLI',
                   bootstrap_cmd(run, '--runtime-root', installed_runtime,
                                 'cli-path'),
                   cwd=agent_start, env=env_all, expect=0)
        b = run.sh('b) 去掉 OSKM_CLI，工具代码在源码树里',
                   quote_command([run.python, tool_in_tree, '--runtime-root',
                                  installed_runtime, 'cli-path']),
                   cwd=agent_start, env=env_tree, expect=0)
        c = run.sh('c) 再去掉源码树，只剩已安装产物',
                   quote_command([run.python, plain_tool, '--runtime-root',
                                  installed_runtime, 'cli-path']),
                   cwd=agent_start, env=env_tree, expect=0)
        d = run.sh('d) 三个候选都不存在',
                   quote_command([run.python, plain_tool, '--runtime-root',
                                  empty_runtime, 'cli-path']),
                   cwd=agent_start, env=env_none)
        run.check('a) 选中 $OSKM_CLI', same_path(a.stdout, fixtures.cli),
                  f'stdout={a.stdout.strip()}')
        run.check('b) 选中源码树 CLI', same_path(b.stdout, source_tree),
                  f'stdout={b.stdout.strip()}')
        run.check('c) 选中 <runtime-root>/oskm-cli.pyz',
                  same_path(c.stdout, installed_runtime / CLI_NAME),
                  f'stdout={c.stdout.strip()}')
        run.check('d) 失败并给出可操作的下一步',
                  d.rc != 0 and 'bootstrap.py install' in d.stderr and
                  'OSKM_CLI' in d.stderr,
                  f'rc={d.rc}；stderr={d.stderr.strip()[:400]}')
        run.check('d) 失败信息说明 CLI 不从网络自动下载',
                  'install' in d.stderr, d.stderr.strip()[:200])
    else:
        if run.arm == 'without-skill':
            give_tool_code(run, ws)
        run.run_agent(agent_prompt(run, run.scenario['prompt'], facts, ws),
                      cwd=agent_start, with_skill=(run.arm == 'with-skill'),
                      env=env_tree)
        observed = run.observed()
        run.check('回答给出 $OSKM_CLI → 源码树 → <runtime-root>/oskm-cli.pyz 的顺序',
                  'OSKM_CLI' in observed and CLI_NAME in observed,
                  'answer/输出中同时出现 OSKM_CLI 与 oskm-cli.pyz')
        run.check('回答提到失败时提示 bootstrap.py install',
                  'bootstrap.py install' in observed,
                  'answer/输出中出现 bootstrap.py install')
        run.manual('解析顺序与失败提示是否与实现一致（人工核对转录）',
                   (run.agent or {}).get('last_message', '')[:600])
    run.check('整个过程工具没有联网', not run.tool_requests(),
              json.dumps(run.tool_requests(), ensure_ascii=False)
              or '工具请求数 0')


# ---------------------------------------------------------------- 场景 7

def scenario_07(run):
    ws = run.workdir
    runtime = ws / 'runtime'
    runtime.mkdir(parents=True, exist_ok=True)
    unmanaged = ws / 'unmanaged'
    unmanaged.mkdir(parents=True, exist_ok=True)
    endpoint = f'{run.server.base}/internal'
    prep_env = run.oskm_env(runtime, source='INTERNAL_CI', endpoint=endpoint)
    # evals.json 的前提是"运行时已经过期"，夹具就得真的造一个过期的：
    # date=昨天。这样 refresh 该下载时会下载，不该下载时一次都不发。
    run.prepare(f'装一个 date={YESTERDAY} 的托管运行时（已过期）',
                bootstrap_cmd(run, '--runtime-root', runtime, 'install',
                              '--source', 'INTERNAL_CI', '--date', YESTERDAY),
                cwd=ws, env=prep_env, expect=0)
    shutil.copy2(run.fixtures.db, unmanaged / DB_NAME)
    unmanaged_before = sha256(unmanaged / DB_NAME)
    run.note('被测前状态',
             f'- 托管运行时 `{runtime}`：`date={YESTERDAY}`（今天 {TODAY}，已过期）\n'
             f'- 自管库 `{unmanaged / DB_NAME}`：sha256={unmanaged_before}\n'
             f'- 自管库没有 `{STATE_NAME}`')
    run.reset_request_mark()

    blackhole = 'http://127.0.0.1:9/blackhole'
    env = run.oskm_env(runtime, source='INTERNAL_CI', endpoint=endpoint)
    query_env = run.oskm_env(runtime, source='INTERNAL_CI', endpoint=blackhole)
    unmanaged_env = run.oskm_env(unmanaged, source='INTERNAL_CI',
                                 endpoint=endpoint)
    facts = [
        f'- 托管运行时：{runtime}（状态文件里的 `date={YESTERDAY}`，'
        f'比今天 {TODAY} 旧，即"已过期"；里面有 {CLI_NAME} 与 {DB_NAME}）',
        f'- 另有一个**自管**库（没有 `{STATE_NAME}`）：{unmanaged / DB_NAME}',
        f'- 下载端点可用：`OSKM_DOWNLOAD_SOURCE=INTERNAL_CI`，'
        f'`OSKM_DOWNLOAD_ENDPOINT={endpoint}`（每次请求都会被记录）',
        f'- Python 解释器：{run.python}',
        f'- 当前目录：{ws}',
        '- 要回答的是：用户只是直接跑查询时会不会触发下载；数据过期时正确的'
        '更新动作是什么；没有状态文件的自管库会不会被刷新或覆盖。',
    ]
    if run.arm == 'scripted':
        run.sh('① 端点设为黑洞，直接调 CLI 查询（运行时已过期）',
               quote_command([run.python, runtime / CLI_NAME, '--db',
                              runtime / DB_NAME, 'ask', 'get_scan_info']),
               cwd=ws, env=query_env, expect=0)
        run.check('① 过期运行时上直接查询不触发任何下载',
                  not run.tool_requests(),
                  json.dumps(run.tool_requests(), ensure_ascii=False)
                  or '工具请求数 0')

        run.reset_request_mark()
        run.sh('② 显式 refresh（不带 --date）',
               bootstrap_cmd(run, '--runtime-root', runtime, 'refresh',
                             '--source', 'INTERNAL_CI'),
               cwd=ws, env=env, expect=0)
        document = state_document(runtime) or {}
        run.check('② 只有显式 refresh 才下载，并把 date 推到今天',
                  len(run.tool_requests()) >= 1 and
                  document.get('date') == TODAY,
                  f'工具请求={len(run.tool_requests())}；date={document.get("date")}')

        run.reset_request_mark()
        stale = run.sh('③ 已是最新时再 refresh',
                       bootstrap_cmd(run, '--runtime-root', runtime, 'refresh',
                                     '--source', 'INTERNAL_CI',
                                     '--date', TODAY),
                       cwd=ws, env=env, expect=0)
        run.check('③ 已是最新时 refresh 判定无需刷新、不下载',
                  not run.tool_requests() and
                  ('无需刷新' in stale.stderr or '已是最新' in stale.stderr),
                  f'工具请求数={len(run.tool_requests())}；'
                  f'stderr={stale.stderr.strip()[:200]}')

        run.reset_request_mark()
        run.sh('④ 对自管库执行 refresh',
               bootstrap_cmd(run, '--runtime-root', unmanaged, 'refresh',
                             '--source', 'INTERNAL_CI', '--date', TODAY),
               cwd=ws, env=unmanaged_env)
        run.check('④ 自管库不会被刷新、接管或下载',
                  not (unmanaged / STATE_NAME).exists() and
                  sha256(unmanaged / DB_NAME) == unmanaged_before and
                  not run.tool_requests(),
                  f'状态文件存在={(unmanaged / STATE_NAME).exists()}；'
                  f'sha 未变={sha256(unmanaged / DB_NAME) == unmanaged_before}；'
                  f'工具请求数={len(run.tool_requests())}')
    else:
        if run.arm == 'without-skill':
            give_tool_code(run, ws)
        run.run_agent(agent_prompt(run, run.scenario['prompt'], facts, ws),
                      cwd=ws, with_skill=(run.arm == 'with-skill'), env=env)
        observed = run.observed()
        paths_ok = all(
            re.fullmatch(r'/internal/\d{8}', item['path'])
            for item in run.tool_requests())
        run.check('工具的请求都是"按日期取归档"（没有凭空的 URL，也没有单独下 CLI）',
                  paths_ok,
                  json.dumps([{key: item[key] for key in ('method', 'path')}
                              for item in run.tool_requests()],
                             ensure_ascii=False) or '工具请求数 0')
        run.check('自管库保持原样：没有状态文件、内容未被改写',
                  not (unmanaged / STATE_NAME).exists() and
                  sha256(unmanaged / DB_NAME) == unmanaged_before,
                  f'状态文件存在={(unmanaged / STATE_NAME).exists()}；'
                  f'sha 未变={sha256(unmanaged / DB_NAME) == unmanaged_before}')
        run.check('托管运行时仍然可用（没有被查询搞坏）',
                  scans_readable(runtime / DB_NAME), f'{runtime / DB_NAME}')
        run.check('回答说明直接查询不会触发下载',
                  any(token in observed for token in
                      ('不会下载', '不下载', '没有下载', '不会自动下载',
                       '不触发下载')),
                  '相关表述见转录的 agent 最终回答')
        run.check('回答给出显式更新入口 refresh',
                  'refresh' in observed, 'agent 回答中出现 refresh')
        run.manual('自管库（无状态文件）是否被正确说明为不刷新/不覆盖',
                   (run.agent or {}).get('last_message', '')[:600])

# ---------------------------------------------------------------- 场景 8

def scenario_08(run):
    ws = run.workdir
    artifacts = ws / 'artifacts' / 'synthetic'
    artifacts.mkdir(parents=True, exist_ok=True)
    synthetic = artifacts / DB_NAME
    shutil.copy2(run.fixtures.db, synthetic)
    before = sha256(synthetic)
    runtime = ws / 'runtime'
    runtime.mkdir(parents=True, exist_ok=True)
    plain_tool = _copy_tool(ws / 'plain-tool')
    env = run.oskm_env(runtime, cli=run.fixtures.cli)
    facts = [
        f'- 单独构建出来的 CLI 产物：{run.fixtures.cli}'
        f'（sha256={run.fixtures.cli_sha[:16]}…，'
        f'{run.fixtures.facts["cli_bytes"]} bytes，由 cli/scripts/build_cli.py 构建）',
        f'- 合成库（product=synthetic）：{synthetic}',
        f'- 运行时根目录：{runtime}',
        f'- Python 解释器：{run.python}',
        f'- 当前目录：{ws}',
        '- 本场景只验证 skill 与 CLI 两个产物能组合运行，不校验真实产品数据。',
    ]
    run.reset_request_mark()
    if run.arm == 'scripted':
        located = run.sh('用 cli-path 定位 CLI',
                         quote_command([run.python, plain_tool, '--runtime-root',
                                        runtime, 'cli-path']),
                         cwd=ws, env=env, expect=0)
        query = run.sh('直接调 CLI 查扫描信息',
                       quote_command([run.python, run.fixtures.cli, '--db',
                                      synthetic, 'ask', 'get_scan_info']),
                       cwd=ws, env=env, expect=0)
        run.check('cli-path 找到测试提供的 pyz',
                  same_path(located.stdout, run.fixtures.cli),
                  f'stdout={located.stdout.strip()}')
        run.check('get_scan_info 返回 product=synthetic',
                  '"product": "synthetic"' in query.stdout,
                  query.stdout.strip()[:200])
    else:
        if run.arm == 'without-skill':
            give_tool_code(run, ws)
        run.run_agent(agent_prompt(run, run.scenario['prompt'], facts, ws),
                      cwd=ws, with_skill=(run.arm == 'with-skill'), env=env)
        observed = run.observed()
        run.check('回答里出现 get_scan_info', 'get_scan_info' in observed,
                  'answer/输出中出现 get_scan_info')
        run.check('回答里出现 synthetic', 'synthetic' in observed,
                  'answer/输出中出现 synthetic')
        run.manual('是否明确说明该场景只验证组合链路、不代表真实产品数据',
                   (run.agent or {}).get('last_message', '')[:600])
    run.check('查询是只读的：合成库 sha256 未变',
              sha256(synthetic) == before, f'sha256={sha256(synthetic)}')
    run.check('工具没有联网', not run.tool_requests(),
              json.dumps(run.tool_requests(), ensure_ascii=False)
              or '工具请求数 0')


# ---------------------------------------------------------------- 元信息

def frontmatter() -> dict:
    text = (SKILL_ROOT / 'SKILL.md').read_text(encoding='utf-8')
    block = text.split('---', 2)[1]
    data, section = {}, None
    for line in block.splitlines():
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(' '))
        key, sep, raw = line.strip().partition(':')
        if not sep:
            continue
        value = raw.strip().strip('"\'')
        if indent == 0:
            section = key
            data[key] = value if value else {}
        elif isinstance(data.get(section), dict):
            data[section][key] = value
    return data


SKILL_NAME = frontmatter().get('name') or 'ohos-design-architecture-evidence-query'
SKILL_VERSION = (frontmatter().get('metadata') or {}).get('version', 'unknown')

SCENARIOS = [
    (1, 'first-install-complete-archive', scenario_01),
    (2, 'openharmony-exact-date', scenario_02),
    (3, 'internal-exact-date', scenario_03),
    (4, 'invalid-archive-preserves-runtime', scenario_04),
    (5, 'local-source-runtime-preferred', scenario_05),
    (6, 'cli-resolution-chain', scenario_06),
    (7, 'refresh-is-explicit', scenario_07),
    (8, 'synthetic-database-smoke', scenario_08),
]


def load_evals() -> dict:
    document = json.loads((EVALS_DIR / 'evals.json').read_text(encoding='utf-8'))
    return {item['id']: item for item in document['evals']}


# ---------------------------------------------------------------- agent 环境

def build_codex_config(source: Path) -> str:
    text = Path(source).read_text(encoding='utf-8')

    def grab(pattern, required=True):
        match = re.search(pattern, text, re.M)
        if match:
            return match.group(1)
        if required:
            raise SystemExit(f'无法从 {source} 解析 {pattern}；'
                             '请用 --codex-config 指定一份可用的 codex 配置')
        return None

    model = grab(r'^model\s*=\s*"([^"]+)"')
    provider = grab(r'^model_provider\s*=\s*"([^"]+)"')
    block = re.search(
        rf'^\[model_providers\.{re.escape(provider)}\](.*?)(?=^\[|\Z)',
        text, re.M | re.S)
    if not block:
        raise SystemExit(f'{source} 里没有 [model_providers.{provider}]')
    section = block.group(1)

    def field(name):
        match = re.search(rf'^{name}\s*=\s*"([^"]*)"', section, re.M)
        return match.group(1) if match else None

    base_url = field('base_url')
    wire_api = field('wire_api') or 'responses'
    token = field('experimental_bearer_token') or field('env_key')
    lines = [
        f'model = "{model}"',
        f'model_provider = "{provider}"',
        'model_reasoning_effort = "high"',
        'approval_policy = "never"',
        '',
        f'[model_providers.{provider}]',
        'name = "oskm-eval-baseline"',
        f'base_url = "{base_url}"',
        f'wire_api = "{wire_api}"',
        'requires_openai_auth = false',
    ]
    if token:
        lines.append(f'experimental_bearer_token = "{token}"')
    return '\n'.join(lines) + '\n'


def install_skill_copy(destination: Path) -> Path:
    """把发布包内容（不含 evals/tests/scripts）装进临时 CODEX_HOME。"""
    if destination.exists():
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    ignore = shutil.ignore_patterns(
        '.env', '__pycache__', '*.pyc', '.DS_Store')
    for name in ('SKILL.md', 'README.md', 'bootstrap.py'):
        shutil.copy2(SKILL_ROOT / name, destination / name)
    for name in ('oskm_runtime', 'references', 'examples'):
        shutil.copytree(SKILL_ROOT / name, destination / name, ignore=ignore)
    return destination


def prepare_home(workdir: Path, arm: str, codex_config: Path) -> Path:
    home = workdir / 'home'
    (home / '.codex').mkdir(parents=True, exist_ok=True)
    if arm in ('with-skill', 'without-skill'):
        (home / '.codex' / 'config.toml').write_text(
            build_codex_config(codex_config), encoding='utf-8')
    if arm == 'with-skill':
        install_skill_copy(home / '.codex' / 'skills' / SKILL_NAME)
    return home


# ---------------------------------------------------------------- 转录

def render_transcript(run, meta, workdir: Path) -> str:
    scenario = run.scenario
    lines = [
        f"# E{scenario['id']} {scenario['name']}（{run.arm} 臂）",
        '',
        f'- 开始时间：{run.started}',
        f'- 结束时间：{now()}',
        f'- 执行臂：`{run.arm}`',
        f'- skill：`{SKILL_ROOT}`（name={SKILL_NAME}, version={SKILL_VERSION}）',
        f'- Python：`{run.python}`',
        f'- 工作区：`{run.workdir}`',
        f'- 夹具服务端：{run.server.base if run.server else "（未使用）"}',
        f'- oskm 源码树（夹具来源）：`{run.source_root}`',
        '',
        '## 用户请求（来自 evals.json）',
        '',
        scenario['prompt'].strip(),
        '',
        '## 期望结果（来自 evals.json）',
        '',
        scenario['expected_output'].strip(),
        '',
        '## evals.json 断言',
        '',
        '| 断言 | 类型 |',
        '|---|---|',
    ]
    for assertion in meta.get('assertions', []):
        lines.append(f"| {assertion['text']} | `{assertion['type']}` |")
    lines.append('')

    if run.agent:
        agent = run.agent
        lines += [
            '## Agent 执行审计',
            '',
            f'- 命令：`codex exec --skip-git-repo-check '
            f'--sandbox danger-full-access -C {agent["cwd"]} --json -o '
            'agent-last-message.md -`（prompt 走 stdin，全文见 `PROMPT.md`）',
            f'- 退出码：{agent["rc"]}；耗时：{agent["seconds"]} s'
            + ('（**超时被杀**）' if agent.get('timed_out') else ''),
            f'- 事件计数：`{json.dumps(agent["events"], ensure_ascii=False)}`',
            f'- 读到 skill 文档：{"是" if agent["skill_files_touched"] else "否"}'
            + (f'（{len(agent["skill_files_touched"])} 处）'
               if agent['skill_files_touched'] else ''),
            f'- 执行的命令数：{len(agent["commands"])}',
            f'- token 用量：`{json.dumps(agent.get("usage") or {}, ensure_ascii=False)}`',
            f'- 越界命令（工作区外找文档/实现/宿主进程）：'
            f'{len(agent.get("outside_hits") or [])} 条',
            '',
            *(('### 越界命令审计', '', '```json',
                json.dumps(agent.get('outside_hits') or [], ensure_ascii=False,
                           indent=2), '```', '')
              if agent.get('outside_hits') else ()),
            '### Agent 执行过的命令',
            '',
            '```console',
            *[f'$ {command}' for command in agent['commands'][:80]],
            '```',
            '',
            '### Agent 最终回答',
            '',
            '```markdown',
            clip(agent.get('last_message') or '(空)', 4000).rstrip(),
            '```',
            '',
        ]
        if agent.get('answer_file'):
            lines += [
                '### Agent 写入的 answer.md',
                '',
                '```markdown',
                clip(agent['answer_file'], 4000).rstrip(),
                '```',
                '',
            ]

    lines += ['## 执行记录', '']
    for index, step in enumerate(run.steps, 1):
        lines += [
            f'### {index}. {step.label}',
            '',
            '```console',
            f'$ {step.command}',
        ]
        output = (step.stdout or '') + (('stderr:\n' + step.stderr)
                                        if step.stderr.strip() else '')
        if output.strip():
            lines.append(clip(output).rstrip())
        lines += ['```', '',
                  f'cwd=`{step.cwd}` · exit={step.rc} · {step.seconds}s', '']

    tool_requests = run.tool_requests()
    probes = run.probe_requests()
    lines += [
        '## 夹具服务端请求（被测阶段）',
        '',
        f'判定只看**工具自己发出**的请求（`User-Agent: {ScenarioRun.TOOL_USER_AGENT}/*`，'
        '即 `oskm_runtime` 的 urllib 调用）；agent 为验证语义另起的 curl 探测'
        '单独列出，不参与契约判定。',
        '',
        f'### 工具请求（{len(tool_requests)} 条）',
        '',
        '```json',
        json.dumps(tool_requests, ensure_ascii=False, indent=2)
        if tool_requests else '[]',
        '```',
        '',
        f'### agent 自己的探测请求（{len(probes)} 条）',
        '',
        '```json',
        json.dumps(probes, ensure_ascii=False, indent=2) if probes else '[]',
        '```',
        '',
    ]
    for title, body in run.notes:
        lines += [f'## {title}', '', body, '']

    if run.agent is not None:
        outside = run.agent.get('outside_hits') or []
        run.check(
            '执行过程未越界（没有去工作区外找文档/实现/评估器）',
            not outside,
            json.dumps(outside[:5], ensure_ascii=False) if outside
            else '所有命令都落在工作区、夹具与临时 CODEX_HOME 内')
    auto = [check for check in run.checks if check.kind == 'auto']
    manual = [check for check in run.checks if check.kind == 'manual']
    passed = sum(1 for check in auto if check.ok)
    lines += [
        '## 断言结果',
        '',
        f'自动断言 {passed}/{len(auto)} 通过'
        + (f'；人工断言 {len(manual)} 条' if manual else ''),
        '',
        '| # | 断言 | 类型 | 结果 | 证据 |',
        '|---:|---|---|---|---|',
    ]
    for index, check in enumerate(run.checks, 1):
        verdict = ('Pass' if check.ok else 'Fail') if check.kind == 'auto' else '人工'
        evidence = check.evidence.replace('\n', ' ').replace('|', '\\|')
        name = check.name.replace('|', '\\|')
        lines.append(f'| {index} | {name} | {check.kind} | {verdict} | '
                     f'{clip(evidence, 400)} |')
    lines += ['', f'**结论：{"PASS" if passed == len(auto) else "FAIL"}**', '']
    return '\n'.join(lines)


def scenario_summary(run) -> dict:
    auto = [check for check in run.checks if check.kind == 'auto']
    passed = sum(1 for check in auto if check.ok)
    return {
        'id': run.scenario['id'],
        'name': run.scenario['name'],
        'arm': run.arm,
        'started': run.started,
        'finished': now(),
        'auto_passed': passed,
        'auto_total': len(auto),
        'manual_total': len(run.checks) - len(auto),
        'verdict': 'PASS' if passed == len(auto) else 'FAIL',
        'failed_checks': [check.name for check in auto if not check.ok],
        'requests': len(run.requests()),
        'tool_requests': len(run.tool_requests()),
        'probe_requests': len(run.probe_requests()),
        'steps': len(run.steps),
        'agent': ({
            'rc': run.agent['rc'],
            'seconds': run.agent['seconds'],
            'commands': len(run.agent['commands']),
            'tokens': (run.agent.get('usage') or {}).get('input_tokens', 0) +
                      (run.agent.get('usage') or {}).get('output_tokens', 0),
            'usage': run.agent.get('usage'),
            'skill_docs_read': bool(run.agent['skill_files_touched']),
            'outside_hits': len(run.agent.get('outside_hits') or []),
        } if run.agent else None),
    }


# ---------------------------------------------------------------- 编排

def run_one(entry, meta, *, arm, workdir, fixtures, home, python, codex,
            timeout, source_root, runs_dir):
    scenario_id, name, function = entry
    ws = Path(workdir) / arm / f'e{scenario_id:02d}-{name}'
    if ws.exists():
        shutil.rmtree(ws)
    ws.mkdir(parents=True)
    server = FixtureServer(fixtures, ws / 'server-requests.jsonl').start()
    scenario = dict(meta)
    scenario.update({'id': scenario_id, 'name': name})
    run = ScenarioRun(scenario=scenario, arm=arm, workdir=ws,
                      fixtures=fixtures, server=server, python=python,
                      codex=codex, home=home, timeout=timeout,
                      source_root=source_root, arm_root=workdir)
    try:
        function(run)
    except Exception as exc:  # noqa: BLE001 - 转录里要留下真实失败
        run.check('场景执行未抛异常', False, f'{type(exc).__name__}: {exc}')
    finally:
        server.stop()
    transcript = render_transcript(run, meta, workdir)
    output = Path(runs_dir) / arm / f'{scenario_id:02d}-{name}.md'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(transcript, encoding='utf-8')
    summary = scenario_summary(run)
    summary['transcript'] = str(output.relative_to(EVALS_DIR))
    summary['workspace'] = str(ws)
    return summary


def live_smoke(args, workdir: Path, source_root: Path) -> int:
    """真连一次 CI 端点：装运行时 → 直接调 CLI 查询 → 校对工具索引。"""
    python = args.python
    home = workdir / 'home'
    (home / '.codex').mkdir(parents=True, exist_ok=True)
    runtime = workdir / 'live-runtime'
    runtime.mkdir(parents=True, exist_ok=True)

    endpoint = args.live_endpoint or os.environ.get('OSKM_DOWNLOAD_ENDPOINT')
    source = args.live_source or os.environ.get('OSKM_DOWNLOAD_SOURCE')
    if not endpoint or not source:
        real_env = Path.home() / '.oskm' / '.env'
        values = {}
        if real_env.is_file():
            for line in real_env.read_text(encoding='utf-8').splitlines():
                key, sep, value = line.strip().partition('=')
                if sep and key.strip() in ('OSKM_DOWNLOAD_SOURCE',
                                           'OSKM_DOWNLOAD_ENDPOINT'):
                    values[key.strip()] = value.strip()
        endpoint = endpoint or values.get('OSKM_DOWNLOAD_ENDPOINT')
        source = source or values.get('OSKM_DOWNLOAD_SOURCE', 'OPENHARMONY_CI')
    if not endpoint:
        raise SystemExit('缺少端点：用 --live-endpoint 或 OSKM_DOWNLOAD_ENDPOINT')
    date = args.live_date or TODAY
    env = {'PATH': os.environ.get('PATH', '/usr/bin:/bin'),
           'HOME': str(home), 'CODEX_HOME': str(home / '.codex'),
           'OSKM_RUNTIME_ROOT': str(runtime),
           'OSKM_DOWNLOAD_SOURCE': source,
           'OSKM_DOWNLOAD_ENDPOINT': endpoint,
           'PYTHONDONTWRITEBYTECODE': '1'}
    run = ScenarioRun(
        scenario={'id': 0, 'name': 'live-smoke',
                  'prompt': f'用真实 {source} 端点装 date={date} 的运行时并查询',
                  'expected_output': '安装成功、CLI 可查、工具索引与 CLI 一致',
                  'assertions': []},
        arm='live-smoke', workdir=workdir, fixtures=None, server=None,
        python=python, codex=args.codex, home=home, timeout=args.timeout,
        source_root=source_root, arm_root=workdir)

    def sh(label, command, **kwargs):
        return run.sh(label, command, env=kwargs.pop('env', env), **kwargs)

    sh('doctor', bootstrap_cmd(run, 'doctor'), cwd=workdir)
    sh(f'install --source {source} --date {date}',
       bootstrap_cmd(run, '--runtime-root', runtime, 'install',
                     '--source', source, '--date', date),
       cwd=workdir, expect=0, timeout=args.timeout)
    sh('状态文件', f'cat {q(runtime / STATE_NAME)}', cwd=workdir)
    sh('运行时体积', f'du -sh {q(runtime)} && find {q(runtime)} -maxdepth 2 -type d | sort',
       cwd=workdir)
    sh('CLI 版本', quote_command([python, runtime / CLI_NAME, '--version']),
       cwd=workdir, expect=0)
    scan = sh('ask get_scan_info',
              quote_command([python, runtime / CLI_NAME, '--db',
                             runtime / DB_NAME, 'ask', 'get_scan_info']),
              cwd=workdir, expect=0)
    overview = sh('arch overview',
                  quote_command([python, runtime / CLI_NAME, '--db',
                                 runtime / DB_NAME, 'arch', 'overview']),
                  cwd=workdir, expect=0)
    listing = sh('ask --list（统计工具数）',
                 quote_command([python, runtime / CLI_NAME, '--db',
                                runtime / DB_NAME, 'ask', '--list']) +
                 ' | tee /dev/stderr | grep -cE "^ {3,4}\\*?[a-z_]+"',
                 cwd=workdir)
    markdown = sh('ask --list --markdown（生成工具索引）',
                  quote_command([python, runtime / CLI_NAME, '--db',
                                 runtime / DB_NAME, 'ask', '--list',
                                 '--markdown']) + f' > {q(workdir / "tools-regen.md")}',
                  cwd=workdir, expect=0)
    diff = sh('与 references/tools.md 逐行对比',
              f'diff <(grep "^| `" {q(SKILL_ROOT / "references" / "tools.md")}) '
              f'<(grep "^| `" {q(workdir / "tools-regen.md")}) && echo IDENTICAL',
              cwd=workdir)

    try:
        info = json.loads(scan.stdout)
        product = info.get('product')
    except (json.JSONDecodeError, ValueError):
        product = None
    try:
        counts = json.loads(overview.stdout).get('counts', {})
    except (json.JSONDecodeError, ValueError):
        counts = {}
    run.check('安装成功且状态文件记录 source/date',
              (state_document(runtime) or {}).get('date') == date,
              json.dumps(state_document(runtime) or {}, ensure_ascii=False)[:300])
    run.check('CLI 能读出扫描元数据', product is not None,
              f'product={product}')
    run.check('arch overview 返回真实计数', bool(counts),
              json.dumps(counts, ensure_ascii=False))
    run.check('references/tools.md 与 CLI 生成的索引逐行一致',
              'IDENTICAL' in diff.stdout, diff.stdout.strip()[:200] or diff.stderr[:200])
    run.note('环境', f'- 端点：`{endpoint}`\n- 下载方式：`{source}`\n'
                     f'- 日期：`{date}`\n- 运行时根：`{runtime}`（隔离 HOME，'
                     '不碰开发者自己的 `~/.oskm`）')

    output = Path(args.runs_dir) / 'live-smoke.md'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_transcript(run, run.scenario, workdir),
                      encoding='utf-8')
    summary = scenario_summary(run)
    summary['transcript'] = str(output.relative_to(EVALS_DIR))
    (Path(args.runs_dir) / 'live-smoke-summary.json').write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'live-smoke: {summary["verdict"]} '
          f'({summary["auto_passed"]}/{summary["auto_total"]}) → {output}')
    return 0 if summary['verdict'] == 'PASS' else 1


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description='Run the release evals for real and record transcripts.')
    parser.add_argument('--arm', choices=('scripted', 'with-skill',
                                          'without-skill'), default='scripted')
    parser.add_argument('--only', type=int, action='append',
                        help='只跑指定场景 id（可重复）')
    parser.add_argument('--jobs', type=int, default=1)
    parser.add_argument('--workdir', type=Path,
                        help='夹具与临时工作区（默认在系统临时目录下保留）')
    parser.add_argument('--runs-dir', type=Path, default=RUNS_DIR)
    parser.add_argument('--python', default=sys.executable)
    parser.add_argument('--codex', default=shutil.which('codex') or 'codex')
    parser.add_argument('--codex-config', type=Path,
                        default=Path.home() / '.codex' / 'config.toml')
    parser.add_argument('--timeout', type=int, default=900,
                        help='agent 臂单场景超时（秒）')
    parser.add_argument('--live-smoke', action='store_true',
                        help='真连 CI 端点装一次运行时并查询')
    parser.add_argument('--live-source')
    parser.add_argument('--live-endpoint')
    parser.add_argument('--live-date')
    args = parser.parse_args(argv)

    source_root = find_source_root()
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S')  # 仅用于报告标注
    label = 'live-smoke' if args.live_smoke else args.arm
    workdir = Path(args.workdir) if args.workdir else Path(tempfile.mkdtemp(
        prefix=f'oskm-eval-{label}-'))
    workdir.mkdir(parents=True, exist_ok=True)

    if args.live_smoke:
        return live_smoke(args, workdir, source_root)

    if args.arm != 'scripted' and not shutil.which(args.codex):
        raise SystemExit(f'找不到 codex 可执行文件：{args.codex}')

    fixtures = build_fixtures(workdir, source_root)
    home = prepare_home(workdir, args.arm, args.codex_config)
    metas = load_evals()
    selected = [entry for entry in SCENARIOS
                if not args.only or entry[0] in args.only]

    print(f'==> arm={args.arm} workdir={workdir} python={args.python}')
    print(f'==> fixtures: cli={fixtures.cli.name}'
          f'({fixtures.facts["cli_bytes"]}B) db={fixtures.db.name} '
          f'archive={fixtures.good_archive.name}')

    def execute(entry):
        meta = metas.get(entry[0])
        if meta is None:
            raise SystemExit(f'evals.json 缺少场景 {entry[0]}')
        return run_one(entry, meta, arm=args.arm, workdir=workdir,
                       fixtures=fixtures, home=home, python=args.python,
                       codex=args.codex, timeout=args.timeout,
                       source_root=source_root, runs_dir=args.runs_dir)

    if args.jobs > 1 and len(selected) > 1:
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            summaries = list(pool.map(execute, selected))
    else:
        summaries = [execute(entry) for entry in selected]

    summaries.sort(key=lambda item: item['id'])
    output_dir = Path(args.runs_dir) / args.arm
    summary_path = output_dir / 'summary.json'
    previous = {}
    reruns = []
    if args.only and summary_path.is_file():
        # 单场景重跑：把新结果并回原来的 summary，别把它冲成"只跑了一个场景"。
        try:
            previous_doc = json.loads(summary_path.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            previous_doc = {}
        previous = {item['id']: item
                    for item in previous_doc.get('scenarios', [])}
        reruns = list(previous_doc.get('partial_reruns', []))
        for item in summaries:
            reruns.append({'id': item['id'], 'at': item['finished'],
                           'workdir': item['workspace']})
        merged = dict(previous)
        merged.update({item['id']: item for item in summaries})
        summaries = [merged[key] for key in sorted(merged)]
    document = {
        'arm': args.arm,
        'skill': SKILL_NAME,
        'version': SKILL_VERSION,
        'generated_at': now(),
        'python': args.python,
        'codex': (args.codex if args.arm != 'scripted' else None),
        'source_root': str(source_root),
        'workdir': str(workdir),
        'fixtures': fixtures.facts,
        'scenarios': summaries,
        'passed': sum(1 for item in summaries if item['verdict'] == 'PASS'),
        'total': len(summaries),
        'partial_reruns': reruns,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8')

    print()
    for item in summaries:
        agent = item['agent']
        suffix = ''
        if agent:
            suffix = (f" agent_rc={agent['rc']} {agent['seconds']}s "
                      f"cmds={agent['commands']} "
                      f"tokens={agent['tokens']} "
                      f"skill_docs={'yes' if agent['skill_docs_read'] else 'no'}")
        print(f"E{item['id']:02d} {item['name']:<38} {item['verdict']:<4} "
              f"{item['auto_passed']}/{item['auto_total']} 自动断言"
              f"（{item['manual_total']} 条人工）{suffix}")
    print(f"\n==> {document['passed']}/{document['total']} 场景通过；"
          f'转录在 {output_dir}')
    return 0 if document['passed'] == document['total'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
