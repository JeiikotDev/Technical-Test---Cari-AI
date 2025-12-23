from __future__ import annotations

from threading import Lock

from app.core.models.entities import HistoryRecord


class HistoryStore:
    """Thread-safe in-memory store for query/suggestion pairs."""

    def __init__(self) -> None:
        self._entries: list[HistoryRecord] = []
        self._lock = Lock()

    def add(self, query: str, suggestion: str) -> HistoryRecord:
        record = HistoryRecord(query=query, suggestion=suggestion)
        with self._lock:
            self._entries.append(record)
        return record

    def list(self) -> list[HistoryRecord]:
        with self._lock:
            return list(self._entries)
