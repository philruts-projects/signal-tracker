"""
app.py — Phase 5: a Streamlit dashboard over the signals database.
Leads with the AI briefings (the signals); full filing log sits below.
Read-only: no API calls.

Run it with:  streamlit run app.py
"""

import sqlite3
import pandas as pd
import streamlit as st

from lookups import friendly_type

DB_FILE = "data/signals.db"

st.set_page_config(page_title="Companies House Signal Tracker", layout="wide")


def load_data():
    conn = sqlite3.connect(DB_FILE)
    companies = pd.read_sql_query("SELECT * FROM companies", conn)
    filings = pd.read_sql_query(
        """
        SELECT f.date, f.type, f.description, f.briefing, c.company_name
        FROM filings f
        JOIN companies c ON c.company_number = f.company_number
        ORDER BY f.date DESC
        """,
        conn,
    )
    conn.close()
    return companies, filings


def prettify(code):
    """Turn 'capital-cancellation-shares' into 'Capital cancellation shares'."""
    if not code:
        return ""
    return code.replace("-", " ").capitalize()


st.title("📊 Companies House Signal Tracker")
st.caption("Monitoring UK company filings and turning them into plain-English briefings.")

companies, filings = load_data()

# --- Summary numbers ---
col1, col2, col3 = st.columns(3)
col1.metric("Companies watched", len(companies))
col2.metric("Filings tracked", len(filings))
col3.metric("Briefings generated", int(filings["briefing"].notna().sum()))

# --- Company filter ---
st.sidebar.header("Filters")
names = ["All companies"] + sorted(companies["company_name"].tolist())
chosen = st.sidebar.selectbox("Company", names)

view = filings if chosen == "All companies" else filings[filings["company_name"] == chosen]

# --- Signals: filings that have a briefing ---
st.subheader("🔔 Signals")
briefed = view[view["briefing"].notna() & (view["briefing"] != "")]

if briefed.empty:
    st.info("No briefings yet. Run `python tracker.py` to detect new filings and generate briefings.")
else:
    for _, row in briefed.iterrows():
        with st.container(border=True):
            label = friendly_type(row["type"], fallback=prettify(row["description"]))
            st.markdown(f"**{row['company_name']}**  ·  {row['date']}  ·  {label}  `{row['type']}`")
            st.markdown(row["briefing"])

# --- Full filing log as a compact table ---
st.subheader("All tracked filings")
table = view[["company_name", "date", "type", "description"]].copy()
table["Filing type"] = table["type"].apply(lambda t: friendly_type(t, fallback=t))
table["description"] = table["description"].apply(prettify)
table = table[["company_name", "date", "Filing type", "type", "description"]].rename(columns={
    "company_name": "Company",
    "date": "Date",
    "type": "Code",
    "description": "Detail",
})
st.dataframe(table, width="stretch", hide_index=True)