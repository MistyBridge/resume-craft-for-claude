#!/usr/bin/env python3
# @MistyBridge — Resume Craft for Claude Code
"""ATS 分析器：JD关键词提取 + 简历匹配度计算 + 匹配报告生成。

Usage:
  python scripts/ats_analyzer.py <profile.json> <jd_text.txt> [--output report.md]
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

# 常见中文停用词
STOP_WORDS = set("的了吗呢吧啊是在有和与及或对对于关于因因为所以而但".split())


def extract_keywords(text: str) -> dict[str, list[str]]:
    """从 JD 文本提取结构化关键词。"""
    text_lower = text.lower()

    # 技术栈关键词（常见编程语言/框架/工具）
    tech_map = [
        "python", "java", "javascript", "typescript", "go", "rust", "c++", "c#",
        "react", "vue", "angular", "node.js", "django", "flask", "spring",
        "docker", "kubernetes", "k8s", "aws", "azure", "gcp", "ci/cd",
        "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
        "git", "linux", "shell", "terraform", "ansible",
    ]
    tech_found = [t for t in tech_map if t in text_lower]

    # 软技能/管理关键词
    soft_map = [
        "沟通", "协作", "团队", "管理", "领导", "项目管理", "敏捷", "scrum",
        "分析", "解决问题", "创新", "学习能力", "抗压",
    ]
    soft_found = [s for s in soft_map if s in text]

    # 学历/证书
    edu_pattern = re.findall(r"(本科|硕士|博士|MBA|CPA|CFA|FRM|PMP|AWS|Azure|GCP)", text)

    # 年限
    years = re.findall(r"(\d+)[\s-]*年", text)

    return {
        "tech_skills": tech_found,
        "soft_skills": soft_found,
        "education_certs": list(set(edu_pattern)),
        "years_required": years,
        "raw_length": len(text),
    }


def match_profile(profile: dict, jd_keywords: dict) -> dict:
    """计算简历与 JD 的匹配度。"""
    profile_text = json.dumps(profile, ensure_ascii=False).lower()
    results = {"total": 0, "hits": 0, "details": []}

    all_kw = (jd_keywords.get("tech_skills", []) +
              jd_keywords.get("soft_skills", []) +
              jd_keywords.get("education_certs", []))
    results["total"] = len(all_kw)

    for kw in all_kw:
        hit = kw in profile_text
        if hit:
            results["hits"] += 1
        results["details"].append({"keyword": kw, "hit": hit})

    results["match_rate"] = round(results["hits"] / max(results["total"], 1) * 100)
    return results


def generate_report(profile: dict, jd_keywords: dict, match_result: dict) -> str:
    """生成匹配报告 Markdown。"""
    name = profile.get("basics", {}).get("name", "未知")
    rate = match_result["match_rate"]

    lines = [
        f"# ATS 匹配报告",
        f"**候选人**: {name}",
        f"**匹配率**: {rate}%（{match_result['hits']}/{match_result['total']} 关键词命中）",
        "",
        "## JD 关键词提取",
        f"- 技术栈: {', '.join(jd_keywords['tech_skills']) or '(未检测到)'}",
        f"- 软技能: {', '.join(jd_keywords['soft_skills']) or '(未检测到)'}",
        f"- 学历/证书: {', '.join(jd_keywords['education_certs']) or '(未检测到)'}",
    ]
    if jd_keywords["years_required"]:
        lines.append(f"- 年限要求: {'/'.join(jd_keywords['years_required'])} 年")

    lines += [
        "",
        "## 命中明细",
        "| 关键词 | 状态 |",
        "|--------|------|",
    ]
    for item in match_result["details"]:
        status = "✅ 命中" if item["hit"] else "❌ 未命中"
        lines.append(f"| {item['keyword']} | {status} |")

    lines += [
        "",
        f"## 优化建议",
    ]
    missed = [i["keyword"] for i in match_result["details"] if not i["hit"]]
    if missed:
        lines.append(f"- 以下关键词未在简历中找到，建议补充相关经历: {', '.join(missed)}")
    if rate >= 80:
        lines.append("- 匹配度较高，可直接投递")
    elif rate >= 50:
        lines.append("- 匹配度中等，建议针对性补充 2-3 个核心关键词")
    else:
        lines.append("- 匹配度偏低，建议重新审视岗位匹配度或大幅补充缺失技能")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="ATS 分析器：JD关键词提取 + 简历匹配 + 报告生成"
    )
    parser.add_argument("profile", help="简历档案 JSON 路径")
    parser.add_argument("jd", help="JD 文本文件路径")
    parser.add_argument("--output", "-o", default=None, help="输出匹配报告路径")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()

    profile_path = Path(args.profile)
    jd_path = Path(args.jd)
    if not profile_path.exists():
        sys.exit(f"Error: 档案不存在: {args.profile}")
    if not jd_path.exists():
        sys.exit(f"Error: JD 文件不存在: {args.jd}")

    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    jd_text = jd_path.read_text(encoding="utf-8")

    jd_kw = extract_keywords(jd_text)
    match = match_profile(profile, jd_kw)
    report = generate_report(profile, jd_kw, match)

    if args.json:
        output = json.dumps({
            "jd_keywords": jd_kw,
            "match": match,
        }, ensure_ascii=False, indent=2)
    else:
        output = report

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"匹配报告已保存: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
