# Use the official Python base image
FROM python:3.9-slim

# Set environment variable for NLTK data path
ENV NLTK_DATA /usr/share/nltk_data

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -m nltk.downloader -d /usr/share/nltk_data words

# Copy application code
COPY . /app
WORKDIR /app

# Command to run your application
CMD ["python", "main.py"]
