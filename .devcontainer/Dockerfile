# syntax=docker/dockerfile:1

# Use the official VS Code Python devcontainer image as a base
ARG VARIANT=3.11-bullseye
FROM mcr.microsoft.com/devcontainers/python:${VARIANT}

# Install SQLite CLI (the Python standard library already includes the SQLite module)
RUN apt-get update \
    && apt-get install -y --no-install-recommends sqlite3 \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

# Upgrade pip (optional)
RUN python -m pip install --upgrade pip 