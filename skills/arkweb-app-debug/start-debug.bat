@echo off
REM ArkWeb App Debug Tool - Quick Start Script for Windows
REM 自动使用 ohos-app-build-debug 检测到的环境启动调试
setlocal enabledelayedexpansion

echo ======================================
echo ArkWeb App Debug Tool - Quick Start
echo ======================================
echo.

REM 查找 ohos-app-build-debug
set "OHOS_SKILL=%USERPROFILE%\.claude\skills\ohos-app-build-debug"

if not exist "%OHOS_SKILL%" (
    echo [ERROR] ohos-app-build-debug skill not found
    echo Please install ohos-app-build-debug skill first:
    echo   https://github.com/your-repo/ohos-app-build-debug
    exit /b 1
)

echo [INFO] Found ohos-app-build-debug skill
echo.

REM 检查 DevEco Studio 环境
echo [INFO] Checking DevEco Studio environment...

REM 运行 ohos-app-build-debug env 并解析输出
"%OHOS_SKILL%\ohos-app-build-debug.exe" env > "%TEMP%\ohos_env.txt" 2>&1

findstr /C:"未检测到 DevEco Studio" "%TEMP%\ohos_env.txt" >nul
if %errorlevel% equ 0 (
    echo [ERROR] DevEco Studio not detected
    echo Please install DevEco Studio first:
    echo   https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/ide-download
    del "%TEMP%\ohos_env.txt"
    exit /b 1
)

echo [SUCCESS] DevEco Studio detected
echo.

REM 解析环境变量
echo [INFO] Setting up environment...

REM 从输出中提取工具路径
for /f "tokens=2*" %%a in ('findstr /C:"toolchains:" "%TEMP%\ohos_env.txt"') do set "TOOLCHAINS=%%b"
for /f "tokens=2*" %%a in ('findstr /C:"hdc:" "%TEMP%\ohos_env.txt"') do set "HDC_PATH=%%b"
for /f "tokens=2*" %%a in ('findstr /C:"hvigorw:" "%TEMP%\ohos_env.txt"') do set "HVIGORW_PATH=%%b"

if defined TOOLCHAINS (
    set "PATH=%TOOLCHAINS%;%PATH%"
    echo   [OK] Toolchains: %TOOLCHAINS%
)

if defined HDC_PATH (
    for %%i in ("%HDC_PATH%") do set "HDC_DIR=%%~dpi"
    set "PATH=%HDC_DIR%;%PATH%"
    echo   [OK] HDC: %HDC_DIR%"
)

if defined HVIGORW_PATH (
    for %%i in ("%HVIGORW_PATH%") do set "HVIGORW_DIR=%%~dpi"
    set "PATH=%HVIGORW_DIR%;%PATH%"
    echo   [OK] Hvigorw: %HVIGORW_DIR%"
)

set "HDC_SERVER_PORT=7035"

del "%TEMP%\ohos_env.txt"
echo.

REM 检查设备连接
echo [INFO] Checking device connection...

hdc list targets > "%TEMP%\devices.txt" 2>&1
set /p DEVICE_ID=<"%TEMP%\devices.txt"

if "%DEVICE_ID%"=="" (
    echo [WARN] No device found
    echo Please check:
    echo   1. Device is connected via USB
    echo   2. USB debugging is enabled
    echo   3. Device is authorized
    echo.
    set /p CONTINUE="Continue anyway? (y/N): "
    if /i not "!CONTINUE!"=="y" (
        del "%TEMP%\devices.txt"
        exit /b 1
    )
) else (
    echo [SUCCESS] Device found: %DEVICE_ID%
)

del "%TEMP%\devices.txt"
echo.

REM 启动调试
echo [INFO] Starting DevTools debugging session...
echo.

REM 获取脚本所在目录
set "SCRIPT_DIR=%~dp0"

cd /d "%SCRIPT_DIR%"
arkweb-app-debug.exe %*

endlocal
