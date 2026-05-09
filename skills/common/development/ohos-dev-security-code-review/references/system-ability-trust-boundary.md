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

## Trusted-Only Path Gate

A System Ability path may be a false positive only when the code proves all of these:
- The reviewed method is reachable only from a narrow SA/native token/UID allowlist or private in-process path.
- Lower-privilege apps cannot directly call the Stub transaction, obtain the same proxy, or influence the trusted SA to perform the action.
- The trusted caller is authorized for this operation, not just for being a system component.
- User/account/device/resource parameters are either inherited from the original caller or revalidated before the privileged action.

SA registration, SAMgr lookup, or "internal" naming is never enough by itself.

## Confused-Deputy Drift

When one SA calls another, preserve or recheck the original authority if the callee performs file, hardware, account, notification, setting, fd, or callback work. Report drift when a lower-privilege caller can cause a higher-privilege SA to use its own identity for a resource the caller could not access directly.

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
