#!/usr/bin/env python3
"""Small YAML readers for ODK's constrained contract files.

This intentionally avoids PyYAML so validation works in clean shell
environments. It only parses the small YAML subset used by ODK contract and
adapter files, independent of source or installed layout.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def _lines(path: str) -> list[str]:
    return Path(path).read_text(encoding="utf-8").splitlines()


def parse_contract_artifacts(path: str) -> dict[str, dict[str, object]]:
    artifacts: dict[str, dict[str, object]] = {}
    current: str | None = None
    mode: str | None = None
    in_artifacts = False

    for raw in _lines(path):
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line == "artifacts:":
            in_artifacts = True
            continue
        if in_artifacts and re.match(r"^\S", line):
            break
        if not in_artifacts:
            continue

        artifact = re.match(r"^  ([A-Za-z0-9_-]+):$", line)
        if artifact:
            current = artifact.group(1)
            artifacts[current] = {
                "file": "",
                "template": "",
                "required": "true",
                "required_sections": [],
                "conditional_sections": [],
            }
            mode = None
            continue
        if current is None:
            continue

        key_value = re.match(r"^    (file|template):\s*(.+)$", line)
        if key_value:
            artifacts[current][key_value.group(1)] = _unquote(key_value.group(2))
            continue
        required = re.match(r"^    required:\s*(true|false)$", line)
        if required:
            artifacts[current]["required"] = required.group(1)
            continue
        if line == "    required_sections:":
            mode = "required_sections"
            continue
        if line == "    conditional_sections:":
            mode = "conditional_sections"
            continue
        section = re.match(r"^      - (.+)$", line)
        if section and mode == "required_sections":
            artifacts[current][mode].append(_unquote(section.group(1)))  # type: ignore[index]
            continue
        conditional = re.match(r"^      - section:\s*(.+)$", line)
        if conditional and mode == "conditional_sections":
            artifacts[current][mode].append(_unquote(conditional.group(1)))  # type: ignore[index]

    if not artifacts:
        raise ValueError(
            f"{path}: parsed 0 artifacts. The contract may be missing the "
            "'artifacts:' key or reformatted (indentation/quoting) beyond what "
            "the lightweight parser supports — restore formatting or use a real YAML loader."
        )

    return artifacts


def parse_resource_contract(path: str) -> dict[str, str | list[str]]:
    """Parse the flat scalar/list resource_contract block."""

    result: dict[str, str | list[str]] = {}
    current_list: str | None = None
    in_contract = False
    for raw in _lines(path):
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line == "resource_contract:":
            in_contract = True
            continue
        if in_contract and re.match(r"^\S", line):
            break
        if not in_contract:
            continue

        list_key = re.match(r"^  ([A-Za-z0-9_]+):$", line)
        if list_key:
            current_list = list_key.group(1)
            result[current_list] = []
            continue
        scalar = re.match(r"^  ([A-Za-z0-9_]+):\s*(.+)$", line)
        if scalar:
            current_list = None
            result[scalar.group(1)] = _unquote(scalar.group(2))
            continue
        item = re.match(r"^    -\s*(.+)$", line)
        if item and current_list:
            values = result[current_list]
            if isinstance(values, list):
                values.append(_unquote(item.group(1)))

    if not result:
        raise ValueError(f"{path}: missing or empty resource_contract block")
    return result


def validate_resource_contract_schema(contract: dict[str, str | list[str]]) -> list[str]:
    """Validate the executable shape of the thin resource contract."""

    issues: list[str] = []
    scalar_keys = ("proposal_section", "evidence_root")
    list_keys = (
        "dimension_labels",
        "impact_states",
        "proposal_columns",
        "active_when_states",
        "conditional_sections",
    )
    for key in scalar_keys:
        if not isinstance(contract.get(key), str) or not str(contract.get(key)).strip():
            issues.append(f"resource_contract.{key} must be a non-empty scalar")
    for key in list_keys:
        value = contract.get(key)
        if not isinstance(value, list) or not value:
            issues.append(f"resource_contract.{key} must be a non-empty list")
        elif len(value) != len(set(value)):
            issues.append(f"resource_contract.{key} contains duplicate values")

    dimensions = contract.get("dimension_labels")
    dimension_keys: set[str] = set()
    dimension_names: set[str] = set()
    if isinstance(dimensions, list):
        for item in dimensions:
            if item.count("=") != 1:
                issues.append(f"invalid resource dimension mapping: {item}")
                continue
            key, label = (part.strip() for part in item.split("=", 1))
            if not re.fullmatch(r"[a-z][a-z0-9_-]*", key) or not label:
                issues.append(f"invalid resource dimension mapping: {item}")
                continue
            if key in dimension_keys or label in dimension_names:
                issues.append(f"duplicate resource dimension key or label: {item}")
            dimension_keys.add(key)
            dimension_names.add(label)

    states = contract.get("impact_states")
    active_states = contract.get("active_when_states")
    if isinstance(states, list) and isinstance(active_states, list):
        unknown = set(active_states) - set(states)
        if unknown:
            issues.append(
                "resource_contract.active_when_states contains unknown states: "
                + ", ".join(sorted(unknown))
            )

    sections = contract.get("conditional_sections")
    section_files: set[str] = set()
    section_headings: set[str] = set()
    if isinstance(sections, list):
        for item in sections:
            if item.count("=") != 1:
                issues.append(f"invalid resource conditional section mapping: {item}")
                continue
            file_name, heading = (part.strip() for part in item.split("=", 1))
            if not file_name.endswith(".md") or not heading:
                issues.append(f"invalid resource conditional section mapping: {item}")
                continue
            if file_name in section_files or heading in section_headings:
                issues.append(f"duplicate resource conditional section mapping: {item}")
            section_files.add(file_name)
            section_headings.add(heading)

    evidence_root = contract.get("evidence_root")
    if isinstance(evidence_root, str):
        evidence_path = Path(evidence_root)
        if evidence_path.is_absolute() or ".." in evidence_path.parts:
            issues.append("resource_contract.evidence_root must be a repo-relative path")
    return issues


def _markdown_table_headers(text: str) -> list[list[str]]:
    lines = text.splitlines()
    result: list[list[str]] = []
    for index in range(len(lines) - 1):
        if not lines[index].lstrip().startswith("|"):
            continue
        header = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
        separator = [cell.strip() for cell in lines[index + 1].strip().strip("|").split("|")]
        if len(header) == len(separator) and separator and all(
            re.fullmatch(r":?-{3,}:?", cell) for cell in separator
        ):
            result.append(header)
    return result


def _heading_section(text: str, heading: str) -> str:
    match = re.search(
        rf"^##\s+{re.escape(heading)}\s*$([\s\S]*?)(?=^##\s+|\Z)",
        text,
        flags=re.MULTILINE,
    )
    return match.group(1) if match else ""


def contract_artifacts(path: str) -> None:
    artifacts = parse_contract_artifacts(path)
    for name, data in artifacts.items():
        print(f"artifact\t{name}\t{data['file']}\t{data['template']}")
        for section in data["required_sections"]:  # type: ignore[index]
            print(f"required_section\t{name}\t{section}")
        for section in data["conditional_sections"]:  # type: ignore[index]
            print(f"conditional_section\t{name}\t{section}")


def conditional_section_keys(path: str) -> None:
    """Print `template_basename|section` for every conditional section.

    Single source of truth consumed by check-examples.sh so conditional
    section exemptions stay in sync with artifacts.yaml.
    """
    artifacts = parse_contract_artifacts(path)
    for _, data in artifacts.items():
        template = str(data.get("template", ""))
        template_base = Path(template).name if template else ""
        for section in data["conditional_sections"]:  # type: ignore[index]
            print(f"{template_base}|{section}")


def validate_resource_templates(path: str, templates_root: str) -> list[str]:
    """Ensure resource conditional headings stay aligned (no column/schema drift)."""

    contract = parse_resource_contract(path)
    artifacts = parse_contract_artifacts(path)
    issues = validate_resource_contract_schema(contract)
    if issues:
        return issues

    def values(key: str) -> list[str]:
        value = contract.get(key)
        return value if isinstance(value, list) else []

    sections: dict[str, str] = {}
    for item in values("conditional_sections"):
        if "=" in item:
            file_name, heading = item.split("=", 1)
            sections[file_name] = heading

    root = Path(templates_root)
    for file_name, heading in sections.items():
        artifact = next(
            (data for data in artifacts.values() if data.get("file") == file_name),
            None,
        )
        declared_sections = artifact.get("conditional_sections", []) if artifact else []
        if heading not in declared_sections:
            issues.append(f"{file_name} resource section differs between contract declarations")
        template = root / file_name
        if not template.is_file():
            issues.append(f"missing resource template: {file_name}")
            continue
        text = template.read_text(encoding="utf-8")
        if f"## {heading}" not in text:
            issues.append(f"{file_name} resource heading differs from contract")
    proposal_section = contract.get("proposal_section")
    if isinstance(proposal_section, str) and proposal_section:
        proposal = root / "proposal.md"
        if not proposal.is_file():
            issues.append("missing resource template: proposal.md")
        else:
            proposal_text = proposal.read_text(encoding="utf-8")
            section_text = _heading_section(proposal_text, proposal_section)
            if not section_text:
                issues.append("proposal.md resource heading differs from contract")
            expected_columns = values("proposal_columns")
            if expected_columns not in _markdown_table_headers(section_text):
                issues.append("proposal.md resource table columns differ from contract")
            expected_labels = {
                item.split("=", 1)[1] for item in values("dimension_labels")
            }
            first_cells = {
                line.strip().strip("|").split("|", 1)[0].strip()
                for line in section_text.splitlines()
                if line.lstrip().startswith("|")
            }
            missing_labels = expected_labels - first_cells
            if missing_labels:
                issues.append(
                    "proposal.md resource table missing dimensions: "
                    + ", ".join(sorted(missing_labels))
                )
    return issues


def resource_template_check(path: str, templates_root: str) -> int:
    issues = validate_resource_templates(path, templates_root)
    for issue in issues:
        print(issue)
    return 1 if issues else 0


def adapter_commands(path: str) -> None:
    current: dict[str, object] | None = None
    mode: str | None = None
    commands: list[dict[str, object]] = []

    for raw in _lines(path):
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line == "mapping:":
            break
        command = re.match(r"^  - name:\s*(.+)$", line)
        if command:
            current = {
                "name": _unquote(command.group(1)),
                "source_capability": "",
                "fallback": [],
            }
            commands.append(current)
            mode = None
            continue
        if current is None:
            continue
        source = re.match(r"^    source_capability:\s*(.+)$", line)
        if source:
            current["source_capability"] = _unquote(source.group(1))
            mode = None
            continue
        if line == "    fallback:":
            mode = "fallback"
            continue
        fallback = re.match(r"^      -\s*(.+)$", line)
        if fallback and mode == "fallback":
            current["fallback"].append(_unquote(fallback.group(1)))  # type: ignore[index]

    for command in commands:
        fallbacks = ",".join(command["fallback"])  # type: ignore[arg-type]
        print(f"{command['name']}\t{command['source_capability']}\t{fallbacks}")


def main() -> int:
    parser = argparse.ArgumentParser()
    subcommands = parser.add_subparsers(dest="command", required=True)

    contract = subcommands.add_parser("contract-artifacts")
    contract.add_argument("path")

    adapter = subcommands.add_parser("adapter-commands")
    adapter.add_argument("path")

    conditional = subcommands.add_parser("conditional-section-keys")
    conditional.add_argument("path")

    resource_templates = subcommands.add_parser("validate-resource-templates")
    resource_templates.add_argument("path")
    resource_templates.add_argument("templates_root")

    args = parser.parse_args()
    if args.command == "contract-artifacts":
        contract_artifacts(args.path)
    elif args.command == "adapter-commands":
        adapter_commands(args.path)
    elif args.command == "conditional-section-keys":
        conditional_section_keys(args.path)
    elif args.command == "validate-resource-templates":
        return resource_template_check(args.path, args.templates_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
