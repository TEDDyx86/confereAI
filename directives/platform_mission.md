# ConfereAI: Plataforma de Identificação de Fraude por Áudio

## Missão
Proteger indivíduos e empresas contra fraudes de engenharia social baseadas em áudio (Deepfakes, vishing, clonagem de voz) através de análise inteligente e em tempo real.

## Arquitetura (Baseado em agente.md)
Este projeto segue a arquitetura de 3 camadas:

1. **Diretivas (`directives/`)**: Procedimentos Operacionais Padrão (SOPs) para análise de áudio, integração com APIs de IA e fluxos de automação.
2. **Orquestração**: Agente Antigravity gerenciando o fluxo de detecção.
3. **Execução (`execution/`)**: Scripts determinísticos para processamento de sinal de áudio, extração de características e chamadas de modelos de detecção de fraude.

## Tecnologias de Análise
1. **Processamento Digital de Sinal (DSP)**: Utilização de `librosa` para extração de MFCCs (Mel-Frequency Cepstral Coefficients) e Espectrogramas de Mel.
2. **Inteligência Artificial**:
    - Abordagem de Visão Computacional: CNNs (ResNet) aplicadas a espectrogramas.
    - Abordagem de Áudio Transformers: Wav2Vec 2.0 (Meta) via Hugging Face para inferência local de deepfakes.

## Fluxo de Trabalho de Detecção
1. **Entrada**: Upload via FastAPI (.wav/.mp3).
2. **Processamento (Execução)**: Conversão para Espectrogramas de Mel e normalização.
3. **Inferência (Execução)**: Aplicação do modelo Wav2Vec 2.0 focado em Voice Spoofing.
4. **Resultado**: JSON com `fraud_score` e `confidence_score`.

## Próximos Passos
- Definir o Design System (Onyx/Audio-themed).
- Implementar o Dashboard de monitoramento.
- Criar scripts de execução para análise preliminar de frequência.
