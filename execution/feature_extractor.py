import sys
import json
import os

try:
    import librosa
    import numpy as np
    import matplotlib.pyplot as plt
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False

def extract_features(audio_path, output_dir=".tmp/"):
    """
    Extrai MFCC e Espectrograma de Mel do áudio.
    """
    if not HAS_LIBS:
        return {"error": "Bibliotecas librosa/numpy não instaladas."}
        
    # Carrega áudio
    y, sr = librosa.load(audio_path)
    
    # Mel Spectrogram
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
    S_dB = librosa.power_to_db(S, ref=np.max)
    
    # MFCC
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    
    # Salva imagem do espectrograma para o dashboard
    spec_filename = os.path.basename(audio_path).split('.')[0] + "_spec.png"
    spec_path = os.path.join(output_dir, spec_filename)
    
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel-frequency spectrogram')
    plt.tight_layout()
    plt.savefig(spec_path)
    plt.close()
    
    return {
        "audio_info": {
            "duration": librosa.get_duration(y=y, sr=sr),
            "sample_rate": sr
        },
        "spectrogram_path": spec_path,
        "mfcc_shape": mfccs.shape
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python feature_extractor.py <audio_path>")
    else:
        print(json.dumps(extract_features(sys.argv[1]), indent=2))
