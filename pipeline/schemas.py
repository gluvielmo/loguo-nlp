from pydantic import BaseModel, Field
from datetime import date, datetime

class JournalEntry(BaseModel):
    id: str
    date: date
    text: str
    source: str = ""
    metadata: dict = {}

class LinguisticFeatures(BaseModel):
    entry_id: str | None = None
    user_id: str | None = None
    processed_at: datetime = Field(default_factory=datetime.utcnow)
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
    negation_terms: list[str] = []
    pressure_terms: list[str] = []
    uncertainty_terms: list[str] = []
    difficulty_terms: list[str] = []
    crisis_terms: list[str] = []
    external_pressure_terms: list[str] = []
    predicate_adjectives: list[str] = []
    negated_terms: list[str] = []
    noun_phrases: list[str] = []
    named_entities: list[str] = []
    temporal_expressions: list[str] = []

class TopicAssignment(BaseModel):
    entry_id: str
    topic_id: int
    topic_label: str
    keywords: list[str]
    probability: float

class Cluster(BaseModel):
    cluster_id: int
    label: str
    description: str = ""
    keywords: list[str] = []
    subthemes: list[str] = []
    entry_ids: list[str]
    representative_entry_ids: list[str]
    labeling_method: str

class Theme(BaseModel):
    name: str
    description: str
    entry_ids: list[str]

class Report(BaseModel):
    condition_name: str
    corpus_size: int
    date_range: tuple[date, date]
    generated_at: datetime
    main_themes: list[Theme]
    subthemes: list[Theme]
    temporal_evolution: dict
    linguistic_patterns: dict
    representative_evidence: list[dict]
    surprising_patterns: list[str]
    reflection_questions: list[str]
    limitations: list[str]

class ConditionArtifacts(BaseModel):
    condition: str
    corpus_id: str
    run_timestamp: datetime
    report: Report
    topics_or_clusters: list[dict]
    lfe_per_entry: list[LinguisticFeatures]
    lfe_aggregated: dict
    token_usage: dict = {}
    runtime_seconds: float = 0.0

