---
name: ohos-dev-arkts-sta-playground
description: Execute isolated ArkTS-Sta snippets or .ets files through the remote ArkTS-Sta Playground compile API. Use when validating ArkTS static syntax, checking small language-feature examples, reproducing compiler diagnostics, comparing expected compile failures, batch-checking standalone snippets, or demonstrating snippet output before using a real OpenHarmony project build.
metadata:
  author: openharmony
  scope: common
  stage: development
  domain: arkts
  capability: sta-playground
  version: 0.1.0
  status: draft
  tags:
    - arkts
    - arkts-sta
    - playground
    - testing
---

# ArkTS-Sta Playground

Use this skill as a remote compiler probe for small, self-contained ArkTS-Sta examples. It answers "does this isolated ArkTS-Sta snippet compile, and what diagnostic does it produce?"

## Use Boundary

Use it for:
- ArkTS-Sta syntax probes and language-feature minimization.
- Expected-failure tests where the exact compiler diagnostic matters.
- Batch checks of standalone `.ets` examples with `--json`.

Do not use it for:
- Proving an OpenHarmony app, HAP, XTS suite, module config, SysCap, resource, import graph, permission, or device-runtime scenario works.
- Code that is proprietary, unreleased, customer-owned, or security-sensitive. The snippet is sent to a remote endpoint.

If the code needs project declarations, decorators, build flags, generated files, or framework runtime behavior, use the project build workflow instead. If possible, first reduce the question to a self-contained snippet and only then use this playground.

## Script Contract

Prefer the bundled script over raw `curl`:

```bash
python3 scripts/run_playground.py path/to/code.ets
python3 scripts/run_playground.py --json --code "console.log('Hello');"
```

The endpoint is POST-only:

```text
https://arkts-play.cn.bz-openlab.ru:10443/compile
```

Opening the URL in a browser sends GET and normally returns `405 Method Not Allowed`; that does not mean the API is down.

## Result Rules

- `success: true` means the remote compiler accepted this isolated snippet. It does not mean an OpenHarmony project builds.
- `has_error: true` is useful for negative tests only when `output` points to the intended language rule.
- Request failures, timeouts, SSL errors, and malformed JSON are tool failures, not ArkTS language results.
- Empty successful output usually means the snippet compiled but did not print anything; add a minimal use site if the test needs observable output.

For positive tests, include enough code to force the relevant check. For example, instantiate the class, call the function, or assign the typed value instead of only declaring unused shapes.

For negative tests, isolate one rule per snippet. Multiple unrelated violations make the first diagnostic hide the real question.

## NEVER

NEVER report a playground pass as proof that a HAP, XTS suite, or OpenHarmony module compiles.

NEVER send sensitive code to the remote compile API.

NEVER accept "any compile error" as a valid negative test. Match the diagnostic to the intended rule.

NEVER mix framework/API behavior with ArkTS-Sta language behavior in one probe.

NEVER conclude the API is unavailable from a browser `Method Not Allowed` page; verify with POST or the bundled script.
