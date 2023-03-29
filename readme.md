# DXCluster to MongoDB

This project consists of two Docker containers. One container connects to a telnet DXCluster, reads the output, and stores it in a MongoDB database. The other container runs a MongoDB database server.

## Prerequisites

- Docker: Make sure you have Docker installed on your system. Visit [Docker's website](https://www.docker.com/) for installation instructions.

## MongoDB Container

1. Change to the MongoDB container directory:

cd path/to/mongodb-container


2. Build the MongoDB container image:

docker build -t my-mongodb .


3. Run the MongoDB container:

docker run -d --name mongodb -p 27017:27017 my-mongodb


This will start the MongoDB server within the container, which will be accessible on the host machine at port 27017. The database will be initialized with the user and password specified in the `mongo_init.js` file.

**Note**: Storing the password directly in the Dockerfile is not recommended for production environments. Consider using Docker secrets, environment variables, or other secret management tools to securely manage sensitive information in production.

## DXCluster to MongoDB Container

1. Change to the DXCluster to MongoDB container directory:

cd path/to/dxcluster-to-mongodb-container


2. Update the `MONGODB_CONNECTION_STRING` environment variable in the `Dockerfile` with the MongoDB username and password.

3. Build the DXCluster to MongoDB container image:

docker build -t dxcluster-to-mongodb .


4. Run the DXCluster to MongoDB container:

docker run -it --rm dxcluster-to-mongodb


This command will start the Docker container and run the Python script within it. The container will be removed when the script is terminated. The output from the DXCluster will be displayed in the terminal, and the parsed data will be stored in your MongoDB database.

**Note**: Replace the MongoDB connection string with the appropriate values for your MongoDB deployment.
