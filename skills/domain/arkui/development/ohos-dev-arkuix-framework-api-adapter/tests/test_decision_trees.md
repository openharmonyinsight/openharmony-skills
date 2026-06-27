# Evaluation Cases: Decision Tree Tests

> **Category B**: Tests the skill's decision logic across architecture modes, scenarios, and boundary cases.
>
> **How to use**: For each case, provide the input to an agent loaded with this skill. Verify the agent's output matches the expected decision.

---

## B01: Scenario A — OHOS Source Available, No Existing Adaptation

**Input context**:
```
Working directory: ArkUI-X SDK source tree (.repo/, plugins/)
Module: @ohos.data.preferences
openharmony.xml: contains "distributeddatamgr_preferences"
plugins/data/preferences/: does NOT exist
```

**Expected agent decision**:
- Phase 1: Identify module name `preferences`, repo `distributeddatamgr_preferences`
- Phase 2: Source code available at `foundation/distributeddatamgr/preferences/`
- Phase 4 Step 0: Scenario A detected
- Phase 4: Full architecture analysis of OHOS source
- Phase 5: Recommend architecture mode based on analysis result

**PASS criteria**: Agent enters full Phase 4 analysis, does NOT skip to Phase 7.

---

## B02: Scenario B — OHOS Source + Partial Adaptation

**Input context**:
```
Working directory: ArkUI-X SDK source tree
Module: @ohos.net.http
openharmony.xml: contains "communication_netstack"
plugins/net/http/: exists with android/ but missing ios/
```

**Expected agent decision**:
- Phase 4 Step 0: Scenario B detected
- Phase 4: Analyze BOTH OHOS source AND existing plugins/ code
- Phase 5: Recommend supplementing iOS in same pattern as existing Android
- Phase 6: Only generate iOS adapter, not re-do Android

**PASS criteria**: Agent reuses existing Android pattern, only generates missing iOS code.

---

## B03: Scenario C — OHOS Source + Already Complete

**Input context**:
```
Working directory: ArkUI-X SDK source tree
Module: @ohos.deviceInfo
openharmony.xml: contains "device_info"
plugins/device_info/: exists with android/java/ AND ios/ — both populated
```

**Expected agent decision**:
- Phase 4 Step 0: Scenario C detected
- SKIP Phase 4-6 entirely
- Go directly to Phase 7 E2E verification

**PASS criteria**: Agent does NOT generate any new code. Proceeds to E2E verification.

---

## B04: Scenario D — No OHOS Source, Already Adapted

**Input context**:
```
Working directory: ArkUI-X SDK source tree
Module: @ohos.pasteboard
openharmony.xml: no entry for pasteboard repo
plugins/pasteboard/: exists with full android/ + ios/ + mock/
```

**Expected agent decision**:
- Phase 4 Step 0: Scenario D detected
- Phase 4: Analyze existing plugins/ code only (no OHOS source to analyze)
- Understand architecture mode used in existing code
- Phase 7: Verify existing code works via E2E

**PASS criteria**: Agent does NOT attempt `repo sync`. Analyzes existing code only.

---

## B05: Mode Selection — Pure Data Module → OHOS Reuse

**Input**: Module `@ohos.data.preferences` with >90% pure C++ code (SQLite-based, no platform APIs).

**Expected**: Architecture mode = **OHOS Reuse**

**Expert heuristics to verify**:
- Module uses SQLite → portable, zero platform code
- No `OHOS::` system service calls in core logic
- Only path differences needed (~50 lines per platform)

**FAIL if**: Agent recommends Independent or Hybrid mode.

---

## B06: Mode Selection — Platform-Heavy Module → Independent

**Input**: Module `@ohos.bluetooth.socket` with JNI/ObjC++ in every file, hardware-dependent.

**Expected**: Architecture mode = **Independent**

**Expert heuristics to verify**:
- Every API requires platform-specific Bluetooth framework
- Android: `android.bluetooth.*`, iOS: `CoreBluetooth.*`
- No shared business logic possible

**FAIL if**: Agent recommends OHOS Reuse for a hardware-dependent module.

---

## B07: Mode Selection — Mixed Module → Hybrid

**Input**: Module `@ohos.geolocation` with shared data structures but platform-specific location services.

**Expected**: Architecture mode = **Hybrid**

**Expert heuristics to verify**:
- Data structures (`LocationInfo`, `LocationRequest`) are portable
- Platform services (GPS, network location) need adapters
- Uses pure virtual interface pattern

**FAIL if**: Agent recommends pure OHOS Reuse (ignoring platform services) or pure Independent (ignoring shared data).

---

## B08: Boundary Case — Settings Module (Data + Platform Control)

**Input**: Module `@ohos.settings` — data read/write (portable) + system settings control (platform-specific).

**Expected**: Architecture mode = **OHOS Reuse** (lean toward reuse per 60/40 Rule)

**Expert heuristics to verify**:
- Read/write is 90% data access → portable
- Platform control APIs can be stubbed on non-OHOS platforms
- 60/40 Rule applied: "If unsure, choose more code reuse"

**FAIL if**: Agent recommends Independent mode without justification for overriding 60/40 Rule.
