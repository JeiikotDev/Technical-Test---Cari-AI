from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from app.api import router
from app.core.config import Settings, get_settings
from app.core.stores import HistoryStore, KnowledgeBase
from app.core.models import KnowledgeBaseEntry
from app.core.services import SuggestionService


def configure_middleware(fastapi_app: FastAPI, settings: Settings) -> None:
    if settings.env == "dev":
        origins = ["*"]
    else:
        origins = settings.cors_origins

    if origins:
        fastapi_app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    fastapi_app.add_middleware(GZipMiddleware)


def configure_routers(fastapi_app: FastAPI, settings: Settings) -> None:
    prefix = settings.api_v1_prefix
    fastapi_app.include_router(router, prefix=prefix)


def create_app(
    *,
    entries: list[KnowledgeBaseEntry] | None = None,
    knowledge_base_path: Path | None = None,
    fallback_message: str | None = None,
    settings: Settings | None = None,
) -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = settings or get_settings()
    prefix = settings.api_v1_prefix
    effective_path = knowledge_base_path or settings.knowledge_base_path
    effective_fallback = fallback_message or settings.fallback_message
    knowledge_base = (
        KnowledgeBase(entries)
        if entries is not None
        else KnowledgeBase.from_json(effective_path)
    )
    history_store = HistoryStore()
    suggestion_service = SuggestionService(
        knowledge_base=knowledge_base,
        history_store=history_store,
        fallback_message=effective_fallback,
    )

    app = FastAPI(
        title="Cari AI - FAQ Suggestions",
        version="0.1.0",
        description="Lightweight service that suggests answers from a FAQ knowledge base.",
        docs_url=f"{prefix}/docs" if settings.docs_enabled else None,
        redoc_url=f"{prefix}/redoc" if settings.docs_enabled else None,
        openapi_url=f"{prefix}/openapi.json" if settings.docs_enabled else None,
    )

    app.state.suggestion_service = suggestion_service
    app.state.history_store = history_store
    app.state.knowledge_base = knowledge_base

    configure_middleware(app, settings)
    configure_routers(app, settings)
    return app


app = create_app()
