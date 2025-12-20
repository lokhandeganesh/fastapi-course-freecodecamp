FROM python:3.12-slim

# Install system dependencies for psycopg and update all packages to latest security patches
RUN apt-get update && apt-get upgrade -y && apt-get install -y libpq-dev gcc apt-utils && rm -rf /var/lib/apt/lists/*

# Set timezone to Asia/Kolkata
ENV TZ=Asia/Kolkata
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
# Copy the application into the container.
COPY . /usr/src/app

# Install the application dependencies.
WORKDIR /usr/src/app
RUN uv sync --frozen --no-cache


# Run the application.
CMD ["/usr/src/app/.venv/bin/uvicorn", "app.main:app", "--port", "8000", "--host", "0.0.0.0"]

# Run the application with gunicorn for production
# COPY entrypoint.sh /usr/src/entrypoint.sh
# RUN chmod +x /usr/src/entrypoint.sh
# ENTRYPOINT ["/usr/src/entrypoint.sh"]

# Copy the favicon
COPY ./app/static/favicon.ico /usr/src/app/app/static/favicon.ico