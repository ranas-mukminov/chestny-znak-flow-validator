from cz_validator.core.consistency_checker import ConsistencyChecker
from cz_validator.models import Code, DiscrepancyType, OwnerType, Status


def test_consistency_checker_detects_missing():
    accounting = [
        Code(code="A1", gtin="1", batch_id="B", status=Status.INTRODUCED, owner_type=OwnerType.PRODUCER, owner_id="P"),
    ]
    system = []
    checker = ConsistencyChecker()
    discrepancies = checker.compare(accounting, system)
    assert any(d.discrepancy_type == DiscrepancyType.MISSING_IN_SYSTEM for d in discrepancies)
