# Plugin Directory Structure Reference

Real-world plugin directory structures from ArkUI-X `plugins/`, categorized by architecture mode.

## OHOS Reuse Mode — Pure Data Module (No Platform Code)

**Reference**: `plugins/data/preferences/`

When a module is pure C/C++ (SQLite, libxml2, OpenSSL), the plugin only needs a BUILD.gn that depends on the OHOS source directly. No `android/` or `ios/` subdirectories needed.

```
plugins/data/preferences/
└── BUILD.gn                     # deps → foundation/distributeddatamgr/preferences/...
```

BUILD.gn pattern:
```gni
template("plugin_data_preferences_static") {
  ohos_source_set(target_name) {
    deps = [
      "//foundation/distributeddatamgr/preferences/frameworks/js/napi/preferences:data_preferences",
      "//foundation/distributeddatamgr/preferences/interfaces/inner_api:native_preferences",
    ]
    subsystem_name = "plugins"
    part_name = "data_preferences"
  }
}
```

## OHOS Reuse Mode — With Platform Adapters

**Reference**: `plugins/device_info/`

When a module needs platform-specific implementations alongside shared NAPI bindings.

```
plugins/device_info/
├── BUILD.gn                     # Template + foreach loop over ace_platforms
├── device_info.cpp              # NAPI bindings + platform dispatch (shared)
├── device_info.h                # Interface definition (shared)
├── device_info_sdk.cpp          # SDK-level helpers (shared)
├── android/
│   └── java/
│       ├── BUILD.gn             # Android JNI build target
│       ├── jni/
│       │   ├── device_info_impl.cpp    # C++ JNI implementation
│       │   ├── device_info_impl.h
│       │   ├── device_info_jni.cpp     # JNI registration
│       │   └── device_info_jni.h
│       └── src/
│           └── ohos/ace/plugin/device_infoplugin/
│               └── DeviceInfoPlugin.java   # Java layer
├── ios/
│   ├── BUILD.gn                # iOS build target
│   ├── device_info_impl.h
│   └── device_info_impl.mm     # ObjC++ implementation
└── etc/                        # Build parameters
    ├── BUILD.gn
    └── build.para
```

BUILD.gn pattern:
```gni
template("plugin_device_info_static") {
  ohos_source_set(target_name) {
    sources = [ "device_info.cpp", "device_info_sdk.cpp" ]
    deps = [
      "//plugins/interfaces/native:ace_plugin_util_${platform}",
      "//plugins/libs/napi:napi_${target_os}",
    ]
    if (platform == "android") {
      deps += [ "android/java:device_info_android_jni" ]
    } else if (platform == "ios") {
      deps += [ "ios:device_info_plugin_ios" ]
    }
    subsystem_name = "plugins"
    part_name = "device_info"
  }
}
```

## Hybrid Mode — Shared Logic + Platform Adapters

**Reference**: `plugins/net/http/`

Shared business logic (cache, serialization) lives at root level. Platform adapters in `android/` and `ios/` subdirectories.

```
plugins/net/http/
├── BUILD.gn                     # Main build entry
├── http.gni                     # Shared source/include path definitions
├── http_module.cpp              # NAPI module entry (shared)
├── http_exec_interface.h        # Platform abstraction interface
├── cache/                       # Shared cache logic (cross-platform)
│   ├── base64_utils.cpp
│   └── cache_proxy.cpp
├── android/
│   ├── BUILD.gn
│   ├── http_exec.cpp            # Android HTTP implementation
│   ├── http_exec.h
│   └── java/
│       ├── BUILD.gn
│       ├── jni/
│       │   ├── http_jni.cpp
│       │   └── http_jni.h
│       └── src/.../HttpPlugin.java
└── ios/
    ├── BUILD.gn
    ├── http_exec.cpp            # iOS HTTP implementation (cURL-based)
    ├── http_exec.h
    ├── http_exec_ios_iml.h
    ├── http_exec_ios_iml.mm     # ObjC++ implementation
    ├── http_ios_request.h
    ├── http_ios_request.mm
    └── lru_cache/               # iOS-specific cache
        └── ...
```

Key pattern: `.gni` file defines shared paths, BUILD.gn uses conditional `target_os` blocks.

## Independent Mode — Full Independent Implementation

**Reference**: `plugins/pasteboard/`

Complete independent implementation with mock headers for OHOS dependencies. No shared code with OHOS source.

```
plugins/pasteboard/
├── BUILD.gn                     # deps → interfaces/kits:pasteboard_napi
├── framework/
│   ├── innerkits/
│   │   ├── include/             # Independent data structures
│   │   │   ├── paste_data.h
│   │   │   ├── paste_data_record.h
│   │   │   ├── pasteboard_client.h
│   │   │   └── ...
│   │   └── src/                 # Independent implementation
│   │       ├── paste_data.cpp
│   │       ├── pasteboard_client.cpp
│   │       └── ...
│   └── tlv/                     # Serialization utilities
│       └── ...
├── interfaces/kits/
│   └── BUILD.gn                 # NAPI bindings
└── mock/                        # OHOS dependency mocks (no real OHOS deps)
    ├── message_parcel.h
    ├── ipasteboard_service.h
    └── ...
```

Key pattern: `mock/` directory replaces OHOS system headers to enable standalone compilation.

## Directory Naming Convention

| Convention | Example | Used In |
|-----------|---------|---------|
| `{module}` | `device_info`, `pasteboard`, `bluetooth` | Top-level modules |
| `{category}/{module}` | `data/preferences`, `net/http`, `multimedia/media` | Categorized modules |
| `{module}/{submodule}` | `bluetooth/ble`, `bluetooth/access`, `bluetooth/a2dp` | Sub-modules |

## All Available Plugins (70+)

```
ability_access_ctrl    display              multimedia
accessibility          drawable_descriptor  multimodalinput
arkts                  effectkit            net
arkui                  events               notification_manager
bluetooth              fastbuffer           pasteboard
bridge                 file                 process
buffer                 geo_location_manager request
common_event_manager   graphics             running_lock
component              hilog                security
console                hitrace_meter        system_date_time
convertxml             hiviewdfx            taskpool
data                   i18n                 timer
device_info            intl                 uitest
libs                   uri                  url
                       util                 vibrator
                       web                  wifi_manager
                       worker               xml
                       zlib
```
