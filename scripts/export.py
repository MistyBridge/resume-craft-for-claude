#!/usr/bin/env python3
"""Export HTML resume to MD / PDF.

Unified CLI entry point. Delegates to converters/ for each format.
DOCX is generated via the built-in docx skill (not pandoc).
"""

import argparse
import sys
from pathlib import Path

# Allow importing from sibling converters/
CONVERTERS_DIR = Path(__file__).resolve().parent.parent / "converters"
sys.path.insert(0, str(CONVERTERS_DIR))

from to_md import html_to_md


def html_to_pdf_wrapper(input_path: str, output_path: str):
    """Wrapper that tries weasyprint first, falls back to pdf skill hint."""
    try:
        from to_pdf import html_to_pdf
        html_to_pdf(input_path, output_path)
    except SystemExit:
        raise
    except ImportError:
        print(
            "WeasyPrint is not installed. Install with: pip install weasyprint\n"
            "Or use the built-in pdf skill to convert HTML → PDF."
        )
        sys.exit(1)


FORMAT_HANDLERS = {
    "md": html_to_md,
    "pdf": html_to_pdf_wrapper,
}


def main():
    parser = argparse.ArgumentParser(
        description="Export HTML resume to MD / PDF"
    )
    parser.add_argument(
        "format",
        choices=["md", "pdf"],
        help="Output format (docx is generated via built-in docx skill)",
    )
    parser.add_argument(
        "input",
        help="Path to input HTML file",
    )
    parser.add_argument(
        "output",
        help="Path to output file",
    )

    args = parser.parse_args()

    handler = FORMAT_HANDLERS[args.format]
    handler(args.input, args.output)


if __name__ == "__main__":
    main()
