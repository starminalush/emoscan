FROM python:3.10
ENV TZ=UTC
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["streamlit","run", "main.py", "--server.port", "8080"]
