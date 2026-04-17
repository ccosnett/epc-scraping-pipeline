# EPC Scraping Pipeline

Data scraping pipeline for EPC certificates.

## Overview

This repository is a starter home for collecting, normalizing, and working with EPC certificate data. The initial scaffold includes a small CLI, a normalized EPC record model, and a mocked source so the pipeline can run before a live source is integrated.

## Project Layout

- `src/epc_scraping_pipeline/` contains the package code.
- `src/epc_scraping_pipeline/sources/` is where source-specific connectors live.
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

To run the starter verification suite:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Next Steps

- Replace the mock source with a real EPC data connector.
- Add request throttling, retry logic, and access-policy guardrails.
- Introduce schema validation and storage targets such as Postgres or object storage.
