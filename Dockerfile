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

###
#May be use this block if we want to install chirp
# RUN pip install poetry
# RUN pip install https://github.com/yoziru/jax/releases/download/jaxlib-v0.4.6/jaxlib-0.4.6-cp310-cp310-manylinux2014_aarch64.manylinux_2_17_aarch64.whl

# RUN git clone https://github.com/google-research/chirp.git chirpgit
# WORKDIR /app/chirpgit

# RUN poetry install

# WORKDIR /app
# RUN mv chirpgit/chirp /app/chirp/
###

RUN pip install https://github.com/google-research/chirp/archive/refs/heads/main.zip

# Copy the rest of the application code
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable for Uvicorn
ENV PORT=80

# Run the command to start Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
