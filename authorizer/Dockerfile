# Use a smaller Python base image
FROM python:3.9

# Set working directory to /app
WORKDIR /app/

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code into the container
COPY main.py .

# Set environment variable
ENV JWT_SECRET=test

# Set the default command to run the app when the container starts
CMD ["python", "main.py"]