from __future__ import annotations

from typing import Protocol

from epc_scraping_pipeline.models import EPCRecord


class EPCSource(Protocol):
    def fetch_records(self) -> list[EPCRecord]:
        """Return normalized EPC records from a source."""


class SourceError(Exception):
    """Raised when a source cannot produce valid EPC records."""
