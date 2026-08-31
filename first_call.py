"""
first_call.py — Phase 2: prove we can talk to the Companies House API.

What this script does, in plain terms:
  1. Reads your secret API key from a local .env file (never hard-coded).
  2. Asks the Companies House API for one company's public profile.
  3. Checks the request actually succeeded.
  4. Prints a few human-readable fields so you can see it worked.

Run it with:  python first_call.py
"""

import os
import sys

import requests                      # the library that makes HTTP calls for us
from dotenv import load_dotenv       # reads key=value pairs out of a .env file


# --- 1. Load the secret ---------------------------------------------------
load_dotenv()

API_KEY = os.getenv("CH_API_KEY")    # the name must match what's in your .env

if not API_KEY:
    sys.exit("No CH_API_KEY found. Copy .env.example to .env and paste your key in.")


# --- 2. Build the request -------------------------------------------------
BASE_URL = "https://api.company-information.service.gov.uk"

# Any real company number works. 00000006 is the example Companies House use in
# their own docs. Find others at https://find-and-update.company-information.service.gov.uk
COMPANY_NUMBER = "00000006"

url = f"{BASE_URL}/company/{COMPANY_NUMBER}"

# Companies House uses "HTTP Basic authentication": your API key as the username
# and an EMPTY password. requests handles that with auth=(key, "").
response = requests.get(url, auth=(API_KEY, ""), timeout=15)


# --- 3. Did it work? ------------------------------------------------------
# 200 = OK. 401 = bad key. 404 = no such company. 429 = rate limit hit.
if response.status_code != 200:
    sys.exit(f"Request failed with status {response.status_code}: {response.text[:200]}")


# --- 4. Read the answer ---------------------------------------------------
data = response.json()

print("Connection to Companies House API succeeded.\n")
print(f"Company name : {data.get('company_name')}")
print(f"Number       : {data.get('company_number')}")
print(f"Status       : {data.get('company_status')}")
print(f"Type         : {data.get('type')}")
print(f"Incorporated : {data.get('date_of_creation')}")