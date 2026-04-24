---
title: ConfereAI
emoji: 🛡️
colorFrom: indigo
colorTo: purple
sdk: docker
pinned: false
---

# 🛡️ ConfereAI - Audio Fraud Detection

ConfereAI é uma plataforma de segurança cibernética avançada projetada para identificar **Deepfakes** e **Clonagem de Voz** em tempo real. Utilizando redes neurais transformadoras (Wav2Vec 2.0), o sistema analisa artefatos acústicos invisíveis ao ouvido humano para distinguir voz real de fala sintetizada.

![ConfereAI Dashboard](dashboard/assets/preview.png)

## 🚀 Tecnologias

### Execução (Backend / ML)
- **FastAPI**: Servidor de alta performance.
- **Wav2Vec 2.0**: Modelo de Deep Learning para análise de representações latentes de áudio.
- **Librosa**: Processamento de sinal digital e extração de espectrogramas.
- **PyTorch & Transformers**: Engine de inferência.

### Interface (Frontend)
- **Glassmorphism Design**: Estética moderna com transparência e profundidade.
- **Vanilla JS & CSS**: UI rápida e leve, focada em performance.
- **Aurora Mesh**: Escopo visual dinâmico em segundo plano.

## 📁 Estrutura do Projeto

Conforme a arquitetura de **3 Camadas (Directive, Orchestration, Execution)**:

```text
├── directives/      # SOPs e Missão (Estratégia)
├── execution/       # Scripts determinísticos (Motor de IA)
│   ├── fastapi_server.py
│   ├── feature_extractor.py
│   └── inference_wav2vec.py
├── dashboard/       # Interface Web (Apresentação)
└── .tmp/            # Arquivos processados (Volátil)
```

## 🔧 Instalação e Uso Local

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Inicie o servidor:
   ```bash
   python execution/fastapi_server.py
   ```

3. Acesse no navegador: `http://localhost:8000`

## 🔒 Segurança e Privacidade
Os arquivos enviados são processados localmente ou em ambiente segregado e deletados após a análise (armazenamento volátil em `.tmp/`).

---
Desenvolvido por **ConfereAI Team**.
