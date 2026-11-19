"""Compile the same delivery contract for agents and the document validator.

Readers deliberately support the shipped, constrained YAML formats. Unknown
profiles, malformed selections and invalid graph references fail explicitly.
Natural-language instructions remain guidance, not claims of semantic checking.
"""
from __future__ import annotations

import copy
import re
from pathlib import Path

if __package__:
    from .odk_yaml import parse_contract_artifacts, parse_resource_contract, contract_version, _unquote
    from .odk_document import require_unique_section, require_unique_table_with_columns, meaningful
    from .odk_involvement import DIMENSIONS, involvement_rows, involvement_value, canonical_dimension
else:
    from odk_yaml import parse_contract_artifacts, parse_resource_contract, contract_version, _unquote
    from odk_document import require_unique_section, require_unique_table_with_columns, meaningful
    from odk_involvement import DIMENSIONS, involvement_rows, involvement_value, canonical_dimension

RISK_DIMENSIONS = {"API/SDK", "安全/权限", "IPC/跨进程", "数据迁移", "性能"}
LEVELS = {"lite", "standard", "critical"}
PHASES = {"define": "proposal", "specify": "spec", "design": "design", "plan": "execution-plan"}
LITE_SECTIONS = {
    "proposal": ["背景与问题", "初始分级判断", "目标", "非目标", "成功标准", "影响范围",
                 "外部依赖", "资源开销审视", "不涉及项确认"],
    "spec": ["概述", "用户故事或场景", "异常与边界规则", "兼容性声明", "验证映射", "API 规格定义"],
    "execution-plan": ["输入状态", "AC 到 Task 追溯", "实现边界", "禁止项", "Task 列表", "Task 详情", "代码范围映射"],
}


def string_list(value: str) -> list[str]:
    value = re.split(r"\s+#", value, maxsplit=1)[0].strip()
    if not (value.startswith("[") and value.endswith("]")):
        raise ValueError("expected an inline YAML list")
    if value == "[]":
        return []
    values = [_unquote(part.strip()) for part in value[1:-1].split(",")]
    if any(not re.fullmatch(r"[A-Za-z0-9_-]+", v) for v in values):
        raise ValueError("invalid list entry")
    if len(values) != len(set(values)):
        raise ValueError("duplicate list entry")
    return values


def profile_selection(path: Path) -> list[str]:
    if not path.exists():
        return []
    result: list[str] = []
    seen = False
    in_list = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"profiles:\s*(.*)", line)
        if match:
            if seen:
                raise ValueError(f"{path}: duplicate profiles key")
            seen = True
            in_list = not match[1] or match[1].startswith("#")
            if not in_list:
                result = string_list(match[1])
        elif in_list and re.match(r"\s+- ", line):
            result.extend(string_list("[" + line.strip()[2:] + "]"))
        elif line and not line[0].isspace():
            in_list = False
        elif in_list:
            raise ValueError(f"{path}: malformed profiles list")
    if len(set(result)) != len(result):
        raise ValueError(f"{path}: duplicate profile")
    return result


def read_profile(path: Path) -> dict:
    if not path.is_file():
        raise ValueError(f"unknown profile: {path.stem}")
    profile = {"id": path.stem, "priority": 100, "overrides": {}, "instructions": {}}
    block = phase = field = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        top = re.fullmatch(r"([a-z_]+):\s*(.*)", line)
        if top:
            block, value = top.groups()
            phase = field = None
            if block == "priority":
                profile["priority"] = int(value)
            continue
        if block == "template_overrides":
            match = re.fullmatch(r"  ([a-z-]+):", line)
            if match:
                phase = match[1]
                if phase not in {"proposal", "spec", "design", "execution-plan"}:
                    raise ValueError(f"{path}: unknown override artifact {phase}")
                profile["overrides"][phase] = {}
                field = None
                continue
            match = re.fullmatch(r"    ([a-z_]+):\s*(.*)", line)
            if match and phase:
                field, value = match.groups()
                if field not in {"required_dimensions", "additional_sections", "additional_ac_categories",
                                 "additional_prohibitions", "fragments"}:
                    raise ValueError(f"{path}: unsupported profile field {field}")
                profile["overrides"][phase][field] = string_list(value) if value else []
                continue
            if phase and field:
                match = re.fullmatch(r"      - (.+)", line)
                if match:
                    if field == "fragments":
                        file_match = re.fullmatch(r"file:\s*(.+)", match[1])
                        if not file_match:
                            raise ValueError(f"{path}: malformed fragment")
                        profile["overrides"][phase][field].append({"file": _unquote(file_match[1])})
                    else:
                        profile["overrides"][phase][field].append(_unquote(match[1]))
                    continue
                match = re.fullmatch(r"        strategy:\s*(.+)", line)
                if match and field == "fragments":
                    profile["overrides"][phase][field][-1]["strategy"] = _unquote(match[1])
                    continue
            raise ValueError(f"{path}: unsupported override syntax: {line.strip()}")
        elif block == "agent_instructions":
            match = re.fullmatch(r"  ([a-z]+):\s*>", line)
            if match:
                phase = match[1]
                profile["instructions"][phase] = ""
            elif phase and line.startswith("    "):
                profile["instructions"][phase] += line.strip() + "\n"
            else:
                raise ValueError(f"{path}: unsupported instruction syntax")
    return profile


