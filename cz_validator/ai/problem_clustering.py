from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from cz_validator.models import Discrepancy


@dataclass
class ProblemCluster:
    type_name: str
    count: int
    sample_codes: List[str]
    counterparty: Optional[str] = None


class ProblemClustering:
    def group(self, discrepancies: List[Discrepancy]) -> List[ProblemCluster]:
        buckets = {}
        for d in discrepancies:
            key = d.discrepancy_type.value
            buckets.setdefault(key, []).append(d)
        clusters: List[ProblemCluster] = []
        for key, items in buckets.items():
            sample_codes = [c.code for d in items for c in d.related_codes][:3]
            clusters.append(ProblemCluster(type_name=key, count=len(items), sample_codes=sample_codes))
        return clusters
