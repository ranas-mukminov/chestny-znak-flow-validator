from __future__ import annotations

from typing import Any, List

from cz_validator.io_import.csv_importer import _infer_owner_type
from cz_validator.models import Code, Status


STATUS_MAP = {s.value: s for s in Status}


def parse_api_response(payload: Any) -> List[Code]:
    items = payload.get("items", []) if isinstance(payload, dict) else []
    codes: List[Code] = []
    for item in items:
        status_value = item.get("status")
        status = STATUS_MAP.get(status_value, Status.UNKNOWN)
        owner_raw = item.get("owner")
        codes.append(
            Code(
                code=item.get("code"),
                gtin=item.get("gtin"),
                batch_id=item.get("batch_id"),
                status=status,
                owner_type=_infer_owner_type(owner_raw),
                owner_id=owner_raw,
            )
        )
    return codes
