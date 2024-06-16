FROM python:3.11

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-dev

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "fastapi_user_management.app:app", "--host", "0.0.0.0", "--port", "8000"]


# https://hunj.dev/dockerize-python-fastapi-poetry/
