FROM python:3.9-slim

# Install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        bash \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install D2 CLI
RUN curl -fsSL https://d2lang.com/install.sh | bash

# Add D2 to PATH
ENV PATH="/root/bin:${PATH}"

# Set the working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Add this line to check the installed version of openai
RUN python -c "import openai; print('OpenAI library version:', openai.__version__)"

# Copy the application code
COPY . .

# Expose the port
EXPOSE 8080

# Start the application
CMD ["python", "app.py"]

