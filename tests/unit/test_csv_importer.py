import csv
from pathlib import Path

from cz_validator.io_import.csv_importer import load_producer_export
from cz_validator.io_import.mapping_profiles import MappingProfile


def test_load_producer_export_parses_codes(tmp_path: Path):
    csv_path = tmp_path / "producer.csv"
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["code", "gtin", "batch_id", "status", "owner_id"],
        )
        writer.writeheader()
        writer.writerow(
            {
                "code": "CODE1",
                "gtin": "12345",
                "batch_id": "B1",
                "status": "INTRODUCED",
                "owner_id": "PROD",
            }
        )
        writer.writerow(
            {
                "code": "CODE2",
                "gtin": "12345",
                "batch_id": "B1",
                "status": "IN_TRANSIT",
                "owner_id": "PROD",
            }
        )
    profile = MappingProfile(
        column_mappings={
            "code": "code",
            "gtin": "gtin",
            "batch_id": "batch_id",
            "status": "status",
            "owner_id": "owner_id",
        }
    )
    codes = load_producer_export(csv_path, profile)
    assert len(codes) == 2
    assert codes[0].code == "CODE1"
    assert codes[1].status.name == "IN_TRANSIT"


def test_missing_columns_are_skipped(tmp_path: Path):
    csv_path = tmp_path / "producer_missing.csv"
    csv_path.write_text("code,gtin\nA,123\n")
    profile = MappingProfile(column_mappings={"code": "code"})
    codes = load_producer_export(csv_path, profile)
    assert len(codes) == 1
    assert codes[0].gtin is None
