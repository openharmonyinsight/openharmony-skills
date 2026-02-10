# Common OpenHarmony Build Errors

Reference for common build errors and their solutions.

## Environment Errors

### Python Version Errors

**Error**:
```
[OHOS ERROR] Please execute the build/prebuilts_download.sh
```

**Cause**: Python prebuilts not available or incompatible version.

**Solution**:
```bash
# Download prebuilts
cd /path/to/openharmony
./build/prebuilts_download.sh
```

### Node.js Version Mismatch

**Error**:
```
[OHOS ERROR] Node.js version mismatch. Expected 14.21.1 but found v<x.y.z>
```

**Cause**: System Node.js version is not 14.21.1.

**Solution**: The build script should auto-configure the correct Node.js from prebuilts. If this fails:
```bash
# Check prebuilts Node.js
ls prebuilts/build-tools/common/nodejs/

# Verify build.sh is using prebuilt Node.js
./build.sh --product-name rk3568 --build-target ohos
```

### Shell Environment Errors

**Error**:
```
Your system shell isn't bash
```

**Cause**: System shell is not bash (e.g., dash).

**Solution**:
```bash
# Change default shell to bash (Ubuntu/Debian)
sudo dpkg-reconfigure dash
# Select "no" when prompted
```

## Compilation Errors

### Undefined Reference Errors

**Error**:
```
ld: error: undefined reference to 'symbol_name'
```

**Cause**: Linker cannot find a symbol definition.

**Common Solutions**:
1. Missing library dependency in BUILD.gn
2. Incorrect linking order
3. Missing source file in build target

**Investigation**:
```bash
# Search for symbol definition in codebase
grep -r "symbol_name" --include="*.h" --include="*.cpp"

# Check BUILD.gn for dependencies
grep -A 20 "target_name" path/to/component/BUILD.gn
```

### Header File Not Found

**Error**:
```
error: 'header_file.h' file not found
```

**Cause**: Include path is incorrect or header is missing.

**Solution**:
1. Verify header file exists in expected location
2. Check include_dirs in BUILD.gn
3. Verify dependency on component providing header

### Template/Inline Function Errors

**Error**:
```
error: undefined reference to 'std::function_template<...>'
```

**Cause**: Template instantiation issue, often in headers.

**Solution**:
- Ensure template implementation is in header file
- Check for explicit instantiation declarations

## Linking Errors

### Missing Library

**Error**:
```
ld: cannot find -l<library_name>
```

**Cause**: Library not found in search path.

**Solution**:
```bash
# Check if library exists in output
find out/ -name "lib<library_name>*"

# Verify library dependency in BUILD.gn
grep "lib<library_name>" path/to/BUILD.gn
```

### Circular Dependencies

**Error**:
```
ninja: error: dependency cycle: target1 -> target2 -> target1
```

**Cause**: Circular dependency between build targets.

**Solution**:
- Reorganize code to remove circular dependency
- Use interface libraries or source sets
- Split targets into smaller units

## Dependency Errors

### npm Package Not Found

**Error**:
```
npm ERR! code ENOENT
npm ERR! syscall open
npm ERR! path /path/to/package.json
```

**Cause**: Missing package.json or npm dependency issue.

**Solution**:
```bash
# Clean npm cache
rm -rf ~/.npm ~/.ohpm .node_modules

# Rebuild (build.sh will reinitialize)
./build.sh --product-name rk3568 --build-target ohos
```

### ohpm Dependency Issues

**Error**:
```
ohpm error: package '@ohos/module-name' not found
```

**Cause**: ohpm registry or dependency issue.

**Solution**:
```bash
# Check ohpm configuration
ohpm config get registry

# Reinitialize ohpm
rm -rf ~/.ohpm
./build.sh --product-name rk3568 --build-target ohos
```

## GN/Ninja Errors

### Build Target Not Found

**Error**:
```
ninja: error: unknown target: 'target_name'
```

**Cause**: Target does not exist in BUILD.gn files.

