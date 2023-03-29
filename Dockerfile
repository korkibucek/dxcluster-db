# Use the official Python image as the base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install any required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY dxcluster_to_mongodb.py .

# Set the environment variables for MongoDB (replace with your own values)
ENV MONGODB_CONNECTION_STRING="mongodb+srv://<username>:<password>@cluster0.mongodb.net/myDatabase?retryWrites=true&w=majority"

# Run the Python script when the container is started
CMD ["python", "dxcluster_to_mongodb.py"]
