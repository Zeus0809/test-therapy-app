FROM python:3.11-slim

WORKDIR /app

# Copy requirements first (for better layer caching)
COPY requirements.txt .

# Install dependencies with standard pip
RUN pip install --no-cache-dir -r requirements.txt

# Create data directory for SQLite with proper permissions
RUN mkdir -p /data && chown -R nobody:nogroup /data && chmod 777 /data

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Run as non-root user for better security
USER nobody

# Expose the port
EXPOSE 8080

# Run the application
CMD ["python", "app.py"]