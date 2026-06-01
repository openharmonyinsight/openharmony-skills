# Phase 4: Architecture Analysis

## Overview

This phase performs comprehensive code architecture analysis to understand module composition, dependencies, and platform dependencies. The analysis informs the architecture pattern recommendation in Phase 5.

## Analysis Dimensions

### 1. Code Volume Statistics

Analyze the size and complexity of the OHOS implementation:

- **NAPI Bindings**: Lines of JavaScript ↔ C++ bridge code
- **Business Logic**: Lines of C/C++ business logic
- **Platform-Specific**: Lines of platform-dependent code
- **Total Lines**: Overall code volume

**Example Output**:
```
📊 Code Composition
   - NAPI bindings: 2,400 lines
   - Business logic (C++): 9,800 lines
   - Platform-specific: 800 lines
   - Total: 13,000 lines
```

### 2. Platform Dependency Analysis

Calculate platform independence ratio:

- **Platform-Independent**: Code that can run on any platform
- **Platform-Specific**: Code tied to OHOS system APIs

**Example Output**:
```
🎯 Platform Dependency
   - Platform-independent: 92.5%
   - Platform-specific: 7.5%
```

**Calculation**:
```
Platform Independence % = (Business Logic - Platform-Specific) / Total × 100
```

### 3. Dependency Identification

Identify external dependencies:

**Internal Dependencies** (within OHOS):
- Common libraries (c_utils, hilog, etc.)
- Framework modules (safwk, IPC, etc.)

**External Dependencies**:
- Third-party libraries (sqlite, icu, libxml2, etc.)
- System frameworks (Android/iOS equivalents)

**Example Output**:
```
📦 Dependencies
Internal:
   - commonlibrary/c_utils: Utils and helpers
   - base/hiviewdfx/hilog: Logging framework
   - foundation/systemabilitymgr/safwk: System ability manager

External:
   - third_party/sqlite: Database engine
   - third_party/icu: Unicode support
   - third_party/libxml2: XML parsing
```

### 4. Detailed Architecture Diagrams

Generate visual representations of:

#### A. Module Architecture Diagram

Shows current OHOS implementation structure with file locations and key functions.

**Example**:
```
@ohos.data.preferences
├── ArkTS API Layer (.d.ts)
│   └── class Preferences
│
├── NAPI Binding Layer
│   └── napi_preferences.cpp:243 - PreferencesProxy::Put()
│       ├── ParseKey() - Validate key parameter
│       ├── ParseDefValue() - Parse value based on type
│       ├── GetSelfInstance() - Get Preferences instance
│       └── AsyncCall::Call() - Execute asynchronously
│
├── Business Logic Layer
│   └── PreferencesImpl class
│       ├── Get(key, defValue) - Retrieve value from cache/disk
│       ├── Put(key, value) - Update cache and queue disk write
│       ├── Delete(key) - Remove from cache and queue disk write
│       └── Flush() - Async write to disk
│
└── Platform-Specific Layer (OHOS only)
    ├── preferences_file_operation.cpp - XML file I/O
    └── DataObsMgrClient - Cross-process notifications
```

#### B. Module Dependency Relationships

Shows how different components within the module depend on each other.

**Example**:
```
napi_preferences.cpp
    │
    ├──► preferences.h (Preferences interface)
    │
    ├──► preferences_helper.h (Factory)
    │      │
    │      └──► preferences_impl.h (Implementation)
    │             │
    │             ├──► preferences_value.h (Type-erased value)
    │             ├──► preferences_observer.h (Observer interface)
    │             └──► preferences_file_operation.h (XML I/O)
    │
    └──► napi/native_api.h (N-API bindings)
```

#### C. Interface Implementation Flowchart

Shows complete call flow from ArkTS API to platform implementation.

**Example**:
```
User: preferences.put('key', 'value')
    │
    ▼
┌─────────────────────────────────┐
│ 1. ArkTS Layer                 │
│    @ohos.data.preferences.d.ts  │
│    Preferences.put()            │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│ 2. NAPI Binding Layer          │
│    napi_preferences.cpp:243    │
│    ParseKey()                  │
│    ParseDefValue()             │
│    AsyncCall::Call()           │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│ 3. Business Logic Layer        │
│    preferences_impl.cpp:252    │
│    Update cache                │
│    Queue disk write            │
└─────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────┐
│ 4. Platform-Specific Layer     │
│    XML file I/O                │
└─────────────────────────────────┘
```

