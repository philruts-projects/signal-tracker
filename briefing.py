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
    "and measured — never alarmist. Base your briefing ONLY on the filing details provided "
    "and its assessed severity. Do not use outside knowledge or real-world events about the "
    "company, even if you recognise it; if you can't explain the significance from the filing "
    "alone, say the risk comes from the filing type or the company's status. This is an "
    "advisory signal for a human to act on, not financial or legal advice."
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
        f"Filing details:\n{_format_values(f.get('description_values'))}\n"
        f"Assessed severity (rules-based): {f.get('severity', 'not set')}\n\n"
        f"Use the filing details above to be specific rather than generic, and write the briefing "
        f"consistent with the assessed severity — a Serious or Critical filing must not read as routine. "
        f"Format it as exactly these four short lines:\n"
        f"Risk: {f.get('severity', 'not set')}\n"
        f"What happened: (one sentence, plain English)\n"
        f"Why it matters: (1-2 sentences on the commercial signal, matching the risk level)\n"
        f"Suggested action: (one sentence)"
    )


def extract_text(message):
    """Return the text of the first text block, skipping any reasoning/thinking blocks."""
    for block in message.content:
        if getattr(block, "type", None) == "text":
            return block.text
    for block in message.content:          # fallback
        if hasattr(block, "text"):
            return block.text
    return ""


def generate_briefing(f):
    client = anthropic.Anthropic()
    message = client.messages.create(
        model=MODEL,
        max_tokens=450,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": build_user_prompt(f)}],
    )
    return extract_text(message)