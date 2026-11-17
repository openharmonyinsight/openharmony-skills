"""定位、校验、下载并载入 **oskm-cli** 产物。

skill 归档里**不包含查询引擎**（2.5.6 时代打包整个 `agentic/`），所以
"CLI 从哪来"是 skill 的一项职责。三级候选，按序尝试，第一个命中的就用：

1. `$OSKM_CLI`                    显式给定的 `.pyz` 或源码目录
2. **源码树**                     从本文件向上找 `cli/oskm_cli/__init__.py`
3. `<runtime-root>/oskm-cli.pyz`  `install` 从 `knowledge.tar.gz` 里解出来的那一份

源码树存在时优先用源码树，便于采集器、CLI 与 skill 同一工作区联调；发布包里
没有 CLI 源码，于是自然回退到已安装产物。

**CLI 不单独下载。** 它和 `knowledge.db` 一起打在 `knowledge.tar.gz` 里
（归档根目录有 `knowledge.db`、`oskm-cli.pyz`、`interface/sdk-js`、
`interface/sdk_c`），由 `install` 一起落盘。所以这里只有三级候选、三步都不联网；
曾经的 `$OSKM_CLI_ENDPOINT` 单独下载通道已删除。

## CLI 与 `knowledge.db` 同类：**不记版本、不锁摘要**

固定文件名 `oskm-cli.pyz`，装在 `<runtime-root>/` 下与 `knowledge.db` 并排。
于是文档与调用方始终不用钉版本号，`install` 也不用维护一份会漂的 pin。

完整性校验因此是**结构性**的（`verify_pyz()`：shebang + 是 zip + 有
`__main__.py` 与 `oskm_cli/cli.py` + CRC 完好），与 DB 那侧的 `verify_sqlite()`
（文件头 + `PRAGMA integrity_check`）是同一思路：**校它是不是一个能用的产物**，
而不是校它是不是某一次构建的那一份。摘要只写进状态文件当**出处记录**
（`cli.sha256`），与 `db.sha256` 一样，不作为期望值。

版本仍然可查：`oskm-cli --version`、`bootstrap.py cli-path`（报告实际用了
哪一个候选）、`doctor`。想让某个特定构建生效，用 `$OSKM_CLI` 显式指过去。

> 曾经有过 `cli_pin.json`（version + sha256）与"源码树版本必须等于 pin，
> 否则硬失败"这两条机制，2026-11-12 删掉。它们防的是"开发时源码树与已装产物
> 漂移"，但代价是每次改 `oskm_cli/**` 都要重跑 `--update-pin`，而失败信息
> 指向一个与改动毫无关系的摘要——实测踩到过（改的是一句注释）。
> 与 DB 对齐之后这个问题不存在了：谁在 `<runtime-root>/` 里，就用谁。

载入方式是**同进程** `sys.path` + `importlib.import_module('oskm_cli.cli')`，
不再起一个解释器：省掉每次调用 100–200 ms 的启动开销。CLI 仍然是能独立
`python3 oskm-cli.pyz …` 运行的完整产物，这一点没有变。
"""

from __future__ import annotations

import importlib
import json
import os
import re
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path

from . import state
from .db_download import DownloadError
from .environment import CLI_PATH_ENV


# 固定名，不带版本（与 knowledge.db 同类）。
ARTIFACT_NAME = 'oskm-cli.pyz'
# 源码树里 CLI 包的相对位置（用于向上探测 packages/oskm）。
SOURCE_LAYOUT = Path('cli') / 'oskm_cli' / '__init__.py'
_VERSION_RE = re.compile(r"^__version__\s*=\s*['\"]([^'\"]+)['\"]", re.M)
# verify_pyz 要看到的条目：少一个就不是一个能跑的 CLI。
REQUIRED_MEMBERS = ('__main__.py', 'oskm_cli/__init__.py', 'oskm_cli/cli.py')

ENV = 'env'
INSTALLED = 'installed'
SOURCE = 'source'
DOWNLOADED = 'downloaded'


class CliInstallError(RuntimeError):
    """A user-actionable failure to obtain the oskm-cli artifact."""


@dataclass(frozen=True)
class CliLocation:
    """Where the CLI was found and what to put on ``sys.path`` to import it."""

    path: Path
    kind: str
    version: str
    sys_path: tuple[str, ...]

    def describe(self) -> str:
        return f'{self.path} ({self.kind}, oskm-cli {self.version})'


def artifact_name() -> str:
    return ARTIFACT_NAME


def installed_path(runtime_root) -> Path:
    """`<runtime-root>/oskm-cli.pyz` —— 与 `knowledge.db` 并排。"""
    return Path(runtime_root).expanduser() / ARTIFACT_NAME


