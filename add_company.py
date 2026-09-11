"""
add_company.py — put a company on the watchlist without editing watchlist.csv by hand.

    python add_company.py "Marks and Spencer"

Searches Companies House, shows the top matches, you pick one by number, it's appended to
watchlist.csv. The next tracker.py run stores that company's filing history as baseline
(never briefed), so adding a company costs nothing in Claude calls.

Why a search step at all: names aren't unique and change over time; the 8-character company
number is the only safe key (see BACKLOG.md). This script is how we get from a name a human
knows to the number the tracker needs, with a human choosing between look-alikes.

Free: one Companies House search call per run, no Claude calls, no database changes.
"""

import csv
import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("CH_API_KEY")
if not API_KEY:
    sys.exit("No CH_API_KEY found. Check your .env file.")

BASE_URL = "https://api.company-information.service.gov.uk"
WATCHLIST = "watchlist.csv"
MAX_RESULTS = 5


def search_companies(query):
    """Top MAX_RESULTS matches from the Companies House search endpoint."""
    response = requests.get(
        f"{BASE_URL}/search/companies",
        params={"q": query, "items_per_page": MAX_RESULTS},
        auth=(API_KEY, ""),
        timeout=15,
    )
    response.raise_for_status()
    return response.json().get("items", [])


def current_numbers():
    with open(WATCHLIST, newline="", encoding="utf-8") as f:
        return {row["company_number"] for row in csv.DictReader(f)}


def append_to_watchlist(number, name):
    # "a" = append mode: adds a line at the end, never rewrites what's already there.
    with open(WATCHLIST, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([number, name])


def main():
    if len(sys.argv) < 2:
        sys.exit('Usage: python add_company.py "company name"')
    query = " ".join(sys.argv[1:])

    items = search_companies(query)
    if not items:
        sys.exit(f"No companies matched {query!r}.")

    already = current_numbers()
    print(f"\nTop matches for {query!r}:\n")
    for i, item in enumerate(items, start=1):
        number = item.get("company_number", "?")
        flag = "  (already on watchlist)" if number in already else ""
        address = (item.get("address_snippet") or "")[:50]
        print(f"  {i}. {number}  {item.get('title')}")
        print(f"     {item.get('company_status', '?')}, incorporated {item.get('date_of_creation', '?')}, {address}{flag}")

    choice = input(f"\nAdd which? (1-{len(items)}, or Enter to cancel): ").strip()
    if not choice.isdigit() or not 1 <= int(choice) <= len(items):
        print("Cancelled. Nothing changed.")
        return

    chosen = items[int(choice) - 1]
    number, name = chosen["company_number"], chosen["title"]
    if number in already:
        print(f"{name} ({number}) is already on the watchlist. Nothing changed.")
        return

    append_to_watchlist(number, name)
    print(f"\nAdded {name} ({number}) to {WATCHLIST}.")
    print("Next tracker.py run will baseline its filing history (no briefings on first poll).")


if __name__ == "__main__":
    main()
