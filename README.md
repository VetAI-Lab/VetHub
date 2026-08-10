# VetHub

**VetHub is an automatically curated registry and discovery layer for open veterinary software, datasets, models, benchmarks, and computational resources.**

VetHub is part of the [VetAI-Lab](https://github.com/VetAI-Lab) ecosystem. Its goal is to make veterinary computational resources easier to **find, compare, reuse, and keep current**.

## What VetHub indexes

- Open-source veterinary software and analysis pipelines
- Veterinary datasets and data resources
- Foundation models and task-specific models
- Benchmarks and evaluation suites
- Annotation and curation tools
- Veterinary bioinformatics resources
- Clinical NLP, imaging, pathology, genomics, epidemiology, welfare, AMR, and One Health projects

VetHub stores **metadata and links**. It does not mirror third-party repositories or redistribute their content.

## How it works

```text
GitHub search
     ↓
candidate repositories
     ↓
metadata enrichment
     ↓
transparent veterinary-relevance scoring
     ↓
deduplication / fork handling
     ↓
candidate registry + reviewed registry
     ↓
searchable catalog
```

A scheduled GitHub Actions workflow refreshes known projects and discovers new candidates. Dynamic metadata such as repository activity, stars, forks, archival status, topics, language, and license can be refreshed automatically.

## Registry model

- `registry/repositories.yaml` — reviewed/accepted resources
- `registry/candidates.yaml` — automatically discovered resources awaiting review
- `data/catalog.json` — machine-readable merged catalog
- `docs/catalog.json` — website-ready catalog

## Initial VetAI-Lab resources

- [VetWelfare-NLP](https://github.com/VetAI-Lab/VetWelfare-NLP) — veterinary clinical NLP and welfare annotation
- [VetJudge](https://github.com/VetAI-Lab/VetJudge) — ensemble agreement, uncertainty, and adjudication for AI-assisted veterinary annotation

## Install

```bash
git clone https://github.com/VetAI-Lab/VetHub.git
cd VetHub
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Run locally

Authenticate with a GitHub token if you want higher API limits:

```bash
export GITHUB_TOKEN="..."
```

Then:

```bash
vethub refresh
```

or run each stage:

```bash
vethub discover
vethub enrich
vethub build
```

## Discovery philosophy

VetHub deliberately does **not** treat a keyword hit as proof of veterinary relevance. Discovery and publication are separated:

```text
discovered → scored → candidate → reviewed → accepted
```

This reduces false positives such as toy "dog-vs-cat" computer-vision repositories that are not veterinary resources.

## Taxonomy

VetHub classifies resources across several axes:

- resource type
- veterinary domain
- species
- modality
- computational task
- curation status

See [`taxonomy/taxonomy.yaml`](taxonomy/taxonomy.yaml).

## Community submissions

Know a veterinary project that is missing? Use the **Submit a veterinary resource** issue template. A submission can start with only a repository URL; VetHub can enrich the remaining metadata.

## Searchable website

A minimal static catalog is included under `docs/`. After enabling GitHub Pages for the repository, users can search by project name, description, domain, species, task, language, and topics.

## Automation

`.github/workflows/refresh.yml` runs on a schedule and:

1. discovers candidate repositories,
2. refreshes metadata for accepted and candidate entries,
3. rebuilds the machine-readable catalog,
4. commits changes when the registry changed.

## Principles

1. **Veterinary relevance first**
2. **Transparent scoring**
3. **Human-reviewable curation**
4. **Open metadata**
5. **No silent mirroring**
6. **Continuous maintenance**
7. **Original project attribution**

## Roadmap

- [x] Registry schema
- [x] Seed VetAI-Lab resources
- [x] GitHub discovery engine
- [x] Metadata enrichment
- [x] Scheduled refresh workflow
- [x] Searchable static catalog
- [ ] DOI / PubMed enrichment
- [ ] Hugging Face model and dataset discovery
- [ ] Automated paper ↔ code ↔ dataset linking
- [ ] Community curator review dashboard
- [ ] Veterinary resource knowledge graph

## License

A project license has intentionally not been selected in this bootstrap. Choose the license that VetAI-Lab wants before the first formal release.
