FROM python:3.10-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia arquivos de requisitos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código
COPY . .

# Garante que a pasta .tmp existe e tem permissão
RUN mkdir -p .tmp && chmod 777 .tmp

# Porta padrão do Hugging Face Spaces
ENV PORT=7860
EXPOSE 7860

# Comando para iniciar o servidor
CMD ["python", "main.py"]
