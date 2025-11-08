# 🚀 Guía de Despliegue - Puddle Marketplace

Guía completa para desplegar Puddle en diferentes plataformas.

---

## 📋 Tabla de Contenidos

- [Preparación Pre-Despliegue](#preparación-pre-despliegue)
- [PythonAnywhere](#pythonanywhere)
- [Heroku](#heroku)
- [DigitalOcean](#digitalocean)
- [AWS EC2](#aws-ec2)
- [Docker](#docker)
- [Configuración Post-Despliegue](#configuración-post-despliegue)
- [Troubleshooting](#troubleshooting)

---

## Preparación Pre-Despliegue

### Checklist de Seguridad

Antes de desplegar, asegúrate de:

- [ ] `DEBUG = False` en producción
- [ ] `SECRET_KEY` única y segura
- [ ] `ALLOWED_HOSTS` configurado correctamente
- [ ] Credenciales en variables de entorno
- [ ] `.env` en `.gitignore`
- [ ] HTTPS habilitado
- [ ] Base de datos con contraseña fuerte
- [ ] Backups configurados

### Configuración de Producción

Crea un archivo `puddle/settings_prod.py`:

```python
from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']

# Security Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
```

---

## PythonAnywhere

### Paso 1: Crear Cuenta

1. Registrarse en [PythonAnywhere](https://www.pythonanywhere.com)
2. Elegir plan (Beginner es gratuito)

### Paso 2: Subir Código

**Opción A: Git (Recomendado)**

```bash
# En PythonAnywhere Bash Console
cd ~
git clone https://github.com/tu-usuario/puddle.git
cd puddle
```

**Opción B: Upload Manual**

1. Comprimir proyecto localmente
2. Subir via Files → Upload
3. Descomprimir en consola

### Paso 3: Crear Virtual Environment

```bash
# En Bash Console
mkvirtualenv --python=/usr/bin/python3.10 puddle-env
pip install -r requirements.txt
```

### Paso 4: Configurar Base de Datos MySQL

1. Ir a **Databases** tab
2. Crear nueva base de datos MySQL
3. Anotar credenciales:
   - Host: `tu-usuario.mysql.pythonanywhere-services.com`
   - Database: `tu-usuario$puddle`
   - User: `tu-usuario`
   - Password: (la que configuraste)

### Paso 5: Configurar Variables de Entorno

**Opción A: Archivo .env**

```bash
# En Bash Console
cd ~/puddle
nano .env
```

Agregar:
```env
DB_NAME=tu-usuario$puddle
DB_USER=tu-usuario
DB_PASSWORD=tu_password_mysql
DB_HOST=tu-usuario.mysql.pythonanywhere-services.com
DB_PORT=3306

SECRET_KEY=tu-secret-key-generada
DEBUG=False
ALLOWED_HOSTS=tu-usuario.pythonanywhere.com

EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
```

**Opción B: WSGI File**

Editar `/var/www/tu-usuario_pythonanywhere_com_wsgi.py`:

```python
import os
import sys

# Agregar variables de entorno
os.environ['DB_NAME'] = 'tu-usuario$puddle'
os.environ['DB_USER'] = 'tu-usuario'
os.environ['DB_PASSWORD'] = 'tu_password'
# ... resto de variables

path = '/home/tu-usuario/puddle'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'puddle.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Paso 6: Ejecutar Migraciones

```bash
cd ~/puddle
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### Paso 7: Configurar Web App

1. Ir a **Web** tab
2. Click **Add a new web app**
3. Seleccionar **Manual configuration**
4. Python version: 3.10

**Configurar rutas**:
- Source code: `/home/tu-usuario/puddle`
- Working directory: `/home/tu-usuario/puddle`
- WSGI file: (ya configurado)

**Virtualenv**:
- Path: `/home/tu-usuario/.virtualenvs/puddle-env`

**Static files**:
- URL: `/static/`
- Directory: `/home/tu-usuario/puddle/staticfiles`

- URL: `/media/`
- Directory: `/home/tu-usuario/puddle/media`

### Paso 8: Reload

Click **Reload** en la Web tab

Acceder a: `https://tu-usuario.pythonanywhere.com`

### Actualizar Código

```bash
cd ~/puddle
git pull
python manage.py migrate
python manage.py collectstatic --noinput
# Click Reload en Web tab
```

---

## Heroku

### Paso 1: Preparar Proyecto

**Instalar dependencias adicionales**:

```bash
pip install gunicorn whitenoise dj-database-url psycopg2-binary
pip freeze > requirements.txt
```

**Crear `Procfile`**:

```
web: gunicorn puddle.wsgi --log-file -
```

**Crear `runtime.txt`**:

```
python-3.10.12
```

**Actualizar `settings.py`**:

```python
import dj_database_url

# Whitenoise para archivos estáticos
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Agregar
    # ... resto
]

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL')
    )
}

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Paso 2: Crear App en Heroku

```bash
# Instalar Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

heroku login
heroku create puddle-marketplace
```

### Paso 3: Agregar PostgreSQL

```bash
heroku addons:create heroku-postgresql:mini
```

### Paso 4: Configurar Variables de Entorno

```bash
heroku config:set SECRET_KEY="tu-secret-key-generada"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="puddle-marketplace.herokuapp.com"
heroku config:set EMAIL_HOST_USER="tu_email@gmail.com"
heroku config:set EMAIL_HOST_PASSWORD="tu_app_password"
```

### Paso 5: Deploy

```bash
git add .
git commit -m "Preparar para Heroku"
git push heroku main
```

### Paso 6: Migraciones

```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
heroku run python manage.py collectstatic --noinput
```

### Paso 7: Abrir App

```bash
heroku open
```

### Logs y Debugging

```bash
heroku logs --tail
heroku run python manage.py shell
```

### Actualizar

```bash
git push heroku main
```

---

## DigitalOcean

### Paso 1: Crear Droplet

1. Crear cuenta en DigitalOcean
2. Crear Droplet:
   - Ubuntu 22.04 LTS
   - Plan: Basic ($6/mes)
   - Datacenter: Más cercano
   - SSH Key o Password

### Paso 2: Conectar via SSH

```bash
ssh root@tu-ip-droplet
```

### Paso 3: Actualizar Sistema

```bash
apt update
apt upgrade -y
```

### Paso 4: Instalar Dependencias

```bash
# Python y pip
apt install python3-pip python3-dev python3-venv -y

# Nginx
apt install nginx -y

# MySQL
apt install mysql-server libmysqlclient-dev -y

# Supervisor (para gestionar procesos)
apt install supervisor -y
```

### Paso 5: Configurar MySQL

```bash
mysql_secure_installation

# Crear base de datos
mysql -u root -p
```

```sql
CREATE DATABASE puddle CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'puddle_user'@'localhost' IDENTIFIED BY 'password_seguro';
GRANT ALL PRIVILEGES ON puddle.* TO 'puddle_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Paso 6: Crear Usuario para la App

```bash
adduser puddle
usermod -aG sudo puddle
su - puddle
```

### Paso 7: Clonar Proyecto

```bash
cd ~
git clone https://github.com/tu-usuario/puddle.git
cd puddle
```

### Paso 8: Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### Paso 9: Configurar Variables de Entorno

```bash
nano .env
```

```env
DB_NAME=puddle
DB_USER=puddle_user
DB_PASSWORD=password_seguro
DB_HOST=localhost
DB_PORT=3306

SECRET_KEY=tu-secret-key
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com,tu-ip

EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
```

### Paso 10: Migraciones

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

### Paso 11: Configurar Gunicorn

```bash
sudo nano /etc/supervisor/conf.d/puddle.conf
```

```ini
[program:puddle]
command=/home/puddle/puddle/venv/bin/gunicorn --workers 3 --bind unix:/home/puddle/puddle/puddle.sock puddle.wsgi:application
directory=/home/puddle/puddle
user=puddle
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/puddle/puddle/logs/gunicorn.log
```

```bash
mkdir -p /home/puddle/puddle/logs
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status puddle
```

### Paso 12: Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/puddle
```

```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/puddle/puddle/staticfiles/;
    }
    
    location /media/ {
        alias /home/puddle/puddle/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/puddle/puddle/puddle.sock;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/puddle /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Paso 13: Configurar Firewall

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

### Paso 14: SSL con Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com
```

### Actualizar Código

```bash
cd ~/puddle
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart puddle
```

---

## AWS EC2

### Paso 1: Lanzar Instancia

1. Ir a AWS Console → EC2
2. Launch Instance:
   - AMI: Ubuntu Server 22.04 LTS
   - Instance Type: t2.micro (Free Tier)
   - Key Pair: Crear o usar existente
   - Security Group:
     - SSH (22) - Tu IP
     - HTTP (80) - Anywhere
     - HTTPS (443) - Anywhere

### Paso 2: Conectar

```bash
chmod 400 tu-key.pem
ssh -i tu-key.pem ubuntu@tu-ip-ec2
```

### Paso 3: Seguir Pasos de DigitalOcean

Los pasos son similares a DigitalOcean desde el Paso 3 en adelante.

### Paso 4: RDS para Base de Datos (Opcional)

1. Crear RDS MySQL instance
2. Configurar Security Group
3. Usar endpoint de RDS en `.env`

---

## Docker

### Dockerfile

```dockerfile
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias del sistema
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código
COPY . .

# Archivos estáticos
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "puddle.wsgi:application"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: puddle
      MYSQL_USER: puddle_user
      MYSQL_PASSWORD: puddle_pass
      MYSQL_ROOT_PASSWORD: root_pass
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"

  web:
    build: .
    command: gunicorn puddle.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
    depends_on:
      - web

volumes:
  mysql_data:
  static_volume:
  media_volume:
```

### Comandos Docker

```bash
# Build
docker-compose build

# Iniciar
docker-compose up -d

# Migraciones
docker-compose exec web python manage.py migrate

# Crear superuser
docker-compose exec web python manage.py createsuperuser

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

---

## Configuración Post-Despliegue

### 1. Verificar Funcionalidad

- [ ] Página principal carga
- [ ] Login funciona
- [ ] Registro funciona
- [ ] Crear item funciona
- [ ] Subir imagen funciona
- [ ] Conversaciones funcionan
- [ ] Email funciona
- [ ] Admin panel accesible

### 2. Configurar Backups

**MySQL Backup Script**:

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/puddle/backups"
DB_NAME="puddle"
DB_USER="puddle_user"
DB_PASS="password"

mkdir -p $BACKUP_DIR

mysqldump -u $DB_USER -p$DB_PASS $DB_NAME > $BACKUP_DIR/puddle_$DATE.sql

# Mantener solo últimos 7 días
find $BACKUP_DIR -name "puddle_*.sql" -mtime +7 -delete
```

**Cron Job**:

```bash
crontab -e

# Backup diario a las 2 AM
0 2 * * * /home/puddle/backup.sh
```

### 3. Monitoreo

**Instalar Sentry** (opcional):

```bash
pip install sentry-sdk
```

```python
# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="tu-sentry-dsn",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
)
```

### 4. Logs

```bash
# Ver logs de Nginx
sudo tail -f /var/log/nginx/error.log

# Ver logs de Gunicorn
tail -f /home/puddle/puddle/logs/gunicorn.log

# Ver logs de Django
tail -f /home/puddle/puddle/logs/django.log
```

---

## Troubleshooting

### Error: Static files no cargan

```bash
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

### Error: 502 Bad Gateway

```bash
# Verificar Gunicorn
sudo supervisorctl status puddle
sudo supervisorctl restart puddle

# Verificar socket
ls -la /home/puddle/puddle/puddle.sock
```

### Error: Database connection failed

```bash
# Verificar MySQL
sudo systemctl status mysql

# Probar conexión
mysql -u puddle_user -p puddle
```

### Error: Permission denied en media/

```bash
sudo chown -R puddle:www-data /home/puddle/puddle/media
sudo chmod -R 775 /home/puddle/puddle/media
```

### Error: CSRF verification failed

Verificar en `settings.py`:
```python
CSRF_TRUSTED_ORIGINS = [
    'https://tu-dominio.com',
    'https://www.tu-dominio.com',
]
```

---

## Checklist Final

- [ ] HTTPS habilitado
- [ ] DEBUG = False
- [ ] SECRET_KEY única
- [ ] Backups configurados
- [ ] Firewall configurado
- [ ] Logs funcionando
- [ ] Email funcionando
- [ ] Dominio apuntando correctamente
- [ ] SSL certificate válido
- [ ] Monitoreo configurado

---

**¡Felicidades! Tu aplicación está en producción 🎉**
