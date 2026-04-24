import os
import time
import requests
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Configuração de CORS para garantir funcionamento via browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurações do Hugging Face
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = "mo-thecreator/Deepfake-audio-detection"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

class AnalysisResult(BaseModel):
    filename: str
    fraud_score: float
    verdict: str
    spectrogram_url: str
    engine: str

@app.get("/api")
def read_root():
    return {"status": "ConfereAI Vercel API is online", "model": MODEL_ID}

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_audio(file: UploadFile = File(...)):
    if not HF_TOKEN:
        raise HTTPException(status_code=500, detail="HF_TOKEN not configured in Vercel environment.")

    # Lê o conteúdo do áudio enviado
    try:
        audio_content = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    # Chamada para a API do Hugging Face com lógica de retry (cold start)
    result = None
    for attempt in range(5):
        response = requests.post(API_URL, headers=headers, data=audio_content, timeout=35)
        
        if response.status_code == 200:
            result = response.json()
            break
        elif response.status_code == 503:
            # Modelo carregando
            wait_time = response.json().get("estimated_time", 20)
            time.sleep(min(wait_time, 15))
            continue
        else:
            raise HTTPException(status_code=response.status_code, detail=f"HF API Error: {response.text}")

    if not result:
         raise HTTPException(status_code=504, detail="Hugging Face API timeout or unavailable.")

    # Processamento do resultado (formato padrão do Hugging Face)
    try:
        # Encontra a probabilidade de ser 'fake'
        fake_score = 0.0
        for item in result:
            if item["label"].lower() in ["fake", "spoof", "fraud"]:
                fake_score = item["score"]
                break
        
        verdict = "FRAUD_DETECTED" if fake_score > 0.7 else "AUTHENTIC"
        
        # Como o Vercel não permite salvar arquivos permanentemente para gerar espectrograma local,
        # retornamos um placeholder ou uma URL de serviço externo se houvesse.
        # Aqui, mantemos o fluxo simples.
        return AnalysisResult(
            filename=file.filename,
            fraud_score=round(fake_score, 4),
            verdict=verdict,
            spectrogram_url="API_GENERATED", # Na Vercel usamos a análise puramente neural
            engine=f"Hugging Face: {MODEL_ID}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Result processing error: {str(e)}")
