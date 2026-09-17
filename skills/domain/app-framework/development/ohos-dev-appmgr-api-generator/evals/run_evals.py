#!/usr/bin/env python3
"""Eval runner for ohos-dev-appmgr-api-generator skill.

Executes each eval defined in evals.json and generates an HTML report.
Supports three test modes:
  1. Module-level — import generator, call functions, check return values
  2. CLI — run script as subprocess with stdin, check stdout/exit code
  3. Generation — create temp project, call generate_all, check snippets
"""
import sys
import os
import re
import json
import subprocess
import tempfile
import importlib.util
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
GEN_SCRIPT = SKILL_DIR / "scripts" / "generate_appmgr_api.py"
EVALS_JSON = SCRIPT_DIR / "evals.json"


def _load_gen():
    spec = importlib.util.spec_from_file_location("gen", str(GEN_SCRIPT))
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _make_project(td, enum_content=None):
    pr = Path(td)
    dirs = [
        "interfaces/inner_api/app_manager/include/appmgr",
        "interfaces/inner_api/app_manager/src/appmgr",
        "services/appmgr/include",
        "services/appmgr/src",
    ]
    for d in dirs:
        (pr / d).mkdir(parents=True, exist_ok=True)
    files = [
        "interfaces/inner_api/app_manager/include/appmgr/app_mgr_ipc_interface_code.h",
        "interfaces/inner_api/app_manager/include/appmgr/app_mgr_client.h",
        "interfaces/inner_api/app_manager/src/appmgr/app_mgr_client.cpp",
        "interfaces/inner_api/app_manager/include/appmgr/app_mgr_proxy.h",
        "interfaces/inner_api/app_manager/src/appmgr/app_mgr_proxy.cpp",
        "interfaces/inner_api/app_manager/include/appmgr/app_mgr_interface.h",
        "services/appmgr/include/app_mgr_service.h",
        "services/appmgr/src/app_mgr_service.cpp",
        "services/appmgr/include/app_mgr_service_inner.h",
        "services/appmgr/src/app_mgr_service_inner.cpp",
        "interfaces/inner_api/app_manager/include/appmgr/app_mgr_stub.h",
        "interfaces/inner_api/app_manager/src/appmgr/app_mgr_stub.cpp",
    ]
    for f in files:
        (pr / f).write_text("// placeholder", encoding="utf-8")
    if enum_content:
        (pr / files[0]).write_text(enum_content, encoding="utf-8")
    else:
        (pr / files[0]).write_text(
            "enum AppMgrInterfaceCode : uint32_t { APP_FIRST = 1, };\n",
            encoding="utf-8",
        )
    return pr


# ---------------------------------------------------------------------------
# Eval executors — each returns (output_text, exit_code)
# ---------------------------------------------------------------------------

def _eval_generate(gen, api_name, return_type, params, is_async=False, enum_content=None):
    """Run generate_all and return all snippet text concatenated.

    Async (TF_ASYNC) forces void return type — the caller may pass
    return_type='bool' with is_async=True, and we set is_void=True and
    return_type='void' to match the prompt_user / validate_api_info behavior.

    Returns ``(output, exit_code, snippets)`` where ``snippets`` is a dict of
    ``{snippet_key: snippet_text}`` so per-snippet assertions can be checked
    against only the relevant snippet instead of the entire concatenated
    output (R6-F4).
    """
    if is_async:
        return_type = "void"
    is_void = return_type == "void"
    with tempfile.TemporaryDirectory() as td:
        pr = _make_project(td, enum_content)
        api = gen.ApiInfo(api_name, return_type, params,
                          is_void=is_void, is_async=is_async)
        gen_inst = gen.AppMgrApiGenerator(pr)
        code, used_names = gen.get_next_ipc_code(pr)
        blocks = gen_inst.generate_all(api, code, used_enum_names=used_names)
        output = f"Generated {len(blocks)} snippets\n\n"
        for key, snippet in blocks.items():
            output += f"--- {key} ---\n{snippet}\n\n"
        return output, 0, dict(blocks)


