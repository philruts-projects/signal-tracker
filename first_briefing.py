"""
first_briefing.py — Phase 4, step 1: prove we can turn one filing into a
plain-English briefing using the Claude API. Standalone test before we wire
this into tracker.py.
"""

import os
import sys

import anthropic
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("ANTHROPIC_API_KEY"):
    sys.exit("No ANTHROPIC_API_KEY found. Add it to your .env file.")

MODEL = "claude-haiku-4-5-20251001"

# A sample filing — the Direct Line director termination we saw earlier.
example = {
    "company_name": "Direct Line Insurance Group plc",
    "company_number": "02280426",
    "date": "2026-08-05",
    "type": "TM01",
    "category": "officers",
    "description": "termination-director-company-with-name-termination-date",
}

SYSTEM_PROMPT = (
    "You are a commercial analyst who writes short, plain-English briefings for "
    "credit, account-management and procurement teams. They monitor UK companies "
    "via Companies House filings but are not accountants or lawyers. "
    "Explain what a filing event means in practical commercial terms. Be factual "
    "and measured — never alarmist. Base your briefing only on the filing details "
    "provided; if the significance is ambiguous, say so. This is an advisory signal "
    "for a human to act on, not financial or legal advice."
)


def build_user_prompt(f):
    return (
        f"Write a briefing about this Companies House filing.\n\n"
        f"Company: {f['company_name']} ({f['company_number']})\n"
        f"Date: {f['date']}\n"
        f"Filing type: {f['type']}\n"
        f"Category: {f['category']}\n"
        f"Description code: {f['description']}\n\n"
        f"Format the briefing as exactly these three short sections:\n"
        f"What happened: (one sentence, plain English)\n"
        f"Why it matters: (1-2 sentences on the commercial signal)\n"
        f"Suggested action: (one sentence)"
    )


def generate_briefing(f):
    client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from the environment
    message = client.messages.create(
        model=MODEL,
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_user_prompt(f)}],
    )
    return message.content[0].text


if __name__ == "__main__":
    print(f"Generating briefing with {MODEL}...\n")
    print(generate_briefing(example))