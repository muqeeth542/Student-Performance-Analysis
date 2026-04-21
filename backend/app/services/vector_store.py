from __future__ import annotations

import json
from pathlib import Path
import faiss
import numpy as np


class VectorStore:
    def __init__(self, storage_dir: Path):
        self.storage_dir = storage_dir
        self.index_path = storage_dir / "faiss.index"
        self.meta_path = storage_dir / "metadata.json"
        self.emb_path = storage_dir / "embeddings.npy"
        self.index: faiss.IndexFlatIP | None = None
        self.metadata: list[dict] = []
        self.embeddings: np.ndarray | None = None
        self._load()

    def _load(self) -> None:
        if self.index_path.exists() and self.meta_path.exists() and self.emb_path.exists():
            self.index = faiss.read_index(str(self.index_path))
            self.metadata = json.loads(self.meta_path.read_text())
            self.embeddings = np.load(self.emb_path)

    def _save(self) -> None:
        if self.index is None:
            return
        faiss.write_index(self.index, str(self.index_path))
        self.meta_path.write_text(json.dumps(self.metadata, ensure_ascii=False, indent=2))
        if self.embeddings is not None:
            np.save(self.emb_path, self.embeddings)

    def reset(self) -> None:
        self.index = None
        self.metadata = []
        self.embeddings = None
        for p in (self.index_path, self.meta_path, self.emb_path):
            if p.exists():
                p.unlink()

    def add(self, vectors: np.ndarray, metas: list[dict]) -> None:
        if len(vectors) == 0:
            return
        dim = vectors.shape[1]
        if self.index is None:
            self.index = faiss.IndexFlatIP(dim)
            self.embeddings = vectors.copy()
        else:
            assert self.index.d == dim, "Embedding dimension mismatch"
            assert self.embeddings is not None
            self.embeddings = np.vstack([self.embeddings, vectors])

        self.index.add(vectors)
        self.metadata.extend(metas)
        self._save()

    def search(self, query_vector: np.ndarray, k: int) -> list[dict]:
        if self.index is None or len(self.metadata) == 0:
            return []

        k = min(k, len(self.metadata))
        distances, indices = self.index.search(query_vector.reshape(1, -1), k)

        results = []
        for score, idx in zip(distances[0], indices[0]):
            if idx < 0:
                continue
            row = self.metadata[idx].copy()
            row["score"] = float(score)
            results.append(row)
        return results
