# AGENTS.md — Window Manager (OpenHarmony)

This repo is the window management subsystem of OpenHarmony. It provides core capabilities for window and display management, serving as the foundational subsystem for UI display. See [README.md](./README.md) for full architecture details.

## What is `window_manager`

`window_manager` is a `Client-Server` architecture subsystem. Key modules:
- `wm/` — Window Manager Client
- `dm/` — Display Manager Client
- `wmserver/` — Window Manager Server (separated arch)
- `dmserver/` — Display Manager Server
- `window_scene/` — Window Manager Server (unified arch)
- `interfaces/innerkits/` — Native APIs
- `interfaces/kits/` — JS/NAPI APIs
- `extension/` — Ability Component window integration
- `utils/` — Shared utilities

Two compile-time architectures are selected via `window_manager_use_sceneboard` (set externally by the OpenHarmony build system):

| Value | Architecture | Key module compiled |
|-------|-------------|---------------------|
| `false` | Separated | `wmserver/` |
| `true` | Unified | `window_scene/` |

## WorkFlow

### CodeStyle specification
You must follow the [CodeStyle](./docs/CodeStyle.md) specification when you write code.

Key rules:
- **C++ standard**: C++11; **Column limit**: 120; **Indent**: 4 spaces, no tabs
- **Namespace**: always `OHOS::Rosen`
- **Naming**: Classes `PascalCase`, methods `camelCase`, member vars `camelCase_`, constants `UPPER_SNAKE_CASE`, files `snake_case`
- **Include order**: corresponding header → stdlib → OH framework → `interfaces/` → other internal
- **Logging**: `TLOGD` / `TLOGI` / `TLOGW` / `TLOGE`
- **Error handling**: return `WMError`/`WmErrorCode`; early-return with `WLOGFE` log
- **Memory**: `sptr<T>` for IPC/singletons, `wptr<T>` for weak refs; prefer RAII
- Every source file must begin with the Apache 2.0 license header

### Testing specification
You must follow the [Testing](./docs/Testing.md) specification after you write testing code and keep testing suite pass.

### Git Commit Rules

- **User approval required**: Ask user before `git commit`. Use `git commit -s` after approval.
- **Angular format**: `type(scope): subject` (feat, fix, docs, style, refactor, test, chore)
- **Co-authored footer**: Append `Co-Authored-By: Agent` to every commit message.

Example:
```
feat(auth): add user login feature

Signed-off-by: Your Name <your.email@example.com>
Co-Authored-by: Agent
```
