# Phase 1: Information Collection

## Overview

This phase collects the minimal information needed to start the adaptation process. The skill uses lazy evaluation - only collecting repository details when actually needed.

## Information Collected

### Required Information (Always Collected)

**1. API Module Name**

The ArkTS API module to be adapted.

- **Format**: `@ohos.{module_path}`
- **Examples**:
  - `@ohos.data.preferences`
  - `@ohos.intl`
  - `@ohos.multimedia.image`

### Optional Information (Collected as Needed)

**2. OHOS Repository Name** (Collected in Phase 2 if needed)

The name of the OHOS repository containing the module implementation.

- **⚠️ Important**: The repository name may not match the module name
- **Verification**: Check at https://gitcode.com/org/openharmony/repos
- **Common Patterns**:
  - `{subsystem}_{module}` (e.g., `distributeddatamgr_preferences`)
  - `{module}` (e.g., `preferences`)
  - `{category}_{subsystem}_{module}` (e.g., `ability_ability_runtime`)

**3. Local Storage Path** (Optional, defaults to standard location)

Where the OHOS code will be stored locally.

- **Example**: `foundation/distributeddatamgr/preferences`
- **Default**: Determined from repository name

## Example Dialogue

```
🔍 Phase 1: Information Collection

Please provide the API module you want to adapt:

Example: @ohos.data.preferences
Your input: @ohos.intl
```

## Decision Flow

After collecting the module name, the skill proceeds to Phase 2 (Code Existence Check) to determine if additional information is needed.

```
Module Name Collected
        ↓
   Phase 2: Check if code exists
        ↓
   ┌─────────────────────┐
   │ Code already exists? │
   └─────────────────────┘
        ↓             ↓
      YES           NO
        ↓             ↓
    Skip to      Collect repo details
  Phase 3       & sync code
```

## Best Practices

1. **Minimal Initial Collection**: Only ask for module name upfront
2. **Lazy Evaluation**: Collect repository details only when Phase 2 determines code sync is needed
3. **Interactive Correction**: If repository verification fails, provide suggested names and allow correction
4. **Clear Examples**: Show concrete examples of expected input format

## Related Files

- **Phase 2**: [CODE_SYNC.md](phase2-code-sync.md) - Code existence check and sync process
- **Repository Search**: https://gitcode.com/org/openharmony/repos
