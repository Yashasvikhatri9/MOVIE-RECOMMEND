# Use official slim Python 3.11 image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and models
COPY . .

# Ensure models are in /app/models
# Example: vector.joblib, svd_model.joblib inside /app/models

# Expose the port your app runs on
EXPOSE 8080

# Command to run the app using gunicorn
# -w 2 uses 2 workers, adjust for your app load
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8080", "recommend_model:app"]
