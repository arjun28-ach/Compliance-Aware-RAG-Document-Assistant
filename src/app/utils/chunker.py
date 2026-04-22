import re
from typing import List


class TextChunker:
    def __init__(self, chunk_size: int = 800, overlap: int = 120):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> List[str]:
        if not text or not text.strip():
            return []

        sections = self._split_by_headings(text)
        chunks: List[str] = []

        for section in sections:
            section = self._normalize(section)
            if not section:
                continue

            if len(section) <= self.chunk_size:
                chunks.append(section)
                continue

            chunks.extend(self._sliding_window(section))

        return [c for c in chunks if c.strip()]

    def _split_by_headings(self, text: str) -> List[str]:
        lines = text.splitlines()
        sections: List[str] = []
        current: List[str] = []

        for line in lines:
            raw = line.strip()

            if not raw:
                if current:
                    current.append("")
                continue

            if self._is_heading(raw):
                if current:
                    sections.append("\n".join(current).strip())
                    current = []
                current.append(raw)
            else:
                current.append(raw)

        if current:
            sections.append("\n".join(current).strip())

        return sections

    def _is_heading(self, line: str) -> bool:
        if len(line) < 3 or len(line) > 120:
            return False

        patterns = [
            r"^(chapter|section)\s+\d+",
            r"^\d+(\.\d+)*\s+[A-Z]",
            r"^[A-Z][A-Z0-9\s\-,/&()]{4,}$",
            r"^(abstract|introduction|conclusion|references|methodology|results|discussion)$",
        ]

        lower = line.lower()
        if any(re.match(p, line, flags=re.IGNORECASE) for p in patterns):
            return True

        upper_letters = sum(1 for ch in line if ch.isalpha() and ch.isupper())
        total_letters = sum(1 for ch in line if ch.isalpha())
        if total_letters > 0 and upper_letters / total_letters > 0.8:
            return True

        return lower in {
            "abstract",
            "introduction",
            "conclusion",
            "references",
            "results",
            "discussion",
        }

    def _sliding_window(self, text: str) -> List[str]:
        chunks: List[str] = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            if end >= len(text):
                break

            start += self.chunk_size - self.overlap

        return chunks

    def _normalize(self, text: str) -> str:
        text = text.replace("\u00ad", "")
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()