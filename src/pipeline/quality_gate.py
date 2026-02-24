from __future__ import annotations

from dataclasses import dataclass
import duckdb

@dataclass(frozen=True)
class QualityResult:
    ok: bool
    checks: dict[str, dict[str, float | int | str]]

def run_quality_gate(duckdb_path: str) -> QualityResult:
    con = duckdb.connect(duckdb_path)
    checks: dict[str, dict[str, float | int | str]] = {}

    missing_ids = con.execute(
        "SELECT COUNT(*) FROM mart_lending_funnel WHERE application_id IS NULL"
    ).fetchone()[0]
    checks["missing_application_id_in_mart"] = {"value": int(missing_ids), "rule": "must be 0"}

    approval_rate = con.execute(
        "SELECT AVG(approved) FROM mart_lending_funnel"
    ).fetchone()[0]
    checks["approval_rate"] = {"value": float(approval_rate), "rule": "0.10 <= rate <= 0.90"}

    payment_rows = con.execute(
        "SELECT COUNT(*) FROM mart_payment_behavior"
    ).fetchone()[0]
    checks["payment_rows"] = {"value": int(payment_rows), "rule": "must be > 0"}

    con.close()

    ok = (missing_ids == 0) and (0.10 <= float(approval_rate) <= 0.90) and (payment_rows > 0)
    return QualityResult(ok=ok, checks=checks)
