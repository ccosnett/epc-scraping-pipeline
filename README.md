# EPC Scraping Pipeline

Data scraping pipeline for EPC certificates.

## Overview

This repository is a starter home for collecting, normalizing, and working with EPC certificate data. The initial scaffold includes a small CLI, a normalized EPC record model, a file-backed source for EPC exports, and a mocked source so the pipeline can run before a live source is integrated.

The uploaded project note in [solving_a_problem_in_the_UK_property_instustry.pdf](/Users/johncosnett/PycharmProjects/epc-scraping-pipeline/solving_a_problem_in_the_UK_property_instustry.pdf) describes the broader UK property workflow problem well: EPC information is often present in awkward, semi-structured formats, so the first useful milestone is reliable normalization.

## Project Layout

- `src/epc_scraping_pipeline/` contains the package code.
- `src/epc_scraping_pipeline/sources/` is where source-specific connectors live.
- `examples/` contains a starter EPC export file for local ingestion.
- `data/raw/` is reserved for captured raw responses or files.
- `data/processed/` stores normalized pipeline output.
- `tests/` contains starter verification coverage.

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
epc-pipeline run --source mock --limit 2
```

The starter command writes a timestamped JSON payload into `data/processed/`.

To normalize a local EPC-style export:

```bash
epc-pipeline run --source file --input examples/sample_epc_export.csv
```

The file source currently accepts `.csv` and `.json` inputs. JSON can be either a list of record objects or an object with a top-level `records` array.

To run the starter verification suite:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Next Steps

- Add an HTTP-backed EPC source that captures raw responses into `data/raw/`.
- Add request throttling, retry logic, and access-policy guardrails.
- Introduce schema validation and storage targets such as Postgres or object storage.
