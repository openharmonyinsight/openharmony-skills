# System Ability Trust Boundary Review

## Expert Checks

System Ability calls often cross privilege boundaries. A high-privilege SA must not become a confused deputy that performs sensitive work for a lower-privilege caller.

Check for:
1. "Internal caller", "system service caller", SA ID, UID, bundle name, or process-name allowlists that skip operation-specific permission.
2. Cross-SA requests that lose the original caller identity.
3. High-privilege services performing file, settings, hardware, account, user, device, callback, or notification work for another component.
4. Remote objects, file descriptors, error codes, and return values from another SA used without validation.
5. Listener/callback/death recipient registration that stores remote objects without caller validation.
6. Authorization decisions reused for a different resource, user, account, device, or operation.

## High-Risk Patterns

```cpp
// VULNERABLE: trusts any system ability caller
if (IsSystemAbilityCaller(IPCSkeleton::GetCallingUid())) {
    return UpdateSecureSetting(key, value);
}
```

```cpp
// REQUIRED: narrow caller allowlist plus operation permission
uint32_t tokenId = IPCSkeleton::GetCallingTokenID();
int32_t uid = IPCSkeleton::GetCallingUid();
if (!IsAllowedSystemAbility(uid) ||
    AccessTokenKit::VerifyAccessToken(tokenId, PERMISSION_UPDATE_SECURE_SETTING) != PERMISSION_GRANTED) {
    return ERR_PERMISSION_DENIED;
}
return UpdateSecureSetting(key, value);
```

## Finding Standard

A strong confused-deputy finding names:
- The lower-privilege or less-trusted caller path.
- The higher-privilege service action.
- The missing preservation or recheck of original authority.
- The concrete data, resource, or system state exposed or modified.
