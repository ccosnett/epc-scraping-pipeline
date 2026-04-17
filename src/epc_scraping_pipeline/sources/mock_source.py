from __future__ import annotations

from datetime import UTC, datetime

from epc_scraping_pipeline.models import EPCRecord


class MockEPCSource:
    """Temporary source used until a real EPC integration is chosen."""

    def __init__(self, limit: int = 2) -> None:
        self.limit = limit

    def fetch_records(self) -> list[EPCRecord]:
        timestamp = datetime.now(UTC).isoformat()
        sample_records = [
            EPCRecord(
                address="1 Example Street",
                postcode="D02 TEST",
                certificate_id="EPC-0001",
                rating="B",
                lodgement_date="2026-04-01",
                source_url="https://example.com/epc/0001",
                scraped_at=timestamp,
                extras={"property_type": "Apartment", "floor_area_m2": 82},
            ),
            EPCRecord(
                address="2 Example Avenue",
                postcode="D04 TEST",
                certificate_id="EPC-0002",
                rating="C",
                lodgement_date="2026-04-02",
                source_url="https://example.com/epc/0002",
                scraped_at=timestamp,
                extras={"property_type": "Detached", "floor_area_m2": 121},
            ),
            EPCRecord(
                address="3 Example Close",
                postcode="D06 TEST",
                certificate_id="EPC-0003",
                rating="A",
                lodgement_date="2026-04-03",
                source_url="https://example.com/epc/0003",
                scraped_at=timestamp,
                extras={"property_type": "Terraced", "floor_area_m2": 94},
            ),
        ]
        return sample_records[: max(self.limit, 0)]
