FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create log directory
RUN mkdir -p logs

# Run monitoring daemon
CMD ["python", "system-monitor.py", "--daemon"]