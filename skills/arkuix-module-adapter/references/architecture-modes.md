# Architecture Modes

This document provides detailed explanations of the three architecture patterns used in OHOS module adaptation.

## Mode 1: OHOS Reuse Mode

### Overview

Maximize code reuse by adapting the existing OHOS implementation with minimal platform-specific adapters.

### Characteristics

- **Code Reuse**: 90-95%
- **New Code**: 500-800 lines
- **Time**: 4-6 weeks
- **Maintenance**: Low (most code shared)
- **Risk**: Low (proven OHOS implementation)

### Architecture Diagram

```
┌────────────────────────────────────────────────────────────────┐
│  ArkTS API Layer (.d.ts)                                     │
│  Same across all platforms                                     │
└────────────────────────────────────────────────────────────────┘
                           ↓
┌────────────────────────────────────────────────────────────────┐
│  NAPI Binding Layer (Shared)                                  │
│  Same code across all platforms                                │
└────────────────────────────────────────────────────────────────┘
                           ↓
┌────────────────────────────────────────────────────────────────┐
│  Business Logic Layer (95% Shared)                           │
│  C++ implementation from OHOS                                  │
└────────────────────────────────────────────────────────────────┘
                           ↓
┌────────────────────────────────────────────────────────────────┐
│  Platform Interface (Pure Virtual)                            │
│  Abstracts platform-specific operations                        │
└────────────────────────────────────────────────────────────────┘
                           ↓
            ┌──────────────┬──────────────┬──────────────┐
            ↓              ↓              ↓              ↓
    ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
    │  OHOS    │   │ Android  │   │   iOS    │   │ Preview  │
    │ (100%    │   │ (JNI +   │   │ (ObjC++  │   │ (Curl/   │
    │ forward) │   │ Native   │   │ + Native │   │  Native) │
    └──────────┘   └──────────┘   └──────────┘   └──────────┘
```

### Implementation Steps

1. **Define Pure Virtual Interface** (OHOS repo)
   - File: `interfaces/adapter/include/{module}_adapter.h`
   - Abstract all platform-specific operations
   - Compile-time platform selection macros

2. **Create OHOS Thin Wrapper** (OHOS repo)
   - File: `services/adapter/{module}_adapter_ohos.cpp`
   - 100% forwarding to existing implementation
   - Zero additional logic

3. **Implement Android Adapter** (Plugin repo)
   - File: `plugins/{module}/adapter/android/{module}_adapter_android.cpp`
   - JNI calls to Android APIs
   - Thread-safe with mutex protection

4. **Implement iOS Adapter** (Plugin repo)
   - File: `plugins/{module}/adapter/ios/{module}_adapter_ios.mm`
   - Objective-C++ calls to iOS APIs
   - Exception handling with @try-@catch

5. **Update NAPI Layer** (OHOS repo)
   - Add `IS_ARKUI_X_TARGET` guards
   - Use helper macros for platform selection

### Example Modules

- `@ohos.data.preferences` - 95% reuse (XML I/O only platform-specific)
- `@ohos.data.kvStore` - 92% reuse (key-value operations independent)
- `@ohos.net.http` - 88% reuse (curl/netstack already cross-platform)

### C/C++ Native Implementation

**Special Case**: Some modules require **zero platform-specific code** due to pure C/C++ implementation:

**Characteristics**:
- 100% code reuse (no Android/iOS platform code)
- Only path/configuration differences
- Uses standard C/C++ libraries and cross-platform third-party libraries

**Examples**:
- **Preferences**: File I/O + XML parsing (libxml2) - fully portable
- **RDB Database**: SQLite engine - fully portable
- **Data Storage**: Standard file operations - fully portable
- **Crypto Operations**: OpenSSL - fully portable
- **Image Decoding**: Skia/libpng - fully portable

**Implementation**:
```
OHOS Implementation (C/C++) ──► Direct Reuse ──► Android/iOS
   - std::map, std::vector (portable)
   - std::fstream (portable)
   - libxml2 (portable)
   - SQLite (portable)

Only platform-specific code: Path initialization
   - Android: "/data/data/{package}/files/"
   - iOS: [NSSearchPathForDirectoriesInDomains(...) objectAtIndex:0]
   - (~50 lines per platform for paths only)
```

### Pros & Cons

**Pros**:
- ✅ Maximum code reuse (up to 100% for C/C++ native modules)
- ✅ Minimal maintenance burden
- ✅ Low risk
- ✅ Faster time-to-market
- ✅ **C/C++ native modules require zero platform code**

