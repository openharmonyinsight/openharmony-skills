#!/usr/bin/env python3
"""
Heuristic checker for OpenHarmony API-document consistency rules.

This script focuses on the stable parts that are worth automating:
- public/system document placement for @systemapi
- field presence for @syscap, @permission, @atomicservice, model-only tags
- deprecation markers, replacement links, and replacement anchor validity
- section-level and document-level error-code coverage for @throws BusinessError
- public/system doc naming, title, Readme entry, and link-direction rules
- basic version marker checks such as module since notes and <sup>x+</sup> usage

It intentionally does not attempt to fully validate prose quality or
implementation-level semantic completeness.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


TAG_RE = re.compile(r"@([A-Za-z0-9_]+)(?:\s+(.*))?$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
ERROR_CODE_HEADING_RE = re.compile(r"^##\s+(\d+)\b")
DECL_RE = re.compile(
    r"^(?:export\s+)?(?:declare\s+)?(?:(namespace|class|interface|enum|function|const|type)\s+([A-Za-z0-9_.$]+))"
)
METHOD_RE = re.compile(r"^\s*([A-Za-z0-9_]+)\s*\(")

DEFAULT_RULES_FILE = Path(__file__).with_name("doc_check_rules.json")


@dataclass
class Rules:
    model_text: dict[str, list[str]]
    system_title_marker: str
    mixed_module_note: str
    error_required_blocks: list[str]
    forbidden_permission_connectors: list[str]


@dataclass
class Symbol:
    full_name: str
    short_name: str
    kind: str
    tags: dict[str, list[str]] = field(default_factory=dict)
    throws: list[int] = field(default_factory=list)
    line: int = 0


@dataclass
class Section:
    heading: str
    level: int
    line: int
    body: str


@dataclass
class Finding:
    severity: str
    location: str
    message: str


def load_rules(path: Path | None) -> Rules:
    rule_path = path or DEFAULT_RULES_FILE
    data = json.loads(rule_path.read_text(encoding="utf-8"))
    return Rules(
        model_text=data["model_text"],
        system_title_marker=data["system_title_marker"],
        mixed_module_note=data["mixed_module_note"],
        error_required_blocks=data["error_required_blocks"],
        forbidden_permission_connectors=data["forbidden_permission_connectors"],
    )


def infer_readme_path(public_doc: Path | None, system_doc: Path | None) -> Path | None:
    base = None
    if public_doc and public_doc.exists():
        base = public_doc.parent
    elif system_doc and system_doc.exists():
        base = system_doc.parent
    if not base:
        return None
    for name in ("Readme-CN.md", "README-CN.md"):
        candidate = base / name
        if candidate.exists():
            return candidate
    return None


def add_tag(symbol: Symbol, key: str, value: str) -> None:
    symbol.tags.setdefault(key.lower(), []).append(value.strip())


def parse_comment_block(lines: list[str]) -> tuple[dict[str, list[str]], list[int]]:
    tags: dict[str, list[str]] = {}
    throws: list[int] = []
    for raw in lines:
        text = raw.strip()
        text = re.sub(r"^\*\s?", "", text)
        match = TAG_RE.search(text)
        if not match:
            continue
        key = match.group(1).lower()
        value = (match.group(2) or "").strip()
        tags.setdefault(key, []).append(value)
        if key == "throws":
            code_match = re.search(r"\b(\d{3,})\b", value)
            if code_match:
                throws.append(int(code_match.group(1)))
    return tags, throws


def parse_dts(path: Path) -> list[Symbol]:
    lines = path.read_text(encoding="utf-8").splitlines()
    symbols: list[Symbol] = []
    pending_comments: list[str] = []
    in_comment = False
    scope_stack: list[tuple[str, int]] = []
    brace_depth = 0

    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("/**"):
            in_comment = True
            pending_comments = []
            continue
        if in_comment:
            if "*/" in stripped:
                in_comment = False
            else:
                pending_comments.append(stripped)
            continue

        open_count = line.count("{")
        close_count = line.count("}")

        decl = DECL_RE.match(stripped)
        if decl:
            kind = decl.group(1)
            name = decl.group(2)
            full_name = ".".join([item[0] for item in scope_stack] + [name])
            symbol = Symbol(full_name=full_name, short_name=name.split(".")[-1], kind=kind, line=lineno)
            tags, throws = parse_comment_block(pending_comments)
            symbol.tags = tags
            symbol.throws = throws
            symbols.append(symbol)
            pending_comments = []
            if kind in {"namespace", "class", "interface", "enum"} and "{" in line:
                scope_stack.append((name, brace_depth + open_count - close_count))
        else:
            method = METHOD_RE.match(line)
            if method and scope_stack and scope_stack[-1][0]:
                container = scope_stack[-1][0]
                kind = "method"
                name = method.group(1)
                full_name = ".".join([item[0] for item in scope_stack] + [name])
                tags, throws = parse_comment_block(pending_comments)
                if tags or throws:
                    symbols.append(
                        Symbol(
                            full_name=full_name,
                            short_name=name,
                            kind=kind,
                            tags=tags,
                            throws=throws,
                            line=lineno,
                        )
                    )
                pending_comments = []

        brace_depth += open_count - close_count
        while scope_stack and brace_depth < scope_stack[-1][1]:
            scope_stack.pop()

    return symbols


def parse_sections(path: Path) -> list[Section]:
    lines = path.read_text(encoding="utf-8").splitlines()
    headings: list[tuple[int, int, str]] = []
    for lineno, line in enumerate(lines, start=1):
        match = HEADING_RE.match(line)
        if match:
            headings.append((lineno, len(match.group(1)), match.group(2).strip()))

    sections: list[Section] = []
    for idx, (lineno, level, heading) in enumerate(headings):
        start = lineno
        end = headings[idx + 1][0] - 1 if idx + 1 < len(headings) else len(lines)
        body = "\n".join(lines[start:end])
        sections.append(Section(heading=heading, level=level, line=lineno, body=body))
    return sections


def parse_error_codes(path: Path | None) -> set[int]:
    if not path or not path.exists():
        return set()
    codes: set[int] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = ERROR_CODE_HEADING_RE.match(line.strip())
        if match:
            codes.add(int(match.group(1)))
    return codes


def parse_error_code_sections(path: Path | None) -> dict[int, str]:
    if not path or not path.exists():
        return {}
    lines = path.read_text(encoding="utf-8").splitlines()
    sections: dict[int, str] = {}
    current_code: int | None = None
    current_lines: list[str] = []
    for line in lines:
        match = ERROR_CODE_HEADING_RE.match(line.strip())
        if match:
            if current_code is not None:
                sections[current_code] = "\n".join(current_lines)
            current_code = int(match.group(1))
            current_lines = [line]
            continue
        if current_code is not None:
            current_lines.append(line)
    if current_code is not None:
        sections[current_code] = "\n".join(current_lines)
    return sections


def parse_doc_title(path: Path | None) -> tuple[int, str] | None:
    if not path or not path.exists():
        return None
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        match = HEADING_RE.match(line)
        if match and len(match.group(1)) == 1:
            return lineno, match.group(2).strip()
    return None


def parse_module_since_from_doc(path: Path | None) -> int | None:
    if not path or not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    match = re.search(r"从API version\s+(\d+)\s+开始支持", text)
    if match:
        return int(match.group(1))
    match = re.search(r"API Version\s+(\d+)", text, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


def extract_sup_versions(text: str) -> set[int]:
    versions: set[int] = set()
    for match in re.finditer(r"<sup>\s*(\d+)\+\s*</sup>", text):
        versions.add(int(match.group(1)))
    return versions


def parse_symbol_since_versions(symbol: Symbol) -> list[int]:
    versions: list[int] = []
    for raw in symbol.tags.get("since", []):
        match = re.match(r"(\d+)", raw.strip())
        if match:
            versions.append(int(match.group(1)))
    return versions


def parse_error_codes_from_section(section: Section) -> set[int]:
    codes: set[int] = set()
    in_error_block = False
    for line in section.body.splitlines():
        if "**错误码" in line:
            in_error_block = True
            continue
        if in_error_block:
            row = re.match(r"^\|\s*(\d{3,})\s*\|", line.strip())
            if row:
                codes.add(int(row.group(1)))
            elif line.strip().startswith("**") and "错误码" not in line:
                break
    return codes


def parse_readme_entries(path: Path | None) -> tuple[list[str], list[str]]:
    if not path or not path.exists():
        return [], []
    normal: list[str] = []
    deleted: list[str] = []
    in_del = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if "<!--Del-->" in line:
            in_del = True
            continue
        if "<!--DelEnd-->" in line:
            in_del = False
            continue
        match = re.search(r"\(([^)]+\.md)\)", line)
        if not match:
            continue
        target = match.group(1)
        if in_del:
            deleted.append(target)
        else:
            normal.append(target)
    return normal, deleted


def extract_markdown_links(path: Path | None) -> list[tuple[int, str]]:
    if not path or not path.exists():
        return []
    links: list[tuple[int, str]] = []
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        for match in pattern.finditer(line):
            links.append((lineno, match.group(1).strip()))
    return links


def normalize_anchor(text: str) -> str:
    lowered = text.lower()
    lowered = re.sub(r"<sup>.*?</sup>", "", lowered)
    lowered = re.sub(r"\(deprecated\)", "", lowered)
    lowered = re.sub(r"[^a-z0-9\u4e00-\u9fff-]+", "", lowered)
    return lowered


def normalize_link_anchor(text: str) -> str:
    normalized = normalize_anchor(text)
    normalized = re.sub(r"\d+$", "", normalized)
    return normalized


def build_anchor_index(path: Path | None) -> set[str]:
    if not path or not path.exists():
        return set()
    anchors: set[str] = set()
    for section in parse_sections(path):
        anchors.add(normalize_anchor(section.heading))
    return anchors


def check_doc_links(path: Path | None) -> list[Finding]:
    findings: list[Finding] = []
    if not path or not path.exists():
        return findings
    current_anchors = build_anchor_index(path)
    for lineno, target in extract_markdown_links(path):
        if target.startswith("http://") or target.startswith("https://"):
            continue
        if target.startswith("#"):
            anchor = normalize_link_anchor(target[1:])
            if anchor and anchor not in current_anchors:
                findings.append(
                    Finding(
                        "warning",
                        f"{path}:{lineno}",
                        f"In-page anchor '{target}' does not resolve to a known heading in the same document.",
                    )
                )
            continue

        relative = target.split("#", 1)[0]
        anchor = target.split("#", 1)[1] if "#" in target else ""
        # Ignore image/assets and obvious non-markdown links.
        if relative and not relative.endswith(".md"):
            continue
        target_path = (path.parent / relative).resolve() if relative else path
        if not target_path.exists():
            findings.append(Finding("warning", f"{path}:{lineno}", f"Relative Markdown link target '{target}' does not exist."))
            continue
        if anchor:
            anchors = build_anchor_index(target_path)
            normalized_anchor = normalize_link_anchor(anchor)
            if normalized_anchor and normalized_anchor not in anchors:
                findings.append(
                    Finding(
                        "warning",
                        f"{path}:{lineno}",
                        f"Relative Markdown link anchor '{target}' does not resolve in {target_path.name}.",
                    )
                )
            continue
    return findings


def find_replacement_links(section: Section) -> list[str]:
    links: list[str] = []
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for match in pattern.finditer(section.body):
        links.append(match.group(1).strip())
    return links


def check_permission_connector_style(section: Section, rules: Rules) -> list[str]:
    issues: list[str] = []
    for line in section.body.splitlines():
        if "需要权限" not in line:
            continue
        lowered = line.lower()
        if any(f" {connector.lower()} " in lowered for connector in rules.forbidden_permission_connectors):
            issues.append(line.strip())
    return issues


def heading_matches(section: Section, name: str) -> bool:
    heading = section.heading.lower()
    target = re.escape(name.lower())
    return bool(re.search(rf"(^|[^a-z0-9_]){target}([^a-z0-9_]|$)", heading))


def find_sections_for_symbol(sections: list[Section], symbol: Symbol) -> list[Section]:
    matched = [section for section in sections if heading_matches(section, symbol.short_name)]
    if matched:
        return matched
    if symbol.kind in {"enum", "interface", "class", "type"}:
        return [section for section in sections if heading_matches(section, symbol.full_name.split(".")[-1])]
    return []


def section_text(sections: list[Section]) -> str:
    return "\n".join(f"{section.heading}\n{section.body}" for section in sections)


def contains_any(text: str, needles: list[str]) -> bool:
    lowered = text.lower()
    return any(needle.lower() in lowered for needle in needles)


def check_system_placement(
    symbol: Symbol,
    public_sections: list[Section],
    system_sections: list[Section],
    overloaded_names: set[str],
) -> list[Finding]:
    findings: list[Finding] = []
    if symbol.short_name in overloaded_names:
        return findings
    in_public = bool(find_sections_for_symbol(public_sections, symbol))
    in_system = bool(find_sections_for_symbol(system_sections, symbol))
    is_system = "systemapi" in symbol.tags

    if is_system and in_public:
        findings.append(Finding("error", f"{symbol.full_name}:{symbol.line}", "System API appears in public API documentation."))
    if not is_system and in_system and not in_public:
        findings.append(Finding("error", f"{symbol.full_name}:{symbol.line}", "Public symbol appears only in system API documentation."))
    return findings


def check_section_fields(symbol: Symbol, sections: list[Section], rules: Rules) -> list[Finding]:
    findings: list[Finding] = []
    if not sections:
        return findings
    combined = section_text(sections)
    detailed_field_kinds = {"function", "method", "type"}

    if symbol.kind in detailed_field_kinds and "syscap" in symbol.tags and "systemcapability." not in combined.lower():
        findings.append(Finding("error", f"{symbol.full_name}:{symbol.line}", "Missing system capability field in documentation section."))

    if symbol.kind in detailed_field_kinds and "atomicservice" in symbol.tags and "原子化服务api" not in combined.lower():
        findings.append(Finding("error", f"{symbol.full_name}:{symbol.line}", "Missing atomic service field in documentation section."))

    for tag_name, literals in rules.model_text.items():
        if symbol.kind in detailed_field_kinds and tag_name in symbol.tags and not contains_any(combined, literals):
            findings.append(Finding("error", f"{symbol.full_name}:{symbol.line}", f"Missing model constraint text for @{tag_name}."))

    if symbol.kind in detailed_field_kinds and "permission" in symbol.tags and "需要权限" not in combined:
        findings.append(Finding("error", f"{symbol.full_name}:{symbol.line}", "Missing required permission field in documentation section."))

    if symbol.kind in detailed_field_kinds and "deprecated" in symbol.tags:
        if "(deprecated)" not in combined.lower():
            findings.append(Finding("error", f"{symbol.full_name}:{symbol.line}", "Missing deprecated marker in documentation section."))
        if "useinstead" in symbol.tags:
            replacements = symbol.tags["useinstead"]
            normalized = []
            for item in replacements:
                normalized.append(item)
                if "#" in item:
                    normalized.append(item.split("#", 1)[1])
                normalized.append(item.split(".")[-1])
            if not contains_any(combined, normalized):
                findings.append(Finding("error", f"{symbol.full_name}:{symbol.line}", "Missing replacement reference required by @useinstead."))
    return findings


def check_replacement_link_targets(
    symbol: Symbol,
    sections: list[Section],
    public_doc: Path | None,
    system_doc: Path | None,
) -> list[Finding]:
    findings: list[Finding] = []
    if not sections or "deprecated" not in symbol.tags or "useinstead" not in symbol.tags:
        return findings

    public_anchors = build_anchor_index(public_doc)
    system_anchors = build_anchor_index(system_doc)
    available_anchors = public_anchors | system_anchors

    found_any_link = False
    seen: set[str] = set()
    for section in sections:
        for link in find_replacement_links(section):
            if "#" not in link:
                continue
            found_any_link = True
            anchor = normalize_link_anchor(link.split("#", 1)[1])
            if anchor and anchor not in available_anchors and anchor not in seen:
                seen.add(anchor)
                findings.append(
                    Finding(
                        "warning",
                        f"{symbol.full_name}:{symbol.line}",
                        f"Replacement link anchor '{link}' does not resolve to a known heading in the checked docs.",
                    )
                )
    if not found_any_link:
        findings.append(
            Finding(
                "warning",
                f"{symbol.full_name}:{symbol.line}",
                "Deprecated section includes no explicit replacement link target.",
            )
        )
    return findings


def check_error_code_coverage(symbols: list[Symbol], error_codes: set[int]) -> list[Finding]:
    findings: list[Finding] = []
    if not error_codes:
        return findings
    for symbol in symbols:
        for code in symbol.throws:
            if code >= 10000000 and code not in error_codes:
                findings.append(Finding("error", f"{symbol.full_name}:{symbol.line}", f"Error code {code} is thrown in d.ts but missing from the error code document."))
    return findings


def check_doc_level_rules(
    public_doc: Path | None,
    system_doc: Path | None,
    readme_doc: Path | None,
    rules: Rules,
) -> list[Finding]:
    findings: list[Finding] = []
    if system_doc and system_doc.exists():
        if not system_doc.name.endswith("-sys.md"):
            findings.append(Finding("error", str(system_doc), "System API doc filename should end with -sys.md."))
        title = parse_doc_title(system_doc)
        if title and rules.system_title_marker not in title[1]:
            findings.append(Finding("error", f"{system_doc}:{title[0]}", f"System API doc title should include {rules.system_title_marker}."))
        content = system_doc.read_text(encoding="utf-8")
        if rules.mixed_module_note not in content:
            findings.append(Finding("warning", str(system_doc), "System API doc is missing the mixed-module note that points readers to the public API doc."))
    if public_doc and public_doc.exists():
        title = parse_doc_title(public_doc)
        if title and rules.system_title_marker in title[1]:
            findings.append(Finding("error", f"{public_doc}:{title[0]}", f"Public API doc title should not include {rules.system_title_marker}."))
        if system_doc and system_doc.exists():
            for lineno, target in extract_markdown_links(public_doc):
                if Path(target).name == system_doc.name:
                    findings.append(Finding("error", f"{public_doc}:{lineno}", "Public API doc must not link to the system API doc."))
    if readme_doc and readme_doc.exists():
        normal, deleted = parse_readme_entries(readme_doc)
        if public_doc and public_doc.exists() and public_doc.name not in normal:
            findings.append(Finding("warning", str(readme_doc), f"Public doc {public_doc.name} was not found in normal Readme entries."))
        if system_doc and system_doc.exists():
            if system_doc.name not in deleted:
                findings.append(Finding("warning", str(readme_doc), f"System doc {system_doc.name} was not found in <!--Del--> Readme entries."))
            if public_doc and public_doc.exists() and public_doc.name in normal and system_doc.name in deleted:
                public_index = normal.index(public_doc.name)
                system_index = deleted.index(system_doc.name)
                if public_index != len(normal) - 1 and system_index == 0:
                    # Entries are separated by blocks, so only flag the obvious case
                    # where the system doc appears to be maintained without the public
                    # one nearby.
                    findings.append(Finding("warning", str(readme_doc), "Readme ordering may not keep the system doc immediately after the related public doc."))
    return findings


def check_section_error_tables(symbol: Symbol, sections: list[Section]) -> list[Finding]:
    findings: list[Finding] = []
    if not sections or not symbol.throws or symbol.kind not in {"function", "method"}:
        return findings
    expected = {code for code in symbol.throws if code >= 100}
    documented: set[int] = set()
    for section in sections:
        documented |= parse_error_codes_from_section(section)
    missing = sorted(expected - documented)
    for code in missing:
        findings.append(Finding("warning", f"{symbol.full_name}:{symbol.line}", f"Error code {code} is thrown in d.ts but missing from the section error-code table."))
    return findings


def check_section_style_rules(symbol: Symbol, sections: list[Section], rules: Rules) -> list[Finding]:
    findings: list[Finding] = []
    if not sections or symbol.kind not in {"function", "method"}:
        return findings
    for section in sections:
        bad_lines = check_permission_connector_style(section, rules)
        for line in bad_lines:
            findings.append(
                Finding(
                    "warning",
                    f"{symbol.full_name}:{symbol.line}",
                    f"Required permission field mixes English connectors in Chinese doc text: {line}",
                )
            )
    return findings


def check_error_doc_structure(error_doc: Path | None, rules: Rules) -> list[Finding]:
    findings: list[Finding] = []
    sections = parse_error_code_sections(error_doc)
    for code, body in sections.items():
        for block in rules.error_required_blocks:
            if block not in body:
                findings.append(Finding("warning", f"{error_doc}:{code}", f"Error code {code} is missing required block {block}."))
    return findings


def check_since_rules(
    symbol: Symbol,
    sections: list[Section],
    module_since: int | None,
) -> list[Finding]:
    findings: list[Finding] = []
    if not sections:
        return findings
    if symbol.kind not in {"function", "method", "enum"}:
        return findings
    if "atomicservice" in symbol.tags or "crossplatform" in symbol.tags:
        return findings
    since_versions = parse_symbol_since_versions(symbol)
    if not since_versions:
        return findings
    if len(set(since_versions)) != 1:
        return findings

    min_since = min(since_versions)
    combined = section_text(sections)
    heading_versions: set[int] = set()
    for section in sections:
        heading_versions |= extract_sup_versions(section.heading)

    if module_since is not None and min_since > module_since and min_since not in heading_versions:
        findings.append(
            Finding(
                "warning",
                f"{symbol.full_name}:{symbol.line}",
                f"Symbol since version {min_since} is newer than module since {module_since}, but the matched heading is missing <sup>{min_since}+</sup>.",
            )
        )
    if module_since is not None and min_since == module_since and heading_versions:
        findings.append(
            Finding(
                "warning",
                f"{symbol.full_name}:{symbol.line}",
                f"Symbol since version equals module since {module_since}, but the matched heading includes explicit version markers {sorted(heading_versions)}.",
            )
        )
    if "deprecated" in symbol.tags and "(deprecated)" not in combined.lower():
        findings.append(Finding("warning", f"{symbol.full_name}:{symbol.line}", "Deprecated symbol section is missing a deprecated marker."))
    return findings


def render(findings: list[Finding]) -> str:
    if not findings:
        return "No issues found by the automated API-doc consistency checks."
    lines = ["# Automated API Doc Consistency Report", ""]
    for finding in findings:
        lines.append(f"- [{finding.severity}] `{finding.location}` {finding.message}")
    return "\n".join(lines)


def validate_rules_against_templates(
    rules: Rules,
    js_template: Path | None,
    ts_template: Path | None,
    error_template: Path | None,
) -> list[Finding]:
    findings: list[Finding] = []
    for template in (js_template, ts_template):
        if template and template.exists():
            text = template.read_text(encoding="utf-8")
            if template == js_template and rules.system_title_marker not in text:
                findings.append(
                    Finding(
                        "warning",
                        str(template),
                        f"Configured system title marker {rules.system_title_marker} was not found in the template. Update doc_check_rules.json if the template changed.",
                    )
                )
            if template == js_template and rules.mixed_module_note not in text:
                findings.append(
                    Finding(
                        "warning",
                        str(template),
                        "Configured mixed-module note text was not found in the JS template. Update doc_check_rules.json if the template changed.",
                    )
                )
    if error_template and error_template.exists():
        text = error_template.read_text(encoding="utf-8")
        for block in rules.error_required_blocks:
            if block not in text:
                findings.append(
                    Finding(
                        "warning",
                        str(error_template),
                        f"Configured required error block {block} was not found in the error template. Update doc_check_rules.json if the template changed.",
                    )
                )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Check d.ts tag to documentation mapping rules.")
    parser.add_argument("--api", required=True, help="Path to the d.ts file.")
    parser.add_argument("--public-doc", help="Path to the public API Markdown doc.")
    parser.add_argument("--system-doc", help="Path to the system API Markdown doc.")
    parser.add_argument("--error-doc", help="Path to the error code Markdown doc.")
    parser.add_argument("--readme-doc", help="Path to Readme-CN.md. If omitted, infer from the doc directory.")
    parser.add_argument("--rules-file", help="Path to a JSON rules file. Defaults to scripts/doc_check_rules.json.")
    parser.add_argument("--js-template", help="Path to the current JS API template.")
    parser.add_argument("--ts-template", help="Path to the current ArkTS template.")
    parser.add_argument("--error-template", help="Path to the current error code template.")
    args = parser.parse_args()

    api_path = Path(args.api)
    public_doc = Path(args.public_doc) if args.public_doc else None
    system_doc = Path(args.system_doc) if args.system_doc else None
    error_doc = Path(args.error_doc) if args.error_doc else None
    readme_doc = Path(args.readme_doc) if args.readme_doc else infer_readme_path(public_doc, system_doc)
    rules = load_rules(Path(args.rules_file) if args.rules_file else None)
    js_template = Path(args.js_template) if args.js_template else None
    ts_template = Path(args.ts_template) if args.ts_template else None
    error_template = Path(args.error_template) if args.error_template else None

    symbols = parse_dts(api_path)
    namespace_symbols = [symbol for symbol in symbols if symbol.kind == "namespace"]
    primary_namespace = namespace_symbols[0].short_name if namespace_symbols else None
    public_sections = parse_sections(public_doc) if public_doc and public_doc.exists() else []
    system_sections = parse_sections(system_doc) if system_doc and system_doc.exists() else []
    error_codes = parse_error_codes(error_doc)
    public_module_since = parse_module_since_from_doc(public_doc)
    system_module_since = parse_module_since_from_doc(system_doc)
    name_counts: dict[str, int] = {}
    for symbol in symbols:
        name_counts[symbol.short_name] = name_counts.get(symbol.short_name, 0) + 1
    overloaded_names = {name for name, count in name_counts.items() if count > 1}

    findings: list[Finding] = []
    findings.extend(validate_rules_against_templates(rules, js_template, ts_template, error_template))
    findings.extend(check_doc_level_rules(public_doc, system_doc, readme_doc, rules))
    findings.extend(check_error_doc_structure(error_doc, rules))
    findings.extend(check_doc_links(public_doc))
    findings.extend(check_doc_links(system_doc))
    findings.extend(check_doc_links(error_doc))
    for symbol in symbols:
        if symbol.kind in {"namespace", "const"}:
            continue
        doc_sections = find_sections_for_symbol(public_sections, symbol) + find_sections_for_symbol(system_sections, symbol)
        if primary_namespace and "." not in symbol.full_name and not doc_sections:
            continue
        findings.extend(check_system_placement(symbol, public_sections, system_sections, overloaded_names))
        target_sections = system_sections if "systemapi" in symbol.tags else public_sections
        matched_sections = find_sections_for_symbol(target_sections, symbol)
        findings.extend(check_section_fields(symbol, matched_sections, rules))
        findings.extend(check_replacement_link_targets(symbol, matched_sections, public_doc, system_doc))
        findings.extend(check_section_error_tables(symbol, matched_sections))
        findings.extend(check_section_style_rules(symbol, matched_sections, rules))
        findings.extend(
            check_since_rules(
                symbol,
                matched_sections,
                system_module_since if "systemapi" in symbol.tags else public_module_since,
            )
        )
    findings.extend(check_error_code_coverage(symbols, error_codes))

    output = render(findings)
    print(output)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
