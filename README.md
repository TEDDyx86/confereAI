<div align="center">

# 🛡️ CONFEREAI
### **Neural Audio Forensic Engine**
*Identificação Cirúrgica de Clonagem de Voz*

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/TEDDyx86/confereai-dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?style=flat&logo=python)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

[**Dashboard Online**](https://huggingface.co/spaces/TEDDyx86/confereai-dev) | [**Notebook de Treino**](ConfereAI_FastTrain_Colab.ipynb) | [**Documentação API**](#api)

</div>

## 📖 O Projeto

O **ConfereAI** é uma plataforma de segurança cibernética de alta performance projetada para identificar fraudes de áudio com precisão forense. Utilizando o **Protocolo de Rigor V3**, o sistema combina múltiplos motores neurais para detectar micro-imperfeições acústicas e descontinuidades rítmicas imperceptíveis ao ouvido humano.

---

## 💎 Diferenciais Estratégicos (V2.4)

| Recurso | Descrição |
| :--- | :--- |
| **🧠 Dual-Engine** | Orquestração entre **HyperMoon (Wav2Vec2)** e **AST (Spectrogram Transformer)**. |
| **🛡️ Rigor V3** | Lógica de decisão Bayesiana que prioriza a soberania do modelo local treinado. |
| **📊 XAI (Explainable AI)** | Mapa de Calor Temporal que indica exatamente onde a IA detectou a anomalia. |
| **⚡ Turbo Inference** | Quantização Dinâmica (FP16) para análises ultra-rápidas em CPU. |
| **🎨 Onyx Interface** | Dashboard Premium com estética Glassmorphism e UX focada em forense. |

---

## 🔬 Arquitetura dos Motores

### 1. 🟣 HyperMoon Engine (O Comandante)
Baseado em **Wav2Vec 2.0**, este motor foca na **textura da voz**. Ele identifica artefatos de compressão e variações na prosódia que denunciam vozes sintéticas. É o motor principal que recebe o ajuste fino (Fine-Tuning) via Google Colab.

### 2. 🔵 AST Spectrogram Engine
Baseado em **Transformers de Visão para Áudio**, este motor analisa o **Espectrograma de Mel**. Ele busca por "ruídos fantasmas" e descontinuidades de frequência que são marcas registradas de vocoders de IA (como RVC ou ElevenLabs).

---

## 🚀 Workflow de Treinamento Híbrido

O ConfereAI permite que você aprimore a detecção com seus próprios dados:

1.  **Dataset**: Organize seus áudios em pastas `real` e `fake`.
2.  **Google Colab**: Use nosso [Notebook de Treino](ConfereAI_FastTrain_Colab.ipynb) para fine-tuning em GPU T4.
3.  **HF Model**: O modelo é enviado para um repositório de **Modelos** (LFS ilimitado).
4.  **Auto-Update**: O Space carrega o novo "cérebro" via variável `CUSTOM_MODEL_REPO`.

---

## 🛠️ Stack Tecnológica

- **Backend**: Python 3.10, FastAPI, Uvicorn
- **Inteligência**: PyTorch, Hugging Face Transformers, Librosa
- **Frontend**: Vanilla JavaScript (ES6+), CSS Aurora Mesh, Glassmorphism
- **DevOps**: Docker, Hugging Face Spaces SDK

---

CONFEREAI - Protegendo a integridade da comunicação humana na era da IA.

Desenvolvido com ❤️ por TEDDyx86