def _eval_module(gen, fn, *args):
    """Call a module-level function and capture the return value as text."""
    result = fn(*args)
    return repr(result), 0, {}


def _eval_validate_raises(gen, api_name, return_type, params, is_async=False):
    """Expect validate_api_info to raise ValueError."""
    api = gen.ApiInfo(api_name, return_type, params,
                      is_void=(return_type == "void"), is_async=is_async)
    try:
        gen.validate_api_info(api)
        return "NO ERROR RAISED (unexpected)", 1, {}
    except ValueError as e:
        return str(e), 0, {}


def _eval_conflict(gen, api_name, enum_content):
    """Expect generate_all to raise ValueError for duplicate enum name."""
    with tempfile.TemporaryDirectory() as td:
        pr = _make_project(td, enum_content)
        gen_inst = gen.AppMgrApiGenerator(pr)
        used_names = gen_inst._read_existing_enum_names()
        api = gen.ApiInfo(api_name, "void", [], is_void=True)
        try:
            gen_inst.generate_all(api, 200, used_enum_names=used_names)
            return ("NO ERROR RAISED (unexpected) — used_names: " + str(sorted(used_names)), 1, {})
        except ValueError as e:
            return f"{e} — used_names: {sorted(used_names)}", 0, {}


def _eval_cli(stdin_text, project_path):
    """Run the script as a CLI subprocess."""
    result = subprocess.run(
        [sys.executable, str(GEN_SCRIPT), project_path],
        input=stdin_text, capture_output=True, text=True, timeout=15,
    )
    combined = f"exit_code={result.returncode}\n{result.stdout}"
    if result.stderr:
        combined += f"\n{result.stderr}"
    return combined, result.returncode, {}


def _eval_cli_tempdir(gen, stdin_text, enum_content=None,
                      target_is_dir=False, root_is_file=False):
    """Run the CLI with a tempdir project root."""
    if root_is_file:
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tf:
            tf.write(b"not a directory")
            tmp = tf.name
        try:
            return _eval_cli(stdin_text, tmp)
        finally:
            os.unlink(tmp)
    with tempfile.TemporaryDirectory() as td:
        if target_is_dir:
            pr = Path(td)
            for f in [
                "interfaces/inner_api/app_manager/include/appmgr/app_mgr_ipc_interface_code.h",
                "interfaces/inner_api/app_manager/include/appmgr/app_mgr_client.h",
                "interfaces/inner_api/app_manager/src/appmgr/app_mgr_client.cpp",
                "interfaces/inner_api/app_manager/include/appmgr/app_mgr_proxy.h",
                "interfaces/inner_api/app_manager/src/appmgr/app_mgr_proxy.cpp",
                "interfaces/inner_api/app_manager/include/appmgr/app_mgr_interface.h",
                "services/appmgr/include/app_mgr_service.h",
                "services/appmgr/src/app_mgr_service.cpp",
                "services/appmgr/include/app_mgr_service_inner.h",
                "services/appmgr/src/app_mgr_service_inner.cpp",
                "interfaces/inner_api/app_manager/include/appmgr/app_mgr_stub.h",
                "interfaces/inner_api/app_manager/src/appmgr/app_mgr_stub.cpp",
            ]:
                (pr / f).mkdir(parents=True, exist_ok=True)
            return _eval_cli(stdin_text, str(pr))
        else:
            pr = _make_project(td, enum_content)
            return _eval_cli(stdin_text, str(pr))


# ---------------------------------------------------------------------------
# Dispatch table: eval_id -> (executor, args)
# ---------------------------------------------------------------------------

