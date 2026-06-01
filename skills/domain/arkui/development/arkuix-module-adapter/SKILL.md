---
name: arkuix-module-adapter
description: >
  Guide OHOS modules cross-platform adaptation with automated architecture analysis, code sync, and configuration generation. Use for adapting OHOS subsystem modules (@ohos.data.preferences, @ohos.intl, @ohos.multimedia.image, etc.) to Android/iOS. Provides 6-phase workflow: info collection → code sync → API analysis → architecture analysis → recommendation → implementation. Includes automated scripts for DTS analysis, architecture analysis, and configuration generation.
  Do NOT use for: adapting existing C++ native modules to Android/iOS (use arkuix-cpp-adapter instead) or creating new Native plugins from scratch (use arkuix-native-dev instead).
  触发关键词："模块适配"、"跨平台适配"、"架构模式分析"、"DTS分析"、
  "module adaptation"、"architecture analysis"、"OHOS cross-platform".
---

# ArkUIX Module Adapter Skill

## 6-Phase Workflow

### Before Starting Adaptation, Ask Yourself

- **Module type**: Is this a data module (preferences, RDB) or platform-service module (bluetooth, camera)? This determines the architecture mode.
- **C/C++ purity**: Is the core logic pure C/C++ with no platform APIs? If yes → likely OHOS Reuse with zero platform code.
- **DTS coverage**: Does the .d.ts already have `@crossplatform` annotations? If yes → some work already done.
- **Reference implementation**: Is there an existing adapted module in `plugins/` you can reference?

### Phase 1: Information Collection

Collect module identification and locate source code.

**What to collect**:
- **Module name**: Full qualified name (e.g., `@ohos.data.preferences`)
- **Subsystem path**: OHOS source path (e.g., `foundation/distributeddatamgr/preferences`)
- **Repository name**: GitCode repo name (e.g., `distributeddatamgr_preferences`)

**Where to find it**:
- `.d.ts` file: `interface/sdk-js/api/@ohos.{module}.d.ts` — confirms module exists and lists APIs
- `.repo/manifests/openharmony-master.xml` — maps module name to source path
- GitCode: `https://gitcode.com/openharmony/{repo}` — verify repo exists

**Validation**: Module name must match between .d.ts filename, BUILD.gn targets, and plugin_lib.gni entries.

**MANDATORY — READ**: [references/phase1-information-collection.md](references/phase1-information-collection.md) — what to collect, from where, and validation rules.
**Do NOT load** other phase references yet — load them when reaching each phase.

**Output**: Module identification information

### Phase 2: Code Existence Check & Sync

Intelligently checks if OHOS code already exists before syncing. Avoids redundant operations.

**Decision Tree**:
1. Check `.repo/manifests/openharmony-master.xml`
2. Check `plugins/` directory
3. Only sync if both checks fail (with repository verification on GitCode)

**Output**: Sync status or repository verification results

### Phase 3: API Interface Analysis

Analyzes `.d.ts` file to determine `@crossplatform` coverage.

**Metrics**:
- Total interface count (by category)
- Adapted vs needs adaptation counts
- Coverage percentage
- Detailed list of interfaces needing adaptation

**Output**: Comprehensive API statistics with coverage progress bar

**Automation**: `scripts/dts_analyzer.py interface/sdk-js/api/@ohos.{module}.d.ts`

**MANDATORY — READ**: [references/phase3-api-analysis.md](references/phase3-api-analysis.md) — detailed DTS analysis workflow and coverage interpretation.
**Do NOT load** phase4 or phase5 references yet.

### Phase 4: Architecture Analysis

Analyzes OHOS module code composition and platform dependencies.

**Analysis Dimensions**:
- Code volume statistics (NAPI, business logic, platform-specific)
- Platform dependency ratio
- Internal and external dependencies
- **Platform implementation necessity** (C/C++ native vs platform-specific code)
- Architecture diagrams (module structure, dependencies, call flow)

