# /Dockerfile  – FastAPI + FAISS + LangChain
FROM python:3.11-slim

# system libs for FAISS & PDFs
RUN apt-get update && apt-get install -y gcc libpoppler-cpp-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
ENV PORT=8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