**Solution**:
```bash
# Search for target in BUILD.gn files
grep -r "target_name = \"target_name\"" --include="BUILD.gn"

# List available targets in component
grep "target_name" path/to/component/BUILD.gn
```

### GN Config Error

**Error**:
```
ERROR at //BUILD.gn:123:25: Unable to find target
```

**Cause**: GN configuration references non-existent target.

**Solution**:
- Verify target name exists in dependency path
- Check for typos in target name
- Ensure dependent component is built

## Memory/Resource Errors

### Out of Memory

**Error**:
```
clang: error: unable to execute command: Killed
```

**Cause**: System ran out of memory during compilation.

**Solution**:
```bash
# Reduce parallel jobs
export NINJA_PARALLEL_LINK_JOBS=1
./build.sh --product-name rk3568 --build-target ohos

# Or add swap space
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Disk Space

**Error**:
```
error: No space left on device
```

**Cause**: Insufficient disk space.

**Solution**:
```bash
# Check disk space
df -h

# Clean build outputs
rm -rf out/*/logs/
./build.sh --product-name rk3568 --build-target ohos

# Clean ccache
ccache -C
```

## Permission Errors

### Permission Denied

**Error**:
```
bash: ./build.sh: Permission denied
```

**Cause**: Script is not executable.

**Solution**:
```bash
chmod +x build.sh
./build.sh --product-name rk3568 --build-target ohos
```

### Write Permission

**Error**:
```
error: cannot create directory: Permission denied
```

**Cause**: No write permission to output directory.

**Solution**:
```bash
# Fix permissions
sudo chown -R $USER:$USER out/

# Or run with proper user (not recommended for full builds)
# sudo ./build.sh --product-name rk3568 --build-target ohos
```

## C++ Standard Library Errors

### std::* Not Found

**Error**:
```
error: 'std' namespace not found
error: 'vector' file not found
```

**Cause**: C++ standard library headers not accessible.

**Solution**:
- Verify toolchain is properly configured
- Check for compiler version mismatch
- Rebuild toolchain if necessary

## ACE Engine Specific Errors

### Pattern Not Found

**Error**:
```
error: no matching function for call to 'Pattern::Method'
```

**Cause**: Pattern class API change or missing include.

**Solution**:
- Check pattern header file for correct API
- Verify component_ng includes are correct
- Look for similar working code as reference

### Property Modifier Error

**Error**:
```
error: no member named 'SetWidth' in 'PropertyType'
```

**Cause**: Property layout or paint property incorrect.

**Solution**:
- Check property modifier pattern
- Verify layout_property.h or paint_property.h includes
- Reference similar component implementations

## Debugging Build Errors

### General Approach

1. **Read the error message**: Understand what's failing
2. **Check the location**: Find the file and line causing error
3. **Examine context**: Look at surrounding code
4. **Search for similar**: Find working code with similar pattern
5. **Verify dependencies**: Ensure required components are built

### Getting More Context

```bash
# Show lines around error in build log
grep -B 10 -A 10 "error:" out/<product>/build.log

# Find first occurrence of error
grep -n "error:" out/<product>/build.log | head -1

# Show compilation command for failing file
grep -B 5 "compiling .*/failing_file.cpp" out/<product>/build.log
```

### Isolating the Problem

```bash
# Build only the failing component
./build.sh --product-name rk3568 --build-target <failing_component>

# Clean and rebuild component
rm -rf out/<product>/logs/<component>/
./build.sh --product-name rk3568 --build-target <component>
```

## When All Else Fails

### Full Clean Build

```bash
# Remove all outputs
rm -rf out/

# Clean ccache
ccache -C

# Rebuild
./build.sh --product-name rk3568 --build-target ohos
```

### Check Environment

```bash
# Verify Python version
python3 --version

# Verify Node.js version
node --version

# Check environment variables
env | grep -E "PATH|NODE|PYTHON"
```

### Seek Help

- Check OpenHarmony documentation
- Search issue tracker
- Ask in community forums
- Review similar component implementations
