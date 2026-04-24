FROM python:3.10-slim

# Instala dependências do sistema para o librosa
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia arquivos de requisitos primeiro para cache
COPY requirements-ml.txt .
RUN pip install --no-cache-dir -r requirements-ml.txt

# Copia o resto do código
COPY . .

# Garante que a pasta .tmp existe e tem permissão
RUN mkdir -p .tmp && chmod 777 .tmp

# Porta padrão do Railway
ENV PORT=8000
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["python", "execution/fastapi_server.py"]
