from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import date, timedelta
import pandas as pd

@dataclass(frozen=True)
class SynthParams:
    n_applications: int = 5000
    start_date: date = date(2025, 1, 1)
    days: int = 180
    seed: int = 42

def _choice_weighted(items):
    values, weights = zip(*items)
    return random.choices(list(values), weights=list(weights), k=1)[0]

def generate(params: SynthParams) -> dict[str, pd.DataFrame]:
    """Generate synthetic lending + marketing + payment datasets.

    - deterministic output via seed
    - realistic correlations (risk tier, FICO, DTI, approvals)
    - no PII
    """
    random.seed(params.seed)

    channels = [
        ("paid_search", 0.35),
        ("affiliate", 0.20),
        ("organic", 0.25),
        ("email", 0.10),
        ("referral", 0.10),
    ]
    states = [
        ("IL", 0.12), ("CA", 0.18), ("TX", 0.16), ("NY", 0.08), ("FL", 0.12),
        ("OH", 0.08), ("GA", 0.06), ("IN", 0.05), ("MI", 0.05), ("WA", 0.10),
    ]
    tiers = [("A", 0.25), ("B", 0.35), ("C", 0.25), ("D", 0.15)]

    applications_rows = []
    for app_id in range(1, params.n_applications + 1):
        app_date = params.start_date + timedelta(days=random.randint(0, params.days - 1))
        channel = _choice_weighted(channels)
        state = _choice_weighted(states)
        tier = _choice_weighted(tiers)

        income = max(18_000, int(random.gauss(72_000, 25_000)))
        dti = max(0.05, min(0.65, random.gauss(0.28, 0.12)))
        fico = int(max(520, min(820, random.gauss(705, 55) - (tier in ["C", "D"]) * 35)))
        amount = int(max(1_000, min(35_000, random.gauss(12_000, 6_000) + (tier == "A") * 2_000)))

        base = {"A": 0.72, "B": 0.55, "C": 0.38, "D": 0.22}[tier]
        p_approve = base + (fico - 680) / 600 - (dti - 0.25) * 1.2
        approved = random.random() < max(0.05, min(0.95, p_approve))

        apr = round(max(5.5, min(34.9, random.gauss({"A": 9.9, "B": 15.9, "C": 22.9, "D": 29.9}[tier], 2.0))), 2)
        term_months = random.choice([24, 36, 48, 60])

        applications_rows.append(
            {
                "application_id": app_id,
                "application_date": app_date.isoformat(),
                "channel": channel,
                "state": state,
                "risk_tier": tier,
                "annual_income": income,
                "dti": round(dti, 3),
                "fico_score": fico,
                "requested_amount": amount,
                "approved": int(approved),
                "apr": apr if approved else None,
                "term_months": term_months if approved else None,
            }
        )

    applications = pd.DataFrame(applications_rows)

    pay_rows = []
    for _, r in applications[applications["approved"] == 1].iterrows():
        start = date.fromisoformat(r["application_date"]) + timedelta(days=14)
        delinquency_chance = {"A": 0.03, "B": 0.05, "C": 0.08, "D": 0.12}[r["risk_tier"]]
        balance = float(r["requested_amount"])
        monthly = max(40.0, balance / float(r["term_months"])) * (1.0 + float(r["apr"]) / 1200.0)

        for m in range(1, 7):
            due = start + timedelta(days=30 * m)
            paid = 1 if random.random() > delinquency_chance else 0
            amount_paid = round(monthly if paid else 0.0, 2)
            balance = max(0.0, balance - (amount_paid * 0.75))
            pay_rows.append(
                {
                    "application_id": int(r["application_id"]),
                    "payment_month": m,
                    "due_date": due.isoformat(),
                    "paid": paid,
                    "amount_paid": amount_paid,
                    "ending_balance_est": round(balance, 2),
                }
            )

    payments = pd.DataFrame(pay_rows)

    events_rows = []
    for i in range(params.n_applications * 2):
        event_date = params.start_date + timedelta(days=random.randint(0, params.days - 1))
        channel = _choice_weighted(channels)
        event_type = _choice_weighted([("impression", 0.55), ("click", 0.35), ("landing", 0.10)])
        application_id = random.randint(1, params.n_applications) if random.random() > 0.15 else None
        events_rows.append(
            {
                "event_id": i + 1,
                "event_date": event_date.isoformat(),
                "channel": channel,
                "event_type": event_type,
                "application_id": application_id,
            }
        )
    marketing_events = pd.DataFrame(events_rows)

    return {
        "applications": applications,
        "payments": payments,
        "marketing_events": marketing_events,
    }
