# Veterinary relevance scoring

VetHub's first release uses an intentionally transparent lexical relevance score.

The automated score is a **triage signal**, not a scientific claim and not a substitute for curator review.

## Inputs

The scorer can use:

- repository name
- GitHub description
- repository topics
- a bounded portion of the README

## Logic

Strong veterinary terms contribute more weight than broad animal or One Health terms. Known false-positive patterns can receive negative weights.

The resulting raw score is converted to a bounded `0–1` score.

## Why not use an LLM immediately?

A deterministic first-stage scorer is:

- reproducible,
- inspectable,
- inexpensive,
- easy for contributors to audit,
- suitable for scheduled GitHub Actions.

A semantic classifier can later be added as a second-stage reviewer while retaining the lexical score for provenance.