def validate_dependencies(artifacts: dict) -> None:
    visiting, visited = set(), set()

    def visit(name):
        if name in visiting:
            raise ValueError(f"artifact dependency cycle at {name}")
        if name in visited:
            return
        visiting.add(name)
        for dependency in artifacts[name].get("requires", []):
            if dependency not in artifacts:
                raise ValueError(f"{name}: unknown dependency {dependency}")
            visit(dependency)
        visiting.remove(name)
        visited.add(name)

    for name in artifacts:
        visit(name)


def _require_artifact(artifacts: dict, name: str) -> dict:
    """Return the named artifact node or raise a ValueError naming it.

    The CLI's ``--effective-contract`` path catches ``ValueError`` and exits 1,
    so callers must avoid bare ``KeyError`` for missing required nodes.
    """
    if name not in artifacts:
        raise ValueError(f"contract is missing required artifact: {name}")
    return artifacts[name]


def frontmatter_level(text: str) -> str:
    if not text.startswith("---\n"):
        return "standard"
    header = text.split("\n---", 1)[0]
    values = re.findall(r"^delivery_level:[ \t]*(.*)$", header, re.M)
    if len(values) > 1:
        raise ValueError("duplicate delivery_level")
    level = _unquote(re.split(r"\s+#", values[0], maxsplit=1)[0]) if values else "standard"
    if level not in LEVELS:
        raise ValueError("delivery_level must be lite, standard or critical")
    return level


def repository_root(change_dir: Path) -> Path:
    change_dir = change_dir.resolve()
    if change_dir.parent.parent.name != "changes" or change_dir.parent.parent.parent.name != "codespec":
        raise ValueError("change directory layout must be exactly codespec/changes/<repo-name>/<proposal-id-or-draft>")
    return change_dir.parent.parent.parent.parent


