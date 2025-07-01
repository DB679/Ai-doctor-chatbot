# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy all files in your repo into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the default Gradio port
EXPOSE 7860

# Run the app
CMD ["python", "gradio_app.py"]
