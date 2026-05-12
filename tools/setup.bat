@echo off
REM =============================================================================
REM Resume Craft for Claude Code — Windows 一键安装脚本
REM 自动安装: Python依赖(jinja2/html2text/weasyprint) + Node.js依赖(docx/puppeteer)
REM 用法: 双击运行 或 命令行执行 tools\setup.bat
REM =============================================================================
echo ========================================
echo   简历 Skill — 工具依赖安装
echo ========================================
echo.

echo [1/3] 安装 Python 依赖...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo Python 依赖安装失败，请检查 Python 是否已安装。
) else (
    echo Python 依赖安装完毕。
)

echo.
echo [2/3] 安装 Node.js 依赖...
cd /d "%~dp0"
if exist package.json (
    call npm install
    if errorlevel 1 (
        echo Node.js 依赖安装失败，请检查 Node.js 是否已安装。
    ) else (
        echo Node.js 依赖安装完毕。
    )
) else (
    echo tools/package.json 未找到，跳过。
)

echo.
echo [3/3] 验证安装...
python -c "import jinja2; print('  jinja2: OK')" 2>nul || echo   jinja2: 未安装
python -c "import html2text; print('  html2text: OK')" 2>nul || echo   html2text: 未安装
python -c "import weasyprint; print('  weasyprint: OK')" 2>nul || echo   weasyprint: 未安装（PDF 可用 Node.js 替代）
node -e "require('docx'); console.log('  docx (npm): OK')" 2>nul || echo   docx (npm): 未安装
node -e "require('puppeteer'); console.log('  puppeteer: OK')" 2>nul || echo   puppeteer: 未安装

echo.
echo ========================================
echo   安装完毕
echo ========================================
pause
