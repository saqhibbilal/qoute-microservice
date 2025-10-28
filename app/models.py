from pydantic import BaseModel, Field, EmailStr
from typing import Literal, List
from decimal import Decimal


class Client(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Gulf Eng."})
    contact: EmailStr = Field(..., json_schema_extra={"example": "omar@client.com"})
    lang: Literal["en", "ar"] = Field(..., json_schema_extra={"example": "en"}, description="Language: 'en' or 'ar'")


class Item(BaseModel):
    sku: str = Field(..., json_schema_extra={"example": "ALR-SL-90W"})
    qty: int = Field(..., gt=0, json_schema_extra={"example": 120})
    unit_cost: Decimal = Field(..., gt=0, json_schema_extra={"example": 240.0})
    margin_pct: Decimal = Field(..., ge=0, le=100, json_schema_extra={"example": 22})


class QuoteRequest(BaseModel):
    client: Client
    currency: str = Field(..., json_schema_extra={"example": "SAR"})
    items: List[Item] = Field(..., min_length=1)
    delivery_terms: str = Field(..., json_schema_extra={"example": "DAP Dammam, 4 weeks"})
    notes: str = Field("", json_schema_extra={"example": "Client asked for spec compliance with Tarsheed."})