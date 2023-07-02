FROM python:3.10
ENV TZ=UTC
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app
CMD ["streamlit","run", "main.py", "--server.port", "8080"]
