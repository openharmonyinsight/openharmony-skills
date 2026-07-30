@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>nul
REM Windows launcher for check_dict
REM - functionally probes for a REAL Python (skips the Microsoft Store stub alias)
REM - if real Python found  -> delegate to check_dict.py
REM - if no real Python     -> do a native dict/hilog check (no Python needed)

set "SCRIPT_DIR=%~dp0"

REM ===== find a REAL python (functional probe) =====
set "PY="
for %%C in (py python3 python) do (
  if not defined PY (
    "%%C" -c "import sys;sys.stdout.write('PYOK')" >"%TEMP%\_xts_pyprobe.txt" 2>nul
    findstr /c:"PYOK" "%TEMP%\_xts_pyprobe.txt" >nul 2>nul && set "PY=%%C"
  )
)
if exist "%TEMP%\_xts_pyprobe.txt" del "%TEMP%\_xts_pyprobe.txt" >nul 2>nul

if defined PY (
  "%PY%" "%SCRIPT_DIR%check_dict.py" %*
  exit /b !errorlevel!
)

REM ===== no python: native dict check =====
set "LOG_DIR=%~1"
if "%LOG_DIR%"=="" (
  echo 用法: check_dict.cmd ^<hilog日志目录^>
  exit /b 1
)
if not exist "%LOG_DIR%" (
  echo [error] 目录不存在: %LOG_DIR%
  exit /b 1
)

echo === 检查hilog日志目录: %LOG_DIR% ===
echo.

set N=0
for %%F in ("%LOG_DIR%\hilog.*.gz") do set /a N+=1
echo 1. hilog文件数量: %N%
if "%N%"=="0" (
  echo    [!] 未找到 hilog.*.gz 文件
) else (
  echo    [OK] 找到 %N% 个 hilog 文件
)
echo.

set "DICT="
for %%F in ("%LOG_DIR%\hilog_dict.*.zip") do if not defined DICT set "DICT=%%~fF"
if not defined DICT if exist "%LOG_DIR%\dict.zip" set "DICT=%LOG_DIR%\dict.zip"

echo 2. 检查dict文件...
if not defined DICT (
  echo    [X] 未找到dict文件（hilog_dict.*.zip / dict.zip）
  echo        没有dict文件hilogtool会超时无响应，请先从测试机获取dict
  exit /b 1
)
for %%F in ("%DICT%") do echo    [OK] 找到: %%~nxF
echo.

for %%I in ("%SCRIPT_DIR%..") do set "SKILL_DIR=%%~fI"
set "HILOGTOOL=%SKILL_DIR%\tools\hilogtool.exe"
set "OUTPUT_DIR=%LOG_DIR%_parsed"

echo 3. dict时间戳无需与hilog匹配（dict是密钥字典，与日志时间无关）
echo.
echo 4. 推荐解密命令（Windows原生，无需Python）:
echo    "%HILOGTOOL%" parse -i "%LOG_DIR%" -o "%OUTPUT_DIR%" -d "%DICT%"
echo.
echo    或用并行解密启动器（自动检测Python，无Python时直跑hilogtool）:
echo    "%SCRIPT_DIR%parallel_decrypt.cmd" "%LOG_DIR%"
echo.
echo === 检查完成 ===
echo.
echo [hint] 后续分析脚本（filter_hilog.py 等）需真正Python:
echo        https://www.python.org/downloads/  （勾选 Add to PATH）
echo        或: winget install Python.Python.3.12
