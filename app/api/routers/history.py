from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_suggestion_service
from app.core.models import HistoryItem
from app.core.services import SuggestionService

router = APIRouter()
SuggestionServiceDep = Annotated[SuggestionService, Depends(get_suggestion_service)]


@router.get(
    "/history",
    response_model=list[HistoryItem],
    status_code=status.HTTP_200_OK,
    summary="History of handled queries",
)
def history(
    service: SuggestionServiceDep,
) -> list[HistoryItem]:
    return [HistoryItem.from_record(record) for record in service.history()]
