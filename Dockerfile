FROM orgoro/dlib-opencv-python 

WORKDIR /app

COPY . .

# Copia os arquivos restantes para o diretório de trabalho
COPY app /app

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
