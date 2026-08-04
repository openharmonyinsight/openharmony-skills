#!/usr/bin/env python3
"""Cross-platform smoke tests for the requirements intake bundle scripts."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
ORCH_DIR = SCRIPT_DIR.parent
SKILLS_DIR = ORCH_DIR.parent

PASS = 0
FAIL = 0


def ok(message: str) -> None:
    global PASS
    PASS += 1
    print(f"PASS: {message}")


def bad(message: str, output: str) -> None:
    global FAIL
    FAIL += 1
    print(f"FAIL: {message}")
    if output:
        print(output)


def setup_sandbox() -> Path:
    root = Path(tempfile.mkdtemp())
    target = root / "skills"
    target.mkdir(parents=True)
    for item in SKILLS_DIR.iterdir():
        if item.is_dir():
            shutil.copytree(item, target / item.name)
    return root


def setup_orchestrator_only_sandbox() -> Path:
    root = Path(tempfile.mkdtemp())
    target = root / "skills"
    target.mkdir(parents=True)
    shutil.copytree(ORCH_DIR, target / ORCH_DIR.name)
    return root


def run_script(path: Path, *args: str, env: dict[str, str] | None = None) -> str:
    proc_env = os.environ.copy()
    if env:
        proc_env.update(env)
    proc = subprocess.run(
        [sys.executable, str(path), *args],
        cwd=str(path.parent),
        env=proc_env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return proc.stdout


def sbx_script(root: Path, name: str) -> Path:
    return (
        root
        / "skills"
        / "ohos-req-intake-orchestration"
        / "scripts"
        / name
    )


def sbx_skill(root: Path, name: str) -> Path:
    return root / "skills" / name


def main() -> int:
    root = setup_sandbox()
    out = run_script(sbx_script(root, "install_related_skills.py"), "--check")
    if "Required missing: 0" in out and "Result: READY" in out:
        ok("S1 完整环境预检 READY")
    else:
        bad("S1 期望 READY", out)

    cout = run_script(sbx_script(root, "check_related_skills_consistency.py"))
    if "Result: CONSISTENT" in cout:
        ok("S1 三方一致性 CONSISTENT")
    else:
        bad("S1 期望 CONSISTENT", cout)

    shutil.rmtree(sbx_skill(root, "ohos-req-feature-proposal-baseline"))
    out = run_script(sbx_script(root, "install_related_skills.py"), "--check")
    if "Required missing: 1" in out and "Result: NOT READY" in out:
        ok("S2 缺失依赖预检失败 (missing 1)")
    else:
        bad("S2 期望 missing 1 NOT READY", out)

    root_orch_only = setup_orchestrator_only_sandbox()
    out = run_script(sbx_script(root_orch_only, "install_related_skills.py"), "--install")
    if (
        "OHOS_REQ_SKILLS_SOURCE_DIR" in out
        and "Installed: 1/7" in out
        and "Required missing: 5" in out
        and "Result: READY" not in out
    ):
        ok("S2a 单独编排 skill 无 source 的 --install 被显式拒绝")
    else:
        bad("S2a 期望单独编排 skill 提示 OHOS_REQ_SKILLS_SOURCE_DIR", out)

    out = run_script(
        sbx_script(root, "install_related_skills.py"),
        "--install",
        env={"OHOS_REQ_SKILLS_SOURCE_DIR": str(SKILLS_DIR)},
    )
    if (
        "Installed missing skill: ohos-req-feature-proposal-baseline" in out
        and "Required missing: 0" in out
        and "Result: READY" in out
    ):
        ok("S2b --install 恢复缺失依赖")
    else:
        bad("S2b 期望 --install 恢复 READY", out)

    skill_file = sbx_skill(root, "ohos-req-arch-decision") / "SKILL.md"
    skill_file.write_text(
        skill_file.read_text(encoding="utf-8").replace(
            "  version: 0.3.0", "  version: 0.0.1", 1
        ),
        encoding="utf-8",
    )
    out = run_script(sbx_script(root, "install_related_skills.py"), "--check")
    if "Version mismatch: 1" in out and "NOT READY" in out:
        ok("S3 版本过低预检失败 (version mismatch 1)")
    else:
        bad("S3 期望 version mismatch", out)

    root2 = setup_sandbox()
    orch = sbx_skill(root2, "ohos-req-intake-orchestration") / "SKILL.md"
    orch.write_text(
        orch.read_text(encoding="utf-8") + "\n调用 `ohos-req-foo-bar` 作为占位引用。\n",
        encoding="utf-8",
    )
    cout = run_script(sbx_script(root2, "check_related_skills_consistency.py"))
    if "Result: INCONSISTENT" in cout:
        ok("S4 正文引用清单外 skill 被检出")
    else:
        bad("S4 期望 INCONSISTENT", cout)

    root3 = setup_sandbox()
    orch = sbx_skill(root3, "ohos-req-intake-orchestration") / "SKILL.md"
    text = orch.read_text(encoding="utf-8")
    text = text.replace("  related-skills:\n", "  related-skills:\n    - name: ohos-req-foo-bar\n", 1)
    orch.write_text(text, encoding="utf-8")
    cout = run_script(sbx_script(root3, "check_related_skills_consistency.py"))
    if "Result: INCONSISTENT" in cout:
        ok("S5 清单声明清单外 skill 被检出")
    else:
        bad("S5 期望 INCONSISTENT", cout)

    root4 = setup_sandbox()
    feature_skill = sbx_skill(root4, "ohos-req-feature-proposal-baseline") / "SKILL.md"
    feature_skill.write_text(
        feature_skill.read_text(encoding="utf-8")
        + "\n- Ready -> 执行 ohos-feat-to-ir 生成旧 IR\n",
        encoding="utf-8",
    )
    cout = run_script(sbx_script(root4, "check_related_skills_consistency.py"))
    if "Result: INCONSISTENT" in cout and "ohos-feat-to-ir" in cout:
        ok("S6 旧别名 ohos-feat-to-ir 被检出")
    else:
        bad("S6 期望旧别名 INCONSISTENT", cout)

    print()
    print(f"Summary: {PASS} passed, {FAIL} failed")
    return 0 if FAIL == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
