# Use official Python image from the Docker Hub
FROM python:3.9-slim

# Install necessary dependencies for Selenium and Chrome
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    ca-certificates \
    libx11-dev \
    libgl1-mesa-glx \
    libgtk-3-0 \
    libgbm-dev \
    fonts-liberation \
    libappindicator3-1 \
    libnss3 \
    lsb-release \
    xdg-utils \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN echo "deb [signed-by=/usr/share/keyrings/google-archive-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" | tee -a /etc/apt/sources.list.d/google-chrome.list
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | tee /usr/share/keyrings/google-archive-keyring.gpg
RUN apt-get update && apt-get install -y google-chrome-stable

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app will run on
EXPOSE 8085

# Command to run the application
CMD ["python", "dr_resilience_app.py"]
