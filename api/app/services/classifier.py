"""
Document classification service.

Sends a document's text to the model and asks it which of the known document
types it is. The result is written back to the document row along with the
model's stated confidence.

If no API key is configured the service falls back to a keyword-based stub so
that the rest of the application remains usable in local development.
"""

import json
import logging

import anthropic

from app.config import ANTHROPIC_API_KEY, CLASSIFIER_MODEL, CONFIDENCE_THRESHOLD, HAS_API_KEY
from app.prompts import build_classification_prompt
from app import db

logger = logging.getLogger(__name__)

# The client is constructed once at import time and reused for every call.
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) if HAS_API_KEY else None


def classify_document(doc_id: int) -> dict | None:
    """Classify a single document and persist the result.

    Loads the document from the database, builds a prompt, sends it to the
    model, parses the response, and writes doc_type and confidence back to the
    document row.

    Args:
        doc_id: the primary key of the document to classify.

    Returns:
        A dict with doc_type and confidence, or None if classification failed.
    """
    rows = db.query(
        "SELECT id, filename, content FROM document WHERE id = %s", (doc_id,)
    )
    if not rows:
        logger.warning("Document %s not found", doc_id)
        return None

    doc = rows[0]

    if not HAS_API_KEY:
        return _stub_classify(doc)

    prompt = build_classification_prompt(doc["filename"], doc["content"])

    try:
        response = client.messages.create(
            model=CLASSIFIER_MODEL,
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text
    except Exception as e:
        # If the API call fails for any reason we log it and move on. The
        # document simply stays unclassified and can be retried later.
        logger.error("Classification call failed for document %s: %s", doc_id, e)
        return None

    try:
        parsed = json.loads(text)
    except Exception as e:
        logger.error("Could not parse model response for document %s: %s", doc_id, e)
        return None

    doc_type = parsed.get("doc_type")
    confidence = parsed.get("confidence")

    db.execute(
        """UPDATE document
              SET doc_type = %s, confidence = %s, classified_at = now()
            WHERE id = %s""",
        (doc_type, str(confidence), doc_id),
    )

    return {"doc_type": doc_type, "confidence": confidence}


def classify_pending(limit: int = 50) -> list[dict]:
    """Classify every document that has not yet been classified.

    Walks the unclassified documents one at a time and calls classify_document
    on each. Returns a list of the results.
    """
    pending = db.query(
        "SELECT id FROM document WHERE doc_type IS NULL ORDER BY id LIMIT %s",
        (limit,),
    )

    results = []
    for row in pending:
        result = classify_document(row["id"])
        if result is not None:
            results.append(result)

    return results


def needs_review(confidence) -> bool:
    """Return True if a classification should be queued for human review.

    A classification is accepted automatically when the model's confidence is
    above the configured threshold. Anything at or below it gets reviewed.
    """
    return confidence <= CONFIDENCE_THRESHOLD


def _stub_classify(doc: dict) -> dict:
    """Keyword fallback used when no API key is configured.

    This is deliberately crude. It exists so that the application can be run
    end-to-end without credentials, not to be accurate.
    """
    content = (doc.get("content") or "").lower()

    if "w-2" in content or "w2" in content:
        guess = "w2"
    elif "pay period" in content or "earnings statement" in content or "gross" in content:
        guess = "pay_stub"
    elif "statement" in content and "balance" in content:
        guess = "bank_statement"
    elif "driver license" in content or "identification card" in content:
        guess = "photo_id"
    elif "policy" in content and "coverage" in content:
        guess = "homeowners_insurance"
    elif "parcel" in content or "tax bill" in content:
        guess = "property_tax_bill"
    elif "counseling" in content:
        guess = "counseling_certificate"
    else:
        guess = "other"

    db.execute(
        """UPDATE document
              SET doc_type = %s, confidence = %s, classified_at = now()
            WHERE id = %s""",
        (guess, "0.50", doc["id"]),
    )
    return {"doc_type": guess, "confidence": 0.5}
