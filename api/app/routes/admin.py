"""Admin routes.

Small operational endpoints used during development. Not linked from the UI.
"""

from fastapi import APIRouter

from app import db

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats")
def stats():
    """Counts by table, for a quick sanity check that seeding worked."""
    return {
        "loan_files": db.query("SELECT count(*) AS n FROM loan_file")[0]["n"],
        "documents": db.query("SELECT count(*) AS n FROM document")[0]["n"],
        "unclassified": db.query(
            "SELECT count(*) AS n FROM document WHERE doc_type IS NULL"
        )[0]["n"],
        "extractions": db.query("SELECT count(*) AS n FROM extraction")[0]["n"],
    }


@router.get("/statuses")
def statuses():
    """Distinct values in loan_file.status, with counts."""
    return db.query(
        "SELECT status, count(*) AS n FROM loan_file GROUP BY status ORDER BY n DESC"
    )


@router.post("/reset-classifications")
def reset_classifications():
    """Clear every classification so the classifier can be re-run from scratch."""
    db.execute(
        "UPDATE document SET doc_type = NULL, confidence = NULL, classified_at = NULL"
    )
    return {"ok": True}


@router.post("/purge-extractions")
def purge_extractions():
    """Delete every extracted field."""
    db.execute("DELETE FROM extraction")
    return {"ok": True}
