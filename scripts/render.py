#!/usr/bin/env python3
# @MistyBridge — Resume Craft
"""
Render a resume JSON profile into a self-contained HTML file using Jinja2.

Features:
  - 16+ discipline-specific template configs (auto-matched or manual)
  - 6 built-in themes with dynamic CSS custom properties
  - Adaptive section ordering and emphasis per discipline
  - Skill proficiency bars (optional)
"""

import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT_DIR / "templates"
SCRIPTS_DIR = ROOT_DIR / "scripts"


# ── Discipline System ──────────────────────────────────────────────────────

def load_disciplines() -> dict:
    """Load discipline template configurations."""
    path = TEMPLATE_DIR / "disciplines.json"
    if not path.exists():
        sys.exit(f"Error: disciplines.json not found at {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def match_discipline(profile: dict, user_target: str = "") -> str:
    """Match profile + target job to the best discipline template. Returns discipline key."""
    disciplines = load_disciplines()

    # Build search text: target job + profile data
    search_text = user_target.lower()
    if profile.get("basics", {}).get("title"):
        search_text += " " + profile["basics"]["title"].lower()
    if profile.get("meta", {}).get("target_roles"):
        search_text += " " + " ".join(profile["meta"]["target_roles"]).lower()
    # Add skill names
    skills = profile.get("skills", {}).get("hard_skills", [])
    search_text += " " + " ".join(s.get("name", "") for s in skills).lower()
    # Add experience titles
    for exp in profile.get("experience", []):
        search_text += " " + exp.get("title", "").lower()

    best_match = "通用"
    best_score = 0

    for disc_key, disc in disciplines.items():
        if disc_key.startswith("_"):
            continue
        keywords = disc.get("keywords", [])
        score = sum(1 for kw in keywords if kw.lower() in search_text)
        if score > best_score:
            best_score = score
            best_match = disc_key

    return best_match


# ── Theme System ──────────────────────────────────────────────────────────

def load_themes() -> dict:
    """Load all theme definitions."""
    themes_path = SCRIPTS_DIR / "themes.json"
    if not themes_path.exists():
        sys.exit(f"Error: themes.json not found at {themes_path}")
    with open(themes_path, "r", encoding="utf-8") as f:
        return json.load(f)


def should_show_skill_bars(profile: dict, discipline: dict) -> bool:
    """Determine if skill proficiency bars should be shown."""
    # Discipline config takes priority
    skill_display = discipline.get("skill_display", "tags")
    if skill_display == "bars":
        return True
    if skill_display == "tags":
        return False

    # Auto-detect from data
    skills = profile.get("skills", {}).get("hard_skills", [])
    if not skills:
        return False
    rated = sum(1 for s in skills if s.get("proficiency"))
    return rated >= len(skills) * 0.6


# ── Rendering ─────────────────────────────────────────────────────────────

def render(profile: dict, theme: dict, discipline: dict,
           template_name: str = "resume", show_bars: bool = False) -> str:
    """Render profile data + theme + discipline config into HTML."""
    try:
        from jinja2 import Environment, FileSystemLoader
    except ImportError:
        sys.exit("Error: Jinja2 is required. Install with: pip install jinja2")

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=False,
    )

    template_file = f"{template_name}.html"
    try:
        template = env.get_template(template_file)
    except Exception:
        available = [f.stem for f in TEMPLATE_DIR.glob("*.html")]
        sys.exit(
            f"Error: Template '{template_file}' not found.\n"
            f"Available: {available or 'none'}"
        )

    context = dict(profile)
    context["theme"] = theme
    context["discipline"] = discipline
    context["show_skill_bars"] = show_bars
    return template.render(**context)


def write_output(html: str, output_path: str) -> None:
    """Write rendered HTML, creating parent directories as needed."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def load_profile(profile_path: str) -> dict:
    """Load and validate the profile JSON file."""
    path = Path(profile_path)
    if not path.exists():
        sys.exit(f"Error: Profile file not found: {profile_path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        sys.exit(f"Error: Invalid JSON in profile: {e}")
    if "basics" not in data:
        sys.exit("Error: Profile missing required field: 'basics'")
    return data


# ── CLI ───────────────────────────────────────────────────────────────────

def main():
    themes = load_themes()
    disciplines = load_disciplines()
    theme_names = list(themes.keys())
    disc_names = [k for k in disciplines if not k.startswith("_")]

    parser = argparse.ArgumentParser(
        description="Render resume JSON profile to HTML with discipline-specific templates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Available themes:\n  " + "\n  ".join(
            f"{k:12s} — {v['name']}" for k, v in themes.items()
        ),
    )
    parser.add_argument("--profile", "-p", help="Path to profile JSON file")
    parser.add_argument("--output", "-o", help="Output HTML file path")
    parser.add_argument("--template", "-t", default="resume",
                        help="Template name (default: resume)")
    parser.add_argument("--theme", choices=theme_names,
                        help="Theme name. Uses discipline default if omitted.")
    parser.add_argument("--discipline", choices=disc_names,
                        help="Discipline template key. Auto-matched from profile if omitted.")
    parser.add_argument("--target", default="",
                        help="Target job title/description for better discipline matching")
    parser.add_argument("--skill-bars", action="store_true",
                        help="Show skill proficiency bars")
    parser.add_argument("--list-themes", action="store_true",
                        help="List all themes and exit")
    parser.add_argument("--list-disciplines", action="store_true",
                        help="List all disciplines and exit")

    args = parser.parse_args()

    if args.list_themes:
        print("Available themes:\n")
        for key, t in themes.items():
            print(f"  {key:12s}  {t['name']}")
            print(f"  {'':12s}  {t['description']}")
            print(f"  {'':12s}  Accent: {t['colors']['accent']}  |  Layout: {t['layout']['columns']}-column\n")
        return

    if args.list_disciplines:
        print("Available discipline templates:\n")
        for key in disc_names:
            d = disciplines[key]
            secs = " → ".join(d.get("sections", []))
            print(f"  {key:10s}  {d['name']}")
            print(f"  {'':10s}  Theme: {d.get('theme','?')}  |  Order: {secs}")
            print(f"  {'':10s}  {d['design_notes'][:80]}...\n")
        return

    if not args.profile or not args.output:
        sys.exit("Error: --profile and --output are required for rendering")

    profile = load_profile(args.profile)

    # Match discipline
    disc_key = args.discipline or match_discipline(profile, args.target)
    if disc_key not in disciplines:
        disc_key = "通用"
    discipline = disciplines[disc_key]

    # Select theme: explicit > discipline default > auto
    theme_name = args.theme or discipline.get("theme", "azure")
    if theme_name not in themes:
        theme_name = "azure"
    theme = themes[theme_name]

    show_bars = args.skill_bars or should_show_skill_bars(profile, discipline)

    html = render(profile, theme, discipline, args.template, show_bars)

    write_output(html, args.output)

    print(f"Rendered:  {args.output}")
    print(f"  Profile:     {args.profile}")
    print(f"  Discipline:  {disc_key} ({discipline['name']})")
    print(f"  Theme:       {theme_name} ({theme['name']})")
    print(f"  Sections:    {' → '.join(discipline['sections'])}")
    print(f"  Skill bars:  {'on' if show_bars else 'off'}")
    print(f"  Notes:       {discipline['design_notes'][:60]}...")


if __name__ == "__main__":
    main()