**Key Rule**: C/C++ Cross-Platform Native Support
- Analyzes whether module actually requires Android/iOS platform code
- Many data modules (preferences, RDB, crypto) are pure C/C++ and require zero platform-specific implementation
- Only path/configuration differences needed (~50 lines per platform)

**Output**: Detailed code composition and dependency analysis

**Automation**: `scripts/architecture_analyzer.py foundation/{module_path}`

**MANDATORY — READ**: [references/phase4-architecture-analysis.md](references/phase4-architecture-analysis.md) — complete analysis dimensions and C/C++ native assessment.
**MANDATORY — READ**: [references/architecture-modes.md](references/architecture-modes.md) — three architecture modes with detailed comparison.

### Phase 5: Architecture Recommendation

Recommends adaptation mode based on analysis: **OHOS Reuse** / **Independent** / **Hybrid**

**Decision Matrix**:

| Mode | Code Reuse | New Code | Time | Best For |
|------|------------|----------|------|----------|
| OHOS Reuse | 90-95% | 500-800 lines | 4-6 weeks | Data-focused (preferences, kv_store) |
| Hybrid | 60-80% | 1,500-2,500 lines | 6-10 weeks | Mixed (location, sensor) |
| Independent | 10-30% | 4,000-6,000 lines | 10-16 weeks | Platform-heavy (BLE, pasteboard) |

**Output**: Recommended mode with rationale and effort estimates

### Phase 6: Implementation Guidance

Generate production-ready code based on the chosen architecture mode.

**Pure virtual interface skeleton** (OHOS repo side — always needed):
```cpp
// interfaces/kits/napi/include/{module}_adapter.h
class {Module}Adapter {
public:
    virtual ~{Module}Adapter() = default;
    virtual int32_t Init() = 0;
    virtual int32_t Destroy() = 0;
    // Add methods from Phase 3 DTS analysis
};
```

**OHOS thin wrapper** (OHOS Reuse mode — 100% forwarding to existing code):
```cpp
// services/adapter/{module}_adapter_ohos.cpp
class {Module}AdapterOHOS : public {Module}Adapter {
public:
    int32_t Init() override { return OHOS::Init(); }  // Forward to existing implementation
    int32_t Destroy() override { return OHOS::Destroy(); }
};
```

**Implementation order**:
1. Define pure virtual interface (`{module}_adapter.h`)
2. Implement OHOS thin wrapper (`{module}_adapter_ohos.cpp`)
3. Implement Android JNI adapter (`{module}_adapter_android.cpp`)
4. Implement iOS ObjC++ adapter (`{module}_adapter_ios.mm`)
5. Update build configuration (GN templates)
6. Generate 4 mandatory configuration files
7. Write unit tests

**Automation**: `scripts/code_generator.py {module} {repo} --api-version {ver}`

**MANDATORY — READ**: [references/phase6-implementation-guide.md](references/phase6-implementation-guide.md) — complete implementation workflow.
**MANDATORY — READ**: [references/code-examples.md](references/code-examples.md) — production-ready code templates for all layers.
**Do NOT load** phase1-4 references — already completed.

**Output**: Production-ready code with comprehensive error handling

## NEVER Do

- **NEVER** skip Phase 4 architecture analysis before choosing a mode — wrong mode selection (e.g., Independent for a pure C/C++ data module) wastes weeks of work
- **NEVER** choose Independent mode for pure C/C++ modules (preferences, kv_store, RDB, crypto) — they need zero platform-specific code, only ~50 lines of path/config differences per platform
- **NEVER** forget to update all 4 mandatory configuration files — missing any one causes silent build failures: `plugin_lib.gni`, `apiConfig.json`, `arkui_cross_sdk_description_std.json`, `@ohos.{module}.d.ts`
- **NEVER** start Phase 6 implementation without completing Phase 3 DTS analysis — you won't know which interfaces need adaptation
- **NEVER** hardcode module paths — use the naming patterns from config.json (`{subsystem}_{module}` or `{module}`)
- **NEVER** skip `--dry-run` when running code_generator.py — always preview changes before applying
- **NEVER** assume a module fits only one architecture mode — hybrid modules (geolocation, sensor) have mixed characteristics requiring careful Phase 4 analysis
- **NEVER** sync OHOS code without verifying the repository exists on GitCode first — `https://gitcode.com/openharmony/{repo}`

