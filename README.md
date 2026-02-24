# Lending Analytics Platform Demo (DuckDB + dbt)

A compact, end-to-end **data & analytics platform** demo. It shows how to:
- ingest raw extracts into a warehouse,
- build curated marts with **dbt**,
- validate data contracts with tests and a quality gate,
- publish a lightweight analytics view (Streamlit).

All data in this repo is **synthetic** and generated locally.

---

## What’s included

### Pipeline (single command)
1. Generate raw CSV extracts (applications, payments, marketing events)
2. Load to a local warehouse (DuckDB)
3. Transform with dbt (staging → marts)
4. Run dbt tests + a Python quality gate
5. Produce a short “run report” (data dictionary + anomaly snapshot)
6. (Optional) View results in a Streamlit dashboard

### Tech stack
- **Python** (pandas, numpy)
- **DuckDB** local warehouse
- **dbt** transformations + tests
- **GitHub Actions** for CI (lint + tests)
- **Streamlit** demo dashboard

---

## Quickstart

### 1) Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Run the pipeline
```bash
python -m src.pipeline.run_all
```

Outputs:
- `warehouse/warehouse.duckdb` (local warehouse)
- `artifacts/quality_report.json`
- `artifacts/data_dictionary.md`
- `artifacts/anomaly_report.md`

### 3) Run the dashboard
```bash
streamlit run apps/dashboard.py
```

---

## Repo layout
```
.
├── apps/                  # simple analytics product
├── dbt/                   # dbt project (staging + marts + tests)
├── src/
│   ├── generators/        # synthetic data generator
│   ├── pipeline/          # orchestration + load + checks
│   └── utils/
├── tests/                 # pytest unit tests
└── .github/workflows/     # CI: ruff + pytest
```

---

## Analytics views

### `mart_lending_funnel`
Application-level facts for funnel analysis:
- channel, state, risk tier, requested amount
- approval indicator
- marketing touch counts (impressions/clicks)

### `mart_payment_behavior`
First 6 months of payment behavior for approved loans:
- on-time indicator
- amount paid
- estimated ending balance

---

## Interview-ready talking points
- **Data contracts:** dbt tests (unique/not_null) + a Python quality gate for platform-level checks
- **Reproducibility:** deterministic generator with seed; one-command rebuild
- **Warehouse-first workflow:** raw → staging → marts; clean separation of concerns
- **Observability:** run artifacts + structured quality report
- **Extensibility:** easy to swap DuckDB for Snowflake/BigQuery/Databricks and schedule with Airflow/Prefect
