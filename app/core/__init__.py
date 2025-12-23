"""Core domain and service layer components."""

from .config import (
    DEFAULT_FALLBACK_SUGGESTION,
    KNOWLEDGE_BASE_PATH,
    Settings,
    get_settings,
)
from .stores import HistoryStore, KnowledgeBase
from .models import HistoryRecord, KnowledgeBaseEntry
from .services import SuggestionService

__all__ = [
    "DEFAULT_FALLBACK_SUGGESTION",
    "KNOWLEDGE_BASE_PATH",
    "Settings",
    "get_settings",
    "HistoryStore",
    "HistoryRecord",
    "KnowledgeBase",
    "KnowledgeBaseEntry",
    "SuggestionService",
]
