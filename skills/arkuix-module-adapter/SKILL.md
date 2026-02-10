---
name: ArkUIX Module Adapter
description: Guide OHOS modules cross-platform adaptation with automated architecture analysis, code sync, and configuration generation. Use for adapting OHOS subsystem modules (@ohos.data.preferences, @ohos.intl, @ohos.multimedia.image, etc.) to Android/iOS. Provides 6-phase workflow: info collection → code sync → API analysis → architecture analysis → recommendation → implementation. Includes automated scripts for DTS analysis, architecture analysis, and configuration generation.
---

# ArkUIX Module Adapter Skill

## Overview

Guide OHOS modules through cross-platform adaptation with automated analysis and code generation. This skill transforms Claude into a specialized adaptation assistant with domain expertise in OHOS/ArkUI-X architecture.

## Quick Start

```
User: "I need to adapt @ohos.data.preferences module"
```

The skill automatically guides through all 6 phases of adaptation.

## 6-Phase Workflow

### Phase 1: Information Collection

Collects minimal information upfront (module name), then lazily collects additional details (repository name, storage path) only when needed.

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

Provides actual implementation code with complete examples for:
- Pure virtual interface (OHOS repo)
- OHOS thin wrapper (100% forwarding)
- Android JNI adapter (complete with error handling)
- iOS Objective-C++ adapter (complete with @try-@catch)
- Build configuration (GN templates)
- Unit tests

**Output**: Production-ready code with comprehensive error handling

**Automation**: `scripts/code_generator.py {module} {repo} --api-version {ver}`

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

### 📚 Progressive Disclosure

Core workflow in SKILL.md (this file), detailed content in references:

- **Phase Details**: `references/phase{1-6}*.md`
- **Architecture Modes**: `references/architecture-modes.md`
- **Code Examples**: `references/code-examples.md`
- **Templates**: `assets/templates/` (code templates for reuse)

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

## Tips

1. **Start Small**: Try with a simple module first (e.g., preferences)
2. **Use Dry-Run**: Always use `--dry-run` flag before applying changes
3. **Verify Repository**: Always verify repository exists before syncing
4. **Read References**: Consult detailed references for complex phases
5. **Run Tests**: Always run tests after implementation
