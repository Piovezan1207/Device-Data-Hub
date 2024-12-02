# Use an official Python runtime as the base image
FROM python:3.10
# FROM 3.11.10-alpine3.20

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory (our Flask app) into the container at /app
COPY . /app

# Install Flask and other dependencies
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

# Run the command to start the Flask app
CMD [ "python", "-u", "mainMqtt.py" ]