from __future__ import annotations

from datetime import datetime
import duckdb

def build_data_dictionary_md(duckdb_path: str, table: str) -> str:
    con = duckdb.connect(duckdb_path)
    cols = con.execute(f"DESCRIBE {table}").fetchall()
    con.close()

    lines = [f"# Data Dictionary: `{table}`", ""]
    lines += ["| Column | Type | Notes |", "|---|---|---|"]
    for col, typ, *_ in cols:
        lines.append(f"| {col} | {typ} |  |")
    lines.append("")
    lines.append("_Notes: Fill in column notes as the mart evolves._")
    return "\n".join(lines)

def build_anomaly_report_md(duckdb_path: str) -> str:
    con = duckdb.connect(duckdb_path)

    overall_n, overall_ar = con.execute(
        "SELECT COUNT(*) AS n, AVG(approved) AS approval_rate FROM mart_lending_funnel"
    ).fetchone()
    by_channel = con.execute(
        """
        SELECT channel, COUNT(*) AS n, AVG(approved) AS approval_rate
        FROM mart_lending_funnel
        GROUP BY 1
        ORDER BY n DESC
        """
    ).fetchall()

    con.close()

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    lines = ["# Daily Run Snapshot", f"_Generated: {now}_", ""]
    lines.append(f"**Overall:** {int(overall_n):,} applications, approval rate **{float(overall_ar):.2%}**")
    lines.append("")
    lines.append("## Channel performance")
    for ch, n, ar in by_channel:
        lines.append(f"- **{ch}**: {int(n):,} apps, approval rate {float(ar):.2%}")
    lines.append("")
    lines.append("## Quick checks")
    lines.append("- Review abrupt changes in channel volume or approval rate.")
    lines.append("- Extend with drift metrics (PSI/KS), seasonality baselines, or alert thresholds.")
    return "\n".join(lines)
