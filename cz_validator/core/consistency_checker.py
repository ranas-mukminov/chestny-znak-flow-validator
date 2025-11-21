from __future__ import annotations

from typing import List

from cz_validator.models import Code, Discrepancy, DiscrepancyType


class ConsistencyChecker:
    def compare(self, accounting_codes: List[Code], system_codes: List[Code]) -> List[Discrepancy]:
        discrepancies: List[Discrepancy] = []
        system_index = {c.code: c for c in system_codes}
        accounting_index = {c.code: c for c in accounting_codes}

        for code in accounting_codes:
            system_match = system_index.get(code.code)
            if not system_match:
                discrepancies.append(
                    Discrepancy(
                        discrepancy_type=DiscrepancyType.MISSING_IN_SYSTEM,
                        related_codes=[code],
                        description="Код отсутствует в выгрузке из системы маркировки",
                    )
                )
            elif system_match.status != code.status:
                discrepancies.append(
                    Discrepancy(
                        discrepancy_type=DiscrepancyType.STATUS_MISMATCH,
                        related_codes=[code, system_match],
                        description="Статусы кода расходятся между системами",
                    )
                )

        for code in system_codes:
            if code.code not in accounting_index:
                discrepancies.append(
                    Discrepancy(
                        discrepancy_type=DiscrepancyType.MISSING_IN_ACCOUNTING,
                        related_codes=[code],
                        description="Код отсутствует в учётной системе",
                    )
                )

        return discrepancies
