from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_suggestion_service
from app.core.models import KnowledgeBaseEntry, KnowledgeBaseItem
from app.core.services import SuggestionService

router = APIRouter()
SuggestionServiceDep = Annotated[SuggestionService, Depends(get_suggestion_service)]


@router.post(
    "/knowledge",
    response_model=KnowledgeBaseItem,
    status_code=status.HTTP_201_CREATED,
    summary="Add a FAQ entry",
)
def add_entry(
    payload: KnowledgeBaseItem,
    service: SuggestionServiceDep,
) -> KnowledgeBaseItem:
    entry = KnowledgeBaseEntry(question=payload.question, answer=payload.answer)
    service.add_entry(entry)
    return KnowledgeBaseItem.from_entry(entry)


@router.get(
    "/knowledge",
    response_model=list[KnowledgeBaseItem],
    status_code=status.HTTP_200_OK,
    summary="View the loaded knowledge base",
)
def list_entries(
    service: SuggestionServiceDep,
) -> list[KnowledgeBaseItem]:
    return [KnowledgeBaseItem.from_entry(entry) for entry in service.knowledge_base()]
