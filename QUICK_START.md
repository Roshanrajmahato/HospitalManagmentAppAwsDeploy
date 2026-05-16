# Quick Start Guide for Docker Setup

## 5 Simple Steps to Run Your App with Docker

### Step 1: Install Docker & Docker Compose
- Download from: https://www.docker.com/products/docker-desktop
- Verify installation:
  ```bash
  docker --version
  docker-compose --version
  ```

### Step 2: Setup Environment Variables
```bash
# In your project folder, create .env file (copy from .env.example)
cp .env.example .env

# Edit .env and set your database password:
# DB_PASSWORD=your_secure_password_123
```

### Step 3: Update Django Settings
Edit `learning/settings.py` and add these imports at the top:

```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
```

Then update DATABASES section (around line 101):

```python
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

Also update around line 32:
```python
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')
```

### Step 4: Build and Run
```bash
# Navigate to project folder
cd "HospitalManagmentApp"

# Build Docker images
docker-compose build

# Start all services
docker-compose up -d

# Wait 2-3 minutes for services to start
docker-compose ps
```

### Step 5: Create Admin User and Access
```bash
# Create superuser
docker-compose exec web python manage.py createsuperuser

# Open browser
# Application: http://localhost:8000
# Admin Panel: http://localhost:8000/admin
```

---

## What's Running?

| Service | Port | Purpose |
|---------|------|---------|
| Django App | 8000 | Your application |
| PostgreSQL | 5432 | Database (internal) |
| Nginx | 80 | Reverse proxy |

---

## Common Commands

```bash
# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f web
docker-compose logs -f db

# Stop all services
docker-compose stop

# Start services again
docker-compose start

# Stop and remove everything
docker-compose down

# Access database directly
docker-compose exec db psql -U postgres -d healthcare_db

# Run Django commands
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic
```

---

## Troubleshooting

**Port 8000 already in use?**
- Edit `.env` and change `APP_PORT=9000`
- Then access at http://localhost:9000

**Database connection error?**
```bash
# Check if database is running
docker-compose logs db

# Restart database
docker-compose restart db
```

**Static files not loading?**
```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Restart services
docker-compose restart
```

---

## File Structure After Setup
```
HospitalManagmentApp/
├── Dockerfile                 # Docker image instructions
├── docker-compose.yml        # Service orchestration
├── requirements.txt          # Python dependencies
├── nginx.conf               # Web server config
├── .env                     # Environment variables (DO NOT COMMIT)
├── .env.example             # Template for .env
├── .dockerignore            # Files to ignore in Docker
├── DOCKER_SETUP.md          # Full setup documentation
├── QUICK_START.md           # This file
├── learning/
│   ├── settings.py          # (Update this file - see Step 3)
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── ... (other Django files)
```

---

## Next Steps After First Run

1. **Add Your Static Files**
   - Place CSS, JS, Images in `static/` folder
   - Run: `docker-compose exec web python manage.py collectstatic --noinput`

2. **Upload Media Files**
   - Place in `media/` folder
   - Automatically served at `/media/` URL

3. **Monitor Logs**
   - Use `docker-compose logs -f` to watch activity
   - Check for errors and debug

4. **Backup Database**
   ```bash
   docker-compose exec db pg_dump -U postgres healthcare_db > backup.sql
   ```

---

## Production Checklist

Before deploying to production:
- [ ] Change DEBUG to False
- [ ] Use strong SECRET_KEY
- [ ] Update ALLOWED_HOSTS
- [ ] Set up SSL certificate
- [ ] Configure proper email backend
- [ ] Set up automated backups
- [ ] Configure logging
- [ ] Use environment-specific secrets

---

For more detailed information, see **DOCKER_SETUP.md** in the project folder.
