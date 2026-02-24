from __future__ import annotations

from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    duckdb_path: str = os.getenv("DUCKDB_PATH", "warehouse/warehouse.duckdb")
    data_dir: str = "data"
    artifacts_dir: str = "artifacts"

settings = Settings()
