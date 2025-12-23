from __future__ import annotations

from dataclasses import dataclass


@dataclass
class KnowledgeBaseEntry:
    question: str
    answer: str


@dataclass
class HistoryRecord:
    query: str
    suggestion: str
