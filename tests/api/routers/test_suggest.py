from typing import Callable

from fastapi.testclient import TestClient


class TestSuggestEndpoint:
    def test_returns_closest_answer(
        self, client: TestClient, api_path: Callable[[str], str]
    ) -> None:
        suggestion_response = client.post(
            api_path("/suggest"),
            json={"query": "¿Cómo cambio mi contraseña?"},
        )

        assert suggestion_response.status_code == 200
        assert suggestion_response.json()["suggestion"].startswith(
            "Puedes cambiar tu contraseña"
        )
