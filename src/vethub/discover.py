from __future__ import annotations

from .github import GitHubClient
from .io import ROOT, load_yaml, save_yaml
from .normalize import normalized_repo
from .scoring import veterinary_relevance


def run() -> int:
    config = load_yaml(ROOT / "config" / "discovery.yaml")
    candidate_path = ROOT / "registry" / "candidates.yaml"
    accepted_path = ROOT / "registry" / "repositories.yaml"

    candidates = load_yaml(candidate_path) or {"version": 1, "resources": []}
    accepted = load_yaml(accepted_path) or {"version": 1, "resources": []}

    known = {
        item["full_name"].lower()
        for collection in (candidates.get("resources", []), accepted.get("resources", []))
        for item in collection
        if item.get("full_name")
    }

    client = GitHubClient()
    new_entries: list[dict] = []

    for query in config.get("search_queries", []):
        print(f"[discover] {query}")

        for repo in client.search_repositories(
            query,
            int(config.get("per_query", 25)),
        ):
            full_name = repo.get("full_name")
            if not full_name or full_name.lower() in known:
                continue

            # Do not index forks as first-class resources during automatic discovery.
            if repo.get("fork"):
                continue

            try:
                topics = client.topics(full_name)
                readme = client.readme_text(full_name)
            except Exception as exc:
                print(f"[skip] {full_name}: {exc}")
                continue

            score, reasons = veterinary_relevance(repo, readme, topics, config)
            if score < float(config.get("minimum_score", 0.35)):
                continue

            entry = normalized_repo(repo, topics, score, reasons)
            new_entries.append(entry)
            known.add(full_name.lower())

            if len(new_entries) >= int(config.get("max_candidates", 1000)):
                break

        if len(new_entries) >= int(config.get("max_candidates", 1000)):
            break

    combined = candidates.get("resources", []) + new_entries
    combined.sort(
        key=lambda x: (
            -(x.get("curation", {}).get("veterinary_relevance_score", 0) or 0),
            x.get("full_name", "").lower(),
        )
    )

    candidates["version"] = 1
    candidates["resources"] = combined
    save_yaml(candidate_path, candidates)

    print(f"[discover] added {len(new_entries)} new candidates")
    return len(new_entries)
