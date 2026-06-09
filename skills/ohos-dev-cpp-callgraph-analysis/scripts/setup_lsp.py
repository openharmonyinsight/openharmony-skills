#!/usr/bin/env python3
"""Prepare a repository-scoped clangd MCP service for OpenHarmony C++ analysis."""

import argparse
import hashlib
import json
import os
import platform
import re
import selectors
import shutil
import subprocess
import sys
import tarfile
import time
import urllib.request
from pathlib import Path


MCP_LANGUAGE_SERVER_VERSION = "v0.1.1"
GO_VERSION = "1.24.4"


def find_clangd(oh_root):
    """Return an OpenHarmony prebuilt clangd, preferring the current host architecture."""
    machine = platform.machine()
    hosts = ["linux-aarch64", "linux-x86_64"] if machine in ("aarch64", "arm64") else [
        "linux-x86_64", "linux-aarch64"
    ]
    for host in hosts:
        candidate = oh_root / "prebuilts" / "clang" / "ohos" / host / "llvm" / "bin" / "clangd"
        if candidate.is_file():
            return candidate
    candidate = shutil.which("clangd")
    return Path(candidate) if candidate else None


def _line_json_objects(source):
    """Parse GN multi-line objects and repository-filtered one-line objects."""
    current = []
    in_object = False
    for line in source:
        stripped = line.strip()
        if not in_object:
            if stripped.startswith("{") and stripped.endswith(("}", "},")):
                yield json.loads(stripped[:-1] if stripped.endswith(",") else stripped)
                continue
            if stripped == "{":
                current = [line]
                in_object = True
            continue
        current.append(line)
        if stripped in ("}", "},"):
            block = "".join(current).rstrip()
            if block.endswith(","):
                block = block[:-1]
            yield json.loads(block)
            current = []
            in_object = False
    if in_object:
        raise ValueError("incomplete JSON object")


def _json_objects(path):
    """Stream top-level JSON objects without loading a multi-gigabyte GN database."""
    if path.stat().st_size < 8 * 1024 * 1024:
        with path.open("r", encoding="utf-8") as source:
            yield from json.load(source)
        return
    with path.open("r", encoding="utf-8") as source:
        try:
            yield from _line_json_objects(source)
        except ValueError as exc:
            raise ValueError(f"{exc} in {path}") from exc


def _entry_source_path(entry):
    file_path = Path(entry["file"])
    if file_path.is_absolute():
        return file_path.resolve()
    return (Path(entry["directory"]) / file_path).resolve()


def filter_compile_database(source, target, repo_root):
    """Write only compilation entries whose source files belong to repo_root."""
    source = source.resolve()
    target = target.resolve()
    repo_root = repo_root.resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    output_target = target.with_suffix(".tmp") if source == target else target
    count = 0
    with output_target.open("w", encoding="utf-8") as output:
        output.write("[\n")
        for entry in _json_objects(source):
            try:
                belongs = _entry_source_path(entry).is_relative_to(repo_root)
            except (KeyError, OSError):
                belongs = False
            if not belongs:
                continue
            if count:
                output.write(",\n")
            json.dump(entry, output, ensure_ascii=True)
            count += 1
        output.write("\n]\n")
    if output_target != target:
        output_target.replace(target)
    return count


def first_compile_file(compdb):
    for entry in _json_objects(compdb):
        return _entry_source_path(entry)
    return None


def run(command, **kwargs):
    print("+", " ".join(str(item) for item in command), file=sys.stderr)
    return subprocess.run([str(item) for item in command], check=True, **kwargs)


def generate_full_compile_database(oh_root, product, build_target):
    """Ask the OpenHarmony build frontend to export compile_commands.json."""
    command = [
        oh_root / "build.sh",
        "--product-name", product,
        "--gn-flags=--export-compile-commands",
        "--build-target", build_target,
        "--ccache",
    ]
    try:
        run(command, cwd=oh_root)
    except subprocess.CalledProcessError:
        pass
    target = oh_root / "out" / product / "compile_commands.json"
    if not target.is_file():
        raise RuntimeError(f"OpenHarmony did not generate {target}")
    return target


