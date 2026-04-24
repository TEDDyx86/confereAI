import os
import sys
import json
import time
import requests
from dotenv import load_dotenv

# Carrega as chaves do .env
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
# Modelo especialista em detecção de áudio sintético (Wav2Vec2)
MODEL_ID = "mo-thecreator/Deepfake-audio-detection"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"

def analyze_audio(file_path):
    """
    Realiza a análise de áudio usando a API de Inferência do Hugging Face.
    """
    if not HF_TOKEN or "your_" in HF_TOKEN:
        return {
            "error": "HF_TOKEN não configurado. Adicione seu token no arquivo .env",
            "verdict": "CONFIG_ERROR"
        }

    if not os.path.exists(file_path):
        return {"error": f"Arquivo não encontrado: {file_path}"}

    print(f"Enviando {file_path} para análise no Hugging Face ({MODEL_ID})...")
    
    with open(file_path, "rb") as f:
        data = f.read()

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    # Tenta a chamada com retry caso o modelo esteja carregando
    for attempt in range(3):
        response = requests.post(API_URL, headers=headers, data=data)
        
        try:
            result = response.json()
        except requests.exceptions.JSONDecodeError:
            return {
                "error": "Resposta da API não é um JSON válido",
                "status_code": response.status_code,
                "response_text": response.text[:500]
            }
        
        if response.status_code == 200:
            break
        elif response.status_code == 503 or "loading" in str(result).lower():
            wait_time = result.get("estimated_time", 15) if isinstance(result, dict) else 15
            print(f"Modelo carregando (503)... Aguardando {wait_time}s (Tentativa {attempt+1}/3)")
            time.sleep(wait_time)
        else:
            return {"error": f"Erro na API ({response.status_code})", "result": result}

    # Processa os resultados
    # O modelo retorna algo como: [{"label": "fake", "score": 0.99}, {"label": "real", "score": 0.01}]
    try:
        # Pega o score de 'fake'
        fake_score = next(item["score"] for item in result if item["label"].lower() == "fake")
        
        verdict = "FRAUD_DETECTED" if fake_score > 0.7 else "AUTHENTIC"
        
        analysis = {
            "file": os.path.basename(file_path),
            "fraud_score": round(fake_score, 4),
            "artifacts_detected": fake_score > 0.5,
            "metadata_consistency": "Checked via Neural Analysis",
            "verdict": verdict,
            "raw_scores": result,
            "model_used": MODEL_ID
        }
        return analysis
    except (KeyError, StopIteration) as e:
        return {"error": f"Erro ao processar resposta do modelo: {str(e)}", "raw": result}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python analyze_audio.py <path_to_audio>")
        sys.exit(1)
        
    path = sys.argv[1]
    results = analyze_audio(path)
    print(json.dumps(results, indent=2))
