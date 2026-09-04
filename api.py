from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from cevap import soru_sor
from arama import en_yakin_parcalari_bul

app = FastAPI()

# Frontend'in (farklı porttan) istek atabilmesi için
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # geliştirme aşamasında tümüne izin, ileride kısıtlanabilir
    allow_methods=["*"],
    allow_headers=["*"],
)

class SoruIstegi(BaseModel):
    soru: str
    limit: int = 5

@app.get("/")
def anasayfa():
    return {"mesaj": "Yargıtay RAG API çalışıyor"}

@app.post("/sor")
def sor(istek: SoruIstegi):
    """Soruyu alır, cevap + kaynak kararları döndürür."""
    return soru_sor(istek.soru, limit=istek.limit)

@app.post("/ara")
def ara(istek: SoruIstegi):
    """Modelsiz test endpoint'i - sadece bulunan parçaları döndürür."""
    parcalar = en_yakin_parcalari_bul(istek.soru, limit=istek.limit)
    return {"soru": istek.soru, "parcalar": parcalar}