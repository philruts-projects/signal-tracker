"""
probe_fca.py — look at what the FCA Financial Services Register API actually returns.

Same idea as probe_charges.py and probe_officers.py: before we store anything, or model
anything, or write a single rule, call the endpoint once and print the raw response so we
can see its shape with our own eyes.

Setup (one off):
  1. Register, free, at https://register.fca.org.uk/Developer/s/
  2. Add two lines to your .env file:
         FCA_EMAIL=the email address you registered with
         FCA_API_KEY=the key they issue you

Run it:
  python probe_fca.py "Admiral Insurance"
"""

import os
import sys
import json

import requests
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("FCA_EMAIL")
KEY = os.getenv("FCA_API_KEY")
if not EMAIL or not KEY:
    sys.exit("Missing FCA_EMAIL or FCA_API_KEY in .env")

BASE = "https://register.fca.org.uk/services/V0.1"

# The FCA authenticates with two custom headers. Companies House used HTTP basic auth
# (the key as a username), so this is a different pattern for the same job: proving who we are.
HEADERS = {"X-Auth-Email": EMAIL, "X-Auth-Key": KEY, "Content-Type": "application/json"}


def fca_get(path, params=None):
    """One GET request. Prints the URL and status so you can see exactly what was asked."""
    response = requests.get(f"{BASE}{path}", headers=HEADERS, params=params, timeout=15)
    print(f"GET {response.url}  ->  HTTP {response.status_code}")
    response.raise_for_status()
    return response.json()


def show(label, payload):
    print(f"\n=============== {label} ===============")
    print(json.dumps(payload, indent=2)[:4000])   # truncated so the output stays readable


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "Admiral Insurance"

    # 1. Search by name. This is the only way in when all we hold is a company name, because
    #    the FCA keys everything on a Firm Reference Number that Companies House knows nothing
    #    about. Read the results carefully: this is the join problem, in the raw.
    search = fca_get("/Search", {"q": name, "type": "firm"})
    show(f"SEARCH for {name!r}", search)

    # 2. Take the first hit and pull its full firm record, so we can see which fields might
    #    be worth storing later. We check a few spellings of the key because we don't yet
    #    know how the FCA cases its field names. Finding that out is the point of the probe.
    data = search.get("Data") or search.get("data") or []
    if not data:
        print("\nNo firms matched that name. Try another.")
        return

    first = data[0]
    print(f"\nFirst match:\n{json.dumps(first, indent=2)}")
    frn = first.get("Reference Number") or first.get("reference_number") or first.get("FRN")
    print(f"\nFRN taken from that match: {frn}")

    if frn:
        show(f"FIRM {frn}", fca_get(f"/Firm/{frn}"))


if __name__ == "__main__":
    main()
