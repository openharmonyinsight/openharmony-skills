"""Read-only Git remote identity and design-document destination suggestions."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import NamedTuple
from urllib.parse import urlsplit

# Built-in default, kept as the last-resort fallback when no config file
# supplies a design_docs_repository. See core/config/odk_config.yaml for the canonical
# default and core/config/odk_config_ext.yaml for the user override path.
DEFAULT_DESIGN_DOCS_REPOSITORY = "https://gitcode.com/OpenHarmonyAI/design-docs"
_CONFIG_FILENAME = "odk_config.yaml"
_CONFIG_EXT_FILENAME = "odk_config_ext.yaml"


def _parse_simple_yaml(text: str) -> dict[str, str]:
    """Parse a flat key: value YAML file without PyYAML.

    Handles only the subset used by odk_config.yaml: top-level scalar string
    assignments with optional single or double quotes, and comment lines.
    """
    result: dict[str, str] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            continue
        key, _, raw_value = stripped.partition(":")
        key = key.strip()
        value = raw_value.strip()
        # Strip inline comments (space/tab + #) before and after unquoting.
        # Handles: url # note, "url" # note, url<TAB># note
        # URLs may contain # so only ' #' and '<TAB>#' are comment delimiters.
        def _strip_comment(s: str) -> str:
            for sep in (" #", "\t#"):
                idx = s.find(sep)
                if idx != -1:
                    s = s[:idx]
            return s.strip()

        # Strip trailing comment FIRST (before quote detection), because a
        # quoted value with a trailing comment ends in the comment, not the
        # closing quote:  "url" # note  →  "url"  →  url
        value = _strip_comment(value)
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        if key:
            result[key] = value
    return result


def _config_search_dirs() -> list[Path]:
    """Directories that may hold odk_config.yaml / odk_config_ext.yaml.

    Source layout:  scripts/lib/odk_repository.py → repo root / core/config/
    Published layout: runtime/executables/lib/odk_repository.py → runtime/assets/
    """
    here = Path(__file__).resolve()
    source_assets = here.parent.parent.parent / "core" / "config"
    # Published: runtime/executables/lib/ → go up three levels to runtime/, then assets/
    published_assets = here.parent.parent.parent / "assets"
    return [d for d in (source_assets, published_assets) if d.is_dir()]


def load_odk_config() -> tuple[dict[str, str], dict[str, str]]:
    """Read odk_config.yaml (shipped default) and odk_config_ext.yaml (user override).

    Returns (base, ext) where ext contains only keys defined in odk_config_ext.yaml.
    Callers that need the merged view can do {**base, **ext}.
    Keys in ext win over base on conflict.
    Missing files are silently skipped. Performs no network access and no writes.
    """
    base: dict[str, str] = {}
    ext: dict[str, str] = {}
    for directory in _config_search_dirs():
        path_base = directory / "odk_config.yaml"
        if path_base.is_file():
            try:
                base.update(_parse_simple_yaml(path_base.read_text(encoding="utf-8")))
            except OSError:
                pass
        path_ext = directory / "odk_config_ext.yaml"
        if path_ext.is_file():
            try:
                ext.update(_parse_simple_yaml(path_ext.read_text(encoding="utf-8")))
            except OSError:
                pass
    return base, ext


class GitRemote(NamedTuple):
    scheme: str
    host: str
    port: int
    user: str
    absolute_path: bool
    repository: str


def parse_git_remote(remote: str) -> GitRemote | None:
    """Retain endpoint identity, including transport, port and SSH account."""
    value = remote.strip()
    if not value or any(char.isspace() for char in value) or re.match(r"^[A-Za-z]:[/\\]", value):
        return None
    if "://" in value:
        try:
            parsed = urlsplit(value)
            if (parsed.scheme not in {"https", "http", "ssh", "git"}
                    or not parsed.hostname or parsed.query or parsed.fragment
                    or parsed.password is not None):
                return None
            scheme = parsed.scheme
            port = parsed.port
            if port is None:
                port = {"https": 443, "http": 80, "ssh": 22, "git": 9418}[scheme]
            user = parsed.username or ""
            host, repo = parsed.hostname.lower(), parsed.path.lstrip("/")
            absolute_path = True
        except ValueError:
            return None
    else:
        match = re.fullmatch(r"(?:(?P<user>[^@/:]+)@)?(?P<host>[A-Za-z0-9.-]+):(?P<repo>[^:]+)", value)
        if not match:
            return None
        host, repo = match.group("host").lower(), match.group("repo")
        scheme, port, user = "ssh", 22, match.group("user") or ""
        absolute_path = repo.startswith("/")
        repo = repo.lstrip("/")
    if not re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", host):
        return None
    repo = repo.rstrip("/")
    if repo.endswith(".git"):
        repo = repo[:-4]
    parts = repo.split("/")
    if len(parts) < 2 or any(
        part in {"", ".", ".."} or not re.fullmatch(r"[A-Za-z0-9_.-]+", part)
        for part in parts
    ):
        return None
    return GitRemote(scheme, host, port, user, absolute_path, repo)


def repository_identity(remote: str) -> str | None:
    parsed = parse_git_remote(remote)
    return parsed.repository if parsed else None


def metadata_repository_url(value: str) -> GitRemote | None:
    """Canonical HTTPS repository identity for cross-host tracking (not Git auth)."""
    parsed = parse_git_remote(value)
    if parsed is None or parsed.scheme != "https" or urlsplit(value).username is not None:
        return None
    return parsed


def metadata_pr_url_matches(url: str, repository_url: str) -> bool:
    """Validate repository ownership of common PR/MR URL shapes, without network."""
    repository = metadata_repository_url(repository_url)
    if repository is None or any(char.isspace() for char in url):
        return False
    try:
        pr = urlsplit(url)
        if (pr.scheme != "https" or pr.username is not None or pr.password is not None
                or pr.query or pr.fragment or pr.hostname != repository.host
                or (443 if pr.port is None else pr.port) != repository.port):
            return False
    except ValueError:
        return False
    return re.fullmatch(
        rf"/{re.escape(repository.repository)}/(?:pulls?|merge_requests|-/merge_requests|pull-requests|pullrequest)/[0-9]+",
        pr.path,
    ) is not None


def same_repository_endpoint(confirmed: str, checkout: str) -> bool:
    """Only normalize syntax/default ports; cross-transport aliases need consent."""
    left, right = parse_git_remote(confirmed), parse_git_remote(checkout)
    return left is not None and right is not None and left == right


def push_targets_match(confirmed: str, push_urls: list[str]) -> bool:
    """Validate all caller-supplied effective URLs; empty sets fail closed."""
    return bool(push_urls) and all(same_repository_endpoint(confirmed, url) for url in push_urls)


def design_docs_target(remote: str, configured: str = "") -> dict[str, str]:
    """Suggest a target; neither a configuration nor a suggestion grants consent."""
    configured = configured.strip()
    if configured:
        if parse_git_remote(configured):
            return {"action": "confirm", "repository": configured, "source": "configured"}
        return {"action": "ask-address", "repository": "", "source": "invalid-config"}
    parsed = parse_git_remote(remote)
    if parsed and parsed.host == "gitcode.com":
        base, ext = load_odk_config()
        override = ext.get("design_docs_repository", "").strip()
        if override and parse_git_remote(override):
            return {"action": "confirm", "repository": override, "source": "config-ext"}
        default = base.get("design_docs_repository", DEFAULT_DESIGN_DOCS_REPOSITORY).strip()
        if not default or not parse_git_remote(default):
            default = DEFAULT_DESIGN_DOCS_REPOSITORY
        return {"action": "confirm", "repository": default, "source": "gitcode-default"}
    return {"action": "ask-address", "repository": "", "source": "unconfigured"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Suggest a design-docs target; confirmation is always required. No writes or network access.")
    parser.add_argument("--remote", default="", help="Business repository origin URL; empty if unavailable")
    parser.add_argument("--configured", default="", help="Developer-provided design_docs_repository, if any")
    parser.add_argument("--checkout-remote", help="Compare an existing checkout against the suggested/confirmed target")
    parser.add_argument("--push-url", action="append", help="Each effective push URL from git remote get-url --push --all; repeat for all URLs")
    args = parser.parse_args()
    target = design_docs_target(args.remote, args.configured)
    result: dict[str, str | bool] = dict(target)
    if args.checkout_remote is not None:
        result["checkout_matches"] = same_repository_endpoint(target["repository"], args.checkout_remote)
    if args.push_url is not None:
        result["push_targets_match"] = push_targets_match(target["repository"], args.push_url)
    print(json.dumps(result, ensure_ascii=False))
