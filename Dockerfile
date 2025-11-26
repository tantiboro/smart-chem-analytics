# Use the FULL Python image (not slim) to guarantee system libraries exist
FROM python:3.9

WORKDIR /app

# Install RDKit graphical dependencies
# We switch to the 'non-slim' image, but we still explicitly add X11/GL libs
RUN apt-get update && apt-get install -y \
    libxrender1 \
    libxext6 \
    libsm6 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Generate the synthetic data
RUN python generate_data.py

# Expose port
EXPOSE 8080

# Run
CMD ["streamlit", "run", "app/main.py", "--server.port=8080", "--server.address=0.0.0.0"]
