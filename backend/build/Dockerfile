FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install -U --no-cache-dir -r requirements.txt
ENV PYTHONPATH=/app

CMD ["python", "main.py"]