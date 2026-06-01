# Phase 3: API Interface Analysis

## Overview

This phase analyzes the .d.ts TypeScript definition file to identify all interfaces that need adaptation and track @crossplatform coverage progress.

## Analysis Process

### Step 1: Locate .d.ts File

**Path Pattern**: `interface/sdk-js/api/@ohos.{module_name}.d.ts`

**Examples**:
- `interface/sdk-js/api/@ohos.data.preferences.d.ts`
- `interface/sdk-js/api/@ohos.intl.d.ts`
- `interface/sdk-js/api/@ohos.multimedia.image.d.ts`

### Step 2: Scan All Interfaces

The analyzer scans for:

- **Namespaces**: Top-level module namespaces
- **Classes**: Class definitions with methods and properties
- **Interfaces**: TypeScript interface definitions
- **Functions**: Standalone functions
- **Methods**: Class/interface methods
- **Properties**: Class/interface properties
- **Constants**: Const declarations
- **Types**: Type aliases and enums

### Step 3: Check @crossplatform Annotations

For each interface found, check for the `@crossplatform` annotation:

```
✅ Has @crossplatform: Already adapted
❌ Missing @crossplatform: Needs adaptation
```

**Annotation Format**:
```typescript
/**
 * @since 9
 * @syscap SystemCapability.ArkUI.ArkUI.Full
 * @crossplatform <- This indicates cross-platform support
 */
export class Preferences {
  put(key: string, value: PreferencesValue): Promise<void>;
}
```

### Step 4: Generate Adaptation Summary

Produce comprehensive statistics:

- Total interface count (by category)
- Already adapted count (with @crossplatform)
- Needs adaptation count (without @crossplatform)
- Adaptation progress percentage
- Detailed list of interfaces needing adaptation

## Output Example

```
📋 API Interface Analysis: @ohos.data.preferences

📊 Interface Statistics:
   Total interfaces:        47
   Namespaces:              1
   Classes:                 3
   Interfaces:              2
   Functions:               8
   Methods:                 25
   Properties:              5
   Constants:               3

✅ Adaptation Status:
   Already adapted (@crossplatform):    42 (89.4%)
   Needs adaptation (no @crossplatform): 5 (10.6%)

📋 Interfaces Needing Adaptation:
   ❌ Preferences.put(key: string, value: ValueType, callback: AsyncCallback<void>)
      Sets an int value for the key in the Preferences object
      - Line 145

   ❌ Preferences.get(key: string, defValue: ValueType, callback: AsyncCallback<ValueType>): void;
      Obtains the value of a preferences in the ValueType format.
      - Line 156

   ❌ Preferences.delete(key: string, callback: AsyncCallback<void>): void
      Deletes the preferences with a specified key from the Preferences object
      - Line 167

   ❌ Preferences.clear(callback: AsyncCallback<void>): void;
      Clears all preferences from the Preferences object
      - Line 178

📈 Adaptation Progress: ████████████████████░░ 89.4%

⚠️  Recommendation:
   Focus on the 5 remaining interfaces to complete 100% adaptation.
   Priority: HIGH - These are core data operations.
```

## Analysis Script Usage

**Automated Analysis** (using bundled script):

```bash
python3 scripts/dts_analyzer.py interface/sdk-js/api/@ohos.data.preferences.d.ts
```

**Manual Analysis** (grep-based):

```bash
# Find all interfaces without @crossplatform
grep -B 5 "export\|class\|interface\|function" \
  interface/sdk-js/api/@ohos.data.preferences.d.ts | \
  grep -v "@crossplatform" | \
  grep "export\|class\|interface"
```

## Output Metrics

### Primary Metrics

1. **Total Interface Count**: All discoverable interfaces
2. **Coverage Percentage**: `(with @crossplatform / total) × 100`
3. **Remaining Work**: Count of interfaces needing adaptation

### Secondary Metrics

1. **By Category**: Breakdown by type (class, function, method, etc.)
2. **By Complexity**: Estimated implementation effort
3. **By Priority**: Core vs peripheral APIs

## Decision Support

Based on analysis results:

**High Coverage (>80%)**:
- Consider incremental adaptation
- Focus on missing high-value APIs
- Quick win scenario

**Low Coverage (<50%)**:
- Consider full module adaptation
- Architecture analysis needed
- May need different strategy

**Mixed Coverage**:
- Analyze which parts are adapted
- Determine if hybrid approach needed
- Consider separating sub-modules

## Best Practices

1. **Comprehensive Scanning**: Don't miss nested interfaces or inherited methods
2. **Line Number Tracking**: Helps locate code quickly
3. **Categorization**: Group by type for better analysis
4. **Progress Tracking**: Compare with previous analysis
5. **Context Collection**: Note related APIs that affect implementation

## Common Issues

### Issue: Interfaces Not Found

**Symptoms**: Analysis returns very low count

**Solutions**:
1. Verify .d.ts file path is correct
2. Check for different file name variants
3. Look for files in subdirectories
4. Check if using legacy .js format

### Issue: False @crossplatform Detection

**Symptoms**: Interfaces marked as adapted but not actually implemented

**Solutions**:
1. Verify actual implementation exists
2. Check for placeholder annotations
3. Confirm platform-specific code exists
4. Test actual functionality

## Related Files

- **Phase 2**: [CODE_SYNC.md](phase2-code-sync.md) - Previous phase (code sync)
- **Phase 4**: [ARCHITECTURE_ANALYSIS.md](phase4-architecture-analysis.md) - Next phase (architecture analysis)
- **Script**: `scripts/dts_analyzer.py` - Automated analysis tool
