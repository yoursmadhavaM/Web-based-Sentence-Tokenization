# Dockerfile for Sentence Segmentation Tool
# Multi-stage build for optimized image size

FROM python:3.11-slim as base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy models
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download de_core_news_sm

# Optional: Download multilingual models (uncomment if needed)
# RUN python -m spacy download fr_core_news_sm
# RUN python -m spacy download es_core_news_sm

# Copy application code
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY evaluation/ ./evaluation/

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
