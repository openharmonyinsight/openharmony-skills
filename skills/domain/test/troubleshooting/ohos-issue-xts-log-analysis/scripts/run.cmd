@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>nul
REM Windows launcher for the pure-Python analysis/gate/validation scripts.
REM   Usage: run.cmd <script-stem> [args...]     e.g.  run.cmd filter_hilog -i hilog.txt --stats-only
REM                                              run.cmd preflight_gate <log-dir>
REM                                              run.cmd validate_report report.md module_run.log crash_dir
REM                                              run.cmd verify_dict_location <log-dir>
REM
REM Why this launcher exists: when `python3` resolves to the Microsoft Store stub
REM (WindowsApps\python3.exe), `python3 xxx.py` SILENTLY exits 0 with zero output in a
REM non-interactive terminal -- the script body never runs. For the decrypt step that
REM is mitigated by parallel_decrypt.cmd (which falls back to native hilogtool.exe).
REM But preflight_gate.py / filter_hilog.py / validate_report.py / verify_dict_location.py
REM are pure Python with NO native fallback, so on a stub machine they would silently
REM no-op: preflight_gate would return 0 (the hard gate would look "passed"!), filter_hilog
REM would emit no line-numbers/layer markers, validate_report would emit no checks. That
REM breaks the skill's own safety chain. This launcher FAILS LOUDLY (exit 1) instead of
REM letting the stub silently succeed, so the AI/user can detect the problem.
REM
REM On Linux/macOS there is no stub problem -- use `python3 scripts/<script>.py` directly.

set "SCRIPT_DIR=%~dp0"

REM ===== first arg is the script stem (without .py) =====
set "STEM=%~1"
if "%STEM%"=="" goto usage
shift /1

REM ===== find a REAL python (functional probe, not path heuristic) =====
REM the WindowsApps stub writes nothing to stdout, so the findstr check skips it.
set "PY="
for %%C in (py python3 python) do (
  if not defined PY (
    "%%C" -c "import sys;sys.stdout.write('PYOK')" >"%TEMP%\_xts_pyprobe.txt" 2>nul
    findstr /c:"PYOK" "%TEMP%\_xts_pyprobe.txt" >nul 2>nul && set "PY=%%C"
  )
)
if exist "%TEMP%\_xts_pyprobe.txt" del "%TEMP%\_xts_pyprobe.txt" >nul 2>nul

if not defined PY (
  echo [error] 未检测到真正的 Python（仅有 Microsoft Store 桩程序 python3.exe 或完全无 Python）。
  echo [error] 目标脚本 %STEM%.py 为纯 Python，无原生回退，无法在桩程序下运行。
  echo [error] 桩程序在非交互终端会静默退出、零输出 -- 若直接 `python3 %STEM%.py` 会看似"无反应"实则根本未执行。
  echo [error] 这会破坏流程安全链：preflight_gate 会静默"通过"、filter_hilog 无分层标记、validate_report 无校验。
  echo [error] 请安装真正的 Python： https://www.python.org/downloads/  （勾选 Add python.exe to PATH）
  echo [error] 或: winget install Python.Python.3.12
  exit /b 1
)

set "TARGET=%SCRIPT_DIR%%STEM%.py"
if not exist "%TARGET%" (
  echo [error] 脚本不存在: %TARGET%
  echo         run.cmd 的第一个参数是脚本名（不带 .py），如 filter_hilog / preflight_gate / validate_report / verify_dict_location
  exit /b 1
)

REM rebuild remaining args (shift past the stem); %* would re-include the stem, so loop-quote each remaining arg
set "ARGS="
:argloop
if "%~1"=="" goto argdone
set "ARGS=!ARGS! "%~1""
shift /1
goto argloop
:argdone

echo [info] Python: %PY%  ->  %STEM%.py
"%PY%" "%TARGET%" !ARGS!
exit /b %errorlevel%

:usage
echo 用法: run.cmd ^<script-stem^> [args...]
echo        第一个参数为 scripts/ 下的脚本名（不带 .py），其余参数原样透传。
echo 示例:
echo   run.cmd preflight_gate ^<日志目录^>
echo   run.cmd filter_hilog -i hilog.txt -d 02B2B --stats-only
echo   run.cmd validate_report report.md module_run.log crash_dir
echo   run.cmd verify_dict_location ^<日志目录^>
echo   run.cmd map_domain "@ohos.multimedia.media"
echo 注意: 仅 Windows 需用本启动器（绕过 python3 桩程序）；Linux/macOS 直接 python3 scripts/^<script^>.py 即可。
exit /b 1
