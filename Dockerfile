FROM python:3.12-slim

# Due to some issues with python:3.12-slim regarding security vulnerabilities,
# using dhi.io/python:3.12-debian13-sfw-ent-dev

# If you haven't authenticated yet, first run in your terminal:
    # docker login dhi.io
# FROM dhi.io/python:3.12-debian13-sfw-ent-dev

# Install system dependencies for psycopg and update all packages to latest security patches
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    libpq-dev gcc apt-utils \
    # postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set timezone to Asia/Kolkata
ENV TZ=Asia/Kolkata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create and set the working directory.
WORKDIR /usr/src/app

# Copy the application requirements into the container.
COPY pyproject.toml uv.lock ./

# Install the application dependencies.
RUN uv sync --frozen --no-cache

# Copy the application into the container.
COPY . /usr/src/app

# Copy the favicon
# COPY ./app/static/favicon.ico /usr/src/app/app/static/favicon.ico

# Run the application.

# For development use uvicorn
CMD ["uv", "run", "uvicorn", "app.main:app", "--port", "9000", "--host", "0.0.0.0"]

# For production use gunicorn with uvicorn workers
# CMD ["uv", "run", "gunicorn", "app.main:app", "--bind", "0.0.0.0:9000", "--worker-class", "uvicorn.workers.UvicornWorker"]

# Run the application with gunicorn for production
# COPY entrypoint.sh /usr/src/entrypoint.sh
# RUN chmod +x /usr/src/entrypoint.sh
# ENTRYPOINT ["/usr/src/entrypoint.sh"]