def _run_eval(gen, eval_id):
    if eval_id == 1:
        return _eval_generate(gen, "ClearData", "void",
                              [("int32_t", "pid"), ("const std::string&", "bundleName")])
    if eval_id == 2:
        return _eval_generate(gen, "RegisterObserver", "int32_t",
                              [("const sptr<IConfigurationObserver>&", "observer")])
    if eval_id == 3:
        return _eval_generate(gen, "IsPluginEnabled", "bool",
                              [("const std::string&", "pluginName"), ("int32_t", "flag")])
    if eval_id == 4:
        return _eval_generate(gen, "ClearUpApplicationData", "AppMgrResultCode", [])
    if eval_id == 5:
        return _eval_generate(gen, "NotifyStateChange", "bool", [], is_async=True)
    if eval_id == 6:
        return _eval_generate(gen, "GetBundleName", "std::string",
                              [("int32_t", "uid")])
    if eval_id == 7:
        return _eval_generate(gen, "GetProcessInfo", "int32_t",
                              [("uint32_t", "pid"), ("uint64_t", "token")])
    if eval_id == 8:
        return _eval_generate(gen, "SetRemoteObject", "void",
                              [("const sptr<IRemoteObject>&", "obj")])
    if eval_id == 9:
        return _eval_cli_tempdir(gen,
                                "MalformedParam\nint32_t\nn\nx\n\n")
    if eval_id == 10:
        r1 = gen._valid_sptr_inner("AAFwk::IUserCallback")
        r2 = gen._valid_sptr_inner("OHOS::AAFwk::IUserCallback")
        return f"AAFwk::IUserCallback -> {r1}\nOHOS::AAFwk::IUserCallback -> {r2}", 0, {}
    if eval_id == 11:
        r1 = gen._valid_sptr_inner("IObserver::class")
        r2 = gen._valid_sptr_inner("int32_t")
        return f"IObserver::class -> {r1}\nint32_t -> {r2}", 0, {}
    if eval_id == 12:
        return _eval_conflict(gen, "Dup",
                              "enum AppMgrInterfaceCode : uint32_t {\n"
                              "    APP_BASE = 1,\n"
                              "    APP_DUP = 1 << 2,\n"
                              "};\n")
    if eval_id == 13:
        return _eval_conflict(gen, "Implicit",
                              "enum AppMgrInterfaceCode : uint32_t {\n"
                              "    APP_BASE = 1,\n"
                              "    APP_IMPLICIT,\n"
                              "};\n")
    if eval_id == 14:
        return _eval_cli_tempdir(gen, "TestApi\nvoid\nn\n\n", target_is_dir=True)
    if eval_id == 15:
        return _eval_cli_tempdir(gen, "TestApi\nvoid\nn\n\n", root_is_file=True)
    if eval_id == 16:
        return _eval_validate_raises(gen, "Dup", "void",
                                     [("int32_t", "value"), ("bool", "value")])
    if eval_id == 17:
        return _eval_validate_raises(gen, "class", "void", [])
    if eval_id == 18:
        return _eval_validate_raises(gen, "VecApi", "void",
                                     [("std::vector<int32_t>", "values")])
    if eval_id == 19:
        return _eval_validate_raises(gen, "BadSptr", "void",
                                     [("sptr<int32_t>", "val")])
    if eval_id == 20:
        return _eval_generate(gen, "RegisterCallback", "void",
                              [("const sptr<AAFwk::IUserCallback>&", "callback")])
    raise ValueError(f"unknown eval id {eval_id}")


# ---------------------------------------------------------------------------
# Assertion checking
# ---------------------------------------------------------------------------

