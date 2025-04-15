# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /frontEnd

# Copy the requirements file into the container
COPY requirement.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirement.txt

# Copy the application code into the container
COPY frontend.py .


# Expose the port the app runs on
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=frontend.py

# Command to run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]