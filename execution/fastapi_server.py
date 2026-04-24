import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Importamos nossos módulos de execução
from feature_extractor import extract_features
from inference_wav2vec import run_inference

app = FastAPI(title="ConfereAI Audio Fraud Detection API")

# Configuração de CORS para permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisResult(BaseModel):
    filename: str
    fraud_score: float
    verdict: str
    confidence: float
    spectrogram_url: str

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_audio_endpoint(file: UploadFile = File(...)):
    # Garante diretório temporário
    temp_dir = ".tmp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        
    # Salva arquivo temporariamente
    file_path = os.path.join(temp_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # 1. Extração de Features
        features = extract_features(file_path, output_dir=temp_dir)
        
        # 2. Inferência de Deepfake
        inference = run_inference(file_path)
        
        # 3. Consolidação (Orquestração)
        return AnalysisResult(
            filename=file.filename,
            fraud_score=inference.get("deepfake_probability", 0.0),
            verdict=inference.get("prediction", "UNKNOWN"),
            confidence=inference.get("confidence", 0.0),
            spectrogram_url=features.get("spectrogram_path", "")
        )
    except Exception as e:
        print(f"Erro na análise: {e}")
        raise e

# Servir arquivos do dashboard e imagens temporárias
app.mount("/tmp", StaticFiles(directory=".tmp"), name="tmp")
app.mount("/", StaticFiles(directory="dashboard", html=True), name="dashboard")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
