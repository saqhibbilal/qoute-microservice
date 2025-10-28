from fastapi import FastAPI, HTTPException
from app.models import QuoteRequest
from app.utils import calculate_quote
from decimal import Decimal

app = FastAPI(
    title="Quotation Microservice",
    description="Task 2: Generate quotes and bilingual email drafts",
    version="1.0.0"
)


@app.get("/")
def home():
    return {"message": "Quotation Microservice is running! Go to /docs"}


@app.post("/quote")
def create_quote(request: QuoteRequest):
    try:
        result = calculate_quote(request)  # Returns dict

        # Format line totals with 2 decimal places
        line_totals = []
        for lt in result["line_totals"]:
            line_totals.append({
                "sku": lt["sku"],
                "qty": lt["qty"],
                "unit_cost": f"{lt['unit_cost']:.2f}",
                "margin_pct": f"{lt['margin_pct']:.2f}",
                "line_total": f"{lt['line_total']:.2f}"
            })

        return {
            "line_totals": line_totals,
            "grand_total": f"{result['grand_total']:.2f}",
            "currency": result["currency"],
            "email_draft": result["email_draft"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))