FROM python:3.8-slim

WORKDIR /app
COPY pyproject.toml .
COPY poetry.lock .

RUN pip install 'poetry>=1.0' \
  && poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction \
  && pip uninstall --yes poetry \
  && rm -rf ~/.cache/pypoetry/cache/repositories/pypi/* \
  && rm -rf ~/.cache/pip

COPY src .

ENV PYTHONUNBUFFERED 1
ARG PORT=8000
ENV PORT=$PORT
CMD python main.py
