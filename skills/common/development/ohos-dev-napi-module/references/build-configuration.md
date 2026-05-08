# BUILD.gn Configuration

OpenHarmony uses GN (Generate Ninja) build system with mandatory security configurations. This differs significantly from Node.js's node-gyp system.

## Template

```python
import("//build/ohos.gni")

ohos_shared_library("module_name") {
    # Security configuration (OpenHarmony specific)
    sanitize = {
        cfi = true              # Control Flow Integrity
        cfi_cross_dso = true    # Cross-DSO CFI protection
        debug = false
    }
    
    branch_protector_ret = "pac_ret"  # Return address protection (ARM PAC)
    
    sources = [
        "src/module_name_module.cpp",
        "src/module_name_napi.cpp",
    ]
    
    # CRITICAL: Must include napi dependency
    external_deps = [
        "napi:ace_napi",
        "hilog:libhilog",
    ]
    
    # Installation path (OpenHarmony specific)
    relative_install_dir = "module/subsystem"  # e.g., "module/multimedia", "module/application"
    
    subsystem_name = "subsystem_name"  # e.g., "multimedia", "ability"
    part_name = "part_name"  # e.g., "av_session", "form_fwk"
}
```

## Key Differences from Node.js

| Feature | OpenHarmony (GN) | Node.js (node-gyp) |
|---------|------------------|-------------------|
| Build System | GN (BUILD.gn) | node-gyp (binding.gyp) |
| Security Config | Mandatory (CFI, PAC) | Optional |
| Installation Path | `relative_install_dir` (system-level) | node_modules directory |
| Dependency | `"napi:ace_napi"` | libnode |
| Target Type | `ohos_shared_library()` | Shared library |

## Security Configurations Explained

### CFI (Control Flow Integrity)
- Validates function call destinations
- Prevents code injection attacks
- Mandatory for all OpenHarmony native modules
- `cfi_cross_dso = true` enables cross-DSO protection

### PAC (Pointer Authentication Code)
- ARM-specific return address protection
- Prevents return-oriented programming (ROP) attacks
- `branch_protector_ret = "pac_ret"` enables PAC for return addresses

## Required Fields

**external_deps**:
- Must include `"napi:ace_napi"` for all NAPI modules
- Additional dependencies like `"hilog:libhilog"` for logging

**relative_install_dir**:
- Specifies installation path under system directory
- Standard paths: `"module/"`, `"module/multimedia/"`, `"module/application/"`
- Must match subsystem structure

**subsystem_name & part_name**:
- Identifies which subsystem and part the module belongs to
- Required for system-level module management

## Common Errors

**Missing napi dependency**:
```python
# ❌ WRONG - Missing napi dependency
external_deps = [
    "hilog:libhilog",
]
```
Solution: Add `"napi:ace_napi"` to external_deps

**Missing security configuration**:
```python
# ❌ WRONG - No security config
ohos_shared_library("module") {
    sources = ["module.cpp"]
}
```
Solution: Add sanitize block and branch_protector_ret

## Best Practices

1. Always include `"napi:ace_napi"` dependency
2. Enable both CFI and PAC for security
3. Use appropriate `relative_install_dir` based on subsystem
4. Define correct subsystem_name and part_name
5. Keep build configuration consistent across modules