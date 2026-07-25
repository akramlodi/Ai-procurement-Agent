import logging

from app.services.classification_service import GeminiClassificationService
from app.services.chunking_service import ChunkingService
from app.services.database_service import DatabaseService
from app.services.embedding_service import HuggingFaceEmbeddingService
from app.services.extraction_service import GeminiExtractionService
from app.services.storage_service import StorageService
from app.services.summary_service import GeminiSummaryService
from app.services.text_extractor import TextExtractor

logger = logging.getLogger(__name__)

CONTENT_TYPES = {
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "doc": "application/msword",
}


class DocumentProcessor:
    def __init__(self, supabase):
        self.db = DatabaseService(supabase)
        self.storage = StorageService(supabase)
        self.extractor = TextExtractor()
        self.classifier = GeminiClassificationService()
        self.summarizer = GeminiSummaryService()
        self.extraction = GeminiExtractionService()
        self.chunker = ChunkingService()
        self.embedder = HuggingFaceEmbeddingService()

    def process_document(self, procurement_id: str, document_id: str, file_bytes: bytes, filename: str) -> None:
        ext = filename.rsplit(".", 1)[-1].lower()
        try:
            storage_path = self.storage.upload_file(
                procurement_id, filename, file_bytes,
                content_type=CONTENT_TYPES.get(ext, "application/octet-stream"),
            )
            self.db.update_document(document_id, {"storage_path": storage_path})
            logger.info("Uploaded %s to storage", filename)

            text = self.extractor.extract_text(file_bytes, filename)
            if not text.strip():
                self.db.update_document(document_id, {"document_status": "failed", "ai_summary": "No text extracted"})
                return
            logger.info("Extracted %d chars from %s", len(text), filename)

            doc_type = self.classifier.classify_document(text)
            self.db.update_document(document_id, {"document_type": doc_type})
            logger.info("Classified %s as %s", filename, doc_type)

            summary = self.summarizer.generate_summary(text)
            self.db.update_document(document_id, {"ai_summary": summary})
            logger.info("Generated summary for %s", filename)

            if doc_type == "Supplier Quotation":
                info = self.extraction.extract_procurement_info(text)
                if info:
                    known_fields = {"supplier_name", "price", "currency", "warranty", "delivery_days", "payment_terms", "compliance_score"}
                    supplier_data = {"procurement_id": procurement_id, "document_id": document_id}
                    raw_extraction = {}
                    for k, v in info.items():
                        if k in known_fields:
                            supplier_data[k] = v
                        else:
                            raw_extraction[k] = v
                    if raw_extraction:
                        supplier_data["raw_extraction"] = raw_extraction
                    self.db.create_supplier(supplier_data)
                    logger.info("Created supplier record for %s", filename)

            chunks = self.chunker.chunk_text(text)
            if chunks:
                embeddings = self.embedder.generate_embeddings(chunks)
                chunk_records = []
                for i, (chunk_text, embedding) in enumerate(zip(chunks, embeddings)):
                    chunk_records.append({
                        "document_id": document_id,
                        "chunk_index": i,
                        "chunk_text": chunk_text,
                        "embedding": str(embedding),
                        "metadata": {
                            "procurement_id": procurement_id,
                            "document_id": document_id,
                            "document_type": doc_type,
                        },
                    })
                self.db.create_chunks(chunk_records)
                logger.info("Stored %d chunks for %s", len(chunks), filename)

            self.db.update_document(document_id, {"document_status": "completed"})
            logger.info("Completed processing for %s", filename)

        except Exception as e:
            logger.error("Processing failed for %s: %s", filename, e)
            self.db.update_document(document_id, {"document_status": "failed", "ai_summary": str(e)})
