import os

import pytest
from fastapi.testclient import TestClient

from app.core.models import KnowledgeBaseEntry
from app.main import create_app


def resolve_api_prefix() -> str:
    prefix = os.getenv("API_PREFIX", "/api/v1").strip()
    if prefix and not prefix.startswith("/"):
        prefix = f"/{prefix}"
    return prefix


@pytest.fixture()
def client() -> TestClient:
    knowledge_base_entries = [
        KnowledgeBaseEntry(
            question="¿Cómo cambio mi contraseña?",
            answer="Puedes cambiar tu contraseña en la sección de configuración de tu perfil.",
        ),
        KnowledgeBaseEntry(
            question="¿Cuál es el horario de atención?",
            answer="Nuestro horario es de lunes a viernes de 8 am a 5 pm.",
        ),
    ]
    app = create_app(
        entries=knowledge_base_entries,
        fallback_message="No encontré coincidencias.",
    )
    return TestClient(app)


@pytest.fixture()
def api_prefix() -> str:
    return resolve_api_prefix()


@pytest.fixture()
def api_path(api_prefix: str):
    def build_api_path(path: str) -> str:
        return f"{api_prefix}{path}" if api_prefix else path

    return build_api_path
