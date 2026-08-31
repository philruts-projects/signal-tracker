"""
lookups.py — plain-English labels for Companies House filing form-type codes.

The API's `type` field uses statutory form codes (AA, SH01, TM01, ...). This maps
the common ones to readable labels. Anything not listed falls back to the code
itself, so the app never breaks on an unknown type — just shows the raw code.

Reference: Companies House api-enumerations (constants.yml) and the standard
statutory forms. Extend this dict as new types appear on the watchlist.
"""

FILING_TYPE_LABELS = {
    # Accounts
    "AA": "Annual accounts",
    "AA01": "Change of accounting reference date",
    # Confirmation statement / annual return
    "CS01": "Confirmation statement",
    "AR01": "Annual return",
    # Officers
    "AP01": "Appointment of a director",
    "AP02": "Appointment of a corporate director",
    "AP03": "Appointment of a secretary",
    "AP04": "Appointment of a corporate secretary",
    "TM01": "Termination of a director",
    "TM02": "Termination of a secretary",
    "CH01": "Change of a director's details",
    "CH03": "Change of a secretary's details",
    # Registered office / address
    "AD01": "Change of registered office address",
    "AD02": "Single alternative inspection location",
    # Share capital
    "SH01": "Allotment of shares",
    "SH03": "Purchase of own shares",
    "SH06": "Cancellation of shares",
    "SH07": "Cancellation of treasury shares",
    # Persons with significant control (ownership)
    "PSC01": "Notification of a person with significant control",
    "PSC02": "Notification of a relevant legal entity with significant control",
    "PSC07": "Cessation of a person with significant control",
    # Charges (secured borrowing) — credit signals
    "MR01": "Registration of a charge (secured borrowing)",
    "MR02": "Registration of a charge (property/undertaking)",
    "MR04": "Charge satisfied in full (debt repaid)",
    # Resolutions & misc
    "RESOLUTIONS": "Resolution",
    "MISC": "Miscellaneous filing",
    # Insolvency / strike-off — distress signals
    "GAZ1": "First Gazette notice for compulsory strike-off",
    "GAZ2": "Final Gazette notice — company dissolved",
    "LIQ01": "Liquidation filing",
    "AM01": "Administration order",
}


def friendly_type(type_code, fallback=""):
    """Return a plain-English label for a filing type code, or a sensible fallback."""
    if not type_code:
        return fallback
    return FILING_TYPE_LABELS.get(type_code, fallback or type_code)
