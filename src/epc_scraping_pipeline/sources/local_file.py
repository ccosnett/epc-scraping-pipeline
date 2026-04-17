from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable

from epc_scraping_pipeline.models import EPCRecord
from epc_scraping_pipeline.sources.base import SourceError


FIELD_ALIASES = {
    "address": ("address", "full_address", "property_address"),
    "postcode": ("postcode", "postal_code", "post_code"),
    "certificate_id": ("certificate_id", "lmk_key", "certificate_number"),
    "rating": (
        "rating",
        "current_energy_rating",
        "current_rating",
        "energy_rating_current",
    ),
    "lodgement_date": (
        "lodgement_date",
        "inspection_date",
        "date_of_assessment",
        "date_of_inspection",
    ),
    "source_url": ("source_url", "url", "listing_url"),
    "scraped_at": ("scraped_at", "retrieved_at", "collected_at"),
}


@dataclass(slots=True)
class LocalFileEPCSource:
    input_path: Path

    def fetch_records(self) -> list[EPCRecord]:
        paths = self._resolve_paths()
        records: list[EPCRecord] = []

        for path in paths:
            if path.suffix.lower() == ".json":
                rows = self._load_json(path)
            elif path.suffix.lower() == ".csv":
                rows = self._load_csv(path)
            else:
                raise SourceError(f"Unsupported input type: {path.suffix} for {path}")

            records.extend(self._normalize_rows(rows, path))

        return records

    def _resolve_paths(self) -> list[Path]:
        if not self.input_path.exists():
            raise SourceError(f"Input path does not exist: {self.input_path}")

        if self.input_path.is_file():
            return [self.input_path]

        paths = sorted(
            path
            for pattern in ("*.json", "*.csv")
            for path in self.input_path.glob(pattern)
            if path.is_file()
        )
        if not paths:
            raise SourceError(f"No .json or .csv files found in {self.input_path}")
        return paths

    def _load_json(self, path: Path) -> list[dict[str, Any]]:
        payload = json.loads(path.read_text(encoding="utf-8"))

        if isinstance(payload, dict) and "records" in payload:
            payload = payload["records"]

        if not isinstance(payload, list):
            raise SourceError(f"Expected a JSON array or records payload in {path}")

        rows: list[dict[str, Any]] = []
        for item in payload:
            if not isinstance(item, dict):
                raise SourceError(f"JSON records must be objects in {path}")
            rows.append(item)
        return rows

    def _load_csv(self, path: Path) -> list[dict[str, Any]]:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                raise SourceError(f"CSV file is missing a header row: {path}")
            return [dict(row) for row in reader]

    def _normalize_rows(self, rows: Iterable[dict[str, Any]], path: Path) -> list[EPCRecord]:
        normalized: list[EPCRecord] = []
        timestamp = datetime.now(UTC).isoformat()

        for index, raw_row in enumerate(rows, start=1):
            cleaned = {self._clean_key(key): value for key, value in raw_row.items()}
            mapped: dict[str, Any] = {}

            for target_field, aliases in FIELD_ALIASES.items():
                mapped[target_field] = self._extract_first(cleaned, aliases)

            missing = [
                field
                for field in ("address", "postcode", "certificate_id", "rating", "lodgement_date")
                if not mapped.get(field)
            ]
            if missing:
                missing_text = ", ".join(missing)
                raise SourceError(
                    f"Missing required field(s) {missing_text} in {path.name} row {index}"
                )

            source_url = mapped["source_url"] or path.resolve().as_uri()
            scraped_at = mapped["scraped_at"] or timestamp
            consumed_keys = {
                alias
                for aliases in FIELD_ALIASES.values()
                for alias in (self._clean_key(name) for name in aliases)
            }
            extras = {
                key: value
                for key, value in cleaned.items()
                if key not in consumed_keys and value not in ("", None)
            }

            normalized.append(
                EPCRecord(
                    address=str(mapped["address"]).strip(),
                    postcode=str(mapped["postcode"]).strip(),
                    certificate_id=str(mapped["certificate_id"]).strip(),
                    rating=str(mapped["rating"]).strip(),
                    lodgement_date=str(mapped["lodgement_date"]).strip(),
                    source_url=str(source_url).strip(),
                    scraped_at=str(scraped_at).strip(),
                    extras=extras,
                )
            )

        return normalized

    def _extract_first(self, row: dict[str, Any], aliases: Iterable[str]) -> Any:
        for alias in aliases:
            cleaned_alias = self._clean_key(alias)
            value = row.get(cleaned_alias)
            if value not in ("", None):
                return value
        return None

    def _clean_key(self, key: str | None) -> str:
        return (key or "").strip().lower().replace("-", "_").replace(" ", "_")
