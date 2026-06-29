@echo off
chcp 65001 >nul 2>&1
setlocal EnableExtensions EnableDelayedExpansion

REM Windows reverse SSH setup for Windows-side USB HDC.
REM The tunnel exposes only Windows sshd on Linux loopback.

set REVERSE_SSH_PORT=2222
set WIN_SSH_PORT=22
set SSH_CONNECT_TIMEOUT=15
set MAX_RETRIES=5
set HDC_EXE=hdc

REM Replace these values before running the script.
set LINUX_USER=CHANGE_ME
set LINUX_IP=CHANGE_ME
set LINUX_SSH_PORT=22

echo ============================================
echo   Windows reverse SSH HDC setup
echo ============================================
echo.

REM Administrator check precedes validation but causes no system mutation.
powershell -NoProfile -Command "if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) { exit 1 }"
if errorlevel 1 (
    echo [ERROR] Run this script as Administrator.
    exit /b 1
)

REM Validate every required input before installing or changing services.
call :validate_config
if errorlevel 1 exit /b 1

call :validate_hdc
if errorlevel 1 exit /b 1

call :ensure_openssh_client
if errorlevel 1 exit /b 1

call :ensure_openssh_server
if errorlevel 1 exit /b 1

call :ensure_ssh_key
if errorlevel 1 exit /b 1

echo.
echo ============================================
echo [INFO] Ready to create the reverse SSH tunnel
echo   Target: %LINUX_USER%@%LINUX_IP%:%LINUX_SSH_PORT%
echo   Forward: Linux 127.0.0.1:%REVERSE_SSH_PORT% -^> Windows localhost:%WIN_SSH_PORT%
echo   HDC: executed on Windows through the SSH session; no HDC port forward
echo ============================================
echo.

set RETRY_COUNT=0
:reconnect
echo [INFO] Connecting... (%date% %time%)
echo [INFO] Enter host confirmation or credentials only in this interactive window.
ssh -N -T -o ConnectTimeout=%SSH_CONNECT_TIMEOUT% -o StrictHostKeyChecking=accept-new -o ServerAliveInterval=60 -o ServerAliveCountMax=3 -o ExitOnForwardFailure=yes -R 127.0.0.1:%REVERSE_SSH_PORT%:localhost:%WIN_SSH_PORT% -p %LINUX_SSH_PORT% %LINUX_USER%@%LINUX_IP%
set SSH_EXIT=%errorlevel%
set /a RETRY_COUNT+=1

echo.
echo [WARN] Tunnel exited with code !SSH_EXIT!; retry !RETRY_COUNT! of %MAX_RETRIES%.
call :show_tunnel_recovery
if !RETRY_COUNT! geq %MAX_RETRIES% (
    echo [BLOCKED] Reverse SSH did not recover after %MAX_RETRIES% attempts.
    if !SSH_EXIT! equ 0 exit /b 1
    exit /b !SSH_EXIT!
)
echo [INFO] Retrying in 5 seconds. Press Ctrl+C to stop.
timeout /t 5 /nobreak >nul
goto reconnect

:validate_config
if "%LINUX_USER%"=="CHANGE_ME" (
    echo [ERROR] Set LINUX_USER before running this script.
    exit /b 1
)
if "%LINUX_IP%"=="CHANGE_ME" (
    echo [ERROR] Set LINUX_IP before running this script.
    exit /b 1
)
if "%LINUX_USER%"=="" (
    echo [ERROR] LINUX_USER must not be empty.
    exit /b 1
)
if "%LINUX_IP%"=="" (
    echo [ERROR] LINUX_IP must not be empty.
    exit /b 1
)
powershell -NoProfile -Command "$ports=@(%LINUX_SSH_PORT%,%WIN_SSH_PORT%,%REVERSE_SSH_PORT%); if ($ports.Where({$_ -lt 1 -or $_ -gt 65535}).Count -ne 0) { exit 1 }"
if errorlevel 1 (
    echo [ERROR] SSH ports must be integers in the range 1-65535.
    exit /b 1
)
powershell -NoProfile -Command "$value=%MAX_RETRIES%; if ($value -lt 1 -or $value -gt 100) { exit 1 }"
if errorlevel 1 (
    echo [ERROR] MAX_RETRIES must be an integer in the range 1-100.
    exit /b 1
)
exit /b 0

