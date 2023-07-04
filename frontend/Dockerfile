FROM python:3.10@sha256:a8462db480ec3a74499a297b1f8e074944283407b7a417f22f20d8e2e1619782
ENV TZ=UTC
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app
CMD ["streamlit","run", "main.py", "--server.port", "8080"]