**Cons**:
- ❌ Requires OHOS code to be well-structured
- ❌ May need to refactor OHOS code
- ❌ Platform differences need abstraction (even if minimal)

---

## Mode 2: Independent Implementation Mode

### Overview

Implement platform-specific versions from scratch, reusing only the NAPI binding structure.

### Characteristics

- **Code Reuse**: 10-30%
- **New Code**: 4,000-6,000 lines
- **Time**: 10-16 weeks
- **Maintenance**: Medium (platform-specific code)
- **Risk**: Medium (new implementations)

### Architecture Diagram

```
┌────────────────────────────────────────────────────────────────┐
│  ArkTS API Layer (.d.ts)                                     │
│  Same across all platforms                                     │
└────────────────────────────────────────────────────────────────┘
                           ↓
┌────────────────────────────────────────────────────────────────┐
│  NAPI Binding Layer (Structure Reused)                       │
│  Same structure, different implementation                       │
└────────────────────────────────────────────────────────────────┘
                           ↓
            ┌──────────────┬──────────────┬──────────────┐
            ↓              ↓              ↓              ↓
    ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
    │ Android Impl    │ │   iOS Impl      │ │  OHOS Impl      │
    │ (JNI + Native)  │ │ (ObjC++ + Native)│ │ (Native APIs)   │
    │                 │ │                 │ │                 │
    │ Business Logic  │ │ Business Logic  │ │ Business Logic  │
    │ Platform Layer  │ │ Platform Layer  │ │ Platform Layer  │
    └─────────────────┘ └─────────────────┘ └─────────────────┘
```

### Implementation Steps

1. **Create Directory Structure** (Plugin repo)
   - Separate directories for Android/iOS/OHOS
   - Each platform has its own implementation

2. **Define Platform Interface** (Optional)
   - Only if sharing common data structures
   - Otherwise, completely independent

3. **Implement Business Logic** (Per platform)
   - File: `plugins/{module}/android/{module}_impl.cpp`
   - Platform-specific data structures and algorithms

4. **Implement Platform Layer** (Per platform)
   - Android: JNI calls to platform APIs
   - iOS: Objective-C++ calls to platform APIs
   - OHOS: Direct use of OHOS APIs

5. **Add NAPI Bindings** (Per platform)
   - Reuse NAPI structure only
   - Different implementations per platform

### Example Modules

- `@ohos.bluetooth` - 15% reuse (different BLE stacks)
- `@ohos.pasteboard` - 10% reuse (different clipboard APIs)
- `@ohos.multimedia.camera` - 5% reuse (platform-specific frameworks)

### Pros & Cons

**Pros**:
- ✅ Platform-native performance
- ✅ Access to all platform features
- ✅ No OHOS code dependency
- ✅ Independent maintenance per platform

**Cons**:
- ❌ Higher implementation cost
- ❌ More code to maintain
- ❌ Potential inconsistencies
- ❌ Longer time-to-market

---

## Mode 3: Hybrid Mode

### Overview

Reuse platform-independent logic while implementing platform-specific layers separately. Use service abstraction to bridge the two.

### Characteristics

- **Code Reuse**: 60-80%
- **New Code**: 1,500-2,500 lines
- **Time**: 6-10 weeks
- **Maintenance**: Medium
- **Risk**: Medium-Low

### Architecture Diagram

```
┌────────────────────────────────────────────────────────────────┐
│  ArkTS API Layer (.d.ts)                                     │
│  Same across all platforms                                     │
└────────────────────────────────────────────────────────────────┘
                           ↓
┌────────────────────────────────────────────────────────────────┐
│  NAPI Binding Layer (Shared)                                  │
│  Same code across all platforms                                │
└────────────────────────────────────────────────────────────────┘
                           ↓
┌────────────────────────────────────────────────────────────────┐
│  Shared Business Logic Layer (70% Shared)                    │
│  Platform-independent data processing                          │
└────────────────────────────────────────────────────────────────┘
                           ↓
┌────────────────────────────────────────────────────────────────┐
│  Service Abstraction Layer (Pure Virtual)                     │
│  Abstracts platform service operations                         │
└────────────────────────────────────────────────────────────────┘
                           ↓
            ┌──────────────┬──────────────┬──────────────┐
            ↓              ↓              ↓              ↓
    ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
    │ Android Service │ │   iOS Service   │ │  OHOS Service   │
    │ (JNI + Native)  │ │ (ObjC++ + Native)│ │ (Native APIs)   │
    │                 │ │                 │ │                 │
    │ LocationManager │ │  CLLocationManager│ │ Locator API     │
    │ + Coordinate     │ │  + Coordinate    │ │ + Coordinate    │
    │   Transformation │ │   Transformation │ │   Transformation│
    └─────────────────┘ └─────────────────┘ └─────────────────┘
```

