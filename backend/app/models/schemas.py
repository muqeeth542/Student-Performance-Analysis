from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=2)
    top_k: int | None = Field(default=None, ge=1, le=20)


class RetrievedChunk(BaseModel):
    chunk_id: str
    score: float
    text: str
    source: str


class QueryResponse(BaseModel):
    answer: str
    chunks: list[RetrievedChunk]


class ChunkPoint(BaseModel):
    chunk_id: str
    source: str
    text: str
    x: float
    y: float
    z: float


class GraphResponse(BaseModel):
    points: list[ChunkPoint]
