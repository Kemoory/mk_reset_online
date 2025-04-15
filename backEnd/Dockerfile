# Use the official Python image as the base image
FROM python:3.9-slim-bullseye

# Set the working directory in the container
WORKDIR /backEnd

# Copy the requirements file and install dependencies
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Copy the application code into the container
COPY backend.py .
COPY config.py .

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD ["python", "backend.py"]