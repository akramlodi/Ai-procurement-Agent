from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: str
    procurement_id: str
    filename: str
    document_type: str
    storage_path: str | None = None
    document_status: str
    ai_summary: str | None = None
    uploaded_at: str


class SupplierResponse(BaseModel):
    id: str
    procurement_id: str
    document_id: str
    supplier_name: str | None = None
    price: float | None = None
    currency: str | None = None
    warranty: str | None = None
    delivery_days: int | None = None
    payment_terms: str | None = None
    compliance_score: float | None = None
    raw_extraction: dict | None = None
    created_at: str
