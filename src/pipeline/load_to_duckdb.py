from __future__ import annotations

from pathlib import Path
import duckdb
from rich.console import Console

console = Console()

def load_csvs_to_duckdb(duckdb_path: str, table_to_csv: dict[str, str]) -> None:
    Path(duckdb_path).parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(duckdb_path)

    for table, csv_path in table_to_csv.items():
        console.print(f"[bold]Load[/bold] {csv_path} → raw_{table}")
        con.execute(
            f"CREATE OR REPLACE TABLE raw_{table} AS "
            f"SELECT * FROM read_csv_auto('{csv_path}')"
        )

    con.close()
