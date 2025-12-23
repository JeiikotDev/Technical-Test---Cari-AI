from app.core.models import KnowledgeBaseEntry
from app.core.services.suggestion import SuggestionService
from app.core.stores import HistoryStore, KnowledgeBase


class TestSuggestionService:
    def test_suggest_uses_best_match_and_tracks_history(self) -> None:
        knowledge_base = KnowledgeBase(
            [
                KnowledgeBaseEntry(
                    question="¿Cómo cambio mi contraseña?",
                    answer="Visita configuración de perfil.",
                )
            ]
        )
        history_store = HistoryStore()
        suggestion_service = SuggestionService(
            knowledge_base=knowledge_base,
            history_store=history_store,
            fallback_message="Sin coincidencias.",
        )

        suggestion_text = suggestion_service.suggest("Como cambio mi contrasena")

        assert suggestion_text == "Visita configuración de perfil."
        history_records = suggestion_service.history()
        assert len(history_records) == 1
        assert history_records[0].query == "Como cambio mi contrasena"
        assert history_records[0].suggestion == "Visita configuración de perfil."

    def test_suggest_uses_fallback_when_no_match(self) -> None:
        empty_knowledge_base = KnowledgeBase([])
        history_store = HistoryStore()
        suggestion_service = SuggestionService(
            knowledge_base=empty_knowledge_base,
            history_store=history_store,
            fallback_message="Sin coincidencias.",
        )

        suggestion_text = suggestion_service.suggest("No existe")

        assert suggestion_text == "Sin coincidencias."
        assert history_store.list()[0].suggestion == "Sin coincidencias."

    def test_add_entry_and_knowledge_base(self) -> None:
        empty_knowledge_base = KnowledgeBase([])
        suggestion_service = SuggestionService(
            knowledge_base=empty_knowledge_base,
            history_store=HistoryStore(),
            fallback_message="Sin coincidencias.",
        )

        support_entry = KnowledgeBaseEntry(
            question="¿Cómo contacto soporte?",
            answer="Puedes escribir al chat o al correo soporte@cariai.com.",
        )
        returned_entry = suggestion_service.add_entry(support_entry)

        assert returned_entry == support_entry
        assert suggestion_service.knowledge_base() == [support_entry]
