"""Step 1: Read text out of PDF, DOCX and TXT files."""
from pathlib import Path

import pdfplumber
from docx import Document


def extract_pdf(path: Path) -> str:
    """Read every page of a PDF and join the text."""
    pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")  # scanned pages return None
    return "\n".join(pages)


def extract_docx(path: Path) -> str:
    """Read paragraphs (and table cells) from a Word file."""
    doc = Document(path)
    parts = [p.text for p in doc.paragraphs]
    for table in doc.tables:
        for row in table.rows:
            parts.extend(cell.text for cell in row.cells)
    return "\n".join(parts)


def extract_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


EXTRACTORS = {".pdf": extract_pdf, ".docx": extract_docx, ".txt": extract_txt}


def extract_text(path) -> str:
    """Pick the right reader based on the file extension."""
    path = Path(path)
    reader = EXTRACTORS.get(path.suffix.lower())
    if reader is None:
        raise ValueError(f"Unsupported file type: {path.suffix}")
    return reader(path)


def load_resumes(folder) -> dict:
    """Return {filename: raw_text} for every supported file in a folder.
    A broken file is skipped with a warning instead of crashing the run."""
    resumes = {}
    for file in sorted(Path(folder).iterdir()):
        if file.suffix.lower() in EXTRACTORS:
            try:
                text = extract_text(file)
                if text.strip():
                    resumes[file.name] = text
                else:
                    print(f"[warn] {file.name}: no text found (scanned image PDF?)")
            except Exception as err:  # keep going if one file is corrupt
                print(f"[warn] could not read {file.name}: {err}")
    return resumes
