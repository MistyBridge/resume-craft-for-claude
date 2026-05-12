#!/usr/bin/env python3
# @MistyBridge — Resume Craft for Claude Code
"""简历模块级字数统计与篇幅建议。

Usage:
  python scripts/word_counter.py <profile.json> [--target brief|normal|detailed]
"""

import argparse
import json
import re
import sys
from pathlib import Path

# 篇幅目标（汉字数）
TARGETS = {
    "brief":    (800, 1500),   # 简略
    "normal":   (1500, 3000),  # 正常
    "detailed": (3000, None),  # 详细（无上限）
}


def count_chinese(text: str) -> int:
    """统计汉字数量（不含标点和英文）。"""
    return len(re.findall(r"[一-鿿]", str(text)))


def count_section(section_data, key: str) -> int:
    """递归统计一个 Section 的汉字数。"""
    if section_data is None:
        return 0
    if isinstance(section_data, str):
        return count_chinese(section_data)
    if isinstance(section_data, list):
        total = 0
        for item in section_data:
            if isinstance(item, dict):
                for v in item.values():
                    total += count_section(v, "")
            elif isinstance(item, str):
                total += count_chinese(item)
        return total
    if isinstance(section_data, dict):
        return sum(count_section(v, k) for k, v in section_data.items())
    return 0


def analyze_profile(profile: dict) -> dict:
    """按模块统计字数。"""
    sections = {
        "个人总结":   profile.get("summary", {}),
        "工作经历":   profile.get("experience", []),
        "项目作品":   profile.get("projects", []),
        "技能描述":   profile.get("skills", {}),
        "教育背景":   profile.get("education", []),
        "其他信息":   profile.get("additional", {}),
    }

    result = {}
    total = 0
    for name, data in sections.items():
        cnt = count_section(data, name)
        result[name] = cnt
        total += cnt
    result["合计"] = total
    return result


def suggest(analysis: dict, target: str) -> str:
    """根据目标篇幅生成建议。"""
    total = analysis["合计"]
    low, high = TARGETS[target]
    lines = []

    if low and total < low:
        diff = low - total
        lines.append(f"⚠️ 篇幅不足：当前 {total} 字，目标 ≥{low} 字，缺少 {diff} 字")
        lines.append("建议详写或新增以下模块：")
        # 按占比排序建议
        sorted_mods = sorted(
            [(k, v) for k, v in analysis.items() if k != "合计"],
            key=lambda x: x[1]
        )
        for name, cnt in sorted_mods:
            if cnt > 0:
                lines.append(f"  - {name}（{cnt}字）: 可扩展至 {cnt + diff // len(sorted_mods)} 字")
    elif high and total > high:
        diff = total - high
        lines.append(f"⚠️ 篇幅超标：当前 {total} 字，目标 ≤{high} 字，超出 {diff} 字")
        lines.append("建议简写或删除以下模块：")
        sorted_mods = sorted(
            [(k, v) for k, v in analysis.items() if k != "合计"],
            key=lambda x: -x[1]
        )
        for name, cnt in sorted_mods:
            pct = cnt / max(total, 1) * 100
            lines.append(f"  - {name}（{cnt}字，{pct:.0f}%）: 可压缩至 {max(0, cnt - diff // max(len(sorted_mods), 1))} 字")
    else:
        range_str = f"{low}-{high}字" if high else f"≥{low}字"
        lines.append(f"✅ 篇幅达标：当前 {total} 字，目标 {range_str}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="简历模块级字数统计与篇幅建议"
    )
    parser.add_argument("profile", help="简历档案 JSON 路径")
    parser.add_argument("--target", "-t", choices=["brief", "normal", "detailed"],
                        default="normal", help="篇幅目标（默认 normal）")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    path = Path(args.profile)
    if not path.exists():
        sys.exit(f"Error: 档案不存在: {args.profile}")

    profile = json.loads(path.read_text(encoding="utf-8"))
    analysis = analyze_profile(profile)
    suggestion = suggest(analysis, args.target)

    if args.json:
        output = json.dumps({
            "target": args.target,
            "limits": {"low": TARGETS[args.target][0], "high": TARGETS[args.target][1]},
            "analysis": analysis,
            "suggestion": suggestion,
        }, ensure_ascii=False, indent=2)
    else:
        lines = ["## 模块字数统计"]
        for name, cnt in analysis.items():
            bar = "█" * min(cnt // 50, 30)
            lines.append(f"  {name:8s}  {cnt:>5d} 字  {bar}")
        lines.append(f"\n{suggestion}")
        output = "\n".join(lines)

    print(output)


if __name__ == "__main__":
    main()
