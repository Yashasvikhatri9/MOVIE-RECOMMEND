# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy backend code
COPY Backend/ml/ ./Backend/ml/

# Set working directory to where Flask app lives
WORKDIR /app/Backend/ml

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port (Render will use $PORT)
EXPOSE 5000

# Start the app using gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "recommend_model:app"]
