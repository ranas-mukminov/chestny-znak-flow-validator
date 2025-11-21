from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from cz_validator.ai.problem_clustering import ProblemCluster


class AIProvider(ABC):
    @abstractmethod
    def cluster_problems(self, discrepancies) -> List[ProblemCluster]:
        raise NotImplementedError

    @abstractmethod
    def generate_management_report(self, aggregates, clusters) -> str:
        raise NotImplementedError

    @abstractmethod
    def generate_claims(self, cluster: ProblemCluster, counterparty: str | None = None) -> str:
        raise NotImplementedError


class NoopAIProvider(AIProvider):
    def cluster_problems(self, discrepancies) -> List[ProblemCluster]:
        from cz_validator.ai.problem_clustering import ProblemClustering

        return ProblemClustering().group(discrepancies)

    def generate_management_report(self, aggregates, clusters) -> str:
        from cz_validator.ai.human_report import generate_report

        return generate_report(aggregates, clusters)

    def generate_claims(self, cluster: ProblemCluster, counterparty: str | None = None) -> str:
        from cz_validator.ai.claim_suggester import ClaimSuggester

        return ClaimSuggester().generate(cluster, counterparty)
