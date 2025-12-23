from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_suggestion_service
from app.core.models import HistoryItem
from app.core.services import SuggestionService

router = APIRouter()


@router.get(
    "/history",
    response_model=list[HistoryItem],
    status_code=status.HTTP_200_OK,
    summary="History of handled queries",
)
def history(
    service: SuggestionService = Depends(get_suggestion_service),
) -> list[HistoryItem]:
    return [HistoryItem.from_record(record) for record in service.history()]
