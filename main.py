from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from services.ai_service import AIService
from typing import List, Dict, Optional
from dotenv import load_dotenv
import os

# .env dosyasını yükle
load_dotenv()

app = FastAPI()

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AI Servisini başlat
ai_service = AIService()

# Veri Modelleri
class AnalyzeRequest(BaseModel):
    text: Optional[str] = None
    image: Optional[str] = None 

class ChatRequest(BaseModel):
    message: str
    history: List[Dict]

@app.get("/")
def read_root():
    return {"message": "Asistan Doktor API Çalışıyor"}

@app.post("/api/analyze")
async def analyze_report(request: AnalyzeRequest):
    try:
        if not request.text and not request.image:
            raise HTTPException(status_code=400, detail="Lütfen metin girin veya resim yükleyin.")
            
        result = ai_service.analyze_report(request.text, request.image)
        return result
    except Exception as e:
        print(f"Hata detayı: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat_with_doctor(request: ChatRequest):
    try:
        response = ai_service.chat_with_doctor(request.message, request.history)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# CORS ayarları (Frontend'in bağlanabilmesi için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AI Servisini başlat
ai_service = AIService()

# --- GÜNCELLENEN KISIM: Veri Modelleri ---
class AnalyzeRequest(BaseModel):
    text: Optional[str] = None
    image: Optional[str] = None 

class ChatRequest(BaseModel):
    message: str
    history: List[Dict]

@app.get("/")
def read_root():
    return {"message": "Asistan Doktor API Çalışıyor"}

# --- EKSİK OLAN KISIM: Analiz Endpoint'i ---
@app.post("/api/analyze")
async def analyze_report(request: AnalyzeRequest):
    try:
        # Eğer ne metin ne de resim varsa hata ver
        if not request.text and not request.image:
            raise HTTPException(status_code=400, detail="Lütfen metin girin veya resim yükleyin.")
            
        # AI servisine gönder
        result = ai_service.analyze_report(request.text, request.image)
        return result
    except Exception as e:
        print(f"Hata detayı: {str(e)}") # Hatayı terminale yaz
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat_with_doctor(request: ChatRequest):
    try:
        response = ai_service.chat_with_doctor(request.message, request.history)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)