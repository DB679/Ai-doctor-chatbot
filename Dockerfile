# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app


# Set environment variables (if needed)
# ENV GROQ_API_KEY=your_key
# ENV ELEVENLABS_API_KEY=your_key

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r minproj/requirements.txt

# Expose port 8080 (Gradio's default)
EXPOSE 8080

# Start the app
CMD ["python", "minproj/gradio_app.py"]
