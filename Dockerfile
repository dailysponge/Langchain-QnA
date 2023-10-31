# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

# Install production dependencies.
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy local code to the container image.
COPY src/ app/
WORKDIR /app

ENV PORT 8080

# Run the web service on container startup. Here we use the gunicorn
# web server, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app