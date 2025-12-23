from app.core.models.entities import HistoryRecord
from app.core.stores.history import HistoryStore


class TestHistoryStore:
    def test_add_and_list_returns_copy(self) -> None:
        store = HistoryStore()

        password_reset_record = store.add(
            query="¿Cómo cambio mi contraseña?",
            suggestion="Puedes cambiar tu contraseña desde configuración.",
        )
        support_hours_record = store.add(
            query="¿Cuál es el horario de atención?",
            suggestion="Nuestro horario es de lunes a viernes.",
        )

        history_records = store.list()

        assert history_records == [password_reset_record, support_hours_record]
        history_records.append(
            HistoryRecord(
                query="¿Cómo contacto soporte?",
                suggestion="Puedes escribir al chat de soporte.",
            )
        )
        assert store.list() == [password_reset_record, support_hours_record]
