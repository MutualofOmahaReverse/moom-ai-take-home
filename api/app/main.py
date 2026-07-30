"""
Loan intake triage API.

Documents arrive against a loan file, get classified by type, have a few
fields pulled out of them, and the file is checked against a per-product
checklist to see what is still missing.
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import admin, documents, loans

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Loan Intake Triage", version="0.3.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(loans.router)
app.include_router(documents.router)
app.include_router(admin.router)


@app.get("/health")
def health():
    """Liveness check."""
    return {"status": "ok"}