def _download(url, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    print(f"download: {url}", file=sys.stderr)
    with urllib.request.urlopen(url) as response, target.open("wb") as output:
        shutil.copyfileobj(response, output)


def _safe_extract(archive, destination):
    destination = destination.resolve()
    for member in archive.getmembers():
        member_path = (destination / member.name).resolve()
        if not member_path.is_relative_to(destination):
            raise RuntimeError(f"unsafe archive member: {member.name}")
    archive.extractall(destination)


def go_is_compatible(binary):
    try:
        output = subprocess.run(
            [str(binary), "version"], capture_output=True, text=True, check=True
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return False
    match = re.search(r"\bgo(\d+)\.(\d+)", output)
    return bool(match and tuple(map(int, match.groups())) >= (1, 24))


def install_go(cache_dir):
    go = shutil.which("go")
    if go and go_is_compatible(go):
        return Path(go)
    machine = platform.machine()
    if machine in ("aarch64", "arm64"):
        arch = "arm64"
    elif machine in ("x86_64", "amd64"):
        arch = "amd64"
    else:
        raise RuntimeError(f"automatic Go installation does not support host architecture: {machine}")
    install_dir = cache_dir / f"go-{GO_VERSION}"
    binary = install_dir / "bin" / "go"
    if binary.is_file() and go_is_compatible(binary):
        return binary
    archive = cache_dir / f"go{GO_VERSION}.linux-{arch}.tar.gz"
    checksum_file = archive.with_suffix(archive.suffix + ".sha256")
    base_url = f"https://go.dev/dl/{archive.name}"
    _download(base_url, archive)
    _download(base_url + ".sha256", checksum_file)
    expected = checksum_file.read_text(encoding="utf-8").split()[0]
    actual = hashlib.sha256(archive.read_bytes()).hexdigest()
    if actual != expected:
        raise RuntimeError(f"Go archive checksum mismatch: expected {expected}, got {actual}")
    extract_dir = cache_dir / f"go-extract-{GO_VERSION}"
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    extract_dir.mkdir(parents=True)
    with tarfile.open(archive, "r:gz") as tar:
        _safe_extract(tar, extract_dir)
    shutil.move(str(extract_dir / "go"), str(install_dir))
    shutil.rmtree(extract_dir)
    return binary


def install_mcp_language_server(cache_dir):
    binary = cache_dir / "bin" / "mcp-language-server"
    if binary.is_file():
        return binary
    existing = shutil.which("mcp-language-server")
    if existing:
        return Path(existing)
    go = install_go(cache_dir)
    binary.parent.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env["GOBIN"] = str(binary.parent)
    env.setdefault("GOCACHE", str(cache_dir / "go-build-cache"))
    env.setdefault("GOMODCACHE", str(cache_dir / "go-mod-cache"))
    run(
        [go, "install", f"github.com/isaacphi/mcp-language-server@{MCP_LANGUAGE_SERVER_VERSION}"],
        env=env,
    )
    if not binary.is_file():
        raise RuntimeError(f"mcp-language-server was not installed at {binary}")
    return binary


def bridge_command(binary, repo_root, clangd, compdb_dir):
    return [
        str(binary),
        "--workspace", str(repo_root),
        "--lsp", str(clangd),
        "--",
        f"--compile-commands-dir={compdb_dir}",
        "--background-index",
    ]


def client_registration_command(client, name, binary, repo_root, clangd, compdb_dir):
    bridge = bridge_command(binary, repo_root, clangd, compdb_dir)
    if client == "codex":
        return ["codex", "mcp", "add", name, "--", *bridge]
    if client == "claude":
        return ["claude", "mcp", "add", "--scope", "project", name, "--", *bridge]
    raise ValueError(f"unsupported MCP client: {client}")


def resolve_clients(requested):
    clients = []
    for client in requested:
        candidates = ["codex", "claude"] if client == "auto" else [client]
        for candidate in candidates:
            if candidate not in clients and shutil.which(candidate):
                clients.append(candidate)
    return clients


def register_client(client, name, binary, repo_root, clangd, compdb_dir):
    subprocess.run([client, "mcp", "remove", name], capture_output=True)
    run(client_registration_command(client, name, binary, repo_root, clangd, compdb_dir))


def _read_response(process, request_id, timeout):
    deadline = time.monotonic() + timeout
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ)
    try:
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0 or not selector.select(remaining):
                raise TimeoutError(f"MCP smoke test timed out after {timeout}s")
            line = process.stdout.readline()
            if not line:
                stderr = process.stderr.read()
                raise RuntimeError(f"MCP server exited during smoke test: {stderr}")
            message = json.loads(line)
            if message.get("id") == request_id:
                return message
    finally:
        selector.close()


def smoke_test(command, sample_file, timeout=30):
    """Verify MCP discovery and one clangd-backed semantic request."""
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    try:
        initialize = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "ohos-callgraph-lsp-setup", "version": "1.0"},
            },
        }
        process.stdin.write(json.dumps(initialize) + "\n")
        process.stdin.flush()
        init_result = _read_response(process, 1, timeout)
        if "result" not in init_result:
            raise RuntimeError(f"MCP initialize failed: {init_result}")
        process.stdin.write(json.dumps({
            "jsonrpc": "2.0", "method": "notifications/initialized"
        }) + "\n")
        process.stdin.write(json.dumps({
            "jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}
        }) + "\n")
        process.stdin.flush()
        tools_result = _read_response(process, 2, timeout)
        tools = tools_result.get("result", {}).get("tools", [])
        names = {tool.get("name") for tool in tools}
        required = {"definition", "references", "hover", "diagnostics"}
        if not required.issubset(names):
            raise RuntimeError(f"MCP tools missing: {sorted(required - names)}")
        process.stdin.write(json.dumps({
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "diagnostics",
                "arguments": {
                    "filePath": str(sample_file),
                    "contextLines": False,
                    "showLineNumbers": False,
                },
            },
        }) + "\n")
        process.stdin.flush()
        semantic_result = _read_response(process, 3, timeout)
        if semantic_result.get("error") or semantic_result.get("result", {}).get("isError"):
            raise RuntimeError(f"clangd semantic smoke test failed: {semantic_result}")
        return sorted(names)
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


