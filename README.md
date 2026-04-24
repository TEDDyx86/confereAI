---
title: ConfereAI - Audio Fraud Detection
emoji: 🛡️
colorFrom: purple
colorTo: indigo
sdk: docker
app_port: 7860
pinned: true
---

# 🛡️ CONFEREAI 
### *Verdade na voz, integridade no som.*

O **ConfereAI** é uma plataforma de segurança cibernética de última geração projetada para identificar e neutralizar fraudes de áudio, deepfakes e vozes clonadas via Inteligência Artificial. Utilizando uma arquitetura de redes neurais profundas, o sistema analisa micro-imperfeições acústicas imperceptíveis ao ouvido humano.

![ConfereAI Dashboard](dashboard/assets/logo.png)

## 🚀 Diferenciais Tecnológicos

- **🧠 Motor Neural Local**: Diferente de soluções que dependem de APIs instáveis, o ConfereAI utiliza um motor dedicado baseado em **Wav2Vec 2.0** (HyperMoon) rodando localmente no servidor.
- **📊 Evidência Espectral**: Gera espectrogramas de Mel em tempo real, permitindo uma análise forense visual das frequências de áudio.
- **⚡ Resposta Instantânea**: Análise completa em segundos, ideal para validação de identidade e prevenção de fraudes em tempo real.
- **💎 Interface Onyx**: Dashboard premium com Estética Onyx e Glassmorphism, focado em clareza e experiência do usuário (UX).

## 🛠️ Arquitetura de Software

O sistema é dividido em duas camadas principais:

1. **Backend (Python/FastAPI)**: 
   - Gerenciamento de arquivos e processamento paralelo.
   - Extração de características com `Librosa`.
   - Inferência neural via `PyTorch` e `Transformers`.
2. **Frontend (Vanilla JS/CSS)**:
   - Interface ultra-responsiva sem dependências pesadas.
   - Visualização dinâmica de resultados e medidores de confiança neon.

## 🔬 O Coração da IA: HyperMoon Engine

Utilizamos o modelo **HyperMoon/wav2vec2-base-960h-finetuned-deepfake**, treinado com o dataset acadêmico **ASVspoof**. 
- **Foco**: Detecção de descontinuidades rítmicas e artefatos de compressão típicos de IAs generativas.
- **Veredito**: Entrega um score de probabilidade (0% a 100%) e um veredito direto: **AUTÊNTICO** ou **FRAUDE DETECTADA**.

## 📦 Como Rodar o Projeto

### Localmente (Docker)
```bash
docker build -t confereai .
docker run -p 7860:7860 confereai
```

### Deploy no Hugging Face Spaces
1. Crie um novo **Space** no Hugging Face.
2. Selecione o SDK: **Docker**.
3. Faça o push deste repositório.
4. O sistema irá buildar e servir automaticamente na porta 7860.

---
**CONFEREAI** - *Protegendo a integridade da comunicação humana na era da IA.*
