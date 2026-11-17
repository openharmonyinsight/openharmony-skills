"""Cross-platform download of date-addressed oskm runtime archives.

Only standard library: ``urllib.request`` / ``tarfile`` / ``zipfile`` /
``sqlite3``. Git is never required, and neither is a shell -- the ``.sh``
wrappers that used to sit next to this module are gone (see
``docs/architecture/cli-skill-split.md``).

Extraction is defensive on purpose: an archive member that would escape the
destination, or a symlink that later members write through, aborts the whole
install instead of leaving a half-written runtime behind.
"""

from __future__ import annotations

import json
import os
import posixpath
import shutil
import sqlite3
import tarfile
import tempfile
import time
import zipfile
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

from .environment import (
    DOWNLOAD_SOURCES,
    INTERNAL_CI,
    OPENHARMONY_CI,
    OPENHARMONY_COMPONENT,
    SOURCE_ENV,
    DownloadConfig,
    download_config,
)


TAR_SUFFIXES = (
    '.tar', '.tar.gz', '.tgz', '.tar.xz', '.txz', '.tar.bz2', '.tbz2')
RUNTIME_SDK_DIRS = ('interface/sdk-js', 'interface/sdk_c')
# 运行时归档根目录下的两个单文件产物。CLI 与 knowledge.db 一起发布、一起落盘，
# 所以它不需要单独的下载端点（2026-11-12 之前有过，已删）。
RUNTIME_DB_NAME = 'knowledge.db'
RUNTIME_CLI_NAME = 'oskm-cli.pyz'


class DownloadError(RuntimeError):
    """A user-actionable database download failure."""


def _resolved_config(source: str | None = None) -> DownloadConfig:
    """Validate source and endpoint before any network operation."""
    try:
        config = download_config()
    except ValueError as exc:
        raise DownloadError(str(exc)) from exc
    if source is None:
        return config
    if source not in DOWNLOAD_SOURCES:
        raise DownloadError(
            f'{SOURCE_ENV} 只能是 {" 或 ".join(DOWNLOAD_SOURCES)}: {source}')
    return DownloadConfig(source=source, endpoint=config.endpoint)


def validate_date(date: str) -> str:
    if len(date) != 8 or not date.isdigit():
        raise DownloadError(f'--date 必须是 YYYYMMDD: {date}')
    try:
        datetime.strptime(date, '%Y%m%d')
    except ValueError as exc:
        raise DownloadError(f'--date 不是有效日期: {date}') from exc
    return date


def _failure_detail(exc: BaseException | str) -> str:
    text = str(exc)
    lowered = text.lower()
    if 'certificate' in lowered or 'ssl' in lowered or 'tls' in lowered:
        return 'TLS 或证书校验失败'
    if 'timed out' in lowered or 'timeout' in lowered:
        return '连接或传输超时'
    return '网络或代理不可用'


def _open(
    request: Request,
    *,
    timeout: float,
    attempts: int,
    retry_delay: float,
):
    last_error: BaseException | None = None
    for attempt in range(attempts):
        try:
            return urlopen(request, timeout=timeout)
        except HTTPError as exc:
            last_error = exc
            retryable = exc.code in (408, 429, 500, 502, 503, 504)
            if not retryable or attempt + 1 == attempts:
                raise DownloadError(
                    f'下载失败（HTTP {exc.code}）: {request.full_url}. '
                    '检查该日期/资源是否存在以及代理设置。') from exc
        except OSError as exc:
            last_error = exc
            if attempt + 1 == attempts:
                raise DownloadError(
                    f'下载失败（{_failure_detail(exc)}）: {request.full_url}: '
                    f'{exc}. 检查网络、DNS、HTTPS_PROXY/HTTP_PROXY/NO_PROXY '
                    '和证书配置。') from exc
        if retry_delay > 0:
            time.sleep(retry_delay)
    raise DownloadError(f'下载失败: {request.full_url}: {last_error}')


def _fetch(
    url: str,
    destination: Path,
    *,
    timeout: float,
    attempts: int,
    retry_delay: float,
) -> None:
    headers = {'Accept': 'application/octet-stream'}
    request = Request(url, headers=headers)
    with _open(
            request, timeout=timeout, attempts=attempts,
            retry_delay=retry_delay) as response:
        with destination.open('wb') as stream:
            shutil.copyfileobj(response, stream)


