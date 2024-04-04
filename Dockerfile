# base image
FROM python:3.10

# working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs in (streamlit default port)
EXPOSE 8000

# Run app.py when the container launches
CMD ["streamlit", "run", "app.py"]
