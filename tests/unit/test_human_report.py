from cz_validator.ai.human_report import generate_report
from cz_validator.ai.problem_clustering import ProblemCluster


def test_generate_report_contains_sections():
    clusters = [ProblemCluster(type_name="STATUS_MISMATCH", count=2, sample_codes=["A", "B"])]
    output = generate_report({"total_codes": 2}, clusters)
    assert "Итоги проверки" in output
    assert "STATUS_MISMATCH" in output
