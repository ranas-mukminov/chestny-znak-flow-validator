from cz_validator.core.quantity_checker import QuantityChecker
from cz_validator.models import Batch


def test_quantity_checker_detects_mismatch():
    batches = [
        Batch(batch_id="B1", quantity=10, owner_id="P"),
        Batch(batch_id="B1", quantity=7, owner_id="W"),
    ]
    checker = QuantityChecker()
    discrepancies = checker.validate(batches)
    assert discrepancies
    assert discrepancies[0].discrepancy_type.name == "QUANTITY_MISMATCH"
