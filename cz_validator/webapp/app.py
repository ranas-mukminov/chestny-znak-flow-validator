from __future__ import annotations

from fastapi import FastAPI, UploadFile

from cz_validator.ai.ai_provider import NoopAIProvider
from cz_validator.webapp.schemas import DiscrepancyDTO, ValidationResponse

app = FastAPI(title="chestny-znak-flow-validator")
provider = NoopAIProvider()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/validate", response_model=ValidationResponse)
async def validate(producer: UploadFile | None = None) -> ValidationResponse:
    _ = producer  # files are not persisted
    discrepancies = []
    clusters = provider.cluster_problems(discrepancies)
    summary = "Нет данных для проверки" if not discrepancies else "Найдены несоответствия"
    dtos = [DiscrepancyDTO(discrepancy_type=c.type_name, description=None, codes=c.sample_codes) for c in clusters]
    return ValidationResponse(summary=summary, discrepancies=dtos)
