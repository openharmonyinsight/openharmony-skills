# E2E Verification Guide

Self-contained end-to-end verification process for adapted modules. Used in Phase 7 after code generation is complete.

## Overview

```
Phase 6 产出                      Phase 7 验证管线
┌───────────────────────┐       ┌──────────────────────────────────┐
│ 适配完成的 C++ 代码    │       │ Step 1: 编译框架 (包含新代码)      │
│ 4 个配置文件           │ ────► │ Step 2: 替换 SDK (overlay)        │
│ @crossplatform 注解    │       │ Step 3: 建测试工程 + 生成测试代码   │
│ Phase 3 API 清单       │       │ Step 4: 编译部署到设备             │
│ Phase 5 测试用例规格   │       │ Step 5: 日志验证 + crash 检测     │
└───────────────────────┘       └──────────────────────────────────┘
```

## Before Starting

**MUST confirm with developer before proceeding:**

```
E2E 验证流程：
1. 确认范围 (目标平台、测试重点)
2. 编译 ArkUI-X 框架 (./build.sh)
3. 替换本地 SDK 产物
4. 创建测试工程 (ace create)
5. 编写测试代码
6. 编译并部署到设备 (ace build & run)
7. 验证日志结果

是否执行完整的端到端验证？(Y/N)
或选择部分执行：只编译、只替换SDK、只跑测试 等
```

**Do NOT proceed until developer explicitly confirms.**

---

## Step 1: Build ArkUI-X Framework

### 1.1 Prerequisites

```bash
# Verify source tree
ls .gn .repo/  # Must exist

# macOS note: build.sh targets Linux; macOS builds run on Linux CI
uname -s
```

### 1.2 Execute Build

```bash
# Android build
./build.sh --product-name arkui-x --target-os android

# iOS build
./build.sh --product-name arkui-x --target-os ios
```

Build duration: typically 30-90 minutes.

**On failure:** Check `out/arkui-x/` for error logs. Report error to developer. Do NOT proceed.

### 1.3 Verify Build Output

```bash
ls out/arkui-x/packages/arkui-x/$(uname -s | tr '[:upper:]' '[:lower:]')/
# Expected: arkui-x-{os}-{arch}-{version}-{release}.zip
```

---

## Step 2: Overlay SDK

### 2.1 Read Build Version

```bash
cat out/arkui-x/arkui-x/$(uname -s | tr '[:upper:]' '[:lower:]')/arkui-x/arkui-x.json
```

Example:
```json
{
  "apiVersion": "26",
  "version": "26.0.0.19",
  "releaseType": "Canary1"
}
```

Extract: `apiVersion`, `version`, `releaseType`.

### 2.2 Locate SDK Install Path

**Priority order:**

1. **Environment variable:**
   ```bash
   echo $ARKUIX_SDK_HOME
   ```
   If set, SDK root is `$ARKUIX_SDK_HOME`.

2. **Default macOS path:**
   ```
   ~/Library/ArkUI-X/Sdk
   ```

3. **Ask developer** if neither found.

### 2.3 Determine Target SDK Path

```
{SDK_ROOT}/{apiVersion}/arkui-x/
├── engine/
├── plugins/
├── toolchains/
├── arkui-x.json
└── ...
```

**Verify version match:**
```bash
cat {SDK_ROOT}/{apiVersion}/arkui-x/arkui-x.json
# apiVersion must match build output
```

### 2.4 Overlay Build Artifacts

```bash
BUILD_ZIP=$(ls out/arkui-x/packages/arkui-x/$(uname -s | tr '[:upper:]' '[:lower:]')/arkui-x-*.zip | head -1)
SDK_TARGET="{SDK_ROOT}/{apiVersion}/arkui-x"

# Backup existing SDK (recommended)
cp -r "$SDK_TARGET" "${SDK_TARGET}.bak.$(date +%Y%m%d%H%M%S)"

# Extract and replace
unzip -o "$BUILD_ZIP" -d /tmp/arkui-x-sdk-overlay/
rm -rf "$SDK_TARGET"
mv /tmp/arkui-x-sdk-overlay/arkui-x "$SDK_TARGET"
```

**Verify overlay:**
```bash
cat "$SDK_TARGET/arkui-x.json"
# version should match build output
```

---

## Step 3: Create Test Project + Generate Test Code

### 3.1 Determine API Version

```bash
API_VERSION=$(cat out/arkui-x/arkui-x/$(uname -s | tr '[:upper:]' '[:lower:]')/arkui-x/arkui-x.json | python3 -c "import sys,json; print(json.load(sys.stdin)['apiVersion'])")
```

### 3.2 Create Project

```bash
TEST_DIR=/tmp/arkuix-e2e-test-$(date +%Y%m%d%H%M%S)
mkdir -p "$TEST_DIR"
cd "$TEST_DIR"

ace create project
# Project name: e2eTest
# Bundle name: com.example.e2etest
# System: 1 (OpenHarmony)
# Project type: 1 (Application)
# Template: 1 (Empty Ability) or 2 (Native C++)
```

**If ace CLI not installed:**
```bash
cd {SDK_ROOT}/{apiVersion}/arkui-x/toolchains/ace_tools
npm install && npm install . -g
```

