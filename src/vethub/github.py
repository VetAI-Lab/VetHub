from __future__ import annotations

import os
import time
from typing import Any

import requests


API = "https://api.github.com"


class GitHubClient:
    def __init__(self, token: str | None = None, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        token = token or os.getenv("GITHUB_TOKEN")

        self.session.headers.update(
            {
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "VetAI-Lab-VetHub",
            }
        )
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def _get(self, url: str, params: dict[str, Any] | None = None) -> Any:
        response = self.session.get(url, params=params, timeout=self.timeout)

        if response.status_code == 403 and "rate limit" in response.text.lower():
            reset = response.headers.get("X-RateLimit-Reset")
            if reset:
                wait = max(0, int(reset) - int(time.time()))
                raise RuntimeError(
                    f"GitHub API rate limit reached; resets in approximately {wait} seconds."
                )

        response.raise_for_status()
        return response.json()

    def search_repositories(self, query: str, per_page: int = 25) -> list[dict[str, Any]]:
        payload = self._get(
            f"{API}/search/repositories",
            params={
                "q": query,
                "sort": "updated",
                "order": "desc",
                "per_page": min(per_page, 100),
            },
        )
        return payload.get("items", [])

    def repository(self, full_name: str) -> dict[str, Any]:
        return self._get(f"{API}/repos/{full_name}")

    def topics(self, full_name: str) -> list[str]:
        payload = self._get(f"{API}/repos/{full_name}/topics")
        return payload.get("names", [])

    def readme_text(self, full_name: str) -> str:
        response = self.session.get(
            f"{API}/repos/{full_name}/readme",
            headers={"Accept": "application/vnd.github.raw+json"},
            timeout=self.timeout,
        )
        if response.status_code == 404:
            return ""
        response.raise_for_status()
        return response.text[:50_000]
