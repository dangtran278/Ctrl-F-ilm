from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel

app = FastAPI()
Instrumentator().instrument(app).expose(app)


class SearchResponse(BaseModel):
    query: str
    results: list[dict]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/search")
def search(query: str) -> SearchResponse:
    return SearchResponse(
        query=query,
        results=[
            {"clip_id": "stub-001", "timestamp": "00:04:32", "score": 0.91},
            {"clip_id": "stub-002", "timestamp": "00:12:10", "score": 0.85},
        ],
    )
