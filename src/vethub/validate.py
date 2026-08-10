from __future__ import annotations

from .io import ROOT, load_yaml


def run() -> None:
    seen = set()

    for filename in ("repositories.yaml", "candidates.yaml"):
        payload = load_yaml(ROOT / "registry" / filename)
        if payload.get("version") != 1:
            raise ValueError(f"{filename}: unsupported or missing version")

        for item in payload.get("resources", []):
            for required in ("id", "source", "full_name", "url"):
                if not item.get(required):
                    raise ValueError(f"{filename}: entry missing {required}: {item}")

            key = item["full_name"].lower()
            if key in seen:
                raise ValueError(f"Duplicate repository across registry: {item['full_name']}")
            seen.add(key)

    print(f"[validate] {len(seen)} unique resources")
