"""
briefing.py — generate a plain-English commercial briefing for a single
Companies House filing, using the Claude API.
"""

import anthropic
from dotenv import load_dotenv

from lookups import friendly_type

load_dotenv()

MODEL = "claude-haiku-4-5-20251001"

SYSTEM_PROMPT = (
    "You are a commercial analyst who writes short, plain-English briefings for "
    "credit, account-management and procurement teams. They monitor UK companies "
    "via Companies House filings but are not accountants or lawyers. "
    "Explain what a filing event means in practical commercial terms. Be factual "
    "and measured — never alarmist. Base your briefing only on the filing details "
    "provided; if the significance is ambiguous, say so. This is an advisory signal "
    "for a human to act on, not financial or legal advice."
)


def _format_values(values):
    """Render the description_values dict as readable lines for the prompt."""
    if not values:
        return "  (none provided)"
    return "\n".join(f"  - {key}: {value}" for key, value in values.items())


def build_user_prompt(f):
    type_code = f.get("type") or ""
    type_label = friendly_type(type_code, fallback=type_code)
    return (
        f"Write a briefing about this Companies House filing.\n\n"
        f"Company: {f['company_name']} ({f['company_number']})\n"
        f"Date: {f['date']}\n"
        f"Filing type: {type_code} ({type_label})\n"
        f"Category: {f['category']}\n"
        f"Description code: {f['description']}\n"
        f"Filing details:\n{_format_values(f.get('description_values'))}\n\n"
        f"Use the filing details above (e.g. officer name, dates, share figures) to make "
        f"the briefing specific rather than generic. Format it as exactly these three "
        f"short sections:\n"
        f"What happened: (one sentence, plain English)\n"
        f"Why it matters: (1-2 sentences on the commercial signal)\n"
        f"Suggested action: (one sentence)"
    )


def generate_briefing(f):
    client = anthropic.Anthropic()
    message = client.messages.create(
        model=MODEL,
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_user_prompt(f)}],
    )
    return message.content[0].text