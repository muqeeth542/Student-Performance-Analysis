# Full-Stack Local RAG + 3D Visualization

This repository now includes a complete Retrieval-Augmented Generation (RAG) application with:

- **FastAPI backend** (PDF ingestion, chunking, embeddings, FAISS persistence, retrieval, answer generation)
- **React + Vite frontend** with **React Three Fiber** 3D embedding graph
- **Local-first architecture** with **FAISS only** (no external vector DB)
- **LLM support** for **Ollama** or **OpenAI API**

---

## Project Structure

```text
backend/
  app/
    api/routes.py
    core/config.py
    models/schemas.py
    services/
      document_loader.py
      embeddings.py
      llm.py
      rag.py
      vector_store.py
    main.py
  requirements.txt

frontend/
  src/
    components/
      ChatPanel.jsx
      ThreeGraph.jsx
      UploadDropzone.jsx
    lib/api.js
    styles/app.css
    App.jsx
    main.jsx
  package.json
  vite.config.js
```

---

## Backend Features

- `POST /upload` uploads a PDF and indexes chunks.
- `POST /query` returns full answer + retrieved chunks.
- `POST /query/stream` streams answer tokens in real time (SSE).
- `POST /reset` clears FAISS index + metadata.
- `GET /graph` returns PCA-reduced 3D points for chunk embeddings.
- Persistent local storage in `backend/storage/`:
  - `faiss.index`
  - `metadata.json`
  - `embeddings.npy`

---

## Frontend Features

- Drag-and-drop PDF upload.
- Chat interface with streamed response rendering.
- Typing animation effect for generated answer.
- “AI is thinking...” loading animation.
- Optional voice input (Web Speech API).
- Interactive 3D graph:
  - zoom/rotate (Orbit controls)
  - node click to inspect chunk text
  - highlight top-k retrieved chunks

---

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm 9+
- (Optional for local LLM) [Ollama](https://ollama.com) running locally

---

## Run Backend (FastAPI)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Backend Environment Variables (optional)

Create `backend/.env`:

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.1:8b
OLLAMA_BASE_URL=http://localhost:11434

# For OpenAI usage:
# LLM_PROVIDER=openai
# OPENAI_API_KEY=your_key_here
# OPENAI_MODEL=gpt-4o-mini
```

---

## Run Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

Optional `.env` for frontend:

```env
VITE_API_URL=http://localhost:8000
```

Then open: `http://localhost:5173`

---

## API Quick Test

Upload:

```bash
curl -X POST http://localhost:8000/upload -F "file=@/path/to/file.pdf"
```

Query:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question":"Summarize key points", "top_k":5}'
```

Reset:

```bash
curl -X POST http://localhost:8000/reset
```

---

## Notes

- Embeddings use `sentence-transformers/all-MiniLM-L6-v2` by default.
- Similarity search is cosine-like via normalized embeddings + FAISS Inner Product index.
- Chunking is overlap-based for better context retention.
- The app is local-friendly and optimized for running with Ollama.
