@echo off
REM Build the Docker image
docker build -t ai-interview:main-latest .

REM Run the Docker container
docker run --env-file .env -p 8501:8501 ai-interview:main-latest