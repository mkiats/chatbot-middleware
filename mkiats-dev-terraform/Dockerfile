# Use official Python image as base
FROM python:3.11-slim

# Install system dependencies including Terraform
RUN apt-get update && apt-get install -y \
    curl \
    unzip

# Install Terraform
RUN curl -fsSL https://releases.hashicorp.com/terraform/1.7.3/terraform_1.7.3_linux_amd64.zip -o terraform.zip && \
    unzip terraform.zip && \
    mv terraform /usr/local/bin/ && \
    rm terraform.zip

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Set environment variables
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]