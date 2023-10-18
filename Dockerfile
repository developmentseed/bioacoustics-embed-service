# Use an official Python base image
FROM python:3.10
RUN apt-get update && apt-get install -y wget curl libopenblas-dev git
RUN pip install --upgrade pip

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

RUN pip install https://github.com/google-research/chirp/archive/refs/heads/main.zip

# Download bird classifier model
RUN wget https://tfhub.dev/google/bird-vocalization-classifier/4?tf-hub-format=compressed -O bird-vocalization-classifier.tar.gz
RUN mkdir savedmodel
RUN tar -zxvf bird-vocalization-classifier.tar.gz -C savedmodel

# label.csv needs to be in the /app folder
RUN cp savedmodel/assets/label.csv .


# Copy the rest of the application code
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable for Uvicorn
ENV PORT=80

# Run the command to start Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
