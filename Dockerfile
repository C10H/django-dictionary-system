FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Create directories
RUN mkdir -p /app/logs
RUN mkdir -p /app/staticfiles

# Set up Django settings for production
ENV DJANGO_SETTINGS_MODULE=dictionary_system.settings

# Configure static files
ENV STATIC_ROOT=/app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations
RUN python manage.py migrate

# Create initial data
RUN python initial_data.py

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "dictionary_system.wsgi:application"]