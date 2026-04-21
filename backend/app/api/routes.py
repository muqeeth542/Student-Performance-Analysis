from __future__ import annotations

from pathlib import Path
import json
import uuid
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.core.config import settings
from app.models.schemas import GraphResponse, QueryRequest, QueryResponse, RetrievedChunk
from app.services.rag import rag_service

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    uploads_dir = settings.data_dir / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)

    safe_name = f"{uuid.uuid4()}_{Path(file.filename).name}"
    target = uploads_dir / safe_name
    target.write_bytes(await file.read())

    result = rag_service.ingest_pdf(target)
    return {"message": "Uploaded and indexed", **result}


@router.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    answer, contexts = await rag_service.answer(req.question, req.top_k)
    return QueryResponse(
        answer=answer,
        chunks=[RetrievedChunk(**c) for c in contexts],
    )


@router.post("/query/stream")
async def query_stream(req: QueryRequest):
    generator, contexts = await rag_service.stream_answer(req.question, req.top_k)

    async def event_stream():
        yield f"event: context\ndata: {json.dumps(contexts)}\n\n"
        async for token in generator:
            yield f"data: {token}\n\n"
        yield "event: done\ndata: [DONE]\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@router.post("/reset")
async def reset_index():
    rag_service.store.reset()
    return {"message": "Index cleared"}


@router.get("/graph", response_model=GraphResponse)
async def graph():
    points = rag_service.graph_points()
    return GraphResponse(points=points)
