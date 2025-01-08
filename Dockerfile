# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Copy environment variables file
COPY /src/.env .

# Expose the port the application runs on
EXPOSE 5000

# Define the command to run the application
CMD ["python", "src/main/app.py"]