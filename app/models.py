from __future__ import annotations

from pydantic import BaseModel, Field

FEATURE_VERSION = "v2"


class AnalyzeRequest(BaseModel):
    entry_id: str | None = None
    user_id: str | None = None
    text: str = Field(..., min_length=1)


class AnalyzeResponse(BaseModel):
    entry_id: str | None = None
    user_id: str | None = None
    processed_at: str
    word_count: int
    sentence_count: int
    direct_question_count: int
    deliberative_question_count: int
    first_person_pronoun_count: int
    first_person_pronoun_ratio: float
    pronoun_count: int
    verb_count: int
    negation_count: int
    pressure_word_count: int
    uncertainty_word_count: int
    adjective_count: int
    adverb_count: int
    passive_voice_count: int
    active_voice_count: int
    present_progressive_count: int
    past_tense_count: int
    difficulty_count: int
    crisis_indicator_count: int
    external_pressure_count: int
    negation_terms: list[str]
    pressure_terms: list[str]
    uncertainty_terms: list[str]
    difficulty_terms: list[str]
    crisis_terms: list[str]
    external_pressure_terms: list[str]
    predicate_adjectives: list[str]
    negated_terms: list[str]
    noun_phrases: list[str]
    named_entities: list[str]
    temporal_expressions: list[str]
    feature_version: str = FEATURE_VERSION