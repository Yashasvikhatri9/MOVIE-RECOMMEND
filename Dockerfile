# Use official slim Python 3.11 image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Railway provides PORT as env variable
# Do NOT hardcode 8080
CMD gunicorn -w 1 -k sync -b 0.0.0.0:$PORT recommend_model:app