# Use a imagem base do OpenShift com suporte ao Python
FROM registry.access.redhat.com/ubi8/python-39

# Instale as dependências necessárias para compilar o dlib
RUN dnf install -y cmake gcc-c++ make git \
    && dnf clean all

# Defina o diretório de trabalho como /app
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copie os arquivos do projeto para o diretório de trabalho
COPY . .

# Defina as variáveis de ambiente necessárias para o OpenCV
ENV LD_LIBRARY_PATH=/usr/local/lib

# Execute o comando para iniciar o aplicativo
CMD ["python", "main.py"]
