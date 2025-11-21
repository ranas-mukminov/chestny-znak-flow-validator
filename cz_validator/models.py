from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class Status(Enum):
    ISSUED = "ISSUED"
    INTRODUCED = "INTRODUCED"
    IN_TRANSIT = "IN_TRANSIT"
    AT_RETAIL = "AT_RETAIL"
    WITHDRAWN = "WITHDRAWN"
    UNKNOWN = "UNKNOWN"


class OwnerType(Enum):
    PRODUCER = "PRODUCER"
    WHOLESALER = "WHOLESALER"
    RETAILER = "RETAILER"


@dataclass
class Code:
    code: str
    gtin: Optional[str] = None
    batch_id: Optional[str] = None
    status: Status = Status.UNKNOWN
    owner_type: Optional[OwnerType] = None
    owner_id: Optional[str] = None


@dataclass
class Movement:
    from_owner_id: str
    to_owner_id: str
    codes: List[str] = field(default_factory=list)
    document: Dict[str, str] = field(default_factory=dict)
    source: Optional[str] = None


@dataclass
class Batch:
    batch_id: str
    codes: List[Code] = field(default_factory=list)
    owner_id: Optional[str] = None
    quantity: Optional[int] = None


class DiscrepancyType(Enum):
    MISSING_IN_SYSTEM = "MISSING_IN_SYSTEM"
    MISSING_IN_ACCOUNTING = "MISSING_IN_ACCOUNTING"
    STATUS_MISMATCH = "STATUS_MISMATCH"
    QUANTITY_MISMATCH = "QUANTITY_MISMATCH"
    CHAIN_BREAK = "CHAIN_BREAK"


@dataclass
class Discrepancy:
    discrepancy_type: DiscrepancyType
    related_codes: List[Code] = field(default_factory=list)
    related_batches: List[Batch] = field(default_factory=list)
    related_movements: List[Movement] = field(default_factory=list)
    technical_details: Optional[str] = None
    description: Optional[str] = None
