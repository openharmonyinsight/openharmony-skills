#!/usr/bin/env python3
"""ohos-sdd core engine, stdlib-only.

Owns: mini YAML parser, validate Levels A/B/C/D, contract self-check.
Profile-extendable Spec for Test support lives in ohos_sdd_spec_for_test.py.
NO third-party imports (no PyYAML). When python is absent the shell dispatcher
takes the no-python path; this file is only reached when python3 is available.
"""
import importlib
import json
import os
import re
import sys

_MAP_KEY = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*$")
AC_ID_PATTERN = r"AC-\d+(?:\.\d+)*"


def _tokenize(text):
    """List of (indent, stripped_line); drops blank and '#' comment lines."""
    out = []
    for raw in text.splitlines():
        if not raw.strip():
            continue
        if raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        out.append((indent, raw.strip()))
    return out


def _split_kv(s):
    """'key: value' -> (key, value); value=='' means nested block.
    (None, None) when the line is not a mapping entry."""
    if s.endswith(":"):
        return s[:-1].strip(), ""
    idx = s.find(": ")
    if idx == -1:
        return None, None
    return s[:idx].strip(), s[idx + 2:].strip()


def _scalar(v):
    """Strip inline comments and normalize empty flow sequences."""
    if not v:
        return v
    # Strip inline comments (only when # is preceded by whitespace and not inside quotes)
    in_single = False
    in_double = False
    for i, ch in enumerate(v):
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == '#' and not in_single and not in_double and i > 0 and v[i-1] in (' ', '\t'):
            v = v[:i].rstrip()
            break
    return v


def _parse_node(lines, i, indent):
    if i >= len(lines):
        return None, i
    if lines[i][1].startswith("- "):
        return _parse_seq(lines, i, indent)
    return _parse_map(lines, i, indent)


def _parse_map(lines, i, indent):
    result = {}
    while i < len(lines) and lines[i][0] == indent:
        key, val = _split_kv(lines[i][1])
        if key is None:
            i += 1
            continue
        i += 1
        if val == "":
            if i < len(lines) and lines[i][0] > indent:
                child, i = _parse_node(lines, i, lines[i][0])
                result[key] = child
            else:
                result[key] = None
        else:
            result[key] = _scalar(val)
    return result, i


def _is_mapping_item(body):
    """True when a `- ...` dash body is `key: value` form (identifier key)."""
    key, _ = _split_kv(body)
    return key is not None and bool(_MAP_KEY.match(key))


def _parse_seq(lines, i, indent):
    result = []
    while i < len(lines) and lines[i][0] == indent and lines[i][1].startswith("- "):
        body = lines[i][1][2:].strip()
        i += 1
        if body and _is_mapping_item(body):
            item = {}
            key, val = _split_kv(body)
            if val == "":
                if i < len(lines) and lines[i][0] > indent:
                    child, i = _parse_node(lines, i, lines[i][0])
                    item[key] = child
                else:
                    item[key] = None
            else:
                item[key] = _scalar(val)
            # remaining keys of this mapping item live deeper than the dash indent
            if i < len(lines) and lines[i][0] > indent:
                rest, i = _parse_node(lines, i, lines[i][0])
                if isinstance(rest, dict):
                    item.update(rest)
            result.append(item)
        else:
            result.append(_scalar(body) if body else None)
    return result, i


def yaml_load(text):
    lines = _tokenize(text)
    if not lines:
        return {}
    value, _ = _parse_node(lines, 0, lines[0][0])
    return value or {}


