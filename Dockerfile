# Use official Python runtime as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for OCR and curl for healthcheck
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-fra \
    poppler-utils \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create Streamlit config to optimize startup
RUN mkdir -p ~/.streamlit && \
    echo "[server]" > ~/.streamlit/config.toml && \
    echo "port = 8501" >> ~/.streamlit/config.toml && \
    echo "address = \"0.0.0.0\"" >> ~/.streamlit/config.toml && \
    echo "headless = true" >> ~/.streamlit/config.toml && \
    echo "enableCORS = false" >> ~/.streamlit/config.toml && \
    echo "enableXsrfProtection = false" >> ~/.streamlit/config.toml && \
    echo "" >> ~/.streamlit/config.toml && \
    echo "[browser]" >> ~/.streamlit/config.toml && \
    echo "serverAddress = \"0.0.0.0\"" >> ~/.streamlit/config.toml && \
    echo "gatherUsageStats = false" >> ~/.streamlit/config.toml

# Expose Streamlit default port
EXPOSE 8501

# Health check for Render (checks if Streamlit is responding)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the application (simple command, config is in config.toml)
CMD ["streamlit", "run", "app.py"]
