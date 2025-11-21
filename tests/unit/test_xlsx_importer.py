from pathlib import Path

from openpyxl import Workbook

from cz_validator.io_import.xlsx_importer import load_wholesaler_export
from cz_validator.io_import.mapping_profiles import MappingProfile


def test_load_wholesaler_export(tmp_path: Path):
    wb = Workbook()
    ws = wb.active
    ws.append(["code", "gtin", "batch_id", "status", "owner_id"])
    ws.append(["WX1", "555", "B2", "IN_TRANSIT", "WHOLE"])
    ws.append(["WX2", "555", "B2", "AT_RETAIL", "WHOLE"])
    xlsx_path = tmp_path / "wholesaler.xlsx"
    wb.save(xlsx_path)

    profile = MappingProfile(
        column_mappings={
            "code": "code",
            "gtin": "gtin",
            "batch_id": "batch_id",
            "status": "status",
            "owner_id": "owner_id",
        }
    )
    codes = load_wholesaler_export(xlsx_path, profile)
    assert [c.code for c in codes] == ["WX1", "WX2"]
    assert codes[0].status.name == "IN_TRANSIT"
