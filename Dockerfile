# Usa uma imagem base do Python
FROM python:3.9

# Instala o CMake
RUN apt-get update && apt-get install -y cmake

# Define o diretório de trabalho como /app
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos restantes para o diretório de trabalho
COPY app app

# Expõe a porta 8080 (ou a porta que você desejar)
EXPOSE 8080

# Define o comando para iniciar o aplicativo
CMD ["python", "app/main.py"]
