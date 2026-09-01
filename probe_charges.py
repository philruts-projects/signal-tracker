"""
probe_charges.py — throwaway: see what the Companies House /charges endpoint really
returns, so we build the enrichment around real fields (esp. whether amounts exist).

Run with:  python probe_charges.py
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

for number, label in [("03782379", "Carillion"), ("08126173", "Greensill"), ("02468686", "Aviva")]:
    r = requests.get(f"{BASE_URL}/company/{number}/charges", auth=(API_KEY, ""), timeout=15)
    if r.status_code != 200:
        print(f"\n==== {label} ({number}) — HTTP {r.status_code} ====")
        continue
    data = r.json()
    items = data.get("items", [])
    print(f"\n==== {label} ({number}) — total {data.get('total_count')}, "
          f"satisfied {data.get('satisfied_count')}, part {data.get('part_satisfied_count')} ====")
    if items:
        print("  sample item keys:", sorted(items[0].keys()))
        print("  sample secured_details:", items[0].get("secured_details"))
    for o in items[:8]:
        lenders = ", ".join(p.get("name", "?") for p in o.get("persons_entitled", []))
        cls = o.get("classification")
        cls = cls.get("description") if isinstance(cls, dict) else cls
        print(f"  {str(o.get('status')):14} created {str(o.get('created_on','?')):11} "
              f"satisfied {str(o.get('satisfied_on','-')):11} | {cls} | {lenders}")
