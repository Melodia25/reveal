# base image
FROM python:3.10-slim as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV POETRY_VIRTUALENVS_CREATE false

RUN pip install --upgrade pip
# install poetry
RUN curl -sSL https://install.python-poetry.org | python - --version 1.4.2
ENV PATH="/root/.local/bin:$PATH"
RUN pip install poetry
RUN poetry self add poetry-plugin-export
RUN poetry --version

WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN poetry install
COPY . ./
EXPOSE 8000
CMD uvicorn main:app --host 0.0.0.0 --port 8000

