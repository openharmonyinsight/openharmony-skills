"""托管运行时的状态文件、廉价刷新判定与退避标记。

**只碰状态，不碰网络。** 下载与安装在 `db_download.py` / `install.py`，
CLI 的定位在 `cli_install.py`。

这里最重要的一条决定是 `needs_refresh()` **只做廉价检查**：状态结构、日期、
文件存在、SDK 目录非空、SQLite 能打开且 `scans` 可读。
旧实现在这条路径上调 `schema_problem()`，于是每次查询都对 19 MB 库跑一遍
`PRAGMA integrity_check`——而库是 `install` 校验通过后才原子落盘的，之后没有
任何代码路径会改它。完整的表/列契约校验仍在 `install` 落盘前和显式
`validate-db` 时执行（都由 CLI 的 `oskm_cli.database` 提供），一处都没少。
理由与影响见 `docs/architecture/cli-skill-split.md` §5.3。

**调用方只有 `bootstrap.py refresh` 一处。** 早先它挂在每次查询前（查询透传
时代），那时还需要一个 15 分钟的失败退避标记，免得端点挂掉时每条命令都去
试一次下载。透传删掉之后刷新是**用户显式要求**的动作，退避没有意义，
`.oskm-refresh-retry` 一并删除。
"""

from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import tempfile
from datetime import datetime
from pathlib import Path


STATE_NAME = '.oskm-runtime.json'
MINIMUM_PYTHON = (3, 10)
SDK_PATHS = {
    'sdk-js': 'interface/sdk-js',
    'sdk_c': 'interface/sdk_c',
}
# version 3 相比 2 多了 `cli` 段（记录了装的是哪个 oskm-cli）。
# version 2 的状态文件必须仍能读：缺 `cli` 只表示"CLI 还没装到这个根目录"，
# 由 `cli_install.ensure_cli()` 单独补齐，**不触发 DB/SDK 重新下载**。
STATE_VERSION = 3
SQLITE_HEADER = b'SQLite format 3\x00'


def today() -> str:
    return datetime.now().astimezone().strftime('%Y%m%d')


def state_path(db_path) -> Path:
    return Path(db_path).expanduser().resolve().parent / STATE_NAME


def load_state(db_path) -> dict | None:
    path = state_path(db_path)
    if not path.is_file():
        return None
    try:
        state = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f'运行时状态文件不可读: {path}: {exc}') from exc
    if not isinstance(state, dict):
        raise ValueError(f'运行时状态文件格式错误: {path}')
    return state


def write_state(path, state: dict) -> None:
    """Atomically replace the state file (temp file + fsync + os.replace)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f'.{path.name}.tmp.', dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, 'w', encoding='utf-8') as stream:
            descriptor = -1
            json.dump(state, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        temporary.unlink(missing_ok=True)


def update_state(db_path, **changes) -> dict | None:
    """Merge fields into an existing state file; no-op when unmanaged."""
    path = state_path(db_path)
    state = load_state(db_path)
    if state is None:
        return None
    state.update(changes)
    write_state(path, state)
    return state


def artifact_path(root: Path, value: object) -> Path | None:
    if not isinstance(value, str) or not value:
        return None
    path = Path(value)
    return path if path.is_absolute() else Path(root) / path


def sha256(path) -> str:
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def database_is_usable(db_path) -> bool:
    """Cheap liveness probe: header magic + read-only open + `scans` readable.

    **故意不跑 `PRAGMA integrity_check`**，也不比表/列——那是 `install` 与
    `validate-db` 的职责（见模块 docstring）。这里要回答的只是"这个文件还在、
    还开得动吗"，用于决定要不要刷新以及刷新失败时旧库能不能继续用。
    """
    path = Path(db_path).expanduser()
    if not path.is_file():
        return False
    connection = None
    try:
        with path.open('rb') as stream:
            if stream.read(len(SQLITE_HEADER)) != SQLITE_HEADER:
                return False
        connection = sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)
        connection.execute('SELECT 1 FROM scans LIMIT 1').fetchone()
    except (OSError, sqlite3.Error, ValueError):
        return False
    finally:
        if connection is not None:
            connection.close()
    return True


def needs_refresh(db_path, *, current_date: str | None = None) -> bool:
    """Return whether a managed runtime is stale or incomplete.

    A database without a state file is an unmanaged input and is left alone for
    backwards compatibility with hand-made ``artifacts/*/knowledge.db`` files.

    The ``cli`` section is deliberately **not** part of this decision: a
    version-2 state file with a perfectly good DB and SDKs must not trigger a
    full re-download just because the CLI artifact was introduced later.
    ``cli_install.ensure_cli()`` handles that separately and idempotently.
    """
    current = current_date if current_date is not None else today()
    db_path = Path(db_path).expanduser().resolve()
    state = load_state(db_path)
    if state is None:
        return False

    root = db_path.parent
    db = state.get('db')
    sdk = state.get('sdk')
    if not isinstance(db, dict) or not isinstance(sdk, dict):
        return True
    is_local = state.get('source') == 'local'
    if not is_local and (db.get('date') != current or sdk.get('date') != current):
        return True

    db_file = artifact_path(root, db.get('path'))
    if db_file is None or not db_file.is_file():
        return True
    if not database_is_usable(db_file):
        return True
    for name in SDK_PATHS:
        item = sdk.get(name)
        if not isinstance(item, dict):
            return True
        sdk_dir = artifact_path(root, item.get('path'))
        if sdk_dir is None or not sdk_dir.is_dir():
            return True
        if not any(sdk_dir.iterdir()):
            return True
    return False
