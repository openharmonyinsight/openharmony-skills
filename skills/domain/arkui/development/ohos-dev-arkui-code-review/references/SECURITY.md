# ACE Engine Security Patterns

Security review focus areas specific to ACE Engine. Generic vulnerability patterns (SQL injection, buffer overflow) are not repeated here — flag them when seen, but the following are the domain-specific security concerns in this codebase.

---

## Layer Boundary as Security Boundary

The four-layer architecture is a security boundary. Platform APIs (Rosen::, OS calls) must not be called directly from Pattern/Property code — they must go through the Platform Adapter layer.

```cpp
class MenuPattern {
    void Show() {
        Rosen::WindowManager::GetInstance()->Show();
    }
};

class MenuPattern {
    void Show() {
        auto* renderContext = GetRenderContext();
        if (renderContext) {
            renderContext->SetVisible(true);
        }
    }
};
```

---

## Input Surface in ACE Engine

| Input Source | Risk | Check |
|-------------|------|-------|
| ArkTS property setters via Model | Type mismatch, negative dimensions, overflow | Validate in ModelNG before applying to LayoutProperty |
| File paths in resource loading | Path traversal | Validate through Resource system, never concatenate raw paths |
| `system()` / `popen()` calls | Command injection | CRITICAL — flag immediately |
| User-influenced data in `sprintf` / `strcpy` | Buffer overflow | CRITICAL — flag immediately |

---

## Sensitive Data Logging

```cpp
LOGI("Password: %{private}s", password.c_str());
LOGI("User data: %{private}s", userData.c_str());

LOGI("Password: %{public}s", password.c_str());
LOGI("API token: %{public}s", api_token.c_str());
```

**Rule:** Use `%{private}s` for any data that could contain user information, tokens, or credentials. Use `%{public}s` only for non-sensitive operational data (IDs, counts, flags).

---

## ArkTS Bridge Security

```typescript
const result = eval(userInput);
element.innerHTML = userInput;

element.textContent = userInput;
```

When reviewing `bridge/declarative_frontend/` code:
- Verify ArkTS property setters validate parameter types before calling `ModelNG::SetXxx()`
- Ensure `ResourceType` usage is correct — raw string resources must go through `$r()` or `Resource` wrapper
- Check that `@Component` structs use proper TypeScript types, not `any` or unchecked casts

---

## Severity

| Issue | Severity |
|-------|----------|
| `system()`/`popen()` with user-influenced input | CRITICAL |
| `strcpy`/`sprintf`/`gets` with user-controlled size | CRITICAL |
| Layer boundary violation (security boundary) | CRITICAL |
| Sensitive data logged with `%{public}s` | HIGH |
| Missing input validation in ModelNG setters | HIGH |
| `eval()` / `innerHTML` with user input in bridge code | HIGH |
| Hardcoded secrets in component code | HIGH |
