from __future__ import annotations

import json
from datetime import datetime, timezone

from .io import ROOT, load_yaml


def run() -> dict:
    accepted = (
        load_yaml(ROOT / "registry" / "repositories.yaml")
        .get("resources", [])
    )

    candidates = (
        load_yaml(ROOT / "registry" / "candidates.yaml")
        .get("resources", [])
    )

    generated_at = datetime.now(timezone.utc).isoformat()

    # Complete internal catalog.
    internal_payload = {
        "schema_version": 1,
        "generated_at": generated_at,
        "counts": {
            "accepted": len(accepted),
            "candidates": len(candidates),
            "total": len(accepted) + len(candidates),
        },
        "accepted": accepted,
        "candidates": candidates,
    }

    # Public website catalog.
    # IMPORTANT: machine-discovered candidates are deliberately excluded.
    public_payload = {
        "schema_version": 1,
        "generated_at": generated_at,
        "counts": {
            "accepted": len(accepted),
        },
        "resources": accepted,
    }

    data_path = ROOT / "data" / "catalog.json"
    data_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_text(
        json.dumps(
            internal_payload,
            indent=2,
            ensure_ascii=False,
        ) + "\n",
        encoding="utf-8",
    )

    docs_path = ROOT / "docs" / "catalog.json"
    docs_path.parent.mkdir(parents=True, exist_ok=True)
    docs_path.write_text(
        json.dumps(
            public_payload,
            indent=2,
            ensure_ascii=False,
        ) + "\n",
        encoding="utf-8",
    )

    print(
        f"[build] accepted={len(accepted)} "
        f"candidates={len(candidates)} "
        f"total={len(accepted)+len(candidates)}"
    )

    print(
        f"[public] publishing {len(accepted)} "
        "reviewed resources"
    )

    return internal_payload
