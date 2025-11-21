from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict

import yaml


@dataclass
class MappingProfile:
    column_mappings: Dict[str, str] = field(default_factory=dict)
    field_types: Dict[str, Any] = field(default_factory=dict)
    tag_mappings: Dict[str, str] = field(default_factory=dict)


def load_profile(path: Path) -> "MappingProfile":
    data = yaml.safe_load(path.read_text())
    return MappingProfile(
        column_mappings=data.get("column_mappings", {}),
        field_types=data.get("field_types", {}),
        tag_mappings=data.get("tag_mappings", {}),
    )


DEFAULT_PROFILES = {
    "1c_ut": MappingProfile(
        column_mappings={
            "code": "Код",
            "gtin": "GTIN",
            "batch_id": "Партия",
            "status": "Статус",
            "owner_id": "Владелец",
        }
    )
}
