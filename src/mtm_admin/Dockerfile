# Use an official Python runtime as the base image
FROM python:3.9-slim

RUN apt-get update && apt-get upgrade -y

# Create a non-root user and group
RUN groupadd -r app_group 
RUN useradd -r -g app_group app_user

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .


# Install the Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port on which the web server will listen
EXPOSE 5000

# Set the ownership of the working directory to the non-root user
RUN chown -R app_user:app_group /app

# set up logs
# RUN mkdir -p /app/log
# RUN touch /app/log/app.log
# RUN chown -R app_user:app_group /app/log/app.log

# Switch to the non-root user
USER app_user

ENV FLASK_APP app.py

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=5000"]