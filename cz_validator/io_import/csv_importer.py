from __future__ import annotations

import csv
from pathlib import Path
from typing import List

from cz_validator.io_import.mapping_profiles import MappingProfile
from cz_validator.models import Code, OwnerType, Status


STATUS_MAP = {s.value: s for s in Status}


def _code_from_row(row: dict, profile: MappingProfile) -> Code:
    mapping = profile.column_mappings
    code_value = row.get(mapping.get("code", "code")) or row.get("code")
    status_value = row.get(mapping.get("status")) if "status" in mapping else None
    status_value = status_value or row.get("status")
    status = STATUS_MAP.get(status_value, Status.UNKNOWN)
    owner_raw = row.get(mapping.get("owner_id")) if "owner_id" in mapping else None
    owner_raw = owner_raw or row.get("owner_id")
    gtin_value = row.get(mapping.get("gtin")) if "gtin" in mapping else None
    batch_value = row.get(mapping.get("batch_id")) if "batch_id" in mapping else None
    return Code(
        code=code_value,
        gtin=gtin_value,
        batch_id=batch_value,
        status=status,
        owner_type=_infer_owner_type(owner_raw),
        owner_id=owner_raw,
    )


def _infer_owner_type(owner_id: str | None) -> OwnerType | None:
    if not owner_id:
        return None
    prefix = owner_id.lower()
    if prefix.startswith("prod"):
        return OwnerType.PRODUCER
    if prefix.startswith("whole"):
        return OwnerType.WHOLESALER
    if prefix.startswith("ret"):
        return OwnerType.RETAILER
    return None


def load_producer_export(path: Path, profile: MappingProfile) -> List[Code]:
    codes: List[Code] = []
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row:
                continue
            code_value = row.get(profile.column_mappings.get("code", "code")) or row.get("code")
            if not code_value:
                continue
            codes.append(_code_from_row(row, profile))
    return codes
