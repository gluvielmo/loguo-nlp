from __future__ import annotations

import os
import re
from functools import lru_cache

import spacy
from spacy.matcher import Matcher
from spacy.util import filter_spans


FIRST_PERSON_PRONOUNS = {
    "i",
    "me",
    "my",
    "mine",
    "myself",
    "we",
    "us",
    "our",
    "ours",
    "ourselves",
}

ALL_PRONOUNS = FIRST_PERSON_PRONOUNS | {
    "you",
    "your",
    "yours",
    "yourself",
    "yourselves",
    "he",
    "him",
    "his",
    "himself",
    "she",
    "her",
    "hers",
    "herself",
    "they",
    "them",
    "their",
    "theirs",
    "themselves",
    "it",
    "its",
    "itself",
}

NEGATION_TERMS = {
    "no",
    "not",
    "never",
    "none",
    "nobody",
    "nothing",
    "neither",
    "nowhere",
    "hardly",
    "barely",
    "scarcely",
    "cannot",
    "can't",
    "dont",
    "don't",
    "didnt",
    "didn't",
    "isnt",
    "isn't",
    "wasnt",
    "wasn't",
    "shouldnt",
    "shouldn't",
    "wouldnt",
    "wouldn't",
    "couldnt",
    "couldn't",
    "wont",
    "won't",
}

PRESSURE_PATTERNS = (
    "should",
    "must",
    "need to",
    "have to",
    "had to",
    "supposed to",
    "ought to",
)

UNCERTAINTY_PATTERNS = (
    "maybe",
    "perhaps",
    "possibly",
    "probably",
    "i guess",
    "i think",
    "not sure",
    "unsure",
    "uncertain",
    "kind of",
    "sort of",
)

NAMED_ENTITY_LABELS = {
    "PERSON",
    "ORG",
    "GPE",
    "LOC",
    "FAC",
    "PRODUCT",
    "EVENT",
    "WORK_OF_ART",
}

TEMPORAL_ENTITY_LABELS = {"DATE", "TIME"}

# spaCy POS tags for WH-words (who, what, where, when, why, how, which, whose)
WH_TAGS = {"WRB", "WP", "WP$"}

# Compound WH-words that introduce subordinate clauses, not questions
WH_SUBORDINATORS = {"whenever", "wherever", "however", "whatever", "whoever", "whomever", "whichever"}

MODAL_LEMMAS = {"should", "could", "would", "can", "will", "shall", "might", "may"}

# Verbs of cognitive deliberation that introduce embedded questions ("whether", "if")
DELIBERATION_VERBS = {
    "debate", "wonder", "consider", "decide", "question",
    "think", "know", "sure", "certain", "tell", "figure",
}

CRISIS_PATTERNS = (
    # Direct/explicit ideation
    "suicide",
    "suicidal",
    "kill myself",
    "killing myself",
    "end my life",
    "take my life",
    "commit suicide",
    "committing suicide",
    "off myself",
    "end it all",
    "hang myself",
    "slit my wrists",
    # Passive/indirect ideation
    "want to die",
    "wanting to die",
    "wish i was dead",
    "wish i were dead",
    "better off dead",
    "no reason to live",
    "not worth living",
    "don't want to be here",
    "dont want to be here",
    "can't go on",
    "cant go on",
    "want it to stop",
    "want to end it",
    "ready to give up on life",
)

# Structural Matcher patterns for externally-imposed social pressure.
# Catches "[person] [verb] me/us to [verb]" — e.g. "my mom told me to",
# "my parents are expecting me to do better".
# Subject filtering (excluding first-person) is applied in match_external_pressure().
EXTERNAL_PRESSURE_MATCHER_PATTERNS = [
    [
        {"LEMMA": {"IN": ["expect", "want", "need", "pressure", "force", "push", "convince", "tell", "ask"]}},
        {"LOWER": {"IN": ["me", "us"]}},
        {"LOWER": "to"},
        {"POS": "VERB"},
    ],
]

