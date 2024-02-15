FROM python:3.10

# Copy requirements and install dependencies
COPY ./requirements.txt /var/api/requirements.txt

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /var/api/requirements.txt

# Copy the rest of the application code
COPY . /
WORKDIR /var/api

# Specify the command to run your application
CMD ["python", "app.py"]