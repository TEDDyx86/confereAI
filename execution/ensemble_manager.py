from execution.inference_wav2vec import run_inference as run_wav2vec
from execution.inference_ast import run_ast_inference as run_ast

def get_combined_verdict(file_path):
    """
    Orquestra a execução dos dois motores e aplica o Protocolo de Rigor (Abordagem Conservadora).
    """
    # 1. Executa Motor 1 (Wav2Vec2 - Ritmo e Nuance)
    res_w2v = run_wav2vec(file_path)
    score_w2v = res_w2v.get("deepfake_probability", 0.0)
    
    # 2. Executa Motor 2 (AST - Espectrograma e Frequência)
    res_ast = run_ast(file_path)
    score_ast = res_ast.get("risk_score", 0.0)
    
    # 3. Lógica do Protocolo de Rigor (Abordagem Conservadora)
    # Se qualquer motor detectar fraude com convicção alta, o veredito é FRAUDE.
    
    HIGH_CONFIDENCE_THRESHOLD = 0.80
    
    is_fraud = False
    verdict = "AUTHENTIC"
    final_score = max(score_w2v, score_ast) # Pega o maior risco detectado
    
    if score_w2v >= HIGH_CONFIDENCE_THRESHOLD and score_ast >= HIGH_CONFIDENCE_THRESHOLD:
        is_fraud = True
        verdict = "SPOOF"
        message = "FRAUDE DETECTADA: Ambos os motores (Wav2Vec2 e AST) confirmam alta probabilidade de deepfake."
    elif score_w2v >= HIGH_CONFIDENCE_THRESHOLD:
        is_fraud = True
        verdict = "SPOOF"
        message = "FRAUDE DETECTADA: O Motor Wav2Vec2 (Nuances Rítmicas) identificou anomalias críticas."
    elif score_ast >= HIGH_CONFIDENCE_THRESHOLD:
        is_fraud = True
        verdict = "SPOOF"
        message = "FRAUDE DETECTADA: O Motor AST (Análise Espectral) detectou frequências sintéticas."
    elif final_score > 0.5:
        is_fraud = True
        verdict = "SPOOF"
        message = "FRAUDE PROVÁVEL: Consenso de risco moderado entre os motores."
    else:
        message = "ÁUDIO AUTÊNTICO: Ambos os motores concordam com baixo risco de manipulação."
        
    return {
        "verdict": verdict,
        "fraud_probability": final_score,
        "wav2vec_score": score_w2v,
        "ast_score": score_ast,
        "engines_consensus": message,
        "details": {
            "protocol": "Protocolo de Rigor (Conservador)"
        },
        "engines": ["Wav2Vec2-Deepfake", "AST-Spectrogram"]
    }
,
        "engines": ["Wav2Vec2-Deepfake", "AST-Spectrogram"]
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        import json
        print(json.dumps(get_combined_verdict(sys.argv[1]), indent=2))
