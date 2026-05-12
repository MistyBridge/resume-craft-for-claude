@echo off
REM =============================================================================
REM Resume Craft for Claude Code — Windows 环境检测脚本
REM 检测所有必需和可选工具的安装状态
REM =============================================================================
echo ========================================
echo   Resume Craft — 环境检测
echo ========================================
echo.

set OK=0
set WARN=0
set FAIL=0

echo [必需工具]
echo.

REM Python
python --version >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] Python — 未安装。请安装 Python 3.9+
    set /a FAIL+=1
) else (
    python -c "import sys; v=sys.version_info; exit(0 if v>=(3,9) else 1)" >nul 2>&1
    if errorlevel 1 (
        echo   [FAIL] Python 版本过低，需 3.9+
        set /a FAIL+=1
    ) else (
        for /f "tokens=2" %%v in ('python --version 2^>^&1') do echo   [ OK ] Python %%v
        set /a OK+=1
    )
)

REM Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] Node.js — 未安装。请安装 Node.js 18+
    set /a FAIL+=1
) else (
    for /f "tokens=1 delims=v" %%v in ('node --version 2^>^&1') do echo   [ OK ] Node.js v%%v
    set /a OK+=1
)

REM pip
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] pip — 未安装
    set /a FAIL+=1
) else (
    echo   [ OK ] pip
    set /a OK+=1
)

REM npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo   [FAIL] npm — 未安装
    set /a FAIL+=1
) else (
    echo   [ OK ] npm
    set /a OK+=1
)

echo.
echo [可选工具]
echo.

REM gh CLI
gh --version >nul 2>&1
if errorlevel 1 (
    echo   [WARN] gh CLI — 未安装。GitHub仓库抓取功能不可用。
    set /a WARN+=1
) else (
    echo   [ OK ] gh CLI
    set /a OK+=1
)

REM 7-Zip
7z --help >nul 2>&1
if errorlevel 1 (
    echo   [WARN] 7-Zip — 未安装。rar/7z 压缩包解析不可用。
    set /a WARN+=1
) else (
    echo   [ OK ] 7-Zip
    set /a OK+=1
)

REM Tesseract OCR
tesseract --version >nul 2>&1
if errorlevel 1 (
    echo   [WARN] Tesseract OCR — 未安装。图片文字识别不可用。
    set /a WARN+=1
) else (
    echo   [ OK ] Tesseract OCR
    set /a OK+=1
)

REM WeasyPrint
python -c "import weasyprint" >nul 2>&1
if errorlevel 1 (
    echo   [WARN] WeasyPrint — 未安装。pip install weasyprint
    set /a WARN+=1
) else (
    echo   [ OK ] WeasyPrint
    set /a OK+=1
)

echo.
echo ========================================
echo   结果: %OK% OK  %WARN% WARN  %FAIL% FAIL
echo ========================================

if %FAIL% gtr 0 (
    echo.
    echo 缺少必需工具，请安装后再运行 setup.bat。
    exit /b 1
)
echo.
echo 所有必需工具已就位，可以运行 setup.bat 安装依赖。
pause
