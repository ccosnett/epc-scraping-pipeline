import json
import tempfile
import unittest
from pathlib import Path

from epc_scraping_pipeline.config import PipelineConfig
from epc_scraping_pipeline.pipeline import run_pipeline
from epc_scraping_pipeline.sources.local_file import LocalFileEPCSource
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

    def test_local_file_source_normalizes_csv_records(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            input_path = tmp_path / "epc_export.csv"
            input_path.write_text(
                "\n".join(
                    [
                        "full_address,postal_code,lmk_key,current_energy_rating,lodgement_date,listing_url,property_type",
                        "1 Test Street,D01 TEST,EPC-9001,A,2026-04-10,https://example.com/9001,Apartment",
                        "2 Test Avenue,D02 TEST,EPC-9002,C,2026-04-11,https://example.com/9002,Detached",
                    ]
                ),
                encoding="utf-8",
            )
            config = PipelineConfig(
                raw_dir=tmp_path / "raw",
                processed_dir=tmp_path / "processed",
                source_name="local-file-test",
                output_basename="local_file_records",
            )

            result = run_pipeline(source=LocalFileEPCSource(input_path=input_path), config=config)

            payload = json.loads(result.output_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["record_count"], 2)
            self.assertEqual(payload["records"][0]["certificate_id"], "EPC-9001")
            self.assertEqual(payload["records"][0]["rating"], "A")
            self.assertEqual(payload["records"][0]["extras"]["property_type"], "Apartment")


if __name__ == "__main__":
    unittest.main()
