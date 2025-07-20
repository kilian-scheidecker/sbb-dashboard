FROM python:3.12-slim-bookworm

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Change the working directory
WORKDIR /app

# Copy uv files
COPY uv.lock .
COPY pyproject.toml .

# Install the venv with uv
RUN uv sync --no-cache

# Copy the application files
COPY src/ /app/src/

# Specify the config file directory
ENV DATA_TABLE_PATH="/app/src/config_files/data_table.toml"

# Run the api
CMD [ "uv", "run", "fastapi", "dev", "src/main.py", "--host", "0.0.0.0", "--port", "8080" ]