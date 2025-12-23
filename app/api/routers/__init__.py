"""API routers package."""

from fastapi import APIRouter

from .history import router as history_router
from .knowledge import router as knowledge_router
from .suggest import router as suggest_router

router = APIRouter()
router.include_router(suggest_router)
router.include_router(history_router)
router.include_router(knowledge_router)

__all__ = ["router"]
