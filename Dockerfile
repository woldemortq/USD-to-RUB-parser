FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl build-essential \
 && curl -LsSf https://astral.sh/uv/install.sh | sh \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml .
COPY . .

RUN uv pip install -r requirements.txt

RUN python manage.py migrate

CMD ["uv", "pip", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