:validate_hdc
if exist "%HDC_EXE%" goto hdc_found
where "%HDC_EXE%" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] HDC_EXE was not found: %HDC_EXE%
    echo [ERROR] Set HDC_EXE to hdc or the full hdc.exe path before system setup.
    exit /b 1
)
:hdc_found
echo [INFO] Checking Windows-side HDC inventory...
set "HDC_INVENTORY=%TEMP%\ohos_hdc_inventory_%RANDOM%_%RANDOM%.txt"
"%HDC_EXE%" list targets -v >"!HDC_INVENTORY!" 2>&1
set HDC_EXIT=!errorlevel!
type "!HDC_INVENTORY!"
if not "!HDC_EXIT!"=="0" (
    echo [ERROR] hdc list targets -v failed. Fix HDC before installing or changing OpenSSH.
    call :show_hdc_recovery
    del /q "!HDC_INVENTORY!" >nul 2>&1
    exit /b 1
)
findstr /I /L /C:"[Empty]" /C:"Unauthorized" /C:"Offline" "!HDC_INVENTORY!" >nul
if not errorlevel 1 (
    echo [BLOCKED] HDC cannot prove a ready device. The tunnel may be created for diagnosis, but do not mutate the device.
    call :show_hdc_recovery
    del /q "!HDC_INVENTORY!" >nul 2>&1
    exit /b 0
)
set CONNECTED_COUNT=0
for /f "delims=" %%C in ('powershell -NoProfile -Command "(Select-String -LiteralPath '!HDC_INVENTORY!' -SimpleMatch 'Connected').Count"') do set CONNECTED_COUNT=%%C
if not "!CONNECTED_COUNT!"=="1" (
    echo [BLOCKED] Expected exactly one Connected target but found !CONNECTED_COUNT!.
    echo [ACTION] Select an explicit connect-key before any mutating HDC command.
) else (
    echo [INFO] HDC command is available and exactly one Connected target is visible.
)
del /q "!HDC_INVENTORY!" >nul 2>&1
exit /b 0

:show_hdc_recovery
echo [ACTION] Check HDC_EXE and run hdc checkserver plus hdc list targets -v.
echo [ACTION] Check device power and boot, USB debugging, data cable, direct USB port, Windows driver, and trust authorization.
echo [ACTION] If USB enumeration works but the daemon fails, verify the intended board/product image contains a running HDC daemon and matches the host SDK/toolchains.
echo [ACTION] Preserve HDC/image evidence and obtain user approval before reflashing.
exit /b 0

:show_tunnel_recovery
echo [ACTION] Confirm this setup script is still running with the intended LINUX_USER, LINUX_IP, and SSH/reverse ports.
echo [ACTION] Check Linux sshd, AllowTcpForwarding, authorized_keys, network reachability, and firewall policy.
echo [ACTION] After SSH recovers, rerun hdc list targets -v and the hardware/image checks before device mutation.
exit /b 0

:ensure_openssh_client
where ssh >nul 2>&1
if not errorlevel 1 (
    echo [INFO] OpenSSH Client is installed.
    exit /b 0
)
echo [INFO] Installing OpenSSH Client...
powershell -NoProfile -Command "$ErrorActionPreference='Stop'; Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0 | Out-Null"
if errorlevel 1 (
    echo [ERROR] OpenSSH Client installation failed.
    exit /b 1
)
where ssh >nul 2>&1
if errorlevel 1 (
    echo [ERROR] ssh is still unavailable after installation.
    exit /b 1
)
exit /b 0

:ensure_openssh_server
sc query sshd >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing OpenSSH Server...
    powershell -NoProfile -Command "$ErrorActionPreference='Stop'; Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0 | Out-Null"
    if errorlevel 1 (
        echo [ERROR] OpenSSH Server installation failed.
        exit /b 1
    )
)
powershell -NoProfile -Command "$ErrorActionPreference='Stop'; Set-Service -Name sshd -StartupType Automatic; Start-Service -Name sshd; if ((Get-Service sshd).Status -ne 'Running') { throw 'sshd is not running' }"
if errorlevel 1 (
    echo [ERROR] Failed to configure or start sshd.
    exit /b 1
)
echo [INFO] OpenSSH Server is running. No broad Windows firewall rule was added for the loopback target.
exit /b 0

:ensure_ssh_key
if exist "%USERPROFILE%\.ssh\id_ed25519" (
    echo [INFO] SSH key already exists.
    exit /b 0
)
echo [INFO] Generating an SSH key...
if not exist "%USERPROFILE%\.ssh" mkdir "%USERPROFILE%\.ssh"
if errorlevel 1 (
    echo [ERROR] Failed to create the SSH directory.
    exit /b 1
)
ssh-keygen -t ed25519 -f "%USERPROFILE%\.ssh\id_ed25519" -N ""
if errorlevel 1 (
    echo [ERROR] SSH key generation failed.
    exit /b 1
)
echo [ACTION] Add this public key to the Linux user's authorized_keys:
type "%USERPROFILE%\.ssh\id_ed25519.pub"
exit /b 0
