# 🛡️ ConfereAI - Detecção de Fraude por Áudio

![ConfereAI Dashboard](https://img.shields.io/badge/Status-Beta-purple?style=for-the-badge)
![AI Model](https://img.shields.io/badge/Engine-Wav2Vec_2.0-cyan?style=for-the-badge)
![Deployment](https://img.shields.io/badge/Hugging_Face-Spaces-yellow?style=for-the-badge)

**ConfereAI** é uma plataforma forense de alta fidelidade projetada para identificar fraudes, deepfakes e vozes clonadas por Inteligência Artificial. Utilizando análise espectral fractal e redes neurais avançadas, o sistema oferece um veredito preciso sobre a autenticidade de qualquer arquivo de voz.

## ✨ Funcionalidades Principais

*   **Identificação de Deepfakes**: Análise neural para detectar marcas d'água sintéticas e artefatos de IA.
*   **Espectrograma de Mel**: Visualização forense da "impressão digital" vocal para identificar descontinuidades rítmicas.
*   **Design Glassmorphism**: Interface premium ultra-moderna com efeitos de Aurora Mesh.
*   **Processamento Ephimeral**: Máxima privacidade - arquivos são processados e descartados instantaneamente.
*   **Integração com Hugging Face**: Conexão direta com modelos de última geração via Inference API.

## 🚀 Arquitetura DOE

O projeto segue a arquitetura **Directive-Orchestration-Execution**:
1.  **Directives**: Procedimentos operacionais padrão em Markdown.
2.  **Orchestration**: Tomada de decisão inteligente baseada em IA.
3.  **Execution**: Scripts Python robustos e determinísticos (`execution/`).

## 🛠️ Instalação e Setup

1.  **Clone o repositório**:
    ```bash
    git clone https://huggingface.co/spaces/TEDDyx86/confereai
    cd confereai
    ```

2.  **Configure o Ambiente**:
    Execute o script de automação (Windows):
    ```powershell
    .\setup_env.ps1
    ```

3.  **Variáveis de Ambiente**:
    Crie um arquivo `.env` baseado no `.env.example` e adicione seu `HF_TOKEN`:
    ```env
    HF_TOKEN=seu_token_aqui
    ```

4.  **Inicie o Servidor**:
    ```powershell
    .\venv\Scripts\python.exe .\execution\fastapi_server.py
    ```
    O dashboard estará disponível em `http://localhost:8000`.

## 🧠 Modelos Utilizados

O motor primário utiliza o modelo [mo-thecreator/Deepfake-audio-detection](https://huggingface.co/mo-thecreator/Deepfake-audio-detection), refinado para detecção de áudio sintético com alta precisão.

## 📜 Licença

Propriedade de TEDDyx86. Desenvolvido para proteção da integridade vocal humana na era das deepfakes.
