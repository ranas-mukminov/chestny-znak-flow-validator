from __future__ import annotations

from typing import List

from cz_validator.models import Code, Discrepancy, DiscrepancyType, Status


class StatusChecker:
    def validate(self, codes: List[Code]) -> List[Discrepancy]:
        discrepancies: List[Discrepancy] = []
        for code in codes:
            if code.status == Status.WITHDRAWN:
                discrepancies.append(
                    Discrepancy(
                        discrepancy_type=DiscrepancyType.STATUS_MISMATCH,
                        related_codes=[code],
                        technical_details="Withdrawn state detected without full history",
                        description="Код выведен из оборота, требуется проверка предыдущих статусов",
                    )
                )
        return discrepancies
