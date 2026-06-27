# Implementation Checklist

Track adaptation progress across all 7 phases. Check off items as they complete.

## Phase 1: Information Collection
- [ ] Module name collected
- [ ] Repository name verified (if needed)
- [ ] `{module}-info.md` written

## Phase 2: Code Sync
- [ ] Repository verified on GitCode
- [ ] Code synced (if needed)
- [ ] Plugin structure created (if needed)
- [ ] `{module}-info.md` updated with sync status

## Phase 3: API Analysis
- [ ] .d.ts file analyzed
- [ ] Coverage percentage calculated
- [ ] Interfaces needing adaptation listed
- [ ] `{module}-api-inventory.md` written

## Phase 4: Architecture Analysis
- [ ] Code volume statistics collected
- [ ] Platform dependency ratio calculated
- [ ] Dependencies identified
- [ ] **Platform implementation necessity analyzed** (C/C++ native vs platform-specific)
- [ ] `{module}-architecture.md` written

## Phase 5: Architecture Recommendation
- [ ] Architecture mode selected
- [ ] Developer confirms choice
- [ ] `{module}-plan.md` written (execution plan + E2E test case spec)

## Phase 6: Implementation
- [ ] Pure virtual interface defined (OHOS repo)
- [ ] OHOS thin wrapper implemented (OHOS repo)
- [ ] Android adapter implemented (Plugin repo)
- [ ] iOS adapter implemented (Plugin repo)
- [ ] Build configuration updated
- [ ] Configuration files generated (4 files)
- [ ] Unit tests written
- [ ] Compilation successful (all platforms)
- [ ] Tests passing
- [ ] Verification evidence collected (via verification-before-completion)

## Phase 7: End-to-End Verification
- [ ] Framework built (Android + iOS)
- [ ] SDK overlaid with new build artifacts
- [ ] Test project created (ace create)
- [ ] Test code generated from `{module}-plan.md` test spec section
- [ ] Android: `ace build apk && ace run apk` — app launches, tests pass
- [ ] iOS: `ace build app && ace run app` — app launches, tests pass
- [ ] Log validation clean (no ERROR / Fatal / SIGABRT / SIGSEGV)
- [ ] `{module}-e2e-report.md` written with per-API per-platform pass/fail

## Mandatory Configuration Files

After code generation, ensure all 4 files are updated:

- [ ] `plugins/plugin_lib.gni` - Module entry
- [ ] `interface/sdk/plugins/api/apiConfig.json` - Library configuration
- [ ] `build_plugins/sdk/arkui_cross_sdk_description_std.json` - Build entries
- [ ] `interface/sdk-js/api/@ohos.{module}.d.ts` - @crossplatform annotations
