from __future__ import annotations

from typing import Any


def veterinary_relevance(
    repo: dict[str, Any],
    readme: str,
    topics: list[str],
    config: dict[str, Any],
) -> tuple[float, list[str]]:
    text = " ".join(
        [
            str(repo.get("name") or ""),
            str(repo.get("description") or ""),
            " ".join(topics),
            readme[:20_000],
        ]
    ).lower()

    raw = 0.0
    reasons: list[str] = []

    for term, weight in config.get("strong_terms", {}).items():
        if term.lower() in text:
            raw += float(weight)
            reasons.append(f"+{weight:g} strong:{term}")

    for term, weight in config.get("supporting_terms", {}).items():
        if term.lower() in text:
            raw += float(weight)
            reasons.append(f"+{weight:g} support:{term}")

    for term, weight in config.get("negative_terms", {}).items():
        if term.lower() in text:
            raw += float(weight)
            reasons.append(f"{weight:g} negative:{term}")

    # Saturating transform: 10 raw points ~= score 1.0.
    score = max(0.0, min(1.0, raw / 10.0))
    return round(score, 3), reasons
