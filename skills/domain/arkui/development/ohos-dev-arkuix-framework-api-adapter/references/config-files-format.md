# Mandatory Configuration Files Format Reference

Every ArkUI-X plugin MUST update 4 configuration files. This document provides the exact format based on the `device_info` reference implementation.

**Reference module**: `plugins/device_info/` → `@ohos.deviceInfo`

## File 1: `plugins/plugin_lib.gni`

Add the module's directory path (relative to `plugins/`) to the `common_plugin_libs` list.

```gni
common_plugin_libs = [
  // ... existing entries ...
  "device_info",          # Top-level module
  "data/preferences",     # Categorized module (path uses /)
  "net/http",             # Categorized module
  // ... add your module here ...
]
```

**Rules**:
- Value = directory path under `plugins/`
- Subdirectory modules use `/` separator: `"data/preferences"`, `"net/http"`
- Top-level modules use just the name: `"device_info"`, `"pasteboard"`
- Alphabetical order within the list (follow existing convention)

## File 2: `interface/sdk/plugins/api/apiConfig.json`

Add a JSON object to the top-level array for the module's library configuration.

```json
{
    "module": "ohos.deviceInfo",
    "library": {
        "android": [
            "lib/device_info/ace_device_info_android.jar",
            "lib/device_info/arch_type/libdeviceinfo.so"
        ],
        "ios": [
            "xcframework/build_modes/libdeviceinfo.xcframework"
        ]
    },
    "deps": {
        "android": [],
        "ios": []
    }
}
```

### Field Reference

