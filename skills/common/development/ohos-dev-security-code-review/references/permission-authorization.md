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
