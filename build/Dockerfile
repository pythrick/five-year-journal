ARG APP_NAME=five_year_journal
ARG APP_PATH=/opt/$APP_NAME
ARG PYTHON_VERSION=3.10.4
ARG POETRY_VERSION=1.1.13
ARG PORT=8000

FROM python:${PYTHON_VERSION}-slim as base
ARG APP_NAME
ARG APP_PATH
ARG POETRY_VERSION

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1
ENV \
    POETRY_VERSION=$POETRY_VERSION \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN apt update -y && apt install -y curl

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python
ENV PATH="$POETRY_HOME/bin:$PATH"

# Import our project files
WORKDIR $APP_PATH
COPY ./poetry.lock ./pyproject.toml ./


# Stage: development
FROM base as development
ARG APP_NAME
ARG APP_PATH
ARG PORT

ENV \
    APP_NAME=$APP_NAME \
    PORT=$PORT

WORKDIR $APP_PATH
RUN poetry install
COPY ./$APP_NAME ./$APP_NAME

COPY ./build/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD ["uvicorn", "${APP_NAME}.api:api", "--host=0.0.0.0", "--port=${PORT}", "--reload"]

# Stage: build
FROM base as build
ARG APP_PATH

WORKDIR $APP_PATH
COPY ./$APP_NAME ./$APP_NAME
RUN poetry build --format wheel
RUN poetry export --format requirements.txt --output constraints.txt --without-hashes

# Stage: production
FROM python:${PYTHON_VERSION}-slim as production
ARG APP_NAME
ARG APP_PATH
ARG PORT

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

ENV \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    APP_NAME=$APP_NAME \
    PORT=$PORT

# Get build artifact wheel and install it respecting dependency versions
WORKDIR $APP_PATH
COPY --from=build $APP_PATH/dist/*.whl ./
COPY --from=build $APP_PATH/constraints.txt ./
RUN pip install ./$APP_NAME*.whl --constraint constraints.txt

COPY ./build/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "${APP_NAME}.api:api", "--host=0.0.0.0","--port=${PORT}"]
