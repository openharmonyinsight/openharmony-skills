#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SELinux policy commit self-check lint script (Part 1: automated checks).

Usage:
  python3 scan.py <git-ref>        # single commit/tag (sha, HEAD, tag): scans that commit only
  python3 scan.py <base>..<head>   # range net diff (recommended; required for PR/multi-commit)
  python3 scan.py <branch>         # branch ref — local short name (feature), remote-tracking
                                    # (origin/feature), or full ref (refs/heads/feature,
                                    # refs/remotes/origin/feature): merge-base auto-resolved,
                                    # scans the full net diff
  python3 scan.py -                # read diff from stdin
Exit codes: 0 completed (does not mean no violations — combine output with semantic analysis);
            1 empty diff (net diff is empty, nothing to review); 2 input/usage error
"""
import re
import subprocess
import sys

PATHSPEC = ["sepolicy/", "service_contexts", "whitelist/"]
MERGE_BASE_CANDIDATES = ["origin/master", "origin/main", "master", "main"]

# S1 sensitive words: vendor/competitor/platform brand words only
# (technical words such as passwords/tokens/internal IPs are not checked)
SENSITIVE_RE = re.compile(
    r"android|google|aosp|huawei|harmonyos",
    re.IGNORECASE,
)
LICENSE_LINE_RE = re.compile(
    r"apache|license|copyright|all rights reserved|spdx|licensed under|"
    r"you may obtain|warranties|distributed under|without warranties",
    re.IGNORECASE,
)
DEFAULT_LABEL_RE = re.compile(r"\b(limit_domain|default_param|default_service|default_hdf_service)\b")
# Product form-factor isolation macros (11 in total, based on build_with_* switches)
PRODUCT_MACROS = (
    "pc_only", "watch_only", "glasses_only", "phone_only", "tablet_only", "tv_only",
    "smarthomehost_only", "tablet_hybrid_only", "emulator_only", "car_only", "ohos_only",
)
_PRODUCT_ALT = "|".join(PRODUCT_MACROS)
INLINE_MACRO_RE = re.compile(r"(%s)\(\s*`([^`]*)'\s*\)" % _PRODUCT_ALT)
MULTILINE_MACRO_OPEN_RE = re.compile(r"(%s)\(\s*`\s*$" % _PRODUCT_ALT)
# (R5-F2) any backtick macro — product form-factor or debug_only/developer_only
# isolation — can open a multi-line body; nesting must be tracked for all of them
MULTILINE_ANY_MACRO_OPEN_RE = re.compile(
    r"\b(%s|debug_only|developer_only)\(\s*`\s*$" % _PRODUCT_ALT
)
MACRO_SEARCH_RE = re.compile("|".join(re.escape(m) + r"\(" for m in PRODUCT_MACROS))
MACRO_CLOSE_RE = re.compile(r"^\s*'\)\s*$")
RULE_LINE_RE = re.compile(r"^\s*(allow|allowxperm|neverallow)\s")
STAT_LINE_RE = re.compile(r"^\s*(allow|allowxperm|neverallow|attribute|typeattribute)\s")
AVC_RE = re.compile(r"#\s*avc", re.IGNORECASE)
BINDER_ALLOW_RE = re.compile(
    r"^allow\s+([a-z0-9_]+)\s+([a-z0-9_]+):binder\s*\{([^}]*)\}"
)
VIOLATOR_PREFIXES = ("violator_", "rgm_violator_", "system_violator_", "vendor_violator_")
S2A_KIND_RE = re.compile(r"^\s*(allow|allowxperm|neverallow|attribute|typeattribute|type)\b")
OBJ_CLASS_RE = re.compile(r"([a-z0-9_]+)\s*:\s*([a-z0-9_]+)")


def s2a_signature(text):
    """(F4/R5-F3) Pairing signature for S2-A, computed on the policy code segment
    (comment part stripped): statement kind + stable object:class skeleton.
    Comment-only lines (including license headers, which are `#` comments in
    policy files) and blank lines never pair (return None) — they cannot exempt
    policy additions. A `license`/`copyright` substring inside a real policy
    statement (e.g. subject `license_service`) is NOT a license header and still
    gets a signature. Rule statements additionally match on the first
    object:class occurrence, so a removed allow only exempts an added allow on
    the same object:class (a rename of the subject still pairs; a different rule
    does not). Wrapped/multi-line rules whose object:class cannot be extracted
    fall back to a kind-only signature."""
    code = code_part(text)
    stripped = code.strip()
    if not stripped:
        return None  # blank or comment-only line (license headers are comments)
    m = S2A_KIND_RE.match(code)
    if not m:
        return ("other",)
    kind = m.group(1)
    if kind in ("allow", "allowxperm", "neverallow"):
        oc = OBJ_CLASS_RE.search(code)
        if oc:
            return (kind, "%s:%s" % (oc.group(1), oc.group(2)))
        return (kind, "?")
    return (kind,)


class Line:
    __slots__ = ("kind", "text")  # kind: 'added' | 'removed' | 'context'

    def __init__(self, kind, text):
        self.kind = kind
        self.text = text


class Hunk:
    def __init__(self):
        self.lines = []


class File:
    def __init__(self):
        self.path = ""
        self.hunks = []


def parse_diff(diff_text):
    files = []
    cur_file = None
    cur_hunk = None
    for raw in diff_text.splitlines():
        if raw.startswith("diff --git "):
            cur_file = File()
            cur_file.path = raw.split(" b/", 1)[-1] if " b/" in raw else raw
            files.append(cur_file)
            cur_hunk = None
        elif raw.startswith("+++ b/"):
            if cur_file is None:
                cur_file = File()
                files.append(cur_file)
            cur_file.path = raw[6:]
            cur_hunk = None
        elif raw.startswith("@@"):
            if cur_file is None:
                cur_file = File()
                files.append(cur_file)
            cur_hunk = Hunk()
            cur_file.hunks.append(cur_hunk)
        elif cur_hunk is not None:
            if raw.startswith("+"):
                cur_hunk.lines.append(Line("added", raw[1:]))
            elif raw.startswith("-"):
                cur_hunk.lines.append(Line("removed", raw[1:]))
            elif raw.startswith(("\\ No newline",)):
                continue
            else:
                cur_hunk.lines.append(Line("context", raw[1:] if raw[:1] == " " else raw))
    return files


def added_lines(files):
    out = []
    for f in files:
        for h in f.hunks:
            for ln in h.lines:
                if ln.kind == "added":
                    out.append((f, ln))
    return out


def run_git(args):
    return subprocess.run(
        ["git"] + args, capture_output=True, text=True, errors="replace"
    )


def resolve_branch_ref(ref):
    """Resolve a CLI ref to a branch ref — local (refs/heads/*) or remote-tracking
    (refs/remotes/*) — for merge-base net-diff scanning (F1). Commits, tags,
    pseudo-refs (HEAD) and rev expressions (sha~2, sha^) return None and stay
    tip-commit scans. Local short name wins over remote-tracking on collision,
    matching git's own DWIM order."""
    if not ref or ref in ("HEAD", "FETCH_HEAD", "ORIG_HEAD", "MERGE_HEAD"):
        return None
    if ".." in ref or re.search(r"[~^:]", ref):
        return None
    if ref.startswith("refs/heads/") or ref.startswith("refs/remotes/"):
        r = run_git(["rev-parse", "--verify", "--quiet", ref])
        return ref if r.returncode == 0 else None
    for prefix in ("refs/heads/", "refs/remotes/"):
        cand = prefix + ref
        r = run_git(["rev-parse", "--verify", "--quiet", cand])
        if r.returncode == 0:
            return cand
    return None


def normalize_diff_text(diff_text):
    """(R5-F1) The GitCode oh-gc CLI renders PR diffs as
    `diff --git a/X b/X` / `status: ...` / `---` / `@@` without `+++ b/` lines.
    File-level checks (S2-B/S11c/S21/S22, summary, ROM) depend on `+++ b/`,
    so insert a synthetic `+++ b/<path>` after each bare `---` header when the
    following line is not already a `+++` line. Idempotent for standard git
    diffs (their `--- a/X` is always followed by a real `+++` line)."""
    lines = diff_text.splitlines()
    out = []
    cur_path = None
    cur_status = ""
    i = 0
    while i < len(lines):
        raw = lines[i]
        if raw.startswith("diff --git "):
            m = re.match(r"diff --git a/\S+ b/(.+)$", raw)
            cur_path = m.group(1) if m else None
            cur_status = ""
            out.append(raw)
            i += 1
            continue
        if cur_path is not None and raw.startswith("status:"):
            cur_status = raw
            out.append(raw)
            i += 1
            continue
        if cur_path is not None and raw == "---":
            out.append(raw)
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if not nxt.startswith("+++"):
                if re.search(r"status:\s*(deleted|removed)", cur_status):
                    out.append("+++ /dev/null")
                else:
                    out.append("+++ b/%s" % cur_path)
            i += 1
            continue
        out.append(raw)
        i += 1
    return "\n".join(out) + ("\n" if diff_text.endswith("\n") else "")


def resolve_target_tree(ref):
    """(R5-F4) Resolve the new-side tree of the scanned target, so S4 definition
    lookups bind to the reviewed version instead of the current checkout.
    Returns a commit sha string or None (stdin). The S17 whole-file check is an
    AI step — the skill instructs `git show <target-ref>:<file>` for it."""
    r = run_git(["rev-parse", "--verify", "--quiet", ref])
    if r.returncode == 0 and r.stdout.strip():
        return r.stdout.strip()
    return None


def get_diff(ref):
    """Return (diff_text, description, target_tree). Branch refs (local or
    remote-tracking) auto-resolve merge-base and scan the net diff, avoiding the
    tip-commit-only trap. target_tree is the new-side commit sha (None for stdin)
    — S4/S17 must bind their lookups to it, never to the current checkout."""
    if ref == "-":
        return normalize_diff_text(sys.stdin.read()), "stdin", None
    ls = run_git(["ls-files", "--", "sepolicy/", "service_contexts", "whitelist/"])
    if ls.returncode == 0 and not ls.stdout.strip():
        sys.stderr.write(
            "WARNING: no sepolicy/ policy paths in this repository; this skill targets "
            "the selinux_adapter repository. The diff may be empty.\n"
        )
    if ".." in ref:
        r = run_git(["diff", ref, "--"] + PATHSPEC)
        if r.returncode != 0:
            sys.stderr.write("ERROR: git diff %s failed: %s\n" % (ref, r.stderr.strip()))
            sys.exit(2)
        return r.stdout, ref, resolve_target_tree(ref.split("..")[-1].lstrip("."))
    # single ref: branch refs (local/remote-tracking/full) resolve merge-base for a
    # net diff (R3-1/F1); commits, tags and rev expressions scan the tip commit only
    branch_ref = resolve_branch_ref(ref)
    if branch_ref:
        head_sha = run_git(["rev-parse", "--verify", "--quiet", branch_ref]).stdout.strip()
        for base in MERGE_BASE_CANDIDATES:
            base_check = run_git(["rev-parse", "--verify", "--quiet", base])
            if base_check.returncode != 0:
                continue
            mb = run_git(["merge-base", branch_ref, base])
            if mb.returncode == 0 and mb.stdout.strip():
                mb_sha = mb.stdout.strip()
                if mb_sha == head_sha:
                    continue  # branch is at the same commit as base, no unique commits
                r = run_git(["diff", "%s..%s" % (mb_sha, branch_ref), "--"] + PATHSPEC)
                if r.returncode == 0:
                    return r.stdout, "%s (merge-base %s..%s net diff)" % (ref, mb_sha[:10], branch_ref), head_sha
        sys.stderr.write(
            "ERROR: cannot derive merge-base for branch '%s' (tried %s). "
            "Use an explicit <base>..<head> range.\n"
            % (ref, ", ".join(MERGE_BASE_CANDIDATES))
        )
        sys.exit(2)
    r = run_git(["show", ref, "--format=", "--patch", "--"] + PATHSPEC)
    if r.returncode != 0:
        sys.stderr.write("ERROR: cannot resolve git ref '%s': %s\n" % (ref, r.stderr.strip()))
        sys.exit(2)
    return r.stdout, ref, resolve_target_tree(ref)


def emit(title):
    print("\n=== %s ===" % title)


def code_part(text):
    """Strip the comment part; return the policy code segment (S16 etc. exclude comments)."""
    stripped = text.lstrip()
    if stripped.startswith("#"):
        return ""
    return text.split("#", 1)[0]


def check_s1(diff_text):
    emit("S1 sensitive words — vendor/competitor/platform brand words only (non-license + lines; anonymized; empty=pass)")
    for raw in diff_text.splitlines():
        if not raw.startswith("+") or raw.startswith("+++"):
            continue
        content = raw[1:]
        # (R5-F3) license exemption is confined to comment lines (license headers
        # are `#` comments); a brand word inside a real policy statement such as
        # `allow android_licensing_dev ...` is still reported
        if content.lstrip().startswith("#") and LICENSE_LINE_RE.search(content):
            continue
        if SENSITIVE_RE.search(content):
            print(SENSITIVE_RE.sub("***", content))


def check_s2a(files):
    emit("S2-A new policy added to sepolicy/base (attributes included; same-block same-kind pairing=modifiable-exempt, pure-addition block=violation)")
    for f in files:
        if "/sepolicy/base/" not in "/" + f.path:
            continue
        print("+++ b/%s" % f.path)
        for h in f.hunks:
            blocks = []
            cur = {"removed": [], "added": []}
            for ln in h.lines:
                if ln.kind in ("added", "removed"):
                    cur[ln.kind].append(ln.text)
                else:
                    if cur["added"] or cur["removed"]:
                        blocks.append(cur)
                    cur = {"removed": [], "added": []}
            if cur["added"] or cur["removed"]:
                blocks.append(cur)
            for block in blocks:
                # (F4) pair only same-signature statements, one removed exempts at
                # most one added; comments/blank/license lines never provide exemptions
                removed_pool = {}
                for text in block["removed"]:
                    sig = s2a_signature(text)
                    if sig is not None:
                        removed_pool[sig] = removed_pool.get(sig, 0) + 1
                for text in block["added"]:
                    sig = s2a_signature(text)
                    if sig is None:
                        continue  # blank/comment/license lines are not policy content
                    if removed_pool.get(sig, 0) > 0:
                        removed_pool[sig] -= 1
                        print("[modifiable-exempt] +%s" % text)
                    else:
                        print("[pure-addition violation] +%s" % text)


def check_s2b(diff_text):
    emit("S2-B involved ohos_policy/<subsystem>/<component> directories (>=2 entries=suggest concentration/splitting MR)")
    dirs = set()
    for raw in diff_text.splitlines():
        m = re.match(r"^\+\+\+ b/sepolicy/ohos_policy/(.*)$", raw)
        if m:
            rel = re.sub(r"/(public|system|vendor)/.*$", "", m.group(1))
            dirs.add(rel)
    for d in sorted(dirs):
        print(d)
    if len(dirs) >= 2:
        subjects = set()
        for _, ln in added_lines(parse_diff(diff_text)):
            m = re.match(r"allow\s+([a-z0-9_]+)", code_part(ln.text).lstrip())
            if m:
                subjects.add(m.group(1))
        if subjects:
            print(
                "Correlation: subject types detected (%s) — the same type across directories may indicate related changes such as exemption+grant pairing"
                % ", ".join(sorted(subjects))
            )
        else:
            print("Hint: %d different component directories, no shared allow subject type — unrelated features should be split into separate MRs" % len(dirs))


def check_s3(diff_text):
    emit("S3 new parameter label parameter_attr (output=needs init domain confirmation)")
    for raw in diff_text.splitlines():
        if raw.startswith("+") and not raw.startswith("+++") and re.search(
            r"type\s+[^,]+,\s*parameter_attr", raw[1:]
        ):
            print(raw[1:])


def check_s7(files):
    emit("S7 write+execute label location (new type+file_type plus allow write/execute)")
    print("--- New type definitions (file_type etc.) ---")
    for _, ln in added_lines(files):
        if re.match(r"type\s+[a-z0-9_]+,", ln.text.lstrip()):
            print(ln.text)
    print("--- allow write/execute (check whether a neverallow guardrail is needed) ---")
    for _, ln in added_lines(files):
        if re.match(r"\s*allow.*\{[^}]*\b(write|execute)\b", ln.text):
            print(ln.text)


def find_def_paths(name, target_tree):
    """(R5-F4) Look up type/attribute definitions in the scanned target's tree —
    never in the current working checkout, so the S4 verdict stays stable when the
    same target is scanned from different checkouts."""
    r = run_git(
        ["grep", "-l", "-E", "^(type|attribute)[[:space:]]+%s[,;[:space:]]" % name,
         target_tree, "--", "sepolicy/"]
    )
    if r.returncode != 0:
        return []
    return [p for p in r.stdout.splitlines() if p and not p.endswith(".bak")]


SKIP_TOKENS = {"{", "}", "self", "not"}


def extract_neverallow_refs(text):
    """Extract type/attribute references of a neverallow statement
    (excluding - exception items and product/isolation macro contents)."""
    m = re.match(r"\s*neverallow\s+(.+?):[a-z_]", text)
    if not m:
        return None
    seg = m.group(1)
    seg = re.sub(
        r"(%s|debug_only|developer_only)\(\s*`[^`]*'\s*\)" % _PRODUCT_ALT, " ", seg
    )
    refs = []
    for tok in seg.split():
        if tok.startswith("-"):
            continue  # - exception items are excluded from the references
        tok = tok.strip("{}-")
        if not tok or tok in SKIP_TOKENS or not re.match(r"^[a-z_][a-z0-9_.]*$", tok):
            continue
        refs.append(tok)
    return refs


def s4_analyze(text, path, target_tree):
    refs = extract_neverallow_refs(text)
    if refs is None:
        print("  [S4] multi-line/wrapped statement; placement needs manual confirmation")
        return
    uniq = sorted(set(refs))
    if not target_tree:
        # (R5-F4) stdin carries no target tree — stay pending-confirmation instead
        # of silently substituting the current checkout
        print(
            "  [S4] no target tree bound (stdin mode); referenced type/attribute: %s "
            "(rerun scan.py with the target ref at the repository root to complete the check)"
            % ", ".join(uniq)
        )
        return
    undefined, non_public = [], []
    for name in uniq:
        paths = find_def_paths(name, target_tree)
        if not paths:
            undefined.append(name)
        elif any("/public/" not in "/" + p for p in paths):
            non_public.append(name)
    in_public = "/public/" in "/" + path
    if undefined:
        print("  [S4 needs confirmation] references without definitions: %s (check spelling/cross-repo definitions)" % ", ".join(undefined))
    elif non_public:
        print("  [S4] %s defined in non-public; current placement reasonable" % ", ".join(non_public))
    elif in_public:
        print("  [S4] all references defined in public/; already in public/")
    else:
        print("  [S4 suggestion] all references defined in public/; current file is not public/; suggest moving to public/ for shared control")


def check_s4_s11(files, target_tree):
    emit("S4/S11 neverallow added/modified (S4 placement: all type/attribute definitions public -> suggest public/; S11 needs security review)")
    for f in files:
        for h in f.hunks:
            for ln in h.lines:
                if ln.kind == "added" and "neverallow" in ln.text:
                    text = ln.text.strip()
                    print("%s: %s" % (f.path, text))
                    s4_analyze(text, f.path, target_tree)


def check_s5_s6(diff_text):
    emit("S5/S6 SA service / system parameters (output=S5 needs neverallow-guardrail confirmation / S6 needs confirmation)")
    for raw in diff_text.splitlines():
        if raw.startswith("+") and not raw.startswith("+++") and re.search(
            r"sa_service_attr|parameter_service", raw[1:]
        ):
            print(raw[1:])


def check_s9_s10_s13(diff_text, files):
    emit("S9/S10/S13 debug_only / developer_only isolation macro positions + su subject/object (wrapping-scope location)")
    for i, raw in enumerate(diff_text.splitlines(), 1):
        if re.search(r"debug_only\(|developer_only\(", raw):
            print("L%d: %s" % (i, raw))
    print("--- su subject (allowed by default, redundant but not a violation) ---")
    for _, ln in added_lines(files):
        code = code_part(ln.text).lstrip()
        if re.match(r"allow\s+su\s", code):
            print(ln.text)
    print("--- su object (needs debug_only isolation) ---")
    for _, ln in added_lines(files):
        code = code_part(ln.text).lstrip()
        if re.match(r"allow\s+[a-z0-9_]+\s+su:", code):
            print(ln.text)


def check_s11a(diff_text):
    emit("S11a multiple same-kind violator exemptions in one neverallow (output=possible uniqueness violation, manual semantic verification)")
    for raw in diff_text.splitlines():
        if not raw.startswith("+") or raw.startswith("+++"):
            continue
        if "neverallow" not in raw:
            continue
        text = raw[1:]
        violators = re.findall(r"-[a-z0-9_]*violator_[a-z0-9_]*", text)
        rgms = re.findall(r"-rgm_violater_[a-z0-9_]*", text)
        if len(violators) > 1 or len(rgms) > 1:
            print(text)


def check_s11d(files):
    emit(
        "S11d violator naming (violator not a prefix=violation; "
        "defined in system/ must be system_violator_, in vendor/ must be vendor_violator_; definition location is the acting partition)"
    )
    for f in files:
        partition = ""
        if re.search(r"/system/", "/" + f.path):
            partition = "system"
        elif re.search(r"/vendor/", "/" + f.path):
            partition = "vendor"
        for h in f.hunks:
            for ln in h.lines:
                if ln.kind != "added":
                    continue
                text = code_part(ln.text)
                m = re.match(r"attribute\s+([a-z0-9_]+)", text.strip())
                if not m:
                    m = re.match(r"typeattribute\s+[a-z0-9_.]+\s+([a-z0-9_]+)", text.strip())
                if not m:
                    continue
                name = m.group(1)
                if "violator" not in name and "violater" not in name:
                    continue
                if not name.startswith(VIOLATOR_PREFIXES):
                    print("[naming violation] violator must be a prefix: %s (%s)" % (name, f.path))
                    continue
                if partition == "system" and not name.startswith("system_violator_"):
                    print("[partition violation] %s defined in system/ partition, must start with system_violator_ (%s)" % (name, f.path))
                elif partition == "vendor" and not name.startswith("vendor_violator_"):
                    print("[partition violation] %s defined in vendor/ partition, must start with vendor_violator_ (%s)" % (name, f.path))


def check_s11c(diff_text):
    emit("S11c non-flex whitelist modification (perm_group_whitelist.json excluded; output=needs security review)")
    for raw in diff_text.splitlines():
        m = re.match(r"^\+\+\+ b/(.*)$", raw)
        if m and "/whitelist/" in ("/" + m.group(1)) and "/whitelist/flex/" not in ("/" + m.group(1)) and "perm_group_whitelist" not in m.group(1):
            print("+++ b/%s" % m.group(1))
    print("--- non-flex whitelist added lines ---")
    active = False
    for raw in diff_text.splitlines():
        m = re.match(r"^\+\+\+ b/(.*)$", raw)
        if m:
            p = "/" + m.group(1)
            active = "/whitelist/" in p and "/whitelist/flex/" not in p and "perm_group_whitelist" not in m.group(1)
            continue
        if active and raw.startswith("+") and not raw.startswith("+++"):
            print(raw[1:])


def check_s12(files):
    emit("S12 sh as subject (output=needs DFX + security review)")
    # (R5-F5) match on the lstripped policy code segment so indented statements
    # (macro bodies) are detected; neverallow sh and comments never match
    for _, ln in added_lines(files):
        code = code_part(ln.text).lstrip()
        if re.match(r"allow\s+sh\s", code):
            print(ln.text)


def check_s15(diff_text):
    emit("S15 hap permissions (manual check of hap_domain vs concrete type scope)")
    for raw in diff_text.splitlines():
        if raw.startswith("+") and not raw.startswith("+++") and re.search(
            r"hap_domain|hap_file|data_app_", raw[1:]
        ):
            print(raw[1:])


def check_s16(files):
    emit("S16 default labels forbidden (policy code segment only; comment mentions not reported; output=violation)")
    for _, ln in added_lines(files):
        code = code_part(ln.text)
        if code and DEFAULT_LABEL_RE.search(code):
            print("[violation] %s" % ln.text)


def check_s17(files):
    emit(
        "S17 new allow/allowxperm lines vs #avc: comment lines (counts should match; "
        "avc gap judged per hunk, no cross-hunk association)"
    )
    allow_lines = []
    avc_lines = []
    for _, ln in added_lines(files):
        if RULE_LINE_RE.match(ln.text) and not ln.text.lstrip().startswith("neverallow"):
            allow_lines.append(ln.text)
        elif AVC_RE.search(ln.text):
            avc_lines.append(ln.text)
    print("allow/allowxperm + lines: %d    #avc: comment + lines: %d" % (len(allow_lines), len(avc_lines)))
    for t in allow_lines:
        print(t)
    print("--- #avc: ---")
    for t in avc_lines:
        print(t)
    print("--- allow lines without nearby #avc: comment (gap>3 lines=possibly missing) ---")
    for f in files:
        for h in f.hunks:  # judged per hunk independently; @@/file boundaries auto-reset (R4-3)
            avc_near = 0
            for ln in h.lines:
                if ln.kind != "added":
                    if avc_near > 0:
                        avc_near -= 1
                    continue
                if AVC_RE.search(ln.text):
                    avc_near = 3
                elif RULE_LINE_RE.match(ln.text) and not ln.text.lstrip().startswith("neverallow"):
                    if avc_near == 0:
                        print("[avc gap] +%s" % ln.text)
                    avc_near = 0
                else:
                    if avc_near > 0:
                        avc_near -= 1


def check_s18(files):
    emit("S18-A new allow under public/ (output=violation) / S18-B/C allow directory and subject (manual system/vendor placement)")
    for f in files:
        for h in f.hunks:
            for ln in h.lines:
                if ln.kind == "added" and RULE_LINE_RE.match(ln.text) and ln.text.lstrip().startswith("allow"):
                    if "/public/" in "/" + f.path:
                        print("[public violation] %s => +%s" % (f.path, ln.text))
                    else:
                        print("[placement] %s => +%s" % (f.path, ln.text))


def check_s19(files):
    emit("S19 adjacent allow blocks missing blank line (output=violation; adjacency tracked on the new side across context+added lines; reported when either side is new; no false positives across files/hunks; rename refactor per step-2 tone)")
    for f in files:
        for h in f.hunks:
            last_allow = False   # previous new-side line (skipping avc comments) was an allow/allowxperm
            last_added_ln = None  # the Line object of the previous added allow (identity, not text — N2)
            last_blank = False   # a blank line separates since the previous allow
            reported_ln = None   # the Line object last reported (each added line at most once)
            for ln in h.lines:
                text = ln.text
                if ln.kind == "removed":
                    continue  # old side only
                if AVC_RE.search(text):
                    continue  # avc comments belong to the allow block — transparent
                if RULE_LINE_RE.match(text) and not text.lstrip().startswith("neverallow"):
                    # (R5-F6) a new rule glued to an adjacent allow — context or added —
                    # without a blank line is a violation; only context-context adjacency
                    # (both sides pre-existing) stays unreported. Dedup is by line
                    # identity, so identical-text adjacent lines each get their report (N2).
                    if last_allow and not last_blank:
                        if ln.kind == "added":
                            if ln is not reported_ln:
                                print("missing blank line: +%s" % text)
                                reported_ln = ln
                        elif last_added_ln is not None and last_added_ln is not reported_ln:
                            print("missing blank line: +%s" % last_added_ln.text)
                            reported_ln = last_added_ln
                    if ln.kind == "added":
                        last_added_ln = ln
                    else:
                        last_added_ln = None  # a context rule line is not an added line
                    last_allow = True
                    last_blank = False
                elif text.strip() == "":
                    last_blank = True
                    last_allow = False
                    reported_ln = None
                else:
                    last_allow = False
                    last_blank = False
                    reported_ln = None


def check_s20(files):
    emit("S20 allow object is appdat (output=suggest normal_app_data)")
    for _, ln in added_lines(files):
        if re.match(r"\s*allow\s+[a-z0-9_]+\s+appdat:", ln.text):
            print(ln.text)


def check_s20b(files):
    emit("S20b binder call/transfer permission check (suggest binder_call macro for complete IPC permissions, ROM +~300B; allow statements only)")
    suggestion = (
        "[suggestion] %s→%s binder IPC permissions: consider binder_call(%s, %s) macro "
        "(expansion includes forward call/transfer, reverse transfer, fd use — not an equivalent replacement), ROM +~300B"
    )
    print("--- combined form: binder { ... call ... transfer ... } ---")
    pair_keys = set()
    for _, ln in added_lines(files):
        stripped = ln.text.lstrip()
        if not stripped.startswith("allow "):  # anchor on allow: excludes neverallow/comments (R4-1)
            continue
        m = BINDER_ALLOW_RE.match(stripped)
        if not m:
            continue
        subj, obj, perm_str = m.group(1), m.group(2), m.group(3)
        perms = perm_str.split()
        if "call" in perms and "transfer" in perms:
            print(suggestion % (subj, obj, subj, obj))
        elif "call" in perms:
            pair_keys.add((subj, obj, "call"))
        elif "transfer" in perms:
            pair_keys.add((subj, obj, "transfer"))
    print("--- two separate lines: allow call + allow transfer ---")
    calls = {(s, o) for s, o, p in pair_keys if p == "call"}
    transfers = {(s, o) for s, o, p in pair_keys if p == "transfer"}
    for subj, obj in sorted(calls & transfers):
        print(suggestion % (subj, obj, subj, obj))


def check_s21(diff_text):
    emit("S21 service_contexts modification (output=needs samgr domain review)")
    for raw in diff_text.splitlines():
        if re.match(r"^\+\+\+ b/.*service_contexts", raw):
            print(raw)
    print("--- service_contexts added lines ---")
    active = False
    for raw in diff_text.splitlines():
        if raw.startswith("+++ b/"):
            active = "service_contexts" in raw
            continue
        if active and raw.startswith("+") and not raw.startswith("+++"):
            print(raw[1:])


def check_s22(diff_text):
    emit("S22 whitelist/flex *_whitelist.json modification (output=needs dedicated flex review)")
    for raw in diff_text.splitlines():
        if re.match(r"^\+\+\+ b/.*whitelist/flex/.*_whitelist\.json", raw):
            print(raw)
    print("--- whitelist/flex added lines ---")
    active = False
    for raw in diff_text.splitlines():
        if raw.startswith("+++ b/"):
            active = bool(re.search(r"whitelist/flex/.*_whitelist\.json", raw))
            continue
        if active and raw.startswith("+") and not raw.startswith("+++"):
            print(raw[1:])


def check_s23(files):
    emit("S23 product macros (%s etc., 11 total) as exception items only (wrapping allow or neverallow statements forbidden; per-instance judgment)" % "/".join(PRODUCT_MACROS[:3]))
    print("--- form-factor macro positions (location aid) ---")
    for f in files:
        for h in f.hunks:
            for ln in h.lines:
                if MACRO_SEARCH_RE.search(ln.text):
                    print("%s: %s" % (f.path, ln.text))
    print("--- violation: inline product macro argument not a - exception item (per-instance; a legal exception does not swallow illegal macros on the same line) ---")
    for f in files:
        for h in f.hunks:
            for ln in h.lines:
                if ln.kind != "added":
                    continue
                text = code_part(ln.text)
                if not text:
                    continue
                for m in INLINE_MACRO_RE.finditer(text):
                    arg = m.group(2).strip()
                    if arg.startswith("-"):
                        continue  # legal - exception item
                    if re.search(r"\b(allow|allowxperm|neverallow)\b", text):
                        print(
                            "[violation] %s: product macro %s(`%s') not a - exception item: +%s"
                            % (f.path, m.group(1), arg, ln.text)
                        )
    print("--- multi-line product macro wrapping allow or neverallow statements ---")
    # (R5-F2) nesting stack over comment-stripped code: all backtick macros
    # (product + debug_only/developer_only) push a frame; a close pops only the
    # innermost frame, so an inner isolation-macro close never clears an outer
    # product-macro scope. Comment-only lines (e.g. `# pc_only(`) are transparent —
    # they can neither open nor close a scope; trailing comments on close lines
    # (`') # end`) are stripped before matching.
    for f in files:
        for h in f.hunks:
            stack = []  # frames: name/product/open_added/open_text/has_rule/flagged
            for ln in h.lines:
                if ln.kind == "removed":
                    continue  # removed lines do not exist on the new side
                code = code_part(ln.text)
                if not code.strip():
                    continue  # comment-only or blank line: transparent to the state machine
                if MACRO_CLOSE_RE.match(code):
                    if stack:
                        frame = stack.pop()
                        if (frame["product"] and frame["open_added"]
                                and frame["has_rule"] and not frame["flagged"]):
                            # new wrapper around pre-existing (context) rules
                            print(
                                "[violation] %s: new multi-line product macro wraps pre-existing rule: +%s"
                                % (f.path, frame["open_text"])
                            )
                    continue
                m = MULTILINE_ANY_MACRO_OPEN_RE.search(code)
                if m:
                    stack.append({
                        "name": m.group(1),
                        "product": m.group(1) in PRODUCT_MACROS,
                        "open_added": ln.kind == "added",
                        "open_text": ln.text,
                        "has_rule": False,
                        "flagged": False,
                    })
                    continue
                if RULE_LINE_RE.match(code):
                    for frame in stack:
                        frame["has_rule"] = True  # the rule sits inside every enclosing body
                    if ln.kind == "added":
                        for frame in reversed(stack):
                            if frame["product"]:
                                print("[violation] %s: multi-line product macro wrap: +%s" % (f.path, ln.text))
                                frame["flagged"] = True
                                break


def rom_estimate(diff_text):
    emit("ROM increment estimate (A=added rule lines D=removed rule lines M=access_vector changes; attribute/typeattribute definitions included)")
    added = removed = 0
    added_keys = []
    removed_keys = []
    for raw in diff_text.splitlines():
        if raw.startswith("+") and not raw.startswith("+++"):
            if STAT_LINE_RE.match(raw[1:]):
                added += 1
            if RULE_LINE_RE.match(raw[1:]) and not raw[1:].lstrip().startswith("neverallow"):
                added_keys.append(re.sub(r"\s*\{.*", "", raw[1:].strip()))
        elif raw.startswith("-") and not raw.startswith("---"):
            if STAT_LINE_RE.match(raw[1:]):
                removed += 1
            if RULE_LINE_RE.match(raw[1:]) and not raw[1:].lstrip().startswith("neverallow"):
                removed_keys.append(re.sub(r"\s*\{.*", "", raw[1:].strip()))
    modcnt = len(set(added_keys) & set(removed_keys))
    print("A=%d  D=%d  M=%d" % (added, removed, modcnt))
    print("ROM increment estimate = (A - D + M) × 100B = %d B" % ((added - removed + modcnt) * 100))


def main():
    ref = sys.argv[1] if len(sys.argv) > 1 else "HEAD"
    diff_text, desc, target_tree = get_diff(ref)
    if not diff_text.strip():
        sys.stderr.write(
            "ERROR: empty diff for target '%s'. Check the git ref or policy paths "
            "(an empty net diff means no changes to review).\n" % desc
        )
        sys.exit(1)
    print("Scan target: %s" % desc)
    file_count = sum(1 for raw in diff_text.splitlines() if raw.startswith("+++ b/"))
    rule_count = sum(
        1
        for raw in diff_text.splitlines()
        if raw.startswith("+") and not raw.startswith("+++") and RULE_LINE_RE.match(raw[1:])
    )
    print("Policy files involved: %d (sepolicy/ + service_contexts + whitelist/)" % file_count)
    print("New rule lines (allow/allowxperm/neverallow, indented included): %d" % rule_count)

    files = parse_diff(diff_text)
    check_s1(diff_text)
    check_s2a(files)
    check_s2b(diff_text)
    check_s3(diff_text)
    check_s7(files)
    check_s4_s11(files, target_tree)
    check_s5_s6(diff_text)
    check_s9_s10_s13(diff_text, files)
    check_s11a(diff_text)
    check_s11d(files)
    check_s11c(diff_text)
    check_s12(files)
    check_s15(diff_text)
    check_s16(files)
    check_s17(files)
    check_s18(files)
    check_s19(files)
    check_s20(files)
    check_s20b(files)
    check_s21(diff_text)
    check_s22(diff_text)
    check_s23(files)
    rom_estimate(diff_text)
    print()
    print(
        "=== Auto-check complete. Items above needing manual/semantic analysis: "
        "S2-B qualification / S4 placement / S5 guardrail / S6 scope / S7 write+execute / "
        "S9-S10 isolation / S11 review / S17 pairing / S18-B/C placement / S20b binder IPC / "
        "S21 samgr review / S22 flex review ==="
    )


if __name__ == "__main__":
    main()
