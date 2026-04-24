import os
import shutil
from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Importamos nossos módulos de execução
from execution.feature_extractor import extract_features
from execution.inference_wav2vec import run_inference

app = FastAPI(title="ConfereAI Audio Fraud Detection API")

# Configuração de CORS
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
    spectrogram_url: str
    engine: str

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
        # 1. Extração de Imagens (Local)
        features = extract_features(file_path, output_dir=temp_dir)
        
        # 2. Inferência Local (Sem depender de API externa!)
        # Usaremos o modelo "HyperMoon/wav2vec2-base-960h-finetuned-deepfake" que é super estável
        inference = run_inference(file_path)
        
        if "error" in inference:
            raise Exception(inference["error"])

        # 3. Resposta Consolidada
        return AnalysisResult(
            filename=file.filename,
            fraud_score=inference.get("deepfake_probability", 0.0),
            verdict=inference.get("verdict", "UNKNOWN"),
            spectrogram_url=features.get("spectrogram_path", ""),
            engine=inference.get("model", "Local Neural Engine")
        )
    except Exception as e:
        print(f"Erro na análise: {e}")
        raise e

# Garante diretório temporário para o mount não falhar
if not os.path.exists(".tmp"):
    os.makedirs(".tmp")

# Servir arquivos do dashboard e imagens temporárias (se existirem)
app.mount("/tmp", StaticFiles(directory=".tmp"), name="tmp")

if os.path.exists("public"):
    app.mount("/", StaticFiles(directory="public", html=True), name="public")
else:
    @app.get("/")
    async def root_fallback():
        return {"status": "ConfereAI API Running", "message": "Public directory not found. Please use the Vercel frontend."}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)
