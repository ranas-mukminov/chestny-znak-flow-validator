from cz_validator.core.status_checker import StatusChecker
from cz_validator.models import Code, OwnerType, Status


def test_status_checker_flags_invalid_transition():
    codes = [
        Code(code="C1", gtin="1", batch_id="B", status=Status.WITHDRAWN, owner_type=OwnerType.RETAILER, owner_id="R"),
    ]
    checker = StatusChecker()
    discrepancies = checker.validate(codes)
    assert discrepancies
    assert discrepancies[0].discrepancy_type.name == "STATUS_MISMATCH"