## Analysis Methods

### Automated Analysis (Recommended)

Use bundled script for comprehensive analysis:

```bash
python3 scripts/architecture_analyzer.py \
  preferences \
  foundation/distributeddatamgr/preferences
```

**Output**:
- Code volume statistics
- Platform dependency ratio
- Dependency tree
- Architecture diagrams (ASCII)

### Manual Analysis (Fallback)

**1. Count Lines**:
```bash
# NAPI bindings
find . -name "*napi*.cpp" -o -name "*napi*.h" | xargs wc -l

# Business logic
find . -name "*impl*.cpp" -o -name "*impl*.h" | xargs wc -l

# Platform-specific
find . -path "*/services/adapter/*" | xargs wc -l
```

**2. Find Dependencies**:
```bash
# Include dependencies
grep -r "^#include" . --include="*.cpp" --include="*.h" | \
  sed 's/.*#include [*<"]\([^>"<]*\)[>"].*/\1/' | sort -u

# GN dependencies
grep -r "deps\|external_deps" BUILD.gn
```

**3. Identify Platform APIs**:
```bash
# OHOS-specific APIs
grep -r "OHOS::" . --include="*.cpp" | grep -v "OHOS::Ace"

# System calls
grep -r "OpenHarmony\|hilog\|safwk" . --include="*.cpp"
```

## Platform Implementation Necessity Analysis

### Key Rule: C/C++ Cross-Platform Native Support

Before recommending platform-specific implementations, analyze whether the module actually requires Android/iOS platform code.

**Analysis Criteria**:

```
Is Platform Implementation Required?
├─ Does the module call platform-specific APIs?
│  ├─ NO → C/C++ implementation is sufficient (cross-platform native)
│  └─ YES → Platform implementation required
│     ├─ Android: JNI + Java/Kotlin
│     └─ iOS: ObjC++ + Objective-C/Swift
```

**Checklist**:

1. **File System Operations**: Uses standard C/C++ file I/O?
   - `std::fstream`, ` fopen`, `fwrite` → **No platform code needed**
   - Only path conversion required (Android: `/data/data/`, iOS: `NSHomeDirectory()`)

2. **Data Serialization**: Uses standard data formats?
   - JSON (third_party/json), XML (libxml2), SQLite → **No platform code needed**
   - Pure C/C++ parsing/serialization

3. **Memory Operations**: Uses standard memory management?
   - `std::map`, `std::vector`, `std::string` → **No platform code needed**
   - Standard C++ containers

4. **Network Operations**: Uses cross-platform libraries?
   - cURL, OpenSSL → **Minimal platform code** (mostly for certificates)
   - Raw sockets → **Platform code required**

5. **System Services**: Calls OS-specific services?
   - Notifications, Bluetooth, Camera → **Platform code required**

**Common C/C++ Native Modules**:

| Module Type | Platform Code Needed? | Reason |
|------------|----------------------|--------|
| Preferences/KV Store | ❌ No | File I/O + XML/JSON parsing |
| Database (RDB) | ❌ No | SQLite is cross-platform |
| Data Storage | ❌ No | Standard file operations |
| Crypto Operations | ❌ No | OpenSSL is cross-platform |
| Image Decoding | ❌ No | Skia/libpng is cross-platform |
| HTTP (cURL-based) | ⚠️ Minimal | Only for certificate paths |
| File System | ⚠️ Minimal | Path conversion only |
| Network (raw sockets) | ✅ Yes | Platform-specific APIs |
| Bluetooth | ✅ Yes | Platform frameworks required |
| Sensor | ✅ Yes | Platform frameworks required |
| Camera | ✅ Yes | Platform frameworks required |
| Notifications | ✅ Yes | Platform frameworks required |

**Examples**:

#### Example 1: Preferences (No Platform Code)

```cpp
// ✅ Pure C/C++ implementation - cross-platform native
class Preferences {
    bool Put(const std::string& key, const std::string& value) {
        cache_[key] = value;                    // std::map - portable
        return WriteToFile();                   // std::fstream - portable
    }

    bool WriteToFile() {
        std::ofstream file(path_);              // Standard C++ I/O
        file << SerializeToXML();               // libxml2 - portable
        return file.good();
    }
};
// Only path initialization needs platform-specific code:
// Android: "/data/data/{package}/files/"
// iOS: [NSSearchPathForDirectoriesInDomains(...) objectAtIndex:0]
```

