#!/usr/bin/env python3
"""Small YAML readers for ODK's constrained contract files.

This intentionally avoids PyYAML so validation works in clean shell
environments. It only parses the small YAML subset used by
core/contracts/*.yaml and core/adapters/*.yaml.
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


def main() -> None:
    parser = argparse.ArgumentParser()
    subcommands = parser.add_subparsers(dest="command", required=True)

    contract = subcommands.add_parser("contract-artifacts")
    contract.add_argument("path")

    adapter = subcommands.add_parser("adapter-commands")
    adapter.add_argument("path")

    conditional = subcommands.add_parser("conditional-section-keys")
    conditional.add_argument("path")

    args = parser.parse_args()
    if args.command == "contract-artifacts":
        contract_artifacts(args.path)
    elif args.command == "adapter-commands":
        adapter_commands(args.path)
    elif args.command == "conditional-section-keys":
        conditional_section_keys(args.path)


if __name__ == "__main__":
    main()
