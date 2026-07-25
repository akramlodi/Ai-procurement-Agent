import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip("/rest/v1").rstrip("/")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

supabase = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global supabase
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    yield


app = FastAPI(title="AI Procurement Backend", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class WorkspaceCreate(BaseModel):
    name: str
    description: str
    status: str = "Draft"


class WorkspaceResponse(BaseModel):
    id: str
    name: str
    description: str
    status: str
    created_at: str


@app.get("/")
def read_root() -> JSONResponse:
    return JSONResponse(content={"message": "AI Procurement API is running", "phase": "2"})


@app.get("/health")
def health_check() -> JSONResponse:
    return JSONResponse(content={"status": "ok"})


@app.post("/api/workspaces", response_model=WorkspaceResponse)
def create_workspace(payload: WorkspaceCreate):
    try:
        result = (
            supabase.table("procurements")
            .insert({
                "name": payload.name,
                "description": payload.description,
                "status": payload.status,
            })
            .execute()
        )
        row = result.data[0]
        return WorkspaceResponse(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            status=row["status"],
            created_at=row["created_at"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/workspaces", response_model=list[WorkspaceResponse])
def list_workspaces():
    try:
        result = (
            supabase.table("procurements")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )
        return [
            WorkspaceResponse(
                id=row["id"],
                name=row["name"],
                description=row["description"],
                status=row["status"],
                created_at=row["created_at"],
            )
            for row in result.data
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
