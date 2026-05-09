# Permission And Authorization Review

## Expert Checks

Server-side authorization is mandatory for privileged IPC. Client-side checks, descriptor checks, or SDK wrappers do not protect the service from direct IPC callers.

Check each exposed transaction branch:
1. The interface token is checked against the descriptor, but not treated as permission.
2. Caller identity is obtained from `IPCSkeleton::GetCallingTokenID()`, `GetCallingUid()`, or `GetCallingPid()`, not from client-controlled parcel fields.
3. Sensitive operations call `AccessTokenKit::VerifyAccessToken(callingTokenId, permission)` or a verified project wrapper.
4. Permission failure returns before state mutation, file access, hardware access, callback registration, cross-SA calls, or persistence.
5. Native token, shell/root, `system_basic`, `system_core`, unknown token types, and AccessToken service errors are explicit and fail closed unless a narrow documented exception applies.
6. New transaction codes do not bypass shared authorization helpers.
7. User, account, device, bundle, and token IDs supplied as parameters are bound to the calling token or guarded by a documented cross-user/cross-device permission.

## Authorization Matrix

For each `*_stub.cpp` or equivalent dispatcher, build a compact matrix before judging a missing-permission finding:

| Field | Question |
| --- | --- |
| `code` | Which transaction code reaches this branch? |
| `handler` | Which `Inner` method or service method handles it? |
| `required authority` | Which permission, native token, UID, or caller allowlist is required? |
| `boundary` | Which user/account/device/resource must match the caller? |
| `sink` | What sensitive data, state mutation, fd, callback, or cross-SA call follows? |

Treat adjacent handlers as evidence. If a new or sensitive transaction code lacks the permission or boundary checks used by comparable handlers, report `authorization drift` only after showing a lower-privilege caller can reach the weaker branch.

## Wrapper Verification Gate

Do not report a missing direct `VerifyAccessToken` call until you trace:
`OnRemoteRequest -> code dispatch -> handler -> local helper/wrapper -> final authorization decision`.

Valid wrappers may combine `VerifyAccessToken`, system-app checks, native-token checks, shell/root build exceptions, UID allowlists, or service-token checks. They are sufficient only when every branch fails closed and the wrapper enforces the same operation, resource, and user/account/device boundary as the handler needs.

## OpenHarmony-Specific Boundaries

- `TokenID` is not only an app identity; it can encode user and app-twin separation. Do not let callers pass an arbitrary `tokenId`, `userId`, `accountId`, `bundleName`, `instIndex`, `deviceId`, or `networkId` unless the service binds it to the caller or checks a cross-user/cross-device authority.
- `system_basic` or `system_core` APL reduces caller population but does not replace operation-specific permission for sensitive state.
- Native, shell, and root exceptions must be narrow: verify whether they are user-build disabled, debug-only, tied to one native service token, or limited to a non-sensitive query.
- A trusted AccessToken/System Ability caller path is a false-positive gate only when lower-privilege callers cannot obtain or influence that path.

## High-Risk Patterns

```cpp
// VULNERABLE: client supplies identity used for authorization
uint32_t callerToken = data.ReadUint32();
if (!HasPermission(callerToken, PERMISSION_DELETE_USER_DATA)) {
    return ERR_PERMISSION_DENIED;
}
```

```cpp
// REQUIRED: identity comes from IPC framework
uint32_t callerToken = IPCSkeleton::GetCallingTokenID();
if (AccessTokenKit::VerifyAccessToken(callerToken, PERMISSION_DELETE_USER_DATA) != PERMISSION_GRANTED) {
    return ERR_PERMISSION_DENIED;
}
```

```cpp
// VULNERABLE: descriptor check is not authorization
if (!data.ReadInterfaceToken().IsEmpty()) {
    return DeleteUserData(data, reply);
}
```

```cpp
// REQUIRED: descriptor first, operation permission next
if (data.ReadInterfaceToken() != GetDescriptor()) {
    return ERR_INVALID_DATA;
}
uint32_t tokenId = IPCSkeleton::GetCallingTokenID();
if (AccessTokenKit::VerifyAccessToken(tokenId, PERMISSION_DELETE_USER_DATA) != PERMISSION_GRANTED) {
    return ERR_PERMISSION_DENIED;
}
return DeleteUserData(data, reply);
```

## Async Caller Identity

If work is posted to another thread, capture the caller token/UID during the IPC call and pass it explicitly. Re-reading `IPCSkeleton` later may produce the service identity or an unrelated caller context.