def _check_assertion(assertion, output, snippets=None):
    """Check a single assertion against the eval output.

    If the assertion has a ``snippet`` key (e.g. ``"stub_cpp"``), the pattern
    is searched **only** within that snippet's text — not the entire
    concatenated output. This prevents a guard in ``proxy_cpp`` from making a
    ``stub-null-check`` assertion falsely pass (R6-F4).

    Without ``snippet``, the pattern is searched against the full output (for
    assertions that span multiple snippets or for CLI/module-level evals).
    """
    name = assertion["name"]
    atype = assertion["type"]
    snippet_key = assertion.get("snippet")
    if snippet_key and snippets:
        search_text = snippets.get(snippet_key, "")
    else:
        search_text = output
    if atype == "regex":
        pattern = assertion["pattern"]
        match = re.search(pattern, search_text)
        scope = f"in {snippet_key}" if snippet_key else "in full output"
        return match is not None, f"pattern /{pattern}/ {scope}" + (" matched" if match else " NOT matched")
    if atype == "not_regex":
        pattern = assertion["pattern"]
        match = re.search(pattern, search_text)
        scope = f"in {snippet_key}" if snippet_key else "in full output"
        return match is None, f"pattern /{pattern}/ {scope}" + (" NOT found (good)" if not match else " FOUND (bad)")
    if atype == "contains":
        expected = assertion["expected"]
        found = expected.lower() in search_text.lower()
        scope = f"in {snippet_key}" if snippet_key else "in full output"
        return found, f"'{expected[:60]}' {scope}" + (" found" if found else " NOT found")
    return False, f"unknown assertion type {atype}"


# ---------------------------------------------------------------------------
# HTML report generation
# ---------------------------------------------------------------------------

