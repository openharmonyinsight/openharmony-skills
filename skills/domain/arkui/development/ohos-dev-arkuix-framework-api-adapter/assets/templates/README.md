# ArkUI-X Module Adapter Templates

This directory contains code templates for module adaptation.

## Directory Structure

```
templates/
├── ohos-reuse-mode/           # Templates for OHOS Reuse Mode
│   ├── adapter_interface.h.template
│   ├── ohos_wrapper.cpp.template
│   ├── android_adapter.cpp.template
│   └── ios_adapter.mm.template
└── build-config/               # Build configuration templates
    ├── BUILD.gn.template
    └── module.gni.template
```

## Template Usage

Templates use Python string formatting with placeholders:

```python
{MODULE_NAME}           # Module name (e.g., preferences)
{MODULE_PATH}           # Module path (e.g., data/preferences)
{REPO_NAME}             # Repository name (e.g., distributeddatamgr_preferences)
{API_VERSION}           # API version (e.g., 23)
{YEAR}                  # Copyright year
```

## Generating from Templates

```python
from pathlib import Path

# Read template
template_path = Path("assets/templates/ohos-reuse-mode/adapter_interface.h.template")
template = template_path.read_text()

# Replace placeholders
code = template.format(
    MODULE_NAME="preferences",
    MODULE_PATH="data/preferences",
    REPO_NAME="distributeddatamgr_preferences",
    API_VERSION=23,
    YEAR=2025
)

# Write to target
output_path = Path("foundation/distributeddatamgr/preferences/interfaces/adapter/include/preferences_adapter.h")
output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(code)
```

## Template Files

### OHOS Reuse Mode Templates

1. **adapter_interface.h.template** - Pure virtual interface definition
2. **ohos_wrapper.cpp.template** - OHOS thin wrapper (100% forwarding)
3. **android_adapter.cpp.template** - Android JNI adapter
4. **ios_adapter.mm.template** - iOS Objective-C++ adapter

### Build Configuration Templates

1. **BUILD.gn.template** - GN build configuration
2. **module.gni.template** - Module-specific configuration

## Best Practices

1. **Keep Templates Simple**: Only include essential structure
2. **Document Placeholders**: Clear comments for each placeholder
3. **Update Regularly**: Keep templates in sync with best practices
4. **Test Templates**: Verify generated code compiles

## Related Files

- **Reference**: [CODE_EXAMPLES.md](../../references/code-examples.md) - Complete examples
- **Scripts**: `scripts/code_generator.py` - Automated generation
