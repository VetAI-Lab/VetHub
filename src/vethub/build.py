from __future__ import annotations

import json
from datetime import datetime, timezone

from .io import ROOT, load_yaml


def run() -> dict:
    accepted = load_yaml(ROOT / "registry" / "repositories.yaml").get("resources", [])
    candidates = load_yaml(ROOT / "registry" / "candidates.yaml").get("resources", [])

    payload = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "counts": {
            "accepted": len(accepted),
            "candidates": len(candidates),
            "total": len(accepted) + len(candidates),
        },
        "accepted": accepted,
        "candidates": candidates,
    }

    for path in (ROOT / "data" / "catalog.json", ROOT / "docs" / "catalog.json"):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    print(
        f"[build] accepted={len(accepted)} "
        f"candidates={len(candidates)} total={len(accepted) + len(candidates)}"
    )
    return payload
