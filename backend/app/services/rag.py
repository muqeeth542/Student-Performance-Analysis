from __future__ import annotations

from pathlib import Path
import numpy as np
from sklearn.decomposition import PCA

from app.core.config import settings
from app.services.document_loader import chunk_text, extract_pdf_text
from app.services.embeddings import EmbeddingService
from app.services.llm import LLMService
from app.services.vector_store import VectorStore


class RAGService:
    def __init__(self):
        self.embedder = EmbeddingService(settings.embedding_model)
        self.store = VectorStore(settings.data_dir)
        self.llm = LLMService(
            provider=settings.llm_provider,
            ollama_base_url=settings.ollama_base_url,
            ollama_model=settings.ollama_model,
            openai_model=settings.openai_model,
            openai_api_key=settings.openai_api_key,
        )

    def ingest_pdf(self, path: Path) -> dict:
        text = extract_pdf_text(path)
        chunks = chunk_text(text, source=path.name, chunk_size=settings.chunk_size, overlap=settings.chunk_overlap)
        if not chunks:
            return {"chunks": 0, "source": path.name}

        texts = [c.text for c in chunks]
        vectors = self.embedder.encode(texts)
        metas = [
            {
                "chunk_id": c.chunk_id,
                "source": c.source,
                "text": c.text,
            }
            for c in chunks
        ]
        self.store.add(vectors, metas)
        return {"chunks": len(chunks), "source": path.name}

    def retrieve(self, question: str, top_k: int | None = None) -> list[dict]:
        k = top_k or settings.top_k
        qvec = self.embedder.encode([question])[0]
        return self.store.search(qvec, k)

    @staticmethod
    def build_prompt(question: str, contexts: list[dict]) -> str:
        context_blob = "\n\n".join(
            [f"[{i+1}] {c['text']}" for i, c in enumerate(contexts)]
        )
        return (
            "You are a precise RAG assistant. Use only the context below. "
            "If the answer is not present, say you don't know.\n\n"
            f"Context:\n{context_blob}\n\nQuestion: {question}\nAnswer:"
        )

    async def answer(self, question: str, top_k: int | None = None) -> tuple[str, list[dict]]:
        contexts = self.retrieve(question, top_k=top_k)
        prompt = self.build_prompt(question, contexts)
        answer = await self.llm.generate(prompt)
        return answer, contexts

    async def stream_answer(self, question: str, top_k: int | None = None):
        contexts = self.retrieve(question, top_k=top_k)
        prompt = self.build_prompt(question, contexts)
        return self.llm.generate_stream(prompt), contexts

    def graph_points(self) -> list[dict]:
        if self.store.embeddings is None or len(self.store.metadata) == 0:
            return []

        embeddings = self.store.embeddings
        n = embeddings.shape[0]
        if n == 1:
            coords = np.array([[0.0, 0.0, 0.0]])
        else:
            pca = PCA(n_components=3)
            coords = pca.fit_transform(embeddings)
            max_abs = np.max(np.abs(coords), axis=0)
            max_abs[max_abs == 0] = 1
            coords = coords / max_abs

        points: list[dict] = []
        for meta, xyz in zip(self.store.metadata, coords):
            points.append(
                {
                    "chunk_id": meta["chunk_id"],
                    "source": meta["source"],
                    "text": meta["text"],
                    "x": float(xyz[0]),
                    "y": float(xyz[1]),
                    "z": float(xyz[2]),
                }
            )
        return points


rag_service = RAGService()
