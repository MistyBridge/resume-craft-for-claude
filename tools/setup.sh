#!/usr/bin/env bash
# =============================================================================
# Resume Craft for Claude Code — Linux/macOS 一键安装脚本
# 自动安装: Python依赖(jinja2/html2text/weasyprint) + Node.js依赖(docx/puppeteer)
# 用法: bash tools/setup.sh
# =============================================================================
set -e

echo "========================================"
echo "  简历 Skill — 工具依赖安装"
echo "========================================"
echo ""

echo "[1/3] 安装 Python 依赖..."
pip install -r "$(dirname "$0")/../requirements.txt"
echo "Python 依赖安装完毕。"

echo ""
echo "[2/3] 安装 Node.js 依赖..."
cd "$(dirname "$0")"
npm install
echo "Node.js 依赖安装完毕。"

echo ""
echo "[3/3] 验证安装..."
python3 -c "import jinja2; print('  jinja2: OK')" 2>/dev/null || echo "  jinja2: 未安装"
python3 -c "import html2text; print('  html2text: OK')" 2>/dev/null || echo "  html2text: 未安装"
python3 -c "import weasyprint; print('  weasyprint: OK')" 2>/dev/null || echo "  weasyprint: 未安装（PDF 可用 Node.js 替代）"
node -e "require('docx'); console.log('  docx (npm): OK')" 2>/dev/null || echo "  docx (npm): 未安装"
node -e "require('puppeteer'); console.log('  puppeteer: OK')" 2>/dev/null || echo "  puppeteer: 未安装"

echo ""
echo "========================================"
echo "  安装完毕"
echo "========================================"
