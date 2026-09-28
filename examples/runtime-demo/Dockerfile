FROM python:3.14.7-slim@sha256:51dafde81dbdb6ebde285137a295cf18a47ca95234fe388a343719cb97305b3d

WORKDIR /app

RUN pip install --no-cache-dir "opentelemetry-proto>=1.44.0"

COPY traffic_generator.py seed_frozen_evidence.py .

CMD ["python", "traffic_generator.py"]
