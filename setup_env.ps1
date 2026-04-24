# setup_env.ps1
# Script para configurar o ambiente virtual e instalar dependências do ConfereAI

Write-Host "Iniciando configuração do ambiente ConfereAI..." -ForegroundColor Cyan

# Cria o ambiente virtual se não existir
if (-not (Test-Path "venv")) {
    Write-Host "Criando ambiente virtual (venv)..."
    python -m venv venv
}

# Ativa o ambiente virtual e instala dependências
Write-Host "Instalando dependências (librosa, transformers, torch, fastapi, uvicorn, matplotlib, python-multipart)..."
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install librosa transformers torch fastapi uvicorn matplotlib soundfile python-multipart requests python-dotenv

Write-Host "Configuração concluída com sucesso!" -ForegroundColor Green