def _fetch_openharmony_obs_path(
    config: DownloadConfig,
    date: str,
    *,
    timeout: float,
    attempts: int,
    retry_delay: float,
) -> str:
    api = config.endpoint
    payload = json.dumps({
        'projectName': 'openharmony',
        'branch': 'master',
        'pageNum': 1,
        'pageSize': 10,
        'deviceLevel': '',
        'component': OPENHARMONY_COMPONENT,
        'type': 1,
        'startTime': f'{date}00000000',
        'endTime': f'{date}235959',
        'sortType': '',
        'sortField': '',
        'hardwareBoard': '',
        'buildStatus': 'success',
        'buildFailReason': '',
        'withDomain': 1,
    }, ensure_ascii=False).encode('utf-8')
    request = Request(
        api,
        data=payload,
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        method='POST',
    )
    with _open(
            request, timeout=timeout, attempts=attempts,
            retry_delay=retry_delay) as response:
        try:
            document = json.load(response)
        except (json.JSONDecodeError, UnicodeDecodeError, OSError) as exc:
            raise DownloadError(
                f'{config.source} 构建响应不是有效 JSON（{date}）: {exc}'
            ) from exc
    try:
        obs_path = document['data']['list']['dataList'][0]['obsPath']
    except (KeyError, IndexError, TypeError) as exc:
        raise DownloadError(
            f'该日期没有成功构建：{date}；'
            '响应缺少 obsPath') from exc
    if not isinstance(obs_path, str) or not obs_path:
        raise DownloadError(
            f'该日期没有成功构建，或 obsPath 为空（{date}）')
    return urljoin(api, obs_path)


def _download_name(url: str) -> str:
    name = PurePosixPath(urlsplit(url).path).name
    if not name:
        raise DownloadError(f'无法从下载 URL 取得文件名: {url}')
    return name


def _download_archive(
    *,
    config: DownloadConfig,
    date: str,
    work_dir: Path,
    timeout: float,
    attempts: int,
    retry_delay: float,
) -> Path:
    """Download the dated runtime archive into ``work_dir``."""
    if config.source == INTERNAL_CI:
        url = f'{config.endpoint}/{date}'
        archive = work_dir / 'knowledge.tar.gz'
    elif config.source == OPENHARMONY_CI:
        url = _fetch_openharmony_obs_path(
            config, date, timeout=timeout, attempts=attempts,
            retry_delay=retry_delay)
        archive = work_dir / _download_name(url)
    else:
        raise DownloadError(f'不支持的下载方式: {config.source}')
    _fetch(
        url, archive, timeout=timeout, attempts=attempts,
        retry_delay=retry_delay)
    return archive


def _archive_member_names(archive: Path) -> list[str]:
    suffix = archive.name.lower()
    if suffix.endswith('.zip'):
        with zipfile.ZipFile(archive) as bundle:
            return [
                member.filename for member in bundle.infolist()
                if not member.is_dir()
            ]
    if suffix.endswith(TAR_SUFFIXES):
        with tarfile.open(archive, 'r:*') as bundle:
            return [
                member.name for member in bundle.getmembers()
                if member.isfile()
            ]
    raise DownloadError(f'无法识别的 DB 下载后缀: {archive.name}')


def _copy_member(archive: Path, member_name: str, destination: Path) -> None:
    if archive.name.lower().endswith('.zip'):
        with zipfile.ZipFile(archive) as bundle:
            with bundle.open(member_name) as source, \
                    destination.open('wb') as target:
                shutil.copyfileobj(source, target)
        return
    with tarfile.open(archive, 'r:*') as bundle:
        source = bundle.extractfile(member_name)
        if source is None:
            raise DownloadError(f'无法读取归档成员: {member_name}')
        with source, destination.open('wb') as target:
            shutil.copyfileobj(source, target)


def extract_database(archive: Path, work_dir: Path) -> Path:
    """Return a temporary DB candidate extracted from a supported download."""
    name = archive.name.lower()
    if name.endswith('.db'):
        return archive
    if not (name.endswith('.zip') or name.endswith(TAR_SUFFIXES)):
        raise DownloadError(f'无法识别的 DB 下载后缀: {archive.name}')

    try:
        names = _archive_member_names(archive)
        matches = [
            member for member in names
            if PurePosixPath(member.replace('\\', '/')).name == 'knowledge.db'
        ]
        if len(matches) != 1:
            raise DownloadError(
                'DB 下载物中应恰有一个 knowledge.db，'
                f'实际找到 {len(matches)} 个')
        candidate = work_dir / 'knowledge.db'
        _copy_member(archive, matches[0], candidate)
        return candidate
    except DownloadError:
        raise
    except (OSError, tarfile.TarError, zipfile.BadZipFile, RuntimeError) as exc:
        raise DownloadError(f'DB 归档解压失败: {archive.name}: {exc}') from exc