# Matcher patterns for difficulty/effort language — uses linguistic constraints
# instead of raw string matching to reduce false positives
DIFFICULTY_MATCHER_PATTERNS = [
    # "hard to get up", "difficult to focus"
    [{"LOWER": {"IN": ["hard", "difficult"]}}, {"LOWER": "to"}, {"POS": "VERB"}],
    # "hard not to give up", "difficult not to quit"
    [{"LOWER": {"IN": ["hard", "difficult"]}}, {"LOWER": "not"}, {"LOWER": "to"}, {"POS": "VERB"}],
    # "so difficult", "very hard", "so exhausting"
    [{"LOWER": {"IN": ["so", "very", "really", "extremely", "incredibly"]}}, {"LOWER": {"IN": ["hard", "difficult", "exhausting", "overwhelming", "draining"]}}],
    # "struggle" / "struggling" standalone
    [{"LEMMA": "struggle"}],
    # "give up"
    [{"LOWER": "give"}, {"LOWER": "up"}],
    # "like a weight" (somatic metaphor)
    [{"LOWER": "like"}, {"LOWER": "a"}, {"LOWER": "weight"}],
    # affective verbs expressing difficulty: "exhausted me", "overwhelming", "draining"
    [{"LEMMA": {"IN": ["exhaust", "overwhelm", "drain", "frustrate", "burden", "suffocate"]}}],
    # "hold back" / "held back"
    [{"LOWER": {"IN": ["hold", "held"]}}, {"LOWER": "back"}],
    # "falling behind"
    [{"LOWER": "falling"}, {"LOWER": "behind"}],
    # "burning out" / "burnt out"
    [{"LOWER": {"IN": ["burning", "burnt"]}}, {"LOWER": "out"}],
]

# Fixed phrases for difficulty that don't fit well as Matcher token sequences
DIFFICULTY_PHRASES = (
    "can't keep up",
    "cant keep up",
    "cannot keep up",
    "too much to handle",
    "at my limit",
    "breaking point",
    "falling apart",
    "falling to pieces",
)


@lru_cache(maxsize=1)
def get_nlp():
    model_name = os.getenv("SPACY_MODEL", "en_core_web_sm")
    return spacy.load(model_name)


@lru_cache(maxsize=1)
def get_difficulty_matcher() -> Matcher:
    matcher = Matcher(get_nlp().vocab)
    for i, pattern in enumerate(DIFFICULTY_MATCHER_PATTERNS):
        matcher.add(f"DIFFICULTY_{i}", [pattern])
    return matcher


@lru_cache(maxsize=1)
def get_external_pressure_matcher() -> Matcher:
    matcher = Matcher(get_nlp().vocab)
    for i, pattern in enumerate(EXTERNAL_PRESSURE_MATCHER_PATTERNS):
        matcher.add(f"EXT_PRESSURE_{i}", [pattern])
    return matcher


def unique_preserving_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []

    for item in items:
        normalized = item.strip()
        if not normalized:
            continue
        key = normalized.lower()
        if key in seen:
            continue
        seen.add(key)
        ordered.append(normalized)

    return ordered


def count_pattern_matches(text: str, patterns: tuple[str, ...]) -> tuple[int, list[str]]:
    lowered = text.lower()
    matches: list[str] = []

    for pattern in patterns:
        escaped = re.escape(pattern)
        regex = rf"(?<!\w){escaped}(?!\w)"
        found = re.findall(regex, lowered)
        if found:
            matches.extend([pattern] * len(found))

    return len(matches), unique_preserving_order(matches)


def count_negations(doc) -> tuple[int, list[str]]:
    matches: list[str] = []

    for token in doc:
        lower = token.text.lower()
        if token.dep_ == "neg" or lower in NEGATION_TERMS:
            matches.append(lower)

    unique_matches = unique_preserving_order(matches)
    return len(matches), unique_matches


def count_active_sentences(doc) -> tuple[int, int]:
    passive = 0
    active = 0

    for sentence in doc.sents:
        has_passive = any(token.dep_ in {"nsubjpass", "auxpass"} for token in sentence)
        if has_passive:
            passive += 1
        else:
            active += 1

    return passive, active


def _has_verb(tokens) -> bool:
    return any(t.pos_ in {"AUX", "VERB"} for t in tokens)


def is_syntactic_question(sent) -> bool:
    if sent.text.strip().endswith("?"):
        return True
    tokens = [t for t in sent if not t.is_space and not t.is_punct]
    if not tokens:
        return False
    first = tokens[0]
    rest = tokens[1:]
    # WH-word at sentence start (who, what, where, when, why, how, which, whose)
    # Exclude compound WH-subordinators which introduce clauses, not questions
    if first.tag_ in WH_TAGS and first.text.lower() not in WH_SUBORDINATORS:
        return len(tokens) >= 3 or _has_verb(rest)
    # Modal auxiliary at sentence start (Should I..., Could I..., Would it...)
    if first.pos_ == "AUX" and first.lemma_ in MODAL_LEMMAS:
        return len(tokens) >= 3 or _has_verb(rest)
    return False


