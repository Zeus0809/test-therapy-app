FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./
COPY python-version ./

# Install dependencies using uv sync
RUN uv sync

# Copy application code
COPY . .

# Create data directory for SQLite
RUN mkdir -p /data && chmod 777 /data

# Run the application
CMD ["python", "app.py"]
