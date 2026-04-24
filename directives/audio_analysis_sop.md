# SOP: Análise de Autenticidade de Áudio

## Objetivo
Padronizar o processo de verificação de arquivos de áudio para detecção de deepfakes e clonagem de voz.

## Procedimento

### 1. Preparação (Camada de Orquestração)
- Receber o arquivo de áudio.
- Validar formato (preferencialmente `.wav` ou `.flac` para preservar harmônicos).
- Criar identificador único para o job no diretório `.tmp/`.

### 2. Extração de Features (Camada de Execução)
- Rodar `execution/feature_extractor.py`.
- Extrair MFCCs e Espectrogramas de Mel usando `librosa`.
- Salvar imagens dos espectrogramas em `.tmp/` para visualização no dashboard.

### 3. Inferência de Deepfake (Camada de Execução)
- Rodar `execution/inference_wav2vec.py`.
- Utilizar modelo pré-treinado do Hugging Face (específico para Voice Spoofing).
- Analisar artefatos de compressão e padrões de rede neural.

### 4. Decisão (Camada de Orquestração)
- Consolidar scores das análises.
- Se Score > 0.8: Marcar como "Fraude Provável".
- Se 0.4 < Score < 0.8: Marcar como "Suspeito - Requer Análise Humana".
- Se Score < 0.4: Marcar como "Autêntico".

## Saída Esperada
Um arquivo JSON contendo:
- `timestamp`
- `verdict`
- `confidence_score`
- `analysis_details`
