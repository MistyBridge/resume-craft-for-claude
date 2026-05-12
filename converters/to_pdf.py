#!/usr/bin/env python3
"""Convert HTML resume to PDF via WeasyPrint.

Usage:
  python converters/to_pdf.py resume.html resume.pdf
"""

import argparse
import sys
from pathlib import Path


def html_to_pdf(input_path: str, output_path: str) -> Path:
    """Convert HTML to PDF using WeasyPrint. Returns output path."""
    try:
        from weasyprint import HTML
    except ImportError:
        sys.exit(
            "Error: WeasyPrint is required. Install with: pip install weasyprint\n"
            "  Additional system deps may be needed:\n"
            "  Windows: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows\n"
            "  Mac:     brew install weasyprint\n"
            "  Linux:   sudo apt install weasyprint"
        )

    input_file = Path(input_path)
    if not input_file.exists():
        sys.exit(f"Error: Input file not found: {input_path}")

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    HTML(filename=str(input_file)).write_pdf(str(output_file))

    print(f"PDF exported: {output_file}")
    return output_file


def main():
    parser = argparse.ArgumentParser(
        description="Convert HTML resume to PDF via WeasyPrint"
    )
    parser.add_argument("input", help="Path to input HTML file")
    parser.add_argument("output", help="Path to output PDF file")
    args = parser.parse_args()
    html_to_pdf(args.input, args.output)


if __name__ == "__main__":
    main()
