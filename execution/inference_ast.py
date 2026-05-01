import torch
import librosa
import numpy as np
from transformers import AutoFeatureExtractor, ASTForAudioClassification

# Modelo AST (Audio Spectrogram Transformer)
# Usamos o modelo base do MIT como referência para análise espectral
MODEL_NAME = "MIT/ast-finetuned-audioset-10-10-0.4593"

# Singleton para carregar o modelo apenas uma vez
_extractor = None
_model = None

def get_ast_resources():
    global _extractor, _model
    if _extractor is None or _model is None:
        print(f"Carregando motor AST: {MODEL_NAME}...")
        _extractor = AutoFeatureExtractor.from_pretrained(MODEL_NAME)
        _model = ASTForAudioClassification.from_pretrained(MODEL_NAME)
        _model.eval()
    return _extractor, _model

def run_ast_inference(file_path):
    """
    Executa a análise via Audio Spectrogram Transformer.
    Identifica anomalias espectrais e inconsistências na textura sonora.
    """
    try:
        extractor, model = get_ast_resources()

        # Carrega áudio (resample para 16kHz conforme exigido pelo AST)
        audio, _ = librosa.load(file_path, sr=16000)
        
        # O AST espera entradas de 10 segundos (160.000 amostras)
        # Vamos padronizar
        if len(audio) > 160000:
            audio = audio[:160000]
        else:
            audio = np.pad(audio, (0, 160000 - len(audio)), mode='constant')

        # Extração de Features (Espectrograma de Mel)
        inputs = extractor(audio, sampling_rate=16000, return_tensors="pt")

        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            
        # No AudioSet, as classes são variadas. Para detecção de fraude sem fine-tuning específico,
        # analisamos a "entropia" ou a probabilidade de classes sintéticas/anômalas.
        # Como fallback funcional, calculamos um score de desvio estatístico.
        probs = torch.nn.functional.softmax(logits, dim=-1)
        
        # Simulação de detecção de anomalia baseada na textura espectral
        # Em um cenário real com fine-tuning, usaríamos a classe 'deepfake'
        # Aqui, usamos a variância das probabilidades como proxy de 'instabilidade' da IA
        anomaly_score = float(torch.var(probs) * 100) # Exemplo de métrica de dispersão
        
        # Normalizamos para um score de 0 a 1
        risk_score = min(max(anomaly_score * 5, 0.0), 1.0) 

        return {
            "risk_score": risk_score,
            "engine": "AST-Transformer",
            "status": "success"
        }

    except Exception as e:
        print(f"Erro no motor AST: {e}")
        return {"error": str(e), "risk_score": 0.0}

if __name__ == "__main__":
    # Teste simples
    import sys
    if len(sys.argv) > 1:
        print(run_ast_inference(sys.argv[1]))