### 3.3 Generate Test Code from Phase 5 Test Case Specification

Use Phase 5's test case specification (not raw API inventory) to generate test code.

**Mapping rule**: One `async test(name, fn)` function per adapted API.

```
Phase 5 Test Case Spec                Test Code
┌──────────────────────────────┐     ┌────────────────────────────────┐
│ testGetValue001              │     │ await test('getValue', ...)    │
│   Android → Build.MODEL      │     │   // platform assertion built  │
│   iOS → UIDevice.name        │────►│   // from Phase 5 spec         │
│ testSetValueWithDomain001    │     │ await test('setValue', ...)    │
│   roundtrip verify           │     │   // roundtrip per spec        │
│ testEnableAirplaneMode001    │     │ await test('airplane', ...)    │
│   iOS → throws unsupported   │     │   // iOS expects error         │
└──────────────────────────────┘     └────────────────────────────────┘
```

Edit `entry/src/main/ets/pages/Index.ets`:

```typescript
import { /* relevant API */ } from '@ohos.{module}'

@Entry
@Component
struct Index {
  @State testResult: string = 'Testing...'

  aboutToAppear() {
    this.runTest()
  }

  runTest() {
    try {
      // Exercise the adapted API
      const result = /* API call */
      this.testResult = 'PASS: ' + JSON.stringify(result)
    } catch (err) {
      this.testResult = 'FAIL: ' + JSON.stringify(err)
    }
  }

  build() {
    Column() {
      Text('E2E Test Result')
        .fontSize(24)
        .margin({ bottom: 20 })
      Text(this.testResult)
        .fontSize(16)
        .fontColor(this.testResult.startsWith('PASS') ? Color.Green : Color.Red)
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
  }
}
```

### 3.4 Plugin Dependency (if needed)

For plugin module tests, add dependency in `entry/oh-package.json5`:

```json
{
  "dependencies": {
    "@ohos/data-preferences": "file://../../libs/data-preferences.har"
  }
}
```

---

## Step 4: Build & Run

### 4.1 Build

```bash
cd "$TEST_DIR/e2eTest"

# Android APK
ace build apk

# iOS App
ace build app
```

### 4.2 iOS Signing (Required for iOS)

**MUST ask developer for:**
- `DEVELOPMENT_TEAM` (Apple Developer Team ID)
- `PRODUCT_BUNDLE_IDENTIFIER` (if custom bundle ID needed)

```bash
# Configure signing
sed -i '' 's/DEVELOPMENT_TEAM = ""/DEVELOPMENT_TEAM = '"$TEAM_ID"'/g' \
  e2eTest/.arkui-x/ios/app.xcodeproj/project.pbxproj
```

### 4.3 Run

```bash
# Android
ace run apk

# iOS
ace run app
```

---

## Step 5: Validate Results

### 5.1 Check Logs

**Android:**
```bash
adb logcat -s Ace ArkUI ArkCompiler | grep -E "PASS|FAIL|ERROR|Fatal"
adb logcat | grep -i "{module-name}"
```

**iOS:**
```bash
log stream --device --predicate 'processImagePath contains "e2eTest"' --level debug
```

### 5.2 Validation Checklist

A module adaptation passes E2E verification when ALL are true:

- [ ] Framework builds successfully with the new module code
- [ ] SDK overlay completes without error
- [ ] Test project compiles on both Android and iOS
- [ ] App launches without crash on both platforms
- [ ] All adapted APIs show PASS in test results
- [ ] No ERROR/Fatal level logs related to the module
- [ ] No SIGABRT/SIGSEGV in crash logs

### 5.3 Report Results

```
E2E Test Results
================
Platform: Android / iOS
Build: {version} from {source-path}
Test focus: {what was tested}

Results:
- Launch: PASS/FAIL
- Test logic: PASS/FAIL
- Logs: clean / errors found

{Any relevant log snippets}
```

---

## Failure Handling

| Failure Point | Action |
|--------------|--------|
| Framework build fails | Fix in Phase 6 code, re-build. Do NOT modify test code. |
| SDK overlay fails | Check version match in arkui-x.json |
| Test project build fails | Check plugin dependency in oh-package.json5 |
| App crashes on launch | Check NAPI module registration + plugin_lib.gni |
| API test returns FAIL | Check platform adapter implementation. Systematic debugging. |
| Crash logs show SIGABRT | Check NAPI binding — likely null pointer or type mismatch |

### After 3 E2E Failures

STOP. Revert to last known working state. Document:
- Full failure log
- Module architecture mode chosen
- Platform-specific behavior differences observed

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `build.sh` fails on macOS | macOS not supported for build | Run build on Linux or CI |
| `ace: command not found` | ACE Tools not installed | Install from `{SDK}/toolchains/ace_tools` |
| iOS build fails with signing error | Missing DEVELOPMENT_TEAM | Ask developer for Team ID |
| `ARKUIX_SDK_HOME` not set | Environment not configured | Ask developer for SDK path |
| APK install fails | No device/emulator | Start emulator or connect device |
| App crashes on launch | SDK overlay mismatch | Verify arkui-x.json version matches |
| `ohpm` errors | ohpm not configured | Run ohpm init in toolchains dir |
