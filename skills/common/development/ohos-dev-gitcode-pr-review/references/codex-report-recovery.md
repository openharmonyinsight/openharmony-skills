# Recovering the full Codex report from the session JSONL

## When to use

The `codex exec` run finished but the full review report is missing or truncated:

1. The `-o /tmp/codex-pr-N-report.md` file contains only a short summary (Codex overwrites
   it at the end with its final assistant message), OR
2. The process log was truncated because the launch command piped through `| tail -N`
   (the report header — usually the high-severity findings — is silently dropped).

The full report is preserved verbatim in the Codex session JSONL as the `apply_patch`
custom tool call that wrote the report file.

## Recovery script

```bash
# Find today's session rollout file (most recent one):
ls -t ~/.codex/sessions/$(date +%Y/%m/%d)/rollout-*.jsonl | head -1
```

```python
import json, re, glob, os

# Pick the newest rollout file (or pass the path explicitly)
paths = glob.glob(os.path.expanduser('~/.codex/sessions/*/*/*/rollout-*.jsonl'))
path = max(paths, key=os.path.getmtime)
print('reading', path)

msgs = []
with open(path) as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            msgs.append(json.loads(line))
        except Exception:
            pass

# Find the custom_tool_call whose input contains the apply_patch that wrote the report
for i, m in enumerate(msgs):
    p = m.get('payload', {})
    if m.get('type') == 'response_item' and p.get('type') == 'custom_tool_call':
        inp = p.get('input')
        if isinstance(inp, str) and '*** Begin Patch' in inp:
            m2 = re.search(r'\*\*\* Begin Patch\\n(.*?)\\n\*\*\* End Patch', inp, re.S)
            if m2:
                # Unescape the JSON-stringified patch content
                content = m2.group(1).replace('\\n', '\n').replace('\\"', '"')
                # Strip the Add File header line if present
                content = re.sub(r'^\*\*\* Add File: [^\n]*\n', '', content)
                out = '/tmp/codex-pr-recovered-report.md'
                with open(out, 'w') as f:
                    f.write(content)
                print(f'recovered {len(content)} chars -> {out}')
```

## Notes

- The `input` field is a **JS code string** (`const patch = "*** Begin Patch\n...*** End Patch";`),
  NOT pure JSON — `json.loads(inp)` fails. Regex directly against the raw string.
- If the report file was written via `apply_patch` (msg type `patch_apply_end` / custom tool
  `exec`), it appears as a `custom_tool_call` response_item; if written via heredoc it may only
  exist in shell stdout.
- The report may ALSO be split: Codex sometimes writes the body to the file and prints only a
  summary to stdout. The JSONL recovery covers the body.
- Production case: PR 316 (2026-08-04). Launch used `2>&1 | tail -80`; the visible log ended at
  the 8th medium finding and the `-o` file was a 10-line summary. Recovery pulled the full
  1-high / 8-medium / 1-low report from the session rollout.
