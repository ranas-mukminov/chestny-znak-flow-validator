from pathlib import Path

from typer.testing import CliRunner

from cz_validator.cli.main import app


runner = CliRunner()


def test_validate_command_runs(tmp_path: Path):
    producer = tmp_path / "p.csv"
    producer.write_text("code\nA1\n")
    result = runner.invoke(
        app,
        [
            "validate",
            "--producer",
            str(producer),
        ],
    )
    assert result.exit_code == 0
    assert "Processed" in result.stdout


def test_generate_report_command(tmp_path: Path):
    report_json = tmp_path / "report.json"
    report_json.write_text("{}")
    result = runner.invoke(app, ["generate-report", str(report_json)])
    assert result.exit_code == 0
    assert "Отчёт" in result.stdout
