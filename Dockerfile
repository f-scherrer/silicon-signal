FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY config/ ./config
COPY src/ ./src
COPY data/ ./data
ENV PYTHONUNBUFFERED=1
CMD ["python","-m","src.main","--pipeline","minimal"]
LABEL org.opencontainers.image.licenses="BUSL-1.1"
