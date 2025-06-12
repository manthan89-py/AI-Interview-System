# Use the official Python 3.11 image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y portaudio19-dev

# Set the working directory
WORKDIR /app

# Copy application files
COPY . /app

# Copy the .env file
COPY .env .env

# Install pip and uv
RUN pip install --no-cache-dir uv

# install dependencies
RUN uv pip install --requirement pyproject.toml --system

# Expose the Streamlit port
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "app.py"]