def default_cache_dir(repo_root):
    base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    digest = hashlib.sha256(str(repo_root.resolve()).encode()).hexdigest()[:12]
    return base / "ohos-callgraph-lsp" / f"{repo_root.name}-{digest}"


ENSURE_COMPDB_SCRIPT = '''\
#!/usr/bin/env python3
"""PreToolUse hook: ensure target file has a compile_commands.json entry."""

import json
import os
import sys
from pathlib import Path

COMPDB = Path(os.environ.get("OHOS_LSP_COMPDB", ""))
REPO_ROOT = Path(os.environ.get("OHOS_LSP_REPO_ROOT", ""))
CPP_EXTS = {".cpp", ".cc", ".cxx", ".c", ".h", ".hpp", ".hxx"}


def find_file_path(tool_input):
    fp = tool_input.get("filePath") or tool_input.get("file_path", "")
    if not fp:
        return None
    p = Path(fp)
    if not p.is_absolute():
        p = REPO_ROOT / p
    return p.resolve()


def file_in_compdb(entries, resolved_path):
    for e in entries:
        ep = Path(e.get("file", ""))
        if not ep.is_absolute():
            ep = Path(e.get("directory", "")) / ep
        if ep.resolve() == resolved_path:
            return True
    return False


def similarity(candidate_file, target_file):
    c_parts = Path(candidate_file).parts
    t_parts = target_file.parts
    score = 0
    for cp, tp in zip(reversed(c_parts), reversed(t_parts)):
        if cp == tp:
            score += 1
        else:
            break
    if Path(candidate_file).suffix == target_file.suffix:
        score += 2
    return score


def clone_entry(entries, target_path):
    best, best_score = None, -1
    for e in entries:
        s = similarity(e["file"], target_path)
        if s > best_score:
            best_score = s
            best = e
    if best is None:
        return None
    rel = os.path.relpath(target_path, Path(best["directory"]).resolve())
    new_entry = dict(best)
    new_entry["file"] = rel
    old_stem = Path(best["file"]).stem
    new_stem = target_path.stem
    if "command" in new_entry:
        new_entry["command"] = new_entry["command"].replace(old_stem, new_stem)
    if "arguments" in new_entry:
        new_entry["arguments"] = [a.replace(old_stem, new_stem) for a in new_entry["arguments"]]
    return new_entry


def append_entry(compdb_path, new_entry):
    with open(compdb_path, "rb+") as f:
        f.seek(-3, 2)
        pos = f.tell()
        while pos > 0:
            f.seek(pos)
            ch = f.read(1)
            if ch == b'}':
                f.seek(pos + 1)
                f.write(b',\\n')
                f.write(json.dumps(new_entry, ensure_ascii=True).encode())
                f.write(b'\\n]\\n')
                f.truncate()
                return True
            pos -= 1
    return False


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return
    tool_input = data.get("tool_input", {})
    target = find_file_path(tool_input)
    if target is None or not target.is_file():
        return
    if target.suffix.lower() not in CPP_EXTS:
        return
    if not COMPDB.is_file():
        return
    with open(COMPDB) as f:
        entries = json.load(f)
    if file_in_compdb(entries, target):
        return
    new_entry = clone_entry(entries, target)
    if new_entry is None:
        json.dump({"systemMessage": f"[ensure_compdb] No similar entry to clone for {target.name}"}, sys.stdout)
        return
    if append_entry(COMPDB, new_entry):
        json.dump({"systemMessage": f"[ensure_compdb] Added compdb entry for {target.name}"}, sys.stdout)
    else:
        json.dump({"systemMessage": f"[ensure_compdb] Failed to append entry for {target.name}"}, sys.stdout)


if __name__ == "__main__":
    main()
'''


