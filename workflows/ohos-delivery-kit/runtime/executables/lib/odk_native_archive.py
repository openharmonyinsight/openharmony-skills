"""Verify OpenSpec final capture and a native archive before freezing task inputs."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re


def digest(path: Path) -> str:
    if path.is_symlink():
        raise ValueError(f"archive evidence must not be a symlink: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evidence_path(root: Path, name: str) -> Path:
    path = Path(name)
    if not name or path.is_absolute() or ".." in path.parts or path == Path("."):
        raise ValueError("archive evidence must be inside the ODK change")
    current = root
    for part in path.parts:
        current /= part
        if current.is_symlink():
            raise ValueError("archive evidence must not traverse symlinks")
    return root / path


def verify_archive(root: Path, native_names: list[str], receipt_name: str) -> dict[str, dict]:
    binding_path = evidence_path(root, "openspec-binding.json")
    receipt_path = evidence_path(root, receipt_name)
    binding = json.loads(binding_path.read_text(encoding="utf-8"))
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if not isinstance(binding, dict) or not isinstance(receipt, dict):
        raise ValueError("native binding and archive result must be JSON objects")
    if binding.get("state_owner") != "openspec" or binding.get("state") != "all_done":
        raise ValueError("archive finalization requires a final all_done native capture")
    change = binding.get("change", "")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", change):
        raise ValueError("unsupported native archive change identity")
    snapshot_hash = binding.get("snapshot_sha256", "")
    if not re.fullmatch(r"[0-9a-f]{64}", snapshot_hash):
        raise ValueError("invalid final snapshot digest")
    snapshot_name = binding.get("snapshot", "")
    if snapshot_name != f"evidence/openspec/{snapshot_hash}":
        raise ValueError("final snapshot must be the captured immutable evidence directory")
    snapshot = evidence_path(root, snapshot_name)
    manifest_path = evidence_path(root, snapshot_name + "/manifest.json")
    if digest(manifest_path) != snapshot_hash:
        raise ValueError("final snapshot manifest changed")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or not isinstance(manifest.get("apply"), dict):
        raise ValueError("invalid final native snapshot manifest")
    if (manifest.get("change") != change or manifest.get("store") != binding.get("store")
            or manifest.get("apply", {}).get("state") != "all_done"):
        raise ValueError("final capture identity/state does not match its binding")
    archive = receipt.get("archive", {})
    if not isinstance(archive, dict):
        raise ValueError("native archive result has no archive object")
    archived_as = archive.get("archivedAs", "")
    if (archive.get("change") != change or not re.fullmatch(r"\d{4}-\d{2}-\d{2}-" + re.escape(change), archived_as)
            or not isinstance(archive.get("path"), str) or not Path(archive["path"]).is_absolute()):
        raise ValueError("native archive result does not identify the captured change")
    archive_root = Path(archive["path"]).resolve()
    if not archive_root.is_dir() or archive_root.name != archived_as:
        raise ValueError("native archive directory is missing or inconsistent")
    if not isinstance(binding.get("project"), str):
        raise ValueError("missing capture project")
    native_root_name = binding.get("native_root")
    if native_root_name is None and binding.get("store") is not None:
        raise ValueError("selected-store archives require a final capture with its resolved native root")
    native_root = (root / (native_root_name if native_root_name is not None else binding["project"])).resolve()
    sources = manifest.get("sources", {})
    if not isinstance(sources, dict):
        raise ValueError("invalid native snapshot sources")
    proof = {"openspec-binding.json": digest(binding_path), receipt_name: digest(receipt_path),
             snapshot_name + "/manifest.json": snapshot_hash}
    records, workspaces = {}, set()
    for blob, source in sources.items():
        if not isinstance(source, dict) or not isinstance(source.get("path"), str):
            raise ValueError("invalid captured native source")
        if not re.fullmatch(r"[A-Za-z0-9_-]+-\d+\.md", blob):
            raise ValueError("invalid captured native blob name")
        source_path = Path(source["path"])
        if source_path.is_absolute() or ".." in source_path.parts:
            raise ValueError("captured native source escaped its root")
        frozen = evidence_path(root, snapshot_name + "/" + blob)
        if digest(frozen) != source["sha256"]:
            raise ValueError("final captured native content changed")
        proof[str(frozen.relative_to(root))] = source["sha256"]
        if not re.fullmatch(r"tasks-\d+\.md", blob):
            continue
        live = (native_root / source_path).resolve()
        original_change = live.parent
        if original_change.name != change or archive_root != (original_change.parent / "archive" / archived_as).resolve():
            raise ValueError("native archive location does not match the original task workspace")
        if original_change.exists():
            raise ValueError("native change still exists; archive was not completed")
        workspaces.add(original_change)
        for other in sources.values():
            original = (native_root / other["path"]).resolve()
            if original.is_relative_to(original_change):
                archived_file = archive_root / original.relative_to(original_change)
                if digest(archived_file) != other["sha256"]:
                    raise ValueError("archived native files differ from the final capture")
        for name in native_names:
            if (root / name).resolve() == live:
                records[name] = {"snapshot": str(frozen.relative_to(root)), "sha256": source["sha256"],
                                 "source_dir": str(original_change), "change": change,
                                 "snapshot_sha256": snapshot_hash}
    unmatched = [name for name in native_names if name not in records
                 and any((root / name).resolve().is_relative_to(workspace) for workspace in workspaces)]
    if unmatched:
        raise ValueError("unmatched native task declarations in the captured archive: " + ", ".join(unmatched))
    if not records:
        raise ValueError("no declared native tasks match the final captured archive")
    return {name: {**record, "evidence": proof} for name, record in records.items()}
