# Stage 1: Build dependency requirements
FROM python:3.12-slim AS builder

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

# Export dependencies to a requirements.txt file
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Stage 2: Final runtime image
FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /tmp/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.layer_05_bootstrap.app_context_web:app", "--host", "0.0.0.0", "--port", "8000"]