from cz_validator.ai.problem_clustering import ProblemClustering
from cz_validator.models import Discrepancy, DiscrepancyType


def test_problem_clustering_groups_by_type():
    discrepancies = [
        Discrepancy(discrepancy_type=DiscrepancyType.MISSING_IN_SYSTEM, description="missing"),
        Discrepancy(discrepancy_type=DiscrepancyType.MISSING_IN_SYSTEM, description="missing2"),
        Discrepancy(discrepancy_type=DiscrepancyType.STATUS_MISMATCH, description="status"),
    ]
    clustering = ProblemClustering()
    clusters = clustering.group(discrepancies)
    assert len(clusters) == 2
    assert clusters[0].count >= 1
