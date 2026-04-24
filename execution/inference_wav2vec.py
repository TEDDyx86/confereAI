import sys
import json
import torch
import librosa
from transformers import AutoFeatureExtractor, AutoModelForAudioClassification

def run_inference(audio_path, model_name="HyperMoon/wav2vec2-base-960h-finetuned-deepfake"):
    """
    Realiza inferência real usando modelo do Hugging Face especializado em detecção de deepfake.
    """
    print(f"Rodando inferência REAL [{model_name}] em: {audio_path}", file=sys.stderr)
    
    try:
        # 1. Carrega extrator de características e modelo
        print("Lendo modelo...", file=sys.stderr)
        feature_extractor = AutoFeatureExtractor.from_pretrained(model_name)
        model = AutoModelForAudioClassification.from_pretrained(model_name)
        
        # 2. Carrega e pré-processa o áudio
        print(f"Lendo áudio: {audio_path}", file=sys.stderr)
        audio, sr = librosa.load(audio_path, sr=16000)
        print(f"Áudio carregado. Shape: {audio.shape}", file=sys.stderr)
        
        # 3. Prepara inputs
        inputs = feature_extractor(audio, sampling_rate=16000, return_tensors="pt", padding=True)
        
        # 3. Inferência
        with torch.no_grad():
            logits = model(**inputs).logits
            
        # 4. Processa resultados
        scores = torch.softmax(logits, dim=-1)
        # O modelo HyperMoon geralmente tem 2 classes: 0 (Fake/Spoof) e 1 (Real/Bonafide) 
        # ou vice-versa. Vamos checar o config id2label
        id2label = model.config.id2label
        
        prediction_idx = torch.argmax(scores, dim=-1).item()
        label = id2label[prediction_idx]
        confidence = scores[0][prediction_idx].item()
        
        # Normaliza para o nosso formato (precisamos saber quem é fraude)
        # Se o label contiver 'fake', 'spoof' ou 'fraud', é fraude.
        is_fraud = any(x in label.lower() for x in ['fake', 'spoof', 'fraud'])
        
        # Queremos o 'deepfake_probability'
        # Se o label 0 for fake, a probabilidade de deepfake é score[0][0]
        # Tentamos encontrar o índice do 'fake'
        fraud_idx = 0
        for idx, lbl in id2label.items():
            if any(x in lbl.lower() for x in ['fake', 'spoof', 'fraud']):
                fraud_idx = int(idx)  # Importante: converter para int
                break
        
        fraud_prob = scores[0][fraud_idx].item()
        
        results = {
            "model": model_name,
            "prediction": label.upper(),
            "confidence": confidence,
            "deepfake_probability": fraud_prob,
            "verdict": "SPOOF" if is_fraud else "BONAFIDE",
            "metadata": {
                "id2label": id2label,
                "all_scores": scores.tolist()
            }
        }
        
    except Exception as e:
        print(f"Erro na inferência: {e}")
        results = {
            "error": str(e),
            "verdict": "ERROR"
        }
    
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python inference_wav2vec.py <audio_path>")
    else:
        # Silenciamos warnings de transformers
        import warnings
        warnings.filterwarnings("ignore")
        print(json.dumps(run_inference(sys.argv[1])))
