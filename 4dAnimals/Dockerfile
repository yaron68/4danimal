# Use an official lightweight Python image.
# alpine is chosen for its small size
FROM python:3-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY /4danimals /app

# Install any needed packages specified in requirements.txt
# Flask-SQLAlchemy will be used for SQLAlchemy support with Flask
# sqlite3 is included in Python, no need to install it separately
RUN pip install flask Flask-SQLAlchemy

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variable to store the database path
ENV DATABASE_PATH /data/4danimals.db

# Create a directory where the SQLite database will be stored
# This directory needs to be mounted as a volume from the host for persistence
VOLUME ["/data"]

# Define the command to run the app using `flask run`
# Assuming your Flask app is named `app.py` and is set to run on port 8080
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
