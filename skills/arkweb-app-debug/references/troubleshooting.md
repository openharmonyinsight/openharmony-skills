# ArkWeb Debug Tool - Troubleshooting Guide

## Common Problems and Solutions

---

### 1. Device Connection Issues

#### Problem: "No device available"

**Symptoms:**
```
Error: No device available
```

**Diagnosis:**
```bash
# Check if HDC sees the device
hdc list targets
```

**Solutions:**

1. **Check USB connection**
   - Ensure device is connected via USB
   - Try different USB port
   - Check USB cable is data-capable (not charge-only)

2. **Restart HDC server**
   ```bash
   hdc kill
   hdc start
   hdc list targets
   ```

3. **Verify device debugging mode**
   - Go to Settings > About Phone
   - Tap "Build Number" 7 times to enable Developer Options
   - Enable "USB Debugging" in Developer Options

4. **Authorize device**
   - Check device screen for debugging authorization prompt
   - Enable "Always allow from this computer"

---

### 2. Socket Not Found

#### Problem: "Socket not found within timeout"

**Symptoms:**
```
Warning: Socket not found within timeout
Error: Failed to create port forward
```

**Root Causes:**
- Application hasn't created debugging socket yet
- Application doesn't have debugging enabled
- Web component hasn't rendered

**Diagnosis:**
```bash
# Check if socket exists
hdc shell "cat /proc/net/unix" | grep webview_devtools_remote

# Check if app is running
hdc shell "ps -A" | grep your.package.name
```

**Solutions:**

1. **Verify application code**
   ```typescript
   // Must be in aboutToAppear()
   aboutToAppear() {
     webview.WebviewController.setWebDebuggingAccess(true);
   }
   ```

2. **Increase timeout**
   ```bash
   arkweb-app-debug start --package com.example.app --socket-timeout 30
   ```

3. **Manually trigger Web component render**
   - Navigate to a URL in the app
   - Ensure Web component is visible

4. **Check for application crashes**
   ```bash
   # Check app logs
   hdc shell "hilog -x | grep your.package.name"

   # Check if app process exists
   hdc shell "ps -A" | grep your.package.name
   ```

---

### 3. Port Forward Failures

#### Problem: "Failed to create port forward"

**Symptoms:**
```
Error: Failed to create port forward
```

**Diagnosis:**
```bash
# Check existing port forwards
hdc fport ls

# Try manual creation
hdc fport tcp:9222 localabstract:socket_name
```

**Solutions:**

1. **Remove old port forwards**
   ```bash
   hdc fport rm tcp:9222
   arkweb-app-debug cleanup
   ```

2. **Check for port conflicts**
   ```bash
   # Check if port is in use
   lsof -i :9222  # macOS/Linux
   netstat -an | grep 9222  # Windows/Linux
   ```

3. **Verify HDC command format**
   ```bash
   # Correct format:
   hdc fport tcp:9222 localabstract:socket_name

   # Wrong format (will fail):
   hdc fport tcplocal:9222 ...
   ```

4. **Use different port**
   ```bash
   arkweb-app-debug start --package com.example.app --local-port 9223
   ```

---

### 4. Device Screen Locked

#### Problem: "Error Code:10106102 The device screen is locked"

**Symptoms:**
```
error: failed to start ability.
Error Code:10106102  Error Message:The device screen is locked
```

**Solutions:**

1. **Unlock device screen**
   - Simply unlock the device
   - Disable auto-lock during debugging sessions

2. **Disable secure lock**
   - Settings > Security & Location > Screen lock
   - Set to "None" or "Swipe" during development

---

### 5. Application Not Installed

#### Problem: "App not installed and no HAP path provided"

**Symptoms:**
```
Error: App not installed and no HAP path provided
```

**Solutions:**

1. **Provide HAP file**
   ```bash
   arkweb-app-debug start --package com.example.app --hap ./app.hap
   ```

2. **Install manually first**
   ```bash
   hdc install entry/build/default/outputs/default/entry-default-signed.hap
   arkweb-app-debug start --package com.example.app
   ```

---

### 6. DevTools Connection Failed

#### Problem: "Could not verify DevTools connection"

**Symptoms:**
```
Warning: Could not verify DevTools connection
```

**Diagnosis:**
```bash
# Test connection manually
curl http://localhost:9222/json

# Expected output: JSON array with page info
```

**Solutions:**

1. **Verify port forward**
   ```bash
   hdc fport ls
   # Should show: tcp:9222 localabstract:socket_name
   ```

2. **Check if app is still running**
   ```bash
   hdc shell "ps -A" | grep your.package.name
   ```

3. **Wait longer after port forward**
   - The socket needs time to initialize
   - Try increasing: `--socket-init-wait 5`

4. **Open DevTools manually**
   - Go to `chrome://inspect/#devices`
   - Look for your device and page
   - Click "inspect"

---

### 7. Chrome Won't Open Automatically

#### Problem: `--open-chrome` doesn't work

**Symptoms:**
```
Warning: Could not open Chrome automatically
```

**Solutions:**

1. **Manually open DevTools**
   ```bash
   # Get DevTools URL
   curl http://localhost:9222/json

   # Open in Chrome
   chrome http://localhost:9222
   # or
   google-chrome http://localhost:9222
   ```

