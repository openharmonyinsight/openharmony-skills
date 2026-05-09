---
name: ohos-dev-security-code-review
description: Use when reviewing OpenHarmony native/C++ system services for security vulnerabilities, especially IPC Stub/OnRemoteRequest transaction authorization, MessageParcel/fd/callback validation, AccessToken permission checks, System Ability confused-deputy paths, cross-user/account/device access, privacy log leaks, or shared-state races.
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
4. **Check boundary guarantees.** Confirm deserialization success checks, logical bounds, caller identity source, operation-specific permission, user/account/device binding, fail-closed errors, and lock/lifetime consistency.
5. **Report only exploitable paths.** Avoid generic "should lock/check" comments unless the code path is reachable and the impact is concrete.

## Load References

Load only the reference files needed for the code under review:

| Scenario Detected | Required Reference Loading | Do NOT Load |
| --- | --- | --- |
| `MessageParcel`, fd, `IRemoteObject`, network parser, deserialization | MANDATORY - read entire [`references/ipc-input-validation.md`](references/ipc-input-validation.md) before judging matched paths | Concurrency/privacy refs unless touched |
| Shared member/global/static state, containers, callbacks, async work, locks | MANDATORY - read entire [`references/concurrency-review.md`](references/concurrency-review.md) before judging matched paths | IPC/privacy refs unless touched |
| HILOG, `%{public}`, `%{private}`, `%p`, phone/contact/SMS/biometric/input-event data | MANDATORY - read entire [`references/privacy-logging.md`](references/privacy-logging.md) before judging matched paths | IPC/concurrency refs unless touched |
| `IPCSkeleton`, `AccessTokenKit`, permissions, transaction codes, user/account/device ids | MANDATORY - read [`references/permission-authorization.md`](references/permission-authorization.md), then trace from public entry to final authorization decision | Concurrency/privacy refs unless touched |
| Cross-System Ability calls, "internal caller", SA allowlist, confused-deputy risk | MANDATORY - read [`references/system-ability-trust-boundary.md`](references/system-ability-trust-boundary.md), then prove the caller trust boundary | Other refs unless touched |

If several scenarios apply to the same path, load each matching reference. If none apply, use a general security review skill instead.

## Severity Calibration

Report as **HIGH SECURITY RISK** when an untrusted or lower-privilege caller can plausibly cause one of:
- Unauthorized access to user data, hardware, system settings, account/device state, or privileged IPC behavior
- Persistent state mutation without server-side authorization
- Memory corruption, use-after-free, iterator invalidation, or denial of service in a privileged service
- Sensitive data, raw input events, or memory layout disclosure
- Confused-deputy behavior across System Abilities

Downgrade or skip only after applying this evidence gate:

| Observation | Required proof before reporting | Downgrade or skip if |
| --- | --- | --- |
| Missing direct permission call | Public entry, transaction code, handler, and final authorization decision are all traced | A shared helper enforces the same permission, caller type, and user/account/device boundary on every branch |
| Trusted-only, native, shell, root, or SA path | Lower-privilege callers can reach or influence the path, or the exception applies in production/user builds | The exception is narrow, documented, and unreachable from lower-privilege callers |
| Cross-user/account/device parameter | Caller can choose another user's/account's/device's resource and reach a sensitive sink | The value is bound to the caller token or guarded by explicit cross-boundary authority |
| Race or TOCTOU suspicion | Two reachable callbacks, IPC calls, timers, work items, or threads can interleave on the same state | The state is provably thread-confined, immutable after publication, or protected by a verified higher-level owner |
| Logging concern | The log exposes PII, credentials, input activity, pointers, user file data, or reconstructable private context | The value is suppressed, non-sensitive, or irreversibly coarse enough that no user/resource can be inferred |
| Style or hygiene issue | The path reaches a sensitive operation with attacker-controlled data and concrete impact | The concern is only cleanup, documentation, or defensive style without exploitable impact |

## Never Do

- NEVER treat `ReadInterfaceToken()` or descriptor checks as authorization; they only verify interface type.
- NEVER assume generated Stub/IDL dispatch performs permission checks for individual transaction codes.
- NEVER trust UID, PID, token ID, bundle name, or permission flags read from `MessageParcel`.
- NEVER re-read IPC caller identity inside delayed async work after the original IPC context may be gone.
- NEVER assume "internal", "system service", or another SA caller is automatically authorized for the requested operation.
- NEVER treat `%{private}` as permission to log credentials, tokens, account data, file contents, or reconstructable private context.
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
