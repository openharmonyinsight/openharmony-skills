"""Durable ODK checkpoints and optimistic, incremental artifact writes.

This helper records observed results. It never runs skills, validates a document's
meaning, infers user consent, or treats a session log as a successful checkpoint.
All paths are relative to the change directory; inputs and watched source files
may live outside it. Outputs, evidence and document writes must stay inside it.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import uuid

try:
    from odk_repository import ODK_PHASES, phase_hooks
except ImportError:
    from .odk_repository import ODK_PHASES, phase_hooks

STATE = ".workflow.json"
VERSION = 1


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def fingerprint(path: Path) -> str:
    if path.is_symlink():
        raise ValueError(f"symlink is not a checkpoint file: {path}")
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except FileNotFoundError:
        return "missing"


def local_path(root: Path, name: str) -> Path:
    path = Path(name)
    if not name or path.is_absolute() or ".." in path.parts or path == Path("."):
        raise ValueError(f"expected a change-relative file path: {name}")
    current = root
    for part in path.parts:
        current /= part
        if current.is_symlink():
            raise ValueError(f"symlink is not an artifact target: {name}")
    if path.parts[0].startswith(".workflow"):
        raise ValueError("workflow bookkeeping is not an artifact")
    return root / path


def snapshots(root: Path, names: list[str], *, inputs=False) -> dict[str, str]:
    result = {}
    for name in names:
        if not isinstance(name, str) or not name or Path(name).is_absolute():
            raise ValueError("checkpoint paths must be relative to the change directory")
        path = root / name if inputs else local_path(root, name)
        result[name] = fingerprint(path)
    return result


def normalize_task_checkboxes(text: str) -> str:
    """Normalize task-list state while preserving code literals and other bytes.

    Markdown's four-space code threshold is relative to the current list item,
    not the start of the source line. Tabs affect columns, never stored bytes.
    """
    title_pattern = r'''(?:"(?:\\[^\r\n]|[^"\\])*"|'(?:\\[^\r\n]|[^'\\])*'|\((?:\\[^\r\n]|[^()\\])*\))'''
    reference_pattern = (r" {0,3}\[((?:\\[^\r\n]|[^\\[\]\r\n])+)\]:[ \t]*"
                         r"(<(?:\\[^\r\n]|[^<>\\\r\n])*>|(?:\\[^\s]|\\(?=\s|$)|[^\s<>\\])+)"
                         r"(?:[ \t]+(" + title_pattern + r"))?[ \t]*(?:\r?\n)?")

    def valid_reference(match):
        if not match or not match[1].strip() or len(match[1]) > 999:
            return False
        destination = match[2]
        if destination.startswith("<"):
            return True
        if any(ord(char) < 32 or ord(char) == 127 for char in destination):
            return False
        depth, index = 0, 0
        while index < len(destination):
            char = destination[index]
            if char == "\\" and index + 1 < len(destination):
                index += 2
                continue
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth < 0:
                    return False
            index += 1
        return depth == 0

    def interrupts_paragraph(body, *, any_ordered=False):
        stripped = body.lstrip(" ")
        if len(body) - len(stripped) > 3:
            return False
        compact = stripped.strip().replace(" ", "")
        if len(compact) >= 3 and set(compact) in ({"-"}, {"*"}, {"_"}):
            return True
        marker = re.match(r"([-+*]|[0-9]{1,9}[.)]) +\S", stripped)
        if marker and (marker[1] in "-+*" or any_ordered or int(marker[1][:-1]) == 1):
            return True
        opening = re.match(r"(`{3,}|~{3,})(.*)", stripped)
        return (bool(opening and (opening[1][0] != "`" or "`" not in opening[2]))
                or bool(re.match(r"#{1,6}(?: |\r?$)|>", stripped)) or stripped.startswith("<!--"))

    def html_block_end(body, paragraph):
        stripped = body.lstrip(" ")
        if len(body) - len(stripped) > 3:
            return False
        raw = re.match(r"<(pre|script|style|textarea)(?=[\s>]|$)", stripped, re.I)
        if raw:
            return r"</(?:pre|script|style|textarea)>"
        for prefix, ending in (("<!--", r"-->"), ("<?", r"\?>"), ("<![CDATA[", r"\]\]>")):
            if stripped.startswith(prefix):
                return ending
        if re.match(r"<![A-Z]", stripped):
            return r">"
        tags = ("address|article|aside|base|basefont|blockquote|body|caption|center|col|colgroup|dd|details|"
                "dialog|dir|div|dl|dt|fieldset|figcaption|figure|footer|form|frame|frameset|h[1-6]|head|"
                "header|hr|html|iframe|legend|li|link|main|menu|menuitem|nav|noframes|ol|optgroup|option|"
                "p|param|search|section|summary|table|tbody|td|tfoot|th|thead|title|tr|track|ul")
        if re.match(r"</?(?:" + tags + r")(?=[\s/>]|$)", stripped, re.I):
            return None  # Block tags continue until a blank line, including after </tag>.
        attribute = r"[A-Za-z_:][A-Za-z0-9_.:-]*(?:\s*=\s*(?:[^\s\"'=<>`]+|'[^']*'|\"[^\"]*\"))?"
        if not paragraph and re.fullmatch(r"(?:</[A-Za-z][A-Za-z0-9-]*\s*>|<[A-Za-z][A-Za-z0-9-]*"
                                          r"(?:\s+" + attribute + r")*\s*/?>)\s*", stripped):
            return None
        return False

    normalized, containers, fence, html, paragraph, reference_title = [], [], None, None, False, None
    empty_item = False
    for index, line in enumerate(text.splitlines(keepends=True)):
        inspected = line[1:] if index == 0 and line.startswith("\ufeff") else line
        expanded = inspected.expandtabs(4)
        if not expanded.strip():
            paragraph = False
            reference_title = None
            if empty_item and containers:
                containers.pop()  # A blank line terminates an empty list item.
            empty_item = False
            if html and html[0] is None:
                html = None
            normalized.append(line)
            continue
        indent = len(expanded) - len(expanded.lstrip(" "))
        previous = containers[:]
        while containers and indent < containers[-1]:
            containers.pop()
        base = containers[-1] if containers else 0
        if containers != previous:
            if (paragraph and not interrupts_paragraph(expanded[base:], any_ordered=True)
                    and html_block_end(expanded[base:], True) is False):
                containers = previous  # An unindented paragraph continuation is lazy.
                normalized.append(line)
                continue
            paragraph = False
        if fence and base < fence[1]:
            fence = None  # An outdent ends the containing list and its code block.
        if html and base < html[1]:
            html = None
        if fence:
            closing = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)", expanded[fence[1]:])
            if closing and closing[1][0] == fence[0][0] and len(closing[1]) >= len(fence[0]) and not closing[2].strip():
                fence = None
            normalized.append(line)
            continue
        if html:
            if html[0] is not None and re.search(html[0], expanded[html[1]:], re.I):
                html = None
            normalized.append(line)
            continue
        title_base, reference_title = reference_title, None
        if (title_base is not None and base >= title_base and re.fullmatch(
                r" {0,3}" + title_pattern + r"[ \t]*(?:\r?\n)?", expanded[base:])):
            normalized.append(line)
            continue
        if paragraph and re.fullmatch(r" {0,3}(?:=+|-+)[ \t]*(?:\r?\n)?", expanded[base:]):
            paragraph = False  # A setext underline closes its preceding paragraph.
            normalized.append(line)
            continue
        empty_item = False
        while True:
            body = expanded[base:]
            compact = body.strip().replace(" ", "")
            if len(compact) >= 3 and set(compact) in ({"-"}, {"*"}, {"_"}):
                break  # A thematic break is not a new list item.
            marker = re.match(r"^ {0,3}([-+*]|[0-9]{1,9}[.)])( +|(?=\r?$))", body)
            if not marker:
                break
            if paragraph and marker[1] not in "-+*" and int(marker[1][:-1]) != 1:
                break  # Ordered lists starting above 1 cannot interrupt a paragraph.
            padding = len(marker[2])
            empty_item = not body[marker.end():].strip()
            base += marker.start(2) + (padding if not empty_item and 1 <= padding <= 4 else 1)
            containers.append(base)
            paragraph = False
            if re.match(r"\[[ xX]\](?= )", expanded[base:]):
                offset = inspected.index("[") + 1 + len(line) - len(inspected)
                line = line[:offset] + " " + line[offset + 1:]
                break
        body = expanded[base:]
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)", body)
        html_end = html_block_end(body, paragraph)
        reference = not paragraph and re.fullmatch(reference_pattern, body)
        if html_end is not False:
            if html_end is None or not re.search(html_end, body, re.I):
                html = (html_end, base)
            paragraph = False
        elif valid_reference(reference):
            reference_title = base if reference[3] is None else None
            paragraph = False
        elif opening and (opening[1][0] != "`" or "`" not in opening[2]):
            fence = (opening[1], base)
            paragraph = False
        elif interrupts_paragraph(body):
            paragraph = False
        elif body.strip() and len(body) - len(body.lstrip(" ")) <= 3:
            paragraph = True
        normalized.append(line)
    return "".join(normalized)


def native_task_contracts(root: Path, names, *, archives=None) -> dict[str, str]:
    """Ignore only actual Markdown checklist state, preserving task definitions."""
    result = {}
    for name in names:
        if not isinstance(name, str) or not name or Path(name).is_absolute():
            raise ValueError("native task paths must be relative to the change directory")
        if Path(name).suffix.lower() != ".md":
            raise ValueError("native task progress requires a Markdown task file")
        archive = (archives or {}).get(name)
        path = local_path(root, archive["snapshot"]) if archive else root / name
        if fingerprint(path) == "missing":
            result[name] = "missing"
            continue
        normalized = normalize_task_checkboxes(path.read_bytes().decode("utf-8"))
        result[name] = hashlib.sha256(normalized.encode()).hexdigest()
    return result


def atomic_write(path: Path, content: bytes, *, create=False) -> None:
    descriptor, temporary = tempfile.mkstemp(prefix="." + path.name + ".", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            if path.exists():
                os.fchmod(stream.fileno(), stat.S_IMODE(path.stat().st_mode))
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if create:
            os.link(temporary, path)  # Never replace an existing target, even on a race.
        else:
            os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextmanager
def locked(root: Path):
    if not root.is_dir():
        raise ValueError("existing ODK change directory required")
    lock = root / ".workflow.lock"
    if lock.is_symlink() or (root / STATE).is_symlink():
        raise ValueError("workflow state/lock must not be symlinks")
    with lock.open("a+b") as stream:
        try:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise ValueError("another workflow writer is active; retry after it finishes") from error
        try:
            yield
        finally:
            fcntl.flock(stream, fcntl.LOCK_UN)


def read_state(root: Path) -> dict:
    path = root / STATE
    if path.is_symlink():
        raise ValueError("workflow state must not be a symlink")
    if not path.exists():
        return {"schema_version": VERSION, "invocations": {}}
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
        if (not isinstance(state, dict) or state.get("schema_version") != VERSION
                or not isinstance(state.get("invocations"), dict)):
            raise ValueError("unsupported workflow state schema")
        # Fail closed on incomplete/corrupt state instead of silently forgetting work.
        for run in state["invocations"].values():
            if (not isinstance(run, dict) or not isinstance(run.get("generation"), int)
                    or not isinstance(run.get("definition"), dict)
                    or not isinstance(run.get("steps"), list) or not run["steps"]
                    or not isinstance(run.get("inputs"), dict)
                    or not isinstance(run.get("outputs"), dict)
                    or not isinstance(run.get("watched"), dict)
                    or not isinstance(run.get("dependencies"), dict)):
                raise ValueError("incomplete workflow invocation")
            if any(step.get("status") not in {"pending", "running", "succeeded", "failed", "blocked"}
                   for step in run["steps"]):
                raise ValueError("invalid workflow step status")
            definition = run["definition"]
            if (definition.get("phase") not in ODK_PHASES
                    or not isinstance(definition.get("steps"), list)
                    or len(definition["steps"]) != len(run["steps"])
                    or not isinstance(definition.get("approval_required"), bool)):
                raise ValueError("invalid workflow definition")
            for index, step in enumerate(run["steps"]):
                if (step.get("index") != index or not isinstance(step.get("attempts"), list)
                        or any(step.get(field) != value for field, value in definition["steps"][index].items())
                        or (step["status"] != "pending" and not step["attempts"])
                        or (step["status"] == "succeeded" and not step.get("evidence"))
                        or (step["status"] == "running" and not step.get("token"))):
                    raise ValueError("inconsistent workflow step checkpoint")
        return state
    except (ValueError, TypeError, AttributeError) as error:
        raise ValueError(f"invalid {STATE}; preserve it and recover from a known checkpoint: {error}") from error


def save(root: Path, state: dict) -> None:
    atomic_write(root / STATE, (json.dumps(state, ensure_ascii=False, indent=2) + "\n").encode())


def native_archive_errors(root: Path, state: dict, names) -> list[str]:
    errors = []
    for name in names:
        archive = state.get("native_archives", {}).get(name)
        if not archive:
            continue
        try:
            if (root / archive["source_dir"]).exists():
                errors.append(f"finalized native workspace reappeared: {name}")
            actual = snapshots(root, list(archive["evidence"]))
            errors.extend(f"native archive evidence changed: {path}" for path, expected in archive["evidence"].items()
                          if actual[path] != expected)
            if fingerprint(local_path(root, archive["snapshot"])) != archive["sha256"]:
                errors.append(f"finalized native task snapshot changed: {name}")
        except (OSError, ValueError, KeyError, TypeError) as error:
            errors.append(f"native archive evidence invalid: {name}: {error}")
    return errors


def watched_snapshots(root: Path, state: dict, definition: dict) -> dict[str, str]:
    native = set(definition.get("native_tasks", []))
    archives = state.get("native_archives", {})
    return {name: fingerprint(local_path(root, archives[name]["snapshot"])) if name in native and name in archives
            else snapshots(root, [name], inputs=True)[name] for name in definition["watch"]}


def finalize_native_archive(root: Path, archive_result: str, *, reason: str) -> dict:
    """Freeze already verified task inputs after a proven native archive, preserving runs."""
    if not reason.strip():
        raise ValueError("native archive finalization requires a reconciliation reason")
    local_path(root, archive_result)
    try:
        from odk_native_archive import verify_archive
    except ImportError:
        from .odk_native_archive import verify_archive
    with locked(root):
        state = read_state(root)
        names = sorted({name for run in state["invocations"].values() for name in run["definition"].get("native_tasks", [])})
        existing = state.get("native_archives", {})
        # An accepted archive is historical evidence. Relocating/removing the
        # native archive directory later does not require replaying its operation.
        accepted = {name: record for name, record in existing.items() if archive_result in record["evidence"]}
        if accepted and not native_archive_errors(root, state, accepted):
            source_dirs = {(root / record["source_dir"]).resolve() for record in accepted.values()}
            uncovered = [name for name in names if name not in accepted
                         and any((root / name).resolve().is_relative_to(source) for source in source_dirs)]
            if uncovered:
                raise ValueError("new native task declarations are uncovered by this finalized archive; "
                                 "use its already verified logical task paths or reconcile the native inputs before archive: "
                                 + ", ".join(uncovered))
            return {"status": "finalized", "native_tasks": {name: record["snapshot"] for name, record in accepted.items()}}
        records = verify_archive(root, names, archive_result)
        for name, record in records.items():
            record["source_dir"] = str(Path(name).parent)
            for run in state["invocations"].values():
                if name in run["definition"].get("native_tasks", []) and run["watched"].get(name) != record["sha256"]:
                    raise ValueError("native archive does not match the task bytes accepted by every checkpoint")
            if name in existing:
                raise ValueError("recorded native archive evidence changed; recover its original verified evidence")
        for name, record in records.items():
            state.setdefault("native_archives", {})[name] = {**record, "reason": reason, "finalized_at": now()}
        save(root, state)
        return {"status": "finalized", "native_tasks": {name: record["snapshot"] for name, record in records.items()}}


def _shared_updates(run: dict, parent: dict, step: dict, outputs: dict,
                    watched: dict, task_contracts: dict) -> dict:
    shared_tasks = set(run["definition"].get("native_tasks", [])) & set(parent["definition"].get("native_tasks", []))
    updates = {}
    for field, current, basis_field in (("outputs", outputs, "output_basis"), ("watched", watched, "watched_basis")):
        shared = set(current) & set(parent[field])
        if field == "watched":
            shared &= shared_tasks
        if any(step.get(basis_field, {}).get(name) != parent[field][name] for name in shared):
            raise ValueError("original upstream baseline changed")
        updates[field] = {name: current[name] for name in shared}
    if not any(updates.values()):
        raise ValueError("backfill requires shared declared outputs or native task progress")
    for name in updates["watched"]:
        if (task_contracts.get(name) == "missing" or task_contracts.get(name) != parent.get("task_contracts", {}).get(name)):
            raise ValueError("native task definitions changed; revalidate the planning contract")
    return updates


def _recovery_probe(root: Path, state: dict, key: str, step: dict) -> dict:
    """Scope reconciled partial output to its consumer, without accepting it globally."""
    probe = deepcopy(state)
    run = state["invocations"][key]
    for parent_key in step["backfill_recovery"]["parents"]:
        if parent_key not in run["dependencies"]:
            raise ValueError("recovery backfill source must be a declared dependency")
        parent = state["invocations"][parent_key]
        if parent["generation"] != run["dependencies"][parent_key]:
            raise ValueError("recovery upstream generation or original output baseline changed")
        updates = _shared_updates(run, parent, step, run["outputs"], run["watched"],
                                  native_task_contracts(root, run["definition"].get("native_tasks", []), archives=state.get("native_archives")))
        for field, values in updates.items():
            probe["invocations"][parent_key][field].update(values)
    return probe


def view(root: Path, state: dict, key: str, visiting=None, memo=None) -> dict:
    memo = {} if memo is None else memo
    if visiting and key in visiting:
        raise ValueError("circular workflow dependency")
    if key in memo:
        return memo[key]
    run = state["invocations"].get(key)
    if run is None:
        return {"key": key, "status": "untracked", "next_step": None, "stale_reasons": []}
    visiting = set() if visiting is None else set(visiting)
    if key in visiting:
        raise ValueError("circular workflow dependency")
    visiting.add(key)
    definition = run["definition"]
    pending = next((step for step in run["steps"] if step["status"] != "succeeded"), None)
    recovery = pending.get("backfill_recovery") if pending else None
    reasons = []
    reasons.extend(native_archive_errors(root, state, definition.get("native_tasks", [])))
    if phase_hooks(definition["phase"])["steps"] != definition["steps"]:
        reasons.append("configured hook order changed")
    for label, expected, input_files in (("input", run["inputs"], True),
                                          ("output", run["outputs"], False),
                                          ("watched file", run["watched"], True)):
        actual = watched_snapshots(root, state, definition) if label == "watched file" else snapshots(root, list(expected), inputs=input_files)
        reasons.extend(f"{label} changed: {name}" for name in expected if expected[name] != actual[name])
    for step in run["steps"]:
        if step["status"] == "succeeded":
            expected = step["evidence"]
            actual = snapshots(root, list(expected))
            reasons.extend(f"evidence changed: {name}" for name in expected if expected[name] != actual[name])
    for backfill in run.get("backfills", []):
        expected = backfill["evidence"]
        actual = snapshots(root, list(expected))
        reasons.extend(f"backfill evidence changed: {name}" for name in expected if expected[name] != actual[name])
    if recovery:
        expected = recovery["evidence"]
        actual = snapshots(root, list(expected))
        reasons.extend(f"recovery evidence changed: {name}" for name in expected if expected[name] != actual[name])
    recovery_probe, recovery_memo = None, {}
    for dependency, generation in run["dependencies"].items():
        parent = view(root, state, dependency, visiting, memo)
        if parent["status"] != "succeeded" and recovery and dependency in recovery["parents"]:
            try:
                if recovery_probe is None:
                    recovery_probe = _recovery_probe(root, state, key, pending)
                parent = view(root, recovery_probe, dependency, visiting, recovery_memo)
            except ValueError as error:
                reasons.append(f"shared-output recovery is stale: {error}")
        if parent["status"] != "succeeded" or parent.get("generation") != generation:
            reasons.append(f"dependency is not current: {dependency}")
    result = "succeeded" if pending is None else pending["status"]
    if result == "succeeded" and definition["approval_required"] and not run.get("approval"):
        result = "awaiting_approval"
    memo[key] = {"key": key, "phase": definition["phase"], "generation": run["generation"],
                 "status": "stale" if reasons else result, "stale_reasons": reasons,
                 "next_step": deepcopy(pending), "approval": run.get("approval")}
    return memo[key]


def status(root: Path, key: str | None = None) -> dict:
    state = read_state(root)
    if key is not None:
        return view(root, state, key)
    memo = {}
    return {"schema_version": VERSION, "native_archives": deepcopy(state.get("native_archives", {})),
            "invocations": {name: view(root, state, name, memo=memo)
            for name in state["invocations"]}}


def prepare(root: Path, phase: str, *, action="", inputs=(), outputs=(), watch=(), native_tasks=(), depends_on=(),
            approval_required=False, restart_reason="", backfill_from=(), evidence=()) -> dict:
    if phase not in ODK_PHASES:
        raise ValueError("prepare one canonical phase at a time; expand composite bridges first")
    if not isinstance(action, str) or any(char in action for char in "\r\n"):
        raise ValueError("invalid action identity")
    key = phase + (":" + action if action else "")
    definition = {"phase": phase, "action": action, "steps": phase_hooks(phase)["steps"],
                  "inputs": sorted(set(inputs)), "outputs": sorted(set(outputs)),
                  "watch": sorted(set(watch) | set(native_tasks)), "native_tasks": sorted(set(native_tasks)),
                  "depends_on": sorted(set(depends_on)), "approval_required": approval_required}
    if set(inputs) & (set(outputs) | set(watch) | set(native_tasks)):
        raise ValueError("a fixed input cannot also be an output or watched mutable file")
    with locked(root):
        state = read_state(root)
        archive_errors = native_archive_errors(root, state, definition["native_tasks"])
        if archive_errors:
            raise ValueError(str(archive_errors))
        previous = state["invocations"].get(key)
        if backfill_from and not restart_reason.strip():
            raise ValueError("shared-artifact restart requires a reconciliation reason")
        current = view(root, state, key)
        if previous and previous["definition"] != definition:
            current["status"] = "stale"
            current["stale_reasons"].append("invocation definition changed")
        if previous and not restart_reason:
            return current
        if previous and any(step["status"] == "running" for step in previous["steps"]):
            raise ValueError("running outcome is unknown; reconcile and retry it before replacing the invocation")
        recovery = None
        recovery_basis = None
        dependency_state = state
        if backfill_from:
            if not previous or not restart_reason.strip() or not evidence:
                raise ValueError("shared-artifact restart requires a previous invocation, reason and evidence")
            fields = ("phase", "action", "inputs", "outputs", "watch", "native_tasks", "depends_on", "approval_required")
            if any(previous["definition"].get(field, []) != definition[field] for field in fields):
                raise ValueError("shared-artifact restart cannot change the invocation scope")
            proof = snapshots(root, list(evidence))
            if "missing" in proof.values():
                raise ValueError("restart reconciliation evidence is missing")
            recovery = {"parents": list(dict.fromkeys(backfill_from)), "evidence": proof, "reason": restart_reason}
            unfinished = next((step for step in previous["steps"] if step["status"] != "succeeded"), {})
            recovery_basis = {
                "output_basis": deepcopy(unfinished.get("output_basis", previous["outputs"])),
                "watched_basis": deepcopy(unfinished.get("watched_basis", previous["watched"])),
            }
            dependency_state = deepcopy(state)
            recovering = dependency_state["invocations"][key]
            recovering["outputs"] = snapshots(root, definition["outputs"])
            recovering["watched"] = watched_snapshots(root, state, definition)
            basis = {**recovery_basis, "backfill_recovery": recovery}
            dependency_state = _recovery_probe(root, dependency_state, key, basis)
        dependencies = {}
        for parent in definition["depends_on"]:
            if parent == key:
                raise ValueError("circular workflow dependency")
            parent_view = view(root, dependency_state, parent)
            if parent_view["status"] != "succeeded":
                raise ValueError(f"dependency must be current and succeeded: {parent}")
            dependencies[parent] = parent_view["generation"]
        generation = previous["generation"] + 1 if previous else 1
        history = previous.get("history", []) + [{k: v for k, v in previous.items() if k != "history"}] if previous else []
        source = snapshots(root, definition["inputs"], inputs=True)
        if "missing" in source.values():
            raise ValueError("declared input file is missing; resolve prerequisites before preparing")
        state["invocations"][key] = {
            "generation": generation, "definition": definition,
            "inputs": source,
            "outputs": snapshots(root, definition["outputs"]), "dependencies": dependencies,
            "watched": watched_snapshots(root, state, definition),
            "task_contracts": native_task_contracts(root, definition["native_tasks"], archives=state.get("native_archives")),
            "steps": [{**step, "index": index, "status": "pending", "attempts": []}
                      for index, step in enumerate(definition["steps"])],
            "history": history, "restart_reason": restart_reason, "prepared_at": now(),
        }
        if recovery:
            for step in state["invocations"][key]["steps"]:
                step.update(backfill_recovery=deepcopy(recovery), **deepcopy(recovery_basis))
                if step["kind"] == "phase":
                    break
        result = view(root, state, key)  # Reject cycles before publishing any state.
        save(root, state)
        return result


def checked_run(root: Path, state: dict, key: str) -> tuple[dict, dict]:
    current = view(root, state, key)
    if current["status"] in {"untracked", "stale"}:
        raise ValueError(f"{current['status']} invocation {key}: {current['stale_reasons']}")
    return state["invocations"][key], current


def start(root: Path, key: str) -> dict:
    with locked(root):
        state = read_state(root)
        run, current = checked_run(root, state, key)
        if current["status"] != "pending":
            raise ValueError(f"cannot start {current['status']} invocation; running outcomes are unknown until reconciled")
        step = run["steps"][current["next_step"]["index"]]
        token = uuid.uuid4().hex
        if not step.get("backfill_recovery"):
            step["output_basis"] = deepcopy(run["outputs"])
            step["watched_basis"] = deepcopy(run["watched"])
        step.update(status="running", token=token)
        step["attempts"].append({"token": token, "status": "running", "started_at": now()})
        save(root, state)
        return {"key": key, "token": token, "step": deepcopy(step)}


def _verification_snapshot(root: Path, state: dict, key: str, token: str) -> dict:
    run = state["invocations"].get(key)
    if run is None or not any(step["status"] == "running" and step.get("token") == token for step in run["steps"]):
        raise ValueError("verification token does not match a running step")
    archive_errors = native_archive_errors(root, state, run["definition"].get("native_tasks", []))
    if archive_errors:
        raise ValueError(str(archive_errors))
    return {"key": key, "token": token, "generation": run["generation"],
            "inputs": snapshots(root, list(run["inputs"]), inputs=True),
            "outputs": snapshots(root, list(run["outputs"])),
            "watched": watched_snapshots(root, state, run["definition"]),
            "task_contracts": native_task_contracts(root, run["definition"].get("native_tasks", []), archives=state.get("native_archives"))}


def verification_snapshot(root: Path, key: str, token: str) -> dict:
    """Capture BEFORE executing verification; finish compares it under the writer lock."""
    with locked(root):
        return _verification_snapshot(root, read_state(root), key, token)


def _backfill(state: dict, key: str, step: dict, parents: list[str], outputs: dict,
              proof: dict, reason: str, *, watched: dict, task_contracts: dict) -> None:
    """Explicitly accept verified, contract-preserving downstream artifact backfill.

    The coordinator checks the semantic diff. This records that decision and its
    evidence; it does not infer that a changed contract has user approval.
    """
    run = state["invocations"][key]
    if step["kind"] != "phase" or not reason.strip():
        raise ValueError("backfill requires a verified phase body and a contract-preservation reason")
    for parent_key in dict.fromkeys(parents):
        if parent_key not in run["dependencies"]:
            raise ValueError("backfill source must be a declared upstream dependency")
        parent = state["invocations"][parent_key]
        if parent["generation"] != run["dependencies"][parent_key]:
            raise ValueError("backfill upstream generation changed")
        updates = _shared_updates(run, parent, step, outputs, watched, task_contracts)
        changed = {field: {name: value for name, value in values.items() if parent[field][name] != value}
                   for field, values in updates.items()}
        previous = {field: {name: parent[field][name] for name in values} for field, values in changed.items()}
        if not any(changed.values()):
            raise ValueError("no changed shared artifact to backfill")
        parent["backfills"] = parent.get("backfills", []) + [{
            "by": key, "generation": run["generation"], "token": step["token"],
            "previous": previous["outputs"], "updated": changed["outputs"],
            "previous_watched": previous["watched"], "updated_watched": changed["watched"],
            "reason": reason, "evidence": proof, "recorded_at": now(),
        }]
        for field, values in changed.items():
            parent[field].update(values)


def finish(root: Path, key: str, token: str, result: str, *, evidence=(), reason="",
           verified=None, backfill_from=()) -> dict:
    if result not in {"succeeded", "failed", "blocked"}:
        raise ValueError("result must be succeeded, failed or blocked")
    with locked(root):
        state = read_state(root)
        if key not in state["invocations"]:
            raise ValueError("untracked invocation")
        run = state["invocations"][key]
        step = next((step for step in run["steps"] if step["status"] == "running"), None)
        if step is None or step.get("token") != token:
            raise ValueError("attempt token does not match the running step")
        observed = _verification_snapshot(root, state, key, token)
        if result == "succeeded":
            if step["kind"] != "pre_hook" and "missing" in observed["task_contracts"].values():
                raise ValueError("declared native task file is missing")
            if verified is None:
                raise ValueError("successful steps require a verification snapshot taken before verification")
            if verified != observed:
                raise ValueError("files changed since verification snapshot; verify the current versions again")
        elif backfill_from:
            raise ValueError("only successful verified phase bodies may backfill upstream outputs")
        proof = snapshots(root, list(evidence))
        if any(value == "missing" for value in proof.values()) or (result == "succeeded" and not proof):
            raise ValueError("successful steps require existing evidence files")
        # Outputs may intentionally change during the action. Inputs, dependencies
        # and already accepted evidence must remain valid throughout the attempt.
        probe = deepcopy(state)
        probe["invocations"][key]["outputs"] = observed["outputs"]
        probe["invocations"][key]["watched"] = observed["watched"]
        probe["invocations"][key]["task_contracts"] = observed["task_contracts"]
        if backfill_from:
            _backfill(probe, key, step, list(backfill_from), observed["outputs"], proof, reason,
                      watched=observed["watched"], task_contracts=observed["task_contracts"])
        if view(root, probe, key)["status"] == "stale":
            raise ValueError("stale inputs/dependencies/evidence; reconcile before recording success")
        outputs = observed["outputs"]
        if step["kind"] == "post_hook" and (outputs != run["outputs"]
                or probe["invocations"][key]["watched"] != run["watched"]):
            raise ValueError("post-hook changed artifacts/source; reconcile and restart phase checks")
        if result == "succeeded" and step["kind"] != "pre_hook" and "missing" in outputs.values():
            raise ValueError("phase output is missing")
        if result != "succeeded" and not reason.strip():
            raise ValueError("failed/blocked steps require an actionable reason")
        if backfill_from:
            _backfill(state, key, step, list(backfill_from), outputs, proof, reason,
                      watched=observed["watched"], task_contracts=observed["task_contracts"])
        step.update(status=result, evidence=proof, reason=reason)
        step["attempts"][-1].update(status=result, evidence=proof, reason=reason, verified=verified, finished_at=now())
        run["outputs"] = outputs
        run["watched"] = probe["invocations"][key]["watched"]
        run["task_contracts"] = observed["task_contracts"]
        save(root, state)
        return view(root, state, key)


def retry(root: Path, key: str, reason: str, evidence: list[str], *, backfill_from=()) -> dict:
    if not reason.strip() or not evidence:
        raise ValueError("retry requires a reconciliation reason and evidence, especially for unknown side effects")
    with locked(root):
        state = read_state(root)
        if key not in state["invocations"]:
            raise ValueError("untracked invocation")
        run = state["invocations"][key]
        step = next((step for step in run["steps"] if step["status"] != "succeeded"), None)
        pending_reconciliation = bool(step and step["status"] == "pending" and step["attempts"] and backfill_from)
        if step is None or (step["status"] not in {"running", "failed", "blocked"} and not pending_reconciliation):
            raise ValueError("no interrupted/failed step to retry")
        proof = snapshots(root, evidence)
        if "missing" in proof.values():
            raise ValueError("reconciliation evidence is missing")
        if backfill_from:
            if step["kind"] != "phase":
                raise ValueError("shared-output recovery requires an interrupted phase body")
            step["backfill_recovery"] = {"parents": list(dict.fromkeys(backfill_from)), "evidence": proof, "reason": reason}
            run["outputs"] = snapshots(root, list(run["outputs"]))
            run["watched"] = watched_snapshots(root, state, run["definition"])
            _recovery_probe(root, state, key, step)  # Validate the original receipt before saving.
        step["attempts"][-1].update(reconciliation=reason, reconciliation_evidence=proof,
                                   reconciled_at=now(), status="unknown" if step["status"] == "running"
                                   else step["attempts"][-1]["status"])
        step.update(status="pending", token=None)
        # Only an interrupted pre-hook/body can acknowledge its own partial
        # writes here. Edits after a recorded result, or during post-hooks, must
        # invalidate prior body verification rather than silently refresh it.
        if step["attempts"][-1]["status"] == "unknown" and step["kind"] != "post_hook":
            run["outputs"] = snapshots(root, list(run["outputs"]))
            run["watched"] = watched_snapshots(root, state, run["definition"])
        save(root, state)
        return view(root, state, key)


def approve(root: Path, key: str, reference: str) -> dict:
    if not reference.strip():
        raise ValueError("approval requires the actual user confirmation reference")
    with locked(root):
        state = read_state(root)
        run, current = checked_run(root, state, key)
        if current["status"] not in {"succeeded", "awaiting_approval"}:
            raise ValueError("only completed, current invocations can be approved")
        run["approval"] = {"reference": reference, "generation": run["generation"],
                           "outputs": run["outputs"], "recorded_at": now()}
        save(root, state)
        return view(root, state, key)


def patch_document(root: Path, name: str, expected: str, edits: list[dict]) -> dict:
    with locked(root):
        path = local_path(root, name)
        before = fingerprint(path)
        if before == "missing" or before != expected:
            raise ValueError("artifact changed or is missing; reread and reconcile before patching")
        body = path.read_bytes().decode("utf-8")  # Preserve CRLF and UTF-8 BOM verbatim.
        original = body
        if not isinstance(edits, list) or not edits:
            raise ValueError("provide a nonempty list of incremental old/new edits")
        for edit in edits:
            if not isinstance(edit, dict):
                raise ValueError("each incremental edit must be an old/new object")
            old, new = edit.get("old"), edit.get("new")
            if (not isinstance(old, str) or not isinstance(new, str) or not old
                    or old == body or body.count(old) != 1):
                raise ValueError("each old fragment must match once; whole-document replacement is forbidden")
            body = body.replace(old, new, 1)
        # Detect a non-cooperating editor as late as possible. Cooperating
        # writers hold the same lock; arbitrary external writers must be paused.
        if fingerprint(path) != before:
            raise ValueError("artifact changed during patch; reread and reconcile")
        if body != original:
            atomic_write(path, body.encode())
        return {"path": name, "sha256": fingerprint(path)}


def create_document(root: Path, name: str, content: str) -> dict:
    with locked(root):
        path = local_path(root, name)
        if path.exists():
            raise ValueError("artifact already exists; read and patch it instead")
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            atomic_write(path, content.encode(), create=True)
        except FileExistsError as error:
            raise ValueError("artifact appeared during creation; read and patch it instead") from error
        return {"path": name, "sha256": fingerprint(path)}


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("status", "prepare", "start", "snapshot", "finish", "retry", "approve", "fingerprint", "patch", "create", "finalize-native-archive"):
        entry = sub.add_parser(command)
        entry.add_argument("change_dir", type=Path)
        if command in {"start", "snapshot", "finish", "retry", "approve"}:
            entry.add_argument("--key", required=True)
        if command == "status":
            entry.add_argument("--key")
        if command == "prepare":
            entry.add_argument("--phase", required=True, choices=ODK_PHASES)
            entry.add_argument("--action", default="")
            for name in ("input", "output", "watch", "depends-on"):
                entry.add_argument("--" + name, action="append", default=[])
            entry.add_argument("--native-task", action="append", default=[])
            entry.add_argument("--backfill-from", action="append", default=[])
            entry.add_argument("--evidence", action="append", default=[])
            entry.add_argument("--approval-required", action="store_true")
            entry.add_argument("--restart-reason", default="")
        if command == "finish":
            entry.add_argument("--result", required=True, choices=("succeeded", "failed", "blocked"))
            entry.add_argument("--verified-file", type=Path)
            entry.add_argument("--backfill-from", action="append", default=[])
        if command == "retry":
            entry.add_argument("--backfill-from", action="append", default=[])
        if command in {"snapshot", "finish"}:
            entry.add_argument("--token", required=True)
        if command in {"retry", "finish"}:
            entry.add_argument("--evidence", action="append", default=[])
            entry.add_argument("--reason", default="")
        if command == "approve":
            entry.add_argument("--reference", required=True)
        if command in {"fingerprint", "patch", "create"}:
            entry.add_argument("--target", required=True)
        if command == "patch":
            entry.add_argument("--expected", required=True)
            entry.add_argument("--edits-file", required=True, type=Path)
        if command == "create":
            entry.add_argument("--content-file", required=True, type=Path)
        if command == "finalize-native-archive":
            entry.add_argument("--archive-result", required=True)
            entry.add_argument("--reason", required=True)
    args = parser.parse_args(argv)
    root = args.change_dir.resolve()
    try:
        if not root.is_dir():
            raise ValueError("existing ODK change directory required")
        if args.command == "status":
            result = status(root, args.key)
        elif args.command == "prepare":
            result = prepare(root, args.phase, action=args.action, inputs=args.input, outputs=args.output,
                             watch=args.watch, native_tasks=args.native_task,
                             depends_on=args.depends_on, approval_required=args.approval_required,
                             restart_reason=args.restart_reason, backfill_from=args.backfill_from, evidence=args.evidence)
        elif args.command == "start":
            result = start(root, args.key)
        elif args.command == "snapshot":
            result = verification_snapshot(root, args.key, args.token)
        elif args.command == "finish":
            verified = json.loads(args.verified_file.read_text(encoding="utf-8")) if args.verified_file else None
            result = finish(root, args.key, args.token, args.result, evidence=args.evidence, reason=args.reason,
                            verified=verified, backfill_from=args.backfill_from)
        elif args.command == "retry":
            result = retry(root, args.key, args.reason, args.evidence, backfill_from=args.backfill_from)
        elif args.command == "approve":
            result = approve(root, args.key, args.reference)
        elif args.command == "fingerprint":
            result = {"path": args.target, "sha256": fingerprint(local_path(root, args.target))}
        elif args.command == "patch":
            result = patch_document(root, args.target, args.expected, json.loads(args.edits_file.read_text(encoding="utf-8")))
        elif args.command == "create":
            result = create_document(root, args.target, args.content_file.read_bytes().decode("utf-8"))
        else:
            result = finalize_native_archive(root, args.archive_result, reason=args.reason)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, KeyError) as error:
        print(f"ODK workflow error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
