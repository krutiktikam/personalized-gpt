# Use official Python 3.13-slim image for a smaller footprint
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HF_HOME /app/models/hf_cache
ENV PYTHONPATH /app

# Set work directory
WORKDIR /app

# Install system dependencies (for potential C++ builds in packages like transformers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create directories for logs, data, and models
RUN mkdir -p logs data models/hf_cache

# Expose the API port
EXPOSE 8000

# Command to run the application
CMD ["python", "-m", "src.api.app"]
