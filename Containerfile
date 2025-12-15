FROM python:3.13-slim

WORKDIR /video-vault

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY README.md LICENSE pyproject.toml uv.lock ./

RUN useradd -m -u 1000 appuser

RUN chown -R appuser:appuser .

USER appuser

COPY --chown=appuser:appuser video_vault video_vault

RUN uv sync --no-group dev

RUN rm README.md LICENSE pyproject.toml uv.lock

ENTRYPOINT ["uv", "run", "video_vault"]

CMD ["main"]