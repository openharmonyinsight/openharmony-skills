# AGENTS.md

This file provides guidance to agents when working with code in repository.

## Build System

- Use GN (Generate Ninja) build system, not traditional Make or CMake
- Main build files: BUILD.gn (root directory) and napi.gni (configuration file)
- Build target: `//foundation/arkui/napi:napi_packages`
- Test target: `//foundation/arkui/napi:napi_packages_test`
- Build commands:
   Build commands must be selected strictly according to the directory structure

   > Note
   >
   > Unless otherwise specified, the working directory for the following commands is the gn root directory
   >
   > Note: target-cpu needs to be asked from the user, available values are arm and arm64

   - If only the `//foundation/arkui/napi` folder exists under the `//foundation/arkui` directory
     In this case, we called it `indenpendicy project`

     ```bash
     # Update dependencies
     bash ./build/prebuilts_config.sh

     # Run build commands
     # Note: If hb tool is not installed, you can install it via path //build/hb
     # Do not compile test cases
     hb build napi -i # Compile all build targets except test cases
     # Compile all targets
     hb build napi -t # Compile all targets, including test cases
     ```
   - For other cases, in addition to using the above commands for compilation, you can also use the following commands

     ```bash
     # Update dependencies
     bash ./build/prebuilts_download.sh
     # Build command
     ./build.sh --product-name rk3568 --target-cpu arm64 --build-target ace_napi # If you need to compile the test suite, change the build target to napi_packages_test
     ```

## Run Test

Run test suits command.

Path must be replace to physisc path in project root. `//` means project root.

ohos-sdk path maybe need update if not exist.

you may need to make a link //out/standard/test to //out/rk3568 if `indenpendicy project` detected.

replace `-t UT` to `to FUZZ` to run fuzz test suit.


```bash
env -C //test/testfwk/developer_test/src \
    PATH="//prebuilts/ohos-sdk/linux/23/toolchains:\
    /usr/local/sbin:\
    /usr/local/bin:\
    /usr/sbin:\
    /usr/bin:\
    /sbin:\
    /bin" \
    //prebuilts/python/linux-x86/current/bin/python3 -m main run -t UT -p rk3568 -ss napi
```

## Key Implementation Details

- Ark JS engine implementation is located in the `native_engine/impl/ark/` directory
- Supports multiple platforms: OHOS, Linux, Windows, macOS, iOS, Android
- Supports multiple architectures: ARM64, ARM32, x86_64, x86
- Data protection feature is automatically enabled on ARM64 OHOS platform

## Development Notes

- New modules need to be registered in the napi_sources list in napi.gni
- Platform-specific code uses conditional compilation directives (e.g., #ifdef OHOS_PLATFORM)
- Error handling uses NativeErrorExtendedInfo structure
- Async operations use NativeAsyncWork and NativeSafeAsyncWork
- Thread-safe operations use appropriate synchronization mechanisms
- Interfaces that need to interact with VM objects like JSValueRef require the caller to ensure thread safety
- For thread-safe API interfaces, when returning error codes, call `napi_set_last_error` or `napi_clear_last_error` to update exception information and return
- Public API interfaces should be declared in `interfaces/kits/napi/native_api.h`, internal interfaces (for use by other system modules) should be declared in `interfaces/inner_api/napi/native_node_api.h`