def verify_pyz(path) -> None:
    """Structural check, the CLI analogue of ``db_download.verify_sqlite``.

    校的是"这是一个能跑的 CLI 产物吗"，不是"它是某一次构建的那一份吗"。
    下载物被截断、被 HTML 错误页替换、或者根本不是 zipapp，都在这里挡住，
    而不是等到 import 时炸出一句看不懂的 ImportError。
    """
    path = Path(path)
    try:
        with path.open('rb') as stream:
            head = stream.read(2)
    except OSError as exc:
        raise CliInstallError(f'CLI 产物不可读: {path}: {exc}') from exc
    if head != b'#!':
        raise CliInstallError(
            f'CLI 产物不是可执行 zipapp（缺少 shebang）: {path}')
    if not zipfile.is_zipfile(path):
        raise CliInstallError(f'CLI 产物不是有效 zip: {path}')
    try:
        with zipfile.ZipFile(path) as archive:
            broken = archive.testzip()
            if broken is not None:
                raise CliInstallError(f'CLI 产物 CRC 校验失败: {broken}')
            names = set(archive.namelist())
    except zipfile.BadZipFile as exc:
        raise CliInstallError(f'CLI 产物不是有效 zip: {path}: {exc}') from exc
    missing = [name for name in REQUIRED_MEMBERS if name not in names]
    if missing:
        raise CliInstallError(
            f'CLI 产物缺少必需条目 {missing}: {path}')


def pyz_version(path) -> str:
    """Read ``oskm_cli.__version__`` out of an installed pyz without running it."""
    try:
        with zipfile.ZipFile(Path(path)) as archive:
            source = archive.read('oskm_cli/__init__.py').decode('utf-8')
    except (OSError, KeyError, zipfile.BadZipFile, UnicodeDecodeError):
        return 'unknown'
    match = _VERSION_RE.search(source)
    return match.group(1) if match else 'unknown'


def _source_version(init_file: Path) -> str:
    match = _VERSION_RE.search(Path(init_file).read_text(encoding='utf-8'))
    return match.group(1) if match else 'unknown'


def find_source_tree(start: Path | None = None) -> Path | None:
    """Walk up from ``start`` looking for ``cli/oskm_cli/__init__.py``."""
    current = Path(start if start is not None else Path(__file__)).resolve()
    for candidate in (current, *current.parents):
        if (candidate / SOURCE_LAYOUT).is_file():
            return candidate
    return None


def _location_from_env(raw: str) -> CliLocation | None:
    path = Path(raw).expanduser()
    if path.is_file() and path.suffix == '.pyz':
        verify_pyz(path)
        return CliLocation(path=path, kind=ENV, version=pyz_version(path),
                           sys_path=(str(path),))
    init = path / SOURCE_LAYOUT
    if init.is_file():
        return CliLocation(
            path=path, kind=ENV, version=_source_version(init),
            sys_path=(str(path / 'cli'), str(path)))
    return None


def _location_from_installed(runtime_root: Path) -> CliLocation | None:
    path = installed_path(runtime_root)
    if not path.is_file():
        return None
    verify_pyz(path)
    return CliLocation(path=path, kind=INSTALLED, version=pyz_version(path),
                       sys_path=(str(path),))


def _location_from_source() -> CliLocation | None:
    root = find_source_tree(Path(__file__))
    if root is None:
        return None
    return CliLocation(path=root, kind=SOURCE,
                       version=_source_version(root / SOURCE_LAYOUT),
                       sys_path=(str(root / 'cli'), str(root)))


def default_runtime_root(runtime_root=None) -> Path:
    """`--runtime-root` > `$OSKM_RUNTIME_ROOT` > `~/.oskm`."""
    from .environment import runtime_root as configured
    return Path(configured(runtime_root)).expanduser().resolve()


def resolve_cli(runtime_root=None, *, allow_download: bool = True) -> CliLocation:
    """Return the first usable CLI location, or raise with every attempt."""
    root = default_runtime_root(runtime_root)
    attempts: list[str] = []

    override = os.environ.get(CLI_PATH_ENV, '').strip()
    if override:
        try:
            location = _location_from_env(override)
        except CliInstallError as exc:
            attempts.append(f'1. ${CLI_PATH_ENV}={override} —— {exc}')
            location = None
        if location is not None:
            return location
        if not attempts:
            attempts.append(f'1. ${CLI_PATH_ENV}={override} —— 不是 .pyz 文件，'
                            f'也不是含 {SOURCE_LAYOUT.as_posix()} 的源码树')
    else:
        attempts.append(f'1. ${CLI_PATH_ENV} 未设置')

    location = _location_from_source()
    if location is not None:
        return location
    attempts.append('2. 源码树 —— 向上没找到 ' + SOURCE_LAYOUT.as_posix())

    installed = installed_path(root)
    try:
        location = _location_from_installed(root)
    except CliInstallError as exc:
        # 文件在但不是个能用的产物：比"不存在"更值得原样报出来。
        attempts.append(f'3. {installed} —— {exc}')
        location = None
    else:
        if location is None:
            attempts.append(f'3. {installed} —— 不存在')
    if location is not None:
        return location

    raise CliInstallError(
        '找不到可用的 oskm-cli 产物。它随 knowledge.tar.gz 一起发布，'
        '所以正常情况下 `bootstrap.py install` 会把它装到 '
        f'{installed}。已尝试：\n  ' + '\n  '.join(attempts) +
        '\n可行做法：\n'
        '  · 跑 `bootstrap.py install` 从运行时归档里装（含 CLI）\n'
        f'  · 或在源码仓构建后手动复制：python3 cli/scripts/build_cli.py，'
        f'再把 cli/dist/{ARTIFACT_NAME} 放到 {installed}\n'
        f'  · 或用 {CLI_PATH_ENV} 直接指向一个 .pyz / 源码树')


