"""Read-only Git remote identity and design-document destination suggestions."""
from __future__ import annotations

import argparse
import json
import re
from typing import NamedTuple
from urllib.parse import urlsplit

DEFAULT_DESIGN_DOCS_REPOSITORY = "https://gitcode.com/OpenHarmonyAI/design-docs"


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
        return {"action": "confirm", "repository": DEFAULT_DESIGN_DOCS_REPOSITORY, "source": "gitcode-default"}
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
