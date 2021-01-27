FROM python:3.8-slim

RUN apt-get update
RUN apt-get install -y gcc make git libffi-dev libssl-dev
RUN pip install "poetry>=1.0"

WORKDIR /app
COPY pyproject.toml .
COPY poetry.lock .

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction

COPY src .

ENV PYTHONUNBUFFERED 1
ARG PORT=8000
ENV PORT=$PORT

CMD ["python", "main.py"]
