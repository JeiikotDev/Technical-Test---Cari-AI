from __future__ import annotations

from fastapi import Request

from app.core.services import SuggestionService


def get_suggestion_service(request: Request) -> SuggestionService:
    return request.app.state.suggestion_service
