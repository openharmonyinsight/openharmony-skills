---
name: ohos-dev-security-code-review
description: Use when reviewing OpenHarmony C++ system service, System Ability, Stub, IPC, MessageParcel, AccessToken, permission, privacy log, or shared-state concurrency code for security vulnerabilities.
metadata:
  author: openharmony
  scope: common
  stage: development
  domain: security
  capability: code-review
  version: 0.2.0
  status: draft
  tags:
    - security
    - code-review
    - cpp
    - ipc
    - concurrency
    - privacy
---

# OpenHarmony Security Code Review

## Core Principle

Review OpenHarmony system-service code as a boundary between untrusted callers and privileged system state. A valid finding must connect an attacker-controlled entry point to a sensitive operation, missing validation, unsafe shared state, or information disclosure with a plausible impact.

## When to Use

Use for OpenHarmony C++ system-service code, especially:
- `*Stub`, `*Service`, `*Ability`, `OnRemoteRequest`, IPC transaction handlers
- `MessageParcel`, `IRemoteObject`, file descriptor, JSON/XML/Protobuf/network input parsing
- `IPCSkeleton`, `AccessTokenKit`, permission checks, System Ability allowlists
- Shared containers or service state reached by IPC, callbacks, timers, or worker threads
- HILOG output that may expose user data, input events, object addresses, or internal state

Do not use for application-layer feature review, non-OpenHarmony C++ code, or pure performance/style review.

## Review Route

1. **Map entry points.** Start at `OnRemoteRequest`, Stub dispatchers, exported service methods, listener/callback registration, and network-facing parsers.
2. **Mark attacker-controlled data.** Treat all `MessageParcel` fields, remote objects, fds, bundle names, UID/PID/token fields supplied by clients, and cross-SA return values as untrusted until proven otherwise.
3. **Trace to sensitive sinks.** Follow data and control flow into file/system settings, hardware, account/user data, persistent state, callbacks, cross-user/cross-device operations, logging, and shared containers.
4. **Check boundary guarantees.** Confirm deserialization success checks, logical bounds, caller identity source, operation-specific permission, fail-closed errors, and lock consistency.
5. **Report only exploitable paths.** Avoid generic "should lock/check" comments unless the code path is reachable and the impact is concrete.

## Load References

Load only the reference files needed for the code under review:

| Scenario Detected | Mandatory Reference | Do NOT Load |
| --- | --- | --- |
| `MessageParcel`, fd, `IRemoteObject`, network parser, deserialization | [`references/ipc-input-validation.md`](references/ipc-input-validation.md) | Concurrency/privacy refs unless touched |
| Shared member/global/static state, containers, callbacks, async work, locks | [`references/concurrency-review.md`](references/concurrency-review.md) | IPC/privacy refs unless touched |
| HILOG, `%{public}`, `%p`, phone/contact/SMS/biometric/input-event data | [`references/privacy-logging.md`](references/privacy-logging.md) | IPC/concurrency refs unless touched |
| `IPCSkeleton`, `AccessTokenKit`, permissions, transaction codes | [`references/permission-authorization.md`](references/permission-authorization.md) | Concurrency/privacy refs unless touched |
| Cross-System Ability calls, "internal caller", SA allowlist, confused-deputy risk | [`references/system-ability-trust-boundary.md`](references/system-ability-trust-boundary.md) | Other refs unless touched |

If several scenarios apply to the same path, load each matching reference. If none apply, use a general security review skill instead.

## Severity Calibration

Report as **HIGH SECURITY RISK** when an untrusted or lower-privilege caller can plausibly cause one of:
- Unauthorized access to user data, hardware, system settings, account/device state, or privileged IPC behavior
- Persistent state mutation without server-side authorization
- Memory corruption, use-after-free, iterator invalidation, or denial of service in a privileged service
- Sensitive data, raw input events, or memory layout disclosure
- Confused-deputy behavior across System Abilities

Downgrade or skip when:
- The path is not externally reachable and has a clear trusted-only invariant
- Authorization occurs in a shared helper you have verified on every branch
- The issue is only style, theoretical cleanup, or a missing comment
- A lock warning lacks a plausible concurrent caller or async path

## Never Do

- NEVER treat `ReadInterfaceToken()` or descriptor checks as authorization; they only verify interface type.
- NEVER trust UID, PID, token ID, bundle name, or permission flags read from `MessageParcel`.
- NEVER re-read IPC caller identity inside delayed async work after the original IPC context may be gone.
- NEVER assume "internal", "system service", or another SA caller is automatically authorized for the requested operation.
- NEVER let permission failure merely log, assert, or record statistics before continuing with side effects.
- NEVER report a generic missing validation issue without naming the attacker-controlled field and the sink it reaches.
- NEVER log PII, raw input events, or pointer addresses as public diagnostic data.

## Output Format

Use this format for confirmed vulnerabilities:

````markdown
**[HIGH SECURITY RISK] <category>**

Location: <file_path>:<line_number>

Issue: <what untrusted caller controls, what check is missing, and what sink is reached>

Evidence:
```cpp
<minimal relevant code>
```

Required fix:
```cpp
<focused fix or required invariant>
```

Impact: <attacker capability if exploited>
````

If evidence is incomplete, state the exact follow-up needed instead of filing a finding.
