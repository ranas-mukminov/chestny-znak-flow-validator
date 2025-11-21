from __future__ import annotations

from collections import defaultdict
from typing import List

from cz_validator.models import Batch, Discrepancy, DiscrepancyType


class QuantityChecker:
    def validate(self, batches: List[Batch]) -> List[Discrepancy]:
        discrepancies: List[Discrepancy] = []
        totals = defaultdict(list)
        for batch in batches:
            totals[batch.batch_id].append(batch.quantity or 0)
        for batch_id, quantities in totals.items():
            if len(set(quantities)) > 1:
                discrepancies.append(
                    Discrepancy(
                        discrepancy_type=DiscrepancyType.QUANTITY_MISMATCH,
                        description=f"Несостыкованные количества по партии {batch_id}",
                    )
                )
        return discrepancies
