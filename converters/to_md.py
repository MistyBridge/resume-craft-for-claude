#!/usr/bin/env python3
"""Convert HTML resume to Markdown via html2text.

Usage:
  python converters/to_md.py resume.html resume.md
"""

import argparse
import sys
from pathlib import Path


def html_to_md(input_path: str, output_path: str) -> Path:
    """Convert HTML to Markdown. Returns output path."""
    try:
        import html2text
    except ImportError:
        sys.exit(
            "Error: html2text is required. Install with: pip install html2text"
        )

    input_file = Path(input_path)
    if not input_file.exists():
        sys.exit(f"Error: Input file not found: {input_path}")

    with open(input_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = True
    converter.body_width = 0
    converter.unicode_snob = True
    converter.ignore_emphasis = False
    converter.skip_internal_links = True

    md_content = converter.handle(html_content)

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"MD exported: {output_file}")
    return output_file


def main():
    parser = argparse.ArgumentParser(
        description="Convert HTML resume to Markdown via html2text"
    )
    parser.add_argument("input", help="Path to input HTML file")
    parser.add_argument("output", help="Path to output MD file")
    args = parser.parse_args()
    html_to_md(args.input, args.output)


if __name__ == "__main__":
    main()
