from __future__ import annotations

import duckdb
import streamlit as st
from src.utils.config import settings

st.set_page_config(page_title="Lending Analytics", layout="wide")
st.title("Lending Analytics Dashboard (Synthetic Demo)")

con = duckdb.connect(settings.duckdb_path, read_only=True)

kpis = con.execute(
    """
    SELECT
      COUNT(*) AS applications,
      AVG(approved) AS approval_rate,
      AVG(requested_amount) AS avg_requested_amount
    FROM mart_lending_funnel
    """
).df()

c1, c2, c3 = st.columns(3)
c1.metric("Applications", f"{int(kpis.loc[0, 'applications']):,}")
c2.metric("Approval rate", f"{float(kpis.loc[0, 'approval_rate']):.1%}")
c3.metric("Avg requested amount", f"${float(kpis.loc[0, 'avg_requested_amount']):,.0f}")

st.subheader("Channel performance")
df = con.execute(
    """
    SELECT
      channel,
      COUNT(*) AS applications,
      AVG(approved) AS approval_rate,
      AVG(requested_amount) AS avg_amount
    FROM mart_lending_funnel
    GROUP BY 1
    ORDER BY applications DESC
    """
).df()
st.dataframe(df, use_container_width=True)

st.subheader("Risk tier mix")
rt = con.execute(
    """
    SELECT risk_tier, COUNT(*) AS applications, AVG(approved) AS approval_rate
    FROM mart_lending_funnel
    GROUP BY 1
    ORDER BY risk_tier
    """
).df()
st.bar_chart(rt.set_index("risk_tier")["applications"])

st.subheader("Payment behavior (first 6 months)")
pb = con.execute(
    """
    SELECT payment_month, AVG(paid) AS on_time_rate, AVG(amount_paid) AS avg_amount_paid
    FROM mart_payment_behavior
    GROUP BY 1
    ORDER BY 1
    """
).df()
st.line_chart(pb.set_index("payment_month")["on_time_rate"])

con.close()
