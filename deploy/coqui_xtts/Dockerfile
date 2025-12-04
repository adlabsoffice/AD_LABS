FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
  git \
  build-essential \
  libsndfile1 \
  ffmpeg \
  && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir \
  TTS==0.22.0 \
  fastapi==0.109.0 \
  uvicorn[standard]==0.27.0 \
  pydantic==2.5.0 \
  python-multipart==0.0.6

# Set environment variable to accept TOS automatically
ENV COQUI_TOS_AGREED=1

# Note: Model will be downloaded on first API call (lazy loading)
# This avoids build timeouts and connection issues

# Copy API server
COPY api.py /app/api.py

# Create directory for reference voices
RUN mkdir -p /app/voices

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8080/health')"

# Run the API
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
