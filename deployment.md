# Deployment Guide

This document provides comprehensive instructions for deploying the English-Chinese Dictionary System to various environments.

## Table of Contents

1. [Production Environment Setup](#production-environment-setup)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Security Considerations](#security-considerations)
6. [Monitoring and Maintenance](#monitoring-and-maintenance)

## Production Environment Setup

### System Requirements

- **Operating System**: Linux (Ubuntu 20.04+ recommended)
- **Python**: 3.9 or higher
- **Memory**: Minimum 1GB RAM
- **Storage**: Minimum 5GB available space
- **Network**: Internet connection for Baidu Translation API

### Production Dependencies

Create a `requirements.txt` file:

```txt
Django==4.2.23
requests==2.32.4
gunicorn==21.2.0
whitenoise==6.6.0
```

### Environment Setup

1. **Create production user**
   ```bash
   sudo adduser dictionary
   sudo usermod -aG sudo dictionary
   su - dictionary
   ```

2. **Install system dependencies**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv nginx supervisor
   ```

3. **Create virtual environment**
   ```bash
   python3 -m venv /home/dictionary/venv
   source /home/dictionary/venv/bin/activate
   ```

4. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Production Settings

Create `dictionary_system/settings_production.py`:

```python
from .settings import *

# Security settings
DEBUG = False
SECRET_KEY = 'your-super-secret-production-key-here'
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com', 'localhost']

# Database settings (for production, consider PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files
STATIC_ROOT = '/home/dictionary/static/'
STATIC_URL = '/static/'

# Security headers
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Session security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/home/dictionary/logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### Gunicorn Configuration

Create `/home/dictionary/gunicorn_config.py`:

```python
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
user = "dictionary"
group = "dictionary"
daemon = False
pidfile = "/home/dictionary/gunicorn.pid"
errorlog = "/home/dictionary/logs/gunicorn_error.log"
accesslog = "/home/dictionary/logs/gunicorn_access.log"
loglevel = "info"
```

### Nginx Configuration

Create `/etc/nginx/sites-available/dictionary`:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;
    
    # SSL configuration (use Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # Static files
    location /static/ {
        alias /home/dictionary/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Main application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        proxy_read_timeout 300;
    }
    
    # Security
    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }
    
    location = /robots.txt { 
        access_log off; 
        log_not_found off; 
    }
}
```

### Supervisor Configuration

Create `/etc/supervisor/conf.d/dictionary.conf`:

```ini
[program:dictionary]
command=/home/dictionary/venv/bin/gunicorn --config /home/dictionary/gunicorn_config.py dictionary_system.wsgi:application
directory=/home/dictionary/dictionary_python
user=dictionary
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/dictionary/logs/supervisor.log
environment=DJANGO_SETTINGS_MODULE="dictionary_system.settings_production"
```

### Deployment Steps

1. **Create directories**
   ```bash
   mkdir -p /home/dictionary/logs
   mkdir -p /home/dictionary/static
   ```

2. **Deploy application**
   ```bash
   cd /home/dictionary
   git clone <your-repository> dictionary_python
   cd dictionary_python
   ```

3. **Set up database**
   ```bash
   source /home/dictionary/venv/bin/activate
   export DJANGO_SETTINGS_MODULE=dictionary_system.settings_production
   python manage.py migrate
   python manage.py collectstatic --noinput
   python initial_data.py
   ```

4. **Set permissions**
   ```bash
   chown -R dictionary:dictionary /home/dictionary
   chmod -R 755 /home/dictionary
   ```

5. **Enable services**
   ```bash
   sudo ln -s /etc/nginx/sites-available/dictionary /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   sudo supervisorctl reread
   sudo supervisorctl update
   sudo supervisorctl start dictionary
   ```

## Local Development

### Quick Start

1. **Activate environment**
   ```bash
   conda activate dictionary_env
   ```

2. **Start development server**
   ```bash
   python manage.py runserver 8085
   ```

3. **Access application**
   - Home: http://localhost:8085
   - Admin: http://localhost:8085/admin

### Development Settings

For development, use the default `settings.py` with:
- `DEBUG = True`
- SQLite database
- Default secret key (change in production)

## Docker Deployment

### Dockerfile

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations
RUN python manage.py migrate

# Create initial data
RUN python initial_data.py

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "dictionary_system.wsgi:application"]
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./db.sqlite3:/app/db.sqlite3
    environment:
      - DJANGO_SETTINGS_MODULE=dictionary_system.settings_production
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./static:/usr/share/nginx/html/static:ro
    depends_on:
      - web
    restart: unless-stopped
```

