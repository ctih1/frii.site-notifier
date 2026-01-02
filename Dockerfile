# Use the official Python image
FROM python:3.12-slim

# Set a working directory inside the container
WORKDIR /app

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app (including main.py)
COPY . .

# Set the default command to run your Python script
CMD ["python", "main.py"]