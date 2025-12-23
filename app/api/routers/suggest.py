from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_suggestion_service
from app.core.models import SuggestRequest, SuggestionResponse
from app.core.services import SuggestionService

router = APIRouter()


@router.post(
    "/suggest",
    response_model=SuggestionResponse,
    status_code=status.HTTP_200_OK,
    summary="Suggest an answer from the knowledge base",
)
def suggest(
    payload: SuggestRequest,
    service: SuggestionService = Depends(get_suggestion_service),
) -> SuggestionResponse:
    suggestion = service.suggest(payload.query)
    return SuggestionResponse(suggestion=suggestion)
