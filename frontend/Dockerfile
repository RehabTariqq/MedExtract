FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    tesseract-ocr poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN python3 -c "import tiktoken; tiktoken.get_encoding('cl100k_base')"

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]