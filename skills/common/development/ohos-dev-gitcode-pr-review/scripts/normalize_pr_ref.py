#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from urllib.parse import urlparse


PR_PATTERNS = (
    re.compile(r"/pulls?/(\d+)(?:/|$)"),
    re.compile(r"/merge_requests?/(\d+)(?:/|$)"),
    re.compile(r"/prs?/(\d+)(?:/|$)"),
)


def parse_repo_from_path(path: str) -> str | None:
    parts = [part for part in path.split("/") if part]
    for marker in ("pull", "pulls", "pr", "prs", "merge_request", "merge_requests"):
        if marker in parts:
            index = parts.index(marker)
            if index >= 2:
                return f"{parts[index - 2]}/{parts[index - 1]}"
    return None


def normalize(ref: str) -> dict[str, object]:
    ref = ref.strip()
    if not ref:
        raise ValueError("PR reference is empty")

    if ref.isdigit():
        return {"number": int(ref), "repo": None, "source": ref}

    parsed = urlparse(ref)
    if parsed.scheme and parsed.netloc:
        path = parsed.path or ""
        for pattern in PR_PATTERNS:
            match = pattern.search(path)
            if match:
                return {
                    "number": int(match.group(1)),
                    "repo": parse_repo_from_path(path),
                    "source": ref,
                }
        raise ValueError(f"Could not find a PR number in URL: {ref}")

    match = re.search(r"(\d+)", ref)
    if match and match.group(1) == ref:
        return {"number": int(match.group(1)), "repo": None, "source": ref}

    raise ValueError(f"Unsupported PR reference: {ref}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize a GitCode PR number or URL.")
    parser.add_argument("ref", help="PR number or URL")
    args = parser.parse_args()

    try:
        result = normalize(args.ref)
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}))
        return 1

    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
