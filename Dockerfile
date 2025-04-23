FROM python:3.13-slim AS builder

WORKDIR /app

# Install system dependencies including C++ compiler and dev tools
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    ln -s $HOME/.local/bin/uv /usr/local/bin/uv

# Copy requirements file
COPY . .

WORKDIR /app

# Expose the server port
EXPOSE 10011

# Run the server
CMD ["uv", "run", "."]
