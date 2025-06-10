# Use a lightweight Python base image
FROM python:3.12-slim-bookworm

# Copy uv from the official uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
# WORKDIR /app

# # Install dependencies from uv.lock
# RUN --mount=type=cache,target=/root/.cache/uv \
#     --mount=type=bind,source=uv.lock,target=uv.lock \
#     --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
#     uv sync --locked --no-install-project

# Copy only necessary project files (controlled by .dockerignore)
COPY . /app

# Install the application dependencies.
WORKDIR /app
RUN uv sync --frozen --no-cache

# Command to be overridden in docker-compose.yml
CMD ["uv", "run", "python", "-u", "main.py"]