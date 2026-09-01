"""
app.py — Signal Tracker dashboard.

Leads with risk: which watched companies need attention, worst first, with the
registered status up top and the filing-level signals and briefings one click down.
Read-only over the SQLite database. No API calls.

Run it with:  streamlit run app.py
"""

import sqlite3
import pandas as pd
import streamlit as st

from lookups import friendly_type
from severity import company_risk

DB_FILE = "data/signals.db"

st.set_page_config(page_title="Signal Tracker", layout="wide")

RISK_ICON = {"Critical": "🔴", "Serious": "🟠", "Watch": "🟡", "Routine": "🟢"}
RISK_RANK = {"Critical": 3, "Serious": 2, "Watch": 1, "Routine": 0}


def load_data():
    conn = sqlite3.connect(DB_FILE)
    companies = pd.read_sql_query("SELECT * FROM companies", conn)
    filings = pd.read_sql_query(
        """SELECT f.company_number, f.date, f.type, f.description, f.severity, f.briefing,
                  c.company_name
           FROM filings f JOIN companies c ON c.company_number = f.company_number""",
        conn,
    )
    conn.close()
    return companies, filings


def prettify(code):
    return code.replace("-", " ").capitalize() if code else ""


def status_label(status):
    return (status or "unknown").replace("-", " ").capitalize()


companies, filings = load_data()

# --- Per-company risk posture -------------------------------------------------
rows = []
for _, co in companies.iterrows():
    risk = company_risk(co.get("status"), co.get("has_insolvency_history"),
                        co.get("accounts_overdue"), co.get("recent_churn"))
    mine = filings[filings["company_number"] == co["company_number"]]
    notable = mine[mine["severity"].isin(["Watch", "Serious", "Critical"])]
    crit = int((mine["severity"] == "Critical").sum())
    ser = int((mine["severity"] == "Serious").sum())
    latest = notable.sort_values("date").tail(1)
    latest_txt = ""
    if not latest.empty:
        r = latest.iloc[0]
        latest_txt = f"{r['date']} · {friendly_type(r['type'], fallback=prettify(r['description']))} ({r['severity']})"
    rows.append({
        "company_number": co["company_number"],
        "company_name": co["company_name"],
        "status": co.get("status"),
        "risk": risk,
        "crit": crit,
        "ser": ser,
        "latest": latest_txt,
        "peak_churn": int(co.get("peak_churn") or 0),
        "peak_churn_date": co.get("peak_churn_date"),
        "short_tenure_exits": int(co.get("short_tenure_exits") or 0),
    })

posture = pd.DataFrame(rows)
posture["rank"] = posture["risk"].map(RISK_RANK)
posture = posture.sort_values(["rank", "crit", "ser"], ascending=False)

need_attention = int(posture["risk"].isin(["Serious", "Critical"]).sum())

# --- Header + headline numbers ------------------------------------------------
st.title("🛡️ Signal Tracker")
st.caption("Which of the companies you're exposed to are heading for trouble — from public filings, in plain English.")

c1, c2 = st.columns(2)
c1.metric("Companies watched", len(posture))
c2.metric("Need attention", need_attention)

if need_attention == 0:
    st.success("Nothing needs your attention today.")

# --- Sidebar filter -----------------------------------------------------------
st.sidebar.header("Filter")
names = ["All companies"] + posture["company_name"].tolist()
chosen = st.sidebar.selectbox("Company", names)
show_log = st.sidebar.checkbox("Show raw filing log", value=False)

view = posture if chosen == "All companies" else posture[posture["company_name"] == chosen]

# --- Company cards, worst first ----------------------------------------------
for _, co in view.iterrows():
    with st.container(border=True):
        icon = RISK_ICON.get(co["risk"], "")
        st.markdown(f"### {icon} {co['company_name']}")
        bits = [f"**Status:** {status_label(co['status'])}", f"**Risk:** {co['risk']}"]
        if co["crit"] or co["ser"]:
            bits.append(f"{co['crit']} critical / {co['ser']} serious signals on record")
        st.markdown("  ·  ".join(bits))
        if co["latest"]:
            st.caption(f"Latest signal: {co['latest']}")
        # Churn is corroboration, not a standalone flag — only show it on already-flagged companies.
        if co["peak_churn"] >= 3 and co["risk"] in ("Watch", "Serious", "Critical"):
            when = f" (to {co['peak_churn_date']})" if co["peak_churn_date"] else ""
            st.caption(f"Board churn: {co['peak_churn']} director resignations within 90 days{when}")

        mine = filings[filings["company_number"] == co["company_number"]]
        notable = mine[mine["severity"].isin(["Watch", "Serious", "Critical"])].sort_values("date", ascending=False)
        if not notable.empty:
            with st.expander(f"View {len(notable)} signal(s)"):
                for _, r in notable.iterrows():
                    tag = RISK_ICON.get(r["severity"], "")
                    st.markdown(
                        f"{tag} **{r['severity']}** · {r['date']} · "
                        f"{friendly_type(r['type'], fallback=prettify(r['description']))}  `{r['type']}`"
                    )
                    if pd.notna(r["briefing"]) and r["briefing"]:
                        st.markdown(r["briefing"])

# --- Optional raw log ---------------------------------------------------------
if show_log:
    st.subheader("Raw filing log")
    log = filings.copy()
    log["Filing type"] = log["type"].apply(lambda t: friendly_type(t, fallback=t))
    log = log[["company_name", "date", "severity", "Filing type", "type"]].rename(
        columns={"company_name": "Company", "date": "Date", "severity": "Severity", "type": "Code"})
    st.dataframe(log.sort_values("Date", ascending=False), width="stretch", hide_index=True)
