FROM python:3

# Make directory
WORKDIR /app

# Copy source code
COPY ./ /

# Install dependencies
RUN pip install -r requirements.txt

# Set Python path to docker workdir
ENV PYTHONPATH /app

# Run application
CMD ["python", "bot.py"]