def has_embedded_question(sent) -> bool:
    """Detects indirect questions like 'debating whether I should shower'."""
    for token in sent:
        if token.text.lower() in {"whether", "if"} and token.dep_ == "mark":
            head = token.head
            if head.lemma_ in DELIBERATION_VERBS or head.head.lemma_ in DELIBERATION_VERBS:
                return True
    return False


def count_questions(doc) -> tuple[int, int]:
    direct = 0
    deliberative = 0
    for sent in doc.sents:
        if is_syntactic_question(sent):
            direct += 1
        if has_embedded_question(sent):
            deliberative += 1
    return direct, deliberative


def count_tense_aspect(doc) -> tuple[int, int]:
    """Returns (present_progressive_count, past_tense_count) across all VERB tokens.

    present_progressive counts finite present-progressive clauses like
    "I am doing" / "I'm moving". We require a progressive verb plus a present-tense
    "be" auxiliary attached either directly or via coordination, which is more
    robust than only checking immediate children.
    """

    def has_be_aux(token) -> bool:
        # Identify be-form auxiliaries by excluding modals (tag MD) rather than
        # matching text or lemma — avoids apostrophe encoding issues with "'m".
        # Be-forms (am/is/are/'m/'re) are always AUX + dep aux/auxpass + non-modal.
        def _is_be_aux(t) -> bool:
            return t.pos_ == "AUX" and t.dep_ in {"aux", "auxpass"} and t.tag_ != "MD"

        if any(_is_be_aux(child) for child in token.children):
            return True

        # Coordinated predicates can inherit the auxiliary from the head.
        if token.dep_ == "conj" and token.head is not token:
            if any(_is_be_aux(child) for child in token.head.children):
                return True

        return False

    present_progressive = 0
    past_tense = 0
    for token in doc:
        if token.pos_ == "VERB":
            if "Prog" in token.morph.get("Aspect") and "Pres" in token.morph.get("Tense"):
                if has_be_aux(token):
                    present_progressive += 1
            elif "Past" in token.morph.get("Tense"):
                past_tense += 1
    return present_progressive, past_tense


def extract_predicate_adjectives(doc) -> list[str]:
    """Adjectives that are predicated of a subject — 'it's difficult', 'I feel exhausted'."""
    return unique_preserving_order([
        token.text for token in doc
        if token.pos_ == "ADJ" and token.dep_ in {"acomp", "attr"}
    ])


def get_negated_terms(doc) -> list[str]:
    """The head word of each syntactic negation — what is actually being negated."""
    return unique_preserving_order([
        token.head.text for token in doc
        if token.dep_ == "neg"
    ])


def match_difficulty(doc) -> tuple[int, list[str]]:
    """Counts difficulty/effort expressions using Matcher patterns and a phrase list.

    Overlapping Matcher matches are deduplicated by keeping the longest span.
    Phrase matches are counted separately and merged into the terms list.
    """
    matcher_matches = get_difficulty_matcher()(doc)
    spans = filter_spans([doc[start:end] for _, start, end in matcher_matches])
    matcher_terms = unique_preserving_order([span.text for span in spans])

    phrase_count, phrase_terms = count_pattern_matches(doc.text, DIFFICULTY_PHRASES)

    all_terms = unique_preserving_order(matcher_terms + phrase_terms)
    return len(spans) + phrase_count, all_terms


def match_external_pressure(doc) -> tuple[int, list[str]]:
    """Detects externally-imposed social pressure using a structural Matcher pattern.

    Finds "[verb] me/us to [verb]" sequences, then uses dependency parsing to filter
    out self-directed cases where the subject is first-person (e.g. "I want me to").
    """
    FIRST_PERSON = {"i", "we", "me", "my", "myself", "our", "ourselves"}

    matches = get_external_pressure_matcher()(doc)
    spans = filter_spans([doc[start:end] for _, start, end in matches])

    results = []
    for span in spans:
        verb_token = span[0]  # key verb is the first token in the pattern
        subj = next(
            (c for c in verb_token.children if c.dep_ in {"nsubj", "nsubjpass"}),
            None,
        )
        if subj is None or subj.text.lower() not in FIRST_PERSON:
            results.append(span.text)

    terms = unique_preserving_order(results)
    return len(results), terms
