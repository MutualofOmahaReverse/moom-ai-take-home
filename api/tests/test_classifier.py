"""Tests for the classification service."""

from app.services import classifier
from app.prompts import build_classification_prompt, DOC_TYPES


def test_stub_classify_returns_a_result():
    """The keyword fallback should return something for any document."""
    doc = {"id": 1, "content": "ACME PAYROLL Pay Period 01/01 Gross 2400.00"}
    result = classifier._stub_classify(doc)
    assert result is not None


def test_prompt_includes_the_document_content():
    prompt = build_classification_prompt("scan.pdf", "FIRST MERIDIAN BANK balance 100")
    assert "FIRST MERIDIAN BANK" in prompt
    assert "scan.pdf" in prompt


def test_all_doc_types_appear_in_the_prompt():
    """Every type the classifier may return should be described in the prompt."""
    prompt = build_classification_prompt("x.pdf", "content")
    for doc_type in DOC_TYPES:
        assert doc_type in prompt


def test_needs_review_flags_low_confidence():
    assert classifier.needs_review(0.4) is True
