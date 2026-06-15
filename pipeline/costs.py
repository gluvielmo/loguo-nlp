GENERATION_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"

_PRICES_PER_TOKEN = {
    "text-embedding-3-small": 0.02 / 1_000_000,
    "gpt-4o-mini-input":      0.15 / 1_000_000,
    "gpt-4o-mini-output":     0.60 / 1_000_000,
}


def estimate_cost(*, embedding_tokens: int, input_tokens: int, output_tokens: int) -> float:
    return round(
        embedding_tokens * _PRICES_PER_TOKEN["text-embedding-3-small"]
        + input_tokens   * _PRICES_PER_TOKEN["gpt-4o-mini-input"]
        + output_tokens  * _PRICES_PER_TOKEN["gpt-4o-mini-output"],
        6,
    )
