from __future__ import annotations

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from .entities import HistoryRecord, KnowledgeBaseEntry


class SuggestRequest(BaseModel):
    query: str = Field(..., min_length=1, description="User query")

    model_config = ConfigDict(str_strip_whitespace=True)


class SuggestionResponse(BaseModel):
    suggestion: str


class HistoryItem(BaseModel):
    query: str
    suggestion: str

    @classmethod
    def from_record(cls, record: HistoryRecord) -> HistoryItem:
        return cls.model_validate(vars(record))


class KnowledgeBaseItem(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        validation_alias=AliasChoices("question", "pregunta"),
        serialization_alias="pregunta",
    )
    answer: str = Field(
        ...,
        min_length=1,
        validation_alias=AliasChoices("answer", "respuesta"),
        serialization_alias="respuesta",
    )

    model_config = ConfigDict(str_strip_whitespace=True, populate_by_name=True)

    @classmethod
    def from_entry(cls, entry: KnowledgeBaseEntry) -> KnowledgeBaseItem:
        return cls.model_validate(vars(entry))