def ensure_cli(runtime_root=None, *, record: bool = True) -> CliLocation:
    """Resolve the CLI, and record its provenance when we installed it."""
    root = default_runtime_root(runtime_root)
    location = resolve_cli(root)
    if record and location.kind in (INSTALLED, DOWNLOADED):
        db_path = root / 'knowledge.db'
        if state.state_path(db_path).is_file():
            state.update_state(
                db_path,
                cli={'path': location.path.name,
                     'sha256': state.sha256(location.path)})
    return location


def activate(location: CliLocation) -> CliLocation:
    """Make a resolved CLI location win over anything activated earlier.

    必须**移到最前**，不能"没有才插入"：同一次进程里先后解析两个不同的 CLI
    （典型场景——install 用归档自带的那个校验，之后 validate-db 用装好的那个）
    时，先激活的路径会一直留在 `sys.path` 里。只在缺失时插入的话，后激活的
    源码树会排在一个更早的临时 pyz **后面**，清掉模块缓存后又被那个 pyz 抢回
    导入权，症状是 `No module named 'oskm_cli.database'` 而报的路径是后一个。
    """
    for entry in reversed(location.sys_path):
        while entry in sys.path:
            sys.path.remove(entry)
        sys.path.insert(0, entry)
    # zipimport 会缓存目录列表；刚下载的 pyz 必须让它重新看一眼。
    importlib.invalidate_caches()
    return location


def _evict_cached_package(location: CliLocation) -> None:
    """Drop a cached ``oskm_cli`` that came from a *different* location.

    `sys.path` 只在导入**之前**生效：一旦 `oskm_cli` 进了 `sys.modules`，
    再插一条新路径也不会换包。这在同一次进程里换 CLI 时会静默用错的版本——
    实测踩过：先加载测试夹具里的裁剪 pyz，再切到真 pyz，`oskm_cli.database`
    就报 `No module named`，而错误信息指向的是**真 pyz 的路径**，完全误导。

    所以换 location 之前先把旧的 `oskm_cli*` 清掉。只清这一个包的缓存，
    不动 `oskm_schema`（它两个产物共用同一份）。
    """
    if not sys.modules.get('oskm_cli'):
        return
    origin = str(getattr(sys.modules['oskm_cli'], '__file__', '') or '')
    if any(origin.startswith(root) for root in location.sys_path):
        return
    for name in [m for m in sys.modules
                 if m == 'oskm_cli' or m.startswith('oskm_cli.')]:
        del sys.modules[name]


def load_cli_module(name: str, location: CliLocation | None = None,
                    runtime_root=None):
    """Import ``oskm_cli.<name>`` from a resolved location."""
    location = activate(location or resolve_cli(runtime_root))
    _evict_cached_package(location)
    try:
        return importlib.import_module(f'oskm_cli.{name}')
    except ImportError as exc:
        raise CliInstallError(
            f'CLI 产物无法导入 oskm_cli.{name}: {location.path}: {exc}') from exc


def load_cli(location: CliLocation | None = None, runtime_root=None):
    """The query CLI module (``oskm_cli.cli``)."""
    return load_cli_module('cli', location, runtime_root)


def load_database(location: CliLocation | None = None, runtime_root=None):
    """The CLI's schema-contract module (``oskm_cli.database``).

    `install` 用它校验下载物。**skill 不复制那份表/列清单**——契约只有
    CLI 一处，否则改一张表就要同时想到两个地方。
    """
    return load_cli_module('database', location, runtime_root)


def cli_path(runtime_root=None) -> Path:
    """The CLI artifact location, as reported by ``bootstrap.py cli-path``."""
    return resolve_cli(runtime_root).path


def state_entry(location: CliLocation) -> dict:
    """The `cli` section of `.oskm-runtime.json` -- provenance, not a pin."""
    entry = {'path': location.path.name}
    if location.kind in (INSTALLED, DOWNLOADED):
        entry['sha256'] = state.sha256(location.path)
    return entry
