from cz_validator.core.graph_builder import GraphBuilder
from cz_validator.models import Code, Movement, OwnerType, Status


def test_graph_builder_creates_paths():
    codes = [
        Code(code="C1", gtin="1", batch_id="B", status=Status.INTRODUCED, owner_type=OwnerType.PRODUCER, owner_id="P"),
        Code(code="C2", gtin="1", batch_id="B", status=Status.INTRODUCED, owner_type=OwnerType.PRODUCER, owner_id="P"),
    ]
    movements = [
        Movement(from_owner_id="P", to_owner_id="W", codes=["C1", "C2"], document={"number": "D1"}, source="ERP"),
        Movement(from_owner_id="W", to_owner_id="R", codes=["C1"], document={"number": "D2"}, source="ERP"),
    ]
    builder = GraphBuilder()
    graph = builder.build(codes, movements)
    assert graph.get_path("C1") == ["P", "W", "R"]
    assert graph.get_path("C2") == ["P", "W"]
