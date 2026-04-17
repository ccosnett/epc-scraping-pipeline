from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class EPCRecord:
    address: str
    postcode: str
    certificate_id: str
    rating: str
    lodgement_date: str
    source_url: str
    scraped_at: str
    extras: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