def yaml_frontmatter(text):
    """Parse a leading `---\n...\n---` YAML frontmatter block; {} if none."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end = idx
            break
    if end is None:
        return {}
    return yaml_load("\n".join(lines[1:end]))


_SPEC_FOR_TEST_SERVICE = None


def _spec_for_test_service():
    """Load the optional Spec for Test runtime only when its capability is used."""
    global _SPEC_FOR_TEST_SERVICE
    if _SPEC_FOR_TEST_SERVICE is None:
        module = importlib.import_module("ohos_sdd_spec_for_test")
        _SPEC_FOR_TEST_SERVICE = module.SpecForTestService(yaml_frontmatter)
    return _SPEC_FOR_TEST_SERVICE


class _LazySpecForTestService:
    """Compatibility facade that keeps imports lazy for existing callers/tests."""

    def __getattr__(self, name):
        return getattr(_spec_for_test_service(), name)


SPEC_FOR_TEST = _LazySpecForTestService()


# 交付件 -> 拥有它的能力 skill(rework_capability 路由)
REWORK = {
    "proposal": "ohos-propose", "manifest": "ohos-propose",
    "spec": "ohos-spec", "epic": "ohos-spec",
    "design": "ohos-design",
    "execution_plan": "ohos-plan", "task": "ohos-plan",
    "bugfix": "ohos-plan", "regression_test": "ohos-plan", "test_spec": "ohos-plan",
    "spec_for_test": "ohos-spec-for-test",
    "review": "ohos-review",
    "gate_checklist": "ohos-validate",
    "scenario_library": "ohos-spec", "claude_agent_instructions": "ohos-propose",
    "threat_model": "ohos-security-threat-model",
}


def load_contract(path):
    with open(path, encoding="utf-8") as f:
        return yaml_load(f.read())


def _find_contract():
    d = os.getcwd()
    while d != "/":
        p = os.path.join(d, "openharmony", "contracts", "artifacts.yaml")
        if os.path.isfile(p):
            return load_contract(p)
        d = os.path.dirname(d)
    here = os.path.dirname(os.path.abspath(__file__))
    for rel in (os.path.join(here, "..", "contracts", "artifacts.yaml"),
                os.path.join(here, "..", "shared", "ohos-sdd", "contracts", "artifacts.yaml"),
                os.path.join(here, "..", "..", "shared", "ohos-sdd", "contracts", "artifacts.yaml")):
        cand = os.path.normpath(rel)
        if os.path.isfile(cand):
            return load_contract(cand)
    raise SystemExit("validate: 找不到契约 artifacts.yaml,请用 --contract <path>")


def _artifact_file_map(contract):
    """Map artifact file basename -> (id, status)."""
    out = {}
    for a in contract.get("artifacts", []):
        out[a["file"]] = (a["id"], a.get("status", ""))
    return out


def validate_level_a(change_dir, contract):
    """Level A 结构:required 交付件必须存在;conditional/recommended/reference 仅记录。"""
    checks = []
    for fname, (aid, status) in _artifact_file_map(contract).items():
        exists = os.path.isfile(os.path.join(change_dir, fname))
        if status == "required" and not exists:
            checks.append({"ok": False, "level": "A", "artifact": aid, "file": fname,
                           "issue": "required 交付件缺失",
                           "rework_capability": REWORK.get(aid, "using-ohos-sdd"),
                           "evidence": "Level A 结构"})
        else:
            checks.append({"ok": True, "level": "A", "artifact": aid, "file": fname,
                           "issue": "", "rework_capability": "", "evidence": ""})
    return checks


# change 级 Level B:只校验 Level C 要读的结构锚点 + H1。
# (模板全量章节校验属于 validate --contract,见 Task 11)
# 注:manifest.md 是纯 frontmatter 元数据(无正文 H1),不纳入 H1 校验。
# execution-plan 关键章节标题(单一真相源:LEVEL_B 与 _HEADING_GROUPS 共用,
# 改标题只改这里,避免模板/Level B/contract 三处漂移)
EP_HEADING_AC_TRACE = "## AC 到 Task 追溯"

LEVEL_B = {
    "proposal.md": [r"^# 需求文档", r"^## 三、需求基线"],
    "spec.md": [r"^# 特性规格", r"^## 验收追溯"],
    "execution-plan.md": [r"^# 执行计划", r"^" + EP_HEADING_AC_TRACE],
    "test-spec.md": [r"^# 测试规格"],
}
LEVEL_B_H1_ONLY = ("design.md", "review.md",
                   "bugfix.md", "regression-test.md", "spec-for-test.md")


def validate_level_b(change_dir, contract):
    checks = []
    for fname, (aid, _status) in _artifact_file_map(contract).items():
        fpath = os.path.join(change_dir, fname)
        if not os.path.isfile(fpath):
            continue  # 缺失归 Level A
        with open(fpath, encoding="utf-8") as f:
            text = f.read()
        issues = []
        for pat in LEVEL_B.get(fname, []):
            if not re.search(pat, text, re.MULTILINE):
                issues.append(f"缺少结构标题 /{pat}/")
        if fname in LEVEL_B_H1_ONLY and not re.search(r"^# .+", text, re.MULTILINE):
            issues.append("缺少 H1 标题")
        if fname == "spec-for-test.md" and yaml_frontmatter(text).get("artifact") != "spec-for-test":
            issues.append("frontmatter.artifact 必须为 spec-for-test")
        if issues:
            checks.append({"ok": False, "level": "B", "artifact": aid, "file": fname,
                           "issue": "; ".join(issues),
                           "rework_capability": REWORK.get(aid, "using-ohos-sdd"),
                           "evidence": "Level B 结构"})
        else:
            checks.append({"ok": True, "level": "B", "artifact": aid, "file": fname,
                           "issue": "", "rework_capability": "", "evidence": ""})
    return checks


EDGE_REWORK = {
    "proposal→spec": "ohos-spec",
    "spec→design": "ohos-design",
    "spec→execution-plan": "ohos-plan",
    "spec→task": "ohos-plan",
    "spec→plan": "ohos-plan",
    "execution-plan→code": "ohos-plan",
    "spec→spec-for-test": "ohos-spec-for-test",
    "design→spec-for-test": "ohos-spec-for-test",
    "spec-for-test→test-spec": "ohos-plan",
}


def _read(change_dir, fname):
    p = os.path.join(change_dir, fname)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as f:
        return f.read()


def _ac_set(text):
    """AC identifiers allow one or more numeric segments, for example AC-1.2.3."""
    return set(re.findall(AC_ID_PATTERN, text or ""))


def _section(text, heading):
    """提取某 `## heading` 标题下到下一个 `## ` 之前的内容;无则 ''。"""
    if not text:
        return ""
    m = re.search(r"^##\s+" + re.escape(heading) + r"\s*$", text, re.MULTILINE)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"^##\s+", rest, re.MULTILINE)
    return rest[:nxt.start()] if nxt else rest


def _edge(ok, edge, issue):
    if ok:
        return {"ok": True, "level": "C", "artifact": edge, "file": "",
                "issue": "", "rework_capability": "", "evidence": ""}
    return {"ok": False, "level": "C", "artifact": edge, "file": "",
            "issue": issue, "rework_capability": EDGE_REWORK.get(edge, "using-ohos-sdd"),
            "evidence": "Level C 依赖边"}


def validate_level_c(change_dir):
    checks = []
    spec = _read(change_dir, "spec.md")
    design = _read(change_dir, "design.md")
    plan = _read(change_dir, "execution-plan.md")
    task = _read(change_dir, "task.md")

    spec_acs = _ac_set(spec)
    plan_acs = _ac_set(plan)
    design_acs = _ac_set(design)
    task_acs = _ac_set(task)

    # edge: proposal→spec — spec 验收追溯 至少 1 个 AC(追溯 proposal 成功标准)
    accept = _ac_set(_section(spec, "验收追溯"))
    checks.append(_edge(bool(accept), "proposal→spec",
                        "spec 验收追溯 无 AC,未追溯 proposal 成功标准" if not accept else ""))

    # edge: spec→design — design 引用的 AC 必须存在于 spec(简单变更跳过 design 时豁免)
    if design is not None:
        missing = design_acs - spec_acs
        checks.append(_edge(not missing, "spec→design",
                            f"design 引用了 spec 不存在的 AC:{sorted(missing)}" if missing else ""))

    # edge: spec→plan — execution-plan 存在时检查 spec→execution-plan;否则检查 spec→task(简单变更)
    if plan is not None:
        uncovered = spec_acs - plan_acs
        checks.append(_edge(not uncovered, "spec→execution-plan",
                            f"plan 未覆盖 spec 的 AC:{sorted(uncovered)}" if uncovered else ""))
        # edge: execution-plan→code — 受影响文件清单 非空
        scope = _section(plan, "受影响文件全量清单")
        files = [ln.strip()[2:].strip() for ln in scope.splitlines()
                 if ln.strip().startswith("- ")]
        checks.append(_edge(bool(files), "execution-plan→code",
                            "execution-plan 受影响文件全量清单为空" if not files else ""))
    elif task is not None:
        # 简单变更:task.md 替代 execution-plan,检查 AC 覆盖
        uncovered = spec_acs - task_acs
        checks.append(_edge(not uncovered, "spec→task",
                            f"task 未覆盖 spec 的 AC:{sorted(uncovered)}" if uncovered else ""))
    else:
        checks.append(_edge(False, "spec→plan",
                            "无 execution-plan.md 且无 task.md,plan 交付件缺失"))

    # conditional bypass: spec/design → Profile-defined spec-for-test
    spec_for_test_path = os.path.join(change_dir, "spec-for-test.md")
    if os.path.isfile(spec_for_test_path):
        source_issues = SPEC_FOR_TEST.source_edge_issues(change_dir, spec, design)
        spec_issues, design_issues = source_issues
        checks.append(_edge(not spec_issues, "spec→spec-for-test", "; ".join(spec_issues)))
        checks.append(_edge(not design_issues, "design→spec-for-test", "; ".join(design_issues)))
        test_spec = _read(change_dir, "test-spec.md")
        if test_spec is not None:
            spec_for_test = _read(change_dir, "spec-for-test.md") or ""
            test_spec_issues = []
            if "spec-for-test.md" not in test_spec:
                test_spec_issues.append("test-spec 未声明 spec-for-test.md 测试输入")
            unknown_acs = _ac_set(test_spec) - _ac_set(spec_for_test)
            if unknown_acs:
                test_spec_issues.append(
                    f"test-spec 引用了 spec-for-test 不存在的 AC:{sorted(unknown_acs)}")
            checks.append(_edge(not test_spec_issues, "spec-for-test→test-spec",
                                "; ".join(test_spec_issues)))

    return checks


def _find_up(start_dir, *segs):
    """从 start_dir 向上找第一个存在的 <segs> 文件;无则 None。"""
    d = os.path.abspath(start_dir)
    while True:
        cand = os.path.join(d, *segs)
        if os.path.isfile(cand):
            return cand
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def _d_edge(ok, item, issue):
    if ok:
        return {"ok": True, "level": "D", "artifact": item, "file": "",
                "issue": "", "rework_capability": "", "evidence": ""}
    return {"ok": False, "level": "D", "artifact": item, "file": "",
            "issue": issue, "rework_capability": "ohos-validate",
            "evidence": "Level D 归档就绪"}


def validate_level_d(change_dir, contract):
    checks = []
    registry = _find_up(change_dir, ".codespec", "registry.md")
    checks.append(_d_edge(bool(registry), "registry",
                          "未找到 .codespec/registry.md(change 未被索引)" if not registry else ""))

    mf = _read(change_dir, "manifest.md")
    ok, issue = False, "manifest.md 缺失"
    if mf is not None:
        fm = yaml_frontmatter(mf)
        if not fm:
            issue = "manifest.md 无 frontmatter"
        elif not fm.get("id"):
            issue = "manifest frontmatter 缺 id"
        elif not fm.get("status"):
            issue = "manifest frontmatter 缺 status"
        else:
            ok, issue = True, ""
    checks.append(_d_edge(ok, "manifest", issue))

    spec_compliance = _read(change_dir, os.path.join("evidence", "reviews", "spec-compliance.md"))
    has_evidence = bool(spec_compliance and spec_compliance.strip())
    rv = _read(change_dir, "review.md")
    review_ok = has_evidence or bool(rv and rv.strip())
    checks.append(_d_edge(review_ok, "review",
                          "" if review_ok else "无 evidence/reviews/spec-compliance.md 且 review.md 为空"))
    if _read(change_dir, "spec-for-test.md") is not None:
        spec_for_test_ok = SPEC_FOR_TEST.archive_ready(change_dir)
        checks.append(_d_edge(spec_for_test_ok, "spec-for-test",
                              "spec-for-test.md 必须满足命中 Profile 的审批要求、状态为 Approved，"
                              "当前 Profile 完整检查通过，且 check-spec-for-test.md 结论为 PASS"
                              if not spec_for_test_ok else ""))
    return checks


PROFILES_RESERVED = {"none", "custom", "security-sensitive"}


def _find_profiles_dir(start_dir):
    """向上找 profile 集合目录:优先源仓 openharmony/profiles,回退 dist shared/ohos-sdd/profiles。"""
    d = os.path.abspath(start_dir)
    while True:
        cand = os.path.join(d, "openharmony", "profiles")
        if os.path.isdir(cand):
            return cand
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    here = os.path.dirname(os.path.abspath(__file__))
    for rel in (os.path.join(here, "..", "profiles"),
                os.path.join(here, "..", "shared", "ohos-sdd", "profiles"),
                os.path.join(here, "..", "..", "shared", "ohos-sdd", "profiles")):
        cand = os.path.normpath(rel)
        if os.path.isdir(cand):
            return cand
    return None


def _parse_profile_md(path, fallback_name):
    """解析单个 profile.md frontmatter → (name, repos_list)。
    子 profile 列表由调用方按布局列出(两布局子目录命名不同)。"""
    with open(path, encoding="utf-8") as fh:
        fm = yaml_frontmatter(fh.read())
    repos = fm.get("repos") or []
    if isinstance(repos, str):
        repos = [] if repos.strip() in ("[]", "") else [repos]
    return (fm.get("name") or fallback_name, repos)


def _list_subprofiles(sub_dir):
    """列出子 profile 目录下的 .md 文件名(去扩展名),排除 README.md 与 _template.md。
    目录不存在时返回 []。两布局共用:source 在 <name>/subprofiles/,dist flatten 在 <name>/。"""
    if not os.path.isdir(sub_dir):
        return []
    return [
        os.path.splitext(sf)[0] for sf in os.listdir(sub_dir)
        if sf.endswith(".md") and sf not in ("README.md", "_template.md")
    ]


def _scan_profiles(profiles_dir):
    """返回 (main: name->repos_list, subs: name->[sub_names])。
    兼容 source(<name>/profile.md + <name>/subprofiles/<sub>.md)与
    dist flatten(<name>.md + <name>/<sub>.md)两种布局。
    分支互斥:同一 profile 的 source 目录形式与 dist flatten 形式不应混合存在于同一 profiles_dir。"""
    main, subs = {}, {}
    if not profiles_dir or not os.path.isdir(profiles_dir):
        return main, subs
    for entry in sorted(os.listdir(profiles_dir)):
        full = os.path.join(profiles_dir, entry)
        # source 布局:<name>/profile.md + <name>/subprofiles/<sub>.md
        if os.path.isdir(full) and entry != "_template":
            pf = os.path.join(full, "profile.md")
            if os.path.isfile(pf):
                name, repos = _parse_profile_md(pf, entry)
                main[name] = repos
                subs[name] = _list_subprofiles(os.path.join(full, "subprofiles"))
                continue
        # dist flatten 布局:<name>.md + <name>/<sub>.md
        if entry.endswith(".md") and entry not in ("README.md", "_template.md"):
            name, repos = _parse_profile_md(full, entry[:-3])
            main[name] = repos
            subs[name] = _list_subprofiles(os.path.join(profiles_dir, name))
    return main, subs


def _e_check(ok, artifact, issue, warn=False):
    """Level E check。warn=True 时 ok 应为 True(软规范不 fail),issue 标注 warn 文本,
    并打 warn 标记供 _assemble/_emit 呈现(不进 broken)。"""
    assert not (warn and not ok), "_e_check: warn=True 时 ok 必须为 True"
    d = {"ok": ok, "level": "E", "artifact": artifact, "file": "",
         "issue": issue, "rework_capability": "ohos-validate" if not ok else "",
         "evidence": "Level E profile" if not ok else ""}
    if warn:
        d["warn"] = True
    return d


def validate_level_e(change_dir, root):
    """Level E profile 维度:E1 合法 / E2 文件存在 / E3 schema warn / E4 subprofile 文件 /
    E5 best-effort repo / E6 repo 唯一。root 用于定位 profiles 集合。"""
    checks = []
    profiles_dir = _find_profiles_dir(change_dir) or os.path.join(root, "openharmony", "profiles")
    main_map, subs_map = _scan_profiles(profiles_dir)

    mf = _read(change_dir, "manifest.md")
    fm = yaml_frontmatter(mf) if mf else {}
    profile = fm.get("profile") or "none"
    subprofiles = fm.get("subprofiles") or []
    # mini YAML parser 不识别 inline flow([]),会把 `subprofiles: []` 解析成字面串 '[]';
    # 同理空 inline。把它们规范化为空列表,只有真实 block 序列(- item)才是 list。
    if isinstance(subprofiles, str):
        subprofiles = [] if subprofiles.strip() in ("[]", "") else [subprofiles]

    # E1 profile 合法
    legal = profile in PROFILES_RESERVED or profile in main_map
    checks.append(_e_check(legal, "E1.profile-legal",
                           "" if legal else f"profile {profile!r} 不在扫描集合且非保留值"))

    # E2 profile 文件存在(保留值豁免)
    if profile in PROFILES_RESERVED:
        checks.append(_e_check(True, "E2.profile-file", f"{profile} 为保留值,文件待补(豁免)"))
    elif profile in main_map:
        checks.append(_e_check(True, "E2.profile-file", ""))
    else:
        checks.append(_e_check(False, "E2.profile-file", f"profile {profile!r} 无对应文件"))

    # E3 schema 推荐节(软规范:缺则 warn,ok=True)
    if profile in main_map and profile not in PROFILES_RESERVED:
        pf = None
        src_pf = os.path.join(profiles_dir, profile, "profile.md")
        dist_pf = os.path.join(profiles_dir, profile + ".md")
        pf = src_pf if os.path.isfile(src_pf) else (dist_pf if os.path.isfile(dist_pf) else None)
        ptxt = ""
        if pf:
            with open(pf, encoding="utf-8") as fh:
                ptxt = fh.read()
        for sec in ("基本信息", "阶段补充约束", "专项检查清单"):
            present = bool(re.search(r"^##\s*" + sec, ptxt, re.MULTILINE))
            checks.append(_e_check(True, f"E3.schema:{sec}",
                                   "" if present else f"推荐节「{sec}」缺失(warn,待社区补)",
                                   warn=not present))
    else:
        checks.append(_e_check(True, "E3.schema", "保留值/无 profile,豁免"))

    # E4 subprofile 文件
    known_subs = set(subs_map.get(profile, []))
    for sp in subprofiles:
        checks.append(_e_check(sp in known_subs, f"E4.subprofile:{sp}",
                               f"subprofile {sp!r} 不在 {profile} 的子 profile 集合"))

    # E5 best-effort repo:有 git remote 时校验 manifest.profile 与仓名归属一致(warn)
    try:
        import subprocess
        url = subprocess.run(["git", "remote", "get-url", "origin"],
                             capture_output=True, text=True,
                             cwd=os.path.abspath(change_dir)).stdout.strip()
    except Exception:
        url = ""
    if url:
        repo = os.path.basename(url.rstrip("/"))
        if repo.endswith(".git"):
            repo = repo[:-4]
        owner = [pname for pname, reps in main_map.items() if repo in reps]
        if owner and profile not in PROFILES_RESERVED and profile not in owner:
            checks.append(_e_check(True, "E5.repo-match",
                                   f"git remote {repo}→{owner[0]},但 manifest.profile={profile}(warn,请确认)",
                                   warn=True))
        elif not owner and profile not in PROFILES_RESERVED:
            checks.append(_e_check(True, "E5.repo-unmatched",
                                   f"git remote {repo} 未匹配任何 profile(可能仓未注册或 manifest.profile 需确认)",
                                   warn=True))
        else:
            checks.append(_e_check(True, "E5.repo-match", ""))
    # E5 无 git remote 时不产出 check(静默)

    # E6 repo 唯一归属:多 profile 声明同仓名 → fail
    repo_owner = {}
    for pname, reps in main_map.items():
        for r in reps:
            repo_owner.setdefault(r, []).append(pname)
    for r, owners in repo_owner.items():
        if len(owners) > 1:
            checks.append(_e_check(False, f"E6.repo-conflict:{r}",
                                   f"仓名 {r} 被多 profile 声明:{sorted(owners)}"))

    # E7 主 profile repos 非空(仓间路由依赖,必填,fail)
    for pname, reps in main_map.items():
        if not reps:
            checks.append(_e_check(False, f"E7.profile-repos:{pname}",
                                   f"profile {pname!r} 的 repos 为空(仓间路由依赖,必填至少 1 仓名)"))

    # E8 子 profile applies_to 非空(仓内路由依赖,必填,fail)
    for pname, sub_names in subs_map.items():
        for sub in sub_names:
            spf = None
            for cand in (os.path.join(profiles_dir, pname, "subprofiles", sub + ".md"),
                         os.path.join(profiles_dir, pname, sub + ".md")):
                if os.path.isfile(cand):
                    spf = cand
                    break
            if not spf:
                continue
            with open(spf, encoding="utf-8") as fh:
                sfm = yaml_frontmatter(fh.read())
            at = sfm.get("applies_to")
            if isinstance(at, str):
                at = [] if at.strip() in ("", "[]") else [at]
            if not at:
                checks.append(_e_check(False, f"E8.subprofile-applies_to:{pname}/{sub}",
                                       f"子 profile {pname}/{sub} 的 applies_to 为空(仓内路由依赖,必填至少 1 glob)"))

    return checks


# contract 自检:模板标题组(与现有 ruby validator 逐字对齐)。
# 注:gate-* 形态是当前契约;P2 gate→check 迁移时须同步本表(见 contract-transition 附录决议 2)。
_HEADING_GROUPS = [
    ("openharmony/templates/proposal.md", [
        "# 需求文档", "## 一、原始需求", "## 二、澄清记录", "## 三、需求基线"]),
    ("openharmony/templates/spec.md", [
        "# 特性规格", "## 用户故事", "## 验收追溯", "## 验证映射", "## Spec 自审清单"]),
    ("openharmony/templates/design.md", [
        "# 架构设计", "## 需求基线", "## 上下文和现状", "## 关键设计决策", "## 后续 Task 拆分"]),
    ("openharmony/templates/execution-plan.md", [
        "# 执行计划", "## 受影响文件全量清单", EP_HEADING_AC_TRACE,
        "## Task 详情", "## Plan 自审清单"]),
    ("openharmony/templates/task.md", [
        "# 任务规格", "## 代码变更摘要", "## 验证检查清单"]),
    ("openharmony/templates/test-spec.md", [
        "# 测试规格", "## 测试范围", "## 环境前置与公共配置", "## 场景"]),
    ("openharmony/templates/gate-checklist.md", [
        "# 阶段检查清单",
        "## 一、定义阶段（进入规格说明条件）",
        "## 二、规格说明阶段（进入设计条件）",
        "## 三、设计阶段（进入计划条件）",
        "## 四、计划阶段（进入实现条件）"]),
    ("openharmony/templates/threat-model.md", [
        "# 威胁模型分析", "## 数据流图", "## STRIDE 威胁分析",
        "## 法规合规检查", "## 风险与缓解"]),
]

_EXAMPLE_FILES = [
    "openharmony/examples/bugfix-example/bugfix.md",
    "openharmony/examples/bugfix-example/regression-test.md",
    "openharmony/examples/archive-shape/.codespec/registry.md",
    "openharmony/examples/archive-shape/.codespec/changes/issue-12345-notification-category/proposal.md",
    "openharmony/examples/archive-shape/.codespec/changes/issue-12345-notification-category/manifest.md",
    "openharmony/examples/archive-shape/.codespec/changes/issue-12345-notification-category/spec.md",
    "openharmony/examples/archive-shape/.codespec/changes/issue-12345-notification-category/design.md",
    "openharmony/examples/archive-shape/.codespec/changes/issue-12345-notification-category/execution-plan.md",
    "openharmony/examples/archive-shape/.codespec/changes/issue-12345-notification-category/review.md",
    "openharmony/examples/archive-shape/.codespec/changes/issue-12345-notification-category/test-spec.md",
    "openharmony/examples/archive-shape/.codespec/changes/issue-12345-notification-category/evidence/checks/check-proposal.md",
    "openharmony/examples/archive-shape/.codespec/changes/issue-12345-notification-category/evidence/checks/check-spec.md",
    "openharmony/examples/archive-shape/.codespec/changes/issue-12345-notification-category/evidence/checks/check-design.md",
    "openharmony/examples/archive-shape/.codespec/changes/issue-12345-notification-category/evidence/checks/check-execution-plan.md",
    "openharmony/examples/archive-shape/.codespec/changes/issue-12345-notification-category/evidence/reviews/spec-compliance.md",
]

_VALID_STATUS = {"required", "conditional", "recommended", "reference"}


def _cok(label):
    return {"ok": True, "level": "contract", "artifact": label, "file": "",
            "issue": "", "rework_capability": "", "evidence": ""}


def _cbad(label, issue):
    return {"ok": False, "level": "contract", "artifact": label, "file": "",
            "issue": issue, "rework_capability": "using-ohos-sdd", "evidence": "contract 自检"}


def validate_contract_source(root):
    """Contract 自检。兼容源仓布局(root/openharmony/contracts/artifacts.yaml)
    和发布布局(root/contracts/artifacts.yaml)。"""
    checks = []
    # 尝试源仓布局和发布布局
    contract_path = os.path.join(root, "openharmony", "contracts", "artifacts.yaml")
    prefix = "openharmony/"  # 模板/示例路径前缀
    if not os.path.isfile(contract_path):
        contract_path = os.path.join(root, "contracts", "artifacts.yaml")
        prefix = ""  # 发布布局:模板路径无 openharmony/ 前缀
    if not os.path.isfile(contract_path):
        checks.append(_cbad("contract", f"artifacts.yaml 缺失(尝试了 openharmony/contracts/ 和 contracts/)"))
        return checks
    contract = load_contract(contract_path)

    checks.append(_cok("schema") if contract.get("schema") == "ohos-sdd-artifacts/v1"
                  else _cbad("schema", f"schema={contract.get('schema')}"))

    arch = contract.get("archive", {})
    target_root = arch.get("target_root", "")
    checks.append(_cok("archive.target_root") if target_root == ".codespec/changes"
                  else _cbad("archive.target_root", str(target_root)))
    checks.append(_cok("archive.registry") if arch.get("registry") == ".codespec/registry.md"
                  else _cbad("archive.registry", str(arch.get("registry"))))

    phases = {p.get("id") for p in contract.get("phase_order", [])}
    artifact_ids = {a.get("id") for a in contract.get("artifacts", [])}
    for a in contract.get("artifacts", []):
        aid = a.get("id", "?")
        tmpl = a.get("template")
        resolution = a.get("template_resolution", "static")
        if resolution == "profile_extendable":
            try:
                template_checks = SPEC_FOR_TEST.contract_template_checks(root, aid)
            except (ModuleNotFoundError, SyntaxError, ImportError) as exc:
                tpath = os.path.join(root, tmpl) if tmpl else None
                if tpath and os.path.isfile(tpath) and os.path.getsize(tpath) > 0:
                    checks.append(_cok(f"{aid}.template"))
                else:
                    checks.append(_cbad(f"{aid}.template", f"模板缺失或空:{tmpl}"))
                checks.append(_cbad(
                    f"{aid}.profile_extendable_runtime",
                    f"spec_for_test 模块不可用，Profile 增量校验降级:{type(exc).__name__}: {exc}"))
            else:
                for ok, label, issue in template_checks:
                    checks.append(_cok(label) if ok else _cbad(label, issue))
        else:
            tpath = os.path.join(root, tmpl) if tmpl else None
            if tpath and os.path.isfile(tpath) and os.path.getsize(tpath) > 0:
                checks.append(_cok(f"{aid}.template"))
            else:
                checks.append(_cbad(f"{aid}.template", f"模板缺失或空:{tmpl}"))
        if resolution not in {"static", "profile_extendable"}:
            checks.append(_cbad(f"{aid}.template_resolution", f"未知解析方式:{resolution}"))
        else:
            checks.append(_cok(f"{aid}.template_resolution"))
        ph = a.get("phase", "")
        checks.append(_cok(f"{aid}.phase") if ph == "all" or ph in phases
                      else _cbad(f"{aid}.phase", f"未知 phase:{ph}"))
        st = a.get("status", "")
        checks.append(_cok(f"{aid}.status") if st in _VALID_STATUS
                      else _cbad(f"{aid}.status", f"未知 status:{st}"))
        if "bypass" in a:
            bypass = str(a.get("bypass") or "").lower()
            valid_bypass = bypass in {"true", "false"} and (bypass != "true" or st == "conditional")
            checks.append(_cok(f"{aid}.bypass") if valid_bypass
                          else _cbad(f"{aid}.bypass", "bypass 必须为 true/false，且 true 时 status 必须为 conditional"))
        layer = a.get("layer", "")
        checks.append(_cok(f"{aid}.layer") if layer in {"core", "oh-extension"}
                      else _cbad(f"{aid}.layer", f"未知 layer:{layer}"))
        checks.append(_cok(f"{aid}.role") if a.get("role")
                      else _cbad(f"{aid}.role", "role 为空"))
        loc = a.get("default_location", "")
        if loc:
            checks.append(_cok(f"{aid}.default_location")
                          if loc.startswith(target_root + "/")
                          else _cbad(f"{aid}.default_location", f"不在 archive root:{loc}"))
        for ro in a.get("runtime_outputs", []) or []:
            checks.append(_cok(f"{aid}.runtime_output:{ro}")
                          if ro.startswith(target_root + "/")
                          else _cbad(f"{aid}.runtime_output", f"不在 archive root:{ro}"))
        for dep in a.get("depends_on", []) or []:
            checks.append(_cok(f"{aid}.depends_on:{dep}")
                          if dep in artifact_ids
                          else _cbad(f"{aid}.depends_on:{dep}", f"未知交付件:{dep}"))
        for conditional in a.get("conditional_depends_on", []) or []:
            dep = conditional.get("artifact") if isinstance(conditional, dict) else None
            when = conditional.get("when") if isinstance(conditional, dict) else None
            valid = dep in artifact_ids and bool(when)
            checks.append(_cok(f"{aid}.conditional_depends_on:{dep}")
                          if valid
                          else _cbad(f"{aid}.conditional_depends_on:{dep or '?'}",
                                     "conditional dependency 必须声明有效 artifact 和 when"))

    for rel, headings in _HEADING_GROUPS:
        # 发布布局:rel 以 openharmony/ 开头,去掉前缀后查找
        fpath = os.path.join(root, rel)
        if not os.path.isfile(fpath) and rel.startswith("openharmony/"):
            fpath = os.path.join(root, rel[len("openharmony/"):])
        if os.path.isfile(fpath):
            with open(fpath, encoding="utf-8") as fh:
                lines = fh.read().splitlines()
        else:
            lines = []
        for h in headings:
            present = any(ln.strip() == h for ln in lines)
            checks.append(_cok(f"{rel}:{h}") if present
                          else _cbad(f"{rel}:{h}", f"缺少标题 {h}"))

    for ex in _EXAMPLE_FILES:
        epath = os.path.join(root, ex)
        if not os.path.isfile(epath) and ex.startswith("openharmony/"):
            epath = os.path.join(root, ex[len("openharmony/"):])
        if os.path.isfile(epath):
            checks.append(_cok(f"example:{ex}"))
        elif not prefix:
            # 发布布局无 examples,跳过(不报 fail)
            checks.append(_cok(f"example:{ex}"))
        else:
            checks.append(_cbad(f"example:{ex}", "示例文件缺失"))

    for d in contract.get("current_drifts", []):
        complete = all(d.get(k) for k in ("id", "severity", "description", "follow_up_batch"))
        checks.append(_cok(f"drift:{d.get('id', '?')}") if complete
                      else _cbad(f"drift:{d.get('id', '?')}", "drift 元数据不全"))

    return checks


def _find_contract_path():
    d = os.getcwd()
    while d != "/":
        p = os.path.join(d, "openharmony", "contracts", "artifacts.yaml")
        if os.path.isfile(p):
            return p
        d = os.path.dirname(d)
    here = os.path.dirname(os.path.abspath(__file__))
    for rel in (os.path.join(here, "..", "contracts", "artifacts.yaml"),
                os.path.join(here, "..", "shared", "ohos-sdd", "contracts", "artifacts.yaml"),
                os.path.join(here, "..", "..", "shared", "ohos-sdd", "contracts", "artifacts.yaml")):
        cand = os.path.normpath(rel)
        if os.path.isfile(cand):
            return cand
    return None


def _assemble(change, command, level, checks):
    broken = [c for c in checks if not c["ok"]]
    warnings = [c for c in checks if c.get("warn")]
    return {
        "change": change or "", "command": command, "level": level,
        "passed": len(broken) == 0, "total": len(checks), "broken": len(broken),
        "broken_edges": broken, "warnings": warnings,
        "next": "全部通过" if not broken
        else "按 broken_edges 的 rework_capability 回到对应能力修复",
    }


# Level A-E 的人类可读副标题(方案 3:单层跑时标题带全称)
LEVEL_TITLE = {
    "A": "结构存在",
    "B": "锚点标题",
    "C": "依赖边一致",
    "D": "归档就绪",
    "E": "profile 命中",
}
# 方案 1:level=all 时顶部图例,帮助一眼看懂 A-E 含义
LEVEL_LEGEND = "level 语义: A=结构存在 B=锚点标题 C=依赖边一致 D=归档就绪 E=profile 命中"


def _emit(result, as_json):
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    warns = result.get("warnings", [])
    tag = "PASS" if result["passed"] else "FAIL"
    level = result["level"]
    if level == "all":
        print(LEVEL_LEGEND)
    # 单层 A-E 标题带全称;contract 等其他 level 保持 level=<x> 原样
    title = f"level={level}·{LEVEL_TITLE[level]}·" if level in LEVEL_TITLE else f"level={level}"
    print(f"[{tag}] {result['command']} {title} "
          f"({result['total']} checks, {result['broken']} broken, {len(warns)} warn)")
    for c in result["broken_edges"]:
        print(f"  - {c['level']} {c['artifact']} ({c.get('file','')}): "
              f"{c['issue']} -> {c['rework_capability']}")
    for c in warns:
        print(f"  ~ {c['level']} {c['artifact']}: {c['issue']} (warn)")


def _parse_validate_args(argv):
    opts = {"change": None, "level": "all", "json": False, "contract": None, "source": False}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--level" and i + 1 < len(argv):
            opts["level"] = argv[i + 1]; i += 2
        elif a == "--json":
            opts["json"] = True; i += 1
        elif a == "--contract" and i + 1 < len(argv):
            opts["contract"] = argv[i + 1]; i += 2
        elif a == "--source":
            opts["source"] = True; i += 1
        elif not a.startswith("-"):
            opts["change"] = a; i += 1
        else:
            i += 1
    return opts


def _root_from_change(change_dir):
    """从 change_dir 推仓库 root:向上找含 openharmony/ 的目录;找不到回退 change_dir 自身绝对路径
    (与 _find_profiles_dir 的参考系一致,而非 cwd)。"""
    d = os.path.abspath(change_dir or os.getcwd())
    while True:
        if os.path.isdir(os.path.join(d, "openharmony")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return os.path.abspath(change_dir or os.getcwd())
        d = parent


def _resolve_levels(level):
    if level == "all":
        return ["A", "B", "C", "D", "E"]
    if level.upper() in {"A", "B", "C", "D", "E"}:
        return [level.upper()]
    return None  # 非法 level:cmd_validate 据此报错,避免静默 0-check PASS


def cmd_validate(argv):
    opts = _parse_validate_args(argv)
    if opts["source"]:
        cpath = opts["contract"] or _find_contract_path()
        if not cpath:
            print("validate --source: 找不到契约 artifacts.yaml",
                  file=sys.stderr)
            return 2
        # 源仓布局: cpath = root/openharmony/contracts/artifacts.yaml → root = 上 3 级
        # 发布布局: cpath = root/contracts/artifacts.yaml → root = 上 2 级
        root = os.path.dirname(os.path.dirname(os.path.dirname(cpath)))
        if not os.path.isfile(os.path.join(root, "openharmony", "contracts", "artifacts.yaml")):
            root = os.path.dirname(os.path.dirname(cpath))
        checks = validate_contract_source(root)
        result = _assemble("", "validate --source", "contract", checks)
        _emit(result, opts["json"])
        return 0 if result["passed"] else 1
    if opts["change"] is None:
        opts["change"] = os.getcwd()
    levels = _resolve_levels(opts["level"])
    if levels is None:
        print(f"validate: 未知 level {opts['level']!r},允许 A/B/C/D/E/all", file=sys.stderr)
        return 2
    contract = load_contract(opts["contract"]) if opts["contract"] else _find_contract()
    checks = []
    for lv in levels:
        if lv == "A":
            checks += validate_level_a(opts["change"], contract)
        elif lv == "B":
            checks += validate_level_b(opts["change"], contract)
        elif lv == "C":
            checks += validate_level_c(opts["change"])
        elif lv == "D":
            checks += validate_level_d(opts["change"], contract)
        elif lv == "E":
            checks += validate_level_e(opts["change"], _root_from_change(opts["change"]))
    result = _assemble(opts["change"], "validate", opts["level"], checks)
    _emit(result, opts["json"])
    return 0 if result["passed"] else 1


def main(argv):
    sub = argv[1] if len(argv) > 1 else ""
    rest = argv[2:]
    if sub == "validate":
        return cmd_validate(rest)
    if sub == "spec-for-test":
        return SPEC_FOR_TEST.command(rest)
    if sub == "version":
        print("ohos-sdd 0.3.1 (engine)"); return 0
    print(f"engine: unknown subcommand {sub!r}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
