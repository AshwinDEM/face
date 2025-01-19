# Use the official Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install system dependencies for Python and OpenCV
RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk2.0-dev \
    libboost-all-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    python3-dev && \
    apt-get clean

# Update pip to the latest version
RUN pip install --upgrade pip

# Install Python dependencies except dlib
RUN pip install --no-cache-dir -r requirements.txt
    # opencv-python==4.8.0.76 \
    # numpy==1.21.2 \
    # face-recognition==1.3.0

# Install the precompiled dlib wheel (if available)
# RUN pip install /app/dlib-19.23.0-cp39-cp39-win_amd64.whl || \
#     pip install dlib

# # Ensure required files are in the correct directory

# Define the default command to run the Python script
CMD ["python", "facial_recognition.py"]
