from cz_validator.core.consistency_checker import ConsistencyChecker
from cz_validator.core.graph_builder import GraphBuilder
from cz_validator.core.status_checker import StatusChecker
from cz_validator.models import Code, Movement, OwnerType, Status


def test_full_flow_detects_no_errors():
    codes = [
        Code(code="X1", gtin="1", batch_id="B", status=Status.INTRODUCED, owner_type=OwnerType.PRODUCER, owner_id="PROD"),
        Code(code="X1", gtin="1", batch_id="B", status=Status.IN_TRANSIT, owner_type=OwnerType.WHOLESALER, owner_id="WHOLE"),
        Code(code="X1", gtin="1", batch_id="B", status=Status.AT_RETAIL, owner_type=OwnerType.RETAILER, owner_id="RET"),
    ]
    movements = [
        Movement(from_owner_id="PROD", to_owner_id="WHOLE", codes=["X1"], document={}, source="ERP"),
        Movement(from_owner_id="WHOLE", to_owner_id="RET", codes=["X1"], document={}, source="ERP"),
    ]
    status_discrepancies = StatusChecker().validate(codes)
    assert not status_discrepancies
    graph = GraphBuilder().build(codes, movements)
    assert graph.get_path("X1") == ["PROD", "WHOLE", "RET"]
    consistency = ConsistencyChecker().compare([codes[0]], [codes[-1]])
    assert consistency
