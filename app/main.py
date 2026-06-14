from __future__ import annotations

import os
from datetime import datetime, timezone

from fastapi import FastAPI

from app.linguistic import (
    ALL_PRONOUNS,
    CRISIS_PATTERNS,
    FIRST_PERSON_PRONOUNS,
    NAMED_ENTITY_LABELS,
    PRESSURE_PATTERNS,
    TEMPORAL_ENTITY_LABELS,
    UNCERTAINTY_PATTERNS,
    count_negations,
    count_pattern_matches,
    count_active_sentences,
    count_questions,
    count_tense_aspect,
    extract_predicate_adjectives,
    get_negated_terms,
    get_nlp,
    match_difficulty,
    match_external_pressure,
    unique_preserving_order,
)
from app.models import AnalyzeRequest, AnalyzeResponse, FEATURE_VERSION


app = FastAPI(title="Project Arist spaCy NLP Service", version="0.1.0")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@app.get("/health")
def healthcheck():
    return {"status": "ok", "model": os.getenv("SPACY_MODEL", "en_core_web_sm")}


@app.post("/debug/tokens")
def debug_tokens(request: AnalyzeRequest):
    """Returns raw spaCy token attributes for inspection. Remove before production."""
    doc = get_nlp()(request.text.strip())
    return [
        {
            "i": token.i,
            "text": token.text,
            "lemma": token.lemma_,
            "pos": token.pos_,
            "tag": token.tag_,
            "dep": token.dep_,
            "head_i": token.head.i,
            "head_text": token.head.text,
            "morph": str(token.morph),
        }
        for token in doc
    ]


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    text = request.text.strip()
    doc = get_nlp()(text)

    content_tokens = [token for token in doc if not token.is_space and not token.is_punct]
    word_count = len(content_tokens)
    sentence_count = len(list(doc.sents))
    direct_question_count, deliberative_question_count = count_questions(doc)

    first_person_pronoun_count = sum(
        1 for token in doc if token.text.lower() in FIRST_PERSON_PRONOUNS
    )
    pronoun_count = sum(1 for token in doc if token.pos_ == "PRON" or token.text.lower() in ALL_PRONOUNS)
    verb_count = sum(1 for token in doc if token.pos_ in {"VERB", "AUX"})
    adjective_count = sum(1 for token in doc if token.pos_ == "ADJ")
    adverb_count = sum(1 for token in doc if token.pos_ == "ADV")

    negation_count, negation_terms = count_negations(doc)
    pressure_word_count, pressure_terms = count_pattern_matches(text, PRESSURE_PATTERNS)
    uncertainty_word_count, uncertainty_terms = count_pattern_matches(text, UNCERTAINTY_PATTERNS)
    passive_voice_count, active_voice_count = count_active_sentences(doc)
    present_progressive_count, past_tense_count = count_tense_aspect(doc)
    difficulty_count, difficulty_terms = match_difficulty(doc)
    crisis_indicator_count, crisis_terms = count_pattern_matches(text, CRISIS_PATTERNS)
    external_pressure_count, external_pressure_terms = match_external_pressure(doc)
    predicate_adjectives = extract_predicate_adjectives(doc)
    negated_terms = get_negated_terms(doc)

    noun_phrases = unique_preserving_order([chunk.text.strip() for chunk in doc.noun_chunks if chunk.root.pos_ != "PRON"])
    named_entities = unique_preserving_order(
        [entity.text.strip() for entity in doc.ents if entity.label_ in NAMED_ENTITY_LABELS]
    )
    temporal_expressions = unique_preserving_order(
        [entity.text.strip() for entity in doc.ents if entity.label_ in TEMPORAL_ENTITY_LABELS]
    )

    ratio = round(first_person_pronoun_count / word_count, 4) if word_count else 0.0

    return AnalyzeResponse(
        entry_id=request.entry_id,
        user_id=request.user_id,
        processed_at=_now(),
        word_count=word_count,
        sentence_count=sentence_count,
        direct_question_count=direct_question_count,
        deliberative_question_count=deliberative_question_count,
        first_person_pronoun_count=first_person_pronoun_count,
        first_person_pronoun_ratio=ratio,
        pronoun_count=pronoun_count,
        verb_count=verb_count,
        negation_count=negation_count,
        pressure_word_count=pressure_word_count,
        uncertainty_word_count=uncertainty_word_count,
        adjective_count=adjective_count,
        adverb_count=adverb_count,
        passive_voice_count=passive_voice_count,
        active_voice_count=active_voice_count,
        present_progressive_count=present_progressive_count,
        past_tense_count=past_tense_count,
        difficulty_count=difficulty_count,
        crisis_indicator_count=crisis_indicator_count,
        crisis_terms=crisis_terms,
        external_pressure_count=external_pressure_count,
        external_pressure_terms=external_pressure_terms,
        negation_terms=negation_terms,
        pressure_terms=pressure_terms,
        uncertainty_terms=uncertainty_terms,
        difficulty_terms=difficulty_terms,
        predicate_adjectives=predicate_adjectives,
        negated_terms=negated_terms,
        noun_phrases=noun_phrases,
        named_entities=named_entities,
        temporal_expressions=temporal_expressions,
        feature_version=FEATURE_VERSION,
    )
