FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y gcc make git libffi-dev libssl-dev

ARG CRYPTOGRAPHY_DONT_BUILD_RUST=1

RUN pip install "poetry>=1.0"

WORKDIR /app
COPY pyproject.toml .
COPY poetry.lock .

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction

COPY src .
COPY docker/boot.sh .

ARG PORT=8000
ENV PORT=$PORT

ENTRYPOINT ["/app/boot.sh"]
CMD ["server"]
