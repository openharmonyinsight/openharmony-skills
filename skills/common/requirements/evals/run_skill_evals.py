#!/usr/bin/env python3
"""Local evaluator for user_guide skill eval specs.

This runner does not invoke an LLM. It grades saved outputs with deterministic
assertions and marks semantic assertions for manual or external judge review.
"""

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


PROGRAMMATIC_TYPES = {"contains", "not_contains", "regex"}
MANUAL_TYPES = {"llm_judge"}


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def eval_id_matches(actual, expected):
    return str(actual) == str(expected)


def select_eval(evals_path, eval_id):
    data = load_json(evals_path)
    for case in data.get("evals", []):
        if eval_id_matches(case.get("id"), eval_id):
            return data.get("skill_name", Path(evals_path).parents[1].name), case
    raise SystemExit("eval id %r not found in %s" % (eval_id, evals_path))


def grade_assertion(assertion, output_text):
    kind = assertion.get("type", "llm_judge")
    needle = assertion.get("text", "")
    if kind == "contains":
        passed = needle in output_text
        evidence = "found text" if passed else "missing text"
    elif kind == "not_contains":
        passed = needle not in output_text
        evidence = "text absent" if passed else "unexpected text present"
    elif kind == "regex":
        passed = re.search(needle, output_text, re.M) is not None
        evidence = "regex matched" if passed else "regex did not match"
    elif kind in MANUAL_TYPES:
        return {
            "text": needle,
            "type": kind,
            "passed": None,
            "status": "manual",
            "evidence": "requires LLM judge or human review",
        }
    else:
        return {
            "text": needle,
            "type": kind,
            "passed": None,
            "status": "unsupported",
            "evidence": "unsupported assertion type",
        }
    return {
        "text": needle,
        "type": kind,
        "passed": passed,
        "status": "passed" if passed else "failed",
        "evidence": evidence,
    }


def summarize_results(results):
    summary = {"passed": 0, "failed": 0, "manual": 0, "unsupported": 0, "total": len(results)}
    for item in results:
        if item["status"] == "passed":
            summary["passed"] += 1
        elif item["status"] == "failed":
            summary["failed"] += 1
        elif item["status"] == "manual":
            summary["manual"] += 1
        else:
            summary["unsupported"] += 1
    graded = summary["passed"] + summary["failed"]
    summary["programmatic_pass_rate"] = round(summary["passed"] / graded, 4) if graded else None
    return summary


def command_grade(args):
    skill_name, case = select_eval(args.evals, args.eval_id)
    output_text = Path(args.output).read_text(encoding="utf-8")
    results = [grade_assertion(a, output_text) for a in case.get("assertions", [])]
    data = {
        "skill_name": skill_name,
        "eval_id": case.get("id"),
        "eval_name": case.get("name", str(case.get("id"))),
        "output": str(args.output),
        "summary": summarize_results(results),
        "expectations": results,
    }
    write_json(args.result, data)


def parse_yaml_case_count(path):
    if not path.exists():
        return 0
    return len(re.findall(r"^\s*-\s+id:", path.read_text(encoding="utf-8"), re.M))


def collect_skill(skill_dir):
    evals_path = skill_dir / "evals" / "evals.json"
    yaml_path = skill_dir / "evals" / "cases.yaml"
    skill_data = {
        "cases": 0,
        "assertions": 0,
        "programmatic_assertions": 0,
        "manual_assertions": 0,
        "unsupported_assertions": 0,
        "assertion_types": {},
    }
    if evals_path.exists():
        data = load_json(evals_path)
        for case in data.get("evals", []):
            skill_data["cases"] += 1
            for assertion in case.get("assertions", []) or []:
                kind = assertion.get("type", "llm_judge")
                skill_data["assertions"] += 1
                skill_data["assertion_types"][kind] = skill_data["assertion_types"].get(kind, 0) + 1
                if kind in PROGRAMMATIC_TYPES:
                    skill_data["programmatic_assertions"] += 1
                elif kind in MANUAL_TYPES:
                    skill_data["manual_assertions"] += 1
                else:
                    skill_data["unsupported_assertions"] += 1
    elif yaml_path.exists():
        skill_data["cases"] = parse_yaml_case_count(yaml_path)
        skill_data["manual_assertions"] = skill_data["cases"]
    return skill_data


def benchmark_markdown(data):
    lines = [
        "# User Guide Skill Eval Benchmark",
        "",
        "| Skill | Cases | Assertions | Programmatic | Manual | Unsupported |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, item in sorted(data["skills"].items()):
        lines.append(
            "| %s | %d | %d | %d | %d | %d |"
            % (
                name,
                item["cases"],
                item["assertions"],
                item["programmatic_assertions"],
                item["manual_assertions"],
                item["unsupported_assertions"],
            )
        )
    summary = data["summary"]
    lines.extend(
        [
            "",
            "## Summary",
            "",
            "- Total cases: %d" % summary["total_cases"],
            "- Total assertions: %d" % summary["total_assertions"],
            "- Programmatic assertions: %d" % summary["programmatic_assertions"],
            "- Manual assertions: %d" % summary["manual_assertions"],
            "- Unsupported assertions: %d" % summary["unsupported_assertions"],
        ]
    )
    return "\n".join(lines) + "\n"


def command_collect(args):
    root = Path(args.root)
    skills = {}
    for skill_md in sorted(root.glob("ohos-req-*/SKILL.md")):
        skills[skill_md.parent.name] = collect_skill(skill_md.parent)
    summary = {
        "total_cases": sum(v["cases"] for v in skills.values()),
        "total_assertions": sum(v["assertions"] for v in skills.values()),
        "programmatic_assertions": sum(v["programmatic_assertions"] for v in skills.values()),
        "manual_assertions": sum(v["manual_assertions"] for v in skills.values()),
        "unsupported_assertions": sum(v["unsupported_assertions"] for v in skills.values()),
    }
    data = {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "summary": summary,
        "skills": skills,
    }
    write_json(args.benchmark_json, data)
    if args.benchmark_md:
        Path(args.benchmark_md).parent.mkdir(parents=True, exist_ok=True)
        Path(args.benchmark_md).write_text(benchmark_markdown(data), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    grade = sub.add_parser("grade", help="grade one saved text output against one eval")
    grade.add_argument("--evals", required=True, type=Path)
    grade.add_argument("--output", required=True, type=Path)
    grade.add_argument("--eval-id", required=True)
    grade.add_argument("--result", required=True, type=Path)
    grade.set_defaults(func=command_grade)

    collect = sub.add_parser("collect", help="collect eval coverage into benchmark files")
    collect.add_argument("--root", required=True, type=Path)
    collect.add_argument("--benchmark-json", required=True, type=Path)
    collect.add_argument("--benchmark-md", type=Path)
    collect.set_defaults(func=command_collect)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