### Implementation Steps

1. **Identify Shared Logic** (Analysis)
   - Data processing algorithms
   - Data structure definitions
   - Utility functions

2. **Extract Shared Code** (Refactoring)
   - Move to common directory
   - Add conditional compilation where needed

3. **Define Service Interface** (Abstraction)
   - Abstract platform service operations
   - Define common data structures

4. **Implement Platform Services** (Per platform)
   - Android: JNI + native service
   - iOS: ObjC++ + native service
   - OHOS: Direct use of native service

5. **Integrate Shared Logic** (Wiring)
   - Connect shared logic to platform services
   - Test integration thoroughly

### Example Modules

- `@ohos.geolocation` - 75% reuse (coordinate transformation independent)
- `@ohos.sensor` - 70% reuse (sensor data processing independent)
- `@ohos.request` - 68% reuse (HTTP layer reusable)

### Pros & Cons

**Pros**:
- ✅ Balanced code reuse
- ✅ Platform-specific optimizations
- ✅ Flexibility in implementation
- ✅ Moderate maintenance

**Cons**:
- ❌ More complex architecture
- ❌ Requires careful abstraction
- ❌ Integration testing critical
- ❌ Potential for abstraction leaks

---

## Mode Selection Guide

### Quick Reference

| Use Case | Recommended Mode |
|----------|-----------------|
| Data storage/processing | OHOS Reuse |
| System framework integration | Independent |
| Mixed data/platform logic | Hybrid |
| Heavy platform APIs (>70%) | Independent |
| Data-focused (>90% logic) | OHOS Reuse |
| Quick time-to-market | OHOS Reuse |
| Maximum platform features | Independent |

### Decision Factors

**Choose OHOS Reuse When**:
- Platform-independent code > 90%
- Data processing focused
- Tight timeline
- Limited team size
- Want to minimize maintenance

**Choose Independent When**:
- Platform-specific code > 70%
- Requires native platform features
- Different architectural patterns per platform
- Team has platform expertise
- Long-term project with resources

**Choose Hybrid When**:
- Mix of independent and platform code (50-90% range)
- Can extract common data structures
- Need platform optimizations
- Moderate timeline
- Team has abstraction experience

---

## Comparison Matrix

| Aspect | OHOS Reuse | Independent | Hybrid |
|--------|-----------|-------------|---------|
| **Code Reuse** | 90-95% | 10-30% | 60-80% |
| **Implementation Time** | 4-6 weeks | 10-16 weeks | 6-10 weeks |
| **Maintenance Effort** | Low | Medium | Medium |
| **Risk Level** | Low | Medium | Medium-Low |
| **Platform Parity** | High | High | Medium |
| **Time to Market** | Fast | Slow | Medium |
| **Best Module Type** | Data-focused | Platform-heavy | Mixed |
| **Team Size Required** | Small | Large | Medium |
| **Platform Expertise** | Low | High | Medium |

---

## Real-World Examples

### Example 1: Preferences (OHOS Reuse)

**Analysis**:
- 92.5% platform-independent
- Only XML file I/O is platform-specific
- Caching, observers fully reusable

**Result**: 95% code reuse, 530 new lines, 4 weeks

### Example 2: Bluetooth (Independent)

**Analysis**:
- 85% platform-specific
- Each platform has different BLE stack
- OHOS tied to OHOS bluetooth service

**Result**: 15% code reuse, 5,200 new lines, 14 weeks

### Example 3: Geolocation (Hybrid)

**Analysis**:
- 75% platform-independent (coordinate transformation)
- 25% platform-specific (location services)
- Can abstract location operations

**Result**: 70% code reuse, 2,000 new lines, 8 weeks

---

## Related Files

- **Phase 5**: [ARCHITECTURE_RECOMMENDATION.md](phase5-architecture-recommendation.md) - How to choose
- **Phase 6**: [IMPLEMENTATION_GUIDE.md](phase6-implementation-guide.md) - How to implement
- **Reference**: [CODE_EXAMPLES.md](code-examples.md) - Code examples for each mode