def _runtime_relative_path(raw: str) -> PurePosixPath:
    path = PurePosixPath(raw.replace('\\', '/'))
    if path.is_absolute() or '..' in path.parts:
        raise DownloadError(f'运行时归档包含越界路径: {raw}')
    parts = tuple(part for part in path.parts if part not in ('', '.'))
    if not parts:
        return PurePosixPath('.')
    return PurePosixPath(*parts)


def _runtime_area(path: PurePosixPath) -> str | None:
    if str(path) == RUNTIME_DB_NAME:
        return 'db'
    if str(path) == RUNTIME_CLI_NAME:
        return 'cli'
    text = str(path)
    for directory in RUNTIME_SDK_DIRS:
        if text == directory or text.startswith(directory + '/'):
            return directory
    return None


def _runtime_symlink_target(
    member_name: PurePosixPath,
    link_name: str,
) -> str:
    target = link_name.replace('\\', '/')
    if PurePosixPath(target).is_absolute():
        raise DownloadError(
            f'运行时归档包含指向完整路径的符号链接: {member_name} -> {link_name}')
    joined = posixpath.normpath(f'{member_name.parent}/{target}')
    resolved = _runtime_relative_path(joined)
    if _runtime_area(resolved) != _runtime_area(member_name):
        raise DownloadError(
            f'运行时归档符号链接越界: {member_name} -> {link_name}')
    return target


def _runtime_members(bundle):
    members = []
    names = set()
    non_directory_names = set()
    for member in bundle.getmembers():
        path = _runtime_relative_path(member.name)
        if member.isfile() and (path.name == '.DS_Store' or path.name.startswith('._')):
            continue
        area = _runtime_area(path)
        allowed_container = member.isdir() and path in (
            PurePosixPath('.'), PurePosixPath('interface'))
        if area is None and not allowed_container:
            if path.parent == PurePosixPath('.') and member.isfile():
                continue
            raise DownloadError(f'运行时归档包含未允许的顶层路径: {member.name}')
        if path in names and not member.isdir():
            raise DownloadError(f'运行时归档包含重复路径: {member.name}')
        names.add(path)
        if not member.isdir():
            non_directory_names.add(path)
        if member.isdir():
            kind = 'dir'
        elif member.isfile():
            kind = 'file'
        elif member.issym():
            kind = 'symlink'
            _runtime_symlink_target(path, member.linkname)
        else:
            raise DownloadError(f'运行时归档包含不支持的文件类型: {member.name}')
        members.append((path, kind, member))
    return members, names, non_directory_names


def _validate_runtime_members(members, names, non_directory_names):
    db_found = [member for path, kind, member in members
                if path == PurePosixPath(RUNTIME_DB_NAME)
                and kind in ('file', 'symlink')]
    if len(db_found) != 1 or db_found[0].islnk():
        raise DownloadError(f'运行时归档根目录必须恰有一个 {RUNTIME_DB_NAME}')
    if not db_found[0].isfile():
        raise DownloadError(f'运行时归档中的 {RUNTIME_DB_NAME} 必须是普通文件')
    cli_found = [member for path, kind, member in members
                 if path == PurePosixPath(RUNTIME_CLI_NAME)
                 and kind in ('file', 'symlink')]
    if len(cli_found) > 1:
        raise DownloadError(f'运行时归档根目录只能有一个 {RUNTIME_CLI_NAME}')
    if cli_found and not cli_found[0].isfile():
        raise DownloadError(f'运行时归档中的 {RUNTIME_CLI_NAME} 必须是普通文件')
    for directory in RUNTIME_SDK_DIRS:
        prefix = PurePosixPath(directory)
        if not any(path != prefix and prefix in path.parents for path in names):
            raise DownloadError(f'运行时归档缺少非空的 {directory}/ 目录')
    symlink_names = {path for path, kind, _ in members if kind == 'symlink'}
    for path in non_directory_names:
        if any(parent in symlink_names for parent in path.parents):
            raise DownloadError(f'运行时归档在符号链接下写入文件: {path}')


