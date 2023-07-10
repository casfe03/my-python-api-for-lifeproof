FROM python:3.6.1

WORKDIR /app

RUN apt-get update -y && \
    apt-get install build-essential cmake pkg-config -y

RUN pip install dlib==19.9.0

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
