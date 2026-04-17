import json
import tempfile
import unittest
from pathlib import Path

from epc_scraping_pipeline.config import PipelineConfig
from epc_scraping_pipeline.pipeline import run_pipeline
from epc_scraping_pipeline.sources.mock_source import MockEPCSource


class PipelineTestCase(unittest.TestCase):
    def test_pipeline_writes_expected_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            config = PipelineConfig(
                raw_dir=tmp_path / "raw",
                processed_dir=tmp_path / "processed",
                source_name="test-source",
                output_basename="test_records",
            )

            result = run_pipeline(source=MockEPCSource(limit=2), config=config)

            self.assertEqual(result.record_count, 2)
            self.assertTrue(result.output_path.exists())

            payload = json.loads(result.output_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["source_name"], "test-source")
            self.assertEqual(payload["record_count"], 2)
            self.assertEqual(len(payload["records"]), 2)
            self.assertEqual(payload["records"][0]["certificate_id"], "EPC-0001")


if __name__ == "__main__":
    unittest.main()
