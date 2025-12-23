from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import asdict
from difflib import SequenceMatcher
from pathlib import Path
from threading import Lock
from typing import Iterable, Optional

from app.core.models.entities import KnowledgeBaseEntry


class KnowledgeBase:
    """In-memory knowledge base backed by FAQ entries."""

    def __init__(self, entries: Iterable[KnowledgeBaseEntry]) -> None:
        self._entries = list(entries)
        self._lock = Lock()

    @classmethod
    def from_json(cls, path: Path) -> "KnowledgeBase":
        """Load entries from a JSON file containing pregunta/respuesta objects."""
        if not path.exists():
            raise FileNotFoundError(f"Knowledge base file not found: {path}")

        raw_entries = json.loads(path.read_text(encoding="utf-8"))
        entries = []
        for item in raw_entries:
            question = item.get("pregunta") or item.get("question")
            answer = item.get("respuesta") or item.get("answer")
            if question is None or answer is None:
                raise ValueError("Knowledge base entries require question/answer fields.")
            entries.append(KnowledgeBaseEntry(question=question, answer=answer))
        return cls(entries)

    def to_json(self) -> list[dict[str, str]]:
        """Return a serializable representation of the current entries."""
        with self._lock:
            return [asdict(entry) for entry in self._entries]

    def add_entry(self, entry: KnowledgeBaseEntry) -> None:
        """Add a new FAQ entry to the knowledge base."""
        with self._lock:
            self._entries.append(entry)

    def best_match(self, query: str, threshold: float = 0.55) -> Optional[str]:
        """Return the answer with the highest similarity over the threshold."""
        normalized_query = _normalize_text(query)
        best_ratio = 0.0
        best_answer: Optional[str] = None

        with self._lock:
            for entry in self._entries:
                ratio = SequenceMatcher(
                    a=normalized_query,
                    b=_normalize_text(entry.question),
                ).ratio()

                if ratio >= threshold and ratio > best_ratio:
                    best_ratio = ratio
                    best_answer = entry.answer

        return best_answer

    def all_entries(self) -> list[KnowledgeBaseEntry]:
        """Return a copy of all entries."""
        with self._lock:
            return list(self._entries)


def _normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    stripped_punctuation = re.sub(r"[^\w\s]", " ", ascii_text.lower())
    return " ".join(stripped_punctuation.split())
