# Set base image (host OS)
FROM --platform=linux/amd64 python:3.7

# By default, listen on port 8080
EXPOSE 8080/tcp

# Set the working directory in the container
WORKDIR /src

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY src .

# Specify the command to run on container start
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]