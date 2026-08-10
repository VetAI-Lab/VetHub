from __future__ import annotations

from .github import GitHubClient
from .io import ROOT, load_yaml, save_yaml
from .normalize import merge_dynamic, normalized_repo


def _refresh_file(path):
    payload = load_yaml(path) or {"version": 1, "resources": []}
    client = GitHubClient()
    refreshed = []

    for existing in payload.get("resources", []):
        full_name = existing.get("full_name")
        if not full_name:
            refreshed.append(existing)
            continue

        try:
            repo = client.repository(full_name)
            topics = client.topics(full_name)
            fresh = normalized_repo(repo, topics)
            refreshed.append(merge_dynamic(existing, fresh))
            print(f"[enrich] {full_name}")
        except Exception as exc:
            existing["refresh_error"] = str(exc)
            refreshed.append(existing)
            print(f"[enrich:failed] {full_name}: {exc}")

    payload["version"] = 1
    payload["resources"] = refreshed
    save_yaml(path, payload)


def run() -> None:
    _refresh_file(ROOT / "registry" / "repositories.yaml")
    _refresh_file(ROOT / "registry" / "candidates.yaml")
