from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any


def make_id(full_name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", full_name.lower()).strip("-")


def normalized_repo(
    repo: dict[str, Any],
    topics: list[str] | None = None,
    score: float | None = None,
    score_reasons: list[str] | None = None,
) -> dict[str, Any]:
    license_obj = repo.get("license") or {}

    result: dict[str, Any] = {
        "id": make_id(repo["full_name"]),
        "source": "github",
        "full_name": repo["full_name"],
        "url": repo["html_url"],
        "description": repo.get("description"),
        "homepage": repo.get("homepage") or None,
        "topics": sorted(topics or repo.get("topics") or []),
        "language": repo.get("language"),
        "license": license_obj.get("spdx_id"),
        "stars": repo.get("stargazers_count"),
        "forks": repo.get("forks_count"),
        "open_issues": repo.get("open_issues_count"),
        "archived": bool(repo.get("archived")),
        "fork": bool(repo.get("fork")),
        "created_at": repo.get("created_at"),
        "updated_at": repo.get("updated_at"),
        "pushed_at": repo.get("pushed_at"),
        "default_branch": repo.get("default_branch"),
        "last_scanned": datetime.now(timezone.utc).isoformat(),
    }

    if score is not None:
        result["curation"] = {
            "status": "candidate",
            "source": "automated-discovery",
            "verified": False,
            "veterinary_relevance_score": score,
            "score_reasons": score_reasons or [],
        }

    return result


def merge_dynamic(existing: dict[str, Any], fresh: dict[str, Any]) -> dict[str, Any]:
    preserved = {
        key: existing.get(key)
        for key in (
            "resource_types",
            "domains",
            "species",
            "modalities",
            "tasks",
            "paper",
            "datasets",
            "models",
        )
        if key in existing
    }

    curation = existing.get("curation")
    merged = {**existing, **fresh, **preserved}

    if curation:
        merged["curation"] = curation

    return merged
