import json

import pytest

from app.core.models import KnowledgeBaseEntry
from app.core.stores.knowledge_base import KnowledgeBase, _normalize_text


class TestKnowledgeBaseFromJson:
    def test_missing_file_raises(self, tmp_path) -> None:
        missing_path = tmp_path / "missing.json"

        with pytest.raises(FileNotFoundError, match="Knowledge base file not found"):
            KnowledgeBase.from_json(missing_path)

    def test_invalid_entry_raises(self, tmp_path) -> None:
        knowledge_base_path = tmp_path / "kb.json"
        knowledge_base_path.write_text(
            json.dumps([{"pregunta": "Hola"}]),
            encoding="utf-8",
        )

        with pytest.raises(ValueError, match="question/answer"):
            KnowledgeBase.from_json(knowledge_base_path)

    def test_parses_spanish_fields(self, tmp_path) -> None:
        knowledge_base_path = tmp_path / "kb.json"
        knowledge_base_path.write_text(
            json.dumps([{"pregunta": "Horario", "respuesta": "Lunes a viernes."}]),
            encoding="utf-8",
        )

        knowledge_base = KnowledgeBase.from_json(knowledge_base_path)

        assert knowledge_base.all_entries() == [
            KnowledgeBaseEntry(question="Horario", answer="Lunes a viernes."),
        ]

    def test_parses_english_fields(self, tmp_path) -> None:
        knowledge_base_path = tmp_path / "kb.json"
        knowledge_base_path.write_text(
            json.dumps([{"question": "Support", "answer": "Email us."}]),
            encoding="utf-8",
        )

        knowledge_base = KnowledgeBase.from_json(knowledge_base_path)

        assert knowledge_base.all_entries() == [
            KnowledgeBaseEntry(question="Support", answer="Email us."),
        ]


class TestKnowledgeBaseOperations:
    def test_to_json_returns_dicts(self) -> None:
        knowledge_base = KnowledgeBase(
            [
                KnowledgeBaseEntry(
                    question="¿Cómo cambio mi contraseña?",
                    answer="Puedes cambiarla desde configuración.",
                ),
                KnowledgeBaseEntry(
                    question="¿Cuál es el horario de atención?",
                    answer="Lunes a viernes.",
                ),
            ]
        )

        assert knowledge_base.to_json() == [
            {
                "question": "¿Cómo cambio mi contraseña?",
                "answer": "Puedes cambiarla desde configuración.",
            },
            {
                "question": "¿Cuál es el horario de atención?",
                "answer": "Lunes a viernes.",
            },
        ]

    def test_add_entry_and_all_entries_return_copy(self) -> None:
        knowledge_base = KnowledgeBase(
            [
                KnowledgeBaseEntry(
                    question="¿Cómo cambio mi contraseña?",
                    answer="Puedes cambiarla desde configuración.",
                )
            ]
        )

        entries_snapshot = knowledge_base.all_entries()
        entries_snapshot.append(
            KnowledgeBaseEntry(
                question="¿Cuál es el horario de atención?",
                answer="Lunes a viernes.",
            )
        )
        assert knowledge_base.all_entries() == [
            KnowledgeBaseEntry(
                question="¿Cómo cambio mi contraseña?",
                answer="Puedes cambiarla desde configuración.",
            )
        ]

        knowledge_base.add_entry(
            KnowledgeBaseEntry(
                question="¿Cuál es el horario de atención?",
                answer="Lunes a viernes.",
            )
        )
        assert knowledge_base.all_entries() == [
            KnowledgeBaseEntry(
                question="¿Cómo cambio mi contraseña?",
                answer="Puedes cambiarla desde configuración.",
            ),
            KnowledgeBaseEntry(
                question="¿Cuál es el horario de atención?",
                answer="Lunes a viernes.",
            ),
        ]

    def test_best_match_returns_answer(self) -> None:
        knowledge_base = KnowledgeBase(
            [
                KnowledgeBaseEntry(
                    question="¿Cómo cambio mi contraseña?",
                    answer="Usa la sección de configuración.",
                ),
                KnowledgeBaseEntry(
                    question="Horario de atención",
                    answer="Lunes a viernes.",
                ),
            ]
        )

        suggestion = knowledge_base.best_match("Como cambio mi contrasena!!!")

        assert suggestion == "Usa la sección de configuración."

    def test_best_match_returns_none_when_below_threshold(self) -> None:
        knowledge_base = KnowledgeBase(
            [
                KnowledgeBaseEntry(
                    question="Información de facturación",
                    answer="Puedes ver tus facturas en el portal.",
                )
            ]
        )

        assert (
            knowledge_base.best_match("Necesito ayuda con soporte", threshold=0.99)
            is None
        )


class TestTextNormalization:
    def test_normalize_text_removes_accents_and_punctuation(self) -> None:
        assert _normalize_text("¿Cómo estás?") == "como estas"
