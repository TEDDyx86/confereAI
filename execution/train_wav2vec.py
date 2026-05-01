import os
import torch
import librosa
from torch.utils.data import Dataset
from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2ForSequenceClassification, Trainer, TrainingArguments
from typing import Dict, List

# Define o modelo base usado pelo projeto
BASE_MODEL_NAME = "HyperMoon/wav2vec2-base-960h-finetuned-deepfake"
LOCAL_MODEL_DIR = "./local_finetuned_model"

def get_processor():
    """Retorna o extrator de características do modelo base (processador de áudio puro, sem tokenizador de texto)"""
    return Wav2Vec2FeatureExtractor.from_pretrained(BASE_MODEL_NAME)

class DeepfakeAudioDataset(Dataset):
    """
    Dataset Customizado do Pytorch para carregar áudios de Pastas.
    Espera-se que o diretório base tenha duas subpastas: 'real' e 'fake'.
    """
    def __init__(self, root_dir: str, processor: Wav2Vec2FeatureExtractor, max_length: int = 160000):
        self.root_dir = root_dir
        self.processor = processor
        self.max_length = max_length
        self.files: List[Dict] = []
        
        self._load_metadata()
        
    def _load_metadata(self):
        real_dir = os.path.join(self.root_dir, 'real')
        fake_dir = os.path.join(self.root_dir, 'fake')
        
        if os.path.exists(real_dir):
            for f in os.listdir(real_dir):
                if f.lower().endswith(('.wav', '.mp3', '.flac')):
                    self.files.append({"path": os.path.join(real_dir, f), "label": 0})
                    
        if os.path.exists(fake_dir):
            for f in os.listdir(fake_dir):
                if f.lower().endswith(('.wav', '.mp3', '.flac')):
                    self.files.append({"path": os.path.join(fake_dir, f), "label": 1})
                    
    def __len__(self):
        return len(self.files)
        
    def __getitem__(self, idx):
        item = self.files[idx]
        audio_path = item["path"]
        label = item["label"]
        
        # Load and resample audio to 16kHz
        speech, _ = librosa.load(audio_path, sr=16000)
        
        # Process audio to get input values
        input_values = self.processor(
            speech, 
            sampling_rate=16000, 
            return_tensors="pt", 
            padding="max_length", 
            max_length=self.max_length, 
            truncation=True
        ).input_values[0]
        
        return {
            "input_values": input_values,
            "labels": torch.tensor(label, dtype=torch.long)
        }

def start_finetuning(dataset_dir: str):
    """
    Inicia o treinamento congelando as camadas base para evitar OOM e focar apenas na cabeça de classificação.
    """
    processor = get_processor()
    
    # Prepara os datasets (simplificação: usando o mesmo para train e eval na V1)
    train_dataset = DeepfakeAudioDataset(dataset_dir, processor)
    
    if len(train_dataset) == 0:
        raise ValueError("Nenhum áudio encontrado no dataset.")
        
    # Carrega modelo e congela base
    model = Wav2Vec2ForSequenceClassification.from_pretrained(
        BASE_MODEL_NAME, 
        num_labels=2, 
        ignore_mismatched_sizes=True
    )
    
    # Freeze feature extractor e a base do transformer para poupar memória e tempo (Adaptação para hardwares fracos)
    if hasattr(model, 'freeze_feature_encoder'):
        model.freeze_feature_encoder()
    elif hasattr(model, 'freeze_feature_extractor'):
        model.freeze_feature_extractor()
        
    if hasattr(model, 'wav2vec2'):
        for param in model.wav2vec2.parameters():
            param.requires_grad = False
            
    # Training args voltados para hardware modesto
    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=5,
        per_device_train_batch_size=2, # Batch muito pequeno para não estourar memória
        gradient_accumulation_steps=4, # Acumula para dar efeito de batch=8
        learning_rate=2e-5,
        save_strategy="epoch",
        logging_dir="./logs",
        logging_steps=1,
        remove_unused_columns=False,
        report_to="none", # Evita erros de conexão com serviços externos de log
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=train_dataset, # Idealmente, devíamos fazer um split de 80/20
    )
    
    trainer.train()
    
    # Salva o modelo afinado
    model.save_pretrained(LOCAL_MODEL_DIR)
    processor.save_pretrained(LOCAL_MODEL_DIR)
    
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        start_finetuning(sys.argv[1])
