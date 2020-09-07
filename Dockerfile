FROM python:3

# Make directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY ./ .

# Set Python path to docker workdir
ENV PYTHONPATH /app

# Run application
CMD ["python", "./bot.py"]