def install_claude_hook(repo_root, compdb_path):
    """Install ensure_compdb.py script and Claude PreToolUse hook into the project."""
    scripts_dir = repo_root / ".claude" / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)

    script_path = scripts_dir / "ensure_compdb.py"
    script_content = ENSURE_COMPDB_SCRIPT.replace(
        'COMPDB = Path(os.environ.get("OHOS_LSP_COMPDB", ""))',
        f'COMPDB = Path(os.environ.get("OHOS_LSP_COMPDB", "{compdb_path}"))',
    ).replace(
        'REPO_ROOT = Path(os.environ.get("OHOS_LSP_REPO_ROOT", ""))',
        f'REPO_ROOT = Path(os.environ.get("OHOS_LSP_REPO_ROOT", "{repo_root}"))',
    )
    script_path.write_text(script_content, encoding="utf-8")
    script_path.chmod(0o755)
    print(f"installed {script_path}")

    settings_path = repo_root / ".claude" / "settings.local.json"
    settings = {}
    if settings_path.is_file():
        with settings_path.open() as f:
            settings = json.load(f)

    hooks = settings.setdefault("hooks", {})
    pre_hooks = hooks.setdefault("PreToolUse", [])
    hook_entry = {
        "matcher": "mcp__ohos-lsp",
        "hooks": [
            {
                "type": "command",
                "command": f"python3 {script_path}",
                "timeout": 5,
            }
        ],
    }
    existing = [h for h in pre_hooks if h.get("matcher") == "mcp__ohos-lsp"]
    if existing:
        existing[0].update(hook_entry)
    else:
        pre_hooks.append(hook_entry)

    with settings_path.open("w") as f:
        json.dump(settings, f, indent=2, ensure_ascii=True)
        f.write("\n")
    print(f"configured Claude PreToolUse hook in {settings_path}")


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--oh-root", required=True, type=Path)
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--product", required=True)
    parser.add_argument("--build-target", help="Defaults to the repository directory name")
    parser.add_argument("--full-compdb", type=Path)
    parser.add_argument("--generate-compile-db", action="store_true")
    parser.add_argument("--cache-dir", type=Path)
    parser.add_argument("--client", action="append", choices=["auto", "codex", "claude", "none"],
                        default=[])
    parser.add_argument("--name", default="ohos-lsp")
    parser.add_argument("--smoke-timeout", type=int, default=120)
    parser.add_argument("--skip-register", action="store_true")
    parser.add_argument("--skip-smoke-test", action="store_true")
    parser.add_argument("--install-hook", action="store_true",
                        help="Install Claude PreToolUse hook when Claude is a selected client")
    return parser.parse_args()


