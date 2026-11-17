"""`bootstrap.py doctor`：一次把"为什么装不上"讲清楚。

doctor 的价值全在**它检查的顺序**：Python → 配置 → CLI 产物 → 运行时状态。
按这个顺序报，第一个 FAIL 通常就是根因；反过来先报"数据库不存在"的话，
使用者会去查一个其实是 CLI 没装上的问题。
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

from . import cli_install, state
from .environment import RUNTIME_MODULES_HINT, download_configuration


def _report_python() -> bool:
    version = '.'.join(str(part) for part in sys.version_info[:3])
    if sys.version_info >= state.MINIMUM_PYTHON:
        print(f'Python: {version} (OK, requires Python 3.10+)')
        return True
    print(f'Python: {version} (FAIL: requires Python 3.10+)')
    return False


def _report_modules() -> bool:
    """skill 自己的包 + CLI 产物里的包，都要能 import。"""
    ready = True
    names = []
    for name in RUNTIME_MODULES_HINT:
        try:
            importlib.import_module(name)
        except (ImportError, RuntimeError, TypeError) as exc:
            names.append(f'{name} (FAIL: {exc})')
            ready = False
        else:
            names.append(f'{name} (OK)')
    print('Modules: ' + ', '.join(names))
    if not ready:
        print('        提示: 先 cd 到 skill 目录；或在任意目录设置 '
              'PYTHONPATH=<skill 目录>。')
    return ready


def _report_cli(root: Path) -> bool:
    try:
        location = cli_install.resolve_cli(root, allow_download=False)
    except (cli_install.CliInstallError, ValueError) as exc:
        print(f'CLI: FAIL: {exc}')
        return False
    print(f'CLI: {location.describe()}')
    # 让 `oskm_cli` / `oskm_schema` 真的可 import，_report_modules 才校得动。
    cli_install.activate(location)
    return True


def runtime_is_complete(root: Path) -> bool:
    """DB 可打开且两套 SDK 目录非空——即"已经能查询了"。

    这个判断决定"下载端点没配"算 FAIL 还是 WARN：什么都还没装的时候它是
    硬故障（install 必然失败）；已经装好的时候它只影响下一次按日期刷新，
    查询完全可用。旧实现一律报 FAIL，于是一个能正常工作的只读环境被
    doctor 判成"未就绪"——那句话会让人去修一个根本没坏的东西。
    """
    db_path = Path(root) / 'knowledge.db'
    if not state.database_is_usable(db_path):
        return False
    for relative in state.SDK_PATHS.values():
        directory = Path(root) / relative
        if not directory.is_dir() or not any(directory.iterdir()):
            return False
    return True


def _hint_local_runtime_candidate() -> None:
    """Point at a reusable source-tree build when the runtime is missing."""
    from . import install
    try:
        local = install.find_local_runtime()
    except Exception:
        return
    if local is not None:
        print(f'提示: 检测到源码根本地构建: {local.db_path}')
        print('      在源码根或其子目录执行 bootstrap.py install，或传 '
              '--source-root <path>，将优先使用本地构建，不联网。')


def _report_runtime(root: Path) -> bool:
    print(f'Runtime root: {root}')
    db_path = root / 'knowledge.db'
    if not db_path.is_file():
        print('Runtime state: 未安装（没有 knowledge.db）；'
              '执行 bootstrap.py install 安装')
        _hint_local_runtime_candidate()
        # 没装不是"环境坏了"，doctor 仍然算 ready，install 会去装。
        return True
    try:
        document = state.load_state(db_path)
    except ValueError as exc:
        print(f'Runtime state: FAIL: {exc}')
        return False
    if document is None:
        print('Runtime state: 非托管（没有 .oskm-runtime.json），'
              '`bootstrap.py refresh` 不会碰它')
        return True
    marks = []
    for label, key in (('db', 'db'), ('sdk', 'sdk'), ('cli', 'cli')):
        marks.append(f'{label}={"✓" if isinstance(document.get(key), dict) else "✗"}')
    print(f"Runtime state: version {document.get('version')}, "
          f"date {document.get('date')}, source {document.get('source')}, "
          + ', '.join(marks))
    if not state.database_is_usable(db_path):
        print('Runtime database: FAIL: 打不开或不是 SQLite 文件')
        return False
    print('Runtime database: 可打开（廉价检查；完整 schema 契约用 '
          'bootstrap.py validate-db）')
    return True


def check_environment(root=None) -> bool:
    """Print a cross-platform readiness report; return overall readiness."""
    root = cli_install.default_runtime_root(root)
    ready = _report_python()

    # 先算运行时是否已完整，再决定下载配置缺失算 FAIL 还是 WARN。
    complete = runtime_is_complete(root)
    config_valid, config_state = download_configuration()
    print(f'Source / Endpoint: {config_state}')
    if not config_valid:
        hint = ('请在 <runtime-root>/.env 或 skill 的 oskm_runtime/.env 中配置 '
                'OSKM_DOWNLOAD_ENDPOINT；OSKM_DOWNLOAD_SOURCE 可选，'
                '默认 OPENHARMONY_CI。')
        if complete:
            print(f'        WARN: 下载配置无效，安装与按日期刷新会失败；'
                  f'但运行时已完整，查询可用。{hint}')
        else:
            print(f'        FAIL: 下载配置无效。{hint}')
            ready = False

    # CLI 先报：它把 oskm_cli 放上 sys.path，模块检查才有意义。
    ready = _report_cli(root) and ready
    ready = _report_modules() and ready
    ready = _report_runtime(root) and ready
    print('提示: 运行时来自单个 knowledge.tar.gz——里面就是 knowledge.db + '
          f'{cli_install.ARTIFACT_NAME} + 两套 SDK，install 一次装齐；'
          '不要求 Git。CLI 按三级候选解析'
          f'（$OSKM_CLI → 源码树 → <runtime-root>/{cli_install.ARTIFACT_NAME}），'
          '全程不单独下载 CLI。')
    print('提示: bootstrap.py 不跑查询。查询直接调 '
          f'<runtime-root>/{cli_install.ARTIFACT_NAME} --db '
          '<runtime-root>/knowledge.db …')
    if not ready:
        print('错误: 运行时依赖检查未通过。')
    return ready


def main(argv=None) -> int:
    root = argv[0] if argv else None
    return 0 if check_environment(root) else 1