| Field | Description | Example |
|-------|-------------|---------|
| `module` | The `@ohos.*` module name from d.ts. **Must match d.ts filename exactly** (may be camelCase). | `"ohos.deviceInfo"` (NOT `ohos.device_info`) |
| `library.android` | Array of Android library paths relative to `arkui-x/plugins/api/`. JAR first, then .so. | `["lib/device_info/ace_device_info_android.jar", "lib/device_info/arch_type/libdeviceinfo.so"]` |
| `library.ios` | Array of iOS library paths. Usually one xcframework. | `["xcframework/build_modes/libdeviceinfo.xcframework"]` |
| `deps.android` | Third-party or engine dependencies needed at runtime. Empty `[]` for most modules. Non-empty when module uses third-party libs or engine utilities. | `["engine/third_party/xml2"]` (preferences), `["engine/third_party/curl", "engine/utils/net_util"]` (http) |
| `deps.ios` | Same as `deps.android` for iOS. May differ from Android (e.g., iOS doesn't need curl). | `["engine/third_party/xml2"]` (preferences), `["engine/utils/net_util"]` (http) |

**Non-empty deps patterns**:
- XML parsing → `"engine/third_party/xml2"` (preferences, convertxml, i18n)
- Crypto → `"engine/third_party/openssl/crypto"` (file.fs, file.hash, security.*)
- HTTP → `"engine/third_party/curl"`, `"engine/utils/net_util"` (net.http, net.socket)
- Bluetooth → `"engine/utils/bluetooth_common"` (bluetooth.*)

### Naming Patterns

| Convention | d.ts module name | Directory name | .so name | JAR name |
|-----------|-----------------|----------------|----------|----------|
| Top-level | `deviceInfo` (camelCase) | `device_info` (snake_case) | `libdeviceinfo.so` (no separator) | `ace_device_info_android.jar` |
| Categorized | `data.preferences` | `data/preferences` | `libdat...` | varies |

**Important**: The `module` field uses the d.ts naming (camelCase), while directory and file paths use snake_case.

## File 3: `build_plugins/sdk/arkui_cross_sdk_description_std.json`

Add build entries that specify how to install the module's build artifacts into the SDK.

### For modules with Java plugin (Android JAR):

```json
{
    "install_dir": "arkui-x/plugins/api/lib/device_info",
    "module_label": "//plugins/device_info/android/java:device_info_java",
    "target_os": ["linux", "windows", "darwin"]
}
```

### For modules with native .so (Android):

```json
{
    "install_dir": "arkui-x/plugins/api/lib/device_info/arch_type",
    "module_label": "//foundation/arkui/ace_engine/adapter/android/build:deviceinfo",
    "target_os": ["linux", "windows", "darwin"]
}
```

### For modules without JAR (pure native):

```json
{
    "install_dir": "arkui-x/plugins/api/lib/display/arch_type",
    "module_label": "//plugins/display:display_static_android",
    "target_os": ["linux", "windows", "darwin"]
}
```

### Field Reference

| Field | Description |
|-------|-------------|
| `install_dir` | Destination path in the SDK. Pattern: `arkui-x/plugins/api/lib/{module_dir}` for JARs, `arkui-x/plugins/api/lib/{module_dir}/arch_type` for .so |
| `module_label` | GN build target label. Points to BUILD.gn target that produces the artifact. Format: `//{path}:{target_name}` |
| `target_os` | Always `["linux", "windows", "darwin"]` — these are the **host** OSes that can build, not the target device OS |

**Two `module_label` patterns for native .so**:
1. `//plugins/{module}/{subpath}:{target}` — native code lives in `plugins/` (most modules)
2. `//foundation/arkui/ace_engine/adapter/android/build:{target}` — native code lives in ACE engine adapter layer (used for system-level .so like `deviceinfo`, `libarkui_android`)

**Rule**: If the module has its own BUILD.gn in `plugins/` that produces the .so, use pattern 1. If the .so is produced by the ACE engine's build system, use pattern 2. Check `//foundation/arkui/ace_engine/adapter/android/build/BUILD.gn` for existing targets.

## File 4: `interface/sdk-js/api/@ohos.{module}.d.ts`

Add `@crossplatform` annotations to each interface/method that has been adapted.

### Annotation Format

```typescript
/**
 * @syscap SystemCapability.Startup.SystemInfo
 * @crossplatform [since 11]     // ← Add this line
 * @since 6
 */
declare namespace deviceInfo {
```

### Rules

1. Add `@crossplatform` after `@syscap` line, before `@since` line
2. If the module was adapted in a specific API version, add `[since {version}]`
3. If the module was adapted from the beginning, just `@crossplatform` without version
4. Apply to: namespace, class, interface, function, method, property — any adapted declaration
5. **Do NOT add `@crossplatform` to interfaces that are NOT yet adapted**

### Example (deviceInfo — module-level):

```typescript
// Before:
/**
 * @syscap SystemCapability.Startup.SystemInfo
 * @since 6
 */
declare namespace deviceInfo {

// After:
/**
 * @syscap SystemCapability.Startup.SystemInfo
 * @crossplatform [since 11]
 * @since 6
 */
declare namespace deviceInfo {
```

## Cross-File Naming Consistency Check

All 4 files must agree on the module identity. Verify character by character:

```
plugin_lib.gni:          "device_info"          (directory path)
apiConfig.json module:   "ohos.deviceInfo"      (d.ts module name)
arkui_cross_sdk module_label: "//plugins/device_info/..."  (GN path)
d.ts file:               @ohos.deviceInfo.d.ts  (filename)
```

| Dimension | Naming Convention | Example |
|-----------|------------------|---------|
| d.ts filename | camelCase module name | `deviceInfo`, `data.preferences` |
| plugin_lib.gni | directory path (snake_case) | `device_info`, `data/preferences` |
| apiConfig.json module | `ohos.` + d.ts module name | `ohos.deviceInfo` |
| apiConfig.json library path | directory path (snake_case) | `lib/device_info/` |
| .so name | `lib` + lowercase concatenated | `libdeviceinfo.so` |
| JAR name | `ace_` + directory path + `_android.jar` | `ace_device_info_android.jar` |

## Related Files

- **Phase 6**: [phase6-implementation-guide.md](phase6-implementation-guide.md) — when to update these files
- **Scripts**: `scripts/code_generator.py` — automated generation (⚠️ has known issues with filename mapping, verify manually)
