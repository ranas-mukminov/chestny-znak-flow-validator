from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from cz_validator.models import Movement


@dataclass
class CodePathGraph:
    adjacency: Dict[str, List[str]] = field(default_factory=dict)

    def get_path(self, code: str) -> List[str]:
        return self.adjacency.get(code, [])


class GraphBuilder:
    def build(self, codes, movements: List[Movement]) -> CodePathGraph:
        graph = CodePathGraph()
        for movement in movements:
            for code in movement.codes:
                path = graph.adjacency.setdefault(code, [])
                if movement.from_owner_id not in path:
                    path.append(movement.from_owner_id)
                if movement.to_owner_id not in path:
                    path.append(movement.to_owner_id)
        return graph
