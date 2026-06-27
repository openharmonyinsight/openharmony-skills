# Phase 2: OHOS Source Code Acquisition

## Overview

Obtain the OHOS module's source code for architecture analysis. **This step is always mandatory** — even if the final adaptation strategy doesn't reuse OHOS code, you must understand the original implementation before making any architectural decisions.

## Decision Tree

```
┌─ Step 1: Check openharmony.xml ─────────────────────────────┐
│                                                               │
│  grep -i "{keyword}" .repo/manifests/openharmony.xml         │
│                                                               │
│  Found?                                                       │
│    ├─ YES → Source already synced at {path}, analyze directly │
│    └─ NO  → Go to Step 2                                     │
└───────────────────────────────────────────────────────────────┘

┌─ Step 2: Ask Developer for Repository Info ──────────────────┐
│                                                               │
│  Developer provides:                                          │
│    1. GitCode repo name (e.g., "startup_init")               │
│    2. Local path (e.g., "base/startup/init")                 │
│    3. Revision (e.g., "weekly_20260525" or "master")         │
│                                                               │
│  If developer doesn't know → browse:                          │
│    https://gitcode.com/org/openharmony/repos                  │
│  OR try common naming patterns:                               │
│    {subsystem}_{module} / {category}_{subsystem}_{module}     │
└───────────────────────────────────────────────────────────────┘

┌─ Step 3: Configure & Sync ──────────────────────────────────┐
│                                                               │
│  1. Add entry to .repo/manifests/openharmony.xml              │
│  2. repo sync {local_path}                                    │
│  3. Verify source code exists at {path}                       │
└───────────────────────────────────────────────────────────────┘
```

## Step 1: Check openharmony.xml

The ArkUI-X SDK project uses `openharmony.xml` to manage OHOS source dependencies. Check if the module's repo is already configured:

```bash
# Search by module keyword (try multiple terms)
grep -i "preferences" .repo/manifests/openharmony.xml
grep -i "settings" .repo/manifests/openharmony.xml
grep -i "deviceinfo\|device_info\|startup_init" .repo/manifests/openharmony.xml
```

**manifest.xml format**:
```xml
<project path="foundation/distributeddatamgr/preferences"
         name="distributeddatamgr_preferences"
         remote="openharmony"
         revision="weekly_20260525" />
```

**Key fields**:
- `path` — local directory where source will be synced to
- `name` — repository name at `https://gitcode.com/openharmony/{name}`
- `remote` — always `"openharmony"` for OHOS repos
- `revision` — branch/tag to sync (e.g., `"weekly_20260525"`, `"master"`)

**If found**: Source code is at the mapped `path`. Proceed to Phase 4 architecture analysis on that code.

**If NOT found**: Proceed to Step 2.

## Step 2: Ask Developer for Repository Info

When the OHOS repository is not in `openharmony.xml`, the developer must provide:

**Required info**:
1. **Repository name** on GitCode (e.g., `startup_init`)
2. **Local path** where it should be placed (e.g., `base/startup/init`)
3. **Revision** (branch name, e.g., `weekly_20260525`)

**How developer can find the repo**:
- Browse: https://gitcode.com/org/openharmony/repos
- Search by module name (e.g., search "deviceinfo" or "settings")
- Common naming patterns:
  - `{subsystem}_{module}` — e.g., `distributeddatamgr_preferences`
  - `{category}_{subsystem}_{module}` — e.g., `ability_ability_runtime`
  - `{module}` — e.g., `build`

**Example dialogue**:
```
📋 OHOS Source Code Required

The module '@ohos.settings' is not in the current manifest.
To analyze its OHOS implementation, I need the repository info.

🔍 Please provide:
  1️⃣ GitCode repository name
     Browse: https://gitcode.com/org/openharmony/repos
     Common patterns: {subsystem}_settings, settings
     Your input: ________

  2️⃣ Local path (where to sync)
     e.g.: base/customization/settings
     Your input: ________

  3️⃣ Revision (branch)
     e.g.: weekly_20260525, master
     Your input: ________
```

## Step 3: Configure & Sync

After developer provides repository info:

### 3.1 Add to openharmony.xml

```bash
# Edit .repo/manifests/openharmony.xml
# Add entry before closing </manifest> tag:
```

```xml
<project path="{local_path}"
         name="{repo_name}"
         remote="openharmony"
         revision="{revision}" />
```

**Example**:
```xml
<project path="base/startup/init"
         name="startup_init"
         remote="openharmony"
         revision="weekly_20260525" />
```

### 3.2 Sync the Repository

```bash
repo sync {local_path}
```

### 3.3 Verify

```bash
ls -la {local_path}/
# Should show OHOS module source code
```

## Relationship Between OHOS Source and plugins/

```
OHOS Source (openharmony.xml)          plugins/ (ArkUI-X repo)
┌──────────────────────────────┐       ┌──────────────────────────────┐
│ Original OHOS implementation │       │ Cross-platform adaptation    │
│ foundation/.../preferences/  │──────►│ plugins/data/preferences/    │
│                              │       │                              │
│ Used for:                    │       │ Used for:                    │
│ • Architecture analysis      │       │ • Build & packaging          │
│ • Understanding impl details │       │ • Platform adapters          │
│ • Code reuse (OHOS Reuse)   │       │ • NAPI bindings              │
└──────────────────────────────┘       └──────────────────────────────┘
```

- `openharmony.xml` repos → **OHOS original code** for analysis and potential reuse
- `plugins/` → **ArkUI-X adaptation layer** (always in the `plugins` repo, synced via `default.xml`)
- These are separate repositories with different remotes:
  - OHOS repos: `remote="openharmony"` → `gitcode.com/openharmony/`
  - plugins repo: `remote="origin"` → `gitcode.com/arkui-x/` (or similar)

## Common Issues

### Issue: repo sync hangs or fails

**Solutions**:
1. Check network connectivity to `gitcode.com`
2. Try `repo sync --force-sync {local_path}`
3. Verify repository name matches exactly on `https://gitcode.com/openharmony/{name}`

### Issue: Developer doesn't know the repository name

**Solutions**:
1. Browse `https://gitcode.com/org/openharmony/repos` and search
2. Check if the d.ts file contains hints (some have `@syscap` annotations referencing subsystem paths)
3. Search GitHub mirror: `https://github.com/openharmony/{guessed_name}`

### Issue: Repository exists but revision not found

**Solutions**:
1. Check available branches: `git ls-remote --heads https://gitcode.com/openharmony/{repo}.git`
2. Use `master` as fallback if weekly branch doesn't exist
3. Match the revision used by other repos in the same `openharmony.xml` file

## Related Files

- **Phase 1**: [phase1-information-collection.md](phase1-information-collection.md) - Module info collection
- **Phase 3**: [phase3-api-analysis.md](phase3-api-analysis.md) - API analysis (next phase)
- **Phase 4**: [phase4-architecture-analysis.md](phase4-architecture-analysis.md) - Architecture analysis of synced code
