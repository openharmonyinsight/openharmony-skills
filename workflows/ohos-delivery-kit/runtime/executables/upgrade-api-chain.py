#!/usr/bin/env python3
"""Upgrade a legacy 0.14/ohos-sdd-v1 API Markdown chain to API metadata.

Run with --dry-run first. The assistant never guesses missing facts; --write is
accepted only after every extracted or developer-confirmed fact is complete and
the rendered metadata passes the current structural contract.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR / "lib"))

from odk_api_chain_upgrade import (  # noqa: E402
    build_upgrade,
    render_metadata,
    render_report,
    render_spec_section,
    replace_api_spec_section,
    validate_rendered_metadata,
)
from odk_api_spec import parse_api_spec  # noqa: E402
from odk_involvement import parse_eight_dim_involvement  # noqa: E402

METADATA_FILES = {
    "arkts": "arkts-api-spec.yaml",
    "c": "c-api-spec.yaml",
}


def validate_fact_keys(facts: dict) -> list[str]:
    """Reject typos in the developer-confirmed facts JSON shape."""

    errors: list[str] = []
    allowed_languages = {"arkts", "c"}
    allowed_language_keys = {
        "branch", "commit", "filePath", "sourcePath", "english", "apis",
        "platform", "applicationModel", "permissions", "deviceDifferences",
    }
    allowed_api_keys = {
        "description", "parameters", "returnType", "errorCodes",
        "since", "syscap", "platform", "applicationModel", "permissions",
        "deviceDifferences", "english", "startLine", "endLine", "apiMode",
    }
    allowed_description_keys = {
        "function", "scenario", "effect", "similarAPIs",
        "defaultBehavior", "constraints", "activation", "notes",
    }
    allowed_parameter_keys = {"en", "zh", "direction"}
    allowed_error_keys = {"constant", "description"}

    def validate_device_differences(
        value: object, path: str
    ) -> None:
        if value is None:
            return
        if not isinstance(value, dict):
            errors.append(f"{path}.deviceDifferences must be an object")
            return
        items = value.get("items")
        if not isinstance(items, list):
            errors.append(f"{path}.deviceDifferences.items must be a list")
            return
        for index, item in enumerate(items, start=1):
            if not isinstance(item, dict) or not item:
                errors.append(
                    f"{path}.deviceDifferences.items[{index}] "
                    "must be a non-empty object"
                )

    unknown_languages = sorted(set(facts) - allowed_languages)
    if unknown_languages:
        errors.append("unknown languages: " + ", ".join(unknown_languages))
    for language, value in facts.items():
        if language not in allowed_languages or not isinstance(value, dict):
            continue
        unknown = sorted(set(value) - allowed_language_keys)
        if unknown:
            errors.append(f"unknown {language} keys: " + ", ".join(unknown))
        validate_device_differences(
            value.get("deviceDifferences"), language
        )
        apis = value.get("apis", {})
        if isinstance(apis, dict):
            for api_id, api_value in apis.items():
                if not isinstance(api_value, dict):
                    errors.append(f"{language}.apis.{api_id} must be an object")
                    continue
                unknown = sorted(set(api_value) - allowed_api_keys)
                if unknown:
                    errors.append(
                        f"unknown {language}.apis.{api_id} keys: "
                        + ", ".join(unknown)
                    )
                validate_device_differences(
                    api_value.get("deviceDifferences"),
                    f"{language}.apis.{api_id}",
                )
                parameters = api_value.get("parameters")
                if isinstance(parameters, dict):
                    for name, parameter in parameters.items():
                        if not isinstance(parameter, dict):
                            errors.append(
                                f"{language}.apis.{api_id}.parameters.{name} "
                                "must be an object"
                            )
                            continue
                        unknown = sorted(
                            set(parameter) - allowed_parameter_keys
                        )
                        if unknown:
                            errors.append(
                                f"unknown {language}.apis.{api_id}.parameters.{name} "
                                "keys: " + ", ".join(unknown)
                            )
                elif isinstance(parameters, list):
                    for index, parameter in enumerate(parameters, start=1):
                        if not isinstance(parameter, dict):
                            errors.append(
                                f"{language}.apis.{api_id}.parameters[{index}] "
                                "must be an object"
                            )
                            continue
                        allowed_c_parameter_keys = {
                            "name", "cType", "required", "direction",
                            "isPointer", "isConst", "description",
                        }
                        unknown = sorted(
                            set(parameter) - allowed_c_parameter_keys
                        )
                        if unknown:
                            errors.append(
                                f"unknown {language}.apis.{api_id}."
                                f"parameters[{index}] keys: "
                                + ", ".join(unknown)
                            )
                english_value = api_value.get("english", {})
                if isinstance(english_value, dict):
                    description = english_value.get("description", {})
                    if isinstance(description, dict):
                        unknown = sorted(
                            set(description) - allowed_description_keys
                        )
                        if unknown:
                            errors.append(
                                f"unknown {language}.apis.{api_id}.english."
                                "description keys: " + ", ".join(unknown)
                            )
                    unknown = sorted(
                        set(english_value) - {"description"}
                    )
                    if unknown:
                        errors.append(
                            f"unknown {language}.apis.{api_id}.english keys: "
                            + ", ".join(unknown)
                        )
        english = value.get("english", {})
        if not isinstance(english, dict):
            continue
        for api_id, api_value in english.items():
            if not isinstance(api_value, dict):
                errors.append(f"{language}.english.{api_id} must be an object")
                continue
            unknown = sorted(set(api_value) - allowed_api_keys)
            if unknown:
                errors.append(
                    f"unknown {language}.english.{api_id} keys: "
                    + ", ".join(unknown)
                )
            description = api_value.get("description", {})
            if isinstance(description, dict):
                unknown = sorted(set(description) - allowed_description_keys)
                if unknown:
                    errors.append(
                        f"unknown {language}.english.{api_id}.description keys: "
                        + ", ".join(unknown)
                    )
            parameters = api_value.get("parameters", {})
            if isinstance(parameters, dict):
                for name, parameter in parameters.items():
                    if not isinstance(parameter, dict):
                        errors.append(
                            f"{language}.english.{api_id}.parameters.{name} "
                            "must be an object"
                        )
                        continue
                    unknown = sorted(set(parameter) - allowed_parameter_keys)
                    if unknown:
                        errors.append(
                            f"unknown {language}.english.{api_id}.parameters.{name} "
                            "keys: " + ", ".join(unknown)
                        )
            error_codes = api_value.get("errorCodes", {})
            if isinstance(error_codes, dict):
                for code, error_code in error_codes.items():
                    if not isinstance(error_code, dict):
                        errors.append(
                            f"{language}.english.{api_id}.errorCodes.{code} "
                            "must be an object"
                        )
                        continue
                    unknown = sorted(set(error_code) - allowed_error_keys)
                    if unknown:
                        errors.append(
                            f"unknown {language}.english.{api_id}.errorCodes.{code} "
                            "keys: " + ", ".join(unknown)
                        )
    errors.extend(_placeholder_fact_values(facts, "facts"))
    return errors


def _placeholder_fact_values(value: object, path: str) -> list[str]:
    if isinstance(value, str):
        if re.search(
            r"\b(?:TBD|TODO)\b|待确认|待定|待补充|待实现|待验证",
            value,
            flags=re.IGNORECASE,
        ) or re.fullmatch(r"<[^>]+>", value.strip()):
            return [f"{path} contains an unresolved placeholder"]
        return []
    if isinstance(value, dict):
        return [
            issue
            for key, item in value.items()
            for issue in _placeholder_fact_values(item, f"{path}.{key}")
        ]
    if isinstance(value, list):
        return [
            issue
            for index, item in enumerate(value, start=1)
            for issue in _placeholder_fact_values(item, f"{path}[{index}]")
        ]
    return []


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("change_dir", type=Path, help="ODK change directory")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Report without writing files")
    mode.add_argument("--write", action="store_true", help="Write after all facts are complete")
    parser.add_argument(
        "--facts",
        type=Path,
        help="JSON file with developer-confirmed branch, commit, paths, and English documentation facts",
    )
    parser.add_argument(
        "--legacy-format",
        choices=("auto", "odk-014", "ohos-sdd-v1"),
        default="auto",
        help="Legacy API chain format to convert (default: auto)",
    )
    parser.add_argument(
        "--language",
        action="append",
        choices=sorted(METADATA_FILES),
        help="Language to upgrade; may be repeated. Defaults to the value detected in proposal/spec",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Report path for --write (default: evidence/api-chain-upgrade-report.md)",
    )
    args = parser.parse_args()
    if not args.write:
        args.dry_run = True
    return args


def _strip_parser_internal_fields(value: object) -> None:
    """Remove parser bookkeeping such as `_raw` from contract data."""

    if isinstance(value, dict):
        for key in list(value):
            if key.startswith("_"):
                del value[key]
            else:
                _strip_parser_internal_fields(value[key])
    elif isinstance(value, list):
        for item in value:
            _strip_parser_internal_fields(item)


def _merge_existing_metadata(
    change_dir: Path, result: object, existing_languages: list[str]
) -> None:
    """Accumulate and fully validate the other prior-run language."""

    for language in existing_languages:
        path = change_dir / METADATA_FILES[language]
        metadata = parse_api_spec(path)
        _strip_parser_internal_fields(metadata)
        result.metadata_by_language[language] = metadata
        result.validation_issues[language] = validate_rendered_metadata(
            render_metadata(metadata)
        )
    if existing_languages:
        result.spec_section = render_spec_section(
            result.metadata_by_language, result.legacy_format
        )


def _write_outputs(
    change_dir: Path,
    spec_path: Path,
    result: object,
    report: str,
    report_path: Path,
) -> Path:
    """Render everything first, then atomically replace or roll back all targets."""

    staged_metadata = {
        change_dir / METADATA_FILES[language]: render_metadata(metadata)
        for language, metadata in result.metadata_by_language.items()
    }
    for target, rendered in staged_metadata.items():
        issues = validate_rendered_metadata(rendered)
        if issues:
            raise ValueError(
                f"staged metadata validation failed for {target.name}: "
                + "; ".join(issues)
            )

    resolved_report_path = report_path.resolve()
    output_targets = {
        spec_path.resolve(),
        *(
            (change_dir / metadata_name).resolve()
            for metadata_name in METADATA_FILES.values()
        ),
    }
    if resolved_report_path in output_targets:
        raise ValueError(
            "report path must not overwrite spec.md, arkts-api-spec.yaml, "
            f"or c-api-spec.yaml: {resolved_report_path}"
        )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    if report_path.exists() and not report_path.is_file():
        raise ValueError(f"report path is not a file: {report_path}")
    staged_contents = dict(staged_metadata)
    staged_contents[spec_path] = replace_api_spec_section(
        spec_path.read_text(encoding="utf-8"), result.spec_section
    )
    staged_contents[report_path] = report

    with tempfile.TemporaryDirectory(
        prefix=".api-chain-write-", dir=change_dir
    ) as temporary:
        staged_paths: dict[Path, Path] = {}
        backups: dict[Path, Path] = {}
        installed: list[Path] = []
        for target, content in staged_contents.items():
            staged = Path(temporary) / f"{len(staged_paths)}-{target.name}"
            staged.write_text(content, encoding="utf-8")
            staged_paths[target] = staged
        try:
            for target, staged in staged_paths.items():
                if target.exists():
                    backup = Path(temporary) / f"backup-{len(backups)}-{target.name}"
                    target.replace(backup)
                    backups[target] = backup
                staged.replace(target)
                installed.append(target)
        except BaseException:
            for target in reversed(installed):
                if target.exists():
                    target.unlink()
            for target, backup in backups.items():
                backup.replace(target)
            raise
    return report_path


def main() -> int:
    args = parse_args()
    change_dir = args.change_dir
    if not change_dir.is_dir():
        print(f"Error: change directory does not exist: {change_dir}", file=sys.stderr)
        return 2

    proposal_path = change_dir / "proposal.md"
    spec_path = change_dir / "spec.md"
    if not proposal_path.is_file() or not spec_path.is_file():
        print("Error: proposal.md and spec.md are required.", file=sys.stderr)
        return 2

    involvement = parse_eight_dim_involvement(
        proposal_path.read_text(encoding="utf-8"), "API/SDK"
    )
    if involvement != "是":
        print(
            "Error: proposal.md must mark API/SDK as 是 before upgrading an API chain.",
            file=sys.stderr,
        )
        return 2

    if (change_dir / "api-spec.yaml").is_file():
        print(
            "Error: legacy api-spec.yaml exists. Split it into "
            "arkts-api-spec.yaml and/or c-api-spec.yaml first; this assistant "
            "does not accept mixed-schema YAML input.",
            file=sys.stderr,
        )
        return 2

    requested_languages = args.language or []
    existing_languages = [
        language
        for language, name in METADATA_FILES.items()
        if (change_dir / name).is_file()
    ]
    same_language = sorted(set(requested_languages) & set(existing_languages))
    if same_language:
        print(
            "Error: current API metadata already exists for "
            + ", ".join(same_language)
            + ". This assistant does not overwrite the same language.",
            file=sys.stderr,
        )
        return 2
    if existing_languages and not requested_languages:
        print(
            "Error: current API metadata exists for "
            + ", ".join(existing_languages)
            + ". Use --language to upgrade the remaining language.",
            file=sys.stderr,
        )
        return 2

    facts: dict = {}
    if args.facts is not None:
        try:
            facts = json.loads(args.facts.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            print(f"Error: cannot read facts JSON: {error}", file=sys.stderr)
            return 2
        if not isinstance(facts, dict):
            print("Error: facts JSON must be an object.", file=sys.stderr)
            return 2

        fact_errors = validate_fact_keys(facts)
        if fact_errors:
            print(
                "Error: invalid facts JSON: " + "; ".join(fact_errors),
                file=sys.stderr,
            )
            return 2

    try:
        result = build_upgrade(
            proposal_path.read_text(encoding="utf-8"),
            spec_path.read_text(encoding="utf-8"),
            facts=facts,
            languages=args.language,
            legacy_format=args.legacy_format,
        )
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2

    try:
        _merge_existing_metadata(change_dir, result, existing_languages)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Error: cannot load existing API metadata: {error}", file=sys.stderr)
        return 2

    report = render_report(result, write=args.write)
    if args.dry_run:
        print(report)
        return 0 if result.ready else 1

    if not result.ready:
        print(report, file=sys.stderr)
        print(
            "Error: upgrade is blocked; resolve all missing facts and conflicts before writing.",
            file=sys.stderr,
        )
        return 1

    try:
        report_path = _write_outputs(
            change_dir,
            spec_path,
            result,
            report,
            args.report or change_dir / "evidence" / "api-chain-upgrade-report.md",
        )
    except (OSError, ValueError) as error:
        print(f"Error: write failed: {error}", file=sys.stderr)
        return 2

    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
