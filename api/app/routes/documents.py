"""Routes for working with individual documents."""

from fastapi import APIRouter, HTTPException

from app import db
from app.services import classifier, extractor

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("")
def list_documents(loan_file_id: int | None = None):
    """List documents, optionally filtered to one loan file."""
    if loan_file_id is not None:
        return db.query(
            """SELECT id, loan_file_id, filename, doc_type, confidence,
                      uploaded_at, classified_at
                 FROM document WHERE loan_file_id = %s ORDER BY uploaded_at""",
            (loan_file_id,),
        )
    return db.query(
        """SELECT id, loan_file_id, filename, doc_type, confidence,
                  uploaded_at, classified_at
             FROM document ORDER BY uploaded_at DESC LIMIT 200"""
    )


@router.get("/{doc_id}")
def get_document(doc_id: int):
    """Return one document with its extracted fields."""
    rows = db.query("SELECT * FROM document WHERE id = %s", (doc_id,))
    if not rows:
        raise HTTPException(status_code=404, detail="document not found")

    doc = rows[0]
    doc["extractions"] = db.query(
        "SELECT field_name, field_value FROM extraction WHERE document_id = %s",
        (doc_id,),
    )
    return doc


@router.post("/{doc_id}/classify")
def classify(doc_id: int):
    """Classify one document."""
    result = classifier.classify_document(doc_id)
    if result is None:
        raise HTTPException(status_code=502, detail="classification failed")
    return result


@router.post("/{doc_id}/extract")
def extract(doc_id: int):
    """Extract fields from one already-classified document."""
    return extractor.extract_fields(doc_id)


@router.post("/classify-pending")
def classify_pending(limit: int = 50):
    """Classify everything that has not been classified yet."""
    return {"classified": classifier.classify_pending(limit)}
