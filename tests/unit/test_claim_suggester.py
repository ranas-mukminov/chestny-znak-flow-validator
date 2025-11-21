from cz_validator.ai.claim_suggester import ClaimSuggester
from cz_validator.ai.problem_clustering import ProblemCluster


def test_claim_suggester_generates_text():
    suggester = ClaimSuggester()
    cluster = ProblemCluster(type_name="MISSING_IN_SYSTEM", count=1, sample_codes=["X"], counterparty="WHOLE")
    text = suggester.generate(cluster)
    assert "WHOLE" in text
    assert "MISSING_IN_SYSTEM" in text
