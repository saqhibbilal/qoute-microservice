import os
from decimal import Decimal
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Load env
MOCK_LLM = os.getenv("MOCK_LLM", "false").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = None
if not MOCK_LLM and OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)


def calculate_quote(request):
    line_totals = []
    grand_total = Decimal("0")

    for item in request.items:
        margin_multiplier = Decimal("1") + (item.margin_pct / 100)
        line_total = item.unit_cost * margin_multiplier * Decimal(item.qty)
        line_totals.append({
            "sku": item.sku,
            "qty": item.qty,
            "unit_cost": item.unit_cost,
            "margin_pct": item.margin_pct,
            "line_total": line_total.quantize(Decimal("0.01"))
        })
        grand_total += line_total

    grand_total = grand_total.quantize(Decimal("0.01"))
    email_draft = generate_email_draft(request, line_totals, grand_total)

    return {
        "line_totals": line_totals,
        "grand_total": grand_total,
        "currency": request.currency,
        "email_draft": email_draft
    }


def generate_email_draft(request, line_totals, grand_total):
    if MOCK_LLM:
        return _mock_email_draft(request, line_totals, grand_total)

    if not client:
        return "ERROR: OpenAI client not initialized (missing API key)."

    prompt = _build_prompt(request, line_totals, grand_total)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"LLM Error: {str(e)}"


def _mock_email_draft(request, line_totals, grand_total):
    lang = request.client.lang
    name = request.client.name
    currency = request.currency

    if lang == "ar":
        lines = "\n".join([
            f"• {lt['sku']}: {lt['qty']} × {lt['unit_cost']} {currency} + {lt['margin_pct']}% = {lt['line_total']} {currency}"
            for lt in line_totals
        ])
        return f"""السيد/ة المحترم في {name},

نشكركم على طلب التسعير. إليكم التفاصيل:

{lines}

الإجمالي: {grand_total} {currency}

شروط التسليم: {request.delivery_terms}
ملاحظات: {request.notes or "لا توجد"}

نتطلع لخدمتكم.
فريق المبيعات - ألروف للإنارة
"""
    else:
        lines = "\n".join([
            f"- {lt['sku']}: {lt['qty']} × {lt['unit_cost']} {currency} + {lt['margin_pct']}% margin = {lt['line_total']} {currency}"
            for lt in line_totals
        ])
        return f"""Dear {name},

Thank you for your quotation request. Here are the details:

{lines}

Grand Total: {grand_total} {currency}

Delivery Terms: {request.delivery_terms}
Notes: {request.notes or "None"}

We look forward to serving you.

Best regards,  
Alrouf Lighting Sales Team
"""


def _build_prompt(request, line_totals, grand_total):
    lang = "Arabic" if request.client.lang == "ar" else "English"
    lines = "\n".join([
        f"{lt['sku']}: {lt['qty']} units at {lt['unit_cost']} {request.currency} each + {lt['margin_pct']}% margin = {lt['line_total']} {request.currency}"
        for lt in line_totals
    ])
    return f"""
Write a professional quotation email in {lang} to {request.client.name} ({request.client.contact}).

Include:
- Line items: {lines}
- Grand total: {grand_total} {request.currency}
- Delivery: {request.delivery_terms}
- Notes: {request.notes or "None"}

Keep it short, polite, and formal. Use proper {lang} script.
"""