from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from epc_scraping_pipeline.config import PipelineConfig
from epc_scraping_pipeline.models import EPCRecord
from epc_scraping_pipeline.sources.base import EPCSource


@dataclass(slots=True)
class PipelineResult:
    output_path: Path
    record_count: int


def run_pipeline(source: EPCSource, config: PipelineConfig) -> PipelineResult:
    config.ensure_directories()
    records = [record.to_dict() for record in source.fetch_records()]
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    output_path = config.processed_dir / f"{config.output_basename}_{timestamp}.json"
    payload = {
        "source_name": config.source_name,
        "generated_at": timestamp,
        "record_count": len(records),
        "records": records,
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return PipelineResult(output_path=output_path, record_count=len(records))
