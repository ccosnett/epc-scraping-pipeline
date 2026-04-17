from __future__ import annotations

import argparse
from pathlib import Path

from epc_scraping_pipeline.config import PipelineConfig
from epc_scraping_pipeline.pipeline import run_pipeline
from epc_scraping_pipeline.sources.mock_source import MockEPCSource


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="epc-pipeline",
        description="Run the EPC scraping pipeline starter workflow.",
    )
    parser.add_argument(
        "command",
        choices=["run"],
        help="Pipeline command to execute.",
    )
    parser.add_argument(
        "--source",
        choices=["mock"],
        default="mock",
        help="Named source implementation to run.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=2,
        help="Maximum number of mock records to emit.",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Project root used for default data directories.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    config = PipelineConfig.from_env(root=Path(args.root).resolve())

    if args.command == "run":
        source = MockEPCSource(limit=args.limit)
        result = run_pipeline(source=source, config=config)
        print(f"Wrote {result.record_count} record(s) to {result.output_path}")
        return 0

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