2. **Use chrome://inspect**
   - Open Chrome
   - Navigate to `chrome://inspect/#devices`
   - Find your device and click "inspect"

3. **Set Chrome path explicitly**
   ```bash
   export CHROME_BIN="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
   arkweb-app-debug start --package com.example.app --open-chrome
   ```

---

### 8. Application Won't Start

#### Problem: "Failed to start app"

**Diagnosis:**
```bash
# Try manual start
hdc shell aa start -a EntryAbility -b com.example.app -m entry

# Check app status
hdc shell aa dump -a com.example.app
```

**Common Causes:**

1. **Wrong ability name**
   ```bash
   # Find correct ability name
   hdc shell bm dump -n com.example.app | grep ability
   ```

2. **Application crashed on startup**
   ```bash
   # Check logs
   hdc shell "hilog -x" | grep -i error
   ```

3. **Module name incorrect**
   - Default is usually "entry"
   - Check your application structure

---

### 9. HDC Command Not Found

#### Problem: "hdc: command not found"

**Solutions:**

1. **Install HDC**
   - Download from HarmonyOS SDK
   - Add to PATH

2. **Add to PATH manually**
   ```bash
   # Temporary
   export PATH="/path/to/hdc:$PATH"

   # Permanent (add to ~/.bashrc or ~/.zshrc)
   echo 'export PATH="/path/to/hdc:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

3. **Specify HDC path**
   ```bash
   arkweb-app-debug start --package com.example.app --hdc-cmd /path/to/hdc
   ```

---

### 10. Permission Errors

#### Problem: Permission denied when accessing files

**Solutions:**

1. **Fix state file permissions**
   ```bash
   mkdir -p ~/.arkweb-app-debug
   chmod 755 ~/.arkweb-app-debug
   ```

2. **Check Python environment**
   ```bash
   # Use virtual environment
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate  # Windows

   pip install -e .
   ```

---

### 11. Python Version Issues

#### Problem: "Python 3.8+ required"

**Solutions:**

1. **Check Python version**
   ```bash
   python --version
   # or
   python3 --version
   ```

2. **Install correct Python version**
   - macOS: `brew install python@3.9`
   - Ubuntu: `sudo apt install python3.9`
   - Windows: Download from python.org

3. **Use specific Python version**
   ```bash
   python3.9 -m pip install -e .
   ```

---

## Debug Mode

Enable verbose logging:

```bash
# Enable debug logging
arkweb-app-debug --verbose start --package com.example.app

# Or set environment variable
export ARKWEB_DEBUG=1
arkweb-app-debug start --package com.example.app
```

---

## Clean Reset

If everything fails, do a complete reset:

```bash
# 1. Stop all sessions
arkweb-app-debug stop-all

# 2. Clean up everything
arkweb-app-debug cleanup --all

# 3. Remove state files
rm -rf ~/.arkweb-app-debug

# 4. Remove all HDC port forwards
hdc fport rm tcp:9220
hdc fport rm tcp:9221
# ... repeat for all ports in range 9220-9299

# 5. Restart HDC
hdc kill
hdc start

# 6. Reinstall tool
pip uninstall arkweb-app-debug
pip install -e .

# 7. Try again
arkweb-app-debug start --package com.example.app
```

---

## Getting Help

If issues persist:

1. **Check logs**: Enable verbose mode and review output
2. **Verify prerequisites**: Ensure all requirements are met
3. **Test manually**: Try manual debugging steps
4. **Check documentation**: Review other guides in `docs/`

---

## Common Pitfalls

### ❌ Wrong: Debugging NOT enabled in app

```typescript
// Missing setWebDebuggingAccess()
aboutToAppear() {
  // Nothing here
}
```

### ✅ Correct: Enable debugging

```typescript
aboutToAppear() {
  webview.WebviewController.setWebDebuggingAccess(true);
}
```

---

### ❌ Wrong: Using instance method

```typescript
this.controller.setWebDebuggingAccess(true);  // Wrong
```

### ✅ Correct: Using static method

```typescript
webview.WebviewController.setWebDebuggingAccess(true);  // Correct
```

---

### ❌ Wrong: Wrong parameter type

```typescript
webview.WebviewController.setWebDebuggingAccess(8888);  // Wrong - number
```

### ✅ Correct: Boolean parameter

```typescript
webview.WebviewController.setWebDebuggingAccess(true);  // Correct - boolean
```

---

### ❌ Wrong: Wrong lifecycle method

```typescript
onPageShow() {
  webview.WebviewController.setWebDebuggingAccess(true);  // Too late
}
```

### ✅ Correct: Use aboutToAppear

```typescript
aboutToAppear() {
  webview.WebviewController.setWebDebuggingAccess(true);  // Before render
}
```

---

## Timing Requirements Summary

| Action | Wait Time | Critical |
|--------|-----------|----------|
| After app start | 10 seconds | ✅ YES |
| After port forward | 2 seconds | ✅ YES |
| Socket find retry | 2 seconds | ✅ YES |
| Socket find timeout | 15 seconds | ✅ YES |

⚠️ **DO NOT reduce these times** - they are based on actual testing

---

**Last Updated**: 2025-02-07
**Tool Version**: 2.1.0
