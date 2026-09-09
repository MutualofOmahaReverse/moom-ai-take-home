"""Tests for the offline classifier and extractor."""

from app.services import offline


def test_classifies_a_w2_before_a_pay_stub():
    doc_type, _ = offline.classify("Form W-2 Wage and Tax Statement 2025 Wages 88,000.00")
    assert doc_type == "w2"


def test_classifies_a_driver_license():
    doc_type, _ = offline.classify("STATE OF NEVADA DRIVER LICENSE SMITH JOHN")
    assert doc_type == "photo_id"


def test_unrecognised_content_falls_back_to_other():
    doc_type, confidence = offline.classify("INVOICE Roofing repair 4,200.00")
    assert doc_type == "other"
    assert confidence < 0.5


def test_extracts_gross_pay_from_a_pay_stub():
    fields = offline.extract("pay_stub", "Gross Pay: 2,180.00\nNet Pay: 1,702.44")
    assert fields["gross_pay"] == "2180.00"


def test_missing_fields_are_omitted_not_nulled():
    fields = offline.extract("pay_stub", "no amounts here at all")
    assert "gross_pay" not in fields
