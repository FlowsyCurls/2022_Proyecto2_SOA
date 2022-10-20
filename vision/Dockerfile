# Specify the Parent Image from which we are building
FROM python:3.10

# Copy dependencies txt
COPY requirements.txt .

# Show python prints in kubernetes logs
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8

# Install dependencies or requirements
RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

# Copy current environment
COPY . .

# Set workspace
WORKDIR /app

# Copy app modules
COPY . /app

# Default executable of a Docker image
CMD ["python","-u", "main.py"]