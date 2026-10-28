"""Read-only Git destination suggestions and effective ODK configuration."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import NamedTuple
from urllib.parse import urlsplit

# Shipped fallback; user overrides are beside the active default configuration.
DEFAULT_DESIGN_DOCS_REPOSITORY = "https://gitcode.com/OpenHarmonyAI/design-docs"
_CONFIG_FILENAME = "odk_config.yaml"
_CONFIG_EXT_FILENAME = "odk_config_ext.yaml"


def _parse_simple_yaml(text: str) -> dict[str, str]:
    """Parse ODK's flat string-scalar YAML, preserving quoted # and empty values.

    Reject malformed/duplicate keys and structured YAML instead of silently
    running default commands when an override was intended.
    """
    result: dict[str, str] = {}
    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*):[ \t]*(.*)", line)
        if not match:
            raise ValueError(f"config line {number}: expected a top-level scalar key: value")
        key, raw = match.groups()
        if key in result:
            raise ValueError(f"config line {number}: duplicate key {key}")
        raw = raw.strip()
        if raw.startswith('"'):
            try:
                value, end = json.JSONDecoder().raw_decode(raw)
            except ValueError as error:
                raise ValueError(f"config line {number}: invalid quoted value") from error
            suffix = raw[end:]
            if not isinstance(value, str) or (suffix.strip() and not re.fullmatch(r"[ \t]+#.*", suffix)):
                raise ValueError(f"config line {number}: invalid quoted scalar")
        elif raw.startswith("'"):
            quoted = re.fullmatch(r"'((?:[^']|'')*)'(?:[ \t]+#.*)?", raw)
            if not quoted:
                raise ValueError(f"config line {number}: invalid single-quoted scalar")
            value = quoted[1].replace("''", "'")
        else:
            value = re.split(r"[ \t]+#", raw, maxsplit=1)[0].rstrip()
            if not value or value[0] in "[{|>&*!#" or value in {"null", "Null", "NULL", "~"}:
                raise ValueError(f"config line {number}: use a string scalar (quote empty values)")
        result[key] = value
    return result


def _config_search_dirs() -> list[Path]:
    """Source, native/neutral runtime, and SkillHub projection layouts."""
    root = Path(__file__).absolute().parent.parent.parent
    return [d for d in (root / "core/config", root / "assets/config", root / "assets") if d.is_dir()]


def _read_config(path: Path) -> dict[str, str]:
    try:
        return _parse_simple_yaml(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise ValueError(f"Cannot read ODK config {path}: {error}") from error


def _default_config_path() -> Path:
    for directory in _config_search_dirs():
        path = directory / _CONFIG_FILENAME
        if path.is_file():
            return path
    raise ValueError("Cannot find shipped odk_config.yaml for this ODK installation")


def user_config_path() -> Path:
    return _default_config_path().with_name(_CONFIG_EXT_FILENAME)


def load_odk_config() -> tuple[dict[str, str], dict[str, str]]:
    """Read defaults and their sibling user override without modifying either.

    Missing override keys inherit defaults; explicit empty strings override them.
    Never search another installation or the business working directory for ext.
    """
    default = _default_config_path()
    override = default.with_name(_CONFIG_EXT_FILENAME)
    return _read_config(default), _read_config(override) if override.exists() else {}


def effective_odk_config() -> dict[str, str]:
    base, ext = load_odk_config()
    return {**base, **ext}


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
        source = "config-ext" if "design_docs_repository" in ext else "gitcode-default"
        destination = {**base, **ext}.get("design_docs_repository", DEFAULT_DESIGN_DOCS_REPOSITORY).strip()
        if not destination or not parse_git_remote(destination):
            return {"action": "ask-address", "repository": "", "source": "invalid-config"}
        return {"action": "confirm", "repository": destination, "source": source}
    return {"action": "ask-address", "repository": "", "source": "unconfigured"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Suggest a design-docs target; confirmation is always required. No writes or network access.")
    parser.add_argument("--remote", default="", help="Business repository origin URL; empty if unavailable")
    parser.add_argument("--configured", default="", help="Developer-provided design_docs_repository, if any")
    parser.add_argument("--checkout-remote", help="Compare an existing checkout against the suggested/confirmed target")
    parser.add_argument("--push-url", action="append", help="Each effective push URL from git remote get-url --push --all; repeat for all URLs")
    parser.add_argument("--effective-config", action="store_true", help="Print merged ODK configuration as JSON")
    args = parser.parse_args()
    if args.effective_config:
        try:
            print(json.dumps({"config": effective_odk_config(), "user_config_path": str(user_config_path())}, ensure_ascii=False))
        except (OSError, ValueError) as error:
            parser.exit(1, f"{error}\n")
        raise SystemExit(0)
    try:
        target = design_docs_target(args.remote, args.configured)
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")
    result: dict[str, str | bool] = dict(target)
    if args.checkout_remote is not None:
        result["checkout_matches"] = same_repository_endpoint(target["repository"], args.checkout_remote)
    if args.push_url is not None:
        result["push_targets_match"] = push_targets_match(target["repository"], args.push_url)
    print(json.dumps(result, ensure_ascii=False))
