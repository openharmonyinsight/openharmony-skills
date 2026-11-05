"""Read-only Git destination suggestions and effective ODK configuration."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import NamedTuple
from urllib.parse import unquote, urlsplit

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
    Normalize legacy names within each layer before merging user overrides.
    """
    default = _default_config_path()
    override = default.with_name(_CONFIG_EXT_FILENAME)
    base = _read_config(default)
    ext = _read_config(override) if override.exists() else {}
    for values in (base, ext):
        legacy_hooks = values.pop("post_pr_hooks", None)
        if legacy_hooks is not None:
            values.setdefault("post_cr_mr_pr_hooks", legacy_hooks)
    return base, ext


def effective_odk_config() -> dict[str, str]:
    base, ext = load_odk_config()
    return {**base, **ext}


_SKILL_CONFIG_KEYS = {
    "pre_commit_reviews", "post_commit_reviews", "post_cr_mr_pr_hooks",
    "device_flash_skill", "ci_trigger", "online_test_trigger",
}


def _config_comment_blocks(path: Path) -> dict[str, list[tuple[int, str]]]:
    """Associate preceding section comments with its consecutive scalar keys."""
    if not path.exists():
        return {}
    blocks: dict[str, list[tuple[int, str]]] = {}
    pending: list[tuple[int, str]] = []
    active: list[tuple[int, str]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.lstrip().startswith("#"):
            pending.append((number, line.lstrip()[1:].strip()))
        elif line.strip():
            match = re.match(r"([A-Za-z_][A-Za-z0-9_]*):", line)
            if match:
                if pending:
                    active, pending = pending, []
                blocks[match[1]] = active
    # Match the same within-file canonical-key precedence as load_odk_config.
    if "post_cr_mr_pr_hooks" not in blocks and "post_pr_hooks" in blocks:
        blocks["post_cr_mr_pr_hooks"] = blocks["post_pr_hooks"]
    return blocks


def _comment_skill_urls(path: Path, key: str, skill: str, source: str) -> list[dict[str, object]]:
    candidates = []
    short_name = re.split(r"[:/]", skill)[-1]
    for line, comment in _config_comment_blocks(path).get(key, []):
        explicit = re.match(r"skill-install:\s+(\S+)\s+(https?://\S+)", comment)
        if explicit and explicit[1] != skill:
            continue
        for raw in re.findall(r"https?://[^\s<>\"']+", comment):
            url = raw.rstrip(".,;)]}`")
            try:
                parsed = urlsplit(url)
                # Installation hints are source URLs, never embedded credentials.
                if not parsed.hostname or parsed.username is not None or parsed.password is not None:
                    continue
                _ = parsed.port
            except ValueError:
                continue
            components = [unquote(part).removesuffix(".git") for part in parsed.path.split("/")]
            match = "explicit" if explicit else "path" if short_name in components else "reference"
            candidates.append({"url": url, "config_path": str(path), "line": line,
                               "source": source, "match": match})
    return sorted(candidates, key=lambda item: ({"explicit": 0, "path": 1, "reference": 2}[item["match"]], item["line"]))


def skill_install_hints(key: str, skill: str | None = None) -> dict[str, object]:
    """Read comment links for configured skills; never detect, install or execute.

    Links are candidates for the agent to inspect, not proof of a skill's identity.
    Restrict discovery to the same parameter's section in this installation.
    """
    key = "post_cr_mr_pr_hooks" if key == "post_pr_hooks" else key
    if key not in _SKILL_CONFIG_KEYS:
        raise ValueError(f"{key} is not a skill configuration field")
    value = effective_odk_config().get(key, "").strip()
    if key in {"ci_trigger", "online_test_trigger"}:
        skills = [value[len("skill:"):].strip()] if value.startswith("skill:") else []
    elif key == "device_flash_skill":
        skills = [value] if value else []
    else:
        skills = value.split()
    if any(not name or len(name.split()) != 1 for name in skills):
        raise ValueError(f"{key} requires a single skill name for this mode")
    if skill is not None and skill not in skills:
        raise ValueError(f"{skill} is not configured in {key}")
    default = _default_config_path()
    override = default.with_name(_CONFIG_EXT_FILENAME)
    hints = []
    for name in ([skill] if skill is not None else skills):
        candidates = []
        seen = set()
        for path, source in ((override, "override"), (default, "default")):
            for candidate in _comment_skill_urls(path, key, name, source):
                if candidate["url"] not in seen:
                    seen.add(candidate["url"])
                    candidates.append(candidate)
        hints.append({"skill": name, "candidates": candidates})
    return {"config_key": key, "configured_skills": skills, "hints": hints,
            "searched_paths": [str(override), str(default)]}


def build_product_options() -> dict[str, object]:
    """Prepare a menu from effective config; a configured default grants no choice."""
    config = effective_odk_config()
    preferred = config.get("build_product", "").strip()
    raw = config["build_products"] if "build_products" in config else preferred
    products = list(dict.fromkeys(raw.split()))
    if not products:
        raise ValueError("Configure a non-empty build_products list before selecting a build product")
    default = preferred if preferred in products else None
    return {
        "products": products,
        "default_product": default,
        "selected_product": None,
        "confirmation_required": True,
        "menu": [{"number": number, "product": product, "is_default": product == default}
                 for number, product in enumerate(products, 1)],
    }


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
    """Check an HTTPS endpoint and repository path boundary, without network.

    PR route names and identifier formats are platform-owned. This structural
    check does not prove that the resource exists, is a PR, or belongs to this
    repository; the publishing workflow must query the actual platform for that.
    """
    repository = metadata_repository_url(repository_url)
    if repository is None or '\\' in url or any(
        char.isspace() or ord(char) < 32 or ord(char) == 127 for char in url
    ):
        return False
    try:
        pr = urlsplit(url)
        if (pr.scheme != "https" or pr.username is not None or pr.password is not None
                or pr.query or pr.fragment or pr.hostname != repository.host
                or (443 if pr.port is None else pr.port) != repository.port):
            return False
    except ValueError:
        return False
    prefix = f"/{repository.repository}/"
    if not pr.path.startswith(prefix):
        return False
    suffix = pr.path[len(prefix):]
    if suffix.endswith('/'):
        suffix = suffix[:-1]
    # Reject navigation and encoded delimiters rather than normalizing a URL
    # into a different resource. Percent-encoded opaque Unicode IDs remain valid.
    try:
        for segment in suffix.split('/'):
            decoded = unquote(segment, errors='strict')
            if (not segment or decoded in {'.', '..'}
                    or any(char in decoded for char in '/\\%')
                    or any(ord(char) < 32 or ord(char) == 127 for char in decoded)):
                return False
    except UnicodeDecodeError:
        return False
    return True


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
    config_action = parser.add_mutually_exclusive_group()
    config_action.add_argument("--effective-config", action="store_true", help="Print merged ODK configuration as JSON")
    config_action.add_argument("--build-product-options", action="store_true", help="Print build-product menu as JSON; no product is selected")
    config_action.add_argument("--skill-install-hints", metavar="CONFIG_KEY", help="Read installation links from a configured skill field's preceding comments")
    parser.add_argument("--skill", help="Limit installation hints to this configured skill; requires --skill-install-hints")
    args = parser.parse_args()
    if args.skill is not None and args.skill_install_hints is None:
        parser.error("--skill requires --skill-install-hints")
    if args.effective_config or args.build_product_options or args.skill_install_hints is not None:
        try:
            if args.skill_install_hints is not None:
                payload = skill_install_hints(args.skill_install_hints, args.skill)
            else:
                payload = build_product_options() if args.build_product_options else {"config": effective_odk_config()}
            payload["user_config_path"] = str(user_config_path())
            print(json.dumps(payload, ensure_ascii=False))
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
