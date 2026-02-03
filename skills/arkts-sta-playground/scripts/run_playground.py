#!/usr/bin/env python3
# Requires Python 3.6+ for type hints
"""
ArkTS-Sta Playground Runner

This script runs ArkTS-Sta code using the ArkTS-Sta Playground HTTP API.

Usage:
    python3 run_playground.py <code.ets>
    python3 run_playground.py --code "let x: number = 42;"

Requirements:
    pip install requests
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    print("Error: requests library is not installed.")
    print("Install it with: pip install requests")
    sys.exit(1)


# API endpoint
COMPILE_API_URL = "https://arkts-play.cn.bz-openlab.ru:10443/compile"
DEFAULT_TIMEOUT = 30  # 30 seconds


def read_code_from_file(file_path: str) -> str:
    """Read ArkTS-Sta code from a file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return path.read_text(encoding="utf-8")


def run_arkts_code(code: str, timeout: int = DEFAULT_TIMEOUT) -> dict:
    """
    Run ArkTS-Sta code using the playground HTTP API.

    Args:
        code: ArkTS-Sta code to execute
        timeout: Maximum time to wait for response (seconds)

    Returns:
        Dictionary with execution results:
        {
            "success": bool,
            "output": str,
            "error": str | None,
            "has_error": bool
        }
    """
    result = {
        "success": False,
        "output": "",
        "error": None,
        "has_error": False
    }

    try:
        # Prepare the request payload
        payload = {
            "code": code
        }

        # Send POST request to the compile API
        print(f"Sending code to {COMPILE_API_URL}...")
        response = requests.post(
            COMPILE_API_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=timeout
        )

        # Check if request was successful
        response.raise_for_status()

        # Parse response
        response_data = response.json()

        # The API returns: { "compile": { "output": "...", "error": "", "exit_code": N }, ... }
        compile_result = response_data.get("compile", {})
        exit_code = compile_result.get("exit_code", 0)
        compile_output = compile_result.get("output", "")

        # Check if there are compilation errors (exit_code != 0 means error)
        if exit_code != 0:
            result["error"] = compile_output
            result["has_error"] = True
            result["output"] = compile_output
            result["success"] = False
        else:
            # Success - no errors
            result["output"] = compile_output
            result["success"] = True
            result["has_error"] = False

    except requests.exceptions.Timeout:
        result["error"] = f"Request timeout after {timeout} seconds"
        result["success"] = False
    except requests.exceptions.RequestException as e:
        result["error"] = f"HTTP request failed: {str(e)}"
        result["success"] = False
    except json.JSONDecodeError as e:
        result["error"] = f"Failed to parse response JSON: {str(e)}"
        result["success"] = False
    except Exception as e:
        result["error"] = f"Unexpected error: {str(e)}"
        result["success"] = False

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Run ArkTS-Sta code using the ArkTS-Sta Playground HTTP API"
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Path to .ets file containing ArkTS-Sta code"
    )
    parser.add_argument(
        "--code",
        help="ArkTS-Sta code to run directly (as string)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Timeout in seconds (default: {DEFAULT_TIMEOUT})"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    # Get code from file or command line
    if args.code:
        code = args.code
    elif args.file:
        try:
            code = read_code_from_file(args.file)
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        print("\nError: Please provide either --code or a file path")
        sys.exit(1)

    # Run the code
    result = run_arkts_code(code=code, timeout=args.timeout)

    # Output results
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("=" * 60)
        if result["success"] and not result["has_error"]:
            print("Success: Code compiled without errors")
            print("=" * 60)
            if result["output"]:
                print("Output:")
                print(result["output"])
        else:
            print("Error: Compilation or execution failed")
            print("=" * 60)
            print(result["error"])
            if result["output"]:
                print("\nOutput:")
                print(result["output"])
            sys.exit(1)


if __name__ == "__main__":
    main()
