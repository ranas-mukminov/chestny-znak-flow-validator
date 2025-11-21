from __future__ import annotations

from defusedxml import ElementTree as ET
from pathlib import Path
from typing import List

from cz_validator.io_import.csv_importer import _infer_owner_type
from cz_validator.io_import.mapping_profiles import MappingProfile
from cz_validator.models import Code, Status


STATUS_MAP = {s.value: s for s in Status}


def load_retail_export(path: Path, profile: MappingProfile) -> List[Code]:
    tree = ET.parse(path)
    root = tree.getroot()
    codes: List[Code] = []
    for movement in root.findall(".//movement"):
        code_val = _get_tag_text(movement, profile.tag_mappings.get("code", "code"))
        if not code_val:
            continue
        status_val = _get_tag_text(movement, profile.tag_mappings.get("status", "status"))
        status = STATUS_MAP.get(status_val, Status.UNKNOWN)
        owner_raw = _get_tag_text(movement, profile.tag_mappings.get("owner_id", "owner_id"))
        codes.append(
            Code(
                code=code_val,
                gtin=_get_tag_text(movement, profile.tag_mappings.get("gtin", "gtin")),
                batch_id=_get_tag_text(movement, profile.tag_mappings.get("batch_id", "batch_id")),
                status=status,
                owner_type=_infer_owner_type(owner_raw),
                owner_id=owner_raw,
            )
        )
    return codes


def _get_tag_text(parent: ET.Element, tag: str | None) -> str | None:
    if not tag:
        return None
    node = parent.find(tag)
    return node.text if node is not None else None
