# PR Triage Patterns for Security Relevance

Used to scan a repo's open PR list and classify which ones need security attention.

## Fetch Command

```bash
oh-gc pr list --repo <owner>/<repo> --state open --limit 50 --json
```

Filter criteria:
- `state` not in (`merged`, `closed`) — only open/active PRs
- `updated_at` >= cutoff date (e.g., last 7 days)
- Sort by `updated_at` descending for recency

## Classification by Title Keywords

### 🔴 HIGH — Direct Security Boundary Changes

| Pattern | Example Titles |
|---|---|
| Permission/authz changes | `enforce SA caller`, `permission check`, `add permission`, `权限校验`, `权限优化` |
| URI/Access control | `grantUriPermission`, `revokeUri`, `UriPerm`, `access control` |
| IPC/Stub/OnRemoteRequest | `OnRemoteRequest`, `transaction handler`, `IPC dispatch` |
| Token/Identity | `AccessToken`, `caller identity`, `token validation` |
| SA trust boundary | `SA caller`, `System Ability allowlist`, `confused deputy` |

### 🟡 MEDIUM — Indirect or Large-Scale Changes

| Pattern | Example Titles |
|---|---|
| Input validation / crash fix | `replace stoi`, `prevent crash`, `input validation`, `参数校验` |
| New public API / interface | `add invokeFunction`, `对外接口`, `public API`, `NAPI binding` |
| SA loading / initialization | `SA load`, `manager init`, `整改加载方式` |
| EDM / device management | `fix edm`, `enterprise device`, `kiosk`, `展台` |
| App install / debug | `install debug`, `开发者模式`, `debugger` |
| Large diff new code | Any PR with +1000 lines, especially if in `services/` or `interfaces/` |
| Agent/Skill framework | `skill`, `agent`, `RemoveSkillParam` — ability_runtime SA 185 area |

### 🟢 LOW — Unlikely Security Impact

| Pattern | Example Titles |
|---|---|
| Pure error message / log fixes | `fix log`, `errInfo`, `错误信息整改`, `innerErrorMsg` |
| GC / freeze diagnostics | `GC时间`, `appfreeze屏蔽`, `freeze代码优化` |
| Render / UI process | `renderSession`, `render process` |
| Pure refactoring | `refactor`, `Optimize the internal code` (small diffs) |
| Build config | `gn adapt` |

## Context-Specific Signals (ability_ability_runtime)

The ability_runtime repo has a code map in `AGENTS.md`. When triaging, map PR titles to these high-risk areas:

| Area | Risk Signal |
|---|---|
| `services/abilitymgr/` (SA 180) | Component lifecycle, startup interception, mission stack |
| `services/appmgr/` (SA 501) | App process lifecycle, AppSpawn |
| `services/uripermmgr/` (SA 183) | Cross-app URI permission — always security-relevant |
| `services/common/` | `PermissionVerification` — global security entry point |
| `interfaces/kits/` | Public SDK API — check permission and compatibility |
| `agent_runtime_framework/` (SA 185) | Agent/Skill framework — growing attack surface |

## Output Format for Triage

Present results as a grouped table to the user:

```markdown
## 🔴 高风险（强烈建议安全检视）— N 个
| PR | 标题 | 作者 | diff | 理由 |

## 🟡 中风险（建议检视）— N 个
...

## 🟢 低风险（可选关注）— N 个
...

**建议优先级**: ...
```

Then ask the user which PR(s) to deep-review before proceeding.
