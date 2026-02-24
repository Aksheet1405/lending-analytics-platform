from __future__ import annotations

import json
from pathlib import Path
from rich.console import Console

from src.utils.config import settings
from src.utils.io import ensure_dir, write_csv
from src.generators.synthetic_fintech import generate, SynthParams
from src.pipeline.load_to_duckdb import load_csvs_to_duckdb
from src.pipeline.run_dbt import dbt_build
from src.pipeline.quality_gate import run_quality_gate
from src.pipeline.reporting import build_data_dictionary_md, build_anomaly_report_md

console = Console()

def main() -> None:
    ensure_dir(settings.data_dir)
    ensure_dir(settings.artifacts_dir)

    console.rule("[bold]1) Generate extracts[/bold]")
    dfs = generate(SynthParams())
    csv_map: dict[str, str] = {}
    for name, df in dfs.items():
        path = f"{settings.data_dir}/{name}.csv"
        write_csv(df, path)
        csv_map[name] = path
        console.print(f"Wrote {path} ({len(df):,} rows)")

    console.rule("[bold]2) Load to DuckDB[/bold]")
    load_csvs_to_duckdb(settings.duckdb_path, csv_map)

    console.rule("[bold]3) Transform + test (dbt)[/bold]")
    dbt_build("dbt")

    console.rule("[bold]4) Quality gate[/bold]")
    qr = run_quality_gate(settings.duckdb_path)
    qpath = Path(settings.artifacts_dir) / "quality_report.json"
    qpath.write_text(json.dumps({"ok": qr.ok, "checks": qr.checks}, indent=2))
    console.print(f"Quality report → {qpath}")

    if not qr.ok:
        raise SystemExit("Quality gate failed. See artifacts/quality_report.json")

    console.rule("[bold]5) Run report[/bold]")
    (Path(settings.artifacts_dir) / "data_dictionary.md").write_text(
        build_data_dictionary_md(settings.duckdb_path, "mart_lending_funnel")
    )
    (Path(settings.artifacts_dir) / "anomaly_report.md").write_text(
        build_anomaly_report_md(settings.duckdb_path)
    )
    console.print("Wrote artifacts/data_dictionary.md and artifacts/anomaly_report.md")

    console.rule("[bold green]Done[/bold green]")
    console.print(f"DuckDB warehouse: {settings.duckdb_path}")

if __name__ == "__main__":
    main()
