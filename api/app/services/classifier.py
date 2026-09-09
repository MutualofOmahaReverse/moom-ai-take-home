"""
Document classification service.

Decides which of the known document types an uploaded file is, and writes the
answer back to the document row along with a confidence.

Two paths. The offline classifier in app/services/offline.py runs by default
and needs no credentials. When ANTHROPIC_API_KEY is set, the live path sends
the document text to the model instead.
"""

import json
import logging

import anthropic

from app.config import (
    ANTHROPIC_API_KEY,
    CLASSIFIER_MODEL,
    CONFIDENCE_THRESHOLD,
    USE_LIVE_MODEL,
)
from app.prompts import build_classification_prompt
from app.services import offline
from app import db

logger = logging.getLogger(__name__)

# The client is constructed once at import time and reused for every call.
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) if USE_LIVE_MODEL else None


def classify_document(doc_id: int) -> dict | None:
    """Classify a single document and persist the result.

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

    if USE_LIVE_MODEL:
        result = _classify_with_model(doc)
    else:
        doc_type, confidence = offline.classify(doc["content"])
        result = {"doc_type": doc_type, "confidence": confidence}

    if result is None:
        return None

    db.execute(
        """UPDATE document
              SET doc_type = %s, confidence = %s, classified_at = now()
            WHERE id = %s""",
        (result["doc_type"], str(result["confidence"]), doc_id),
    )
    return result


def _classify_with_model(doc: dict) -> dict | None:
    """Ask the model to classify one document.

    Returns None when the call or the parse fails, in which case the document
    is left unclassified and can be retried later.
    """
    prompt = build_classification_prompt(doc["filename"], doc["content"])

    try:
        response = client.messages.create(
            model=CLASSIFIER_MODEL,
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text
    except Exception as e:
        logger.error("Classification call failed for document %s: %s", doc["id"], e)
        return None

    try:
        parsed = json.loads(text)
    except Exception as e:
        logger.error(
            "Could not parse model response for document %s: %s", doc["id"], e
        )
        return None

    return {
        "doc_type": parsed.get("doc_type"),
        "confidence": parsed.get("confidence"),
    }


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
