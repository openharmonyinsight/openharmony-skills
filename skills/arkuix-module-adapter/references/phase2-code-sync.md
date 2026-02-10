# Phase 2: Code Existence Check & Sync

## Overview

This phase intelligently checks if the OHOS module already exists in the project before attempting to sync. This avoids redundant operations and saves time.

## Decision Tree

```
┌─ Step 1: Check Manifest ─┐
│                          │
│ Found in manifest?       │
│    ├─ YES → Go to Step 2 │
│    └─ NO  → Go to Step 3 │
└──────────────────────────┘

┌─ Step 2: Check Plugins ───┐
│                           │
│ Plugin directory exists?  │
│    ├─ YES → ✅ Use existing │
│    └─ NO  → Go to Step 3   │
└───────────────────────────┘

┌─ Step 3: Verify & Sync ────┐
│                            │
│ 1. Verify repo exists     │
│ 2. Add to manifest        │
│ 3. Run repo sync          │
│ 4. Create plugin structure│
└────────────────────────────┘
```

## Step 1: Check Repo Manifest

Check if the module is already configured in `.repo/manifests/openharmony-master.xml`:

```bash
# Check if module exists in manifest
grep -i "{repository_name}" .repo/manifests/openharmony-master.xml

# Example for preferences:
grep -i "distributeddatamgr_preferences" .repo/manifests/openharmony-master.xml
```

**Output Scenarios**:

- ✅ **Found**: Module is configured in manifest, proceed to Step 2
- ❌ **Not found**: Module not configured, proceed to Step 3

## Step 2: Check Plugins Directory

Check if the module has already been adapted in the `plugins/` directory:

```bash
# Check if plugin directory exists
ls -la plugins/{module_name}/

# Example for preferences:
ls -la plugins/data/preferences/
```

**Decision Scenarios**:

1. **Both manifest and plugins exist**: ✅ Use existing adaptation
2. **Only manifest exists**: Plugin structure needs creation
3. **Neither exists**: Full sync required

## Step 3: Verify Repository & Sync (if needed)

Only perform sync if Step 1 and Step 2 both return negative.

### Step 3.1: Verify Repository on GitCode

**CRITICAL**: Before syncing, verify the repository exists on https://gitcode.com/org/openharmony/repos

```bash
# Method 1: Using curl (recommended)
curl -s "https://gitcode.com/org/openharmony/{repository_name}" | grep -q "404"

# Method 2: Using git ls-remote
git ls-remote https://gitcode.com/org/openharmony/{repository_name}.git

# Method 3: Manual verification
# Visit: https://gitcode.com/org/openharmony/repos
# Search for: {repository_name}
```

#### Scenario A: Repository Found ✅

```
📋 Step 3: Verify Repository & Sync

🔍 Verifying repository: 'distributeddatamgr_preferences'
📡 Querying: https://gitcode.com/org/openharmony/distributeddatamgr_preferences
✅ VERIFIED - Repository exists on GitCode

📋 Step 3.2: Sync Module
⚠️  Action Required:
   1. Adding to manifest...
   2. Running repo sync...
   3. Creating plugin structure...

✅ Sync complete: foundation/distributeddatamgr/preferences/
   Total files synced: 81
   Proceeding to Phase 3...
```

#### Scenario B: Repository Not Found ❌ - Interactive Correction

```
📋 Step 3: Verify Repository & Sync

🔍 Verifying repository: 'globalintl'
📡 Querying: https://gitcode.com/org/openharmony/globalintl
❌ NOT FOUND - Repository does not exist on GitCode

⚠️  Repository Verification Failed!
   The repository 'globalintl' was not found on:
   https://gitcode.com/org/openharmony/repos

📋 Suggested Repository Names:
   1. global_i18n (most likely for @ohos.intl module)
   2. globalization
   3. i18n

💡 Tip: You can manually verify at:
   https://gitcode.com/org/openharmony/repos

📋 Please provide the correct repository name:
   Your input: [Type repository name or press Ctrl+C to cancel]
```

### Step 3.2: Perform Sync

After repository verification is successful, proceed with the sync:

```bash
# Add to manifest (if missing)
# Edit .repo/manifests/openharmony-master.xml
<project path="{local_storage_path}"
          name="{verified_repository_name}"
          remote="openharmony"
          revision="master" />

# Sync the repository
repo sync {local_storage_path}
```

## Output Example (Successful Sync)

```
🔍 Phase 2: Code Existence Check & Sync

📋 Information Needed:
1️⃣ OHOS Repository Name
   ⚠️ Will be verified at: https://gitcode.com/org/openharmony/repos
   e.g.: distributeddatamgr_preferences
   Your input: distributeddatamgr_preferences

2️⃣ Local Storage Path (optional, press Enter to skip)
   e.g.: foundation/distributeddatamgr/preferences
   Your input: [Enter]  ← Using default: foundation/distributeddatamgr/preferences

📋 Step 1: Check Manifest (.repo/manifests/openharmony-master.xml)
❌ NOT FOUND - Module 'distributeddatamgr_preferences' not in manifest

📋 Step 2: Check Plugins Directory
❌ NOT FOUND - Plugin directory does not exist: plugins/data/preferences/

📋 Step 3: Verify Repository & Sync
🔍 Verifying repository: 'distributeddatamgr_preferences'
📡 Querying: https://gitcode.com/org/openharmony/distributeddatamgr_preferences
✅ VERIFIED - Repository exists on GitCode

📋 Step 3.2: Sync Module
⚠️  Action Required:
   1. Adding to manifest...
   2. Running repo sync...
   3. Creating plugin structure...

✅ Sync complete: foundation/distributeddatamgr/preferences/
   Total files synced: 81
   Proceeding to Phase 3...
```

## Best Practices

1. **Always Verify**: Never skip repository verification
2. **Interactive Correction**: Allow user to correct repository name if verification fails
3. **Suggest Alternatives**: Provide likely repository name suggestions
4. **Lazy Sync**: Only sync when absolutely necessary
5. **Clear Progress**: Show detailed progress during sync operation

## Common Issues

### Issue: Repository Not Found

**Symptoms**: Verification fails with 404 error

**Solutions**:
1. Check spelling of repository name
2. Browse https://gitcode.com/org/openharmony/repos manually
3. Try common naming patterns:
   - `{subsystem}_{module}`
   - `{module}`
   - `{category}_{subsystem}_{module}`

### Issue: Sync Fails

**Symptoms**: `repo sync` command fails

**Solutions**:
1. Check network connectivity
2. Verify remote URL in manifest
3. Try `repo sync --force-sync` to override local changes
4. Check available disk space

## Related Files

- **Phase 1**: [INFORMATION_COLLECTION.md](phase1-information-collection.md) - Initial info collection
- **Phase 3**: [API_ANALYSIS.md](phase3-api-analysis.md) - Next phase after sync
