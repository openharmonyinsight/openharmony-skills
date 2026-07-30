@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>nul
REM Windows launcher for parallel_decrypt
REM - functionally probes for a REAL Python (skips the Microsoft Store stub alias)
REM - if real Python found  -> delegate to parallel_decrypt.py (parallel + cache)
REM - if no real Python     -> run hilogtool.exe natively (zero Python needed)
REM Why a launcher, not an in-script check: the WindowsApps python3.exe stub never
REM launches an interpreter in non-interactive shells, so any .py self-check would
REM never execute (the script body simply does not run -> zero output).

set "SCRIPT_DIR=%~dp0"

REM ===== find a REAL python (functional probe, not path heuristic) =====
set "PY="
for %%C in (py python3 python) do (
  if not defined PY (
    "%%C" -c "import sys;sys.stdout.write('PYOK')" >"%TEMP%\_xts_pyprobe.txt" 2>nul
    findstr /c:"PYOK" "%TEMP%\_xts_pyprobe.txt" >nul 2>nul && set "PY=%%C"
  )
)
if exist "%TEMP%\_xts_pyprobe.txt" del "%TEMP%\_xts_pyprobe.txt" >nul 2>nul

if defined PY (
  echo [info] Python: %PY%
  "%PY%" "%SCRIPT_DIR%parallel_decrypt.py" %*
  exit /b !errorlevel!
)

REM ===== no real python: fall back to native hilogtool.exe =====
echo [warn] 未检测到真正的 Python（仅有 Microsoft Store 桩程序 python3.exe 或完全无 Python）
echo [warn] 桩程序在非交互终端会静默退出、零输出，导致 .py 脚本看似“无反应”
echo [warn] 已切换为直接调用 hilogtool.exe 原生解密（无需 Python）
echo.

set "LOG_DIR=%~1"
if "%LOG_DIR%"=="" (
  echo 用法: parallel_decrypt.cmd ^<hilog日志目录^> [输出目录] [dict文件]
  echo        有真正 Python 时，本启动器会自动改用 parallel_decrypt.py 获得并行/缓存
  exit /b 1
)
if not exist "%LOG_DIR%" (
  echo [error] 目录不存在: %LOG_DIR%
  exit /b 1
)

for %%I in ("%SCRIPT_DIR%..") do set "SKILL_DIR=%%~fI"
set "HILOGTOOL=%SKILL_DIR%\tools\hilogtool.exe"
REM honor explicit hilogtool path passed as 5th arg (same position parallel_decrypt.py uses)
if not "%~5"=="" if exist "%~5" set "HILOGTOOL=%~5"
if not exist "%HILOGTOOL%" (
  echo [error] hilogtool.exe 未找到: %HILOGTOOL%
  echo         可在命令行第5参数显式传入 hilogtool.exe 绝对路径
  exit /b 1
)

set "OUTPUT_DIR=%~2"
if "%OUTPUT_DIR%"=="" set "OUTPUT_DIR=%LOG_DIR%_parsed"

set "DICT=%~3"
if "%DICT%"=="" (
  for %%F in ("%LOG_DIR%\hilog_dict.*.zip") do if not defined DICT set "DICT=%%~fF"
  if not defined DICT if exist "%LOG_DIR%\dict.zip" set "DICT=%LOG_DIR%\dict.zip"
)
if not defined DICT (
  echo [error] 未找到 dict 文件（hilog_dict.*.zip / dict.zip）
  echo         请确认 %LOG_DIR% 下存在字典文件，否则 hilogtool 会超时无响应
  exit /b 1
)

if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

echo [info] hilogtool: %HILOGTOOL%
echo [info] 输入: %LOG_DIR%
echo [info] 输出: %OUTPUT_DIR%
echo [info] dict:  %DICT%
echo.

"%HILOGTOOL%" parse -i "%LOG_DIR%" -o "%OUTPUT_DIR%" -d "%DICT%"
set "RC=!errorlevel!"

echo.
if "%RC%"=="0" (
  echo [ok] 解密完成，输出: %OUTPUT_DIR%
  echo [hint] 后续 filter_hilog.py / validate_report.py 等分析脚本仍需真正的 Python
  echo         建议安装: https://www.python.org/downloads/  （勾选 Add python.exe to PATH）
  echo         或: winget install Python.Python.3.12
) else (
  echo [error] hilogtool 解密失败，退出码 %RC%
)
exit /b %RC%
