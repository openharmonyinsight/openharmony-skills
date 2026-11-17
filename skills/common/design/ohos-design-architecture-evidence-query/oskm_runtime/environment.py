"""Skill 侧的下载配置：DB / SDK 归档端点，以及 CLI 产物端点。

**CLI 不读这个模块。** 端点、来源、`.env` 都是"把东西装到位"才需要的概念，
属于 skill；查询 CLI 只认一个库路径（见 cli-skill-split.md §2.2）。
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit


SOURCE_ENV = 'OSKM_DOWNLOAD_SOURCE'
ENDPOINT_ENV = 'OSKM_DOWNLOAD_ENDPOINT'
# 直接指定 CLI 位置（.pyz 或源码目录），优先级最高，主要给开发和 CI 用。
CLI_PATH_ENV = 'OSKM_CLI'
# 托管运行时根目录，等价于每条命令都写 --runtime-root。
RUNTIME_ROOT_ENV = 'OSKM_RUNTIME_ROOT'

OPENHARMONY_CI = 'OPENHARMONY_CI'
INTERNAL_CI = 'INTERNAL_CI'
DOWNLOAD_SOURCES = (OPENHARMONY_CI, INTERNAL_CI)
OPENHARMONY_COMPONENT = 'dayu600_7885_ai'

ENV_KEYS = (SOURCE_ENV, ENDPOINT_ENV, CLI_PATH_ENV, RUNTIME_ROOT_ENV)

# doctor 报告里"内部模块"这一行要检查的包。`oskm_cli` 在 CLI 产物里、
# `oskm_schema` 被打进同一个 pyz；skill 自己的包是 `oskm_runtime`。
RUNTIME_MODULES_HINT = ('oskm_runtime', 'oskm_cli', 'oskm_schema')
# `.env` 查找顺序见 env_file_candidates()：运行时根目录优先于 skill 目录，
# 因为已安装的 skill 目录可能是只读的。
ENV_FILE = Path(__file__).with_name('.env')
DEFAULT_RUNTIME_ROOT = Path('~/.oskm')


@dataclass(frozen=True)
class DownloadConfig:
    source: str
    endpoint: str


def runtime_root(explicit: str | Path | None = None) -> Path:
    """Resolve the managed runtime root from a flag, the environment, or ~."""
    raw = str(explicit).strip() if explicit else \
        os.environ.get(RUNTIME_ROOT_ENV, '').strip()
    return Path(raw).expanduser() if raw else DEFAULT_RUNTIME_ROOT.expanduser()


def env_file_candidates(root: str | Path | None = None) -> list[Path]:
    """`.env` lookup order, most specific first."""
    return [runtime_root(root) / '.env', ENV_FILE]


def _parse_line(raw: str, path: Path, line_number: int) -> tuple[str, str] | None:
    line = raw.strip()
    if not line or line.startswith('#'):
        return None
    if line.startswith('export '):
        line = line[len('export '):].lstrip()
    key, separator, value = line.partition('=')
    key = key.strip()
    if not separator or not key:
        raise ValueError(f'{path}:{line_number}: 配置行必须使用 KEY=VALUE')
    if key not in ENV_KEYS:
        raise ValueError(
            f'{path}:{line_number}: 不支持的配置项 {key}；'
            f'只允许 {", ".join(ENV_KEYS)}')

    value = value.strip()
    if value[:1] in ('"', "'"):
        quote = value[0]
        closing = value.find(quote, 1)
        if closing < 0:
            raise ValueError(f'{path}:{line_number}: 引号未闭合')
        trailing = value[closing + 1:].strip()
        if trailing and not trailing.startswith('#'):
            raise ValueError(f'{path}:{line_number}: 引号后的内容无法识别')
        value = value[1:closing]
    elif ' #' in value:
        value = value.split(' #', 1)[0].rstrip()
    return key, value


def load_env_file(path: Path | None = None) -> Path | None:
    """Load supported settings from one .env file without overriding env."""
    path = Path(path) if path is not None else ENV_FILE
    if not path.is_file():
        return None
    try:
        lines = path.read_text(encoding='utf-8-sig').splitlines()
    except OSError as exc:
        raise ValueError(f'环境文件不可读: {path}: {exc}') from exc

    values: dict[str, str] = {}
    for line_number, raw in enumerate(lines, start=1):
        parsed = _parse_line(raw, path, line_number)
        if parsed is not None:
            key, value = parsed
            values[key] = value
    # setdefault：真实环境变量始终赢过文件，否则 CI 里 export 会被静默盖掉。
    for key, value in values.items():
        os.environ.setdefault(key, value)
    return path


def load_env_files(root: str | Path | None = None) -> Path | None:
    """Load the first existing `.env` from `env_file_candidates()`."""
    for candidate in env_file_candidates(root):
        loaded = load_env_file(candidate)
        if loaded is not None:
            return loaded
    return None


def download_source() -> str:
    """Return the selected download source, defaulting to OpenHarmony CI."""
    source = os.environ.get(SOURCE_ENV, '').strip() or OPENHARMONY_CI
    if source not in DOWNLOAD_SOURCES:
        raise ValueError(
            f'{SOURCE_ENV} 只能是 {" 或 ".join(DOWNLOAD_SOURCES)}: {source}')
    return source


def _endpoint() -> str:
    endpoint = os.environ.get(ENDPOINT_ENV, '').strip().rstrip('/')
    if not endpoint:
        raise ValueError(f'{ENDPOINT_ENV} 未配置')
    if _is_invalid_endpoint(endpoint):
        raise ValueError(f'{ENDPOINT_ENV} 必须是 HTTP(S) URL')
    return endpoint


def download_config() -> DownloadConfig:
    """Validate and return the environment-driven download settings."""
    source = download_source()
    endpoint = _endpoint()
    return DownloadConfig(source=source, endpoint=endpoint)


def download_configuration() -> tuple[bool, str]:
    """Return doctor-readable download readiness."""
    try:
        config = download_config()
    except ValueError:
        source = os.environ.get(SOURCE_ENV, '').strip() or OPENHARMONY_CI
        endpoint = os.environ.get(ENDPOINT_ENV, '').strip()
        source_state = source if source in DOWNLOAD_SOURCES else '格式错误'
        endpoint_state = '已配置' if endpoint else '未配置'
        if endpoint and _is_invalid_endpoint(endpoint):
            endpoint_state = '格式错误'
        return False, (
            f'{SOURCE_ENV}={source_state}, '
            f'{ENDPOINT_ENV}={endpoint_state}')
    return True, (
        f'{SOURCE_ENV}={config.source}, '
        f'{ENDPOINT_ENV}=已配置')


def _is_invalid_endpoint(value: str) -> bool:
    parsed = urlsplit(value)
    return parsed.scheme not in ('http', 'https') or not parsed.netloc
