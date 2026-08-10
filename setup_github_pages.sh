#!/usr/bin/env bash
set -euo pipefail

echo "[1/5] Backing up current files..."
mkdir -p .backup_pages
cp src/vethub/build.py .backup_pages/build.py
cp docs/index.html .backup_pages/index.html
cp docs/app.js .backup_pages/app.js
cp .github/workflows/refresh.yml .backup_pages/refresh.yml

echo "[2/5] Making public catalog REVIEWED-ONLY..."

cat > src/vethub/build.py <<'PY'
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
PY

echo "[3/5] Updating website..."

cat > docs/index.html <<'HTML'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport"
        content="width=device-width, initial-scale=1">

  <meta
    name="description"
    content="VetHub: discover open veterinary software, datasets, models, benchmarks and computational resources."
  >

  <title>VetHub | Veterinary Open Resources</title>

  <link rel="stylesheet" href="styles.css">
</head>

<body>

<main>

<header>

  <p class="eyebrow">VetAI-Lab</p>

  <h1>VetHub</h1>

  <p class="lede">
    Discover open veterinary software, datasets,
    models, benchmarks, and computational resources.
  </p>

  <input
    id="search"
    type="search"
    placeholder="Search veterinary resources…"
    autocomplete="off"
  >

  <div id="stats"></div>

</header>


<section>

  <div id="themes"></div>

  <div id="results"></div>

</section>


<footer style="margin-top:50px;color:#68737d">

  <p>
    VetHub is an open veterinary resource discovery project
    maintained by VetAI-Lab.
  </p>

  <p>
    Only reviewed resources are displayed publicly.
  </p>

</footer>

</main>

<script src="app.js"></script>

</body>
</html>
HTML


cat > docs/app.js <<'JS'
let catalog = null;
let activeTheme = null;

const q = (id) => document.getElementById(id);

function searchableText(item) {
  return [
    item.full_name,
    item.description,
    item.language,
    ...(item.topics || []),
    ...(item.domains || []),
    ...(item.species || []),
    ...(item.tasks || []),
    ...(item.resource_types || []),
    ...(item.modalities || []),
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();
}


function getThemes(resources) {
  const counts = {};

  resources.forEach((item) => {
    (item.domains || []).forEach((domain) => {
      counts[domain] = (counts[domain] || 0) + 1;
    });
  });

  return Object.entries(counts)
    .sort((a, b) => b[1] - a[1]);
}


function renderThemes() {

  const themes = getThemes(catalog.resources || []);

  q("themes").innerHTML = `
    <div style="
      display:flex;
      gap:8px;
      flex-wrap:wrap;
      margin-bottom:24px;
    ">

      <button
        class="theme-button"
        data-theme=""
      >
        All
      </button>

      ${themes.map(([theme, count]) => `
        <button
          class="theme-button"
          data-theme="${theme}"
        >
          ${theme.replaceAll("-", " ")} (${count})
        </button>
      `).join("")}

    </div>
  `;

  document.querySelectorAll(".theme-button")
    .forEach((button) => {

      button.addEventListener("click", () => {

        activeTheme =
          button.dataset.theme || null;

        render();

      });

    });

}


function render() {

  if (!catalog) return;

  const query =
    q("search").value.trim().toLowerCase();

  let items = [...(catalog.resources || [])];

  if (activeTheme) {
    items = items.filter(
      (item) =>
        (item.domains || []).includes(activeTheme)
    );
  }

  if (query) {
    items = items.filter(
      (item) =>
        searchableText(item).includes(query)
    );
  }

  q("stats").textContent =
    `${catalog.counts.accepted} reviewed resources · ${items.length} shown`;

  q("results").innerHTML =
    items.map((item) => {

      const tags = [
        ...(item.domains || []),
        ...(item.species || []),
        ...(item.tasks || []),
        ...(item.topics || []).slice(0, 4),
      ].slice(0, 10);

      return `
        <article class="card">

          <h2>
            <a
              href="${item.url}"
              target="_blank"
              rel="noopener"
            >
              ${item.full_name}
            </a>
          </h2>

          <p class="description">
            ${item.description || "No description available."}
          </p>

          <div class="meta">

            ${
              item.language
                ? `<span>${item.language}</span>`
                : ""
            }

            ${
              item.license
                ? `<span>${item.license}</span>`
                : ""
            }

            ${
              Number.isFinite(item.stars)
                ? `<span>★ ${item.stars}</span>`
                : ""
            }

            ${
              item.archived
                ? `<span>Archived</span>`
                : ""
            }

          </div>

          <div class="tags">

            ${tags.map(
              (tag) =>
                `<span class="tag">${tag}</span>`
            ).join("")}

          </div>

        </article>
      `;

    }).join("");

}


fetch("catalog.json")
  .then((response) => response.json())
  .then((data) => {

    catalog = data;

    renderThemes();
    render();

  })
  .catch((error) => {

    q("results").textContent =
      `Unable to load catalog: ${error}`;

  });


q("search")
  .addEventListener("input", render);
JS


touch docs/.nojekyll


echo "[4/5] Adding GitHub Pages deployment..."

cat > .github/workflows/pages.yml <<'YAML'
name: Deploy VetHub Pages

on:
  push:
    branches:
      - main
    paths:
      - "docs/**"
      - ".github/workflows/pages.yml"

  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:

  deploy:

    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}

    runs-on: ubuntu-latest

    steps:

      - name: Checkout
        uses: actions/checkout@v4

      - name: Configure Pages
        uses: actions/configure-pages@v5

      - name: Upload VetHub website
        uses: actions/upload-pages-artifact@v4
        with:
          path: docs

      - name: Deploy GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
YAML


echo "[5/5] Rebuilding catalog..."

python -m pip install -e . >/dev/null

vethub validate
vethub build

echo
echo "========================================"
echo "VetHub GitHub Pages patch complete"
echo "========================================"
echo
echo "Public catalog:"
echo "  docs/catalog.json"
echo
echo "Internal candidate catalog:"
echo "  registry/candidates.yaml"
echo
echo "Run:"
echo
echo "  git status"
echo "  git add ."
echo '  git commit -m "Add VetHub GitHub Pages website"'
echo "  git push origin main"
echo
