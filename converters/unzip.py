#!/usr/bin/env python3
# @MistyBridge — Resume Craft for Claude Code
"""压缩包解析：支持 zip/rar/7z/tar/gz 解压，加密包自动跳过。

Usage:
  python converters/unzip.py <archive> [--out <dir>] [--list]
"""

import argparse
import shutil
import sys
import zipfile
from pathlib import Path

ARCHIVE_EXTS = {".zip", ".rar", ".7z", ".tar", ".gz", ".tgz", ".bz2", ".xz"}


def extract_zip(path: Path, out_dir: Path) -> list[Path]:
    """解压 .zip 文件。如加密则抛出异常。"""
    extracted = []
    with zipfile.ZipFile(path, "r") as zf:
        # 检测加密
        for info in zf.infolist():
            if info.flag_bits & 0x1:
                raise PermissionError(f"加密文件，已跳过: {path.name}")
        zf.extractall(out_dir)
        extracted = [out_dir / name for name in zf.namelist()]
    return extracted


def extract_shutil(path: Path, out_dir: Path) -> list[Path]:
    """通过 shutil 解压 .tar/.gz 等格式。"""
    shutil.unpack_archive(str(path), str(out_dir))
    return list(out_dir.rglob("*"))


def extract_rar_sevenzip(path: Path, out_dir: Path) -> list[Path]:
    """通过 7z 解压 .rar/.7z。需要安装 7-Zip。"""
    import subprocess
    try:
        result = subprocess.run(
            ["7z", "x", str(path), f"-o{out_dir}", "-y"],
            capture_output=True, text=True, timeout=120
        )
        if "Wrong password" in result.stderr or "password" in result.stderr.lower():
            raise PermissionError(f"加密文件，已跳过: {path.name}")
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())
        return list(out_dir.rglob("*"))
    except FileNotFoundError:
        raise RuntimeError(
            "7-Zip 未安装。\n"
            "  Windows: winget install 7zip\n"
            "  Mac:     brew install p7zip\n"
            "  Linux:   sudo apt install p7zip-full"
        )


def extract(path: Path, out_dir: Path) -> list[Path]:
    """自动选择解压方式。"""
    ext = path.suffix.lower()
    if ext == ".zip":
        return extract_zip(path, out_dir)
    elif ext in {".rar", ".7z"}:
        return extract_rar_sevenzip(path, out_dir)
    else:
        return extract_shutil(path, out_dir)


def main():
    parser = argparse.ArgumentParser(description="压缩包解析")
    parser.add_argument("archive", help="压缩包路径")
    parser.add_argument("--out", "-o", default=None, help="输出目录（默认同目录）")
    parser.add_argument("--list", "-l", action="store_true", help="仅列出内容")
    args = parser.parse_args()

    path = Path(args.archive)
    if not path.exists():
        sys.exit(f"Error: 文件不存在: {args.archive}")
    if path.suffix.lower() not in ARCHIVE_EXTS:
        sys.exit(f"不支持的格式: {path.suffix}。支持: {', '.join(sorted(ARCHIVE_EXTS))}")

    out_dir = Path(args.out) if args.out else path.parent / f"_extracted_{path.stem}"

    try:
        if args.list:
            print(f"[列出内容] {path.name} — 请解压以查看文件列表")
        else:
            files = extract(path, out_dir)
            print(f"[解压成功] {path.name} → {out_dir}")
            for f in sorted(files):
                print(f"  {f.relative_to(out_dir)}")
    except PermissionError as e:
        print(f"🔒 {e}")
    except Exception as e:
        print(f"[解压失败] {path.name}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
