from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, UploadFile, File

from app.models import DocumentResponse
from app.services.document_processor import DocumentProcessor

router = APIRouter()


@router.post("/api/workspaces/{procurement_id}/documents", response_model=list[DocumentResponse])
async def upload_documents(
    procurement_id: str,
    background_tasks: BackgroundTasks,
    request: Request,
    files: list[UploadFile] = File(...),
):
    supabase = request.app.state.supabase
    processor = DocumentProcessor(supabase)

    created: list[dict] = []
    for file in files:
        content = await file.read()
        if not content:
            continue

        doc = processor.db.create_document(procurement_id, file.filename, "")
        created.append(doc)
        background_tasks.add_task(
            processor.process_document, procurement_id, doc["id"], content, file.filename,
        )

    if not created:
        raise HTTPException(status_code=400, detail="No valid files provided")

    return [
        DocumentResponse(
            id=row["id"],
            procurement_id=row["procurement_id"],
            filename=row["filename"],
            document_type=row["document_type"],
            storage_path=row.get("storage_path"),
            document_status=row["document_status"],
            ai_summary=row.get("ai_summary"),
            uploaded_at=row["uploaded_at"],
        )
        for row in created
    ]


@router.get("/api/workspaces/{procurement_id}/documents", response_model=list[DocumentResponse])
async def list_documents(procurement_id: str, request: Request):
    supabase = request.app.state.supabase
    result = (
        supabase.table("documents")
        .select("*")
        .eq("procurement_id", procurement_id)
        .order("uploaded_at", desc=True)
        .execute()
    )
    return [
        DocumentResponse(
            id=row["id"],
            procurement_id=row["procurement_id"],
            filename=row["filename"],
            document_type=row["document_type"],
            storage_path=row.get("storage_path"),
            document_status=row["document_status"],
            ai_summary=row.get("ai_summary"),
            uploaded_at=row["uploaded_at"],
        )
        for row in result.data
    ]
