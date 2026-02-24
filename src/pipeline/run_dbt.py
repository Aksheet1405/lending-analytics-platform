from __future__ import annotations

import subprocess
from pathlib import Path
from rich.console import Console

console = Console()

def _run(cmd: list[str], cwd: str) -> None:
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if p.returncode != 0:
        console.print(p.stdout)
        console.print(p.stderr)
        raise RuntimeError(f"dbt command failed: {' '.join(cmd)}")
    console.print(p.stdout)

def dbt_build(dbt_dir: str) -> None:
    Path(dbt_dir).mkdir(parents=True, exist_ok=True)
    console.print("[bold]dbt[/bold] deps")
    _run(["dbt", "deps"], cwd=dbt_dir)
    console.print("[bold]dbt[/bold] build")
    _run(["dbt", "build"], cwd=dbt_dir)
