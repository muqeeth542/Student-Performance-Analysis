from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from PyPDF2 import PdfReader


@dataclass
class DocumentChunk:
    chunk_id: str
    source: str
    text: str


def extract_pdf_text(file_path: Path) -> str:
    reader = PdfReader(str(file_path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)


def chunk_text(text: str, source: str, chunk_size: int, overlap: int) -> list[DocumentChunk]:
    text = " ".join(text.split())
    if not text:
        return []

    chunks: list[DocumentChunk] = []
    start = 0
    idx = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        raw = text[start:end]

        if end < len(text):
            last_space = raw.rfind(" ")
            if last_space > chunk_size // 2:
                end = start + last_space
                raw = text[start:end]

        cleaned = raw.strip()
        if cleaned:
            chunks.append(
                DocumentChunk(
                    chunk_id=f"{Path(source).stem}-{idx}",
                    source=source,
                    text=cleaned,
                )
            )
            idx += 1

        if end >= len(text):
            break

        start = max(0, end - overlap)

    return chunks
