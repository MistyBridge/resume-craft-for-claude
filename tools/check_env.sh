#!/usr/bin/env bash
# =============================================================================
# Resume Craft for Claude Code — Linux/macOS 环境检测脚本
# 检测所有必需和可选工具的安装状态
# =============================================================================

echo "========================================"
echo "  Resume Craft — 环境检测"
echo "========================================"
echo ""

OK=0; WARN=0; FAIL=0

echo "[必需工具]"
echo ""

# Python
if command -v python3 &>/dev/null; then
    VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    MAJOR=$(echo "$VER" | cut -d. -f1)
    MINOR=$(echo "$VER" | cut -d. -f2)
    if [ "$MAJOR" -ge 3 ] && [ "$MINOR" -ge 9 ]; then
        echo "  [ OK ] Python $VER"
        ((OK++))
    else
        echo "  [FAIL] Python $VER — 需 3.9+"
        ((FAIL++))
    fi
else
    echo "  [FAIL] Python — 未安装"
    ((FAIL++))
fi

# Node.js
if command -v node &>/dev/null; then
    NVER=$(node -v)
    echo "  [ OK ] Node.js $NVER"
    ((OK++))
else
    echo "  [FAIL] Node.js — 未安装"
    ((FAIL++))
fi

# pip
if python3 -m pip --version &>/dev/null; then
    echo "  [ OK ] pip"
    ((OK++))
else
    echo "  [FAIL] pip — 未安装"
    ((FAIL++))
fi

# npm
if command -v npm &>/dev/null; then
    echo "  [ OK ] npm"
    ((OK++))
else
    echo "  [FAIL] npm — 未安装"
    ((FAIL++))
fi

echo ""
echo "[可选工具]"
echo ""

# gh CLI
if command -v gh &>/dev/null; then
    echo "  [ OK ] gh CLI"
    ((OK++))
else
    echo "  [WARN] gh CLI — GitHub仓库抓取不可用"
    ((WARN++))
fi

# 7-Zip
if command -v 7z &>/dev/null; then
    echo "  [ OK ] 7-Zip"
    ((OK++))
else
    echo "  [WARN] 7-Zip — rar/7z解压不可用"
    ((WARN++))
fi

# Tesseract OCR
if command -v tesseract &>/dev/null; then
    echo "  [ OK ] Tesseract OCR"
    ((OK++))
else
    echo "  [WARN] Tesseract OCR — 图片识别不可用"
    ((WARN++))
fi

# WeasyPrint
if python3 -c "import weasyprint" &>/dev/null; then
    echo "  [ OK ] WeasyPrint"
    ((OK++))
else
    echo "  [WARN] WeasyPrint — pip install weasyprint"
    ((WARN++))
fi

echo ""
echo "========================================"
echo "  结果: $OK OK  $WARN WARN  $FAIL FAIL"
echo "========================================"

if [ "$FAIL" -gt 0 ]; then
    echo ""
    echo "缺少必需工具，请安装后再运行 setup.sh。"
    exit 1
fi
echo ""
echo "所有必需工具已就位，可以运行 bash tools/setup.sh 安装依赖。"
