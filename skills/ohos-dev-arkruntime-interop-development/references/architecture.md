# ArkTS-JS Interop Architecture

The interop layer sits in `runtime_core/static_core/plugins/ets/runtime/interop_js/`. It bridges the gap between the ArkTS runtime (ETS) and the JavaScript runtime (via Node-API/NAPI).

## Key Directories

*   **`ets_proxy/`**: Mechanisms to expose ETS objects to JavaScript. Handles wrappers and reference counting for ETS objects living in JS world.
*   **`js_proxy/`**: Mechanisms to expose JavaScript objects to ETS. Wraps JS objects so they can be manipulated from ArkTS.
*   **`intrinsics/`**: Low-level intrinsic functions that provide direct access to interop functionality from ArkTS.
*   **`napi_impl/`**: Implementation details related to Node-API (NAPI), which is the standard interface for JS engine interactions.
*   **`native_api/`**: APIs exposed to native code.

## Key Files

*   **`interop_context.h/cpp`**: Defines `InteropCtx`, the central context manager for a thread's interop state.
*   **`js_convert.h`**: Templates and logic for converting values between ETS and JS representations.
*   **`js_refconvert_*.h/cpp`**: Specific reference converters for Arrays, Functions, Records, Unions, etc.
*   **`ets_vm_plugin.cpp`**: The plugin entry point that initializes the interop layer within the ArkVM.
