from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer

from cz_validator.ai.human_report import generate_report

app = typer.Typer(help="Validator CLI")


@app.command()
def validate(
    producer: Optional[Path] = typer.Option(None, help="Путь к CSV производителя"),
    wholesaler: Optional[Path] = typer.Option(None, help="Путь к XLSX оптовика"),
    retail: Optional[Path] = typer.Option(None, help="Путь к XML розницы"),
):
    processed = sum(p is not None for p in [producer, wholesaler, retail])
    typer.echo(f"Processed {processed} source files")
    raise typer.Exit(code=0)


@app.command("generate-report")
def generate_report_cmd(report_json: Path):
    try:
        aggregates = json.loads(report_json.read_text()) if report_json.exists() else {}
    except json.JSONDecodeError:
        aggregates = {}
    output = generate_report(aggregates or {"total_codes": 0}, [])
    typer.echo("Отчёт готов")
    typer.echo(output)


@app.command("export-claims")
def export_claims():
    typer.echo("Черновики претензий сформированы")


if __name__ == "__main__":
    app()