_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Eval Report — {skill_name}</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 2rem; background: #f8f9fa; color: #1a1a1a; }}
  h1 {{ border-bottom: 2px solid #0b69c3; padding-bottom: .5rem; color: #0b69c3; }}
  .summary {{ display: flex; gap: 1rem; margin: 1.5rem 0; flex-wrap: wrap; }}
  .stat {{ background: #fff; border-radius: 8px; padding: 1rem 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,.1); min-width: 120px; text-align: center; }}
  .stat .num {{ font-size: 2rem; font-weight: 700; }}
  .stat .label {{ font-size: .85rem; color: #666; text-transform: uppercase; }}
  .stat.pass .num {{ color: #28a745; }}
  .stat.fail .num {{ color: #dc3545; }}
  .stat.total .num {{ color: #0b69c3; }}
  .stat.rate .num {{ color: #6f42c1; }}
  table {{ width: 100%; border-collapse: collapse; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,.1); }}
  th, td {{ padding: .6rem .8rem; text-align: left; border-bottom: 1px solid #e9ecef; font-size: .9rem; vertical-align: top; }}
  th {{ background: #0b69c3; color: #fff; font-weight: 600; }}
  tr.pass {{ background: #f0fff4; }}
  tr.fail {{ background: #fff5f5; }}
  .badge {{ display: inline-block; padding: .15rem .5rem; border-radius: 4px; font-size: .75rem; font-weight: 600; }}
  .badge.pass {{ background: #28a745; color: #fff; }}
  .badge.fail {{ background: #dc3545; color: #fff; }}
  .detail {{ font-family: "Cascadia Code", "Fira Code", monospace; font-size: .82rem; white-space: pre-wrap; max-height: 200px; overflow-y: auto; background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 4px; padding: .5rem; }}
  .assertion-list {{ list-style: none; padding-left: 0; margin: 0; }}
  .assertion-list li {{ padding: .15rem 0; font-size: .82rem; }}
  .assertion-list .ok {{ color: #28a745; }}
  .assertion-list .ko {{ color: #dc3545; }}
  .meta {{ color: #888; font-size: .85rem; margin-bottom: 1rem; }}
</style>
</head>
<body>
<h1>Evaluation Report — {skill_name}</h1>
<div class="meta">Generated: {timestamp} | Script: generate_appmgr_api.py | Eval count: {total}</div>
<div class="summary">
  <div class="stat total"><div class="num">{total}</div><div class="label">Total</div></div>
  <div class="stat pass"><div class="num">{passed}</div><div class="label">Passed</div></div>
  <div class="stat fail"><div class="num">{failed}</div><div class="label">Failed</div></div>
  <div class="stat rate"><div class="num">{rate}%</div><div class="label">Pass Rate</div></div>
</div>
<table>
<thead>
<tr>
  <th style="width:40px">#</th>
  <th style="width:220px">Eval Name</th>
  <th style="width:60px">Result</th>
  <th style="width:50px">Asserts</th>
  <th>Assertion Details</th>
  <th>Output Sample</th>
</tr>
</thead>
<tbody>
{rows}
</tbody>
</table>
</body>
</html>
"""

_ROW_TEMPLATE = """<tr class="{row_class}">
  <td>{id}</td>
  <td>{name}</td>
  <td><span class="badge {badge_class}">{badge_text}</span></td>
  <td>{passed}/{total}</td>
  <td><ul class="assertion-list">{assertion_items}</ul></td>
  <td><div class="detail">{output_sample}</div></td>
</tr>"""


def _html_escape(text):
    return (text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))


def generate_html_report(skill_name, results, output_path):
    total = len(results)
    passed = sum(1 for r in results if r["pass"])
    failed = total - passed
    rate = f"{passed * 100 // total}" if total else "0"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    rows = []
    for r in results:
        items = []
        for a in r["assertions"]:
            cls = "ok" if a["pass"] else "ko"
            mark = "[PASS]" if a["pass"] else "[FAIL]"
            items.append(f'<li class="{cls}">{mark} <b>{_html_escape(a["name"])}</b> — {_html_escape(a["detail"])}</li>')
        output_sample = _html_escape(r["output"][:500])
        rows.append(_ROW_TEMPLATE.format(
            row_class="pass" if r["pass"] else "fail",
            id=r["id"],
            name=_html_escape(r["name"]),
            badge_class="pass" if r["pass"] else "fail",
            badge_text="PASS" if r["pass"] else "FAIL",
            passed=sum(1 for a in r["assertions"] if a["pass"]),
            total=len(r["assertions"]),
            assertion_items="".join(items),
            output_sample=output_sample,
        ))
    html = _HTML_TEMPLATE.format(
        skill_name=_html_escape(skill_name),
        timestamp=timestamp,
        total=total, passed=passed, failed=failed, rate=rate,
        rows="".join(rows),
    )
    Path(output_path).write_text(html, encoding="utf-8")
    return html


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    evals_data = json.loads(EVALS_JSON.read_text(encoding="utf-8"))
    skill_name = evals_data["skill_name"]
    evals = evals_data["evals"]
    gen = _load_gen()

    results = []
    for ev in evals:
        eid = ev["id"]
        ename = ev["eval_name"]
        try:
            output, exit_code, snippets = _run_eval(gen, eid)
        except Exception as e:
            output = f"RUNNER ERROR: {e}"
            exit_code = 1
            snippets = {}

        assertions = []
        for a in ev["assertions"]:
            ok, detail = _check_assertion(a, output, snippets)
            assertions.append({"name": a["name"], "pass": ok, "detail": detail})
        all_pass = all(a["pass"] for a in assertions)
        results.append({
            "id": eid,
            "name": ename,
            "pass": all_pass,
            "assertions": assertions,
            "output": output,
        })
        status = "PASS" if all_pass else "FAIL"
        n_ok = sum(1 for a in assertions if a["pass"])
        print(f"  [{status}] #{eid:2d} {ename} ({n_ok}/{len(assertions)})")

    total = len(results)
    passed = sum(1 for r in results if r["pass"])
    failed = total - passed
    rate = f"{passed * 100 // total}%" if total else "0%"
    print(f"\n{'='*60}")
    print(f"  Total: {total}  Passed: {passed}  Failed: {failed}  Rate: {rate}")
    print(f"{'='*60}")

    # Generate HTML report
    report_path = SCRIPT_DIR / "eval_report.html"
    generate_html_report(skill_name, results, report_path)
    print(f"\nHTML report: {report_path}")

    # Also generate JSON report
    json_report_path = SCRIPT_DIR / "eval_report.json"
    json_report = {
        "skill_name": skill_name,
        "timestamp": datetime.now().isoformat(),
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": rate,
        "results": [
            {
                "id": r["id"],
                "name": r["name"],
                "pass": r["pass"],
                "assertions": [{"name": a["name"], "pass": a["pass"], "detail": a["detail"]}
                               for a in r["assertions"]],
            }
            for r in results
        ],
    }
    json_report_path.write_text(json.dumps(json_report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"JSON report: {json_report_path}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
