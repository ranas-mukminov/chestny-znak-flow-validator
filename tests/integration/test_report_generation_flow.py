from cz_validator.ai.human_report import generate_report
from cz_validator.ai.problem_clustering import ProblemClustering
from cz_validator.models import Discrepancy, DiscrepancyType


def test_report_generation_flow():
    discrepancies = [
        Discrepancy(discrepancy_type=DiscrepancyType.STATUS_MISMATCH, description="bad status")
    ]
    clusters = ProblemClustering().group(discrepancies)
    report = generate_report({"total_codes": 1}, clusters)
    assert "Критичные проблемы" in report
    assert "STATUS_MISMATCH" in report
