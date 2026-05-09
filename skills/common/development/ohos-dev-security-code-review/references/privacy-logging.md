# Privacy And Logging Review

## Expert Checks

OpenHarmony logs are security boundaries because privileged services can observe private user activity and internal memory state. Review both explicit log arguments and values embedded in helper-generated strings.

Flag public logging of:
- Phone numbers, contacts, SMS content, account data, biometric data, credentials, tokens, precise location
- Raw `KeyEvent`, touch coordinates, screen bounds, window rectangles, input timing, or gesture traces
- File paths that expose user/account/app private data
- Pointer addresses, object addresses, buffer addresses, or `%p` output
- User/account/device boundary data that can link activity across local users, app twins, or distributed devices

## High-Risk Patterns

```cpp
// VULNERABLE: user data and input coordinates are public
HILOG_INFO("Phone: %{public}s", phone.c_str());
HILOG_INFO("Touch at %{public}d,%{public}d", x, y);
HILOG_DEBUG("object=%{public}p", object);
```

```cpp
// REQUIRED: suppress or redact
HILOG_INFO("Processing phone number");
HILOG_INFO("Touch event received");
HILOG_DEBUG("object id=%{public}d", objectId);
```

## `%{private}` Gate

Use `%{private}` only when the value is genuinely needed for diagnostics. Prefer complete suppression in release paths for highly sensitive values.

`%{private}` is not sufficient when the log still records:
- credentials, tokens, secrets, permission names tied to a specific caller, or authentication material;
- account identifiers, hardware identifiers, user file names, file contents, message contents, biometric data, or precise location;
- enough public surrounding context to reconstruct private user activity, cross-user access, or distributed-device behavior;
- sensitive values embedded into the format string before HiLog receives them;
- the same data through non-HiLog paths, HiSysEvent payloads, dumps, traces, or helper-generated strings without privacy marking.

For such cases, require suppression, coarser event labels, counters, result codes, or stable non-reversible IDs.

## Impact Language

- PII exposure: unauthorized disclosure through system logs.
- Input-event exposure: reconstruction of user activity, screen content, or interaction patterns.
- Pointer exposure: ASLR weakening that can make separate memory-corruption bugs easier to exploit.
