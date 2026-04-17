from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class PipelineConfig:
    raw_dir: Path
    processed_dir: Path
    source_name: str = "epc-certificates"
    output_basename: str = "epc_records"

    @classmethod
    def from_env(cls, root: Path | None = None) -> "PipelineConfig":
        base_root = root or Path.cwd()
        raw_dir = Path(os.getenv("EPC_PIPELINE_RAW_DIR", base_root / "data" / "raw"))
        processed_dir = Path(
            os.getenv("EPC_PIPELINE_PROCESSED_DIR", base_root / "data" / "processed")
        )
        return cls(raw_dir=raw_dir, processed_dir=processed_dir)

    def ensure_directories(self) -> None:
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
