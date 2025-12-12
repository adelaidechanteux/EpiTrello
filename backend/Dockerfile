FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

RUN mkdir /app
WORKDIR /app
COPY ./pyproject.toml ./uv.lock /app
RUN uv sync --locked
COPY ./epitrello /app


FROM python:3.13-slim-trixie

RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

COPY --from=builder --chown=nonroot:nonroot /app /app

ENV PATH="/app/.venv/bin:$PATH"

USER nonroot

WORKDIR /app

EXPOSE 5081

CMD ["daphne", "-b", "0.0.0.0", "-p", "5081", "trellobackend.asgi:application"]
