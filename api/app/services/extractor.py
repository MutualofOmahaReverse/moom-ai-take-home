"""
Field extraction service.

Once a document has been classified, this service pulls the handful of
structured fields that the downstream checklist cares about out of the
document text and writes them to the extraction table.

Historically this ran as a nightly batch job over every document in the
system. It now runs on demand, one document at a time, triggered from the
document detail route.
"""

import json
import logging

import anthropic

from app.config import ANTHROPIC_API_KEY, CLASSIFIER_MODEL, HAS_API_KEY
from app.prompts import build_extraction_prompt
from app import db

logger = logging.getLogger(__name__)

_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) if HAS_API_KEY else None


def parse_model_json(raw: str) -> dict:
    """Parse a JSON object out of a model response.

    Args:
        raw: the raw text of the model's reply.

    Returns:
        The parsed dictionary, or an empty dictionary if parsing failed.
    """
    try:
        return json.loads(raw)
    except Exception:
        return {}


def extract_fields(doc_id: int) -> dict:
    """Extract the configured fields for one document.

    Skips documents that have not been classified yet, since which fields to
    ask for depends on the document type.
    """
    rows = db.query(
        "SELECT id, doc_type, content FROM document WHERE id = %s", (doc_id,)
    )
    if not rows:
        return {}

    doc = rows[0]
    if not doc["doc_type"]:
        logger.info("Document %s is not classified yet, skipping extraction", doc_id)
        return {}

    if not HAS_API_KEY:
        return {}

    prompt = build_extraction_prompt(doc["doc_type"], doc["content"])

    response = _client.messages.create(
        model=CLASSIFIER_MODEL,
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )

    fields = parse_model_json(response.content[0].text)

    for name, value in fields.items():
        db.execute(
            """INSERT INTO extraction (document_id, field_name, field_value)
                    VALUES (%s, %s, %s)""",
            (doc_id, name, None if value is None else str(value)),
        )

    return fields
