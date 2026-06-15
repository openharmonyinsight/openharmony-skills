# Phase 1: Information Collection

## Overview

Collect the minimal information needed to start the adaptation process. The key deliverable is the module name — repository details are resolved in Phase 2.

## Prerequisites

This skill executes within an **ArkUI-X SDK source tree** (the directory containing `.repo/`, `plugins/`, `interface/`). The d.ts file is at:

```
interface/sdk-js/api/@ohos.{module_name}.d.ts
```

If you are in an **application project** (contains `entry/`, `.arkui-x/`), this skill does not apply — app-level extension uses CMake + Gradle/Xcode, not the BUILD.gn-based 7-phase workflow.

## Information Collected

### Required: API Module Name

The ArkTS API module to be adapted.

- **Format**: `@ohos.{module_path}`
- **Examples**:
  - `@ohos.data.preferences`
  - `@ohos.settings`
  - `@ohos.multimedia.image`
- **d.ts Location**: `interface/sdk-js/api/@ohos.{module_path}.d.ts` (relative to SDK root)

### Resolved in Phase 2 (Not Here)

Repository name, local path, and revision are resolved during Phase 2's code sync step. Do NOT ask for them upfront — the module may already be in `openharmony.xml`.

## Decision Flow

```
Module Name Collected
        ↓
   Phase 2: Check openharmony.xml
        ↓
   ┌─────────────────────────┐
   │ OHOS repo in manifest?  │
   └─────────────────────────┘
        ↓             ↓
      YES           NO
        ↓             ↓
   Analyze code   Ask developer
   directly       for repo info
                      ↓
                 Add to manifest
                 + repo sync
                      ↓
                 Analyze code
```

## Example Dialogue

```
🔍 Phase 1: Information Collection

Please provide the API module you want to adapt:

Example: @ohos.data.preferences
Your input: @ohos.settings
```

## Best Practices

1. **Minimal Initial Collection**: Only ask for module name upfront
2. **Lazy Repository Resolution**: Don't ask for repo details until Phase 2 determines they're needed
3. **One Input**: Developer provides just the `@ohos.*` name — everything else is derived

## Related Files

- **Phase 2**: [phase2-code-sync.md](phase2-code-sync.md) - OHOS source code acquisition
