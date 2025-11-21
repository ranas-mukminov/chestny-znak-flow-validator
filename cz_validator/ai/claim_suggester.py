from __future__ import annotations

from cz_validator.ai.problem_clustering import ProblemCluster


class ClaimSuggester:
    def generate(self, cluster: ProblemCluster, counterparty: str | None = None) -> str:
        counterpart = counterparty or cluster.counterparty or "контрагент"
        return (
            f"Уважаемая команда {counterpart},\n"
            f"Обнаружена проблема {cluster.type_name} по {cluster.count} позициям. "
            f"Пожалуйста, проверьте коды: {', '.join(cluster.sample_codes)}."
        )
