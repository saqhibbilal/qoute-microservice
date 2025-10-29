# Quotation Microservice (Task 2)

A **FastAPI microservice** that **automatically calculates quotation totals** and **generates a professional email draft** in **English or Arabic** — using mock mode (no API key needed).

---

## Aim

> Turn a JSON quote request into a ready-to-send quotation email — instantly.

**Input**: Client name, items, unit cost, margin, delivery terms  
**Output**: Line totals, grand total, and a **bilingual email draft**

No manual math. No copy-paste. Perfect for Alrouf Lighting sales.

---

## Features

- `POST /quote` endpoint
- Accurate pricing: `unit_cost × (1 + margin%) × qty`
- Bilingual email draft (English / Arabic)
- **Mock mode**: Runs **without OpenAI key**
- Full input validation (Pydantic)
- OpenAPI docs: `http://127.0.0.1:8000/docs`
- 4 automated tests (pytest)
- Docker support
- Clean, readable JSON output

---

## Tech Stack

| Tool       | Purpose                     |
| ---------- | --------------------------- |
| FastAPI    | Fast API + auto docs        |
| Pydantic   | Input validation            |
| Decimal    | Accurate money math         |
| OpenAI API | Smart email drafts          |
| Mock LLM   | Run locally without secrets |
| pytest     | Test reliability            |
| Docker     | Deploy anywhere             |

---

---

## How to Run Locally

1. Clone the Repo
   git clone https://github.com/YOUR_USERNAME/quotation-microservice.git
   cd quotation-microservice
2. Create Virtual Environment
   python -m venv .venv
   .venv\Scripts\activate
3. Install Dependencies
   pip install -r requirements.txt

4. Run in Mock Mode (No OpenAI Key)
   $env:MOCK_LLM = "true"
   uvicorn app.main:app --reload

---

Run Tests using:

pytest -v

**Run with Docker**:
docker build -t quotation-ms .
docker run -p 8000:8000 quotation-ms

API Example (Try in /docs):
{
"client": {"name": "Gulf Eng.", "contact": "omar@client.com", "lang": "en"},
"currency": "SAR",
"items": [
{"sku": "ALR-SL-90W", "qty": 120, "unit_cost": 240.0, "margin_pct": 22},
{"sku": "ALR-OBL-12V", "qty": 40, "unit_cost": 95.5, "margin_pct": 18}
],
"delivery_terms": "DAP Dammam, 4 weeks",
"notes": "Client asked for spec compliance with Tarsheed."
}
