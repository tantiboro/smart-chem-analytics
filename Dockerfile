FROM python:3.9-slim

WORKDIR /app

# Install system tools needed for some scientific packages
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Generate the synthetic data during the build process
RUN python generate_data.py

# Expose the port Streamlit runs on
EXPOSE 8080

# Run the app
CMD ["streamlit", "run", "app/main.py", "--server.port=8080", "--server.address=0.0.0.0"]
