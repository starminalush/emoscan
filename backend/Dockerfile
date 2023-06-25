FROM python:3.10-slim@sha256:7dc5b4e948acd18c1633b0e593ad0224298646612ce7d0b5ac6d4e17616d7e4b
ENV TZ=UTC
WORKDIR /app
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
COPY . /app
RUN pip install -U --no-cache-dir -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
