import os
import shutil
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException, Depends, Header, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import zipfile
import uuid
import uvicorn

# Carrega variáveis do arquivo .env
load_dotenv()

# Importamos nossos módulos de execução
from execution.feature_extractor import extract_features
from execution.ensemble_manager import get_combined_verdict

app = FastAPI(title="ConfereAI Audio Fraud Detection API")

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estado global do treinamento (simplificado para MVP)
training_status = {
    "status": "idle", # idle, processing, training, completed, failed
    "progress": 0,
    "message": "Aguardando",
    "error": None
}

# Verificador de token super simples
def verify_admin_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token ausente ou inválido")
    
    token = authorization.split(" ")[1]
    # No mundo real, usaríamos JWT decodificado
    if token != "confereai_admin_token_2026":
        raise HTTPException(status_code=401, detail="Token inválido")
    return token

class AnalysisResult(BaseModel):
    filename: str
    fraud_score: float
    verdict: str
    spectrogram_url: str
    engine: str
    wav2vec_score: float = 0.0
    ast_score: float = 0.0
    engines_consensus: str = ""
    temporal_scores: list = []

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_audio_endpoint(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # Garante diretório temporário
    temp_dir = ".tmp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        
    # Salva arquivo temporariamente com ID único para evitar colisões
    unique_id = str(uuid.uuid4())[:8]
    filename = f"{unique_id}_{file.filename}"
    file_path = os.path.join(temp_dir, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # 1. Extração de Imagens (Local)
        features = extract_features(file_path, output_dir=temp_dir)
        
        # 2. Inferência via Ensemble (Wav2Vec2 + AST)
        analysis = get_combined_verdict(file_path)
        
        # 3. Agenda limpeza em background (após 5 minutos para dar tempo do front ler a imagem)
        def cleanup_temp_files(paths):
            import time
            time.sleep(300) # 5 minutos
            for p in paths:
                if os.path.exists(p):
                    try:
                        os.remove(p)
                        print(f"Cleanup: {p} removido.")
                    except Exception as e:
                        print(f"Cleanup error: {e}")

        background_tasks.add_task(cleanup_temp_files, [file_path, features.get("spectrogram_path")])

        # 4. Resposta Consolidada
        return AnalysisResult(
            filename=file.filename,
            fraud_score=analysis.get("fraud_probability", 0.0),
            verdict=analysis.get("verdict", "UNKNOWN"),
            spectrogram_url=features.get("spectrogram_path", "").replace(".tmp/", "/tmp/"),
            engine="Dual Engine (Wav2Vec2 + AST) - Protocolo de Rigor",
            wav2vec_score=analysis.get("wav2vec_score", 0.0),
            ast_score=analysis.get("ast_score", 0.0),
            engines_consensus=analysis.get("engines_consensus", ""),
            temporal_scores=analysis.get("temporal_scores", [])
        )

    except Exception as e:
        print(f"Erro na análise: {e}")
        raise e

# --- ADMIN ENDPOINTS ---

class LoginRequest(BaseModel):
    password: str

@app.post("/admin/login")
async def admin_login(req: LoginRequest):
    admin_pw = os.environ.get("ADMIN_PASSWORD", "Casa102030@")
    if req.password == admin_pw:
        return {"token": "confereai_admin_token_2026"}
    raise HTTPException(status_code=401, detail="Senha incorreta")

@app.post("/admin/upload_dataset")
async def admin_upload(file: UploadFile = File(...), token: str = Depends(verify_admin_token)):
    global training_status
    if not file.filename.endswith(('.zip', '.rar')):
        raise HTTPException(status_code=400, detail="Apenas .zip ou .rar")
        
    dataset_dir = ".tmp/dataset"
    if os.path.exists(dataset_dir):
        shutil.rmtree(dataset_dir)
    os.makedirs(dataset_dir)
    
    file_path = os.path.join(".tmp", file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    training_status["status"] = "processing"
    training_status["progress"] = 10
    training_status["message"] = "Arquivo recebido. Extraindo..."
    
    try:
        # Extração
        if file.filename.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(dataset_dir)
        # RAR necessita do pacote rarfile, assumiremos ZIP para simplificar ou instruir o usuário.
        
        training_status["progress"] = 25
        training_status["message"] = "Dataset extraído. Aguardando início do treinamento."
        return {"status": "success", "message": "Upload concluído."}
    except Exception as e:
        training_status["status"] = "failed"
        training_status["message"] = "Erro na extração do dataset."
        training_status["error"] = str(e)
        raise HTTPException(status_code=500, detail=str(e))

from execution.train_wav2vec import start_finetuning

def real_training_task():
    """Tarefa em background que executa o fine-tuning real no dataset."""
    global training_status
    training_status["status"] = "training"
    training_status["progress"] = 35
    training_status["message"] = "Carregando modelo e dataset para treinamento..."
    
    try:
        dataset_dir = ".tmp/dataset"
        # Executa o fine-tuning
        start_finetuning(dataset_dir)
        
        training_status["progress"] = 100
        training_status["status"] = "completed"
        training_status["message"] = "Fine-Tuning concluído com sucesso! Modelo salvo localmente."
    except Exception as e:
        training_status["status"] = "failed"
        training_status["message"] = f"Erro no treinamento: {str(e)}"
        training_status["error"] = str(e)
        print(f"Treinamento falhou: {e}")

@app.post("/admin/train")
async def admin_train(background_tasks: BackgroundTasks, token: str = Depends(verify_admin_token)):
    global training_status
    if training_status["status"] == "training":
        raise HTTPException(status_code=400, detail="Treinamento já está em andamento.")
        
    training_status["progress"] = 30
    training_status["message"] = "Iniciando pipeline de treinamento..."
    background_tasks.add_task(real_training_task)
    return {"status": "success", "message": "Treinamento iniciado em background"}

@app.get("/admin/status")
async def admin_status(token: str = Depends(verify_admin_token)):
    return training_status

# Garante diretório temporário para o mount não falhar
if not os.path.exists(".tmp"):
    os.makedirs(".tmp")

# Servir arquivos do dashboard e imagens temporárias (se existirem)
app.mount("/tmp", StaticFiles(directory=".tmp"), name="tmp")

if os.path.exists("dashboard"):
    app.mount("/", StaticFiles(directory="dashboard", html=True), name="dashboard")
else:
    @app.get("/")
    async def root_fallback():
        return {"status": "ConfereAI API Running", "message": "Dashboard directory not found. Please use the Vercel frontend."}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)
