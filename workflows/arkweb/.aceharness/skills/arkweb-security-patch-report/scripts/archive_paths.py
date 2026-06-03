from __future__ import annotations

from pathlib import Path


def validate_project_output_root(output_root: Path, project_root: Path) -> tuple[Path, Path]:
    project = project_root.expanduser().resolve()
    output = output_root.expanduser().resolve()
    if not project.is_dir():
        raise SystemExit(f"project root not found: {project}")
    if ".aceharness/runs" in str(output):
        raise SystemExit(f"invalid output root under ACEHarness run logs: {output}")
    if output.parent.name != ".ace-outputs":
        raise SystemExit(
            "invalid output root: "
            f"{output}; expected <workflowRoot>/.ace-outputs/<runId>"
        )
    return output, project
