"""
probe_officers.py — throwaway: inspect what the Companies House /officers endpoint
actually returns, so we design the enrichment around real data, not assumptions.

Run with:  python probe_officers.py
"""

import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("CH_API_KEY")
if not API_KEY:
    sys.exit("No CH_API_KEY found. Check your .env file.")

BASE_URL = "https://api.company-information.service.gov.uk"

for number, label in [("03782379", "Carillion"), ("08126173", "Greensill")]:
    r = requests.get(
        f"{BASE_URL}/company/{number}/officers?items_per_page=35",
        auth=(API_KEY, ""), timeout=15,
    )
    r.raise_for_status()
    data = r.json()
    print(f"\n==== {label} ({number}) — {data.get('total_results')} officers total ====")
    print(f"{'role':10} | {'appointed':10} | {'resigned':10} | occupation / name")
    for o in data.get("items", []):
        print(
            f"{str(o.get('officer_role'))[:10]:10} | "
            f"{str(o.get('appointed_on','?'))[:10]:10} | "
            f"{str(o.get('resigned_on','-'))[:10]:10} | "
            f"{str(o.get('occupation','-'))} — {o.get('name')}"
        )
