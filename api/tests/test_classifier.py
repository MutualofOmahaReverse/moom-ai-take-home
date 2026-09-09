"""Tests for the classification service."""

from app.services import classifier, offline
from app.prompts import build_classification_prompt, DOC_TYPES


def test_offline_classify_returns_a_result():
    """The offline classifier should return something for any document."""
    doc_type, confidence = offline.classify(
        "ACME PAYROLL Pay Period 01/01 Gross 2400.00"
    )
    assert doc_type is not None


def test_prompt_includes_the_document_content():
    prompt = build_classification_prompt("scan.pdf", "FIRST MERIDIAN BANK balance 100")
    assert "FIRST MERIDIAN BANK" in prompt
    assert "scan.pdf" in prompt


def test_all_doc_types_appear_in_the_prompt():
    """Every type the classifier may return should be described in the prompt."""
    prompt = build_classification_prompt("x.pdf", "content")
    for doc_type in DOC_TYPES:
        assert doc_type in prompt


def test_needs_review_is_available():
    """The review gate should be importable from the classifier module."""
    assert callable(classifier.needs_review)
