import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
import os
os.environ["MOCK_LLM"] = "true"


def test_quote_endpoint_valid_en():
    payload = {
        "client": {"name": "Test Co", "contact": "test@co.com", "lang": "en"},
        "currency": "SAR",
        "items": [{"sku": "TEST-1", "qty": 2, "unit_cost": 100.0, "margin_pct": 20}],
        "delivery_terms": "EXW",
        "notes": ""
    }
    response = client.post("/quote", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["grand_total"] == "240.00"
    assert "Dear Test Co" in data["email_draft"]


def test_quote_endpoint_valid_ar():
    payload = {
        "client": {"name": "شركة اختبار", "contact": "test@co.com", "lang": "ar"},
        "currency": "SAR",
        "items": [{"sku": "TEST-1", "qty": 1, "unit_cost": 500.0, "margin_pct": 25}],
        "delivery_terms": "EXW",
        "notes": "ملاحظة"
    }
    response = client.post("/quote", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["grand_total"] == "625.00"
    assert "السيد/ة المحترم في شركة اختبار" in data["email_draft"]


def test_invalid_lang():
    payload = {**payload_en, "client": {**payload_en["client"], "lang": "fr"}}
    response = client.post("/quote", json=payload)
    assert response.status_code == 422


def test_empty_items():
    payload = {**payload_en, "items": []}
    response = client.post("/quote", json=payload)
    assert response.status_code == 422


# Helper
payload_en = {
    "client": {"name": "Test", "contact": "t@e.com", "lang": "en"},
    "currency": "SAR",
    "items": [{"sku": "X", "qty": 1, "unit_cost": 10, "margin_pct": 10}],
    "delivery_terms": "EXW",
    "notes": ""
}