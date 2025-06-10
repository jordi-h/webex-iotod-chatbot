# Use Ubuntu 22.04 as the base image
FROM ubuntu:22.04

# Avoid prompts during apt operations
ARG DEBIAN_FRONTEND=noninteractive

# Install Python 3.7 and all required build dependencies
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && \
    apt-get install -y \
        python3.7 \
        python3-pip \
        python3.7-venv \
        python3.7-distutils \
        python3.7-dev \
        build-essential \
        curl \
        git \
        && python3.7 -m pip install --upgrade pip && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy application files to the container
COPY . /app

# Copy and make the wait-for-it script executable
COPY docker/wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Install Python dependencies
RUN python3.7 -m pip install --no-cache-dir -r requirements.txt

# Default command to run the app
CMD ["python3.7", "main.py"]
