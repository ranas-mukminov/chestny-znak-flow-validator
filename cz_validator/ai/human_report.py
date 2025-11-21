from __future__ import annotations

from typing import Dict, List

from cz_validator.ai.problem_clustering import ProblemCluster


def generate_report(aggregates: Dict[str, int], clusters: List[ProblemCluster]) -> str:
    lines = ["# Итоги проверки", ""]
    for key, value in aggregates.items():
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("## Критичные проблемы")
    for cluster in clusters:
        lines.append(f"- {cluster.type_name}: {cluster.count} (коды: {', '.join(cluster.sample_codes)})")
    lines.append("")
    lines.append("## Рекомендации по исправлению")
    lines.append("- Уточните цепочку движения и повторите обмен данными.")
    return "\n".join(lines)
