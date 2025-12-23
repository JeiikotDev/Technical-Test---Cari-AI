from __future__ import annotations

from app.core.stores import HistoryStore, KnowledgeBase
from app.core.models.entities import HistoryRecord, KnowledgeBaseEntry


class SuggestionService:
    """Coordinates knowledge base lookup and history tracking."""

    def __init__(
        self,
        knowledge_base: KnowledgeBase,
        history_store: HistoryStore,
        fallback_message: str,
    ) -> None:
        self._knowledge_base = knowledge_base
        self._history_store = history_store
        self._fallback_message = fallback_message

    def suggest(self, query: str) -> str:
        suggestion = self._knowledge_base.best_match(query)
        if suggestion is None:
            suggestion = self._fallback_message

        self._history_store.add(query=query, suggestion=suggestion)
        return suggestion

    def history(self) -> list[HistoryRecord]:
        return self._history_store.list()

    def add_entry(self, entry: KnowledgeBaseEntry) -> KnowledgeBaseEntry:
        self._knowledge_base.add_entry(entry)
        return entry

    def knowledge_base(self) -> list[KnowledgeBaseEntry]:
        return self._knowledge_base.all_entries()
