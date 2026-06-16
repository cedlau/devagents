"""Extract text from a PDF file, one page at a time, to a sibling .txt file.

Used by the `pdf-extraction` recipe to bypass LLM PDF-size limits by producing
a pre-extracted text file that can be read directly.
"""

import os
import sys
from pathlib import Path

import pypdf


def extract_pdf_to_text(pdf_path: str) -> Path:
    """Extract all pages of a PDF to a UTF-8 text file.

    Args:
        pdf_path: Path to the source PDF file.

    Returns:
        Path to the generated `-extracted.txt` file.

    Raises:
        FileNotFoundError: If ``pdf_path`` does not exist.
        pypdf.errors.PdfReadError: If the file cannot be parsed as a PDF.
    """
    source = Path(pdf_path)
    if not source.exists():
        raise FileNotFoundError(f"{source} not found.")

    output_txt = source.with_name(f"{source.stem}-extracted.txt")

    reader = pypdf.PdfReader(str(source))
    print(f"Total pages: {len(reader.pages)}")

    with output_txt.open("w", encoding="utf-8") as f:
        for i, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if text:
                f.write(f"\n--- Page {i} ---\n{text}")

    print(f"Full text extracted to {output_txt}")
    return output_txt


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_text.py <pdf_path>")
        sys.exit(1)

    try:
        extract_pdf_to_text(sys.argv[1])
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        sys.exit(1)
    except pypdf.errors.PdfReadError as exc:
        print(f"Error: failed to parse PDF — {exc}")
        sys.exit(1)
