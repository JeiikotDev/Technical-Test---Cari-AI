from collections.abc import Callable

from fastapi.testclient import TestClient


class TestKnowledgeEndpoint:
    def test_can_add_entry_and_use_it(
        self, client: TestClient, api_path: Callable[[str], str]
    ) -> None:
        add_entry_response = client.post(
            api_path("/knowledge"),
            json={
                "pregunta": "¿Cómo obtengo soporte?",
                "respuesta": "Puedes escribirnos al chat o al correo soporte@cariai.com.",
            },
        )
        assert add_entry_response.status_code == 201

        suggestion_response = client.post(
            api_path("/suggest"),
            json={"query": "¿Cómo obtengo soporte?"},
        )
        assert suggestion_response.status_code == 200
        assert suggestion_response.json()["suggestion"].startswith("Puedes escribirnos")
