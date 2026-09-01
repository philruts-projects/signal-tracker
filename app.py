"""
app.py — Signal Tracker dashboard.

Leads with risk: which watched companies need attention, worst first, with the
registered status up top and the filing-level signals and briefings one click down.
Read-only over the SQLite database. No API calls.

Company risk is a REVIEW PRIORITY heuristic (status + this company's own filing signals),
not a probability of insolvency.

Run it with:  streamlit run app.py
"""

import json
import sqlite3
import pandas as pd
import streamlit as st

from lookups import friendly_type
from severity import portfolio_company_risk

DB_FILE = "data/signals.db"

st.set_page_config(page_title="Signal Tracker", layout="wide")

RISK_ICON = {"Critical": "🔴", "Serious": "🟠", "Watch": "🟡", "Routine": "🟢", "Unknown": "⚪"}
RISK_RANK = {"Critical": 3, "Serious": 2, "Watch": 1, "Unknown": 0.5, "Routine": 0}


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


def as_bool(value, default=True):
    """Read a possibly-absent SQLite flag as a bool, defaulting when the column/value is missing."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return default
    return bool(value)


def cluster_summaries(mine):
    """Plain-English summaries of cross-filing CLUSTERS for one company's filings.

    This is the 'drill-down grouping': a burst of charges or a run of accounting-date
    changes is the distress signal, not any single filing, so we surface the group as one line.
    """
    out = []
    df = mine.copy()
    df["d"] = pd.to_datetime(df["date"], errors="coerce")
    up = df["type"].fillna("").str.upper()
    desc = df["description"].fillna("")

    # Registered-charge burst: widest 30-day window containing 3+ charge registrations.
    ch = df[(up.str.startswith("MR") | (df["description"].fillna("").str.contains("mortgage", case=False)))
            & ~desc.str.contains("satisf", case=False)]
    dates = ch["d"].dropna().sort_values().reset_index(drop=True)
    best, span = 0, None
    for i in range(len(dates)):
        window = dates[(dates >= dates[i]) & (dates <= dates[i] + pd.Timedelta(days=30))]
        if len(window) > best:
            best, span = len(window), (dates[i], window.max())
    if best >= 3 and span:
        days = (span[1] - span[0]).days
        window_txt = "the same day" if days == 0 else f"{days} day(s)"
        out.append(f"🔶 **Charge cluster:** {best} charges registered within {window_txt} "
                   f"(to {span[1].date()}) — scrambling for secured finance is a distress marker.")

    # Repeated accounting-reference-date changes.
    ard = df[(up == "AA01") | desc.str.contains("reference-date", case=False)]
    if len(ard) >= 2:
        out.append(f"🔶 **Repeated accounting-date changes:** {len(ard)} on record — "
                   f"repetition can signal delayed or obfuscated accounts.")

    # Governance churn — a corroborator, shown for context, never a standalone trigger.
    tm = df[up.str.startswith("TM")]
    if len(tm) >= 3:
        out.append(f"◽ **Governance:** {len(tm)} director/secretary departures on record "
                   f"(corroborator — only counts alongside other stress).")
    return out


companies, filings = load_data()

# --- Per-company risk posture -------------------------------------------------
rows = []
for _, co in companies.iterrows():
    mine = filings[filings["company_number"] == co["company_number"]]
    watch = int((mine["severity"] == "Watch").sum())
    ser = int((mine["severity"] == "Serious").sum())
    crit = int((mine["severity"] == "Critical").sum())

    # Review priority: status-based risk escalated by THIS company's own filing signals,
    # so a Serious filing can't leave the headline at Routine.
    risk, reason = portfolio_company_risk(
        co.get("status"), co.get("has_insolvency_history"), co.get("accounts_overdue"),
        co.get("recent_churn"), watch_signals=watch, serious_signals=ser, critical_signals=crit,
        profile_ok=as_bool(co.get("profile_ok")),
    )

    notable = mine[mine["severity"].isin(["Watch", "Serious", "Critical"])]
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
        "reason": reason,
        "crit": crit,
        "ser": ser,
        "latest": latest_txt,
        "peak_churn": int(co.get("peak_churn") or 0),
        "peak_churn_date": co.get("peak_churn_date"),
        "short_tenure_exits": int(co.get("short_tenure_exits") or 0),
        "charges_outstanding": int(co.get("charges_outstanding") or 0),
        "charges_rows": json.loads(co["charges_json"]) if co.get("charges_json") else [],
    })

posture = pd.DataFrame(rows)
posture["rank"] = posture["risk"].map(RISK_RANK)
posture = posture.sort_values(["rank", "crit", "ser"], ascending=False)

need_attention = int(posture["risk"].isin(["Serious", "Critical"]).sum())
data_issues = int((posture["risk"] == "Unknown").sum())

# --- Header + headline numbers ------------------------------------------------
st.title("🛡️ Signal Tracker")
st.caption("A review queue for the companies you're exposed to — public filings, triaged and explained in plain English. "
           "Risk here is a review priority, not a probability of failure.")

c1, c2, c3 = st.columns(3)
c1.metric("Companies watched", len(posture))
c2.metric("Need attention", need_attention)
c3.metric("Data issues", data_issues, help="Companies whose latest data fetch failed — status Unknown, not assumed healthy.")

if need_attention == 0 and data_issues == 0:
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
        if co["reason"]:
            st.caption(f"⬆️ {co['reason']}")
        if co["risk"] == "Unknown":
            st.caption("⚪ Data unavailable — the last fetch for this company failed, so its status is not known.")
        if co["latest"]:
            st.caption(f"Latest signal: {co['latest']}")

        mine = filings[filings["company_number"] == co["company_number"]]

        # Drill-down grouping: lead flagged companies with the CLUSTER story, not one filing.
        if co["risk"] in ("Watch", "Serious", "Critical"):
            for line in cluster_summaries(mine):
                st.markdown(line)

        # Churn is corroboration, not a standalone flag — only show it on already-flagged companies.
        if co["peak_churn"] >= 3 and co["risk"] in ("Watch", "Serious", "Critical"):
            when = f" (to {co['peak_churn_date']})" if co["peak_churn_date"] else ""
            st.caption(f"Board churn: {co['peak_churn']} director resignations within 90 days{when}")
        # Secured borrowing — corroboration on already-flagged companies, with the lender named.
        if co["charges_outstanding"] and co["risk"] in ("Watch", "Serious", "Critical"):
            outstanding = [r for r in co["charges_rows"] if r.get("status") in ("outstanding", "part-satisfied")]
            latest = outstanding[0] if outstanding else None
            extra = f", latest to {latest['lender']} ({latest['created_on']})" if latest and latest.get("lender") else ""
            st.caption(f"Secured borrowing: {co['charges_outstanding']} charge(s) outstanding{extra}")

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
