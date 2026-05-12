#!/usr/bin/env python3
# @MistyBridge — Resume Craft for Claude Code
"""多模态文本提取：图片OCR + 音频转文字。

Usage:
  python converters/to_text.py <file> [--lang chi_sim]  → 输出提取的文本
"""

import argparse
import subprocess
import sys
from pathlib import Path

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".heic", ".gif", ".svg", ".tiff", ".bmp", ".webp"}
AUDIO_EXTS = {".mp3", ".m4a", ".wav", ".ogg", ".flac"}
SUPPORTED = IMAGE_EXTS | AUDIO_EXTS


def ocr_image(path: Path, lang: str = "chi_sim") -> str:
    """使用 Tesseract OCR 提取图片文字。需要安装 tesseract。"""
    try:
        result = subprocess.run(
            ["tesseract", str(path), "stdout", "-l", lang],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())
        text = result.stdout.strip()
        if not text:
            return "[未识别到文字]"
        return text
    except FileNotFoundError:
        return (
            "[OCR 不可用] Tesseract 未安装。\n"
            "  Windows: choco install tesseract  或  winget install tesseract\n"
            "  Mac:     brew install tesseract\n"
            "  Linux:   sudo apt install tesseract-ocr tesseract-ocr-chi-sim"
        )
    except Exception as e:
        return f"[OCR 失败] {e}"


def transcribe_audio(path: Path) -> str:
    """音频转文字占位。提示用户提供文字稿。"""
    return (
        f"[音频文件] {path.name}\n"
        "当前环境未配置语音识别引擎。请提供此音频的文字稿，"
        "或安装 whisper 后重试：pip install openai-whisper && whisper <file>"
    )


def main():
    parser = argparse.ArgumentParser(description="多模态文本提取：图片OCR + 音频转文字")
    parser.add_argument("file", help="输入文件路径")
    parser.add_argument("--lang", default="chi_sim", help="OCR 语言（默认 chi_sim）")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        sys.exit(f"Error: 文件不存在: {args.file}")

    ext = path.suffix.lower()
    if ext in IMAGE_EXTS:
        text = ocr_image(path, args.lang)
    elif ext in AUDIO_EXTS:
        text = transcribe_audio(path)
    else:
        sys.exit(f"不支持的文件类型: {ext}。支持: {', '.join(sorted(SUPPORTED))}")

    print(text)


if __name__ == "__main__":
    main()
