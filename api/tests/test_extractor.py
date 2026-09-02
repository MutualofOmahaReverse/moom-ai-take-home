"""Tests for the extraction service."""

from app.services.extractor import parse_model_json
from app.prompts import build_extraction_prompt


def test_parse_model_json_handles_plain_json():
    assert parse_model_json('{"employer": "ACME"}') == {"employer": "ACME"}


def test_parse_model_json_survives_garbage():
    assert parse_model_json("not json at all") == {}


def test_extraction_prompt_lists_the_right_fields():
    prompt = build_extraction_prompt("pay_stub", "some content")
    assert "gross_pay" in prompt
    assert "employer" in prompt


def test_extraction_prompt_for_unknown_type():
    prompt = build_extraction_prompt("something_new", "content")
    assert prompt is not None