def main():
    args = parse_args()
    oh_root = args.oh_root.resolve()
    repo_root = args.repo_root.resolve()
    if not repo_root.is_relative_to(oh_root):
        raise SystemExit(f"--repo-root must be inside --oh-root: {repo_root}")
    cache_dir = (args.cache_dir or default_cache_dir(repo_root)).resolve()
    cache_dir.mkdir(parents=True, exist_ok=True)

    clangd = find_clangd(oh_root)
    if not clangd:
        raise SystemExit("clangd not found in OpenHarmony prebuilts or PATH")

    full_compdb = args.full_compdb or oh_root / "out" / args.product / "compile_commands.json"
    if not full_compdb.is_file():
        if not args.generate_compile_db:
            raise SystemExit(
                f"{full_compdb} does not exist; rerun with --generate-compile-db "
                "after obtaining approval for the OpenHarmony build"
            )
        full_compdb = generate_full_compile_database(
            oh_root, args.product, args.build_target or repo_root.name
        )

    filtered = cache_dir / "compdb" / "compile_commands.json"
    count = filter_compile_database(full_compdb, filtered, repo_root)
    if count == 0:
        raise SystemExit(f"no compile commands found for {repo_root}")
    print(f"repository compile database: {filtered} ({count} entries)")

    binary = install_mcp_language_server(cache_dir)
    command = bridge_command(binary, repo_root, clangd, filtered.parent)
    if not args.skip_smoke_test:
        sample_file = first_compile_file(filtered)
        if not sample_file:
            raise SystemExit(f"cannot select a semantic smoke-test file from {filtered}")
        tools = smoke_test(command, sample_file, timeout=args.smoke_timeout)
        print(f"MCP + clangd semantic smoke test passed: {', '.join(tools)}")

    requested = args.client or ["auto"]
    clients = [] if "none" in requested or args.skip_register else resolve_clients(requested)
    if not args.skip_register and "none" not in requested and not clients:
        raise SystemExit("no requested MCP client found; use --client none to prepare without registration")
    for client in clients:
        register_client(client, args.name, binary, repo_root, clangd, filtered.parent)
        print(f"registered {args.name} for {client}")

    if args.install_hook:
        if "claude" in clients:
            install_claude_hook(repo_root, filtered)
        else:
            print(
                "--install-hook currently supports Claude PreToolUse hooks only; "
                "for Codex or other MCP clients, use the manual compile_commands.json "
                "fix in references/lsp-bootstrap.md.",
                file=sys.stderr,
            )

    print("LSP bootstrap complete.")
    print("Warm up clangd with hover on a relevant file before the first global definition/reference query.")


if __name__ == "__main__":
    main()