#### Example 2: Bluetooth (Platform Code Required)

```cpp
// ❌ Requires platform-specific implementation
class BluetoothManager {
    void ScanDevices() {
        #ifdef ANDROID
            // Call Android BluetoothManager via JNI
            jni_call_android_bluetooth_scan();
        #elif defined(IOS)
            // Call iOS CoreBluetooth framework
            [coreBluetoothManager scanForPeripherals];
        #endif
    }
};
```

**Decision Flow**:

```
START: Analyze module for platform dependencies
   ↓
Review source code for:
   - Platform-specific API calls (OHOS::, Android::, iOS::*)
   - System service dependencies (safwk, bundlemgr)
   - Hardware-specific operations (Bluetooth LE, Camera, Sensor)
   ↓
Found ANY platform-specific dependencies?
   ↓
   NO → Use C/C++ Native Mode
          - No Android/iOS platform code
          - Only path/config differences
          - 95-100% code reuse
   ↓
   YES → Proceed to Platform Dependency Classification
```

**Output Format**:

```
🎯 Platform Implementation Analysis
   ✅ C/C++ Native Support: YES
   └─ Reason: Pure data operations with standard C/C++ libraries
   └─ Platform Code: Not needed (except path initialization)

   OR

   ⚠️  Platform Implementation Required: YES
   ├─ Android: JNI adapter needed (~500 lines)
   ├─ iOS: ObjC++ adapter needed (~500 lines)
   └─ Reason: Depends on platform-specific services (Bluetooth/Camera/Sensor)
```

## Platform Dependency Classification

### High Platform Independence (>90%)

**Characteristics**:
- Mostly data processing algorithms
- Standard C/C++ libraries
- Minimal system API usage
- **May not require platform-specific code at all**

**Examples**:
- Database engines (SQLite)
- Data serialization (XML/JSON)
- Cryptographic operations (OpenSSL)
- Key-Value storage (file-based)
- Image decoding (Skia/libpng)

**Recommended**: OHOS Reuse Mode with C/C++ Native Implementation

**When C/C++ Native is sufficient**:
- Module only uses standard C/C++ libraries
- Data processing is platform-agnostic
- File I/O uses standard paths or minor path conversion
- No hardware/system service integration

### Medium Platform Independence (50-90%)

**Characteristics**:
- Mix of data processing and platform APIs
- Some system service interactions
- Partial abstraction possible

**Examples**:
- HTTP clients
- File system operations
- Sensor data processing

**Recommended**: Hybrid Mode

### Low Platform Independence (<50%)

**Characteristics**:
- Heavy platform API usage
- Native framework integration
- System service dependencies

**Examples**:
- Bluetooth Low Energy
- Camera/AVCapture
- Input Method Editor

**Recommended**: Independent Implementation Mode

## Best Practices

1. **Start Automated**: Always use script first for comprehensive analysis
2. **Verify Manually**: Spot-check automated results for accuracy
3. **Document Diagrams**: Visual representations aid understanding
4. **Track Dependencies**: Both internal and external
5. **Measure Accurately**: Use actual line counts, not estimates

## Common Issues

### Issue: Incomplete Dependency Detection

**Symptoms**: Missing dependencies in analysis

**Solutions**:
1. Check both source and build files
2. Look for conditional compilation (#ifdef)
3. Check for runtime dynamic loading
4. Verify transitive dependencies

### Issue: Platform Misclassification

**Symptoms**: Code incorrectly classified as platform-specific

**Solutions**:
1. Check if abstraction layer exists
2. Look for portable alternatives
3. Verify actual OHOS-specific API usage
4. Consider refactoring potential

## Related Files

- **Phase 3**: [API_ANALYSIS.md](phase3-api-analysis.md) - Previous phase (API analysis)
- **Phase 5**: [ARCHITECTURE_RECOMMENDATION.md](phase5-architecture-recommendation.md) - Next phase (recommendation)
- **Reference**: [ARCHITECTURE_MODES.md](architecture-modes.md) - Architecture pattern details
- **Script**: `scripts/architecture_analyzer.py` - Automated analysis tool