def _write_runtime_members(bundle, destination, members):
    destination.mkdir(parents=True, exist_ok=True)
    for path, kind, _ in members:
        if kind == 'dir':
            (destination / path).mkdir(parents=True, exist_ok=True)
    for path, kind, member in members:
        if kind != 'file':
            continue
        target = destination / path
        target.parent.mkdir(parents=True, exist_ok=True)
        source = bundle.extractfile(member)
        if source is None:
            raise DownloadError(f'无法读取运行时归档成员: {member.name}')
        with source, target.open('wb') as output:
            shutil.copyfileobj(source, output)
        target.chmod((member.mode or 0o644) & 0o777)
    for path, kind, member in members:
        if kind != 'symlink':
            continue
        target = destination / path
        target.parent.mkdir(parents=True, exist_ok=True)
        os.symlink(member.linkname, target)


def extract_runtime(archive: Path, destination: Path) -> Path:
    """Securely extract a complete runtime archive into ``destination``."""
    if not archive.name.lower().endswith(TAR_SUFFIXES):
        raise DownloadError(f'运行时归档必须是 tar 格式: {archive.name}')
    destination = Path(destination)
    try:
        with tarfile.open(archive, 'r:*') as bundle:
            members, names, non_directory_names = _runtime_members(bundle)
            _validate_runtime_members(members, names, non_directory_names)
            _write_runtime_members(bundle, destination, members)
    except DownloadError:
        raise
    except (OSError, tarfile.TarError, RuntimeError) as exc:
        raise DownloadError(f'运行时归档解压失败: {archive.name}: {exc}') from exc
    return destination


def verify_sqlite(path: Path) -> None:
    path = Path(path)
    try:
        with path.open('rb') as stream:
            header = stream.read(16)
        if header != b'SQLite format 3\x00':
            raise DownloadError('SQLite integrity_check 未通过: 文件头无效')
        connection = sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)
        try:
            rows = [row[0] for row in connection.execute('PRAGMA integrity_check')]
        finally:
            connection.close()
        if rows != ['ok']:
            detail = '；'.join(str(row) for row in rows) or '没有返回结果'
            raise DownloadError(f'SQLite integrity_check 未通过: {detail}')
    except DownloadError:
        raise
    except (OSError, sqlite3.Error) as exc:
        raise DownloadError(f'SQLite integrity_check 未通过: {exc}') from exc


def _atomic_replace(candidate: Path, output: Path) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f'.{output.name}.tmp.', dir=output.parent)
    temporary = Path(temporary_name)
    try:
        with candidate.open('rb') as source, \
                os.fdopen(descriptor, 'wb') as target:
            descriptor = -1
            shutil.copyfileobj(source, target)
            target.flush()
            os.fsync(target.fileno())
        os.replace(temporary, output)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        temporary.unlink(missing_ok=True)


def download_database(
    *,
    source: str | None = None,
    date: str,
    output: Path,
    timeout: float = 90,
    attempts: int = 3,
    retry_delay: float = 2,
    verify: Callable[[Path], None] = verify_sqlite,
) -> Path:
    """Download, extract, verify, and atomically install a dated DB."""
    validate_date(date)
    config = _resolved_config(source)
    output = Path(output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(
            prefix='.oskm-db-download.', dir=output.parent) as temp:
        work_dir = Path(temp)
        archive = _download_archive(
            config=config,
            date=date,
            work_dir=work_dir,
            timeout=timeout,
            attempts=attempts,
            retry_delay=retry_delay,
        )
        candidate = extract_database(archive, work_dir)
        verify(candidate)
        _atomic_replace(candidate, output)
    return output


def download_runtime_bundle(
    *,
    source: str | None = None,
    date: str,
    output: Path,
    timeout: float = 90,
    attempts: int = 3,
    retry_delay: float = 2,
    verify: Callable[[Path], None] = verify_sqlite,
) -> Path:
    """Download and extract a complete DB + SDK runtime archive."""
    validate_date(date)
    config = _resolved_config(source)
    output = Path(output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(
            prefix='.oskm-runtime-download.', dir=output.parent) as temp:
        work_dir = Path(temp)
        archive = _download_archive(
            config=config,
            date=date,
            work_dir=work_dir,
            timeout=timeout,
            attempts=attempts,
            retry_delay=retry_delay,
        )
        candidate = extract_runtime(archive, work_dir / 'runtime')
        verify(candidate / 'knowledge.db')
        if output.exists():
            raise DownloadError(f'运行时临时输出已存在: {output}')
        shutil.move(str(candidate), str(output))
    return output
