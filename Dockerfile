# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app


# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the default Gradio port
EXPOSE 7860

# Start the Gradio app
CMD ["python", "gradio_app.py"]
