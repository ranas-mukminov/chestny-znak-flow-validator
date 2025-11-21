from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel


class DiscrepancyDTO(BaseModel):
    discrepancy_type: str
    description: Optional[str]
    codes: List[str] = []


class ValidationResponse(BaseModel):
    summary: str
    discrepancies: List[DiscrepancyDTO]
