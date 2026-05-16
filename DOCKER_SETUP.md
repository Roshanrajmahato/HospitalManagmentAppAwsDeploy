# Docker Setup Guide - MediCare Hospital Management System

## Overview
This guide will help you set up the MediCare Hospital Management System using Docker with PostgreSQL database.

## Files Included
- **Dockerfile** - Container image for Django application
- **docker-compose.yml** - Orchestration for Django + PostgreSQL + Nginx
- **requirements.txt** - Python dependencies
- **nginx.conf** - Nginx reverse proxy configuration
- **.env.example** - Environment variables template
- **.dockerignore** - Files to exclude from Docker build

## Prerequisites
- Docker (v20.10+) installed
- Docker Compose (v2.0+) installed
- Git

## Setup Instructions

### 1. Clone or Download the Project
```bash
cd "d:\Roshan raj Mahato\Desktop\Data Analytics\DJANGO_RAHUL_SIR\HospitalManagmentApp"
```

### 2. Create Environment File
Copy `.env.example` to `.env` and update with your settings:
```bash
cp .env.example .env
```

Edit `.env` file:
```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DB_PASSWORD=your-secure-password
```

### 3. Update Django Settings
Edit `learning/settings.py` and update the DATABASES section:

**Replace:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**With:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.getenv('DB_NAME', 'healthcare_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'secure_password_123'),
        'HOST': os.getenv('DB_HOST', 'db'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

Also update ALLOWED_HOSTS:
```python
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key')
```

### 4. Build and Start Services
```bash
# Build images
docker-compose build
docker compose build --no-cache
# Start services in background
docker-compose up -d
docker compose down 
# View logs
docker-compose logs -f

# Wait for all services to be healthy (2-3 minutes)
```

### 5. Run Initial Commands
```bash
# Create superuser
docker-compose exec web python manage.py createsuperuser

# Or if migrations are not run
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --noinput
```

### 6. Access the Application
- **Application**: http://localhost:8000
- **Nginx Proxy**: http://localhost (port 80)
- **Admin Panel**: http://localhost:8000/admin

## Services

### PostgreSQL Database
- **Container Name**: hospital_db
- **Port**: 5432
- **Default Credentials**:
  - Username: postgres
  - Password: secure_password_123 (change in .env)
  - Database: healthcare_db

### Django Application
- **Container Name**: hospital_app
- **Port**: 8000
- **Volumes**: 
  - Static files: /app/staticfiles
  - Media files: /app/media
  - Database backups: /backups

### Nginx Reverse Proxy
- **Container Name**: hospital_nginx
- **Port**: 80
- **Serves**: Static files, media, and proxies to Django

## Useful Docker Commands

### View Running Services
```bash
docker-compose ps
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f nginx
```

### Access Database
```bash
docker-compose exec db psql -U postgres -d healthcare_db
```

### Run Management Commands
```bash
# Migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Shell
docker-compose exec web python manage.py shell

# Create backup
docker-compose exec db pg_dump -U postgres healthcare_db > backups/backup_$(date +%Y%m%d_%H%M%S).sql
```

### Stop Services
```bash
# Stop (containers remain)
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove everything (including volumes)
docker-compose down -v
```

### Restart Services
```bash
docker-compose restart

# Restart specific service
docker-compose restart web
```

### Rebuild After Changes
```bash
# Update requirements.txt, then:
docker-compose build --no-cache
docker-compose up -d
```

## Database Backup and Restore

### Backup Database
```bash
docker-compose exec db pg_dump -U postgres healthcare_db > backups/backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restore Database
```bash
docker-compose exec -T db psql -U postgres healthcare_db < backups/backup_filename.sql
```

## Troubleshooting

### Port Already in Use
If ports 8000, 5432, or 80 are already in use:
1. Update `.env` file:
```
APP_PORT=8001
DB_PORT=5433
NGINX_PORT=8080
```
2. Restart services: `docker-compose down && docker-compose up -d`

### Database Connection Error
```bash
# Check database logs
docker-compose logs db

# Verify database is healthy
docker-compose exec db pg_isready -U postgres
```

### Static Files Not Showing
```bash
# Rebuild static files
docker-compose exec web python manage.py collectstatic --noinput

# Check volumes
docker volume ls | grep hospital
```

### Permission Errors
```bash
# Fix permissions
docker-compose exec web chmod -R 755 /app/media
docker-compose exec web chown -R www-data:www-data /app/media
```

### Clear Everything and Start Fresh
```bash
docker-compose down -v
docker system prune -a
docker-compose build --no-cache
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## Production Deployment Notes

For production deployment:
1. Set `DEBUG=False` in `.env`
2. Use strong `SECRET_KEY`
3. Update `ALLOWED_HOSTS` with your domain
4. Set up SSL/HTTPS with Let's Encrypt
5. Use proper email backend configuration
6. Set up regular database backups
7. Use environment-specific settings
8. Configure logging and monitoring

## Additional Resources

- Django Documentation: https://docs.djangoproject.com/
- Docker Documentation: https://docs.docker.com/
- PostgreSQL Documentation: https://www.postgresql.org/docs/
- Docker Compose Documentation: https://docs.docker.com/compose/

## Support

For issues or questions, refer to the project README.md or contact the development team.
