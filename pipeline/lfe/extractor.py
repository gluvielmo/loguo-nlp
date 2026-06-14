import spacy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app import linguistic as ling
from pipeline.schemas import JournalEntry, LinguisticFeatures

spacy_model = spacy.load("en_core_web_sm")

def _extract_from_doc(entry: JournalEntry) -> LinguisticFeatures:
    doc = spacy_model(entry.text)

    content_tokens = [token for token in doc if not token.is_space and not token.is_punct]

    # Document stats
    word_count = len(content_tokens)
    sentence_count = len(list(doc.sents))
    direct_question_count, deliberative_question_count = ling.count_questions(doc)

    # Part-of-speech stats
    first_person_pronoun_count = sum(
        1 for token in doc if token.text.lower() in ling.FIRST_PERSON_PRONOUNS
    )
    pronoun_count = sum(
        1 for token in doc if token.pos_ == "PRON" or token.text.lower() in ling.ALL_PRONOUNS
    )
    verb_count = sum(
        1 for token in doc if token.pos_ in {"VERB", "AUX"}
    )
    adjective_count = sum(
        1 for token in doc if token.pos_ == "ADJ"
    )
    adverb_count = sum(
        1 for token in doc if token.pos_ == "ADV"
    )

    # Psychological / linguistic patterns
    negation_count, negation_terms = ling.count_negations(doc)
    pressure_word_count, pressure_terms = ling.count_pattern_matches(entry.text, ling.PRESSURE_PATTERNS)
    uncertainty_word_count, uncertainty_terms = ling.count_pattern_matches(entry.text, ling.UNCERTAINTY_PATTERNS)
    passive_voice_count, active_voice_count = ling.count_active_sentences(doc)
    present_progressive_count, past_tense_count = ling.count_tense_aspect(doc)
    difficulty_count, difficulty_terms = ling.match_difficulty(doc)
    crisis_indicator_count, crisis_terms = ling.count_pattern_matches(entry.text, ling.CRISIS_PATTERNS)
    external_pressure_count, external_pressure_terms = ling.match_external_pressure(doc)
    predicate_adjectives = ling.extract_predicate_adjectives(doc)
    negated_terms = ling.get_negated_terms(doc)

    # Extracted data
    noun_phrases = ling.unique_preserving_order([chunk.text.strip() for chunk in doc.noun_chunks if chunk.root.pos_ != "PRON"])
    named_entities = ling.unique_preserving_order(
        [entity.text.strip() for entity in doc.ents if entity.label_ in ling.NAMED_ENTITY_LABELS]
    )
    temporal_expressions = ling.unique_preserving_order(
        [entity.text.strip() for entity in doc.ents if entity.label_ in ling.TEMPORAL_ENTITY_LABELS]
    )

    # Other
    first_person_pronoun_ratio = round(first_person_pronoun_count / word_count, 4) if word_count else 0.0

    return LinguisticFeatures(
        entry_id=entry.id,
        word_count=word_count,
        sentence_count=sentence_count,
        direct_question_count=direct_question_count,
        deliberative_question_count=deliberative_question_count,
        first_person_pronoun_count=first_person_pronoun_count,
        first_person_pronoun_ratio=first_person_pronoun_ratio,
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
        temporal_expressions=temporal_expressions
    )

def extract(entry: JournalEntry) -> LinguisticFeatures:
    doc = spacy_model(entry.text)
    return _extract_from_doc(entry, doc)

def extract_batch(entries: list[JournalEntry]) -> list[LinguisticFeatures]:
    docs = spacy_model.pipe([e.text for e in entries], batch_size=64)
    return [_extract_from_doc(e, doc) for e, doc in zip(entries, docs)]
