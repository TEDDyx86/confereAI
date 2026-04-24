import sys
import json

def extract_metadata(file_path):
    """
    Extrai metadados básicos de um arquivo de áudio.
    """
    # Mock de extração
    metadata = {
        "format": "WAV",
        "sample_rate": 44100,
        "channels": 2,
        "duration_seconds": 12.5,
        "encoder": "Lavf60.3.100",
        "creation_time": "2026-04-23 19:40:00"
    }
    return metadata

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python metadata_extractor.py <path_to_audio>")
        sys.exit(1)
        
    path = sys.argv[1]
    meta = extract_metadata(path)
    print(json.dumps(meta, indent=2))
