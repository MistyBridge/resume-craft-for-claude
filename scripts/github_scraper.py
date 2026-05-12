#!/usr/bin/env python3
# @MistyBridge — Resume Craft for Claude Code
"""GitHub 仓库项目经历抓取。通过 gh CLI 或 WebFetch 获取 README/技术栈/项目定位。

Usage:
  python scripts/github_scraper.py <owner/repo>   → 输出结构化项目摘要
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def fetch_via_gh(repo: str) -> dict:
    """通过 gh CLI 获取仓库信息。"""
    try:
        # 仓库基本信息
        result = subprocess.run(
            ["gh", "repo", "view", repo, "--json",
             "name,description,url,languages,stargazerCount,forkCount,createdAt,updatedAt"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())
        info = json.loads(result.stdout)

        # README 内容
        readme = subprocess.run(
            ["gh", "api", f"repos/{repo}/readme",
             "-H", "Accept: application/vnd.github.raw"],
            capture_output=True, text=True, timeout=30
        )

        summary = {
            "name": info.get("name", ""),
            "url": info.get("url", ""),
            "description": info.get("description", ""),
            "languages": [l["name"] for l in (info.get("languages", "[]") or [])],
            "stars": info.get("stargazerCount", 0),
            "created": info.get("createdAt", ""),
            "updated": info.get("updatedAt", ""),
            "readme_preview": readme.stdout[:1500] if readme.returncode == 0 else "",
        }
        return summary
    except FileNotFoundError:
        raise RuntimeError(
            "gh CLI 未安装。安装方式: https://cli.github.com/"
        )


def format_output(data: dict) -> str:
    """格式化为可读摘要。"""
    lines = [
        f"# {data['name']}",
        f"链接: {data['url']}",
        f"简介: {data['description'] or '(无)'}",
        f"技术栈: {', '.join(data['languages']) if data['languages'] else '(未知)'}",
        f"Star: {data['stars']} | 创建: {data['created']} | 更新: {data['updated']}",
        "",
        "## README 预览",
        data["readme_preview"] or "(无法获取)",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="GitHub 仓库项目经历抓取"
    )
    parser.add_argument("repo", help="owner/repo 格式的仓库名")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    parser.add_argument("--save", "-s", default=None, help="保存到文件")
    args = parser.parse_args()

    if not re.match(r"^[\w.-]+/[\w.-]+$", args.repo):
        sys.exit("Error: 格式应为 owner/repo，如: microsoft/vscode")

    try:
        data = fetch_via_gh(args.repo)
        if args.json:
            output = json.dumps(data, ensure_ascii=False, indent=2)
        else:
            output = format_output(data)

        if args.save:
            Path(args.save).write_text(output, encoding="utf-8")
            print(f"已保存至: {args.save}")
        else:
            print(output)
    except Exception as e:
        sys.exit(f"抓取失败: {e}")


if __name__ == "__main__":
    main()
