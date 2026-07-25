import logging

logger = logging.getLogger(__name__)


class DatabaseService:
    def __init__(self, supabase):
        self.supabase = supabase

    def create_document(self, procurement_id: str, filename: str, storage_path: str, document_type: str = "Unknown") -> dict:
        result = (
            self.supabase.table("documents")
            .insert({
                "procurement_id": procurement_id,
                "filename": filename,
                 "document_type": document_type,
                "storage_path": storage_path,
                "document_status": "processing",
            })
            .execute()
        )
        return result.data[0]

    def update_document(self, document_id: str, updates: dict) -> dict:
        result = (
            self.supabase.table("documents")
            .update(updates)
            .eq("id", document_id)
            .execute()
        )
        return result.data[0]

    def list_documents(self, procurement_id: str) -> list[dict]:
        result = (
            self.supabase.table("documents")
            .select("*")
            .eq("procurement_id", procurement_id)
            .order("uploaded_at", desc=True)
            .execute()
        )
        return result.data

    def create_supplier(self, data: dict) -> dict:
        result = (
            self.supabase.table("suppliers")
            .insert(data)
            .execute()
        )
        return result.data[0]

    def create_chunks(self, chunks: list[dict]) -> None:
        if not chunks:
            return
        self.supabase.table("document_chunks").insert(chunks).execute()