### Docker Commands

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild
docker-compose build --no-cache
```

## Cloud Deployment

### AWS EC2 Deployment

1. **Launch EC2 instance**
   - Ubuntu 20.04 LTS
   - t3.micro or larger
   - Security group: HTTP (80), HTTPS (443), SSH (22)

2. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx certbot python3-certbot-nginx
   ```

3. **Follow production setup steps**

4. **Configure SSL with Let's Encrypt**
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

### Heroku Deployment

1. **Create Heroku app**
   ```bash
   heroku create your-app-name
   ```

2. **Configure environment**
   ```bash
   heroku config:set DJANGO_SETTINGS_MODULE=dictionary_system.settings_production
   heroku config:set SECRET_KEY=your-secret-key
   ```

3. **Deploy**
   ```bash
   git push heroku main
   heroku run python manage.py migrate
   heroku run python initial_data.py
   ```

## Security Considerations

### Environment Variables

Create `.env` file (never commit to version control):

```env
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
BAIDU_APP_ID=20240531002066782
BAIDU_SECRET_KEY=2UYrEDwvtMgOShDLo3u8
```

### Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Set DEBUG=False in production
- [ ] Configure ALLOWED_HOSTS
- [ ] Use HTTPS in production
- [ ] Set up proper firewall rules
- [ ] Regular security updates
- [ ] Monitor logs for suspicious activity
- [ ] Use strong passwords for admin accounts
- [ ] Regular database backups

## Monitoring and Maintenance

### Log Management

1. **Django logs**: `/home/dictionary/logs/django.log`
2. **Gunicorn logs**: `/home/dictionary/logs/gunicorn_*.log`
3. **Nginx logs**: `/var/log/nginx/`
4. **Supervisor logs**: `/home/dictionary/logs/supervisor.log`

### Backup Strategy

```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/dictionary/backups"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
cp /home/dictionary/dictionary_python/db.sqlite3 $BACKUP_DIR/db_$DATE.sqlite3

# Backup logs
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz /home/dictionary/logs/

# Clean old backups (keep 7 days)
find $BACKUP_DIR -name "*.sqlite3" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

### Performance Monitoring

1. **Server resources**
   ```bash
   htop
   df -h
   free -h
   ```

2. **Application performance**
   ```bash
   sudo supervisorctl status
   sudo systemctl status nginx
   ```

3. **Database optimization**
   ```bash
   # SQLite optimization
   sqlite3 db.sqlite3 "VACUUM;"
   sqlite3 db.sqlite3 "ANALYZE;"
   ```

### Update Process

1. **Backup current version**
2. **Pull latest changes**
3. **Install new dependencies**
4. **Run migrations**
5. **Collect static files**
6. **Restart services**
7. **Verify deployment**

```bash
#!/bin/bash
# update.sh
cd /home/dictionary/dictionary_python
git pull origin main
source /home/dictionary/venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart dictionary
sudo systemctl reload nginx
```

## Troubleshooting

### Common Issues

1. **500 Internal Server Error**
   - Check Django logs
   - Verify database permissions
   - Ensure static files are collected

2. **Database Connection Error**
   - Check database file permissions
   - Verify database path in settings

3. **Translation API Issues**
   - Check internet connectivity
   - Verify API credentials
   - Check API quota limits

4. **Static Files Not Loading**
   - Run `collectstatic` command
   - Check nginx static file configuration
   - Verify file permissions

### Getting Help

1. Check application logs
2. Review Django documentation
3. Verify Baidu Translation API status
4. Check server resource usage
5. Review nginx/gunicorn configurations