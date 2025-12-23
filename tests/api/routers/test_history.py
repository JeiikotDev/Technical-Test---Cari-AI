from collections.abc import Callable

from fastapi.testclient import TestClient


class TestHistoryEndpoint:
    def test_returns_previous_suggestions(
        self, client: TestClient, api_path: Callable[[str], str]
    ) -> None:
        first_response = client.post(
            api_path("/suggest"),
            json={"query": "¿Cómo cambio mi contraseña?"},
        )
        second_response = client.post(
            api_path("/suggest"),
            json={"query": "¿Cuál es el horario de atención?"},
        )

        history_response = client.get(api_path("/history"))

        assert first_response.status_code == second_response.status_code == 200
        assert history_response.status_code == 200

        history_items = history_response.json()
        assert len(history_items) == 2
        assert history_items[0]["query"] == "¿Cómo cambio mi contraseña?"
        assert history_items[0]["suggestion"].startswith("Puedes cambiar tu contraseña")
        assert history_items[1]["query"] == "¿Cuál es el horario de atención?"
        assert history_items[1]["suggestion"].startswith("Nuestro horario")
