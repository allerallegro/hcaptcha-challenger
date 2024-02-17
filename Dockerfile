FROM --platform=linux/amd64 python:3.11.0-slim-bullseye
WORKDIR /app
COPY application /app/application/
COPY backend /app/backend/
COPY hcaptcha_challenger /app/hcaptcha_challenger/
COPY infrastructure /app/infrastructure/
COPY models /app/models
COPY main.py /app/
COPY requirements.txt /app/requirements.txt
COPY exception /app/exception
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
RUN playwright install
RUN playwright install-deps
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl -f http://localhost:5000/healthcheck || exit 1
CMD python main.py