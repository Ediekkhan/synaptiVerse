FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for agent storage
RUN mkdir -p /app/.uagents

# Expose ports for agents (if needed)
EXPOSE 8000 8001

# Default command (can be overridden in docker-compose)
CMD ["python", "src/agents/appointment_coordinator.py"]
