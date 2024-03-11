FROM python:3.8

WORKDIR /docker

COPY crypto_api/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY crypto_api/crypto_api.py .

CMD ["python3", "crypto_api.py"]
