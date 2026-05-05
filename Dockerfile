# Use official Python image as base
# "slim" = lightweight version, no unnecessary packages
FROM python:3.9-slim

# Set the working directory inside the container
# All following commands run from here
WORKDIR /app

# Copy requirements first (before copying all code)
# This is a Docker optimization — if requirements don't change,
# Docker uses cached layer and skips reinstalling packages
COPY requirements.txt .

# Install all dependencies inside the container
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of your project code into the container
COPY . .

# Tell Docker your app listens on port 8080
EXPOSE 8080

# Command to start the app when container runs
# "0.0.0.0" means accept connections from outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]