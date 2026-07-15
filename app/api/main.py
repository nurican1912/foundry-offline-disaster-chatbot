"""API Layer (Modül F) — FastAPI ile /ask endpoint'i.

pipeline.answer(query, role) fonksiyonunu bir HTTP servisine sarar.
Çalıştırma:  uvicorn app.api.main:app --reload
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal

from app.config import settings
from app.data.database import log_query
from app.rag.pipeline import answer

app = FastAPI(title="Acil Durum RAG Asistanı")


# --- İstek gövdesi (request body) modeli ---
# İstemci POST /ask'e JSON gönderecek: {"query": "...", "role": "victim"}
# FastAPI bu JSON'u aşağıdaki modele göre otomatik doğrular.
class AskRequest(BaseModel):
    query: str
    role: Literal["victim", "rescuer"] = "victim"  # istemci göndermezse varsayılan victim


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


# --- Endpoint ---
@app.post("/ask")
def ask(req: AskRequest) -> dict:
    """Soruyu pipeline'a verir, paketi loglar ve yapılandırılmış JSON döner."""
    sonuc = answer(req.query, req.role)   # paket: {answer, sources, outcome, top_score}

    # 1) Soruyu query_log'a yaz (paketten alanları çekerek)
    log_query(
        settings.db_path, req.query, req.role,
        sonuc["outcome"], sonuc["top_score"], sonuc["answer"],
    )

    # 2) İstemciye yapılandırılmış JSON döndür (top_score iç bilgi, dışarı vermiyoruz)
    return {
        "answer": sonuc["answer"],
        "sources": sonuc["sources"],
        "outcome": sonuc["outcome"],
    }
