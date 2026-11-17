"""skill 的唯一入口：**只负责装，不负责查**。

    doctor      检查 Python、配置、CLI 与运行时状态
    install     安装或刷新 DB + 两套 SDK + CLI
    refresh     廉价检查，过期才重装（install 的幂等版）
    update-cli  只补齐/更换 CLI 产物
    download-db 只下载指定日期的 knowledge.db
    validate-db 完整 schema 契约校验（转发给 CLI）
    cli-path    打印解析到的 CLI 位置

**查询命令不在这里。** 2026-11-12 之前 `bootstrap.py` 还把 `ask/arch/diff/sql`
透传给 CLI，并顺手注入 `--db <runtime-root>/knowledge.db`；现已删除。理由：

1. 它要求 bootstrap **手抄一份 CLI 的解析器知识**（哪些全局 flag 带取值、
   第一个位置参数在哪）。实测过漂移后果：假设 CLI 新增全局 `--profile NAME`，
   `bootstrap.py --profile sql arch overview` 会把 `sql` 当成子命令。
   这与被删掉的 `packages/oskm/oskm.py` 是同一类病。
2. skill 的职责是"把 CLI/DB/SDK 装到位并说明怎么用"，多一个查询入口就多一处
   会与 CLI 不一致的行为（退出码、`--db` 语义、错误文案）。
3. CLI 装在**固定名字** `<runtime-root>/oskm-cli.pyz` 上，所以文档可以直接写
   完整调用，不必靠 bootstrap 缩短命令，也不会钉住版本号。

查询一律直接调 CLI：

    python3 ~/.oskm/oskm-cli.pyz --db ~/.oskm/knowledge.db arch overview

`--runtime-root` 是 bootstrap 级的选项，可以从 argv 任意位置摘掉；摘掉之后
子命令解析器看到的就是干净的参数。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import cli_install, doctor, install, state
from .db_download import DownloadError, download_database
from .environment import (
    DOWNLOAD_SOURCES,
    download_source,
    load_env_files,
)


EXIT_OK = 0
EXIT_ERROR = 1
EXIT_USAGE = 2

MANAGED = ('doctor', 'install', 'refresh', 'update-cli', 'download-db',
           'validate-db', 'cli-path')

USAGE = """\
用法: python3 bootstrap.py [--runtime-root DIR] <命令>

本 skill 只负责**装**，不负责查。命令：

  doctor                                  检查 Python、配置、CLI 与运行时状态
  install [--source S] [--date YYYYMMDD]  安装或刷新 DB + 两套 SDK + CLI
          [--skip-db | --skip-sdk]
  refresh [--source S] [--date YYYYMMDD]  只在过期时重装（install 的幂等版）
  update-cli [--force]                    重新解析 CLI（例如从源码树取新的）
  download-db --date D --output PATH      只下载指定日期的 knowledge.db
  validate-db PATH                        完整 schema 契约校验（转发给 CLI）
  cli-path                                打印解析到的 CLI 位置

查询直接调 CLI（固定文件名，不带版本号）：

  python3 <runtime-root>/oskm-cli.pyz --db <runtime-root>/knowledge.db arch overview
  python3 <runtime-root>/oskm-cli.pyz --db <runtime-root>/knowledge.db ask --list
  python3 <runtime-root>/oskm-cli.pyz --help