## Key Features

### 🤖 Automated Scripts

All scripts are in `scripts/` directory:

```bash
# Analyze .d.ts coverage
python3 scripts/dts_analyzer.py interface/sdk-js/api/@ohos.data.preferences.d.ts

# Analyze module architecture
python3 scripts/architecture_analyzer.py foundation/distributeddatamgr/preferences

# Generate configuration files (dry-run)
python3 scripts/code_generator.py data/preferences distributeddatamgr_preferences --api-version 23 --dry-run

# Apply changes
python3 scripts/code_generator.py data/preferences distributeddatamgr_preferences --api-version 23
```

### 🎯 Three Architecture Modes

#### OHOS Reuse Mode (90-95% reuse)

For data-focused modules with minimal platform dependencies.

**Characteristics**:
- Platform-independent business logic >90%
- Thin platform adapters (JNI/ObjC++)
- Zero OHOS runtime overhead
- **C/C++ Native modules may require zero platform code** (up to 100% reuse)

**Example Modules**: preferences, kv_store, http

#### Independent Implementation Mode (10-30% reuse)

For modules with heavy platform API dependencies.

**Characteristics**:
- Platform-specific code >70%
- Native framework integration
- Each platform has own implementation

**Example Modules**: bluetooth, pasteboard, camera

#### Hybrid Mode (60-80% reuse)

For mixed data/platform logic modules.

**Characteristics**:
- Extract common data structures
- Service abstraction layer
- Shared business logic

**Example Modules**: geolocation, sensor, request

## Implementation Checklist

Use this checklist to track adaptation progress:

### Phase 1: Information Collection
- [ ] Module name collected
- [ ] Repository name verified (if needed)

### Phase 2: Code Sync
- [ ] Repository verified on GitCode
- [ ] Code synced (if needed)
- [ ] Plugin structure created (if needed)

### Phase 3: API Analysis
- [ ] .d.ts file analyzed
- [ ] Coverage percentage calculated
- [ ] Interfaces needing adaptation listed

### Phase 4: Architecture Analysis
- [ ] Code volume statistics collected
- [ ] Platform dependency ratio calculated
- [ ] Dependencies identified
- [ ] **Platform implementation necessity analyzed** (C/C++ native vs platform-specific)

### Phase 5: Architecture Recommendation
- [ ] Architecture mode selected
- [ ] Developer confirms choice

### Phase 6: Implementation
- [ ] Pure virtual interface defined (OHOS repo)
- [ ] OHOS thin wrapper implemented (OHOS repo)
- [ ] Android adapter implemented (Plugin repo)
- [ ] iOS adapter implemented (Plugin repo)
- [ ] Build configuration updated
- [ ] Configuration files generated (4 files)
- [ ] Unit tests written
- [ ] Compilation successful (all platforms)
- [ ] Tests passing

## Mandatory Configuration Files

After code generation, ensure all 4 files are updated:

- [ ] `plugins/plugin_lib.gni` - Module entry
- [ ] `interface/sdk/plugins/api/apiConfig.json` - Library configuration
- [ ] `build_plugins/sdk/arkui_cross_sdk_description_std.json` - Build entries
- [ ] `interface/sdk-js/api/@ohos.{module}.d.ts` - @crossplatform annotations

## Troubleshooting

**Repository not found on GitCode?**
- Browse https://gitcode.com/org/openharmony/repos manually
- Try naming pattern: `{subsystem}_{module}` or `{module}`

**Validation failed?**
- Check all 4 mandatory files exist
- Verify module name format (use forward slashes)
- Ensure .d.ts file path is correct

**Build errors?**
- Check GN configuration syntax
- Verify dependency declarations
- Check for missing includes

## Related Skills

- **arkuix-api-adapter** - For adapting individual API methods within a module
