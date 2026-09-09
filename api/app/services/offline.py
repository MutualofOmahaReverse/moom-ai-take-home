"""
Offline classification and extraction.

This is the original implementation, from before the model was wired in. It is
still the default path: it needs no credentials, it is deterministic, and it is
fast enough that nobody has had a reason to turn it off for local work.

It is deliberately crude. Classification is keyword matching and extraction is
a handful of regexes. Neither is meant to be accurate -- they are meant to keep
the application usable end to end without an API key.
"""

import re

# Ordered most specific first. The first rule whose keywords all appear wins,
# so 'w2' has to be checked before the generic wage keywords.
_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("w2",                     ("w-2",)),
    ("w2",                     ("wage and tax statement",)),
    ("counseling_certificate", ("counseling",)),
    ("photo_id",               ("driver license",)),
    ("photo_id",               ("identification card",)),
    ("property_tax_bill",      ("parcel",)),
    ("property_tax_bill",      ("tax bill",)),
    ("property_tax_bill",      ("property tax",)),
    ("homeowners_insurance",   ("policy", "coverage")),
    ("homeowners_insurance",   ("policy", "premium")),
    ("pay_stub",               ("pay period",)),
    ("pay_stub",               ("earnings statement",)),
    ("pay_stub",               ("payroll",)),
    ("bank_statement",         ("statement", "balance")),
]

# Rough confidence per type. A keyword hit on a distinctive phrase is worth
# more than one on a common word.
_CONFIDENCE = {
    "w2": 0.82,
    "counseling_certificate": 0.80,
    "photo_id": 0.86,
    "property_tax_bill": 0.78,
    "homeowners_insurance": 0.74,
    "pay_stub": 0.77,
    "bank_statement": 0.71,
    "other": 0.30,
}


def classify(content: str) -> tuple[str, float]:
    """Guess a document type from its text.

    Returns (doc_type, confidence). Falls back to ('other', 0.30) when no rule
    matches, which is most of the time for anything unusual.
    """
    text = (content or "").lower()

    for doc_type, keywords in _RULES:
        if all(k in text for k in keywords):
            return doc_type, _CONFIDENCE[doc_type]

    return "other", _CONFIDENCE["other"]


# Field patterns, by document type. Only the fields that are reliably findable
# with a regex are here; the model path asks for more.
_PATTERNS: dict[str, dict[str, str]] = {
    "pay_stub": {
        "gross_pay": r"gross(?:\s+pay)?[:\s]+([\d,]+\.\d{2})",
        "net_pay": r"net(?:\s+pay)?[:\s]+([\d,]+\.\d{2})",
    },
    "bank_statement": {
        "ending_balance": r"ending\s+balance[:\s]+([\d,]+\.\d{2})",
        "account_last4": r"(?:ending|\*{2,})\s*(\d{4})\b",
    },
    "homeowners_insurance": {
        "policy_number": r"policy\s*(?:no\.?|number)?[:\s]*([A-Z]{2}-?\d{4,})",
    },
    "property_tax_bill": {
        "parcel": r"parcel[:\s]+([\d\-]+)",
    },
    "w2": {
        "wages": r"wages[^\d]{0,40}([\d,]+\.\d{2})",
    },
}


def extract(doc_type: str, content: str) -> dict:
    """Pull whatever fields the regexes can find for this document type.

    Returns a dict of field name to string value. Fields that do not match are
    left out entirely rather than set to None -- a missing key and a null value
    mean different things downstream.
    """
    patterns = _PATTERNS.get(doc_type, {})
    found = {}

    for field, pattern in patterns.items():
        match = re.search(pattern, content or "", re.IGNORECASE)
        if match:
            found[field] = match.group(1).replace(",", "")

    return found