"""


# ---------------------------------------------------------------- argv 处理

def pop_runtime_root(argv):
    """Remove every ``--runtime-root`` occurrence and return its last value."""
    rest, value, skip = [], None, False
    for token in argv:
        if skip:
            value = token
            skip = False
            continue
        if token == '--runtime-root':
            skip = True
            continue
        if token.startswith('--runtime-root='):
            value = token.split('=', 1)[1]
            continue
        rest.append(token)
    return value, rest


def first_command(argv):
    """The first non-flag token.

    不再需要"跳过带取值的全局 flag"那套逻辑：bootstrap 自己没有全局带值 flag
    （只有 `--runtime-root`，已在上一步摘掉），而子命令的 flag 都写在命令名
    **之后**。少一份手抄的 CLI 解析器知识，就少一处会漂的地方。
    """
    for token in argv:
        if not token.startswith('-'):
            return token
    return None


def resolve_root(explicit, argv=()) -> Path:
    """`--runtime-root` > `validate-db PATH` 的父目录 > `$OSKM_RUNTIME_ROOT` > `~/.oskm`。

    `validate-db` 那一支是必要的：它点名了一个库，而 CLI 就装在那个库旁边
    （`<root>/oskm-cli.pyz`）。不认它的话，`bootstrap.py validate-db
    /some/root/knowledge.db` 会退回 `~/.oskm` 找 CLI，然后报"找不到可用的
    oskm-cli 产物"——用户明明已经把路径写在命令里了（实测踩过）。
    """
    if explicit:
        return cli_install.default_runtime_root(explicit)
    tokens = list(argv)
    if tokens and tokens[0] == 'validate-db':
        for token in tokens[1:]:
            if not token.startswith('-'):
                return Path(token).expanduser().resolve().parent
    return cli_install.default_runtime_root(None)


# ---------------------------------------------------------------- 托管命令

def cmd_doctor(root: Path, argv) -> int:
    return doctor.main([str(root)])


def _install_arguments(prog: str, description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=prog, allow_abbrev=False,
                                     description=description)
    parser.add_argument('--source', choices=DOWNLOAD_SOURCES,
                        help='下载方式；默认读 OSKM_DOWNLOAD_SOURCE，'
                             '未配置时为 OPENHARMONY_CI')
    parser.add_argument('--date', help='YYYYMMDD；缺省取系统当天')
    parser.add_argument(
        '--source-root', default=None,
        help='OpenHarmony 源码根；指定后只优先使用该源码根的本地构建。'
             '不指定时从 cwd 向上探测最近的源码根')
    return parser


def _do_install(root: Path, args, *, skip_db: bool, skip_sdk: bool) -> int:
    try:
        source = args.source or download_source()
        source_root = (Path(args.source_root).expanduser()
                       if args.source_root else None)
        # 归档自带 CLI，所以没有"先装 CLI 再下载 DB"的必要，也没有单独的
        # CLI 下载端点（2026-11-12 之前有，已删）。
        install.install_runtime(
            root, source, args.date or state.today(),
            download_db=not skip_db, download_sdk=not skip_sdk,
            source_root=source_root,
        )
    except DownloadError as exc:
        print(f'错误: {exc}', file=sys.stderr)
        print('提示: 未检测到可用的源码根本地运行时。若源码根在别处，'
              '用 --source-root <path> 指定，或在源码根及其子目录执行 install。',
              file=sys.stderr)
        return EXIT_ERROR
    except (cli_install.CliInstallError, OSError, RuntimeError,
            ValueError) as exc:
        print(f'错误: {exc}', file=sys.stderr)
        return EXIT_ERROR
    return EXIT_OK


def cmd_install(root: Path, argv) -> int:
    parser = _install_arguments('bootstrap.py install',
                                '安装或刷新托管运行时（DB + 两套 SDK + CLI）')
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--skip-db', action='store_true')
    modes.add_argument('--skip-sdk', action='store_true')
    args = parser.parse_args(argv)
    return _do_install(root, args, skip_db=args.skip_db, skip_sdk=args.skip_sdk)


def cmd_refresh(root: Path, argv) -> int:
    """`install` 的幂等版：只有过期/不完整时才真的重装。

    查询透传删掉之后，"每次查询前顺手刷新"没有了触发点。与其让运行时静默
    停在旧日期，不如给一条**显式**命令：它跑的是同一套廉价检查
    （状态、日期、文件存在、SDK 非空、SQLite 可开且 `scans` 可读，
    **不跑 `PRAGMA integrity_check`**），过期才下载。
    """
    parser = _install_arguments('bootstrap.py refresh',
                                '只在运行时过期或不完整时重新安装')
    args = parser.parse_args(argv)
    db_path = root / 'knowledge.db'
    if not state.needs_refresh(db_path, current_date=args.date or state.today()):
        print(f'==> 运行时已是最新，无需刷新: {root}', file=sys.stderr)
        return EXIT_OK
    return _do_install(root, args, skip_db=False, skip_sdk=False)


def cmd_update_cli(root: Path, argv) -> int:
    parser = argparse.ArgumentParser(
        prog='bootstrap.py update-cli', allow_abbrev=False,
        description='补齐或更换托管运行时里的 CLI 产物')
    parser.add_argument('--force', action='store_true',
                        help='先删掉已安装的产物再重新解析（配合端点即重新下载）')
    args = parser.parse_args(argv)
    try:
        if args.force:
            cli_install.installed_path(root).unlink(missing_ok=True)
        location = cli_install.ensure_cli(root)
    except (DownloadError, cli_install.CliInstallError, OSError,
            ValueError) as exc:
        print(f'错误: {exc}', file=sys.stderr)
        return EXIT_ERROR
    print(location.describe())
    return EXIT_OK


def cmd_download_db(root: Path, argv) -> int:
    parser = argparse.ArgumentParser(
        prog='bootstrap.py download-db', allow_abbrev=False,
        description='只下载指定日期的 knowledge.db（不安装 SDK）')
    parser.add_argument('--source', choices=DOWNLOAD_SOURCES)
    parser.add_argument('--date', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args(argv)
    try:
        source = args.source or download_source()
        output = download_database(
            source=source, date=args.date,
            output=Path(args.output).expanduser().resolve())
    except (DownloadError, ValueError) as exc:
        print(f'错误: {exc}', file=sys.stderr)
        return EXIT_ERROR
    print(output)
    return EXIT_OK


def cmd_validate_db(root: Path, argv) -> int:
    """转发给 CLI——schema 契约只有那一处（见 cli_install.load_database）。"""
    if not argv:
        print('错误: validate-db 需要一个路径', file=sys.stderr)
        return EXIT_USAGE
    try:
        cli = cli_install.load_cli(runtime_root=root)
    except (cli_install.CliInstallError, ValueError) as exc:
        print(f'错误: {exc}', file=sys.stderr)
        return EXIT_ERROR
    return cli.main(['validate-db', *argv])


def cmd_cli_path(root: Path, argv) -> int:
    try:
        location = cli_install.resolve_cli(root)
    except (cli_install.CliInstallError, ValueError) as exc:
        print(f'错误: {exc}', file=sys.stderr)
        return EXIT_ERROR
    print(location.path)
    return EXIT_OK


MANAGED_COMMANDS = {
    'doctor': cmd_doctor,
    'install': cmd_install,
    'refresh': cmd_refresh,
    'update-cli': cmd_update_cli,
    'download-db': cmd_download_db,
    'validate-db': cmd_validate_db,
    'cli-path': cmd_cli_path,
}


# ---------------------------------------------------------------- 入口

def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        load_env_files(cli_install.default_runtime_root(None))
    except ValueError as exc:
        print(f'错误: {exc}', file=sys.stderr)
        return EXIT_USAGE

    explicit_root, argv = pop_runtime_root(argv)
    command = first_command(argv)

    if command is None or command in ('help', '--help', '-h'):
        print(USAGE)
        return EXIT_OK

    if command not in MANAGED_COMMANDS:
        print(f'错误: 未知命令 {command}。bootstrap.py 只负责安装，'
              '查询请直接调 CLI：\n'
              f'  python3 <runtime-root>/{cli_install.ARTIFACT_NAME} '
              '--db <runtime-root>/knowledge.db <ask|arch|diff|sql> …\n'
              f'可用命令: {", ".join(MANAGED)}', file=sys.stderr)
        return EXIT_USAGE

    root = resolve_root(explicit_root, argv)
    rest = argv[argv.index(command) + 1:]
    return MANAGED_COMMANDS[command](root, rest)


if __name__ == '__main__':
    raise SystemExit(main())