def compile_contract(change_dir: Path, contract_path: Path, *, phase: str | None = None,
                     submission: bool = False) -> dict:
    artifacts = copy.deepcopy(parse_contract_artifacts(str(contract_path)))
    validate_dependencies(artifacts)
    proposal_path = change_dir / "proposal.md"
    proposal = proposal_path.read_text(encoding="utf-8") if proposal_path.is_file() else ""
    level = frontmatter_level(proposal.replace("\r\n", "\n"))
    ids = profile_selection(repository_root(change_dir) / "codespec/profile.yaml")
    profiles = sorted((read_profile(contract_path.parent.parent / "profiles" / (p + ".yaml"))
                       for p in ids), key=lambda p: (p["priority"], p["id"]))
    if level == "lite":
        _require_artifact(artifacts, "design")["required"] = "false"
        execution_plan = _require_artifact(artifacts, "execution-plan")
        requires = execution_plan.setdefault("requires", [])
        if "design" in requires:
            requires.remove("design")
        for name, sections in LITE_SECTIONS.items():
            _require_artifact(artifacts, name)["required_sections"] = list(sections)

    for name, artifact in artifacts.items():
        artifact.update(dimensions=[], dimension_policy="explicit-assessment-with-reason",
                        ac_categories=[], prohibitions=[], fragments=[], instructions=[], profile_sections=[])
        for profile in profiles:
            overrides = profile["overrides"].get(name, {})
            for source, target in (("required_dimensions", "dimensions"),
                                   ("additional_sections", "required_sections"),
                                   ("additional_ac_categories", "ac_categories"),
                                   ("additional_prohibitions", "prohibitions")):
                for item in overrides.get(source, []):
                    if item not in artifact[target]:
                        artifact[target].append(item)
            artifact["profile_sections"].extend(overrides.get("additional_sections", []))
            instruction = profile["instructions"].get(artifact.get("phase"))
            if instruction:
                artifact["instructions"].append(instruction.strip())
            for fragment in overrides.get("fragments", []):
                path = (contract_path.parent.parent / "profiles" / fragment["file"]).resolve()
                if not path.is_relative_to((contract_path.parent.parent / "profiles").resolve()):
                    raise ValueError("profile fragment escapes profile root")
                if not path.is_file() or fragment.get("strategy") not in {"prepend", "append", "wrap"}:
                    raise ValueError(f"invalid profile fragment: {path}")
                artifact["fragments"].append({**fragment, "path": str(path)})

    involvement = involvement_rows(proposal)
    for row in involvement:
        row["维度"] = canonical_dimension(row.get("维度", ""))
    risks = {row["维度"] for row in involvement
             if involvement_value(row.get("是否涉及", "")) != "否" and row["维度"] in RISK_DIMENSIONS}
    resource_contract = parse_resource_contract(str(contract_path))
    active_states = set(resource_contract.get("active_when_states", ["required"]))
    # Cache the section/table parse results once; the lite branch and signal
    # computation reuse them instead of re-scanning the proposal (P1).
    resource_section = require_unique_section(proposal, "资源开销审视")
    resource_active = any(row.get("状态", "").strip() in active_states for row in (
        require_unique_table_with_columns(resource_section or "", ["维度", "状态"]) or []))
    signals = {"resource-active": resource_active}
    for trigger, label in (("security", "安全/权限"), ("i18n", "国际化")):
        # Look up directly from the already-parsed, canonicalized involvement
        # rows instead of re-calling parse_eight_dim_involvement (P1).
        signals[trigger] = next(
            (involvement_value(row.get("是否涉及", "")) for row in involvement
             if row.get("维度") == label), None) == "是"
    for artifact in artifacts.values():
        for title, condition in artifact.get("conditions", {}).items():
            trigger = condition.get("trigger")
            if trigger and trigger not in signals:
                raise ValueError(f"unknown condition trigger: {trigger}")
            condition["evaluation"] = "machine" if trigger else "manual"
            condition["active"] = signals.get(trigger)
            if condition["active"] and title not in artifact["required_sections"]:
                artifact["required_sections"].append(title)
    if level == "lite":
        if any(row.get("维度") in {"国际化", "构建/组件"}
               and involvement_value(row.get("是否涉及", "")) != "否" for row in involvement):
            raise ValueError("lite requires host-only, device-independent scope; use standard/critical for build/i18n work")
        declared = {row["维度"] for row in involvement if involvement_value(row.get("是否涉及", "")) == "否"}
        risk_rows = [row for row in involvement if row.get("维度") in RISK_DIMENSIONS]
        if (risks or RISK_DIMENSIONS - declared or len(risk_rows) != len(RISK_DIMENSIONS)
                or any(not meaningful(row.get("依据", "")) for row in risk_rows)):
            raise ValueError("lite requires explicit 否 for API/SDK, 安全/权限, IPC/跨进程, 数据迁移 and 性能; use standard/critical")
        resources = resource_section or ""
        if re.search(r"\|\s*(required|review-required)\s*\|", resources):
            raise ValueError("lite cannot waive active resource review; use standard/critical")
        external_deps = require_unique_section(proposal, "外部依赖") or ""
        if any((r.get("子系统", "") != "不涉及") for r in (
                require_unique_table_with_columns(
                    external_deps, ["子系统", "仓库", "模块/路径", "依赖类型"]) or [])):
            raise ValueError("lite requires no cross-repository dependencies; use standard/critical")
        if not meaningful(external_deps):
            raise ValueError("lite must declare external dependencies not applicable with a reason")
        design = change_dir / "design.md"
        if design.is_file():
            text = design.read_text(encoding="utf-8")
            if re.search(r"^### (?:DFX 故障模式处置|AD-)", text, re.M):
                raise ValueError("lite cannot drop existing FMEA dispositions; use standard/critical")
    if level == "critical":
        _require_artifact(artifacts, "design")["required_sections"].append("状态归属与不变量")
        _require_artifact(artifacts, "spec-for-validation")["required"] = "true"
        if "安全/权限" in risks:
            _require_artifact(artifacts, "threat-model")["required"] = "true"
    if submission:
        # External design-docs contract always requires all five base files.
        _require_artifact(artifacts, "design")["required"] = "true"
        _require_artifact(artifacts, "metadata-tracking")["required"] = "true"
    if phase:
        if phase not in PHASES:
            raise ValueError(f"unknown phase: {phase}")
        selected = set()

        def select(name):
            if name in selected:
                return
            selected.add(name)
            for dependency in artifacts[name]["requires"]:
                select(dependency)

        select(PHASES[phase])
        artifacts = {name: item for name, item in artifacts.items() if name in selected}
    return {"contract_version": contract_version(str(contract_path)), "delivery_level": level,
            "profiles": [p["id"] for p in profiles], "artifacts": artifacts}
